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

from twilio.rest import Client

def exitNow():
    os._exit(1) # updated this to remove quit() with caused exception error
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
        driver.quit()
        scriptError()
        return
    try: # go to the URL
        driver.get(ohanaLink)
        WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except:
        driver.quit()
        scriptError()
        return
    try: #pick the time
        reqTime = str(chosenTimeInput.get()).lower()
        driver.find_element_by_class_name("select-toggle").click()
        time.sleep(0.25)
        driver.find_element_by_css_selector ('ol > li[aria-label="%s"]' % reqTime).click()
        time.sleep(0.25)
    except:
        driver.quit()
        scriptError()
        return
    try: # pick the party size
        partySize = str(partySizeInput.get())
        driver.find_element_by_xpath('//*[@aria-owns="partySize-dropdown-list"]').click()
        time.sleep(0.25)
        driver.find_element_by_css_selector ('ol > li[data-display="%s"]' % partySize).click()
        time.sleep(0.25)
    except:
        driver.quit()
        scriptError()
        return
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
            driver.quit()
            scriptError()
            return
        try: # logic for if the month has changed
            while siteMonth != currMonth:
                driver.find_element_by_class_name("ui-icon-circle-triangle-e").click() # Goes to next month
                time.sleep(0.25)
                siteMonth = driver.find_element_by_class_name("ui-datepicker-month").get_attribute("innerHTML")
                time.sleep(0.25)
        except:
            driver.quit()
            scriptError()
            return
        try: # choses date from open date menu - the page does not refresh so we only need to open this once
            time.sleep(1.5)
            driver.find_element_by_xpath('//*[@aria-label="%s"]' % fullDate).click() # click date
            time.sleep(0.25)
        except:
            driver.quit()
            scriptError()
            return
    except:
        driver.quit()
        scriptError()
        return
    while True: # main loop 
        try: # clicks search button
            time.sleep(2.5)
            driver.find_element_by_id("dineAvailSearchButton").click() # Click search times button
            time.sleep(7.5) # change this to wait for loading element to dissapear
        except:
            driver.quit()
            scriptError()
            return 
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
                messagebox.showinfo("There is an opening!", popUpMsg)
                MsgBox = messagebox.askquestion('Exit Application','Are you sure you want to exit the application',icon = 'warning')
                if MsgBox == 'yes':
                    driver.quit()
                    root.destroy()
                else:
                    tk.messagebox.showinfo('Return','You will now return to the application screen')

                account_sid = 'AC8e14b1e892a9456d0a2656ac0ca8634e'
                auth_token = '003436af2c87166e199a44c46a299403'
                client = Client(account_sid, auth_token)

                message = client.messages \
                .create(
                     body=popUpMsg,
                     from_='+12565008428',
                     to='+16039735334'
                 )
                print(message.sid)
        except:
            time.sleep(0.05)
        time.sleep(int(loopTimeInput.get())-2.5)
    driver.quit()
# -------------------------------------------------------------------------------- end browser --------------------------------------------------------------------------------
# -------------------------------------------------------------------------------- Begin validating inputs --------------------------------------------------------------------------------
def validateInputs():
    pSizeBool = 0
    chosenTimeBool = 0
    choseDateBool = 0
    loopTimeBool = 0
    # verify party size
    if int(partySizeInput.get()) >= 2: 
        if int(partySizeInput.get()) <= 49:
            pSizeBool = 1
    # verify time
    if (chosenTimeInput.get()).lower() in ["breakfast","dinner"]: 
        chosenTimeBool = 1
    # verify data
    try:
        tempChosenDate = datetime.datetime.strptime(chosenDateInput.get(), '%m/%d/%Y')
    except:
        messagebox.showinfo("Alert!", "The entered date format does not match what is expected. Please reenter the data using the format 'MM/DD/YYYY'")
        return 
    tempTodayVar = datetime.datetime.today()
    if (tempChosenDate > (tempTodayVar + timedelta(days=2))):
        if (tempChosenDate <= (tempTodayVar + timedelta(days=180))):
            choseDateBool = 1
    # verify loop time
    if (int(loopTimeInput.get()) > 14):
        loopTimeBool = 1
    if (pSizeBool == 1):
        if (chosenTimeBool == 1):
            if (choseDateBool == 1):
                if (loopTimeBool == 1):
                    startScript()
                else:
                    messagebox.showinfo("Alert!", "There is an issue with the chosen loop time, the value must be a number greater than 15. Please input a different number and try again.")
                    return
            else:
                messagebox.showinfo("Alert!", "There is an issue with the chosen date, Disney only allows reservations up to 180 days from today's date and the script can only check dates more then 2 days ahead.")
                return
        else:
            messagebox.showinfo("Alert!", "There is an issue with the chosen time, currently the only values allowed are Dinner or Breakfast - support for other times will be added later")
            return
    else:
        messagebox.showinfo("Alert!", "There is an issue with the party size, Disney only allows parties between 2 and 49 people. Please try again.")
        return
    # if all bools true then call startScript 
# -------------------------------------------------------------------------------- end validating inputs --------------------------------------------------------------------------------
def scriptError():
    print("An error occured when picking the time.")
    messagebox.showinfo("Alert!", "There was an error with the script. Hit 'Start' to try again.")
    root.deiconify()
    return
# -------------------------------------------------------------------------------- begin GUI --------------------------------------------------------------------------------
root = Tk()
root.title('Disney Reservation Checker')
labelName = Label(root, text="Ohana Reservation Checker")
enterButton = Button(root, text=" Start " ,bg="yellow",fg="black", command=validateInputs) # change to validate first and startScript second
exitButton = Button(root, text= " Exit  " ,bg ="red",fg="black", command=exitNow)
partySizeLabel = Label(root, text="Enter a party size between 2 and 49")
partySizeInput = Entry(root)
partySizeInput.insert(10, "4")
chosenTimeLabel = Label(root, text="Breakfast or Dinner?")
chosenTimeInput = Entry(root)
chosenTimeInput.insert(10, "Dinner")
chosenDateLabel = Label(root, text="Please enter a date ex: MM/DD/YYYY")
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

# centers screen
root.withdraw()
root.update_idletasks()  
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))
root.deiconify()
# centers screen

root.mainloop()
# -------------------------------------------------------------------------------- end GUI --------------------------------------------------------------------------------