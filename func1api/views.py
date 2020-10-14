from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, LocationMessage
from module1 import func

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                #如果用戶發送文件為訊息文件，回傳函數
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '@使用說明':
                        func.sendText(event)
     
                    elif mtext == '@最新電影':
                        func.sendMovie(event)
    
                    elif mtext == '@頭條新聞':
                        func.sendNew(event)
    
                    elif mtext == '@抽':
                        func.sendBeautyImg(event)
                        
                    elif mtext == '@我已滿18歲':
                        func.sendSex(event)    
                    
                    elif mtext == "@是否已滿十八歲":
                        func.sendAdultMenu(event)
    
                    elif mtext == '@我未滿18歲':
                        func.sendNO(event)
                    else:
                        mtext == mtext
                        func.sendOlmi(event)
                #如果用戶發送文件為位置訊息，回傳附近美食 
                if isinstance(event.message, LocationMessage):
                    func.sendRestaurant(event)
        return HttpResponse()

    else:
        return HttpResponseBadRequest()
