import requests
import json
import subprocess
from pyrogram.types.messages_and_media import message
import helper
from pyromod import listen
from pyrogram.types import Message
import pyrogram
import logging
from pyrogram import Client, filters
from subprocess import getstatusoutput
import re
from pyrogram.types import User, Message
import os

import requests
bot = Client(
    "CW",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

logger = logging.getLogger()
thumb = os.environ.get("THUMB")
if thumb.startswith("http://") or thumb.startswith("https://"):
    getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
    thumb = "thumb.jpg"


@bot.on_message(filters.command(["start"]))
async def start(bot, update):
       await update.reply_text("Hi i am **Careerwill Downloader**.\n\n"
                              "**NOW:-** "
                                       
                                       "Press **/login** to continue..\n\n")
                                     

ACCOUNT_ID = "6206459123001"
BCOV_POLICY = "BCpkADawqM1474MvKwYlMRZNBPoqkJY-UWm7zE1U769d5r5kqTjG0v8L-THXuVZtdIQJpfMPB37L_VJQxTKeNeLO2Eac_yMywEgyV9GjFDQ2LTiT4FEiHhKAUvdbx9ku6fGnQKSMB8J5uIDd"
bc_url = (
    f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"
)
bc_hdr = {"BCOV-POLICY": BCOV_POLICY}

url="https://elearn.crwilladmin.com/api/v1/"

info= {
 "deviceType":"android",
    "password":"",
    "deviceModel":"Asus ASUS_X00TD",
    "deviceVersion":"Pie(Android 9.0)",
    "email":"",
}

@bot.on_message(filters.command(["login"])& ~filters.edited)
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
        "Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**"
    )

    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text
    info["email"] = raw_text.split("*")[0]
    info["password"] = raw_text.split("*")[1]
    await input1.delete(True)

    login_response=requests.post(url+"login-other",info)
    token=login_response.json( )["data"]["token"]
    await editable.edit("**login Successful**")
    await editable.edit("You have these Batches :-")
    
    url1 = requests.get("https://elearn.crwilladmin.com/api/v1/comp/my-batch?&token="+token)
    b_data = url1.json()['data']['batchData']

    cool=""
    for data in b_data:
        aa=f"**Batch Name -** {data['batchName']}\n**Batch ID -** ```{data['id']}```\n**By -** {data['instructorName']}\n\n"
        if len(f'{cool}{aa}')>4096:
            await m.reply_text(aa)
            cool =""
        cool+=aa
    await m.reply(cool)

    editable1= await m.reply_text("**Now send the Batch ID to Download**")
    input2 = message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

