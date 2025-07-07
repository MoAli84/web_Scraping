import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
csv_filename = 'matches.csv'
url = "https://www.yallakora.com/match-center?date=6/9/2025"

def extract(url ,csv_filename):
    web_data =requests.get(url)
    soup =BeautifulSoup(web_data.text,'lxml')
    matches_sections = soup.find_all('div',{'class':'matchCard'})
    print(f"the number of leagues are : {len(matches_sections)}")
    matches_data =[]
    for match_section in matches_sections:
        league_tag = match_section.find('a', {'class': 'tourTitle'})
        league_name = league_tag.find('h2').get_text(strip=True) if league_tag else "League Unknown"

        matches_container = match_section.find('div', {'class': 'ul'})
        if not matches_container:
            continue

        matches = matches_container.find_all('div', {'class': 'item'})
        for match in matches:
            channel_tag = match.find('div', {'class': 'channel icon-channel'})
            channel = channel_tag.get_text(strip=True) if channel_tag else "N/A"

            match_type_div = match.find('div', {'class': 'date'})
            type = match_type_div.get_text(strip=True) if match_type_div else "Type Unknown"

            status_div = match.find('div', {'class': 'matchStatus'})
            status_span = status_div.find('span') if status_div else None
            status_name = status_span.get_text(strip=True) if status_span else "Status Unknown"

            teamA = match.find('div', {'class': 'teamA'})
            teamA_name = teamA.find('p').get_text(strip=True) if teamA and teamA.find('p') else "Team A Unknown"

            teamB = match.find('div', {'class': 'teamB'})
            teamB_name = teamB.find('p').get_text(strip=True) if teamB and teamB.find('p') else "Team B Unknown"

            mresult = match.find('div', class_='MResult')
            score_spans = mresult.find_all('span', class_='score') if mresult else []
            score = f"{score_spans[0].get_text()} - {score_spans[1].get_text()}" if len(score_spans) >= 2 else "Score Unknown"

            time_tag = match.find('span', class_='time')
            match_time = time_tag.get_text(strip=True) if time_tag else "Time Unknown"

        # Save all data into one row (dictionary)
            matches_data.append({
            "league": league_name,
            "channel": channel,
            "match_type": type,
            "status": status_name,
            "teamA": teamA_name,
            "teamB": teamB_name,
            "score": score,
            "time": match_time
            })
            
    with open('matches.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["league", "channel", "match_type", "status", "teamA", "teamB", "score", "time"])
        writer.writeheader()
        writer.writerows(matches_data)        
    df = pd.DataFrame(matches_data)
    df.to_csv("Test.csv", index=False)
extract(url,csv_filename)