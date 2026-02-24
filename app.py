import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import logging
import pymongo
import os

save_dir = "images/"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

query="Tiger"

response = requests.get( f"https://www.google.com/search?q={query}&tbm=isch")

print("Address of response web page",response)
# print(response.content) # this gave whole html content modify it 
soup=BeautifulSoup(response.content,'html.parser')
# print(soup) 

#------ finding image url
images_tags=soup.find_all("img") # all images url
print(len(images_tags))

# first tag is header so delete in images_tags
del images_tags[0]

# now we iterate in images tags for url
img_data_mongo=[]
for img in images_tags:
    image_url=img['src']
    image_data=requests.get(image_url).content
    mydict = {"index":image_url,"image":image_data}
    img_data_mongo.append(mydict)
    with open(os.path.join(save_dir,f"{query}_{images_tags.index(img)}.jpg"),"wb") as f :
               f.write(image_data)

# mongo db

client = pymongo.MongoClient("mongodb+srv://Dipak_mongo:Dipak12345@cluster0.nfh2qpm.mongodb.net/?appName=Cluster0")
db = client['image_scrap']
coll_img=db["image_scrap"]
# insert data
coll_img.insert_many(img_data_mongo)
  