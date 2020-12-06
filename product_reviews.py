
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from selenium import webdriver
import re
import time
from predict import Predict_ECommerce_Review

def valid_flipkart_url(link):
    regex = re.compile(r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?flipkart+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")
    
    return regex.search(link)

#link = 'https://www.flipkart.com/oneplus-bullets-wireless-z-bluetooth-headset/product-reviews/itm0fa6e667285c4?pid=ACCFR3Q77R6RRGAC&lid=LSTACCFR3Q77R6RRGAC2RJOEB&marketplace=FLIPKART'

#link = input("Enter Link : ")

def create_output(link):
    if (link != None and valid_flipkart_url(link)):
        options = webdriver.ChromeOptions()
        options.headless = True
        prefs = {"profile.default_content_setting_values.notifications":2}
        options.add_experimental_option("prefs",prefs)

        driver = webdriver.Chrome('chromedriver.exe',options=options)
        driver.maximize_window()
        time.sleep(5)

        driver.get(link) 
        time.sleep(1)
        [item.click() for item in driver.find_elements_by_class_name("_1BWGvX")]
        time.sleep(1)
        #page = requests.get(driver.current_url)

        #print(page.content)

        soup = bs(driver.page_source,'html.parser')
        #print(soup.prettify())
        df = pd.DataFrame(columns=['Review_Title','Review_Text'])
        review_cards = soup.find_all('div',{"class":"col _2wzgFH K0kLPL"})
        #total_cards = len(review_cards)
        for card in review_cards:
            #cust_name = card.find('p',{"class":"_3LYOAd _3sxSiS"})
            review_title = card.find('p',{"class":"_2-N8zT"})
            if (review_title != None):
                review_title = review_title.text
            else:
                review_title = ''
            review_body = card.find("div",{"class":"t-ZTKy"}).find("div").find("div")
            if (review_body != None):
                review_body = review_body.text
                #review_body = review_body.lstrip('\n').rstrip('\n')
            else:
                review_body = ''
            
            
            df = df.append({
                            'Review_Title':review_title,
                            'Review_Text':review_body,
                        },ignore_index=True)
        df.to_csv('reviews.csv',index=True)
        driver.quit()

        df = Predict_ECommerce_Review("reviews.csv")
        result = [{
                    'review_title':row['Review_Title'],
                    'review_body':row['Review_Text'],
                    'sentiment':row['Sentiment'],
                    'authenticity':row['Authenticity']
                } for _, row in df.iterrows()]
        return result

    else:
        print("Either blank or wrong url")

#print(create_output(link))