import datetime
import requests
import json
from jsonpath import jsonpath
import time
import random
import hmac
from hashlib import sha1
import random


def create_activity(data):
    env = data["env"]
    headers = data["headers"]
    body = data["body"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/activity/%s"%(env,sales_id)
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    response = requests.post(url,headers=headers,json=body)
    print(response.json())
    if response.status_code==200:
        activity_id = response.json()["data"]
        return activity_id
    else:
        return response

def delate_activity(data):
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    url = "%s/api/activity/%s" % (env, activity_id)
    response = requests.delete(url,headers=headers).json()
    return response

def start_activity(data):
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    url = "%s/api/activity/%s/start" % (env, activity_id)
    response = requests.post(url,headers=headers).json()
    return response

def end_activity(data):
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    url = "%s/api/activity/%s/end" % (env, activity_id)
    response = requests.post(url, headers=headers).json()
    return response

def send__live_comment(data):
    env = data["env"]
    key = data["key"]
    platform = "FACEBOOK"
    page_id = ""
    post_id = ""
    group_id = ""

    if "page_id" in data:
        page_id = data['page_id']
    if "platform" in data:
        platform = data['platform']
    if "post_id" in data:
        post_id = data['post_id']
    if "group_id" in data:
        post_id = data['group_id']
    if page_id == "" or post_id == "":
        info = get_live_info(data)
        platform_list = jsonpath(info, "$..relatedPostList..platform")
        i = platform_list.index(platform.upper())
        page_id = info["data"]["relatedPostList"][i]["page_id"]
        platform = info["data"]["relatedPostList"][i]["platform"]
        post_id = info["data"]["relatedPostList"][i]["post_id"]
        group_id = info["data"]["relatedPostList"][i]["group_id"]
    # info = get_live_info(data)
    # related_post_list = info["data"]["relatedPostList"][0]
    # page_id = related_post_list["page_id"]
    # post_id = related_post_list["post_id"]
    # platform = related_post_list["platform"]
    stamp = int(time.time())
    num = random.randint(100000, 999999)
    user_id = "488864%d" % int(time.time())
    if "user_id" in data:
        user_id = data['user_id']
    name = "test live%d" % int(time.time())
    if "name" in data:
        name = data['name']
    comment_id = "%s_%d%d" % (page_id, stamp, num)
    if "comment_id" in data:
        comment_id = data['comment_id']
    keyword = "接口测试普通留言"
    if "keyword" in data:
        keyword = data['keyword']
    body = {"object": "page", "entry": [{"id": page_id, "time": stamp, "changes": [{"field": "feed", "value": {
            "from": {"id": user_id, "name": name},
            "post": {"status_type": "added_video", "is_published": True, "updated_time": "2022-11-18T09:57:26+0000",
                     "permalink_url": "https://www.facebook.com/permalink.php?story_fbid=pfbid02jLK3e6YdFSXp2DmD7j7vtStLXoBzTi8rxKrp6jFhVMUTTEgz6qvZA8soR9Uwydd8l&id=107977035056574",
                     "promotion_status": "inactive", "id": post_id}, "message": keyword, "item": "comment",
            "verb": "add", "post_id": post_id, "comment_id": comment_id,
            "created_time": stamp, "parent_id": post_id}}]}]}

    if platform.upper() == "INSTAGRAM":
        body = {"entry": [{"id": page_id, "time": stamp, "changes": [{"value": {"from": {"id": user_id,
                 "username": name},
                  "media": {"id": post_id,
                   "media_product_type": "FEED"},
                "id": comment_id, "text": keyword},
                   "field": "comments"}]}], "object": "instagram"}
    elif platform.upper() == "FB_GROUP":
        t_time = stamp*1000
        post_id = post_id.split("_")[-1]
        comment_id = "%d%d" % ( stamp, num)
        body = {"object":"page","entry":[{"id":page_id,"time":t_time,"messaging":[{"recipient":{"id":page_id},"message":keyword,
        "from":{"id":user_id,"name":name},"group_id":group_id,"post_id":post_id,"comment_id":comment_id,"created_time":stamp,"item":"comment",
         "verb":"add","parent_id":post_id,"field":"group_feed"}]}]}

    print(body)
    url = "%s/facebook/webhook" % env
    sign_text = hmac.new(key.encode("utf-8"), json.dumps(body).encode("utf-8"), sha1)
    signData = sign_text.hexdigest()
    # print("body", json.dumps(body))
    header = {"Content-Type": "application/json", "x-hub-signature": "sha1=%s" % signData}
    response = requests.post(url, headers=header, data=json.dumps(body))
    print(response.text)
    return user_id, name, comment_id

def send_mc_message(data):
    env = data["env"]
    key = data["key"]
    stamp = int(time.time()*1000)
    user_id = "488864%d" % int(time.time())
    type = "commment"
    payload = "{}"
    if "payload" in data:
        payload = data["payload"]
    if "type" in data:
        type = data["type"]
    if "user_id" in data:
        user_id = data['user_id']
    name = "test live%d" % int(time.time())
    if "name" in data:
        name = data['name']
    message = "接口测试普通留言"
    if "message" in data:
        message = data['message']
    page_id = ""
    if "page_id" in data:
        page_id = data['page_id']
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data['platform']
    if page_id=="":
        info = get_live_info(data)
        platform_list = jsonpath(info, "$..relatedPostList..platform")
        i = platform_list.index(platform)
        page_id = info["data"]["relatedPostList"][i]["page_id"]
        platform = info["data"]["relatedPostList"][i]["platform"]
    mid = "m_hhAqPhSlMTY4En2oWjSB59T3BFjeU97DdDV4WHr3DLWnPrO0iCsjQlG3hBN%d-sBlT26-6oNg" % stamp
    body = {"entry": [{"id": "%s" % page_id, "messaging": [{"message":
      {
       "mid": mid,
        "text": "%s" % message},
         "recipient": {"id": "%s" % page_id},
         "sender": {"id": "%s" % user_id}, "timestamp": stamp}],
         "time": stamp}], "object": "page"}
    # if platform.upper()=="FACEBOOK":
    #     body = {"entry":[{"id":"%s"%page_id,"messaging":[{"message":
    #     {"mid":"m_hhAqPhSlMTY4En2oWjSB59T3BFjeU97DdDV4WHr3DLWnPrO0iCsjQlG3hBN%d-sBlT26-6oNg"%stamp,"text":"%s"%message},
    #     "recipient":{"id":"%s"%page_id},"sender":{"id":"%s"%user_id},"timestamp":stamp}],"time":stamp}],"object":"page"}
    if platform.upper()=="INSTAGRAM":
        body={"object":"instagram","entry":[{"time":stamp,"id":"%s"%page_id,"messaging":[{"sender":{"id":"%s"%user_id},"recipient":{"id":"%s"%page_id},
       "timestamp":stamp,"message":{"mid":"aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDUwMzgwODgwNTMzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI3NjAyNDExMzcwMDc2NTA5MDozMTgzODU0Mzg3NTY4MDYwMTE3ODUxOTE2MD%d"%stamp,"text":"%s"%message}}]}]}
    elif type=="postback" and platform.upper() in ("FB_GROUP","FACEBOOK"):
        # t_time = stamp * 1000
        body = {"object":"page","entry":[{"time":stamp,"id":"%s"%page_id,"messaging":[{"sender":{"id":"%s"%user_id},"recipient":{"id":"%s"%page_id},"timestamp":stamp,"postback":{"title":"继续 ➡️","payload":payload,"mid":"m_w6KNGd0PMndK0LvCw7Hzy1zsVSWT0fpN3ievQ9LtB0NxnnTQGDMyKI5DFeVbaJIRni1cqqJYXIJ-wq98aw%d"%stamp}}]}]}
    elif type=="postback" and platform.lower()=="instagram":
        body = {"object": "instagram", "entry": [{"time": stamp, "id": "%s" % page_id, "messaging": [
            {"sender": {"id": "%s" % user_id}, "recipient": {"id": "%s" % page_id}, "timestamp": stamp,
             "postback": {"title": "继续 ➡️", "payload": payload,
                          "mid": "m_w6KNGd0PMndK0LvCw7Hzy1zsVSWT0fpN3ievQ9LtB0NxnnTQGDMyKI5DFeVbaJIRni1cqqJYXIJ-wq98aw%d" % stamp}}]}]}

    url = "%s/facebook/webhook" % env
    sign_text = hmac.new(key.encode("utf-8"), json.dumps(body).encode("utf-8"), sha1)
    signData = sign_text.hexdigest()
    header = {"Content-Type": "application/json", "x-hub-signature": "sha1=%s" % signData}
    response = requests.post(url, headers=header, data=json.dumps(body))
    # print(response.text)
    print(body)
    return user_id, name



def get_live_info(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s" % (env, sales_id)
    response = requests.get(url,headers=headers).json()
    return response



def get_activity_detail(data):
    """
    type:
    luckyDraw,抽奖活动
    voucher--留言抢优惠
    answerFirst--抢答
    bidding--竞标
    vote:投票
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    type = data["type"]
    url = ""
    if type in "luckyDraw":
        url = "%s/api/activity/luckyDraw/%s"% (env, activity_id)
    elif type in "voucher":
        url = "%s/api/activity/voucher/%s" % (env, activity_id)
    elif type in "answerFirst":
        url = "%s/api/activity/answerFirst/%s" % (env, activity_id)
    elif type in "bidding":
        url = "%s/api/activity/bidding/%s" % (env, activity_id)
    elif type in "vote":
        url = "%s/api/activity/vote/%s" % (env, activity_id)
    response = requests.get(url,headers=headers).json()
    return response

def live_search_oa_gift(data):
    """
    查询oa赠品，命名转为驼峰和返回第一个赠品的信息
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/gifts"%env
    params = {"page":1}
    response = requests.get(url,headers=headers,params=params).json()
    items = response["data"]["items"]

    if items == []:
        # 新增赠品
        body = {"unlimited_quantity": True, "title_translations": {"zh-cn": "接口自动化新增的赠品%s" % int(time.time())},
                "media_ids": "610d2865ca92cf00264c563c"}
        requests.post(url, headers=headers, json=body).json()
        time.sleep(5)
        #新增后去查询
        response = requests.get(url, headers=headers, params=params).json()
        items = response["data"]["items"]

    # 返回数量不是0的赠品和spu_id
    # print(json.dumps(items))
    quantityList = jsonpath(items,"$..quantity")
    gift_info = items[0]
    for a,b in enumerate(quantityList):
        if b!=0:
            gift_info = items[a]
    spu_id = gift_info["id"]
    return spu_id,gift_info,response

def live_search_oa_product(data):
    """
    查询OA的商品，并返回响应,返回第一个有库存的商品
    spu:返回无规格
    sku:返回多规格
    quantity:0 返回无库存商品
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/products?page=1&per_page=50" %env
    type = "spu"
    quantity = 100
    if "type" in data:
        type = data["type"]
    if "quantity" in data:
        quantity = data["quantity"]
    if "query" in data:
        query = data["query"]
        url = "%s/openApi/proxy/v1/products?page=1&per_page=4&query=%s" % (env,query)
    response = requests.get(url, headers=headers).json()
    items = response["data"]["items"]
    variant_options_list = jsonpath(items,"$..variations")
    product_info = ""
    spu_id = ""
    sku_id = ""
    sku_id_quantity =[]
    for a, b in enumerate(variant_options_list):
        if type=="spu" and b==[] and quantity!=0:
            quantitys=items[a]["total_orderable_quantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys!=0 or unlimited_quantity==True:
                product_info=items[a]
                spu_id = items[a]["id"]
                break
        elif type=="sku" and b!=[] and quantity!=0:
            quantitys = items[a]["total_orderable_quantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys!=0 or unlimited_quantity==True:
                product_info = items[a]
                spu_id = items[a]["id"]
                sku_id = jsonpath(items[a]["variations"],"$..id")
                sku_id_quantity = jsonpath(items[a]["variations"],"$..total_orderable_quantity")
                break
        elif type == "spu" and b == [] and quantity == 0:
            quantitys = items[a]["total_orderable_quantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys != 0 or unlimited_quantity == True:
                product_info = items[a]
                spu_id = items[a]["id"]
                break
        elif type == "sku" and b != [] and quantity == 0:
            quantitys = items[a]["total_orderable_quantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys != 0 or unlimited_quantity == True:
                product_info = items[a]
                spu_id = items[a]["id"]
                sku_id = jsonpath(items[a]["variations"], "$..id")
                sku_id_quantity = jsonpath(items[a]["variations"], "$..total_orderable_quantity")
                break
    return spu_id,sku_id,sku_id_quantity,product_info



def get_merchant_info(data):
    env = data["env"]
    headers = data["headers"]
    merchant_id = data["merchant_id"]
    url = "%s/openApi/proxy/v1/merchants/%s" % (env,merchant_id)
    response = requests.get(url, headers=headers).json()
    base_country_code = response["data"]["base_country_code"]
    default_language_code = response["data"]["default_language_code"]
    currency = ""
    if base_country_code=="TW":
        currency="NT$"
    elif base_country_code=="TH":
        currency = "฿"
    elif base_country_code == "VN":
        #放金额后面
        currency = "₫"
    return base_country_code,currency,response

def delete_broadcast(data):
    env = data["env"]
    headers = data["headers"]
    broadcast_id = data["broadcast_id"]
    url = "%s/admin/api/bff-web/live/broadcast/%s"%(env,broadcast_id)
    response = requests.delete(url,headers=headers).json()
    return response

def get_broadcast_list(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    name = ""
    platform= data["platform"]
    broadcast_id = ""
    pageNum = 1
    pageSize = 12
    if "pageNum" in data:
        pageNum = data["pageNum"]
    if "pageSize" in data:
        pageSize = data["pageSize"]
    if "name" in data:
        name= data["name"]
    url = "%s/admin/api/bff-web/live/broadcast/query"%env
    body = {
    "businessId": "%s"%sales_id,
    "businessType": "LIVE",
    "businessSubType": "LIVE_STREAM",
    "platform": "%s"%platform,
    "pageNum": pageNum,
    "pageSize": pageSize
    }
    reponse = requests.post(url,headers=headers,json=body).json()
    if name !="":
        name_list = jsonpath(reponse,"$..name")
        broadcast_id_list = jsonpath(reponse,"$..id")
        for i,value in enumerate(name_list):
            if value==name:
                broadcast_id =broadcast_id_list[i]
    return broadcast_id,reponse

def get_broadcast_detail(data):
    env = data["env"]
    headers = data["headers"]
    broadcast_id = data["broadcast_id"]
    platform = data["platform"]
    url = "%s/admin/api/bff-web/live/broadcast/detail"%env
    body = {
    "id": "%s"%broadcast_id,
    "platform": "%s"%platform
        }
    response = requests.post(url,headers=headers,json=body).json()
    return response

def end_live(data):
    """结束帖文"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s/end" % (env, sales_id)
    response = requests.put(url, headers=headers).json()
    return response

def get_channel(data):
    "查询粉丝页信息，用于创建帖文"
    env = data["env"]
    headers = data["headers"]
    platform = data["platform"]
    url = "%s/api/posts/post/sales/multiPlatformChannelList?platformList=%s"%(env,platform.upper())
    response = requests.get(url,headers=headers).json()
    return response



def create_live(data):
    """创建直播，不套用通用配置"""
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/live/sales" % (env)
    stamp = int(time.time())
    title = "接口创建的直播活动名称%d"%stamp
    salesDescription = "接口创建的直播活动介绍%d"%stamp
    salesOwner = "接口创建的直播主%d"%stamp
    platform = "FB_GROUP"
    patternModel = "INCLUDE_MATCH"
    keywordValidInLive = True
    keywordValidAfterLive =False
    autoNotifyPayEnable = False
    autoNotifyPayMessage = ""
    autoNotifyPayButton = ""
    autoNotifyPayTime = None
    stockEnable = False
    stockIime = None
    lowOfQuantityEnable = False
    lowOfQuantitySound = False
    lowOfQuantityQuantity = "1"
    has_interaction_message = ""
    has_interaction_message_button = ""
    no_interaction_message_first = ""
    second_message = ""
    first_message_button = ""
    second_message_button = " ️"
    need_send_message = True
    has_link = True
    startTime = None
    # endTime = datetime.datetime.now()+datetime.timedelta(days=3)
    endTime = None
    if "title" in data:
        title = data["title"]
    if "salesDescription" in data:
        title = data["salesDescription"]
    if "salesOwner" in data:
        salesOwner = data["salesOwner"]
    if "platform" in  data:
        platform = data["platform"]
    if "patternModel" in data:
        patternModel = data["patternModel"]
    if "keywordValidInLive" in data:
        keywordValidInLive = data["keywordValidInLive"]
    if "keywordValidAfterLive" in data:
        keywordValidAfterLive = data["keywordValidAfterLive"]

    if "autoNotifyPayEnable" in data:
        autoNotifyPayEnable = data["autoNotifyPayEnable"]
    if "autoNotifyPayMessage" in data:
        autoNotifyPayMessage = data["autoNotifyPayMessage"]
    if "autoNotifyPayButton" in data:
        autoNotifyPayButton = data["autoNotifyPayButton"]
    if "autoNotifyPayTime" in data:
        autoNotifyPayTime = data["autoNotifyPayTime"]

    if "stockEnable" in data:
        stockEnable = data["stockEnable"]
    if "stockIime" in data:
        stockIime = data["stockIime"]

    if "lowOfQuantityEnable" in data:
        lowOfQuantityEnable = data["lowOfQuantityEnable"]
    if "lowOfQuantitySound" in data:
        lowOfQuantitySound = data["lowOfQuantitySound"]
    if "lowOfQuantityQuantity" in data:
        lowOfQuantityQuantity = data["lowOfQuantityQuantity"]

    if "has_interaction_message" in data:
        has_interaction_message = data["has_interaction_message"]
    if "has_interaction_message_button" in data:
        has_interaction_message_button = data["has_interaction_message_button"]
    if "no_interaction_message_first" in data:
        no_interaction_message_first = data["no_interaction_message_first"]
    if "first_message_button" in data:
        first_message_button = data["first_message_button"]
    if "second_message" in data:
        second_message = data["second_message"]
    if "second_message_button" in data:
        second_message_button = data["second_message_button"]
    if "need_send_message" in data:
        need_send_message = data["need_send_message"]
    # if "message_button" in data:
    #     message_button = data["message_button"]
    if "has_link" in data:
        has_link = data["has_link"]
    # platform = platform.upper()
    body = {}
    if platform.lower() in ("fb_group","facebook","instagram"):
        body = {
        "sales": {
            "title": title,
            "salesOwner": salesOwner,
            "salesDescription": salesDescription,
            "platforms": [
                platform
            ],
            "platformChannels": [],
            "startTime": startTime,
            "endTime": endTime
        },
        "salesConfig": {
            "patternModel": {
                "patternModel": patternModel,
                "keywordValidInLive": keywordValidInLive,
                "keywordValidAfterLive": keywordValidAfterLive
            },
            "autoNotifyPay": {
                "enable": autoNotifyPayEnable,
                "message": autoNotifyPayMessage,
                "button": autoNotifyPayButton
            },
            "stock": {
                "lockStock": stockEnable,
                "salesStockLockExpireTime": stockIime
            },
            "lowOfQuantity": {
                "enable": lowOfQuantityEnable,
                "sound": lowOfQuantitySound,
                "quantity": lowOfQuantityQuantity
            }
            },
            "postConfigMap": {
                platform: {
                    "message": {
                        "needSendMessage": need_send_message,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": has_interaction_message
                            },
                            "messageButton": has_interaction_message_button
                        },
                        "hasLink": has_link,
                        "noInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": no_interaction_message_first
                            },
                            "firstMessageButton": first_message_button,
                            "secondMessageTemplate": {
                                "topMessage": second_message
                            },
                            "secondMessageButton": second_message_button
                        },
                        "messageType": "MESSAGE"
                    }
                }
            }
        }
    elif platform in ("pl&fb" ,"obc&fb") :
        platformSubType = platform.split("&")[0].upper()
        data["platform"] = "FACEBOOK"
        res = get_channel(data)
        body = {
        "sales": {
            "title": title,
            "salesOwner": salesOwner,
            "salesDescription": salesDescription,
            "platforms": [
                "SHOPLINE",
                "FACEBOOK"
            ],
            "platformSubType": platformSubType,
            "platformChannels": [
                res["data"][0]
            ],
            "startTime":startTime ,
            "endTime": endTime
        },
        "salesConfig": {
            "patternModel": {
                "patternModel": patternModel,
                "keywordValidInLive": keywordValidInLive,
                "keywordValidAfterLive": keywordValidAfterLive
            },
            "autoNotifyPay": {
                "enable": autoNotifyPayEnable,
                "message": autoNotifyPayMessage,
                "button": autoNotifyPayButton,
                "notifyTime": autoNotifyPayTime
            },
            "stock": {
                "lockStock": stockEnable,
                "salesStockLockExpireTime": stockIime
            },
            "lowOfQuantity": {
                "enable": lowOfQuantityEnable,
                "sound": lowOfQuantitySound,
                "quantity": lowOfQuantityQuantity
            }
        },
        "postConfigMap": {
            "FACEBOOK": {
                "message": {
                    "needSendMessage": need_send_message,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": has_interaction_message
                        },
                        "messageButton": has_interaction_message_button
                    },
                    "hasLink": has_link,
                    "noInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": no_interaction_message_first
                        },
                        "firstMessageButton": first_message_button,
                        "secondMessageButton": second_message_button,
                        "secondMessageTemplate": {
                            "topMessage": second_message
                        }
                    },
                    "messageType": "MESSAGE"
                }
            },
            "SHOPLINE": {
                "message": {
                    "needSendMessage": need_send_message,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": has_interaction_message
                        },
                        "messageButton": has_interaction_message_button
                    },
                    "hasLink": has_link,
                    "noInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": no_interaction_message_first
                        },
                        "firstMessageButton": first_message_button,
                        "secondMessageButton": second_message_button,
                        "secondMessageTemplate": {
                            "topMessage": second_message
                        }
                    },
                    "messageType": "MESSAGE"
                    }
                }
            }
        }
    elif platform in ("pl","obc"):
        platformSubType = platform.upper()
        platform = "SHOPLINE"
        body = {
        "sales": {
            "title": title,
            "salesOwner": salesOwner,
            "salesDescription": salesDescription,
            "platforms": [
                platform
            ],
            "platformChannels": [],
            "startTime": startTime,
            "endTime": endTime,
            "platformSubType":platformSubType
        },
        "salesConfig": {
            "patternModel": {
                "patternModel": patternModel,
                "keywordValidInLive": keywordValidInLive,
                "keywordValidAfterLive": keywordValidAfterLive
            },
            "autoNotifyPay": {
                "enable": autoNotifyPayEnable,
                "message": autoNotifyPayMessage,
                "button": autoNotifyPayButton
            },
            "stock": {
                "lockStock": stockEnable,
                "salesStockLockExpireTime": stockIime
            },
            "lowOfQuantity": {
                "enable": lowOfQuantityEnable,
                "sound": lowOfQuantitySound,
                "quantity": lowOfQuantityQuantity
            }
            },
            "postConfigMap":{}
        }
    response = requests.post(url,headers=headers,json=body).json()
    # print(json.dumps(body))
    print(response)
    sales_id = response["data"]["sales"]["id"]
    return sales_id


