import time
import os
import zipfile
from zipfile import ZipFile

import unrar
import requests
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession


def writeToFile(text, nick):
    with open("CSGOSettings/" + nick + "/info.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")


def ParseProInfo(url, nick, full_parse):
    if not os.path.exists("CSGOSettings/" + nick):
        os.mkdir("CSGOSettings/" + nick)
    else:
        if full_parse:
            pass
        else:
            return True

    with open("CSGOSettings/" + nick + "/info.txt", "w", encoding="utf-8") as f:
        f.write("")

    URL_TEMPLATE = "https://csgosettings.ru" + str(url)
    try:
        r = requests.get(URL_TEMPLATE)
    except Exception as _ex:
        print(_ex)
    if r.status_code != 200:
        print(r.status_code)
        return False
    soup = bs(r.text, "html.parser")

    name = soup.find('div', class_="page-player-name title-4").text
    #print("Имя:" + name)
    writeToFile("Имя~" + name, nick)

    settings = soup.find_all('div', class_="page-player-params-item")
    for i in settings:
        temp1 = i.find('span', class_="page-player-label").text
        temp2 = i.find('span', class_="page-player-val").text
        #print(temp1 + temp2)
        writeToFile(temp1 + "~" + temp2, nick)

    try:
        session = HTMLSession()
        response = session.get(URL_TEMPLATE)
        response.html.render()
        crosshair = response.html.find('#crosshairShareCode', first=True).text
        session.close()
        #print("sharecode:" + crosshair)
        writeToFile("sharecode~" + crosshair, nick)

    except:
        return False
        print("Не спарсился шаре код, повторная попытка для", url, nick)

    #parameters = soup.find('div', class_="code-console code-1295-2").find_next().text

    try:
        parameters = soup.find('div', class_="aim-page-item page-player-start")
        parameters = parameters.find('noindex').text
        #print("Параметры запуска:" + parameters)
        writeToFile("Параметры запуска~" + parameters, nick)
    except:
        print("Параметры запуска отсутствуют")

    social = soup.find_all('a', class_="soc")
    for i in social:
        #print(i['id'] + ":" + i['href'])
        writeToFile(i['id'] + "~" + i['href'], nick)

    image = soup.find('div', class_="page-player-images").find_next()['src']
    #print(image)
    response = requests.get("https://csgosettings.ru" + image)
    with open("CSGOSettings/" + nick + "/image.png", "wb") as f:
        f.write(response.content)


    try:
        country_team = soup.find_all('div', class_="page-player-geo-item")
        try:
            team = country_team[0].find('span', class_="page-player-val").text
            writeToFile("Команда~" + team, nick)
        except:
            print("Команды нет")
        try:
            country = country_team[1].find('span', class_="page-player-val").text.replace("\n", "").strip(' ')
            writeToFile("Страна~" + country, nick)
        except:
            print("Страны нет")
    except:
        print("country_team нет")


    try:
        dicr = soup.find('div', class_="descr-cat-text").text
        with open("CSGOSettings/" + nick + "/discr.txt", "w", encoding="utf-8") as f:
            f.write(dicr)
    except:
        print("Описания нет")

    try:
        playerCFG = soup.find('div', class_="page-player-config")
        playerCFG = playerCFG.find("a", class_="btn")["href"]
        #print(playerCFG)
    except:
        print("Не удалось найти конфиг у", nick)
        return True

    URL_TEMPLATE = "https://csgosettings.ru" + str(playerCFG)
    try:
        r = requests.get(URL_TEMPLATE)
        time.sleep(0.5)
        with open(f'./CSGOSettings/{nick}/config.zip', 'wb') as f:
            f.write(r.content)
            f.close()
    except Exception as _ex:
        print(_ex)

    try:
        zip_file = ZipFile(f'./CSGOSettings/{nick}/config.zip')
        dfs = [text_file.filename for text_file in zip_file.infolist()]

        for i in dfs:
            if ".cfg" in i:
                with zipfile.ZipFile(f'./CSGOSettings/{nick}/config.zip', 'r') as zip_file:
                    zip_file.extract(i, path=f'./CSGOSettings/{nick}')
        os.remove(f'./CSGOSettings/{nick}/config.zip')
    except Exception as ex:
        print(f'./CSGOSettings/{nick}/config.zip не распакован ', ex)
        unrar.unrar(nick)
    return True

#ParseProInfo("/dadte-cfg-csgo", "DaDte")

if __name__ == "__main__":
    n = 0
    full_parse = True
    with open("CSGOSettings/CSGOSettingsProURL.txt", "r", encoding="utf-8") as f:
        for line in f:
            name, link = line.strip().split(":")
            while ParseProInfo(link, name, full_parse) != True:
                ParseProInfo(link, name, full_parse)
            n += 1
            print(n, name)
