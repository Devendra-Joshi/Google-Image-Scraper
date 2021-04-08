import requests
import os
from bs4 import BeautifulSoup
import json
import user_agent

agent = user_agent.generate_user_agent(os=None, navigator=None, platform=None, device_type=None)
usr_agent={
    'User-Agent':agent,
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,8/8;q=0.8',
    'Accept_Charset':'ISO-8859-1,ytf-8;q=0.7,8;q=0.3',
    'Accept-Encoding':'none',
    'Accept-Language':'en-US,en;q=0.8',
    'connection':'keep-alive',
}

def main():

  SAVE_FOLDER = input("Enter the keyword: ")
  if not os.path.exists(SAVE_FOLDER):
      os.mkdir(SAVE_FOLDER)
  download_images(SAVE_FOLDER)


def download_images(SAVE_FOLDER):

  data = SAVE_FOLDER
  data= data.split()
  data='+'.join(data)

  print('Start searching.....')
  searchurl = 'https://www.google.com/search?q=' + data + '&source=lnms&tbm=isch'

  try:
    response = requests.get(searchurl, headers=usr_agent)
    response.raise_for_status()
  except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
  except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
  except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
  except requests.exceptions.RequestException as err:
    print ("OOps: Something Else",err)

  # request url, without usr_agent, the permission gets denied
  response = requests.get(searchurl, headers=usr_agent)

  soup = BeautifulSoup(response.text, 'html.parser')
  results = soup.findAll('img')

  # gathering requested number of list of image links with data-src attribute
  # continue the loop in case query fails for non-data-src attributes
 
  links = []
  for res in results:
      try:
          link = res['data-src']
          links.append(link)


      except KeyError:
          continue

  print(f'Downloading {len(links)} images....')

  # Access the data URI and download the image to a file
  for i, link in enumerate(links):
      response = requests.get(link)

      image_name = SAVE_FOLDER + '/' + data + str(i + 1) + '.jpg'
      with open(image_name, 'wb') as raw_img:
          raw_img.write(response.content)

if __name__=='__main__':
    main()