def add_live(data):
    """fb——group 链接帖文"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s/addLive"%(env,sales_id)
    pageId = data["page_id"]
    relationUrl = data["relationUrl"]

    body = {
        "pageId": pageId,
        "platform": "FB_GROUP",
        "relationUrl": relationUrl
    }
    response = requests.post(url,headers=headers,json=body).json()
    return response


def get_live_info(data):
    """查询直播间信息"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s" % (env, sales_id)
    response = requests.get(url,headers=headers).json()
    return response

def edit_live_info(data):
    """
    直播前编辑直播间信息:prepare
    直播中编辑直播间信息:progress
    """
    stamp = int(time.time())
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s" % (env, sales_id)
    title = "接口编辑的直播活动名称%d" % stamp
    salesDescription = "接口编辑的直播活动介绍%d" % stamp
    salesOwner = "接口编辑的直播主%d" % stamp
    patternModel = "INCLUDE_MATCH"
    keywordValidInLive = True
    keywordValidAfterLive = False
    autoNotifyPayEnable = False
    autoNotifyPayMessage = ""
    autoNotifyPayButton = ""
    autoNotifyPayTime = None
    stockEnable = False
    stockPreTime = None
    stockExpireTime = None
    lowOfQuantityEnable = False
    lowOfQuantitySound = False
    lowOfQuantityQuantity = "1"
    has_interaction_message = ""
    has_interaction_message_button = ""
    no_interaction_message_first = ""
    second_message = ""
    first_message_button = ""
    second_message_button = "️"
    need_send_message = True
    has_link = True
    commentIntent = True
    #无库存讯息
    allOutOfStockMessage = ""
    allOutOfStockEnable = True
    #欢迎讯息
    welcomeMessage = ""
    welcomeMessageEnable = True
        # 欢迎comment
    welcomeComment = ""
    welcomeCommentEnable = True
    productRecommendMessage = ""
    productRecommendMessageEnable = True
    platform = "FB_GROUP"
    type = "prepare"
    if "type" in data:
        type = data["type"]
    if "title" in data:
        title = data["title"]
    if "salesDescription" in data:
        title = data["salesDescription"]
    if "salesOwner" in data:
        title = data["salesOwner"]
    if "platform" in data:
        platform = data["platform"]
    if "patternModel" in data:
        patternModel = data["patternModel"]
    if "keywordValidInLive" in data:
        keywordValidInLive = data["keywordValidInLive"]
    if "keywordValidAfterLive" in data:
        keywordValidAfterLive = data["keywordValidAfterLive"]
    if "autoNotifyPayEnable" in data:
        autoNotifyPayEnable = data["autoNotifyPayEnable"]
    if "autoNotifyPayMessage" in data:
        autoNotifyPayMessage = data["autoNotifyPayMessage"]
    if "autoNotifyPayButton" in data:
        autoNotifyPayButton = data["autoNotifyPayButton"]
    if "autoNotifyPayTime" in data:
        autoNotifyPayTime = data["autoNotifyPayTime"]
    if "stockEnable" in data:
        stockEnable = data["stockEnable"]
    if "stockExpireTime" in data:
        stockExpireTime = data["stockExpireTime"]
    if "lowOfQuantityEnable" in data:
        lowOfQuantityEnable = data["lowOfQuantityEnable"]
    if "lowOfQuantitySound" in data:
        lowOfQuantitySound = data["lowOfQuantitySound"]
    if "lowOfQuantityQuantity" in data:
        lowOfQuantityQuantity = data["lowOfQuantityQuantity"]
    if "has_interaction_message" in data:
        has_interaction_message = data["has_interaction_message"]
    if "has_interaction_message_button" in data:
        has_interaction_message_button = data["has_interaction_message_button"]
    if "no_interaction_message_first" in data:
        no_interaction_message_first = data["no_interaction_message_first"]
    if "first_message_button" in data:
        first_message_button = data["first_message_button"]
    if "second_message" in data:
        second_message = data["second_message"]
    if "second_message_button" in data:
        second_message_button = data["second_message_button"]
    if "need_send_message" in data:
        need_send_message = data["need_send_message"]
    # if "message_button" in data:
    #     message_button = data["message_button"]
    if "has_link" in data:
        has_link = data["has_link"]
    if "commentIntent" in data:
        commentIntent = data["commentIntent"]
    if "allOutOfStockMessage" in data:
        allOutOfStockMessage = data["allOutOfStockMessage"]
    if "allOutOfStockEnable" in data:
        allOutOfStockEnable = data["allOutOfStockEnable"]
    if "welcomeMessage" in data:
        welcomeMessage = data["welcomeMessage"]
    if "welcomeMessageEnable" in data:
        welcomeMessageEnable = data["welcomeMessageEnable"]
    if "welcomeComment" in data:
        welcomeComment = data["welcomeComment"]
    if "welcomeCommentEnable" in data:
        welcomeCommentEnable = data["welcomeCommentEnable"]
    if "productRecommendMessage" in data:
        productRecommendMessage = data["productRecommendMessage"]
    if "productRecommendMessageEnable" in data:
        productRecommendMessageEnable = data["productRecommendMessageEnable"]
    platformChannels = []
    startTime = None
    endTime = None
    body = {}
    if type=="progress":
        #进行中不允许修改基础设置、关键子下单设置、保留库存、
        res = get_live_info(data)
        title = res["data"]["sales"]["post_sales_title"]
        salesOwner = res["data"]["sales"]["post_sales_owner"]
        salesDescription = res["data"]["sales"]["post_sales_title"]
        patternModel = res["data"]["salesConfig"]["patternModel"]["patternModel"]
        keywordValidInLive = res["data"]["salesConfig"]["patternModel"]["keywordValidInLive"]
        keywordValidAfterLive = res["data"]["salesConfig"]["patternModel"]["keywordValidAfterLive"]
        if "start_time_timestamp" in res["data"]["sales"]:
            startTime = res["data"]["sales"]["start_time_timestamp"]
        if "end_time_timestamp" in res["data"]["sales"]:
            endTime = res["data"]["sales"]["end_time_timestamp"]
        relatedPostList = res["data"]["relatedPostList"]
        for relatedPost in relatedPostList:
            platformChannelName = relatedPost["page_name"]
            platformChannelId = relatedPost["page_id"]
            platformChannel = {
                    "platformChannelName": platformChannelName,
                    "platformChannelId": platformChannelId,
                    "platform": platform
                }
            platformChannels.append(platformChannel)
    if platform.upper()=="FB_GROUP":
        body = {
        "sales": {
            "title": title,
            "salesOwner": salesOwner,
            "salesDescription": salesDescription,
            "platforms": [
                platform
            ],
            "platformSubType": "",
            "platformChannels": [],
            "archivedStreamVisibleTime": None
        },
        "salesConfig": {
            "patternModel": {
                "patternModel": patternModel,
                "keywordValidInLive": keywordValidInLive,
                "keywordValidAfterLive": keywordValidAfterLive
            },
            "autoNotifyPay": {
                "enable": autoNotifyPayEnable,
                "notifyTime": autoNotifyPayTime,
                "message": autoNotifyPayMessage,
                "button": autoNotifyPayButton
            },
            "stock": {
                "lockStock": stockEnable,
                "salesStockLockExpireTime": stockExpireTime,
                "salesStockLockPreTime": stockPreTime
            },
            "commentIntent": {
                "enabled": commentIntent
            },
            "variationToggleOn": {
                "enable": True
            },
            "productSort": {
                "productSort": "NEW_TO_OLD"
            },
            "lowOfQuantity": {
                "enable": lowOfQuantityEnable,
                "sound": lowOfQuantitySound,
                "quantity": lowOfQuantityQuantity
            },
            "notice": None,
            "frontLive": None,
            "liveViewSdk": None,
            "runningLightsConfig": None,
            "fbGroupSettingConfig": {
                "scGroupPmCommentId": True,
                "scGroupWebhook": True
            },
            "productPinningStyle": None
        },
        "postConfigMap": {
            platform: {
                "message": {
                    "needSendMessage": need_send_message,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": has_interaction_message
                        },
                        "messageButton": has_interaction_message_button
                    },
                    "hasLink": has_link,
                    "noInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": no_interaction_message_first
                        },
                        "firstMessageButton": first_message_button,
                        "secondMessageTemplate": {
                            "topMessage": second_message
                        },
                        "secondMessageButton": second_message_button
                    },
                    "messageType": "MESSAGE"
                },
                "allOutOfStockMessage": {
                    "needSendMessage": allOutOfStockEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": allOutOfStockMessage
                        }
                    },
                    "messageType": "ALL_OUT_OF_STOCK"
                },
                "welcomeMessage": {
                    "needSendMessage": welcomeMessageEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": welcomeMessage
                        }
                    },
                    "messageType": "WELCOME_MESSAGE"
                },
                "productRecommendMessage": {
                    "needSendMessage": productRecommendMessageEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "message": productRecommendMessage
                        }
                    },
                    "messageType": "PRODUCT_RECOMMEND_FB_MESSAGE"
                },
                "welcomeMessageComment": {
                    "needSendMessage": welcomeCommentEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": welcomeComment
                        }
                    },
                    "messageType": "WELCOME_MESSAGE_COMMENT"
                },
                "showNumberOfViewers": None,
                "showShareButton": None
            }
            }
        }
    elif platform.lower() in ("facebook","instagram"):
        body = {
        "sales": {
            "title": title,
            "salesOwner": salesOwner,
            "salesDescription": salesDescription,
            "platforms": [
                platform.upper()
            ],
            "platformSubType": "",
            "platformChannels": platformChannels,
            "archivedStreamVisibleTime": None,
            "startTime":startTime,
            "endtTime":endTime
        },
        "salesConfig": {
            "patternModel": {
                "patternModel": patternModel,
                "keywordValidInLive": keywordValidInLive,
                "keywordValidAfterLive": keywordValidAfterLive
            },
            "autoNotifyPay": {
                "enable": autoNotifyPayEnable,
                "notifyTime": autoNotifyPayTime,
                "message": autoNotifyPayMessage,
                "button": autoNotifyPayButton
            },
            "stock": {
                "lockStock": stockEnable,
                "salesStockLockExpireTime": stockExpireTime,
                "salesStockLockPreTime": stockPreTime
            },
            "commentIntent": {
                "enabled": commentIntent
            },
            "variationToggleOn": {
                "enable": True
            },
            "productSort": {
                "productSort": "NEW_TO_OLD"
            },
            "lowOfQuantity": {
                "enable": lowOfQuantityEnable,
                "sound": lowOfQuantitySound,
                "quantity": lowOfQuantityQuantity
            },
            "notice": None,
            "frontLive": None,
            "liveViewSdk": None,
            "runningLightsConfig": None,
            "fbGroupSettingConfig": None,
            "productPinningStyle": None
        },
        "postConfigMap": {
            "FACEBOOK": {
                "message": {
                    "needSendMessage": need_send_message,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": has_interaction_message
                        },
                        "messageButton": has_interaction_message_button
                    },
                    "hasLink": has_link,
                    "noInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": no_interaction_message_first
                        },
                        "firstMessageButton": first_message_button,
                        "secondMessageTemplate": {
                            "topMessage": second_message
                        },
                        "secondMessageButton": second_message_button
                    },
                    "messageType": "MESSAGE"
                },
                "allOutOfStockMessage": {
                    "needSendMessage": allOutOfStockEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": allOutOfStockMessage
                        }
                    },
                    "messageType": "ALL_OUT_OF_STOCK"
                },
                "welcomeMessage": {
                    "needSendMessage": welcomeMessageEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": welcomeMessage
                        }
                    },
                    "messageType": "WELCOME_MESSAGE"
                },
                "productRecommendMessage": {
                    "needSendMessage": productRecommendMessageEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "message": productRecommendMessage
                        }
                    },
                    "messageType": "PRODUCT_RECOMMEND_FB_MESSAGE"
                },
                "welcomeMessageComment": {
                    "needSendMessage": welcomeCommentEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": welcomeComment
                        }
                    },
                    "messageType": "WELCOME_MESSAGE_COMMENT"
                },
                "showNumberOfViewers": None,
                "showShareButton": None
            }
            }
        }
    print(body)
    response = requests.put(url, headers=headers, json=body).json()
    return response


