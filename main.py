from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
import pandas as pd

# INITIALISE DRIVER
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

load_dotenv(dotenv_path=".env.local")
page_url = os.getenv("URL_PAGE")

driver = webdriver.Chrome(options=chrome_options)
driver.get(page_url)

# SLEEP FOR 2 SEC MANUALLY FOR DYNAMIC RENDERING PAGES
time.sleep(2)

# REJECT COOKIES
reject_all_btn = driver.find_element(By.ID, "onetrust-reject-all-handler")
reject_all_btn.click()

# SCROLL TO THE BOTTOM OF THE PAGE TO LOAD CONTENT
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# SLEEP FOR 1 SEC MANUALLY FOR DYNAMIC RENDERING PAGES
time.sleep(1)

# WAIT UNTIL PRESENCE OF ELEMENT LOCATED
wait = WebDriverWait(driver, 3)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "paging-eof")))

# STORE INTO A DIFFERENT LIST ACTUALLY SPACE: O(n)
trackList_username = driver.find_elements(By.CLASS_NAME, value="trackItem__username")
trackList_trackTitle = driver.find_elements(By.CLASS_NAME, value="trackItem__trackTitle")

users = [user.text for user in trackList_username]
tracks = [track.text for track in trackList_trackTitle]

# CLOSE AFTER COMPLETION OF TASKS
driver.close()

# CHECK WHETHER BOTH HAVE SAME LENGTH
if len(users) == len(tracks):
    # SAVE TO CSV AS 2 COLUMN
    data_frame = pd.DataFrame({"Users": users, "Tracks": tracks})
    data_frame.to_csv("./music-books/soundcloud.csv", index=False)
    print("Created Successfully.")
else:
    # DON'T SAVE INSTEAD PRINT 'NOT EQUAL'
    print("Not equal")