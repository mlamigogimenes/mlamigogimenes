# This code was done using the one in this page 'https://www.thepythoncode.com/article/get-youtube-data-python'

from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs # importing BeautifulSoup
import pandas as pd
import json


# sample youtube video url
video_url = 'https://youtu.be/zjDsnyaRA3M '
# init an HTML Session
session = HTMLSession()
# get the html content
response = session.get(video_url)
# execute Java-script
response.html.render(sleep=1)
# create bs object to parse HTML
soup = bs(response.html.html, "html.parser")

video_metadata = {}
video_metadata["title"] = str(soup.find("meta", itemprop="name")['content'])
video_metadata["views"] = str(soup.find("meta", itemprop="interactionCount")['content'])
video_metadata["description"] = soup.find("meta", itemprop="description")['content']
video_metadata["date_published"] = soup.find("meta", itemprop="datePublished")['content']
video_metadata["duration"] = soup.find("span", {"class": "ytp-time-duration"}).text
video_metadata["tags"] = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])

channel_metadata = {}
channel_tag = soup.find("meta", itemprop="channelId")['content']
channel_metadata['channel_tag '] = list(soup.find("meta", itemprop="channelId")['content'])
channel_metadata['channel_name '] = soup.find("span", itemprop="author").next.next['content']
channel_metadata['channel_url '] = f"https://www.youtube.com/{channel_tag}"

#video_metadata = [str(soup.find("meta", itemprop="name")['content']), str(soup.find("meta", itemprop="interactionCount")['content']), str(soup.find("meta", itemprop="datePublished")['content']), str(soup.find("span", {"class": "ytp-time-duration"}).text)]
#video_metadata_dict = {}

#video_metadata_dict['Name'] = video_metadata[0]
#video_metadata_dict['Views'] = video_metadata[1]
#video_metadata_dict['Date'] = video_metadata[2]
#video_metadata_dict['Duration'] = video_metadata[3]

#print(video_metadata_dict)
df_v = pd.DataFrame.from_records(video_metadata, index=[0])
df_v.to_excel('youtube_scrapping_video.xls',index=False)

df_c = pd.DataFrame.from_records(channel_metadata)
df_c.to_excel('youtube_scrapping_channel.xls',index=False)