def save_global_config(data):
    "保存直播间通用配置"
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales/global/LIVE"%env
    patternModel = "INCLUDE_MATCH"
    keywordValidInLive = True
    keywordValidAfterLive = False
    autoNotifyPayEnable = False
    autoNotifyPayMessage = ""
    autoNotifyPayButton = ""
    autoNotifyPayTime = None
    stockEnable = False
    stockPreTime = None
    stockExpireTime = None
    lowOfQuantityEnable = False
    lowOfQuantitySound = False
    lowOfQuantityQuantity = "1"
    has_interaction_message = ""
    has_interaction_message_button = ""
    no_interaction_message_first = ""
    second_message = ""
    first_message_button = ""
    second_message_button = " ️"
    need_send_message = True
    has_link = True
    commentIntent = True
    # 无库存讯息
    allOutOfStockMessage = ""
    allOutOfStockEnable = True
    # 欢迎讯息
    welcomeMessage = ""
    welcomeMessageEnable = True
    # 欢迎comment
    welcomeComment = ""
    welcomeCommentEnable = True
    #推荐讯息
    fbProductRecommendMessage = ""
    igProductRecommendMessage = ""
    slProductRecommendMessage = ""
    # productRecommendMessageEnable = True
    #视频观看人数
    show_number = True
    show_share = True

    if "title" in data:
        title = data["title"]
    if "salesDescription" in data:
        title = data["salesDescription"]
    if "salesOwner" in data:
        title = data["salesOwner"]
    if "platform" in data:
        platform = data["platform"]
    if "patternModel" in data:
        patternModel = data["patternModel"]
    if "keywordValidInLive" in data:
        keywordValidInLive = data["keywordValidInLive"]
    if "keywordValidAfterLive" in data:
        keywordValidAfterLive = data["keywordValidAfterLive"]

    if "autoNotifyPayEnable" in data:
        autoNotifyPayEnable = data["autoNotifyPayEnable"]
    if "autoNotifyPayMessage" in data:
        autoNotifyPayMessage = data["autoNotifyPayMessage"]
    if "autoNotifyPayButton" in data:
        autoNotifyPayButton = data["autoNotifyPayButton"]
    if "autoNotifyPayTime" in data:
        autoNotifyPayTime = data["autoNotifyPayTime"]

    if "stockEnable" in data:
        stockEnable = data["stockEnable"]
    if "stockExpireTime" in data:
        stockExpireTime = data["stockExpireTime"]

    if "lowOfQuantityEnable" in data:
        lowOfQuantityEnable = data["lowOfQuantityEnable"]
    if "lowOfQuantitySound" in data:
        lowOfQuantitySound = data["lowOfQuantitySound"]
    if "lowOfQuantityQuantity" in data:
        lowOfQuantityQuantity = data["lowOfQuantityQuantity"]

    if "has_interaction_message" in data:
        has_interaction_message = data["has_interaction_message"]
    if "has_interaction_message_button" in data:
        has_interaction_message_button = data["has_interaction_message_button"]
    if "no_interaction_message_first" in data:
        no_interaction_message_first = data["no_interaction_message_first"]
    if "first_message_button" in data:
        first_message_button = data["first_message_button"]
    if "second_message" in data:
        second_message = data["second_message"]
    if "second_message_button" in data:
        second_message_button = data["second_message_button"]
    if "need_send_message" in data:
        need_send_message = data["need_send_message"]
    # if "message_button" in data:
    #     message_button = data["message_button"]
    if "has_link" in data:
        has_link = data["has_link"]
    if "commentIntent" in data:
        commentIntent = data["commentIntent"]

    if "allOutOfStockMessage" in data:
        allOutOfStockMessage = data["allOutOfStockMessage"]
    if "allOutOfStockEnable" in data:
        allOutOfStockEnable = data["allOutOfStockEnable"]

    if "welcomeMessage" in data:
        welcomeMessage = data["welcomeMessage"]
    if "welcomeMessageEnable" in data:
        welcomeMessageEnable = data["welcomeMessageEnable"]

    if "welcomeComment" in data:
        welcomeComment = data["welcomeComment"]
    if "welcomeCommentEnable" in data:
        welcomeCommentEnable = data["welcomeCommentEnable"]

    if "show_number" in data:
        show_number = data["show_number"]
    if "show_share" in data:
        show_share = data["show_share"]

    if "fbProductRecommendMessage" in data:
        fbProductRecommendMessage = data["fbProductRecommendMessage"]
    if "igProductRecommendMessage" in data:
        igProductRecommendMessage = data["igProductRecommendMessage"]
    if "slProductRecommendMessage" in data:
        slProductRecommendMessage = data["slProductRecommendMessage"]


    body = {
    "saveList": [
        {
            "configKey": "PATTERN_MODEL",
            "configValue": {
                "patternModel": patternModel,
                "keywordValidInLive": keywordValidInLive,
                "keywordValidAfterLive": keywordValidAfterLive
            }
        },
        {
            "configKey": "STOCK",
            "configValue": {
                "lockStock": stockEnable,
                "salesStockLockExpireTime": stockExpireTime
            }
        },
        {
            "configKey": "LOW_OF_QUANTITY",
            "configValue": {
                "enable": lowOfQuantityEnable,
                "sound": lowOfQuantitySound,
                "quantity": lowOfQuantityQuantity
            }
        },
        {
            "configKey": "MESSAGE",
            "configValue": {
                "needSendMessage": need_send_message,
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "topMessage": has_interaction_message
                    },
                    "messageButton": has_interaction_message_button
                },
                "hasLink": has_link,
                "noInteractionMessage": {
                    "firstMessageTemplate": {
                        "topMessage": no_interaction_message_first
                    },
                    "firstMessageButton": first_message_button,
                    "secondMessageTemplate": {
                        "topMessage": second_message
                    },
                    "secondMessageButton": second_message_button
                },
                "messageType": "MESSAGE"
            }
        },
        {
            "configKey": "WELCOME_MESSAGE",
            "configValue": {
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "topMessage": welcomeMessage
                    }
                },
                "needSendMessage": welcomeMessageEnable,
                "messageType": "WELCOME_MESSAGE"
            }
        },
        {
            "configKey": "WELCOME_MESSAGE_COMMENT",
            "configValue": {
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "topMessage": welcomeComment
                    }
                },
                "needSendMessage": welcomeCommentEnable,
                "messageType": "WELCOME_MESSAGE_COMMENT"
            }
        },
        {
            "configKey": "PRODUCT_RECOMMEND_FB_MESSAGE",
            "configValue": {
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "message": fbProductRecommendMessage
                    }
                },
                "messageType": "PRODUCT_RECOMMEND_FB_MESSAGE"
            }
        },
        {
            "configKey": "PRODUCT_RECOMMEND_IG_MESSAGE",
            "configValue": {
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "message": igProductRecommendMessage
                    }
                },
                "messageType": "PRODUCT_RECOMMEND_IG_MESSAGE"
            }
        },
        {
            "configKey": "PRODUCT_RECOMMEND_SHOP_LINE_MESSAGE",
            "configValue": {
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "message": slProductRecommendMessage
                    }
                },
                "messageType": "PRODUCT_RECOMMEND_SHOP_LINE_MESSAGE"
            }
        },
        {
            "configKey": "ALL_OUT_OF_STOCK",
            "configValue": {
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "topMessage": allOutOfStockMessage
                    }
                },
                "needSendMessage": allOutOfStockEnable,
                "messageType": "ALL_OUT_OF_STOCK"
            }
        },
        {
            "configKey": "AUTO_NOTIFY_PAY",
            "configValue": {
                "enable": autoNotifyPayEnable,
                "message": autoNotifyPayMessage,
                "button": autoNotifyPayButton
            }
        },
        {
            "configKey": "COMMENT_INTENT",
            "configValue": {
                "enabled": commentIntent
            }
        },
        {
            "configKey": "SHOW_NUMBER_OF_VIEWERS",
            "configValue": {
                "enabled": show_number
            }
        },
        {
            "configKey": "SHOW_SHARE_BUTTON",
            "configValue": {
                "enabled": show_share
            }
        }
    ]
}
    response = requests.post(url, headers=headers, json=body).json()
    return response


