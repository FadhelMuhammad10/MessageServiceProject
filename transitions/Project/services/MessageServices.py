import requests as requests

from transitions.settings import URL_MESSAGE, URL_WHATSAPP, TOKEN_WHATSAPP, USERKEY, PASSKEY


class SendMessageService:
    def send_message(self, req):
        url = URL_MESSAGE
        dataQ = {
            "userkey": USERKEY,
            "passkey": PASSKEY,
            "nohp": req['phone_number'],
            "pesan": req['text']
        }
        response = requests.post(url=url, json=dataQ)
        return response

    def send_whatsapp(self, req):
        url = URL_WHATSAPP + "sendhsm" + "/" + req['type_template'].templates
        dataQ = {
            "token": TOKEN_WHATSAPP,
            "to": req['phone_number'],
            "param": [P for P in req['text']]
        }
        response = requests.post(url=url, json=dataQ)
        return response

    def send_whatsapp_text(self, val):
        url = URL_WHATSAPP + "sendText"
        dataQ = {
            "token": TOKEN_WHATSAPP,
            "to": val['phone_number'],
            "message": val['text']
        }
        response = requests.post(url=url, json=dataQ)
        return response
