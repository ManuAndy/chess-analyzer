import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

def extract_participants(tournament_url):
    if '?' in tournament_url:
        tournament_url = tournament_url + "&zeilen=99999"
        if "lan=" in tournament_url:
            tournament_url = tournament_url + "lan=0"
    else:
        tournament_url = tournament_url + "?zeilen=99999"

    response = requests.get(tournament_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Assuming participants' data is in a specific table structure
    participants = []
    table = soup.find('table', {"class":"CRs1"})
    header = table.find('tr')
    cells = header.find_all('th')
    for i, cell in enumerate(cells):
        if cell.text.strip() == "Name":
            name_index = i
        if cell.text.strip() == "FideID":
            fide_id_index = i
        if cell.text.strip() == "FED":
            country_index = i
        if cell.text.strip() == "Rtg" or cell.text.strip() == "RtgI":
            rating_index = i
    rows = table.find_all('tr')[1:]
    for row in rows:
        participant = {}
        cells = row.find_all('td')
        if len(cells) < 5:  # Check if the row has the required number of cells to avoid index errors
            continue
        fide_id_cell = cells[fide_id_index]
        rating_cell = cells[rating_index]
        seed_number_cell = cells[0]
        name_cell = cells[name_index]
        country_cell = cells[country_index]
        participant["fide_id"] = fide_id_cell.text.strip()
        participant["name"] = name_cell.text.strip()
        participant["seed_number"] = seed_number_cell.text.strip()
        participant["rating"] = rating_cell.text.strip()
        participant["country"] = country_cell.text.strip()
        participants.append(participant)
    return participants


def get_performance_data(fide_ids):
    driver = None
    def initialize_driver(driver):
        if driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=options)
        return driver

    def close_driver(driver):
        if driver:
            driver.quit()
        return driver
    driver = initialize_driver(driver)  # Initialize WebDriver if not already done

    participants = []
    for fide_id in fide_ids:
        print("Starting rating calculation for id: " + fide_id)
        participant = {"fide_id": fide_id}
        fide_url = f"https://ratings.fide.com/profile/{fide_id}/calculations"
        if len(fide_id.strip()) == 0:
             participant["rating_change_year"] = "N/A"
             participant["rating_change_three_years"] = "N/A"
             participant["birthday_year"] = "N/A"
             participants.append(participant)
             continue
        participant = {"fide_id": fide_id}
        driver.get(fide_url)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'profile-table.profile-table_colors'))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        year = soup.find_all('div', class_='profile-top-info__block__row__data')[3].text.strip()
        participant["birthday_year"] = year
        if int(year) >= int(datetime.date.today().year) - 15:
            # means player is at least 15 years old
            participant["normal_player"] = True
        else:
            participant["normal_player"] = False
        table = soup.find('table', class_='profile-table profile-table_colors')
        rows = table.find('tbody').find_all('tr')
        counter_three_years = 0
        rating_change = 0
        for row in rows:
            columns = row.find_all('td')
            counter_three_years = counter_three_years + 1
            if counter_three_years == 12:
                #date = columns[0].text.strip()
                participant["rating_change_year"] = rating_change

            if counter_three_years == 36:
                participant["rating_change_three_years"] = rating_change
                break
            if columns[1].text.strip() != "No Games":
                #link = f"https://ratings.fide.com/{columns[1].find('a', class_='tur')['href']}"
                #response = requests.get(link)
                #soup = BeautifulSoup(response.content, 'html.parser')
                update_string = columns[1].text.split()
                # if only available is shown, then first rating was gained in this month, no changes otherwise
                if len(update_string) == 1:
                    continue
                rating_change = rating_change + float(update_string[1].strip())
                #performance_data.append((date, rating_change))
        participants.append(participant)
    driver = close_driver(driver)
    return participants


#participants = extract_participants("https://chess-results.com/tnr792656.aspx")
#average_rating_change = analyze_participant_performance(participants)
#print(average_rating_change)
#participants = get_performance_data([])
#print(participants)