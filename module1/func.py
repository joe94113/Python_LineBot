#DJANGO套件===================================================================================
from django.conf import settings

#爬蟲請求====================================================================================
import requests
import time
import re
import random
from hashlib import md5
from bs4 import BeautifulSoup

#LINEAPI=========================================================================================
from linebot import LineBotApi
from linebot.models import TemplateSendMessage, CarouselTemplate, CarouselColumn,URITemplateAction, TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def sendRestaurant(event): #傳送附近餐廳
    #地址        
    #userAddress = event.message.address
    #緯度
    latitude = event.message.latitude
    #經度
    longitude = event.message.longitude
        
    #googlePlace_url = "https://www.google.com.tw/maps/place/"
        
    google_apikey = "&key="+"你的api"
        
    Nearby_search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(latitude)+ ',' + str(longitude) +" &radius=1500&type=restaurant" + google_apikey

    pictureApi = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&photoreference='
            
    restaurantData = requests.get(Nearby_search_url).json()
        
    allRestaurantList = list()
    for item in restaurantData['results'][0:5]:
            RestaurantList = list()
            #名子0
            RestaurantList.append(item['name'])
            #地址1
            RestaurantList.append(item['vicinity'])
            #緯度2
            RestaurantList.append(str(item['geometry']['location']['lat']))
            #經度3
            RestaurantList.append(str(item['geometry']['location']['lng']))
            #評價4
            RestaurantList.append(str(item['rating']))
            #是否營業5
            RestaurantList.append(str(item['opening_hours']['open_now']))
            #總留言數6
            RestaurantList.append(str(item['user_ratings_total']))
            #相片網址7
            RestaurantList.append(pictureApi + item['photos'][0]['photo_reference'] + google_apikey)
            allRestaurantList.append(RestaurantList)
    try:
        message = TemplateSendMessage(
            alt_text = "餐廳多頁訊息",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url = allRestaurantList[0][7],
                        title= "餐廳:" + allRestaurantList[0][0],
                        text= "Google評價:" + allRestaurantList[0][4] + "\n營業中:" + allRestaurantList[0][5] + "\n總評論數" + allRestaurantList[0][6],
                        actions=[
                            
                            URITemplateAction(
                                label='出發',
                                uri = "https://www.google.com/maps/search/?api=1&query=" + allRestaurantList[0][2]+","+ allRestaurantList[0][3] 
                            ),
                            
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url = allRestaurantList[1][7],
                        title="餐廳:" + allRestaurantList[1][0],
                        text="Google評價:" + allRestaurantList[1][4] + "\n營業中:" + allRestaurantList[1][5] + "\n總評論數" + allRestaurantList[1][6],
                        actions=[
                        
                            URITemplateAction(
                                label='出發',
                                uri = "https://www.google.com/maps/search/?api=1&query=" + allRestaurantList[1][2]+","+ allRestaurantList[1][3]
                            ),
                           
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=allRestaurantList[2][7],
                        title="餐廳:" + allRestaurantList[2][0],
                        text="Google評價:" + allRestaurantList[2][4] + "\n營業中:" + allRestaurantList[2][5] + "\n總評論數" + allRestaurantList[2][6],
                        actions=[
                            URITemplateAction(
                                label='出發',
                                uri="https://www.google.com/maps/search/?api=1&query=" + allRestaurantList[2][2]+","+ allRestaurantList[2][3]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=allRestaurantList[3][7],
                        title="餐廳:" + allRestaurantList[3][0],
                        text="Google評價:" + allRestaurantList[3][4] + "\n營業中:" + allRestaurantList[3][5] + "\n總評論數" + allRestaurantList[3][6],
                        actions=[
                            URITemplateAction(
                                label='出發',
                                uri="https://www.google.com/maps/search/?api=1&query=" + allRestaurantList[3][2]+","+ allRestaurantList[3][3]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=allRestaurantList[4][7],
                        title="餐廳:" + allRestaurantList[4][0],
                        text="Google評價:" + allRestaurantList[4][4] + "\n營業中:" + allRestaurantList[4][5] + "\n總評論數" + allRestaurantList[4][6],
                        actions=[
                            URITemplateAction(
                                label='出發',
                                uri="https://www.google.com/maps/search/?api=1&query=" + allRestaurantList[4][2]+","+ allRestaurantList[4][3]
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='挖勒發生錯誤！\n聯絡我感恩!'))
#==============================================================================
#使用歐拉密api取得文本回應,數字加減計算,kkbox音樂點播,天氣回應
def sendOlmi(event): #傳送文字跟音樂
    #使用URL請求api
    inputtext=event.message.text
    apiBaseUrl = 'https://tw.olami.ai/cloudservice/api'
    appKey = '你的api ker'
    appSecret = '你的app secret'
    api='nli'
    cusid='keaidigou'
        
    timestamp_ms = (int(time.time() * 1000))
        
    data = appSecret + 'api=' + api + 'appkey=' + appKey + 'timestamp=' + \
               str(timestamp_ms) + appSecret
    sign= md5(data.encode('ascii')).hexdigest()
        
    params = {'appkey': appKey,
                  'api': api,
                  'timestamp': timestamp_ms,
                  'sign': sign,
                  'rq': inputtext}
    if cusid is not None:
        params.update(cusid=cusid)
    params1=params
    '''    
    header={
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
    '''
    url="%s?appkey=%s&api=%s&timestamp=%s&sign=%s&rq={'data':{'input_type':1,'text':'%s'},'data_type':'stt'}&cusid=%s"
    furl=url%(apiBaseUrl,params1['appkey'],params1['api'],params1['timestamp'],params1['sign'],params1['rq'],params1['cusid'])
    res = requests.get(furl).json()
    try:
        #傳送kkbox多頁訊息
        if res['data']['nli'][0]['desc_obj']['result'] == "馬上為你播放。":
            message = TemplateSendMessage(
                alt_text = "KKBOX多頁訊息",
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url = res['data']['nli'][0]['data_obj'][0]['photo'][1]['url'],
                            title= "為你點播:" + res['data']['nli'][0]['data_obj'][0]['title'],
                            text= "歌手:" + res['data']['nli'][0]['data_obj'][0]['artist'],
                            actions=[
                                
                                URITemplateAction(
                                    label='KKBOX聽歌去',
                                    uri = res['data']['nli'][0]['data_obj'][0]['url'] 
                                ),
                                
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = res['data']['nli'][0]['data_obj'][1]['photo'][1]['url'],
                            title="為你點播:" + res['data']['nli'][0]['data_obj'][1]['title'],
                            text="歌手:" + res['data']['nli'][0]['data_obj'][1]['artist'],
                            actions=[
                                URITemplateAction(
                                    label = 'KKBOX聽歌去',
                                    uri = res['data']['nli'][0]['data_obj'][1]['url']
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = res['data']['nli'][0]['data_obj'][2]['photo'][1]['url'],
                            title="為你點播:" + res['data']['nli'][0]['data_obj'][2]['title'],
                            text="歌手:" + res['data']['nli'][0]['data_obj'][2]['artist'],
                            actions=[
                                URITemplateAction(
                                    label = 'KKBOX聽歌去',
                                    uri = res['data']['nli'][0]['data_obj'][2]['url']
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = res['data']['nli'][0]['data_obj'][3]['photo'][1]['url'],
                            title="為你點播:" + res['data']['nli'][0]['data_obj'][3]['title'],
                            text="歌手:" + res['data']['nli'][0]['data_obj'][3]['artist'],
                            actions=[
                                URITemplateAction(
                                    label = 'KKBOX聽歌去',
                                    uri = res['data']['nli'][0]['data_obj'][3]['url']
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = res['data']['nli'][0]['data_obj'][4]['photo'][1]['url'],
                            title="為你點播:" + res['data']['nli'][0]['data_obj'][4]['title'],
                            text="歌手:" + res['data']['nli'][0]['data_obj'][4]['artist'],
                            actions=[
                                URITemplateAction(
                                    label = 'KKBOX聽歌去',
                                    uri = res['data']['nli'][0]['data_obj'][4]['url']
                                )
                            ]
                        ),
                    ]
                )
            )
        else:
            #否，則傳送文本
            message = TextSendMessage(  
                text = res['data']['nli'][0]['desc_obj']['result']
            )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！\n聯絡我感恩!'))
#===============================================================================
#取得電影日期函數
def get_date(date_str):
    # e.g. "上映日期：2017-03-23" -> match.group(0): "2017-03-23"
    pattern = '\d+-\d+-\d+'
    match = re.search(pattern, date_str)
    if match is None:
        return date_str
    else:
        return match.group(0)      
    
def sendMovie(event): #傳送電影
    Yahoo_MOVIE_URL = 'https://tw.movies.yahoo.com/movie_thisweek.html'

    # 以下網址後面加上 "/id=MOVIE_ID" 即為該影片各項資訊
    Yahoo_INTRO_URL = 'https://tw.movies.yahoo.com/movieinfo_main.html'  # 詳細資訊
    Yahoo_PHOTO_URL = 'https://tw.movies.yahoo.com/movieinfo_photos.html'  # 劇照
    Yahoo_TIME_URL = 'https://tw.movies.yahoo.com/movietime_result.html'  # 時刻表
    
    resp = requests.get(Yahoo_MOVIE_URL)
    
    try:
        if resp.status_code != 200:
            message = TextSendMessage(
                text = "網站改版拉告知我!!!"
                )
        else:
            dom = resp.text
            soup = BeautifulSoup(dom, 'html5lib')
            movies = list()
            rows = soup.find_all('div', 'release_info_text')
            for row in rows[0:5]:
                movie = list()
                #評價0
                movie.append(row.find('div', 'leveltext').span.text.strip())
                #片名1
                movie.append(row.find('div', 'release_movie_name').a.text.strip())
                #電影照片2
                movie.append(row.parent.find_previous_sibling('div', 'release_foto').a.img['src'])
                #上映日期3
                movie.append(get_date(row.find('div', 'release_movie_time').text))
                
                trailer_a = row.find_next_sibling('div', 'release_btn color_btnbox').find_all('a')[1]
                #電影網址4
                movie.append(trailer_a['href'] if 'href' in trailer_a.attrs.keys() else '')
                
                movies.append(movie)
            message = TemplateSendMessage(
                alt_text = "電影多頁訊息",
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url = movies[0][2],
                            title= "片名:" + movies[0][1],
                            text= "網友期待度:" + movies[0][0] + "\n\n上映日期:" + movies[0][3],
                            actions=[
                                
                                URITemplateAction(
                                    label='電影預告',
                                    uri = movies[0][4] 
                                ),
                                
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = movies[1][2],
                            title="片名:" + movies[1][1],
                            text="網友期待度:" +  movies[1][0] + "\n\n上映日期:" + movies[1][3],
                            actions=[
                                URITemplateAction(
                                    label = '電影預告',
                                    uri = movies[1][4]
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = movies[2][2],
                            title="片名:" + movies[2][1],
                            text="網友期待度:" +  movies[2][0] + "\n\n上映日期:" + movies[2][3],
                            actions=[
                                URITemplateAction(
                                    label = '電影預告',
                                    uri = movies[2][4]
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = movies[3][2],
                            title="片名:" + movies[3][1],
                            text="網友期待度:" +  movies[3][0] + "\n\n上映日期:" + movies[3][3],
                            actions=[
                                URITemplateAction(
                                    label = '電影預告',
                                    uri = movies[3][4]
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = movies[4][2],
                            title="片名:" + movies[4][1],
                            text="網友期待度:" +  movies[4][0] + "\n\n上映日期:" + movies[4][3],
                            actions=[
                                URITemplateAction(
                                    label = '電影預告',
                                    uri = movies[4][4]
                                )
                            ]
                        ),
                        
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！\n聯絡我感恩!'))        

#=================================================================================
def sendText(event):  #使用說明
    try:
        message = [
            TextSendMessage(  
            text = "主人您好\n\n輸入【播放音樂】【來點音樂】，給您隨機五首歌曲選擇\n\n" +
            "輸入【XX天氣】 播報縣市或區域天氣\n\n" +
            "點選 + 選擇【傳送位置訊息】，給予附近五家餐廳做參考\n\n" +
            "您還可以詢問計算【15*2*3*(5*3-5)】以及時間問題【今天日期】\n\n" + 
            "此外還可以陪你聊天哦\n" +
            "開發者LineId:joe94113"
        ),
            StickerSendMessage(  #傳送貼圖
                package_id='1',  
                sticker_id='2'
            )
            ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！\n聯絡我感恩!'))

#==============================================================================
def sendNew(event):  #傳送聯合即時新聞
    udn_url = "https://udn.com"
    udn_new_url = "https://udn.com/news/breaknews/1"
    dom = requests.get(udn_new_url).text
    soup = BeautifulSoup(dom, 'html5lib')
    
    
    allnewlist = list()
    for new in soup.find_all('div',{"class":"story-list__news"})[0:6]:
        newlist = list()
        #大標題0
        newlist.append(new.find("div",'story-list__text').h2.text.strip())
        #內文1
        newlist.append(new.find("div",'story-list__text').p.text.strip())
        #新聞連結2
        newlist.append(udn_url + new.find("div",'story-list__text').h2.a['href'])
        #圖片連結3
        newlist.append(new.find("div","story-list__image").img['data-src'])
        allnewlist.append(newlist)
    
    try:
        message = TemplateSendMessage(
                alt_text = "新聞快訊",
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url = allnewlist[0][3],
                            title= allnewlist[0][0],
                            text= allnewlist[0][1][:50]+ "...",
                            actions=[
                                URITemplateAction(
                                    label='詳全文',
                                    uri = allnewlist[0][2] 
                                ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = allnewlist[1][3],
                            title= allnewlist[1][0],
                            text= allnewlist[1][1][:50] + "...",
                            actions=[
                                
                                URITemplateAction(
                                    label='詳全文',
                                    uri = allnewlist[1][2] 
                                ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = allnewlist[2][3],
                            title= allnewlist[2][0],
                            text= allnewlist[2][1][:50] + "...",
                            actions=[
                                
                                URITemplateAction(
                                    label='詳全文',
                                    uri = allnewlist[2][2] 
                                ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = allnewlist[3][3],
                            title= allnewlist[3][0],
                            text= allnewlist[3][1][:50] + "...",
                            actions=[
                                
                                URITemplateAction(
                                    label='詳全文',
                                    uri = allnewlist[3][2] 
                                ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = allnewlist[4][3],
                            title= allnewlist[4][0],
                            text= allnewlist[4][1][:50] + "...",
                            actions=[
                                
                                URITemplateAction(
                                    label='詳全文',
                                    uri = allnewlist[4][2] 
                                ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = allnewlist[5][3],
                            title= allnewlist[5][0],
                            text= allnewlist[5][1][:50] + "...",
                            actions=[
                                
                                URITemplateAction(
                                    label='詳全文',
                                    uri = allnewlist[5][2] 
                                ),
                            ]
                        ),
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！\n聯絡我感恩!'))

#=======================================================================
def get_web_page(url):#取得網頁
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        return None
    else:
        return resp.text

def get_articles(dom):#取得當頁有超連結文章
    soup = BeautifulSoup(dom, 'html5lib')

    articles = list()  # 儲存取得的文章資料
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
            # 取得文章連結及標題
            if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                href = d.find('a')['href']
                articles.append(href)
    return articles

def sendBeautyImg(event):  #傳送表特版美女或恐龍圖
    PTT_URL = 'https://www.ptt.cc'
    
    current_page = get_web_page(PTT_URL + '/bbs/Beauty/index.html')
    
    articles = get_articles(current_page)
    
    imgs = list()
    
    for article in articles:
        page = get_web_page(PTT_URL + article)
        soup = BeautifulSoup(page, 'html.parser')
        links = soup.find(id='main-content').find_all('a')
        img_urls = list()
        for link in links:#正規搜尋法尋找圖片網址
            if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
                img_urls.append(link['href'])
                imgs.append(img_urls)
        
    #一維陣列亂數
    imgs_One_dimensionalSum = int(len(imgs))
    One_dimensionalRandom = random.randint(0,imgs_One_dimensionalSum-1)
    #二維陣列亂數
    imgs_Two_dimensionalSum = int(len(imgs[One_dimensionalRandom]))
    Two_dimensionalRandom = random.randint(0,imgs_Two_dimensionalSum-1)
    try:
        message = ImageSendMessage(  #傳送圖片
            original_content_url = imgs[One_dimensionalRandom][Two_dimensionalRandom],
            preview_image_url = imgs[One_dimensionalRandom][Two_dimensionalRandom]
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！\n聯絡我感恩!'))

#=========================================================================================

def sendSex(event):#西斯版爬取
    Dcard_url = "https://www.dcard.tw"
    Dcard_sex_url = "https://www.dcard.tw/f/sex"
    
    resp = requests.get(
            url=Dcard_sex_url,
            cookies={'over18': '1'}
        ).text
    soup = BeautifulSoup(resp, 'html5lib')
    
    articles = list()  # 儲存取得的文章資料
    divs = soup.find_all('article', 'tgn9uw-0 bpyTee')
    for d in divs:
        # 取得文章連結及標題
        if d.find('img','sc-2rneb0-0 khMHQx tgn9uw-7 ksWRdc'):# 有超連結，表示文章有圖片
            article = list()
            #標題0
            article.append(d.find('h2').text)
            #文章網址1
            article.append(Dcard_url + d.a['href'])
            #文章縮圖2
            article.append(d.find('img','sc-2rneb0-0 khMHQx tgn9uw-7 ksWRdc')['src'])
            #文章內文3
            article.append(d.find('div','uj732l-0 eLjDMI').text.strip())
            articles.append(article)
    try:
        message = TemplateSendMessage(
                alt_text = "西斯熱門",
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url = articles[2][2],
                            title= articles[2][0],
                            text= articles[2][3][:45] + "...",
                            actions=[
                                URITemplateAction(
                                    label='詳全文',
                                    uri = articles[2][1] 
                                ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = articles[3][2],
                            title= articles[3][0],
                            text= articles[3][3][:45] + "...",
                            actions=[
                                URITemplateAction(
                                    label='詳全文',
                                    uri = articles[3][1] 
                                ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = articles[5][2],
                            title= articles[5][0],
                            text= articles[5][3][:45] + "...",
                            actions=[
                                URITemplateAction(
                                    label='詳全文',
                                    uri = articles[5][1] 
                                ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = articles[6][2],
                            title= articles[6][0],
                            text= articles[6][3][:45] + "...",
                            actions=[
                                URITemplateAction(
                                    label='詳全文',
                                    uri = articles[6][1] 
                                ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = articles[8][2],
                            title= articles[8][0],
                            text= articles[8][3][:45] + "...",
                            actions=[
                                URITemplateAction(
                                    label='詳全文',
                                    uri = articles[8][1] 
                                ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = articles[10][2],
                            title= articles[10][0],
                            text= articles[10][3][:45] + "...",
                            actions=[
                                URITemplateAction(
                                    label='詳全文',
                                    uri = articles[10][1] 
                                ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = articles[11][2],
                            title= articles[11][0],
                            text= articles[11][3][:45] + "...",
                            actions=[
                                URITemplateAction(
                                    label='詳全文',
                                    uri = articles[11][1] 
                                ),
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url = articles[12][2],
                            title= articles[12][0],
                            text= articles[12][3][:45] + "...",
                            actions=[
                                URITemplateAction(
                                    label='詳全文',
                                    uri = articles[12][1] 
                                ),
                            ]
                        ),
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！\n聯絡我感恩!'))
#==============================================================================================
def sendAdultMenu(event):  #成人選單
    try:
        message = TextSendMessage(
            text='未滿18歲請勿食用!',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="我已滿18歲", text="@我已滿18歲")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="我未滿18歲", text="@我未滿18歲")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！\n聯絡我感恩!'))
#================================================================================================        
def sendNO(event):
    try:
        message = [
            TextSendMessage(  
            text = "兄弟沒事的"
        ),
            ImageSendMessage(  #傳送圖片
            original_content_url = "https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1593800913533.jpg",
            preview_image_url = "https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1593800913533.jpg"
        )
            ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！\n聯絡我感恩!'))
    
        
        
