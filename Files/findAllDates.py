import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta, date
import os

today = datetime.today()
ohanaLink = ("https://disneyworld.disney.go.com/dining/polynesian-resort/ohana/")

try: # finds ChromeDriver based on user
    userName = os.getlogin()
    if userName == "Brandon":
        print("Current user "+userName)
        driver = webdriver.Chrome(executable_path=r'C:\Users\Brandon\AppData\Local\Programs\Python\Python38-32\chromedriver.exe') 
    if userName == "Jimmy Bowden":
        print("Current user "+userName)  
        driver = webdriver.Chrome(executable_path=r'C:\Users\Jimmy Bowden\AppData\Local\Programs\Python\Python37-32\chromedriver.exe')
except:
    print("An error occured identifying ChromeDriver.")

try: # go to the URL
    driver.get(ohanaLink)
    driver.set_window_position(0, 0)
    driver.set_window_size(1024, 1400)
    time.sleep(0.5)
except:
    print('An error occured when picking party size and time.')

try: #pick the time
    reqTime = ("dinner")
    driver.find_element_by_class_name("select-toggle").click()
    time.sleep(0.25)
    driver.find_element_by_css_selector ('ol > li[aria-label="%s"]' % reqTime).click()
    time.sleep(0.25)
    print("Successfuly picked %s as the time." % (reqTime))
except:
    print("An error occured when picking the time.")

try: # pick the party size
    partySize = (4)
    driver.find_element_by_xpath('//*[@aria-owns="partySize-dropdown-list"]').click()
    time.sleep(0.25)
    driver.find_element_by_css_selector ('ol > li[data-display="%s"]' % partySize).click()
    time.sleep(0.25)
    print("Successfully picked %s as the party size." % (partySize))
except:
    print("An error occured when picking the party size.")

x = 3
while True:
    currDate = (today + timedelta(days=x))
    currWeekDay = currDate.strftime("%A")
    currMonth = currDate.strftime("%B")
    currDay = currDate.strftime("%d").replace('0', '')
    currYear = currDate.strftime("%Y")
    fullDate = ("%s, %s %s, %s" % (currWeekDay, currMonth, currDay, currYear))

    print("Full date = %s" % fullDate)
    try: # open date menu
        time.sleep(1)
        driver.find_element_by_class_name("calendarMonth-finderDetailsDining").click()
        time.sleep(0.25)
        siteMonth = driver.find_element_by_class_name("ui-datepicker-month").get_attribute("innerHTML")
    except:
        print("There was an determining the site month.")

    try: # logic for if the month has changed
        while siteMonth != currMonth:
            time.sleep(1)
            driver.find_element_by_class_name("ui-icon-circle-triangle-e").click() # Goes to next month
            time.sleep(0.25)
            siteMonth = driver.find_element_by_class_name("ui-datepicker-month").get_attribute("innerHTML")
            time.sleep(0.25)
            print("Clicked next month")
        print("Current month %s and site month %s " % (currMonth, siteMonth))
    except:
        print("We encountered an error selecting the correct month.")

    try: # clicks correct date
        time.sleep(1)
        driver.find_element_by_xpath('//*[@aria-label="%s"]' % fullDate).click() # click date
        time.sleep(0.25)
        print("Date selected")
        driver.find_element_by_id("dineAvailSearchButton").click() # Click search times button
        print("Search button clicked")
        time.sleep(8)
    except:
        print("We encountered a problem selecting the day")

    try: # if available dates
        if driver.find_element_by_class_name("ctaNoAvailableTimesContainer"):
            print("No available times.")
        else: #not working **************************************************************
            times = (driver.find_element_by_css_selector('timesContainer > div.ctaAvailableTimesContainer > div > a > span > span > span').innerHTML)
            print(times)
    except:
        print("An error occured gathering available times")
    x = x + 1
    print("Waiting 3 seconds to loop")
    time.sleep(3)
driver.quit()

#timesContainer > div.ctaAvailableTimesContainer > div > a > span > span > span