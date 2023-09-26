import os

import psycopg2
from datetime import datetime

def connetDB():
    conn = psycopg2.connect(
        host="localhost",
        database="crossDB",
        user="postgres",
        password="fh1q2w3e"
    )
    return conn


def get_team_discr(team):
    try:
        with open(f"teams/{team}/discr.txt", "r", encoding='UTF-8') as f:
            dicr = f.read()
            return dicr
    except:
        return None


def write_team(team):

    dicr = get_team_discr(team)

    conn = connetDB()
    # Создайте объект-курсор для выполнения запросов
    cur = conn.cursor()

    # Выполните SQL-запрос на поиск записи в таблице
    cur.execute(f"SELECT COUNT(*) FROM api_team WHERE name = %s;", (team,))

    # Получите результаты запроса
    result = cur.fetchone()

    if result[0] == 0:
        cur.execute(
            f"INSERT INTO api_team(name, photo, description) VALUES (%s, %s, %s);", (team, "/teamlogo/" + team, dicr,))
        # Получите результаты запроса (None - успешно)
        result = conn.commit()
        if result == None:
            print(f"Запсись {team} успешно добавлена")
        else:
            print(f"При доавблении записи {team} произошла ошибка", result)
    else:
        cur.execute(f"SELECT * FROM api_team WHERE name = %s;", (team,))
        result = cur.fetchone()
        if result[3] != dicr:
            cur.execute(f"UPDATE api_team SET description = '{dicr}' WHERE id = {result[0]}")
            conn.commit()
            print("Описание обновлено")


def write_all_teams():
    # Получите текущий путь к папке проекта
    project_directory = os.getcwd()

    # Укажите относительный путь к каталогу, для которого нужно получить имена папок
    directory = os.path.join(project_directory, "teams")

    # Получите список всех элементов (файлов и папок) в указанном каталоге
    all_items = os.listdir(directory)

    # Отфильтруйте только папки из списка элементов
    folders = [item for item in all_items if os.path.isdir(os.path.join(directory, item))]

    # Выведите имена всех папок
    for folder in folders:
        print(folder)
        write_team(folder)


def read_player_info(nick):
    name = nationality = team = teamid_id = photo = description = aspect_ratio = cfg = commands = dpi = facebook = \
        image_format = instagram = m_acceleration = m_freq = m_rawinput = m_sens_game = m_sens_windows = m_sens_zoom = \
        refresh_rate = resolution = sharecode = steam = twitch = twitter = vk = youtube = None

    try:
        with open(f"CSGOSettings/{nick}/info.txt", "r", encoding='UTF-8') as f:
            dicr = f.readlines()
            for line in dicr:
                temp1, temp2 = line.strip().split("~")
                if temp1 == "Имя":
                    name = temp2
                elif temp1 == "DPI:":
                    dpi = temp2
                elif temp1 == "Частота мыши:":
                    m_freq = temp2
                elif temp1 == "Чувствительность мыши в игре:":
                    m_sens_game = temp2
                elif temp1 == "Чувствительность мыши в зуме:":
                    m_sens_zoom = temp2
                elif temp1 == "Чувствительность мыши в Windows:":
                    m_sens_windows = temp2
                elif temp1 == "m_rawinput:":
                    m_rawinput = temp2
                elif temp1 == "Ускорение мыши:":
                    m_acceleration = temp2
                elif temp1 == "Разрешение:":
                    resolution = temp2
                elif temp1 == "Соотношение сторон:":
                    aspect_ratio = temp2
                elif temp1 == "Формат изображения:":
                    image_format = temp2
                elif temp1 == "Частота обновления:":
                    refresh_rate = temp2
                elif temp1 == "sharecode":
                    sharecode = temp2
                elif temp1 == "Параметры запуска":
                    commands = temp2
                elif temp1 == "st":
                    steam = temp2
                elif temp1 == "twitch":
                    twitch = temp2
                elif temp1 == "fb":
                    facebook = temp2
                elif temp1 == "tw":
                    twitter = temp2
                elif temp1 == "in":
                    instagram = temp2
                elif temp1 == "vk":
                    vk = temp2
                elif temp1 == "yt":
                    youtube = temp2
                elif temp1 == "Команда":
                    team = temp2
                elif temp1 == "Страна":
                    nationality = temp2
    except Exception as ex:
        print(ex)
        return False
    try:
        conn = connetDB()
        # Создайте объект-курсор для выполнения запросов
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM api_team WHERE name = %s;", (team,))
        result = cur.fetchone()
        teamid_id = result[0]
    except Exception as ex:
        print("team id не найден", ex)
        teamid_id = None

    try:
        with open(f"CSGOSettings/{nick}/discr.txt", "r", encoding='UTF-8') as f:
            description = f.read()
    except:
        pass
    try:
        with open(f"CSGOSettings/{nick}/image.png", "r", encoding='UTF-8'):
            photo = f"/playerlogo/{nick}"
    except:
        pass
    try:
        with open(f"CSGOSettings/{nick}/config.cfg", "r", encoding='UTF-8'):
            cfg = f"/playercfg/{nick}"
    except:
        pass

    return name, nationality, team, teamid_id, photo, description, aspect_ratio, cfg, commands, dpi, facebook, image_format, \
        instagram, m_acceleration, m_freq, m_rawinput, m_sens_game, m_sens_windows, m_sens_zoom, refresh_rate, \
        resolution, sharecode, steam, twitch, twitter, vk, youtube



