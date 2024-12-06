from bing_image_downloader.bing import Bing
from google_images_download import google_images_download

import re
import urllib


def test(keywords, images_number, output_folder):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
        'AppleWebKit/537.11 (KHTML, like Gecko) '
        'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    #gid = google_images_download()
    #gid.download(keywords = keywords, size = 'large', aspect_ratio = 'panoramic')
    
    #bing = Bing(keywords, images_number, output_folder, False, 100, False, False)
    # Parse the page source and download pics
    request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(keywords) \
                    + '&first=' + '0' + '&count=' + str(images_number) \
                    + '&adlt=' + 'False' + '&qft=' + 'False'
    request = urllib.request.Request(request_url, None, headers = HEADERS)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf8')
    if html ==  "":
        return None
    links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)
    for link in links:
        print(link)
        #if self.download_count < self.limit and link not in self.seen:
            #self.seen.add(link)
            #self.download_image(link)


    # download(keywords, limit = images_number, output_dir = output_folder)
