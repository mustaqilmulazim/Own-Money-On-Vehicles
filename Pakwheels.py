from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import xlwt
import pandas


options = webdriver.ChromeOptions()
options.headless = False
mypath = ''
driver = webdriver.Chrome(executable_path=mypath, \
    chrome_options=options)


"""
    - The function below, when called, opens up the browser and goes to wwww.pakwheels.com and then navigates to their
      used cars section.
      
    - It then inserts queries into their query bar such as:
      Car Make Model
      City
      Price Range
      From - To Year
      
    - Finally it clicks on the search button and the page with the inserted criteria opens 
"""


def navigation(vehicle = []):
    driver.get("https://www.pakwheels.com")

    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'onesignal-slidedown-cancel-button')))
        driver.find_element_by_id('onesignal-slidedown-cancel-button').click()
    except:
        print ("No initial banner")

    time.sleep(3)
    driver.find_element_by_link_text('Used Cars').click()
    driver.find_element_by_id('more_option').click()
    driver.find_element_by_name('home-query').send_keys(vehicle)
    yr_from = Select(driver.find_element_by_id('YearFrom'))
    yr_to = Select(driver.find_element_by_id('YearTo'))
    yr_from.select_by_value('2021')
    yr_to.select_by_value('2021')

    driver.find_element_by_id("reg_in_chzn").click()
    
    time.sleep(10)
    driver.find_element_by_id("reg_in_chzn").click()
    driver.find_element_by_id("reg_in_chzn_o_2").click()

    seller_type = Select(driver.find_element_by_id('ads_type'))
    time.sleep(5)
    seller_type.select_by_value('2')

    driver.find_element_by_id('used-cars-search-btn').click()


'''

    - This function gets all the required links.
    
    - Firstly it gets all the Anchor tags that has the required links (class = "car-name ad-detail-path")
    
    - Then through the for-loop, it further parses the anchor tags to get the href from the anchor tags one by one and appends it to another list called as links and returns that list.
    

'''
def get_car_links(vehicle = []):
        
    items=driver.find_elements_by_class_name('classified-listing   ')

    l_files = []

    for item in items:
        l_files.append(item.text.split('\n'))

    try:
        while driver.find_element_by_class_name('next_page'):
            driver.find_element_by_class_name('next_page').click()
            time.sleep(10)
            items=driver.find_elements_by_class_name('classified-listing   ')

            for item in items:
                l_files.append(item.text.split('\n'))
    except:
        print ("Pages done")

    df = pandas.DataFrame(data=l_files)
    df.to_csv(vehicle + ".csv")

try:
    print('Starting')   

    vehicles = ['Toyota Yaris', 'Suzuki Wagon R', 'Toyota Fortuner', 'KIA Picanto', \
        'Suzuki Swift', 'Toyota Land Cruiser', 'KIA Sportage', \
            'Hyundai Tucson', 'Honda BR-V', 'MG HS']

    for vehicle in vehicles:
        # Open used car pages
        navigation(vehicle=vehicle)
        
        # Open pages for each car type and download and store information
        get_car_links(vehicle=vehicle)
    
finally:
    print('Done')
    driver.quit()
