from tkinter import *
from tkinter import messagebox

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
expand on the notifications of an openin
finally build into executable with py.exe
'''

def exitNow():
    quit()
# -------------------------------------------------------------------------------- start browser --------------------------------------------------------------------------------
def startScript():
    root.withdraw() # hides menu so it runs in the background
    ohanaLink = ("https://disneyworld.disney.go.com/dining/polynesian-resort/ohana/")
    try: # finds ChromeDriver based on user
        userName = os.getlogin() 
        if userName == "Brandon":
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            driver = webdriver.Chrome(executable_path=r'C:\Users\Brandon\AppData\Local\Programs\Python\Python38-32\chromedriver.exe', chrome_options=options) 
    except:
        print("An error occured identifying ChromeDriver.")
    try: # go to the URL
        driver.get(ohanaLink)
        WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except:
        print('An error occured when picking party size and time.')
    try: #pick the time
        reqTime = str(chosenTimeInput.get()).lower()
        driver.find_element_by_class_name("select-toggle").click()
        time.sleep(0.25)
        driver.find_element_by_css_selector ('ol > li[aria-label="%s"]' % reqTime).click()
        time.sleep(0.25)
    except:
        print("An error occured when picking the time.")
    try: # pick the party size
        partySize = str(partySizeInput.get())
        driver.find_element_by_xpath('//*[@aria-owns="partySize-dropdown-list"]').click()
        time.sleep(0.25)
        driver.find_element_by_css_selector ('ol > li[data-display="%s"]' % partySize).click()
        time.sleep(0.25)
    except:
        print("An error occured when picking the party size.")
    try:
        inputMonth = int(chosenDateInput.get().split("/")[0])
        inputDay = int(chosenDateInput.get().split("/")[1])
        inputYear = int(chosenDateInput.get().split("/")[2])
        requiredDate = datetime.date(inputYear, inputMonth, inputDay) # change this based on user GUI drop down menu options
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
            time.sleep(1.5)
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
                popUpMsg = ("There is an opening at %s on %s." % (availbility, fullDate))
                root.lift()
                messagebox.showinfo("Alert!", popUpMsg)
                MsgBox = messagebox.askquestion('Exit Application','Are you sure you want to exit the application',icon = 'warning')
                if MsgBox == 'yes':
                    driver.quit()
                    root.destroy()
                else:
                    tk.messagebox.showinfo('Return','You will now return to the application screen')
        except:
            time.sleep(0.05)
        time.sleep(int(loopTimeInput.get())-2.5)
    driver.quit()
# -------------------------------------------------------------------------------- end browser --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- begin GUI --------------------------------------------------------------------------------
root = Tk()

labelName = Label(root, text="Disney Reservation Checker")
enterButton = Button(root, text=" Start " ,bg="yellow",fg="black", command=startScript)
exitButton = Button(root, text= " Exit  " ,bg ="red",fg="black", command=exitNow)
partySizeLabel = Label(root, text="Enter a party size between 2 and 49")
partySizeInput = Entry(root)
partySizeInput.insert(10, "4")
chosenTimeLabel = Label(root, text="Breakfast or Dinner?")
chosenTimeInput = Entry(root)
chosenTimeInput.insert(10, "Dinner")
chosenDateLabel = Label(root, text="Please enter a date ex: 04/25/2020")
chosenDateInput = Entry(root)
chosenDateInput.insert(10, "04/13/2020")
loopTime = Label(root, text="How often should we check? (seconds)")
loopTimeInput = Entry(root)
loopTimeInput.insert(10, "30")

partySizeLabel.grid(row=2,column=0,sticky=E)
partySizeInput.grid(row=2,column=1,sticky=E)
chosenTimeLabel.grid(row=3,column=0,sticky=E)
chosenTimeInput.grid(row=3,column=1,sticky=E)
chosenDateLabel.grid(row=4,column=0,sticky=E)
chosenDateInput.grid(row=4,column=1,sticky=E)
loopTime.grid(row=5,column=0,sticky=E)
loopTimeInput.grid(row=5,column=1,sticky=E)

labelName.grid(row=0,columnspan=2)

enterButton.grid(row=6,column=0,sticky=E)
exitButton.grid(row=6,column=1,sticky=W)

root.mainloop()
# -------------------------------------------------------------------------------- end GUI --------------------------------------------------------------------------------