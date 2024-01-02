from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
import openpyxl

# Set up Chrome driver
#service = Service('/Volumes/Disk B/Projects/Personal/Py/chrome-mac-arm64/Google Chrome for Testing')  # Replace with the path to your chromedriver executable

driver = webdriver.Chrome()

# URL of the website you want to scrape

weburl = input("Please Enter website url: ")
sheetName = input("Please Enter sheet Name: ")
print("Working on it. Please Wait ....")
url = weburl#"https://www.google.com/localservices/prolist?g2lbs=AP8S6EPxjyBIpgtLpCbgNzs9FwH1LUrnJ5S_xIweRe7IUU6L5dZvZoR1Mt5N7yJ3Nfcl87JYNcu2y43edTXHW19Ka8mGGKR0SThSp2OPrYXQsmCTtlfcfu4j_zYp17BdiWknAZTbYbOi&hl=en-IN&gl=in&cs=1&ssta=1&q=top%2010%20salons%20in%20chandigarh&oq=top%2010%20salons%20in%20chandigarh&slp=MgA6HENoTUl5NF81eDViWGdBTVZJNU5tQWgwdHhBUWxSAggCYAGSAbECCg0vZy8xMWY1ZDZuZ2Y0CgwvZy8xcHR6amY5MWYKDS9nLzExZGR6aGxyNzAKDS9nLzExdDVkMndtNmsKDS9nLzExcjh4c21mZGoKCy9nLzF0ZmJscHM0Cg0vZy8xMWM0YnAzanByCg0vZy8xMWZwNTRidnRqCg0vZy8xMWdkNHljanNqCg0vZy8xMXRkOWhmXzVjCg0vZy8xMWxscjk0M25mCgsvZy8xdHNjbWN2egoML2cvMXB0d2c2bHRqCg0vZy8xMWR5bWMwcnNfCg0vZy8xMWpkcDhqYmtiCg0vZy8xMWxnMnJmNDI2Cg0vZy8xMXEyeGdqeXEyCg0vZy8xMWxsX3h2c2ZuCg0vZy8xMWI2cnc0MXZ4CgwvZy8xaG00MDEwdmQSBBICCAESBAoCCAGaAQYKAhcZEAE%3D&src=2&serdesk=1&sa=X&ved=2ahUKEwjhlfLHlteAAxV_bmwGHTL0BF0QjGp6BAgZEAE&scp=ChFnY2lkOmJlYXV0eV9zYWxvbhJMEhIJa8lu5gvtDzkR_hlzUvln_6UaEglPOJA9BO0PORFi_-ruAM5xTSIKQ2hhbmRpZ2FyaCoUDbHfRxIV7Ba2LR2MulsSJcdHzC0wABoNdG9wIDEwIHNhbG9ucyIbdG9wIDEwIHNhbG9ucyBpbiBjaGFuZGlnYXJoKg5CZWF1dHkgUGFybG91cg%3D%3D"

# Open the website in the browser
driver.get(url)

# Wait for some time to allow JavaScript content to load
time.sleep(5)  # Adjust the sleep duration as needed

workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Sheet"

last_count = 0
curreny_list_count = 0

def getData():
    hasMore = True
    
    article_titles = driver.find_elements(By.CLASS_NAME, "ykYNg")
    count = 0
   
    # Iterate through the found elements and extract the text (article titles)
    for title in article_titles:
        a = title.find_elements(By.CLASS_NAME, "E94Gcd")
        
        for b in a:
            name = b.find_elements(By.CLASS_NAME, "rgnuSb")
            phone = b.find_elements(By.CLASS_NAME, "hGz87c")
            elements = []
            count = len(a)
            for d in name:
                
                elements.append(d.text)
                elements.append(phone[-1].text)
                
            try:
                # Attempt to find the element by its ID
                web = title.find_element(By.CLASS_NAME, "DyM7H").find_elements(By.CLASS_NAME, "zuotBc")[0]
                site = web.find_element(By.TAG_NAME, "a").get_attribute("href")
                elements.append(site)
                
            except NoSuchElementException:
                elements.append("Website not found")
                
            sheet.append(elements)
            if len(a) < 20 :
                hasMore = False
                
    
    change_count(count)
            
                
               
    if hasMore :
        clickOnNextButton()
        time.sleep(5)
        getData()
    else :
        workbook.save(sheetName+".xlsx")
        print("Scraping is Done. Your sheet is ready")

def clickOnNextButton():
    button_element = driver.find_elements(By.CLASS_NAME, "sspfN")
    button_element[-1].click()
    

def change_count(current_size):
    global curreny_list_count
    last_count = curreny_list_count
    curreny_list_count = last_count + current_size
    print("Extracting data from " + str(last_count) + " to " + str(curreny_list_count)) 
    
    

    
# Close the browser\

getData()

driver.quit()