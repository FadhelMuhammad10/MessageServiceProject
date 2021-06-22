import django_filters
from exchangelib import Message, Account, DELEGATE, Mailbox, FileAttachment, Configuration, Credentials, HTMLBody
from rest_framework import status, viewsets
from rest_framework.response import Response

from transitions.Project.helper.permission import IsCustomer
from transitions.Project.models import CustomerEmail
from transitions.Project.serializers.CustomerEmailSerializers import CustomerEmailSendEmailGeneralSerializer
from transitions.settings import IMAP_USER, IMAP_PASSWORD, IMAP_SERVER, SMTP_ADDRESS

list_status_code = [401, 400]
class CustomerEmailSendemailView(viewsets.ModelViewSet):
    queryset = CustomerEmail.objects.all()
    serializer_class = CustomerEmailSendEmailGeneralSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = CustomerEmailSendEmailGeneralSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            to_recepient = [Mailbox(email_address=P) for P in serializer.validated_data['email']]
            cc_recipient = [Mailbox(email_address=xx) for xx in serializer.validated_data['cc']]
            body = serializer.validated_data["body"]
            if serializer.validated_data["body_type"] == "html":
                body = HTMLBody(serializer.validated_data["body_type"])
            email = IMAP_USER
            password = IMAP_PASSWORD
            a = Credentials(username=email, password=password)
            config = Configuration(server=IMAP_SERVER, credentials=a)
            akun = Account(primary_smtp_address=SMTP_ADDRESS, config=config, access_type=DELEGATE, autodiscover=True)
            m = Message(account=akun, folder=akun.sent, subject=serializer.validated_data["subject"], body=body,
                        to_recipients=to_recepient, cc_recipients=cc_recipient)
            try:
                for f in serializer.validated_data['attachments']:
                    print(f['filename'])
                    r = FileAttachment(name=f['filename'], content=f['filebase64'])
                    m.attach(r)
            except Exception as e:
                return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            stats = m.send_and_save()
            if stats.status_code not in list_status_code:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=stats.status_code)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsCustomer]
        return [p() for p in self.permission_classes]

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response({"mes": self.get_object().id}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
