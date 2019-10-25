import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta, date

driver = webdriver.Chrome(executable_path=r'C:\Users\Brandon\AppData\Local\Programs\Python\Python38-32\chromedriver.exe')
ohanaLink = ("https://disneyworld.disney.go.com/dining/polynesian-resort/ohana/")
months = {'January': 0, 'February': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5, 'July': 6, 'August': 7, 'September': 8, 'October': 9, 'November': 10, 'December': 11}

"""
Reservations can be made up to 180 days ahead
Need to loop through all months one at a time (7)
Need to loop through all dates within the month
Need to loop through breakfast and dinner for each date
Need to save all openins for each date
"""

driver.get(ohanaLink)
time.sleep(1)
today = datetime.today()
y = 2
while y < 180: # start loop (has to start at tomorrow cannot do today)
    currDate = (today + timedelta(days=y))
    currWeekDay = currDate.strftime("%A")
    currMonth = currDate.strftime("%B")
    currDay = currDate.strftime("%d")
    currYear = currDate.strftime("%Y")
    reqMonth = (months[currMonth])
    fullDate = ("%s, %s %s, %s" % (currWeekDay, currMonth, currDay, currYear))
    reqTime = ("dinner")
    partySize = (4)
    print("Searching for %s reservations on %s for a party of %s" % (reqTime, fullDate, partySize))
    
    driver.find_element_by_class_name("ui-datepicker-trigger").click() #works
    siteMonth = driver.find_element_by_class_name("ui-datepicker-month").get_attribute("innerHTML") #get current month 
    siteMonth = (months[currMonth] + 1)

    time.sleep(2)
    while siteMonth < reqMonth: # not working - will not switch months
        driver.find_element_by_class_name("ui-icon-circle-triangle-e").click() # Goes to next month
        siteMonth = driver.find_element_by_class_name("ui-datepicker-month").get_attribute("innerHTML") #get current month
        siteMonth = (months[siteMonth] + 1)

    time.sleep(2)
    driver.find_element_by_xpath('//*[@aria-label="%s"]' % fullDate).click() # click date
    time.sleep(2)
    print("Date selected")

    driver.find_element_by_class_name("select-toggle").click() # open time menu
    time.sleep(2)
    driver.find_element_by_css_selector ('ol > li[aria-label="%s"]' % reqTime).click() #click time (dinner for testing)
    time.sleep(2)
    print("Time selected")


    driver.find_element_by_xpath('//*[@aria-owns="partySize-dropdown-list"]').click() #open party size menu
    time.sleep(2)
    driver.find_element_by_css_selector ('ol > li[data-display="%s"]' % partySize).click() #works
    print("Party size selected")

    driver.find_element_by_id("dineAvailSearchButton").click() # Click search times button
    print("Search button clicked")

    
    try:
        allTimes = []
        for allTimes in driver.find_elements_by_class_name('availableTime'):
            availTime = allTimes.find_element_by_xpath('.//div[@class="buttonText"]/a').text
            allTimes.append({'Time available': availTime, 'Date': fullDate})
            print(allTimes)
    except:
        print("No available tables for this date.")

    #this sections pulls available dates to add to 
    time.sleep(5)


    y = y+1 #end loop



