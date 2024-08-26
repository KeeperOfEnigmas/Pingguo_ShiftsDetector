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
path_to_driver_edge = "C:\\Users\\david\\Desktop\\pingguo\\msedgedriver.exe"

refresh_timer = 3 # in minutes
    
# send notification email
def send_email(subject, body, email, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(email, password)
        smtp_server.sendmail(email, email, msg.as_string())
    print("Email notification sent!")

# detect if job is available
def detect_job(driver, refresh_timer):
    curr_url = driver.current_url
    if curr_url != url:
        if curr_url != url_shifts:
            driver.get(url)
    
    while True:
        driver.refresh()
        time.sleep(10)
        
        try:
            element = driver.find_element(By.TAG_NAME, "h")
            #element = driver.find_element(By.ID, "offline-state-overlay")
        except:
            pass   
        try:
            if element != None:
                print(element.text)
                #send_email(subject, body, email, password)
        except:
                print("No shift found!")
        
        time.sleep(refresh_timer*60-10)
    
# terminate the program
def terminate(driver):
    driver.quit()
    
# initialize edge driver 
def initialize_driver():
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    driver_path = path_to_driver_edge

    driver = webdriver.Edge(options=options, service=Service(driver_path))
    
    return driver

try:
    driver = initialize_driver()
    detect_job(driver, refresh_timer)
except KeyboardInterrupt:
    terminate(driver)
    print("Program terminate!")
    
