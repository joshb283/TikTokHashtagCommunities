from tikapi import TikAPI, ValidationException, ResponseException
import pandas as pd
from datetime import datetime
import numpy as np


df = pd.read_csv("nosabokids.csv") #file generated from tikapi_videos.py


api = TikAPI("ENTER_API_KEY_HERE")
User = api.user(
    accountKey="ENTER_ACCOUNT_KEY"
)

try:
    f = open("nosabokids_comments.csv","a") #output file
    header = "video_id,author,text,create_time,comment_language,cid,reply_comment_total,queryTime\n"
    f.write(header)

    video_ids = list(df["videoId"])
    for video_id in video_ids:
        response = User.posts.comments.list(
            media_id=str(video_id)
        )

        while(response):
            comments = response.json()["comments"]
            if(comments == None):
                break
            for comment in comments:
                if(comment == None or comment["user"] == None or comment["user"]["unique_id"] == None or comment["text"] == None):
                    continue
                author = str(comment["user"]["unique_id"])
                text = str(comment["text"]).replace(","," ").replace("\n", " ")
                create_time = str(comment["create_time"])
                comment_language = str(comment["comment_language"])
                cid = str(comment["cid"])
                reply_comment_total = str(comment["reply_comment_total"])
                querytime = str(datetime.now())
                f.write(str(video_id)+","+author+","+text+","+create_time+","+comment_language+","+cid+","+reply_comment_total+","+querytime+"\n")
            cursor = response.json().get('cursor')
            print("Getting next items ", cursor)
            response = response.next_items()
    f.close()

except ValidationException as e:
    print(e, e.field)

except ResponseException as e:
    print(e, e.response.status_code)