import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from dateutil import parser
import calendar
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

reqDate = (6)
reqMonth = (11)
reqYear = (2019)
reqTime = ("7:00pm")
fullDate = (", November 6, 2019")
weekDay = parser.parse(fullDate).strftime("%A")
fullDate = (weekDay + fullDate) # converts to disney friendly format to be clicked

today = date.today()
todaysDay = today.strftime("%d")
todaysMonth = today.strftime("%m")

print(todaysDay + " " + todaysMonth)

driver.get(ohanaLink) 
time.sleep(1) # Let the user actually see something!

#testing
driver.find_element_by_class_name("ui-datepicker-trigger").click() #works
currMonth = driver.find_element_by_class_name("ui-datepicker-month").get_attribute("innerHTML") #get current month 
currYear = driver.find_element_by_class_name("ui-datepicker-year").get_attribute("innerHTML") #get current year 
currMonth = (months[currMonth] + 1)
print (currMonth, currYear)


while currMonth < reqMonth: # working - goes to correct month
    driver.find_element_by_class_name("ui-icon-circle-triangle-e").click() # Goes to next month
    currMonth = driver.find_element_by_class_name("ui-datepicker-month").get_attribute("innerHTML") #get current month
    currMonth = (months[currMonth] + 1)
    print("Current month = ",currMonth," Required month = ",reqMonth)
print("At current Month")

driver.find_element_by_xpath('//*[@title="%s"]' % fullDate).click() #working
print("Clicked")

# need to add function for time
#need to click arrow key first

driver.find_element_by_class_name("select-toggle").click()
time.sleep(5)
driver.find_element_by_css_selector ('ol > li[aria-label="%s"]' % reqTime).click() #works

# add function for party size
time.sleep(25)
# retrieve results

# loop




#testing

#driver.quit()























driver.quit()
