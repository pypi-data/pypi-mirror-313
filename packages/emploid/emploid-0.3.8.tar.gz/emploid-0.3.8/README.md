# Emploid

**Emploid** is a Python package designed to simplify the automation of web, Android, and Windows processes. With a focus on ease of use and flexibility, Emploid is the perfect tool for anyone looking to streamline repetitive tasks.

---

## Features

- **Web Automation**: Automate browser tasks such as form submissions, web scraping, and more.
- **Android Automation**: Control Android devices for app testing, UI interaction, and task automation.
- **Windows Automation**: Manage desktop applications, simulate keyboard/mouse input, and automate system processes.

---

## Installation

Install Emploid via pip:

```bash
pip install emploid
```

## Module Import

You import emploid into your .py files like this:

```bash
from emploid.emploid import Emploid
from emploid.constants import *
```

## Web Automation
**Prerequesites:**
* You must install [Chromedriver](https://googlechromelabs.github.io/chrome-for-testing/) under a 'drivers' folder in your working directory. 
    * ![alt text](image.png)

* Make sure the version of the driver matches the version of chrome browser installed on your machine.
___
**Example code:**
```bash
emp = Emploid(_driver_type=SETTINGS_USE_SELENIUM) #init emploid for web
emp.get("https://google.com") #go to google.com
emp.click("/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[2]/div") #click on popup accept button
emp.submit("hello world", "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea") #search for the string "hello world"
emp.pause() #pause so that the browser window does not terminate
```
---

## Android Automation
**Prerequesites:**
* Install an android emulator such as [MeMu](https://www.memuplay.com/) and run it.
* Install [Appium Server](https://appium.io/docs/en/2.0/quickstart/install/). 
* Make sure to install the [UiAutomator driver](https://appium.io/docs/en/2.0/quickstart/uiauto2-driver/) for appium:
```bash
appium driver install uiautomator2
```
* Then run appium from the command-line:
```bash
appium
```
Now, you can run your program and it'll connect to your android emulator through appium.

**Example code:**
```bash
emp = Emploid(_driver_type=SETTINGS_USE_APPIUM) #init emploid for android
emp.appium_connect()

emp.activate_app("com. android. chrome")
emp.click("""...""", _tries=10)
emp.input_into("hello", """//android.widget.EditText""", _tries=10)
emp.pause() #pause so that the browser window does not terminate
```
---

## Windows Automation
**Prerequesites:**
* You must include all elements you want to interact with as .png files under  a "elements" folder in your working directory.
___
**Example code:**
```bash
emp = Emploid(_driver_type=SETTINGS_USE_PYAUTOGUI) #init emploid for windows
emp.get("https://google.com") #go to google.com
emp.click("/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[2]/div") #click on popup accept button
emp.submit("hello world", "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea") #search for the string "hello world"
emp.pause() #pause so that the browser window does not terminate
```
---


