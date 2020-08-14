import tweepy
from PIL import Image
import requests
from io import BytesIO
import time

consumer_key = '2JvZtXuAY7azndLVw4ilGLTPD'
consumer_secret = 'trusSYKWafvcvXsHHdw7H4czRL2y5pyoFgLhzu4ISkuOmykGbb'
access_key = '1293881066973929472-CddkLQDqabsRU3bTUdBtYqXqT1YzbX'
access_secret = 'rpGg1RViL0twToXKiOBokPgDMZFhgVeWBCAoX7H3xKz4x'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_tweets():
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id)
    
    for mention in reversed(mentions) :
        if 'media' in mention.entities and mention.entities['media'][0]['type'] == 'photo' :
            
            photo_url = mention.entities['media'][0]['media_url']
            response = requests.get(photo_url)
            img = Image.open(BytesIO(response.content))
            
            width, height = img.size   # Get dimensions
            if width != height :
                if width>height :
                    new_width = height
                    new_height=height
                elif width<height :
                    new_width=width
                    new_height=width
                    
                left = (width - new_width)/2
                top = (height - new_height)/2
                right = (width + new_width)/2
                bottom = (height + new_height)/2
    
                # Crop the center of the image
                img = img.crop((left, top, right, bottom))
                width, height = img.size
            
            if 'hmif' in mention.text.lower():
                overlay_url='https://i.ibb.co/LzpZX0P/hmif.png'
                response = requests.get(overlay_url)
                overlay = Image.open(BytesIO(response.content))
                overlay = overlay.resize((width,height))
                overlay.show()
                img.show()
                base=img.copy()
                base.paste(overlay,(0,0),overlay)
                base.save('jadi.jpg')
                print("updating...")
                print(mention.id)
                api.update_with_media(filename='jadi.jpg',
                                      status= "@"+mention.user.screen_name+' '+"here's your edited image!",
                                      in_reply_to_status_id = mention.id)
            elif 'sailor moon' in mention.text.lower() :
                overlay_url='https://i.ibb.co/pjQ95XZ/sailormoon.png'
                response = requests.get(overlay_url)
                overlay = Image.open(BytesIO(response.content))
                overlay = overlay.resize((width,height))
                overlay.show()
                img.show()
                base=img.copy()
                base.paste(overlay,(0,0),overlay)
                base.save('jadi.jpg')
                print("updating...")
                print(mention.id)
                api.update_with_media(filename='jadi.jpg',
                                      status= "@"+mention.user.screen_name+' '+"here's your edited image!",
                                      in_reply_to_status_id = mention.id)
            last_seen_id = mention.id
            store_last_seen_id(last_seen_id, FILE_NAME)
while True:
    reply_tweets()
    time.sleep(10)

            
                
                
                
                
                
            

            
        



