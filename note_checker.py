import time
from selenium import webdriver
from lxml import html

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')

browser = webdriver.Chrome(chrome_options=options)

browser.get("https://my.uni.li/Study/Intranet/tabid/661/language/de-CH/Default.aspx")
source = browser.page_source
identifier = """<span id="dnn_ctr3480_dnnTITLE_titleLabel" class="title">User Log In</span>"""
if identifier in source:
    browser.find_element_by_id("dnn_ctr3480_Login_Login_DNN_txtUsername").send_keys('myUserName')
    browser.find_element_by_id("dnn_ctr3480_Login_Login_DNN_txtPassword").send_keys('myPassword')
    browser.find_element_by_id("dnn_ctr3480_Login_Login_DNN_cmdLogin").click()
    time.sleep(5)
    source = browser.page_source
else:
    source = browser.page_source

if 'Module / Veranstaltungen SS 19' in source:
    print("You're logged in!")
else:
    print("Logging in failed. Perhaps, it was attempted with invalid credentials")
    exit()

browser.find_element_by_id("dnn_ctr1297_Splitter_ctl00_ImageButtonLeft1").click()
time.sleep(5)
source = browser.page_source
if 'WS 18/19' in source:
    print("You reached page WS 18/19")
else:
    print("Target page could not be reached")
    exit()

tree = html.fromstring(source)
state = tree.get_element_by_id("dnn_ctr1297_Splitter_ctl00_TablePruefungen").text_content()

with open("html.txt", "r", encoding="UTF8") as file:
    old_state = file.read()

if (old_state == state):
    print("There is no change!")
    exit()
else:
    print("Sending an email...")
    import smtplib, ssl

    sender_email = "your email"
    receiver_email = [ 'youremail@email.com' ]
    message = """\
    Subject: Grade Checker

    A new grade is online. You might want to check it.

    https://my.uni.li/
    """

    port = 465  # For SSL
    password = "myemailPassword"

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("youremail", password)
        server.sendmail(sender_email, receiver_email, message)
    print("Email sent!")

with open("html.txt", "w", encoding='UTF8') as file:
    file.write(state)