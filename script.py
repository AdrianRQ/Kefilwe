from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import os
import sqlite3
import time

def is_file_downloaded(filename, timeout=60):
    # custom function to check if file has been downloaded
    end_time = time.time() + timeout
    while not os.path.exists(filename):
        time.sleep(1)
        if time.time() > end_time:
            return False

    if os.path.exists(filename):
        return True

path = os.getcwd()
chrome_options = Options()
prefs = {'download.default_directory' : r'{}'.format(path), "download.directory_upgrade": True}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://jobs.homesteadstudio.co/data-engineer/assessment/download/")
button = driver.find_element(By.CLASS_NAME, "wp-block-button")
button.click()

confirm_download = is_file_downloaded('./skill_test_data.xlsx', 60)

data_df = pd.read_excel('./skill_test_data.xlsx', sheet_name='data')
pivot_df = pd.pivot_table(data_df, values=['Spend', 'Attributed Rev (1d)', 'Imprs', 'Visits', 'New Visits', 'Transactions (1d)', 'Email Signups (1d)'], 
    index=['Platform (Northbeam)'], aggfunc=np.sum).sort_values(by='Attributed Rev (1d)', ascending=False)

conn = sqlite3.connect('test_database') 
pivot_df.to_sql("pivot_table", conn, if_exists="replace")
conn.commit()
conn.close()

driver.quit()