import glob
import os


def clearCFG(nick):
    #print(nick)
    delete = ["", "say www.CSGOSETTINGS.ru", "--- CSGOSETTINGS.ru ---",
              "echo ---------------------------------------------------", "echo Site - CSGOSETTINGS.ru",
              "echo VK - vk.com/CSGOSETTINGS_ru", "echo Steam - steamcommunity.com/groups/CSGOSETTINGS_ru",
              "echo CSGOSETTINGS.ru - CFG for CS:GO", "п»ї--- CSGOSETTINGS.ru ---",
              "say CFG for CSGO - www.CSGOSETTINGS.ru", "--- CSGOSETTINGS.ru ---", "-вЂ” CSGOSETTINGS.ru вЂ”-",
              "--- CSGOSETTINGS.ru --- ", 'name "Xyp9x.cfg www.CSGOSETTINGS.ru"',
              'echo Xyp9x.cfg for www.CSGOSETTINGS.ru', "-- CSGOSETTINGS.ru ---", "--- CSGOSETTINGS.ru ---\\"]

    split = ['"+spray_menusay www.CSGOSETTINGS.ru"', ";say www.CSGOSETTINGS.ru", '"; say www.CSGOSETTINGS.ru"',
             '" ;say www.CSGOSETTINGS.ru"', "say CFG for CSGO - www.CSGOSETTINGS.ru", '"say www.CSGOSETTINGS.ru"']

    project_root = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(project_root, "CSGOSettings")
    folder_path = os.path.join(folder_path, nick)
    extension = "*.cfg"  # Укажите нужное расширение файлов

    file_paths = glob.glob(f"{folder_path}/{extension}")

    file_names = [file_path.split("/")[-1] for file_path in file_paths]

    for file_name in file_names:
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                with open(file_name, 'w') as file:
                    for line in lines:
                        if line.strip("\n") not in delete:

                            for i in split:
                                if i in line.strip("\n"):
                                    # print(line)
                                    line = line.replace(i, "")

                            file.write(line)
                            if "csgosettings" in line.lower():
                                print(line)
        except Exception as ex:
            print(ex)
            return("Нет конфига")





if __name__ == "__main__":
    clearCFG("SLY")
    #with open("CSGOSettings/CSGOSettingsProURL.txt", "r") as f:
     #   for line in f:
      #      name, link = line.strip().split(":")
       #     clearCFG(name)