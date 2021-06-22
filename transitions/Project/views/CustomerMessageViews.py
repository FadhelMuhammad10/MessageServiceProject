from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from transitions.Project.helper.permission import IsAdmin, IsUser, IsCustomer, IsPermission
from transitions.Project.models import CustomerMessage, Template
from transitions.Project.serializers.CustomerMessageSerializers import CustomerMessageSendWhatsappCheckSerializer, \
    CustomerMessageSendSMSCheckSerializer, CustomerMessageSendWhatsapNoTemplateSerializer, \
    CustomerMessageSendSMSNoTemplateSerializer
from transitions.Project.services.MessageServices import SendMessageService

list_status_code = [401, 400]
MessageService = SendMessageService()

def web_page(request):
    print('entered web page')
    try:
        # return render(request,'http://127.0.0..1:3000')
        return redirect("http://127.0.0.1:3000")
    except Exception as e:
        print(str(e))

    # return render(request,'localhost:3000')
class CustomerMessageSendWhatsappView(viewsets.ModelViewSet):
    queryset = CustomerMessage.objects.all()
    serializer_class = CustomerMessageSendWhatsappCheckSerializer
    permission_classes = []
    def get_permissions(self):
        if self.action == 'post':
            self.permission_classes = []
        return [p() for p in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serialize = CustomerMessageSendWhatsappCheckSerializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
            # status_message = MessageService.send_whatsapp(req=serialize.validated_data)
            try:#start
                temp = Template.objects.get(type=serialize.validated_data['type_template'].type).templates
                temp = "\"" + temp + "\"%("
                for u in range(0, len(serialize.validated_data['text'])):
                    if u == 0:
                        temp = temp + "\"" + serialize.validated_data['text'][u] + "\""
                    else:
                        temp = temp + ",\"" + serialize.validated_data["text"][u] + "\""
                temp = temp + ")"
                print(eval(temp))
                serialize.validated_data['text'] = eval(temp)
            except Exception as e:
                return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
            # if status_message.status_code not in list_status_code:
            #     try:
            #         temp = Template.objects.get(type=serialize.validated_data['type_template'].type).templates
            #         temp = "\"" + temp + "\"%("
            #         for u in range(0, len(serialize.validated_data['text'])):
            #             if u == 0:
            #                 temp = temp + "\"" + serialize.validated_data['text'][u] + "\""
            #             else:
            #                 temp = temp + ",\"" + serialize.validated_data["text"][u] + "\""
            #         temp = temp + ")"
            #         print(eval(temp))
            #         serialize.validated_data['text'] = eval(temp)
            #     except Exception as e:
            #         return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            #     serialize.save()
            #     return Response(serialize.data, status=status.HTTP_201_CREATED)
            # else:
            #     return Response({"Message": "error message"}, status=status_message.status_code)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response({"mes": self.get_object().id}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CustomerMessageSendSMSView(viewsets.ModelViewSet):
    queryset = CustomerMessage.objects.all()
    serializer_class = CustomerMessageSendSMSCheckSerializer
    permission_classes = []

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = []
        elif self.action == "create":
            self.permission_classes = []

        return [p() for p in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serial = CustomerMessageSendSMSCheckSerializer(data=request.data)
        if serial.is_valid(raise_exception=True):
            try:
                par = "\"" + Template.objects.get(type=serial.validated_data['type_template'].type).templates + "\""
                template = par + "%("
                for p in range(0, len(serial.validated_data['text'])):
                    if p == 0:
                        template = template + "\"" + serial.validated_data['text'][p] + "\""
                    else:
                        template = template + ",\"" + serial.validated_data['text'][p] + "\""
                template = template + ")"
                serial.validated_data["text"] = eval(template)
            except Exception as e:
                test = str(e)
                if test == "not all arguments converted during string formatting":
                    return Response({"Message": "parameter berlebihan"}, status=status.HTTP_400_BAD_REQUEST)
                elif test == "not enough arguments for format string":
                    return Response({"Message": "param tidak cukup"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            serial.save()#start
            return Response(serial.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        #     status_message = MessageService.send_message(serial.validated_data)
        #     if status_message.status_code not in list_status_code:
        #         serial.save()
        #         return Response(serial.data, status=status.HTTP_201_CREATED)
        #     else:
        #         return Response({"Message": "Error Message"}, status=status_message.status_code)
        # return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response({"mes": self.get_object().id}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CustomerMessageSendWhatsappNoTemplateView(viewsets.ModelViewSet):
    queryset = CustomerMessage.objects.all()
    serializer_class = CustomerMessageSendWhatsapNoTemplateSerializer
    permission_classes = [IsAdmin, IsUser]

    def create(self, request, *args, **kwargs):
        serializer = CustomerMessageSendWhatsapNoTemplateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            status_message = MessageService.send_whatsapp_text(val=serializer.validated_data)
            serializer.save()#start
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
            # if status_message.status_code == "success":
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     else:
        #         print(status_message.status_code)
        #         return Response({"Message": "message"}, status=status_message.status_code)
        # return Response(status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == "list":
            print(self.permission_classes)
            print("done done")
            self.permission_classes = [self.permission_classes[0]]
            print(self.permission_classes)
        return [p() for p in self.permission_classes]

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response({"mes": self.get_object().id}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CustomerMessageSendSMSNoTemplateView(viewsets.ModelViewSet):
    queryset = CustomerMessage.objects.all()
    serializer_class = CustomerMessageSendSMSNoTemplateSerializer

    def create(self, request, *args, **kwargs):
        serializer = CustomerMessageSendSMSNoTemplateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            status_message = MessageService.send_message(req=serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        #     if status_message.status_code not in list_status_code:
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     else:
        #         return Response({"Message": "Error Message"}, status=status_message.status_code)
        # return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response({"mes": self.get_object().id}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
