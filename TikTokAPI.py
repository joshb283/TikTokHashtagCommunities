from TikTokApi import TikTokApi
import json

with TikTokApi() as api:
    nosabo = api.hashtag(name="nosabo")
    nosabokids = api.hashtag(name="nosabokids")
    nosabokidsbelike = api.hashtag(name="nosabokidsbelike")
    yonosabokid = api.hashtag(name="yonosabokid")
    tags = [nosabo,nosabokids,nosabokidsbelike,yonosabokid]
    flag = 0
    f = open("output/nosabo.csv", "w")
    g = open("output/nosabocomments.csv", "w")
    f.write("my_id,url,video_id,video_author,hashtags,createtime,description,isAd,stickersOnItem,privateItem,commentCount,playCount,shareCount\n")
    g.write("my_id,comment_id,text,author,likecount,language,ReplyCommenttotal,createtime\n")
    curr_video_id = 0
    for tag in tags:
        for video in tag.videos():
            video_id = str(video.id)
            video_author = str(video.author.username)
            video_hashtags = ""
            for hashtag in video.hashtags:
                video_hashtags += "#" +str(hashtag.name) + " "
            video_url = "https://www.tiktok.com/@"+str(video.author.username)+"/video/"+str(video.id)
            video_dict = video.as_dict
            video_createtime = str(video.create_time)
            video_description = str(video_dict["desc"]).replace(",", " ").replace("\n", " ")
            video_isAd = str(video_dict["isAd"])
            video_stickersOnItem = ""
            video_stickers = []
            try:
                video_stickers = video_dict["stickersOnItem"]
            except:
                video_stickers = []
            for sticker in video_stickers:
                sticker1 = sticker["stickerText"]
                for sticker2 in sticker1:
                    video_stickersOnItem += (str(sticker2.replace("\n"," ").replace("\t", " ").replace(",",""))) + " "
            stats_dict = video_dict["stats"]
            video_commentCount = stats_dict["commentCount"]
            video_playCount = stats_dict["playCount"]
            video_shareCount = stats_dict["shareCount"]
            video_privateItem = video_dict["privateItem"]
            f.write(str(curr_video_id)+","+video_url+","+str(video_id)+","+video_author+","+ video_hashtags+ "," + str(video_createtime)+ ","+video_description+","+str(video_isAd) +","+video_stickersOnItem + ","+str(video_privateItem)+","+str(video_commentCount)+","+str(video_playCount)+","+str(video_shareCount)+"\n" )
            try:
                for comment in video.comments():
                    comment_id = comment.id
                    comment_text = str(comment.text).replace(",", " ").replace("\n", " ")
                    comment_author = comment.author.username
                    comment_likecount = comment.likes_count
                    comment_parent = comment.parent
                    comment_dict = comment.as_dict
                    comment_language = comment_dict["comment_language"]
                    comment_replycommenttotal = comment_dict["reply_comment_total"]
                    comment_createtime = comment_dict["create_time"]
                    g.write(str(curr_video_id)+","+str(comment_id)+","+str(comment_text)+","+str(comment_author)+","+str(comment_likecount)+","+str(comment_language)+","+str(comment_replycommenttotal)+","+str(comment_createtime)+"\n")
            except:
                print("no comments")
            video_data = video.bytes()
            with open("output/nosabovids/"+str(tag.name)+"_"+str(curr_video_id)+".mp4", "wb") as out_file:
                out_file.write(video_data)
            curr_video_id += 1