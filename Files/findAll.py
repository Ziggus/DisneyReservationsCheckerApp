import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta, date
import os

userName = os.getlogin()
# changed to remove the need to comment/uncomment depending on user
if userName == "Brandon":
    print("Current user "+userName)
    driver = webdriver.Chrome(executable_path=r'C:\Users\Brandon\AppData\Local\Programs\Python\Python38-32\chromedriver.exe') 
if userName == "Jimmy Bowden":
    print("Current user "+userName)  
    driver = webdriver.Chrome(executable_path=r'C:\Users\Jimmy Bowden\AppData\Local\Programs\Python\Python37-32\chromedriver.exe')

ohanaLink = ("https://disneyworld.disney.go.com/dining/polynesian-resort/ohana/")
months = {'January': 0, 'February': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5, 'July': 6, 'August': 7, 'September': 8, 'October': 9, 'November': 10, 'December': 11}

driver.get(ohanaLink)
time.sleep(1)
today = datetime.today()
y = 1

try: #removed this section from the loop as once these are selected they do not change until the page is loaded
    reqTime = ("dinner")
    partySize = (4)

    driver.find_element_by_class_name("select-toggle").click() # open time menu
    time.sleep(2)
    driver.find_element_by_css_selector ('ol > li[aria-label="%s"]' % reqTime).click() #click time (dinner for testing)
    time.sleep(2)
    print("Time selected")
    driver.find_element_by_xpath('//*[@aria-owns="partySize-dropdown-list"]').click() #open party size menu
    time.sleep(2)
    driver.find_element_by_css_selector ('ol > li[data-display="%s"]' % partySize).click() #works
    print("Party size selected")
except:
    print('An error occured.')

while y < 180: # start loop (has to start at tomorrow cannot do today)
    currDate = (today + timedelta(days=y))
    currWeekDay = currDate.strftime("%A")
    currMonth = currDate.strftime("%B")
    currDay = currDate.strftime("%d").replace(' 0', '')
    currYear = currDate.strftime("%Y")
    reqMonth = (months[currMonth]) #remove
    fullDate = ("%s, %s %s, %s" % (currWeekDay, currMonth, currDay, currYear))
    print("Searching for %s reservations on %s for a party of %s" % (reqTime, fullDate, partySize))
    
    driver.find_element_by_class_name("calendarMonth-finderDetailsDining").click() #works
    siteMonth = driver.find_element_by_class_name("ui-datepicker-month").get_attribute("innerHTML") #get current month 
    print("Current month %s and site month %s ..." % (currMonth, siteMonth))
    try:
        while siteMonth != currMonth:
            driver.find_element_by_class_name("ui-icon-circle-triangle-e").click() # Goes to next month
            siteMonth = driver.find_element_by_class_name("ui-datepicker-month").get_attribute("innerHTML") #get current month
            time.sleep(2)
        print("Correct month selected")
        print("Current month %s and site month %s " % (currMonth, siteMonth))
    except:
        pass
    time.sleep(5)

    driver.find_element_by_xpath('//*[@aria-label="%s"]' % fullDate).click() # click date
    time.sleep(2)
    print("Date selected")
    driver.find_element_by_id("dineAvailSearchButton").click() # Click search times button
    print("Search button clicked")
    time.sleep(5)
    print(driver.findElements(driver.find_element_by_css_selector("span.gradient > span.buttonText").innerHTML)
    y = y + 1 #end loop
    
driver.quit()



