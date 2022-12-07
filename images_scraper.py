from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests 
import time
import os
import uuid
from urllib.parse import urlparse

#Generate random string 
def random_string():
    random = str(uuid.uuid4()) 
    random = random.upper() 
    random = random.replace("-","")  
    return random[0:5] 

#Random string generator for folder name
random_string = str(random_string())

#Driver Settings
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(600,700)

#Generating new folder in working path
def folder_create(url,folder_name,images_name,scroll_count):
    try:
        #Folder name check operations
        if(os.path.isdir(folder_name + random_string) == False):   
            os.mkdir(folder_name + random_string)
        else: 
            print("the folder already exist the same name")
            return
    except:
         print("the folder not create error")
         return
        
    #Starting to fetch images..
    start_download_images(url, folder_name,images_name,scroll_count)


#Fetch images operations
def start_download_images(url, folder_name,images_name,scroll_count):
    current_page = 0
    i = 0
    
    #Driver options
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    
    #Set link in driver
    driver.get(url)
    time.sleep(5)
    
    #Scrolls operations
    while (current_page < scroll_count):
        #fetch all data
        soup = BeautifulSoup(driver.page_source,'html.parser')
        
        #Parse img html
        images = soup.findAll('img')
        
        #Parse and fetch images
        fetchImages(images,i)
        
        #Scroll to end of page
        driver.execute_script("window.scrollTo(1,100000);") 
        
        #Increase page number 
        current_page += 1
        time.sleep(3)
        
        print("Scrolling... page=" + str(current_page))
        #driver.execute_script("scrollBy(0,-500);")
        
#Parse operations
def fetchImages(images,i):
    
    if(len(images) != 0):
        for i,link in enumerate(images):
            #Fetch all images links
            links = link.get('src')
            
            #Image links parsing operations..
            parsed_link = urlparse(links).path
            parse1 = str(parsed_link).translate({ord('/'): None})
            image_names = str(parse1).translate({ord(letter): None for letter in '.jpg'})
            
            #Save the images
            with open(f"{folder_name}{random_string}/{images_name}_" + image_names + ".jpg", "wb+") as f:
                im = requests.get(links)
                f.write(im.content)
    else:
        input("images not found")
        return


def main(url,folder_name,images_name,scroll_count): 
    
    #Create folder and start fetch images
    folder_create(url,folder_name,images_name,scroll_count)
    
    #Shut down the driver
    driver.quit()

#Filter search string
search = "christmasP"

#Page Scrolling count
scroll_count = 10

#Set Folder and images name 
folder_name = search                                               
images_name = search

#Search Url for images
url = f"https://tr.pinterest.com/search/pins/?q={search}"

#Run to main
main(url,folder_name,images_name,scroll_count)