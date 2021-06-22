import uuid

from django.db import models

from transitions.Project.custom_fields.fields.MultiEmailFields import MultiEmailField


class CustomerMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    phone_number = models.CharField(max_length=15)
    text = models.TextField()
    type_template = models.ForeignKey(to='Template', db_column='type_template', on_delete=models.SET_NULL,
                                      null=True, blank=True, default=None)
    kind = models.CharField(max_length=20)

    class Meta:
        db_table = "customer_message"
        permissions = (("can_add_customer_message", "Can add customer message"),
                       ("can_view_customer_message", "Can view customer message"),
                       ("can_change_customer_message", "Can change customer message"),
                       ("can_delete_customer_message", "Can delete customer message"),)


class CustomerEmail(models.Model):
    type = (("text", "text"),
            ("html", "html"))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    cc = MultiEmailField(null=True, blank=True, default=None)
    email = MultiEmailField(null=False, blank=False)
    subject = models.CharField(max_length=50)
    body = models.TextField()
    body_type = models.CharField(max_length=10, choices=type, default="text")

    class Meta:
        db_table = "customer_email"
        permissions = (("can_add_customer_email", "Can add customer email"),
                       ("can_view_customer_email", "Can view customer email"),
                       ("can_change_customer_email", "Can change customer email"),
                       ("can_delete_customer_email", "Can delete customer email"),)


class Template(models.Model):
    type = models.CharField(max_length=20, primary_key=True)
    templates = models.TextField()

    class Meta:
        db_table = "template"
        permissions = (("can_add_customer_template", "Can add customer template"),
                       ("can_view_customer_template", "Can view customer template"),
                       ("can_change_customer_template", "Can change customer template"),
                       ("can_delete_customer_template", "Can delete customer template"),)


class Log(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    path = models.CharField(max_length=10, db_column='path')
    request_body = models.CharField(max_length=100)
    response_body = models.CharField(max_length=100)
    ip = models.CharField(max_length=20, db_column="ip")
    request_date = models.DateTimeField()
    response_date = models.DateTimeField()

    class Meta:
        db_table = "log"
