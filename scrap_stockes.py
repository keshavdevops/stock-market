import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()
driver.get('https://www.screener.in/screens/71064/all-stocks/')
wait = WebDriverWait(driver, 10)


def login(username, password):
    edit_columns = driver.find_element(By.CSS_SELECTOR, 'a.button:nth-child(4)')
    edit_columns.click()

    go_to_login = driver.find_element(By.CSS_SELECTOR, 'p.text-align-center > a:nth-child(1)')
    go_to_login.click()
    
    wait.until(EC.presence_of_element_located((By.ID, 'id_username')))

    username_field = driver.find_element(By.ID, 'id_username')
    username_field.click()
    username_field.send_keys(username)

    password_field = driver.find_element(By.ID, 'id_password')
    password_field.click()
    password_field.send_keys(password)

    click_login = driver.find_element(By.CSS_SELECTOR, 'button.button-primary')
    click_login.click()



def select_verticals():
    # time.sleep(5)
    while True:
        try:        
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.draggable-row:nth-child(1) > button:nth-child(2) > i:nth-child(1)')))
            manage_menu = driver.find_element(By.ID, 'manage-menu')
            existing_verticals = manage_menu.find_element(By.CSS_SELECTOR, 'li.draggable-row:nth-child(1) > button:nth-child(2) > i:nth-child(1)')
            existing_verticals.click()

        except Exception as e:
            break
    
    price_tab = driver.find_element(By.XPATH, '/html/body/main/div[2]/form/div[2]/div/div[2]/div/button[7]')
    price_tab.click()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.flex:nth-child(8)')))
            
    options = driver.find_element(By.CSS_SELECTOR, 'div.flex:nth-child(8)')

    verticals = [
                'Current price', 'Volume', 'Return over 1day', 'Return over 1week',
                'Return over 1month', 'Return over 3months', 'Return over 6months', 'Return over 1year',
                'Return over 3years', 'Volume 1month average', 'Volume 1week average'
                ]
    
    for vertical in verticals:
        element = options.find_element(By.CSS_SELECTOR, f'label[data-name="{vertical}"]')
        element.click()

    save_vertical = driver.find_element(By.CSS_SELECTOR, 'button.button-primary')
    save_vertical.click()

    page_limit = driver.find_element(By.CSS_SELECTOR, 'div.options:nth-child(2) > a:nth-child(1)')
    page_limit.click()


    page_limit = driver.find_element(By.CSS_SELECTOR, 'div.options:nth-child(2) > a:nth-child(3)')
    page_limit.click()


login('kg829041@gmail.com', 'Keshav1234k')
select_verticals()

stocks_table = []

state = True
while state:
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
    except Exception as e:
        time.sleep(10)
        print(e)
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))

    page_source = driver.page_source

    page_soup = BeautifulSoup(page_source, 'lxml')
    body = page_soup.find('tbody')
    table = body.find_all('tr')
    for rows in table:
        head_row = table[0].find_all('th')
        row_values = rows.find_all('td')
        dis = {}

        if len(row_values) != 0:
            for head,row_value in zip(head_row, row_values):
                head = head.text
                row_ = row_value.text
        
                dis[head.strip()] = row_.strip()  # Remove leading and trailing whitespace
            print(dis)
            stocks_table.append(dis)
    time.sleep(1)
    try:
        next_page = driver.find_element(By.CLASS_NAME, 'icon-right')
        next_page.click()
    except Exception as e:
        print(f'\nnext page error \n\n\n')
        state = False

print(f'\n\nTotal stock scraped {len(stocks_table)}')
file = f'/home/keshav/Downloads/stock_market/stock_data_{datetime.date.today()}.csv'
df = pd.DataFrame(stocks_table)

df.to_csv(file)

time.sleep(3)
driver.quit()


import sys
sys.path.append('/home/keshav/Projects/Post_mail')
import mailer


subject = f"Stock file {datetime.date.today()}"
body = f"complete screener python scraping code executed on {datetime.datetime.now()}"
path  = [file]

mail = mailer.mailing(sender="gkeshav911@gmail.com", receiver="niharikahandicrafts1726@gmail.com",
                       sender_password="etajhpxanumrxfpx")

# With attachment
mail.compose_mail(subject, body, file_paths=path)

