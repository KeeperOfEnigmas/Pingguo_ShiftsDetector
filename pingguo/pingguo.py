"""
Created on 2024.10.10 Thursday
@author: 林威邑
"""

import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import sys

# constants
SUBJECT = "苹果，你有新的工作，请及时处理！"
BODY = "上班!!!"
EMAIL = "kingarthur0323@gmail.com"
EMAIL_PASSWORD = "rbeyrnxthkkmmgxz"

USERNAME = "hongpeng.li"
EMAIL_PASSWORD = "hgfdsa765432"

URL = "https://lothianeol.allocate-cloud.com/EmployeeOnlineMobile/LOTHIANLIVE/#/login"
URL_SHIFTS = "https://lothianeol.allocate-cloud.com/EmployeeOnlineMobile/LOTHIANLIVE/#/bankshifts/shifts"
PATH_TO_DRIVER_EDGE = "C:\\Users\\Arthur\\Desktop\\pingguo\\msedgedriver.exe"

REFRESH_TIMER = 3  # in minutes


def send_email(subject, body, day, email, password):
    """
    Send notification email.

    `subject` -- title of the email \n
    `body` -- content of the email \n
    `day` -- the day of the shift \n
    `email` -- emaili address \n
    `password` -- passkey
    """

    msg = MIMEText(body + " " + day + "!")
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(email, password)
        smtp_server.sendmail(email, email, msg.as_string())
    print("Email notification sent!")


def detect_shift(driver, refresh_timer, day):
    """
    Check if a shift exists on a given day.

    `driver` -- driver for connecting to web browser \n
    `refresh_timer` -- checking interval in minute \n
    `day` -- the day of the shift
    """

    curr_url = driver.current_url
    if curr_url != URL:
        if curr_url != URL_SHIFTS:
            driver.get(URL)

    while True:
        driver.refresh()
        time.sleep(10)
        shift_found = False

        elements_time = driver.find_elements(By.CLASS_NAME, "list")

        for e_time in elements_time:
            try:
                text = e_time.text
                index = text.find(day)
                subText = text[index:]
                if "08:00" in subText:
                    print("Early shift found!")
                    # print("Shift starts from: " + text[index:index+len(day)])
                    print(f"Shift starts from: {text[index:index+len(day)]}")

                    shift_found = True
                    send_email(SUBJECT, BODY, day, EMAIL, EMAIL_PASSWORD)
                    terminate(driver)
            except Exception:
                pass

        if not (shift_found):
            print("No shift found!")

        time.sleep(refresh_timer * 60 - 10)
        # time.sleep(5)


def terminate(driver):
    """
    Stop the driver.

    `driver` -- driver for connecting to web browser
    """

    driver.quit()
    print("Drivet terminated!")
    sys.exit()


def initialize_driver():
    """
    Initialize the driver.
    """

    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    driver = webdriver.Edge(options=options, service=Service(PATH_TO_DRIVER_EDGE))
    return driver


def main():
    """
    Main function.
    """

    try:
        day = input("Enter which day you want(capitalized): ")
        print("Program running!")
        driver = initialize_driver()
        detect_shift(driver, REFRESH_TIMER, day)
        return 0
    except KeyboardInterrupt:
        terminate(driver)


if __name__ == "__main__":
    sys.exit(main())
