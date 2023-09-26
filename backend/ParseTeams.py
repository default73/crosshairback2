import os

from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup as bs

def get_team_discr(url, team):
    try:
        r = requests.get(url)
    except Exception as _ex:
        print(_ex)
    if r.status_code != 200:
        print(r.status_code)
        return False
    soup = bs(r.text, "html.parser")

    try:
        discr = soup.find('div', class_="descr-cat-text").text
        lines = discr.split('\n')
        filtered_lines = [line for line in lines if line.strip() and not line.startswith('Немного о')]
        discr2 = '\n'.join(filtered_lines)
        with open("teams/" + team + "/discr.txt", "w", encoding="utf-8") as f:
            f.write(discr2)
    except:
        print("Описания нет")

def ParseTeam():
    URL_TEMPLATE = 'https://csgosettings.ru/files/'
    try:
        r = requests.get(URL_TEMPLATE)
    except Exception as _ex:
        print(_ex)
    if r.status_code != 200:
        print(r.status_code)
        return False
    soup = bs(r.text, "html.parser")

    teams = soup.find_all('td', class_="catsTdI")

    for team in teams:
        try:
            url = team.find('a', class_='team-item-link')['href']
        except Exception as ex:
            #print(team, ex)
            pass
        title = team.find('div', class_='team-item-title').text
        print(title)
        if not os.path.exists("teams/" + title):
            os.mkdir("teams/" + title)

        img = team.find('div', class_='team-item-img').find_next()['src']
        print(img)
        response = requests.get("https://csgosettings.ru" + img)
        with open("teams/" + title + "/image.png", "wb") as f:
            f.write(response.content)
        get_team_discr(url, title)


if __name__ == "__main__":
    ParseTeam()