def get_global_config(data):
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales/global/LIVE" % env
    response = requests.get(url,headers=headers).json()
    # print(response)
    return response




outOfStock = {
        "en":"The following product(s) doesn't have enough stock, please select other products, thanks!\n❗️{products}".replace("️{products}","ffddd"),
        "zh-cn":"以下商品库存不足，请选购其他商品，谢谢！\n❗️{products}".replace("️{products}","ffddd"),
        "zh-hant":"以下商品庫存不足，請選購其他商品，謝謝！\n❗️{products}".replace("️{products}","ffddd")
        }



def remove_live_product(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    product_id = data["product_id"]
    url = "%s/api/posts/post/sales/%s/product/%s"%(env,sales_id,product_id)
    response = requests.delete(url,headers=headers).json()
    return response


def change_keyword_status(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    product_id = data["product_id"]
    status = "true"
    if "status" in data:
        status = data["status"]
    url = "%s/api/posts/post/sales/%s/product/keyword/status/%s"%(env,sales_id,status)
    body = {
    "spuIdList": [
        product_id
        ]
     }
    response = requests.put(url, headers=headers,json=body).json()
    return response

def delete_product_set(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    product_id = data["product_id"]
    url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set"%(env,sales_id)
    body = {
    "ids": [
            product_id
        ]
    }
    res = requests.delete(url,headers=headers,json=body).json()
    return res
#查询普通商品列表
def get_live_product(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    query = ""
    if "query" in data:
        query = data["query"]
    url = "%s/api/posts/post/sales/%s/product/v2" % (env, sales_id)
    params = {"salesId":sales_id,"pageIndex":1,"pageSize":25,}
    if query!="":
        params["queryType"] = "PRODUCT_NAME"
        params["query"] = query
    response = requests.get(url, headers=headers,params=params).json()
    return response

def search_product_set(data):
    """查询直播间组合商品列表"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    query = ""
    pageNum = 1
    if "pageNum" in data:
        pageNum = data["pageNum"]
    if "query" in data:
        query = data["query"]
    url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set"%(env,sales_id)
    param = {"pageNum":pageNum,"pageSize":10,"query":query,"queryType":"PRODUCT_NAME"}
    # print(param)
    res = requests.get(url,headers=headers,params=param).json()
    return res

def get_product_set(data):
    """查询来添加组合商品"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    query = ""
    pageNum = 1
    if "pageNum" in data:
        pageNum = data["pageNum"]
    if "query" in data:
        query = data["query"]
    url = "%s/admin/api/bff-web/live/sale/%s/product/product_set/list"%(env,sales_id)
    param = {"pageNum":pageNum,"pageSize":10,"query":query}
    # print(param)
    while True:
        res = requests.get(url, headers=headers, params=param)
        if res.status_code==200:
            return res.json()

def get_sales_keyword(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/admin/api/bff-web/live/sale/%s/keyword/list"%(env,sales_id)
    res = requests.get(url, headers=headers).json()
    return res

def get_stock_product_set(res,type="stock"):
    list_data = res["data"]["list"]
    if type=="stock":
        for i in list_data:
            combinationList = i["combinationList"]
            for combination in combinationList:
                products = combination["products"]
                for product in products:
                    count = product["count"]
                    quantity = product["quantity"]
                    if quantity==-1:
                        # print("库存无限数量")
                        pass
                    elif quantity>count:
                        break
                    keyword = combination["keywords"][0]
                    product_id = i["id"]
                    combination_id = combination["id"]
                    return keyword, product_id, combination_id,i
    elif type=="out":
        for i in list_data:
            combinationList = i["combinationList"]
            for combination in combinationList:
                products = combination["products"]
                for product in products:
                    count = product["count"]
                    quantity = product["quantity"]
                    if quantity != -1 and quantity < count:
                        keyword = combination["keywords"][0]
                        product_id = i["id"]
                        combination_id = combination["id"]
                        return keyword, product_id, combination_id,i

def  change_product_set_keyword_status(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    product_id = data["product_id"]
    status = True
    if "status" in data:
        status = data["status"]
    url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set/keyword/status" % (env, sales_id)
    body = {
    "ids": [
        product_id
        ],
        "status": status
        }
    response = requests.put(url, headers=headers, json=body).json()
    return response


def get_produnct_set_detail(data):
    # print(data)
    env = data["env"]
    headers = data["headers"]
    spu_ids = data["spu_ids"]
    sales_id = data["sales_id"]
    url = "%s/admin/api/bff-web/live/sale/%s/product/product/list" % (env, sales_id)
    body = {
        "ids": spu_ids,
        "pageNum": 1,
        "pageSize": 101
    }
    while True:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code==200:
            return response.json()


def add_specific_product_set_to_live(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    set_list_res = get_product_set(data)
    data_list = set_list_res["data"]["list"]
    arr = 0
    if "arr" in data:
        arr = data["arr"]
        if arr >len(data_list)-1:
            arr = 0
    product_info = data_list[arr]
    product_id = product_info["id"]
    childrenInfo = product_info["childrenInfo"]
    title = product_info["title"]
    spu_ids = list(childrenInfo.keys())
    # necessaryQuantitys  = jsonpath(data_list, "$..necessaryQuantity")
    data["spu_ids"] = spu_ids
    # 查询子商品信息
    response = get_produnct_set_detail(data)
    products = []
    zi_list = response["data"]["list"]
    # print(vars["childrenInfo"])
    for i in zi_list:
        product = {}
        spu_id = i["id"]
        product["count"] = childrenInfo[spu_id]["necessaryQuantity"]
        product["spuId"] = spu_id
        variations = i["variations"]
        if variations == []:
            product["skuId"] = spu_id
        else:
            sku_id = variations[0]["id"]
            product["skuId"] = sku_id
        products.append(product)

    url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set" % (env, sales_id)
    keyword = "python添加商品关键子%d" % int(time.time())
    add_body = {
        "spuList": [
            {
                "id": "%s" % product_id,
                "defaultKey": "",
                "combinationList": [
                    {
                        "products": products,
                        "keywords": [
                            "%s" % keyword
                        ],
                        "skuId": ""
                    }
                ]
            }
        ]
    }
    try:
        #先删除再添加
        data["product_id"] = product_id
        delete_product_set(data)
        time.sleep(2)
        data_res = requests.post(url, headers=headers, json=add_body).json()
        return product_id,products,keyword,title,data_res
    except Exception:
        print("出现异常")

def add_mutil_product_set_to_live(data):
    """添加多规格商品的全部"""
    pass


def add_all_product_set_to_live(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    while True:
        print(data)
        set_list_res = get_product_set(data)
        print(set_list_res)
        data_list = set_list_res["data"]["list"]
        for product_info in data_list:
            product_id = product_info["id"]
            childrenInfo  = product_info["childrenInfo"]
            spu_ids = list(childrenInfo.keys())
            # necessaryQuantitys  = jsonpath(data_list, "$..necessaryQuantity")
            data["spu_ids"] = spu_ids
            #查询子商品信息
            response = get_produnct_set_detail(data)
            products = []
            zi_list = response["data"]["list"]
                    # print(vars["childrenInfo"])
            for i in zi_list:
                product = {}
                spu_id = i["id"]
                product["count"] = childrenInfo[spu_id]["necessaryQuantity"]
                product["spuId"] = spu_id
                variations = i["variations"]
                if variations == []:
                    product["skuId"] = spu_id
                else:
                    sku_id = variations[0]["id"]
                    product["skuId"] = sku_id
                products.append(product)
            url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set"%(env,sales_id)
            keyword = "python添加商品关键子%d"%int(time.time())
            add_body = {
                      "spuList": [
                    {
                        "id": "%s"%product_id,
                        "defaultKey": "",
                        "combinationList": [
                            {
                                "products": products,
                                "keywords": [
                                    "%s"%keyword
                                ],
                                "skuId": ""
                                }
                            ]
                        }
                        ]
                    }
            try:
                data_res = requests.post(url,headers=headers,json=add_body).json()
                print(data_res)
            except Exception:
                print("出现异常")
        lastPage = set_list_res["data"]["pageInfo"]["lastPage"]
        pageNum = set_list_res["data"]["pageInfo"]["pageNum"]
        print("加前的pagenum",pageNum)
        # print(lastPage)
        if lastPage == False:
            pageNum = pageNum + 1
            data["pageNum"] = pageNum
            print("pageNum=",pageNum)
        else:
            break

if __name__=="__main__":
    pass

