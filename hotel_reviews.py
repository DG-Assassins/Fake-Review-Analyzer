
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from selenium import webdriver
import re
import time
from predict import Predict_Hotel_Review

def valid_trip_advisor_url(link):
    regex = re.compile(r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?tripadvisor+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")
    
    return regex.search(link)

#link = 'https://www.tripadvisor.com/Hotel_Review-g304551-d11561000-Reviews-Roseate_House_New_Delhi-New_Delhi_National_Capital_Territory_of_Delhi.html'

#link = input("Enter Link : ")

def create_hotel_output(link):
    if (link != None and valid_trip_advisor_url(link)):
        options = webdriver.ChromeOptions()
        options.headless = True
        prefs = {"profile.default_content_setting_values.notifications":2}
        options.add_experimental_option("prefs",prefs)

        driver = webdriver.Chrome('chromedriver.exe',options=options)
        driver.maximize_window()
        time.sleep(5)

        driver.get(link) 
        time.sleep(1)
        #[item.click() for item in driver.find_elements_by_class_name("_3maEfNCR")]
        driver.find_element_by_class_name("_3maEfNCR").click()
        time.sleep(1)
        #page = requests.get(driver.current_url)

        #print(page.content)

        soup = bs(driver.page_source,'html.parser')
        #print(soup.prettify())
        df = pd.DataFrame(columns=['Review_Text'])
        review_cards = soup.find_all('div',{"class":"_2wrUUKlw _3hFEdNs8"})
        #total_cards = len(review_cards)
        for card in review_cards:
            #cust_name = card.find('p',{"class":"_3LYOAd _3sxSiS"})
            """
            if (cust_name != None):
                cust_name = cust_name.text
            else:
                cust_name = ''
            """
            """
            review_title = card.find('a',{"class":"ocfR3SKN"}).find("span").find("span")
            if (review_title != None):
                review_title = review_title.text
            else:
                review_title = ''
                """
            """
            review_rating = card.find('div',{"class":"hGSR34 E_uFuv"}) 
            #print(review_rating)
            if (review_rating != None):
                review_rating = review_rating.text
            else:
                review_rating = ''
            """
            review_body = card.find("q",{"class":"IRsGHoPm"}).find("span")
            if (review_body != None):
                review_body = review_body.text
                #review_body = review_body.lstrip('\n').rstrip('\n')
            else:
                review_body = ''
            
            
            df = df.append({
                            'Review_Text':review_body,
                        },ignore_index=True)
        df.to_csv('reviews_hotel.csv',index=True)
        driver.quit()

        df = Predict_Hotel_Review("reviews_hotel.csv")
        result = [{
                    'review_body':row['Review_Text'],
                    'sentiment':row['Sentiment'],
                    'authenticity':row['Authenticity']
                } for _, row in df.iterrows()]
        return result

    else:
        print("Either blank or wrong url")


#print(create_hotel_output(link))