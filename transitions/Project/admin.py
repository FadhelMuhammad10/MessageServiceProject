import operator
from functools import reduce

from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.utils import lookup_needs_distinct
from django.db import models
from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db.models.constants import LOOKUP_SEP
from django.utils.http import urlencode

from transitions.Project.models import CustomerMessage, Template, CustomerEmail, Log

@admin.register(CustomerMessage)
class AdminCustomer(admin.ModelAdmin):
    list_display = ('id','kind','phone_number')
    def has_add_permission(self, request):
        return False
    # def has_delete_permission(self, request, obj=None):
    #     return False
    def has_change_permission(self, request, obj=None):
        return False
@admin.register(Template)
class AdminTemplate(admin.ModelAdmin):
    list_display = ['type','templates','jumlah']
    def jumlah(self,obj):
        x = CustomerMessage.objects.filter(type_template=obj.type)
        return len(x)
    jumlah.short_description = "total"
    def has_change_permission(self, request, obj=None):
        return False
    # def has_add_permission(self, request):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False
@admin.register(CustomerEmail)
class AdminEmailList(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
class Admin_Log_Template_Filter(admin.SimpleListFilter):
    title = "template"
    parameter_name = "page"
    def lookups(self, request, model_admin):
        temp = Template.objects.all()
        tee=[]
        for t in temp:
            tee.append((str(t.type),str(t.type)))
        return tee
    def queryset(self, request, queryset):
        print('===========')
        print('entered filter admin')
        # print(queryset)
        print(self.value())
        try:
            return Log.objects.filter(request_body__icontains=self.value())
        except:
            pass
@admin.register(Log)
class AdminLog(admin.ModelAdmin):
    search_fields = ['path','id']
    list_filter = ['path',Admin_Log_Template_Filter]
    list_display =  ['id','path','customer_id', 'template','number_phone']
    def number_phone(self,obj):
        return eval(obj.request_body)['phone_number']
    number_phone.short_description = 'number'
    def get_preserved_filters(self, request):
        """
        Return the preserved filters querystring.
        """
        match = request.resolver_match
        if self.preserve_filters and match:
            opts = self.model._meta
            current_url = '%s:%s' % (match.app_name, match.url_name)
            changelist_url = 'admin:%s_%s_changelist' % (opts.app_label, opts.model_name)
            if current_url == changelist_url:
                preserved_filters = request.GET.urlencode()
            else:
                preserved_filters = request.GET.get('_changelist_filters')
            if preserved_filters:
                return urlencode({'_changelist_filters': preserved_filters})
        return ''
    def get_search_results(self, request, queryset, search_term):
        """
        Return a tuple containing a queryset to implement the search
        and a boolean indicating if the results may contain duplicates.
        """

        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            # Use field_name if it includes a lookup.
            opts = queryset.model._meta
            lookup_fields = field_name.split(LOOKUP_SEP)
            # Go through the fields, following all relations.
            prev_field = None
            for path_part in lookup_fields:
                if path_part == 'pk':
                    path_part = opts.pk.name
                try:
                    field = opts.get_field(path_part)
                except FieldDoesNotExist:
                    # Use valid query lookups.
                    if prev_field and prev_field.get_lookup(path_part):
                        return field_name
                else:
                    prev_field = field
                    if hasattr(field, 'get_path_info'):
                        # Update opts to follow the relation.
                        opts = field.get_path_info()[-1].to_opts
            # Otherwise, use the field with icontains.
            return "%s__icontains" % field_name

        use_distinct = False
        search_fields = self.get_search_fields(request)
        if search_fields and search_term:
            if queryset.filter(response_body__icontains=search_term):
                return queryset.filter(response_body__icontains=search_term), False
            if queryset.filter(request_body__icontains=search_term):
                return queryset.filter(request_body__icontains=search_term), False
            orm_lookups = [construct_search(str(search_field))
                            for search_field in search_fields]
            for bit in search_term.split():
                or_queries = [models.Q(**{orm_lookup: bit})
                              for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
            use_distinct |= any(lookup_needs_distinct(self.opts, search_spec) for search_spec in orm_lookups)
        return queryset, use_distinct
    def customer_id(self,obj):
        return eval(obj.response_body)['id']
    customer_id.short_description = 'customer_id'
    def template(self,obj):
        return eval(obj.request_body)['type_template']
    def upper_case_name(self, obj):
        return 1
    upper_case_name.short_description = 'Name'
    def has_add_permission(self, request):
        return False
