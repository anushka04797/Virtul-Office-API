import requests

class SmsGateway():
    def post(request):
        url = "http://103.123.8.69:8080/send/sms"
        
        r = requests.post(url, request)
        # print(r)
        if (r.status_code == 200):
            print("Successfully sent to pisci!!")
        else:
            print("Unsuccessful sending to pisci!!")