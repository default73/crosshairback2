import time

import requests
from bs4 import BeautifulSoup as bs


def parsePages():
    temp = []
    URL_TEMPLATE = "https://csgosettings.ru/pro-settings-csgo"
    try:
        r = requests.get(URL_TEMPLATE)
    except Exception as _ex:
        print(_ex)
    if r.status_code != 200:
        print(r.status_code)
        return False
    soup = bs(r.text, "html.parser")
    lastpage = soup.find_all('a', class_="swchItem")

    span_values = []  # Создаем пустой список для хранения числовых значений

    for item in lastpage:
        span = item.find('span')  # Находим тег span в каждом элементе
        if span:
            span_text = span.text.strip()  # Извлекаем текст из тега span и удаляем лишние пробелы
            try:
                span_value = int(span_text)  # Преобразуем текст в числовое значение
                span_values.append(span_value)  # Добавляем числовое значение в список
            except ValueError:
                print(f"Невозможно преобразовать в число: {span_text}")

    return max(span_values)  # Возвращаем список числовых значений


def ParseURLS(page):
    URL_TEMPLATE = "https://csgosettings.ru/pro-settings-csgo?page" + str(page)
    try:
        r = requests.get(URL_TEMPLATE)
    except Exception as _ex:
        print(_ex)
    if r.status_code != 200:
        print(r.status_code)
        return False
    soup = bs(r.text, "html.parser")
    playerlink = soup.find_all('a', class_="player")
    for i in playerlink:
        try:
            link = i.get('href')
            nick = i.find('span', class_="player-title")
            nick = nick.text
            if "csgosettings.ru" not in link:
                print(link)
                print(nick)
                with open("CSGOSettings/CSGOSettingsProURL.txt", "a", encoding="utf-8") as f:
                    f.write(nick + ":" + link + "\n")
        except Exception as Ex:
            print("Ошибка", Ex, i)


if __name__ == "__main__":
    with open("CSGOSettings/CSGOSettingsProURL.txt", "w", encoding="utf-8") as f:
        f.write("")
    for i in range(1, parsePages() + 1):
        ParseURLS(i)

