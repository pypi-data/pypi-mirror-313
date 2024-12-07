"""
    This is not working at all, it could be removed in a near future.
"""
from utils.downloader.image import download_by_url
from utils.scrapper.chrome import start_chrome, go_to_and_wait_loaded
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from objects.google_image_scraper import GoogleImageScraper

import urllib.request
import urllib
import urllib.parse
import imghdr
import posixpath
import re
import time
from itertools import filterfalse


IMAGE_FILE_EXTENSIONS = ['jpe', 'jpeg', 'jfif', 'exif', 'tiff', 'gif', 'bmp', 'png', 'webp', 'jpg']

class Bing:
    # Based on this (https://github.com/gurugaurav/bing_image_downloader/blob/master/bing_image_downloader/bing.py), but modified to my own purpose
    __instance = None

    def __new__(cls, ignore_repeated = True):
        if not Bing.__instance:
            Bing.__instance = object.__new__(cls)
        
        return Bing.__instance

    def __init__(self, output_dir, adult = '', timeout = 100,  filter = '', ignore_repeated = True):
        self.download_count = 0
        self.output_dir = output_dir
        self.adult = adult
        self.filter = filter
        self.ignore_repeated = ignore_repeated
        self.seen = set()
        self.downloaded_urls = set()

        self.timeout = timeout

        self.page_counter = 0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
            'AppleWebKit/537.11 (KHTML, like Gecko) '
            'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

    def activate_ignore_repeated(self):
        self.ignore_repeated = True

    def deactivate_ignore_repeated(self):
        self.ignore_repeated = False

    def __get_filter(self, shorthand):
            if shorthand == "line" or shorthand == "linedrawing":
                return "+filterui:photo-linedrawing"
            elif shorthand == "photo":
                return "+filterui:photo-photo"
            elif shorthand == "clipart":
                return "+filterui:photo-clipart"
            elif shorthand == "gif" or shorthand == "animatedgif":
                return "+filterui:photo-animatedgif"
            elif shorthand == "transparent":
                return "+filterui:photo-transparent"
            else:
                return ""
            
    def __get_url(self, query, limit):
        """
        Returns the url to search the provided 'query' to get 'limit' images.
        """
        query = urllib.parse.quote_plus(query)

        # This below works
        #return 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(query) + '&first=' + str(self.page_counter) + '&count=' + str(limit) + '&adlt=' + self.adult + '&qft=' + ('' if self.filter is None else self.__get_filter(self.filter))

        #url = 'https://www.google.com/search?q=' + query + '&sca_esv=ff48bec18c46a1e3&udm=2&biw=1368&bih=785&sxsrf=ACQVn0-wIFIFwKpRcfa_i7u23WlweS5fMg%3A1711107979098&ei=i2_9ZZrBBYmPxc8P2d2o8Aw&ved=0ahUKEwjaspD65YeFAxWJR_EDHdkuCs4Q4dUDCBA&uact=5&oq=cristiano+ronaldo&gs_lp=Egxnd3Mtd2l6LXNlcnAiEWNyaXN0aWFubyByb25hbGRvMgUQABiABDIKEAAYgAQYigUYQzIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAESOAQUABYmxBwAXgAkAEAmAHeAaABuBWqAQYwLjE0LjK4AQPIAQD4AQGYAhGgAsYWwgIEECMYJ8ICCRAAGIAEGBgYCpgDAJIHBjEuMTMuM6AHwVM&sclient=gws-wiz-serp#vhid=-7UHW1Lud3bYdM&vssid=mosaic'

        # Last week and >800x800 images
        #return 'https://www.bing.com/images/search?q=' + query + '&qft=+filterui:age-lt10080+filterui:imagesize-custom_800_800&form=IRFLTR&first=1'

        return 'https://www.bing.com/images/search?q=' + query + '&go=Buscar&qs=ds&form=QBILPG&first=1'

        return 'https://www.bing.com/images/search?q=' + urllib.parse.quote_plus(query) + '&form=HDRSC3&first=1'

    """
    def save_image(self, link, file_path):
        request = urllib.request.Request(link, None, self.headers)
        image = urllib.request.urlopen(request, timeout = self.timeout).read()
        if not imghdr.what(None, image):
            print('[Error]Invalid image, not saving {}\n'.format(link))
            raise ValueError('Invalid image, not saving {}\n'.format(link))
        with open(str(file_path), 'wb') as f:
            f.write(image)
    """
    
    def download_image(self, link, output_filename):
        """
        This methods downloads the provided 'link' image and stores locally as
        'output_filename'. It will return the final filename with which it has
        been downloaded (as it can change due to wrong extension).
        """
        self.download_count += 1
        # Get the image link
        try:
            path = urllib.parse.urlsplit(link).path
            filename = posixpath.basename(path).split('?')[0]
            file_type = filename.split('.')[-1]
            if file_type.lower() not in IMAGE_FILE_EXTENSIONS:
                file_type = 'jpg'
                
            # We fix the extension if it is wrong
            if '.' in output_filename:
                extension = output_filename.split('.')[1]
                if extension != file_type:
                    output_filename.replace(extension, '.' + file_type)
            else:
                output_filename += '.' + file_type

            download_by_url(link, output_filename)
            # We append this link to avoid downloading it again
            self.downloaded_urls.add(link)

        except Exception as e:
            self.download_count -= 1
            print("[!] Issue getting: {}\n[!] Error:: {}".format(link, e))

        return output_filename

    def find_chrome(self, keywords, number_of_images):
        """
        image_scraper = GoogleImageScraper('', 'wip/', keywords, number_of_images)
        image_urls = image_scraper.find_image_urls()
        image_scraper.save_images(image_urls)

        return
        """
        # TODO: This is not working
    

        driver = start_chrome(True)
        #url = url = self.__get_url(keywords, 100)
        url = 'https://www.google.com/search?sca_esv=39bd196d7b057ff4&hl=es&sxsrf=ACQVn0-8K1iFPGSxADM3D9TRk5lpkoEV5A:1711109110553&q=' + keywords + '&uds=AMwkrPufgvfzFeIw5yilA4Gzc5SO9lVaLhgRHmmyPgNVqiyWpt_hRF_KcRkqwX4V1Ixye4HvydlY1Cv-RxhicPyEkaYN9AhDv9yeDfVCM1kWTfhEYzCUH1n5KMkCtCr83dibHEyrsdYFB09rfewbV-2PsHlpAxQkUqcQqO0Nswl38TiDcmJN_z4J94SD8eKY0Yx6_Aa2qTAWyLHuYV-xlZhimJRxB_QS2iSu6RC2hCa8GCd9HzMh8cubNzVF8XaauXGMqfjxBM-bVMAcgsvIHv6z7QwKxUFe6WRZkSTWMfpK8jlWaFprdh9pcL-iiNebRsbohdq5ESfr&udm=2&prmd=invsbmtz&sa=X&ved=2ahUKEwjJ7dKV6oeFAxX8XfEDHTpqAuIQtKgLegQIDRAB&biw=1368&bih=785&dpr=2'
        go_to_and_wait_loaded(driver, url)
        time.sleep(10)

        #href="https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fe%2Fef%2FIbai_Llanos_in_2020.jpg&amp;tbnid=oA2nnqJVRGvgrM&amp;vet=12ahUKEwi73cLrgoiFAxVVov0HHRs-BdMQMygAegQIARBu..i&amp;imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FIbai_Llanos&amp;docid=7HS4A3h3iDalNM&amp;w=620&amp;h=680&amp;q=ibai&amp;hl=es&amp;ved=2ahUKEwi73cLrgoiFAxVVov0HHRs-BdMQMygAegQIARBu"

        # https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fe%2Fef%2FIbai_Llanos_in_2020.jpg&tbnid=oA2nnqJVRGvgrM&vet=12ahUKEwje6vS-gYiFAxXtnf0HHar3C7YQMygAegQIARBv..i&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FIbai_Llanos&docid=7HS4A3h3iDalNM&w=620&h=680&q=ibai&hl=es&ved=2ahUKEwje6vS-gYiFAxXtnf0HHar3C7YQMygAegQIARBv

        #elements = driver.find_elements(By.XPATH, "//a[contains(@href,'/imgres?q=')]")
        #elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'https://www.google.com/imgres?')]")
        #elements = driver.find_elements(By.XPATH, "//h3[contains(@class, 'ob5Hkd')]")#/*[1]
        #elements = driver.find_elements(By.CLASS_NAME, 'ob5Hkd')
        #elements = driver.find_elements(By.TAG_NAME, 'a')
        #elements = driver.find_elements(By.XPATH, "//a[contains(@data-navigation, 'server')]")#/*[1]
        #elements = driver.find_elements(By.XPATH, '//div[contains(@role, "list-item")]')
        # press tab 40 times and get focused
        actions = ActionChains(driver) 
        actions.send_keys(Keys.TAB * 50)
        actions.perform()
        elem = driver.switch_to.active_element
        print(elem.tag_name)
        elem.click()
        time.sleep(2)
        eless = driver.find_element(By.XPATH, '//a[contains(@aria-hidden, "false")]')
        print(len(eless))
        print(eless[0].get_attribute('href'))
        if elem.tag_name == 'a':
            print(elem.get_attribute('href'))
            print(elem.text)
        time.sleep(60)
        return []
        for element in elements:
            href = element.get_attribute('href')
            if href:
                print(href)
                if '/imgres' in href:
                    print(href)
            else:
                print(element.text)
        return []
        urls = []
        for element in elements:
            # Url is like this one:
            # https://www.google.com/imgres?q=cristiano%20ronaldo&imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fd%2Fd7%2FCristiano_Ronaldo_playing_for_Al_Nassr_FC_against_Persepolis%252C_September_2023_%2528cropped%2529.jpg&imgrefurl=https%3A%2F%2Fes.wikipedia.org%2Fwiki%2FCristiano_Ronaldo&docid=ty38cmTK8QLflM&tbnid=AB35wZltZBgFqM&vet=12ahUKEwjc_uGW6oeFAxVcQ_EDHXxbBF4QM3oECBYQAA..i&w=805&h=1053&hcb=2&itg=1&ved=2ahUKEwjc_uGW6oeFAxVcQ_EDHXxbBF4QM3oECBYQAA
            url = element.get_attribute('src')
            url = url.split('&')[1] # imgurl=...
            url = url.split('=')[1]
            url = urllib.parse.unquote(url)
            urls.append(url)

        return urls

    def find(self, keywords, number_of_images):
        """
        This will look for 'number_of_images' images using the Bing browser and will
        return their links. This method will skip the previously downloaded images
        to avoid duplicities, if that options is active.
        """
        driver = start_chrome()
        url = url = self.__get_url(keywords, 100)
        go_to_and_wait_loaded(driver, url)
        buttons = driver.find_elements(By.XPATH, "//img[contains(@class, 'mimg')]")
        links = []
        for button in buttons:
            links.append(button.get_attribute('src'))

        if self.ignore_repeated:
            links = list(filterfalse(self.downloaded_urls.__contains__, links))

        # Force limit here
        links = links[:number_of_images]

        return links

        # I force the 'limit' to be 100 and then I manually remove
        url = self.__get_url(keywords, 100)
        request = urllib.request.Request(url, None, headers = self.headers)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf8')
        if html ==  "":
            return None
        
        # TODO: Implement a way of requesting in other pages
        # This below works with the first option in '__get_url()'
        #links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)
        links = re.findall('src2=&quot;(.*?)&quot;', html)

        if self.ignore_repeated:
            links = list(filterfalse(self.downloaded_urls.__contains__, links))

        # Force limit here
        links = links[:number_of_images]

        return links
    
    def find_and_download(self, keywords, number_of_images):
        """
        This will look for 'number_of_images' images using the Bing browser and will
        download those images. This method will skip the previously downloaded images
        to avoid duplicities, if that options is active.
        """
        #urls = self.find(keywords, number_of_images)
        urls = self.find(keywords, number_of_images)
        for url in urls:
            self.download_image(url)
    
    """
    def run(self):
        while self.download_count < self.limit:
            # Parse the page source and download pics
            request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(self.query) \
                          + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                          + '&adlt=' + self.adult + '&qft=' + ('' if self.filter is None else self.__get_filter(self.filter))
            request = urllib.request.Request(request_url, None, headers=self.headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf8')
            if html ==  "":
                print("[%] No more images are available")
                break
            links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)

            for link in links:
                if self.download_count < self.limit and link not in self.seen:
                    self.seen.add(link)
                    self.download_image(link)

            self.page_counter += 1
    """