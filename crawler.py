from bs4 import BeautifulSoup as bs
from selenium import webdriver as  wb
from selenium.webdriver.common.keys import Keys
import time
from urllib.request import urlretrieve
import os

class Crawler:

    # constructor
    def __init__(self):
        self.keyword = str(input('keyword... : '))  # image keyword for searching
        self.dirPath = ""                           # image stored directory
    
    # create directory for download if it is not exist
    def createNewDirectory(self):
        cwd = os.getcwd()
        print("current working directory : " + cwd)
        self.dirPath = os.path.join(cwd, self.keyword)
        print("new directory path : " + self.dirPath)

        if not os.path.exists(self.dirPath):
            os.mkdir(self.dirPath)

    # create the url path    
    def createURL(self):
        url = 'https://www.google.com/search?q=' + self.keyword + '&source=lnms&tbm=isch'
        return url

    def searchURL(self, url):
        driver = wb.Chrome()
        driver.get(url)

        body = driver.find_element_by_tag_name('body')
        btn_more = driver.find_element_by_class_name('mye4qd')

        for num in range(10):
            try:
                btn_more.click()
                time.sleep(0.5)
            except:
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)
                
        soup = bs(driver.page_source, 'lxml')
        img = soup.select('img.rg_i')
        img[2]['src']

        self.img_src = []
        print(str(len(img)))

        for i in img:
            try:
                img_temp = i['src']
                self.img_src.append(img_temp)
            except:
                try:
                    img_temp = i['data-src']
                    self.img_src.append(img_temp)
                except:
                    continue
                
    # download the image
    def downloadImage(self):
        file_no = 0
        count = 0

        print('dirpath: '+self.dirPath)

        for j in range(len(self.img_src)):

            try:
                urlretrieve(self.img_src[j], self.dirPath + '/' + str(file_no) + '.jpg')
                # \를 2개씩으로 바꿈
            except:
                print(str(file_no)+" is error")
                continue
                
            file_no += 1
            time.sleep(1)
            
            print(str(file_no)+" is saving")

    def run(self):
        self.createNewDirectory()           # 1. create the directory
        url = self.createURL()              # 2. create the path
        self.searchURL(url)       # 3. search image
        self.downloadImage()         # 4. download image
