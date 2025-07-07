import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
csv_filename = 'matches.csv'
url = "https://www.yallakora.com/match-center?date=7/01/2025"
def extract_leagues_and_matches_to_csv(url, csv_filename):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    match_cards = soup.find_all('div', class_='matchCard')
    print(f"Found {len(match_cards)} leagues")

    # Create a list to store all data rows
    all_matches = []

    for card in match_cards:
        # Extract league name
        league_tag = card.find('a', class_='tourTitle')
        league_name = league_tag.find('h2').get_text(strip=True) if league_tag else "Unknown League"

        # Find match container
        matches_container = card.find('div', class_='ul')
        if not matches_container:
            continue

        # Extract each match
        matches = matches_container.find_all('div', class_='item')
        for match in matches:
            # Extract team names
            teamA = match.find('div', class_='teamA')
            teamB = match.find('div', class_='teamB')
            status = match.find('div', class_='matchStatus') 
            teamA_name = teamA.find('p').get_text(strip=True) if teamA else "Team A Unknown"
            teamB_name = teamB.find('p').get_text(strip=True) if teamB else "Team B Unknown"
            status_name = status.find('span').get_text(strip=True) if status else "Status Unknown"
            # Extract score
            score_spans = match.find('div', class_='MResult').find_all('span', class_='score') if match.find('div', class_='MResult') else []
            score = f"{score_spans[0].get_text()} - {score_spans[1].get_text()}" if len(score_spans) >= 2 else "Score Unknown"

            # Extract time
            time_tag = match.find('span', class_='time')
            match_time = time_tag.get_text(strip=True) if time_tag else "Time Unknown"

            # Append match as a dictionary
            all_matches.append({
                'League': league_name,
                'Team A': teamA_name,
                'Team B': teamB_name,
                "Status":status_name,
                'Score': score,
                'Time': match_time
            })

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(all_matches)
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')  # utf-8-sig supports Arabic characters

    print(f"Saved {len(df)} matches to {csv_filename}")


# Usage example:
extract_leagues_and_matches_to_csv(url, csv_filename)
