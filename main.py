from selenium import webdriver
import time
import json
import datetime
import creds
import mail

with open("dataleft.json") as f: # getjson
    jsonrecieve = json.load(f)
    print("jsonrecieve: " + str(jsonrecieve))

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")  # Optional argument, if not specified will search path.
driver.get('https://www.giffgaff.com/auth/login?redirect=%2Fdashboard')
time.sleep(5) # Let the user actually see something!

def login():
    time.sleep(2)
    driver.find_element_by_css_selector("#cookie-banner > div > div.cbot-layout--2column.cbot-layout--right.cbot-layout--ctas > a.cbot-btn.cbot-btn--primary > span").click()
    input = driver.find_element_by_css_selector('#memberName')
    input.send_keys(creds.giffgaffuser)
    time.sleep(1)
    input = driver.find_element_by_css_selector('#password')
    input.send_keys(creds.giffgaffpassword)
    input = driver.find_element_by_css_selector('#__next > div > main > section.LoginForm__CustomSection-pu8cj5-0.cWwtWo.gg-o-page-section > form > button')
    input.click()
    time.sleep(6)

login()

def getdataleft():
    driver.execute_script("document.body.style.zoom='60%'")
    dataleft = driver.find_element_by_css_selector("#balance-content > div.row-fluid.dasboard-goodybag-section > div:nth-child(1) > div > div:nth-child(1) > div.goodybag-container.clearfix > div.pull-left.goodybag-container-right-column > div:nth-child(1) > div > div.progressbar-label").text
    return dataleft

def parse():
    dataleft = getdataleft()
    dataleft = dataleft[0:3]
    print("dataleft: " + dataleft)
    return dataleft

dataleft = parse()

def sendemail():
    print("\n\nsendemail")
    Recipient = creds.email
    Subject = "Mobile Data Checkup"
    Contents = "Data left this month: " + dataleft + "GB"
    mail.main(Subject, Contents, Recipient)
    print("\n\n")

def updatedict():
    jsonrecieve["dataleft"] = dataleft

    lastdate = int(jsonrecieve["lastdate"])

    if lastdate == int("7"):
        jsonrecieve["lastdate"] = str("0")
        sendemail()

    else:
        jsonrecieve["lastdate"] = str(int(lastdate) + int("1"))
        print("updated json: " + str(jsonrecieve))

updatedict()

with open('dataleft.json', 'w') as fw: # write json
    json.dump(jsonrecieve, fw)

driver.quit()