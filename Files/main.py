import time
from datetime import datetime, timedelta, date
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

'''
Todo:
Add error checking for chrome version and webdriver location based on user
Remove time.sleeps and have the program wait for elements to load using a loop 
build GUI and generate variables for the link, dates, times via drop down menus
add all possibilities to dictionaries for (links/restaurants), dates and times for each restaurants into dicts to populate the drop down menus
expand on the notifications of an openin
hide the browser
finally build into executable with py.exe
'''
ohanaLink = ("https://disneyworld.disney.go.com/dining/polynesian-resort/ohana/") # change this based on user GUI drop down menu options
# WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

try: # finds ChromeDriver based on user
    userName = os.getlogin()
    if userName == "Brandon":
        driver = webdriver.Chrome(executable_path=r'C:\Users\Brandon\AppData\Local\Programs\Python\Python38-32\chromedriver.exe') 
except:
    print("An error occured identifying ChromeDriver.")

try: # go to the URL
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #driver = webdriver.Chrome(options=chrome_options)
    driver.get(ohanaLink)
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
except:
    print('An error occured when picking party size and time.')

try: #pick the time
    reqTime = ("dinner") # change this based on user GUI drop down menu options
    driver.find_element_by_class_name("select-toggle").click()
    time.sleep(0.25)
    driver.find_element_by_css_selector ('ol > li[aria-label="%s"]' % reqTime).click()
    time.sleep(0.25)
except:
    print("An error occured when picking the time.")

try: # pick the party size
    partySize = (4) # change this based on user GUI drop down menu options
    driver.find_element_by_xpath('//*[@aria-owns="partySize-dropdown-list"]').click()
    time.sleep(0.25)
    driver.find_element_by_css_selector ('ol > li[data-display="%s"]' % partySize).click()
    time.sleep(0.25)
except:
    print("An error occured when picking the party size.")


try:
    requiredDate = datetime.date(2020, 4, 13) # change this based on user GUI drop down menu options
    currWeekDay = requiredDate.strftime("%A")
    currMonth = requiredDate.strftime("%B")
    currDay = requiredDate.strftime("%d").replace('0', '')
    currYear = requiredDate.strftime("%Y")
    fullDate = ("%s, %s %s, %s" % (currWeekDay, currMonth, currDay, currYear))
    try: # open date menu
        time.sleep(1)
        driver.find_element_by_class_name("calendarMonth-finderDetailsDining").click()
        time.sleep(0.25)
        siteMonth = driver.find_element_by_class_name("ui-datepicker-month").get_attribute("innerHTML")
    except:
        print("There was an determining the site month.")

    try: # logic for if the month has changed
        while siteMonth != currMonth:
            driver.find_element_by_class_name("ui-icon-circle-triangle-e").click() # Goes to next month
            time.sleep(0.25)
            siteMonth = driver.find_element_by_class_name("ui-datepicker-month").get_attribute("innerHTML")
            time.sleep(0.25)
    except:
        print("We encountered an error selecting the correct month.")

    try: # choses date from open date menu - the page does not refresh so we only need to open this once
        time.sleep(1)
        driver.find_element_by_xpath('//*[@aria-label="%s"]' % fullDate).click() # click date
        time.sleep(0.25)
    except:
        print("An error occured clicking the date")
except:
    print("An error occured when selecting the month")


while True: # main loop 
    try: # clicks search button
        time.sleep(2.5)
        driver.find_element_by_id("dineAvailSearchButton").click() # Click search times button
        time.sleep(7.5) # change this to wait for loading element to dissapear
    except:
        print("We encountered a problem selecting the day") 
    try: # case no dates
        if driver.find_element_by_class_name("ctaNoAvailableTimesContainer"):
            time.sleep(0.05)
    except:
        time.sleep(0.05)
    try: # case dates
        if driver.find_element_by_class_name("pillLink"):
            availbility = driver.find_element_by_class_name("pillLink").text
            print("There is an opening at %s on %s." % (availbility, fullDate))
            input("Hit enter to continue searching... ")
    except:
        print("Error with an opening")
driver.quit()
