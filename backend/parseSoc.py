
arr = []
def parseSoc(nick, arr):
    try:
        with open(f"CSGOSettings/{nick}/info.txt", "r", encoding='UTF-8') as f:
            for line in f:
                if "http" in line:
                    id, link = line.strip().split("~")
                    if id not in arr:
                        arr.append(id)
                        print(id, nick, link)
    except:
        pass



with open("CSGOSettings/CSGOSettingsProURL.txt", "r") as f:
    for line in f:
        name, link = line.strip().split(":")
        parseSoc(name, arr)

print(arr)

