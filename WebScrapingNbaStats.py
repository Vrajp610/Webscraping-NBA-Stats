from selenium import  webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

nba_seasons = ['2019-20', '2018-19', '2017-18']
timeout = 25

driver = webdriver.Chrome(executable_path="/System/Volumes/Data/Users/vrajpatel/Desktop/PythonProject/chromedriver")

for season in nba_seasons:
    url = f"https://www.nba.com/stats/players/advanced/?Season={season}&SeasonType=Regular%20Season&sort=GP&dir=-1"
    driver.get(url)
    element_present = EC.presence_of_element_located((By.XPATH, r"/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select"))
    WebDriverWait(driver, timeout).until(element_present)

    select = Select(driver.find_element_by_xpath(r"/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select"))
    select.select_by_index(0)

    src = driver.page_source
    parser = BeautifulSoup(src, "lxml")
    table = parser.find("div", attrs={"class": "nba-stat-table__overflow"})
    headers = table.find_all('th')
    headerList = [h.text.strip() for h in headers[1:]]
    headerList1 = [a for a in headerList if not 'RANK' in a]

    rows = table.find_all('tr')[1:]
    player_stats = [[td.getText().strip() for td in rows[i].findAll('td')[1:]] for i in range(len(rows))]

    headerList1 = headerList1[:-5]
    stats = pd.DataFrame(player_stats, columns=headerList1)

    print(stats)