def write_player(nick):
    conn = connetDB()
    # Создайте объект-курсор для выполнения запросов
    cur = conn.cursor()

    # Выполните SQL-запрос на поиск записи в таблице
    cur.execute(f"SELECT COUNT(*) FROM api_player WHERE nick = %s;", (nick,))

    # Получите результаты запроса
    result = cur.fetchone()

    if result[0] == 0 and read_player_info(nick) != False:
        name, nationality, team, teamid_id, photo, description, aspect_ratio, cfg, commands, dpi, facebook, image_format, \
            instagram, m_acceleration, m_freq, m_rawinput, m_sens_game, m_sens_windows, m_sens_zoom, refresh_rate, \
            resolution, sharecode, steam, twitch, twitter, vk, youtube = read_player_info(nick)
        cur.execute(
            f"INSERT INTO api_player(nick, name, nationality, team, teamid_id, photo, description, aspect_ratio, cfg, "
            f"commands, dpi, facebook, image_format, instagram, m_acceleration, m_freq, m_rawinput, m_sens_game, "
            f"m_sens_windows, m_sens_zoom, refresh_rate, resolution, sharecode, steam, twitch, twitter, vk, "
            f"youtube, updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            f"%s, %s, %s, %s, %s, %s, %s, %s, %s);", (nick ,name, nationality, team, teamid_id, photo, description, aspect_ratio, cfg, commands, dpi, facebook, image_format, \
            instagram, m_acceleration, m_freq, m_rawinput, m_sens_game, m_sens_windows, m_sens_zoom, refresh_rate, \
            resolution, sharecode, steam, twitch, twitter, vk, youtube, datetime.now(),))
        # Получите результаты запроса (None - успешно)
        result = conn.commit()
        if result == None:
            print(f"Запсись {nick} успешно добавлена")
        else:
            print(f"При доавблении записи {nick} произошла ошибка", result)
    elif result[0] > 0 and read_player_info(nick) != False:
        name, nationality, team, teamid_id, photo, description, aspect_ratio, cfg, commands, dpi, facebook, image_format, \
            instagram, m_acceleration, m_freq, m_rawinput, m_sens_game, m_sens_windows, m_sens_zoom, refresh_rate, \
            resolution, sharecode, steam, twitch, twitter, vk, youtube = read_player_info(nick)
        # Выполните SQL-запрос на поиск записи в таблице
        cur.execute(f"SELECT * FROM api_player WHERE nick = %s;", (nick,))

        # Получите результаты запроса
        result = cur.fetchone()
        if result[2] != name:
            cur.execute(f"UPDATE api_player SET name=%s, updated=%s WHERE nick = %s;", (name, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{name} {nick} успешно обновлено")
            else:
                print(f"При обновлении {name} {nick} произошла ошибка", result1)
        if result[3] != nationality:
            cur.execute(f"UPDATE api_player SET nationality=%s, updated=%s WHERE nick = %s;", (nationality, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{nationality} {nick} успешно обновлено")
            else:
                print(f"При обновлении {nationality} {nick} произошла ошибка", result1)
        if result[4] != team:
            cur.execute(f"UPDATE api_player SET team=%s, updated=%s WHERE nick = %s;", (team, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{team} {nick} успешно обновлено")
            else:
                print(f"При обновлении {team} {nick} произошла ошибка", 1)
        if result[5] != teamid_id:
            cur.execute(f"UPDATE api_player SET teamid_id=%s, updated=%s WHERE nick = %s;", (teamid_id, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{teamid_id} {nick} успешно обновлено")
            else:
                print(f"При обновлении {teamid_id} {nick} произошла ошибка", result1)
        if result[6] != photo:
            cur.execute(f"UPDATE api_player SET photo=%s, updated=%s WHERE nick = %s;", (photo, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{photo} {nick} успешно обновлено")
            else:
                print(f"При обновлении {photo} {nick} произошла ошибка", result1)
        if result[7] != description:
            cur.execute(f"UPDATE api_player SET description=%s, updated=%s WHERE nick = %s;", (description, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{description} {nick} успешно обновлено")
            else:
                print(f"При обновлении {description} {nick} произошла ошибка", result1)
        if result[8] != aspect_ratio:
            cur.execute(f"UPDATE api_player SET aspect_ratio=%s, updated=%s WHERE nick = %s;", (aspect_ratio, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{aspect_ratio} {nick} успешно обновлено")
            else:
                print(f"При обновлении {aspect_ratio} {nick} произошла ошибка", result1)
        if result[9] != cfg:
            cur.execute(f"UPDATE api_player SET cfg=%s, updated=%s WHERE nick = %s;", (cfg, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{cfg} {nick} успешно обновлено")
            else:
                print(f"При обновлении {cfg} {nick} произошла ошибка", result1)
        if result[10] != commands:
            cur.execute(f"UPDATE api_player SET commands=%s, updated=%s WHERE nick = %s;", (commands, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{commands} {nick} успешно обновлено")
            else:
                print(f"При обновлении {commands} {nick} произошла ошибка", result1)
        if str(result[11]) != dpi:
            cur.execute(f"UPDATE api_player SET dpi=%s, updated=%s WHERE nick = %s;", (dpi, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{dpi} {nick} успешно обновлено")
            else:
                print(f"При обновлении {dpi} {nick} произошла ошибка", result1)
        if result[12] != facebook:
            cur.execute(f"UPDATE api_player SET facebook=%s, updated=%s WHERE nick = %s;", (facebook, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{facebook} {nick} успешно обновлено")
            else:
                print(f"При обновлении {facebook} {nick} произошла ошибка", result1)
        if result[13] != image_format:
            cur.execute(f"UPDATE api_player SET image_format=%s, updated=%s WHERE nick = %s;", (image_format, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{image_format} {nick} успешно обновлено")
            else:
                print(f"При обновлении {image_format} {nick} произошла ошибка", result1)
        if result[14] != instagram:
            cur.execute(f"UPDATE api_player SET instagram=%s, updated=%s WHERE nick = %s;", (instagram, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{instagram} {nick} успешно обновлено")
            else:
                print(f"При обновлении {instagram} {nick} произошла ошибка", result1)
        if result[15] != m_acceleration:
            cur.execute(f"UPDATE api_player SET m_acceleration=%s, updated=%s WHERE nick = %s;", (m_acceleration, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{m_acceleration} {nick} успешно обновлено")
            else:
                print(f"При обновлении {m_acceleration} {nick} произошла ошибка", result1)
        if result[16] != m_freq:
            cur.execute(f"UPDATE api_player SET m_freq=%s, updated=%s WHERE nick = %s;", (m_freq, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{m_freq} {nick} успешно обновлено")
            else:
                print(f"При обновлении {m_freq} {nick} произошла ошибка", result1)
        if result[17] != m_rawinput:
            cur.execute(f"UPDATE api_player SET m_rawinput=%s, updated=%s WHERE nick = %s;", (m_rawinput, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{m_rawinput} {nick} успешно обновлено")
            else:
                print(f"При обновлении {m_rawinput} {nick} произошла ошибка", result1)
        if result[18] != m_sens_game:
            cur.execute(f"UPDATE api_player SET m_sens_game=%s, updated=%s WHERE nick = %s;", (m_sens_game, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{m_sens_game} {nick} успешно обновлено")
            else:
                print(f"При обновлении {m_sens_game} {nick} произошла ошибка", result1)
        if result[19] != m_sens_windows:
            cur.execute(f"UPDATE api_player SET m_sens_windows=%s, updated=%s WHERE nick = %s;", (m_sens_windows, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{m_sens_windows} {nick} успешно обновлено")
            else:
                print(f"При обновлении {m_sens_windows} {nick} произошла ошибка", result1)
        if result[20] != m_sens_zoom:
            cur.execute(f"UPDATE api_player SET m_sens_zoom=%s, updated=%s WHERE nick = %s;", (m_sens_zoom, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{m_sens_zoom} {nick} успешно обновлено")
            else:
                print(f"При обновлении {m_sens_zoom} {nick} произошла ошибка", result1)
        if result[21] != refresh_rate:
            cur.execute(f"UPDATE api_player SET refresh_rate=%s, updated=%s WHERE nick = %s;", (refresh_rate, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{refresh_rate} {nick} успешно обновлено")
            else:
                print(f"При обновлении {refresh_rate} {nick} произошла ошибка", result1)
        if result[22] != resolution:
            cur.execute(f"UPDATE api_player SET resolution=%s, updated=%s WHERE nick = %s;", (resolution, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{resolution} {nick} успешно обновлено")
            else:
                print(f"При обновлении {resolution} {nick} произошла ошибка", result1)
        if result[23] != sharecode:
            cur.execute(f"UPDATE api_player SET sharecode=%s, updated=%s WHERE nick = %s;", (sharecode, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{sharecode} {nick} успешно обновлено")
            else:
                print(f"При обновлении {sharecode} {nick} произошла ошибка", result1)
        if result[24] != steam:
            cur.execute(f"UPDATE api_player SET steam=%s, updated=%s WHERE nick = %s;", (steam, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{steam} {nick} успешно обновлено")
            else:
                print(f"При обновлении {steam} {nick} произошла ошибка", result1)
        if result[25] != twitch:
            cur.execute(f"UPDATE api_player SET twitch=%s, updated=%s WHERE nick = %s;", (twitch, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{twitch} {nick} успешно обновлено")
            else:
                print(f"При обновлении {twitch} {nick} произошла ошибка", result1)
        if result[26] != twitter:
            cur.execute(f"UPDATE api_player SET twitter=%s, updated=%s WHERE nick = %s;", (twitter, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{twitter} {nick} успешно обновлено")
            else:
                print(f"При обновлении {twitter} {nick} произошла ошибка", result1)
        if result[28] != vk:
            cur.execute(f"UPDATE api_player SET vk=%s, updated=%s WHERE nick = %s;", (vk, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{vk} {nick} успешно обновлено")
            else:
                print(f"При обновлении {vk} {nick} произошла ошибка", result1)
        if result[29] != youtube:
            cur.execute(f"UPDATE api_player SET youtube=%s, updated=%s WHERE nick = %s;", (youtube, datetime.now(), nick,))
            result1 = conn.commit()
            if result1 == None:
                print(f"{youtube} {nick} успешно обновлено")
            else:
                print(f"При обновлении {youtube} {nick} произошла ошибка", result1)


def write_all_players():
    # Получите текущий путь к папке проекта
    project_directory = os.getcwd()

    # Укажите относительный путь к каталогу, для которого нужно получить имена папок
    directory = os.path.join(project_directory, "CSGOSettings")

    # Получите список всех элементов (файлов и папок) в указанном каталоге
    all_items = os.listdir(directory)

    # Отфильтруйте только папки из списка элементов
    folders = [item for item in all_items if os.path.isdir(os.path.join(directory, item))]

    # Выведите имена всех папок
    for folder in folders:
        print(folder)
        write_player(folder)

if __name__ == "__main__":
    #write_all_players()
    write_player("sly")