# topic id url = https://elearn.crwilladmin.com/api/v1/comp/batch-topic/881?type=class&token=d76fce74c161a264cf66b972fd0bc820992fe576
    url2 = requests.get("https://elearn.crwilladmin.com/api/v1/comp/batch-topic/"+raw_text2+"?type=class&token="+token)
    topicid = url2.json()["data"]["batch_topic"]
    bn =url2.json()["data"]["batch_detail"]["name"]
    await m.reply_text(f'Batch details of **{bn}** are :')
    cool1 = ""
    for data in topicid:
        t_name=(data["topicName"])
        tid = (data["id"])
        
        urlx = "https://elearn.crwilladmin.com/api/v1/comp/batch-detail/"+raw_text2+"?redirectBy=mybatch&topicId="+tid+"&token="+token
        ffx = requests.get(urlx)
        vcx =ffx.json()["data"]["class_list"]["batchDescription"]
        vvx =ffx.json()["data"]["class_list"]["classes"]
        vvx.reverse()
        zz= len(vvx)
        
       
        hh = f"**Topic -** {t_name}\n**Topic ID - ** ```{tid}```\nno. of videos are : {zz}\n\n"
        
        if len(f'{cool1}{hh}')>4096:
            await m.reply_text(hh)
            cool1=""
        cool1+=hh
    await m.reply_text(cool1)
    await m.reply_text(f'**{vcx}**')

    editable2= await m.reply_text("**Now send the Topic ID to Download**")
    input3 = message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    
    editable3= await m.reply_text("**Now send the Resolution**")
    input4 = message = await bot.listen(editable.chat.id)
    raw_text4 = input4.text

    # editable4= await m.reply_text("Now send the **Thumb url** or send **no**")
    # input6 = message = await bot.listen(editable.chat.id)
    # raw_text6 = input6.text

    # thumb = input6.text
    # if thumb.startswith("http://") or thumb.startswith("https://"):
    #     getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
    #     thumb = "thumb.jpg"
    # else:
    #     thumb == "no"

    
    
    #gettting all json with diffrent topic id https://elearn.crwilladmin.com/api/v1/comp/batch-detail/881?redirectBy=mybatch&topicId=2324&token=d76fce74c161a264cf66b972fd0bc820992fe57
    
    url3 = "https://elearn.crwilladmin.com/api/v1/comp/batch-detail/"+raw_text2+"?redirectBy=mybatch&topicId="+raw_text3+"&token="+token   
    ff = requests.get(url3)
    #vc =ff.json()["data"]["class_list"]["batchDescription"]
    mm = ff.json()["data"]["class_list"]["batchName"]
    
    vv =ff.json()["data"]["class_list"]["classes"]
    vv.reverse()
    #clan =f"**{vc}**\n\nNo of links found in topic-id {raw_text3} are **{len(vv)}**"
    #await m.reply_text(clan)
    count = 1
    try:
        for data in vv:
            vidid = (data["id"])
            lessonName = (data["lessonName"]) 
            bcvid = (data["lessonUrl"][0]["link"])
            
        
            if bcvid.startswith("62"):
                try:
                    video_response = requests.get(f"{bc_url}/{bcvid}", headers=bc_hdr)
                    video = video_response.json()
                    video_source = video["sources"][5]
                    video_url = video_source["src"]
                    #print(video_url)

                    surl=requests.get("https://elearn.crwilladmin.com/api/v1/livestreamToken?type=brightcove&vid="+vidid+"&token="+token)
                    stoken = surl.json()["data"]["token"]
                    #print(stoken)

                    link = video_url+"&bcov_auth="+stoken
                    #print(link)
                except Exception as e:
                    print(str(e))
                
            else:
                link="https://www.youtube.com/embed/"+bcvid
            # await m.reply_text(link)

            #editable3= await m.reply_text("**Now send the Resolution**")
            #input4 = message = await bot.listen(editable.chat.id)
            #raw_text4 = input4.text

            cc = f"**{count}) Title :** {lessonName}\n\n**Quality :** {raw_text4}\n**Batch :** {mm}\n\n**THESE VIDEOS ARE NOT FOR SELLING PURPOSE**"
            Show = f"**Downloading:-**\n```{lessonName}\nQuality - {raw_text4}```\n\n**Url :-** ```{link}```"
            prog = await m.reply_text(Show)

            if "youtu" in link:
                if raw_text4 in ["144", "240", "480"]:
                    ytf = f"'bestvideo[height<={raw_text4}][ext=mp4]+bestaudio[ext=m4a]'"
                elif raw_text4 == "360":
                    ytf = 18
                elif raw_text4 == "720":
                    ytf = 22
                else:
                    ytf = 18
            else:
                ytf=f"bestvideo[height<={raw_text4}]"

            try:
                
                
                cmd = f'yt-dlp -o "{lessonName}.mp4" -f "{ytf}+bestaudio" "{link}"'
                download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                os.system(download_cmd)
            

                filename = f"{lessonName}.mp4"
                subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:19 -vframes 1 "{filename}.jpg"', shell=True)
                
                
                # thumbnail = f"{filename}.jpg"
                try:
                    if thumb == "":
                        thumbnail = f"{filename}.jpg"
                    else:
                        thumbnail = thumb
                except Exception as e:
                    print(e)



                dur = int(helper.duration(filename))

                await m.reply_video(f"{lessonName}.mp4",caption=cc, supports_streaming=True,height=720,width=1280,thumb=thumbnail,duration=dur)
                count +=1
                os.remove(f"{lessonName}.mp4")
                await prog.delete (True)
                os.remove(f"{filename}.jpg")
            except Exception:
                continue

    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Done")
        
        
        





        
                
        














bot.run()
