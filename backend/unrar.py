import os
import patoolib


def unrar(nick):
    try:
        os.rename(f'./CSGOSettings/{nick}/config.zip', f'./CSGOSettings/{nick}/config.rar')
    except:
        return

    try:
        patoolib.extract_archive(f"./CSGOSettings/{nick}/config.rar", outdir=f"./CSGOSettings/{nick}", interactive=False)

        path = os.listdir(f"./CSGOSettings/{nick}")
        for i in path:
            if ".cfg" not in i and i != "info.txt" and i != "image.png" and i != "discr.txt":
                os.remove(f'./CSGOSettings/{nick}/{i}')
        print(f"CFG {nick} распакован успешно")
    except Exception as ex:
        print(f"Не удалось раcпокавать  f'./CSGOSettings/{nick}/", ex)
        print(f'Попытка переименовать в cfg')
        try:
            os.rename(f'./CSGOSettings/{nick}/config.rar', f'./CSGOSettings/{nick}/config.cfg')
            f = open(f'./CSGOSettings/{nick}/config.cfg')
            f.read()
            f.close()
        except Exception as ex2:
            print("Это даже не CFG", ex2)


#unrar("Twistzz")

if __name__ == "__main__":
    with open("CSGOSettings/CSGOSettingsProURL.txt", "r", encoding="utf-8") as f:
        for line in f:
            name, link = line.strip().split(":")
            unrar(name)