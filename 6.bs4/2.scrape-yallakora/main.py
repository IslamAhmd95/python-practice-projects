import requests
from bs4 import BeautifulSoup
from datetime import date
import helpers
import json
import os
import csv

while True:
    date_str = input('\nEnter date in format (mm/dd/yyyy), leave empty for today, or type "x" to exit: ').strip()

    if date_str.lower() == 'x':
        print("Exiting the program.")
        exit() 

    if not date_str:
        date_str = date.today().strftime('%m/%d/%Y')
    else:
        check_date = helpers.is_date_valid(date_str)
        if not check_date:
            date_str = date.today().strftime('%m/%d/%Y')
            print('Invalid date, try again')
            continue

    break

page = requests.get(f'https://www.yallakora.com/match-center?date={date_str}#days')
src = page.content
soup = BeautifulSoup(src, 'lxml')

if soup.find('div', {'class': 'noStatsDiv'}):
    print('No matches found')
    exit()

matches = []

matchesList = soup.find_all('div', {'class': 'matchesList'})
for section in matchesList:

    champion_text = section.find_all('a', {'class': 'tourTitle'})[0].h2.get_text(strip=True)
    matchesDetails = section.find_all('div', {'class': 'allData'})

    for matchesDetail in matchesDetails:
        match = dict()

        match['championship'] = champion_text

        topData = matchesDetail.find('div', {'class': 'topData'})
        match['stage'] = topData.find('div', {'class': 'date'}).get_text(strip=True)

        match['teamA'] = matchesDetail.find('div', {'class': 'teamA'}).get_text(strip=True)
        match['teamB'] = matchesDetail.find('div', {'class': 'teamB'}).get_text(strip=True)

        result = matchesDetail.find('div', {'class': 'MResult'})
        result_scores = result.find_all('span', {'class': 'score'})
        if len(result_scores) == 2:
            match['score'] = f"{result_scores[0].get_text(strip=True)} - {result_scores[1].get_text(strip=True)}"
        else:
            match['score'] = 'Not available'

        timeDiv = result.find('span', {'class': 'time'})
        match['time'] = timeDiv.get_text(strip=True) if timeDiv and timeDiv.text.strip() else 'Not available'

        match['status'] = topData.find('div', {'class': 'matchStatus'}).span.get_text(strip=True)
      
        matchPlatformDiv = matchesDetail.find('div', {'class': 'channel icon-channel'})
        match['platform'] = matchPlatformDiv.get_text(strip=True) if matchPlatformDiv else 'Not available'

        matches.append(match)


current_dir = os.path.dirname(os.path.abspath(__file__))

# save to json file
json_file_name = "matches.json"
json_file_path = os.path.join(current_dir, json_file_name)
with open(json_file_path, 'w', encoding='utf-8') as f:
# ensure_ascii=False → tells json.dump() not to escape Arabic or other non-ASCII characters.
# encoding='utf-8' → ensures the file saves Arabic properly.
    json.dump(matches, f, indent=4, ensure_ascii=False)


# save to csv file
csv_file_name = "matches.csv"
csv_file_path = os.path.join(current_dir, csv_file_name)
with open(csv_file_path, 'w', newline="", encoding="utf-8") as f:
    csv_writer = csv.DictWriter(f, fieldnames=matches[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(matches)