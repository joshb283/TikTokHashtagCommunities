from tikapi import TikAPI, ValidationException, ResponseException
from datetime import datetime

api = TikAPI("ENTER_API_KEY_HERE")
idsCollected = []
# import pandas as pd
# df = pd.read_csv("nosabo1.csv")
# idsCollected = list(df["videoId"])

try:
    all_hashtags = ["nosabokids", "yonosabokid", "nosabo", "nosbokidsbelike"]   #Enter the hashtags to query
    myIdPrefix = "ns_"
    myId = 0
    f = open("nosabokids.csv", "a")  #Output File
    headers = "myId,url,hashtags,isAd,authorUsername,authorId,authorFollowers,authorHeartCount,authorVideoCount,createTime,desc,id,privateItem,commentCount,playCount,shareCount,videoId,searchQuery,timeQueried\n"
    f.write(headers)

    for tag in all_hashtags:
        response = api.public.hashtag(
            name=tag
        )
        hashtagId = response.json()['challengeInfo']['challenge']['id']
        response = api.public.hashtag(
            id=hashtagId
        )

        flag = 1

        while(response):
            if(not "itemList" in response.json()):
                if(flag == 2):
                    flag = 1
                    break
                if(not "cursor" in response.json()):
                    flag = 1
                    break
                else:
                    flag = 2
                    cursor = response.json().get('cursor')
                    print("Getting next items ", cursor)
                    response = response.next_items()
                    if(not response):
                        break
            flag = 1
            itemlist = response.json()["itemList"]
            for item in itemlist:
                id = str(item["id"]).strip("\n").strip(",")
                if(id in idsCollected):
                    continue
                idsCollected.append(id)
                authorUsername = str(item["author"]["uniqueId"]).strip("\n").strip(",")
                authorId = str(item["author"]["id"]).strip("\n").strip(",")
                authorFollowers = str(item["authorStats"]["followerCount"]).strip("\n").strip(",")
                authorHeartCount = str(item["authorStats"]["heartCount"]).strip("\n").strip(",")
                authorVideoCount = str(item["authorStats"]["videoCount"]).strip("\n").strip(",")
                createTime = str(item["createTime"]).strip("\n").strip(",")
                desc = str(item["desc"]).replace(","," ").strip("\n").strip(",")
                privateItem = str(item["privateItem"]).strip("\n").strip(",")
                commentCount = str(item["stats"]["commentCount"]).strip("\n").strip(",")
                playCount = str(item["stats"]["playCount"]).strip("\n").strip(",")
                shareCount = str(item["stats"]["shareCount"]).strip("\n").strip(",")
                videoId = str(item["video"]["id"]).strip("\n").strip(",") 
                url = "https://www.tiktok.com/@"+authorUsername+"/video/"+id
                challenges =  item["challenges"]
                hashtags = ""
                for challenge in challenges:
                    hashtags += ("#"+challenge["title"] + " ")
                isAd = str(item["isAd"])
                searchQuery = tag
                timeQueried = str(datetime.now())
                
                curr = myIdPrefix + str(myId) + "," +url+","+hashtags+","+isAd+","+authorUsername +"," + authorId+','+authorFollowers+","+authorHeartCount+","+authorVideoCount+','+createTime+","+desc+","+id+","+privateItem+","+commentCount+","+playCount+","+shareCount+","+videoId+","+searchQuery+","+timeQueried+"\n"
                f.write(curr)
                myId += 1
            cursor = response.json().get('cursor')
            print("Getting next items ", cursor)
            response = response.next_items()
            
    f.close()

except ValidationException as e:
    print(e, e.field)

except ResponseException as e:
    print(e, e.response.status_code)

