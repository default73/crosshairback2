from ParseCSGOSettingsProInfo import ParseProInfo
from ParseCSGOSettingsProURL import parsePages, ParseURLS
from ParseTeams import ParseTeam
from clearCFG import clearCFG
from db import write_all_players, write_all_teams
from unrar import unrar

with open("CSGOSettings/CSGOSettingsProURL.txt", "w", encoding="utf-8") as f:
    f.write("")
for i in range(1, parsePages() + 1):
    ParseURLS(i)

n = 0
full_parse = True # полное обновление или только запись новых
with open("CSGOSettings/CSGOSettingsProURL.txt", "r", encoding="utf-8") as f:
    for line in f:
        name, link = line.strip().split(":")
        i = 0
        while ParseProInfo(link, name, full_parse) != True and i < 3:
            ParseProInfo(link, name, full_parse)
            i += 1
        n += 1
        print(n, name)


ParseTeam()


with open("CSGOSettings/CSGOSettingsProURL.txt", "r") as f:
    for line in f:
        name, link = line.strip().split(":")
        clearCFG(name)

write_all_teams()
write_all_players()

