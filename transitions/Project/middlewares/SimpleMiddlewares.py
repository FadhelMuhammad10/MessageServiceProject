from datetime import datetime

from django.utils.deprecation import MiddlewareMixin

from transitions.Project.models import Log

list_status_code = [401, 400, 404, 403]
list_url = ['/api/sendsms/', '/api/sendwhatsapp/', '/api/sendemail/', '/api/sendsmsnotemplate/',
            '/api/sendwhatsappnotemplate/']


class SimpleLogMiddleware(MiddlewareMixin):
    bod = None
    req_date = None

    def process_request(self, request):
        self.req_date = datetime.now()
        # a,b,c,d=request
        # print(a,b,c,d)
        # print(request.url)
        # print(request.status)
        request.body

    def process_exception(self, request, exception):
        print('==============================================')
        print("Entered Exception funtion in simple middleware")
        print(exception)
        return exception

    def process_response(self, request, response):
        if request.method == 'POST' and request.META['PATH_INFO'] in list_url and response.status_code not in list_status_code:
            requ = request.body.decode("utf-8")
            requ = eval(requ)
            Log.objects.create(ip=request.META['REMOTE_ADDR'], path=request.META['PATH_INFO'],
                               request_body=requ,response_body=response.data, request_date=self.req_date, response_date=datetime.now())
        return response