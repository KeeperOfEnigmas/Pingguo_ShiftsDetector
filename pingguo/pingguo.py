# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 12:21:57 2024

@author: 林威邑
"""

import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time

# constants
subject = "苹果，你有新的工作，请及时处理！"
body = "上班!!!"
email = "kingarthur0323@gmail.com"
email_password = "rbeyrnxthkkmmgxz"

username = "hongpeng.li"
password = "hgfdsa765432"

url = "https://lothianeol.allocate-cloud.com/EmployeeOnlineMobile/LOTHIANLIVE/#/login"
url_shifts = "https://lothianeol.allocate-cloud.com/EmployeeOnlineMobile/LOTHIANLIVE/#/bankshifts/shifts"
path_to_driver_edge = "C:\\Users\\Arthur\\Desktop\\pingguo\\msedgedriver.exe"

refresh_timer = 3 # in minutes
shift_found = False
    
# send notification email
def send_email(subject, body, email, password):
    msg = MIMEText(body+" "+day+"!")
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(email, password)
        smtp_server.sendmail(email, email, msg.as_string())
    print("Email notification sent!")

# detect if a shift is available
def detect_job(driver, refresh_timer, day):
    curr_url = driver.current_url
    if curr_url != url:
        if curr_url != url_shifts:
            driver.get(url)
    
    while True:
        driver.refresh()
        time.sleep(10)
        shift_found = False
               
        elements = driver.find_elements(By.CSS_SELECTOR, "span.sub")
            
        for e in elements:
            if e.text == day:
                print("Shift found!")
                shift_found = True
                send_email(subject, body, email, password)
                terminate(driver)
                return
        if not(shift_found):
            print("No shift found!")  

        time.sleep(refresh_timer*60-10)
        #time.sleep(10)
    
# terminate the program
def terminate(driver):
    driver.quit()
    print("Program terminate!")
    
# initialize edge driver 
def initialize_driver():
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    driver_path = path_to_driver_edge
    driver = webdriver.Edge(options=options, service=Service(driver_path))    
    return driver



try:
    day = input("Enter which day you want(capitalized): ")
    print("Program running!")
    driver = initialize_driver()
    detect_job(driver, refresh_timer, day)
except KeyboardInterrupt:
    terminate(driver)
    
    
