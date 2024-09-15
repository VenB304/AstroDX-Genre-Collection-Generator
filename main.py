import os
import json
import urllib.request

def parse_JSON_Database():
    maimaisongInfoJSON_hasLoaded = False
    genre_manualCheckJSON_hasLoaded = False

    try:
        response = urllib.request.urlopen(maimai_JP_songlist_URL)
        if response.status == 200:
            maimaiSongInfoJSON = json.loads(response.read())
            print("online official maimai song information loaded")
        else:
            response = urllib.request.urlopen(maimai_JP_songlist_other_URL)
            if response.status == 200:
                maimaiSongInfoJSON = json.loads(response.read())
                print("Fallback: online other official maimai song information loaded")
            else:
                print(f"maimaisongInfoJSON: Failed to fetch data, status code: {response.status}")
                print("Fallback: loading from local database")
                fallback = open("AstroDX-Collection-Genre-Reorganizer/data/maimai_songs.json", 'r', encoding='utf-8-sig')
                maimaiSongInfoJSON = json.load(fallback)
                print("Fallback: offline official maimai song information loaded")
                fallback.close()
        maimaisongInfoJSON_hasLoaded = True
    except Exception as e:
        print(f"maimaisongInfoJSON: Error fetching or parsing JSON: {e}")
        try:
            fallback = open("AstroDX-Collection-Genre-Reorganizer/data/maimai_songs.json", 'r', encoding='utf-8-sig')
            print("Fallback: loading from local database")
            maimaiSongInfoJSON = json.load(fallback)
            print("Fallback offline official maimai song information loaded")
            maimaisongInfoJSON_hasLoaded = True
            fallback.close()
        except:
            maimaiSongInfoJSON = []
            print("Failed to load maimai song information")
            maimaisongInfoJSON_hasLoaded = False

    try:
        response = urllib.request.urlopen(genre_manualCheckURL)
        if response.status == 200:
            genre_manualCheckJSON = json.loads(response.read())
            print("online manual checking json for genre loaded")
        else:
            print(f"genre manual check json: Failed to fetch data, status code: {response.status}")
            print("Fallback: loading from local database")
            fallback = open("AstroDX-Collection-Genre-Reorganizer/data/genre_manualCheck.json", 'r', encoding='utf-8-sig')
            genre_manualCheckJSON = json.load(fallback)
            print("Fallback: offline manual checking json for genre loaded")
            fallback.close()
        genre_manualCheckJSON_hasLoaded = True
        
    except Exception as e:
        print(f"genre manual check json: Error fetching or parsing JSON: {e}")
        try:
            print("Fallback: loading from local database")
            fallback = open("AstroDX-Collection-Genre-Reorganizer/data/genre_manualCheck.json", 'r', encoding='utf-8-sig')
            genre_manualCheckJSON = json.load(fallback)
            print("Fallback: offline genre to title list loaded")
            genre_manualCheckJSON_hasLoaded = True
            fallback.close()
        except:
            genre_manualCheckJSON = []
            print("Failed to load genre to title information")
            genre_manualCheckJSON_hasLoaded = False

    if not maimaisongInfoJSON_hasLoaded or not genre_manualCheckJSON_hasLoaded:
        print("Failed to load all JSON files, please check your internet connection or the files in the directory")
        print(f"maimaisongInfoJSON: {maimaisongInfoJSON_hasLoaded}\ngenre_manualCheckJSON: {genre_manualCheckJSON_hasLoaded}\n")
        exit()

    elif maimaisongInfoJSON_hasLoaded and genre_manualCheckJSON_hasLoaded:
        print("All JSON files loaded successfully")
        print("Parsing genre information")

        for item in maimaiSongInfoJSON:
            getCategory = item.get('catcode')
            getTitle = item.get('title')
            match getCategory:
                case "maimai":
                    title_to_Genre["maimai"].append(getTitle)
                case "POPS＆アニメ":
                    title_to_Genre["POPS＆ANIME"].append(getTitle)
                case "ゲーム＆バラエティ":
                    title_to_Genre["GAME&VARIETY"].append(getTitle)
                case "東方Project":
                    title_to_Genre["TOUHOUProject"].append(getTitle)
                case "niconico＆ボーカロイド":
                    title_to_Genre["niconico＆VOCALOID"].append(getTitle)
                case "オンゲキ＆CHUNITHM":
                    title_to_Genre["ONGEKI&CHUNITHM"].append(getTitle)
                case "宴会場":
                    continue
                case "_":
                    print(f"WARNIING: Unknown catcode: {item.get('catcode')} Title: {getTitle}")
        
        print("Genre information parsed")
        print("Parsing complete")

    return maimaiSongInfoJSON, genre_manualCheckJSON

def parse_maidata(filepath):
    lv_7_value = None
    title_value = None
    
    with open(filepath, 'r', encoding='utf-8-sig') as file:
        for line in file:
            if line.startswith("&title="):
                title_value = line.strip().split('=')[1]
                if not title_value:  # If title is somehow empty
                    print(f"Warning: Title is empty in file {filepath}")
                    title_value = ""
            elif line.startswith("&lv_7="):
                lv_7_value = line.strip().split('=')[1]
    
    return lv_7_value, title_value

def check_and_List(root_path,genre_manualCheckJSON, catcode):
    Pop_titles, Vocaloid_titles, Touhou_titles, variety_titles, Maimai_titles, gekichu_titles, Utage_titles, Chinese_titles, Unidentifiedtitles = [],[],[],[],[],[],[],[],[]
    Pop_folders, Vocaloid_folders, Touhou_folders, variety_folders, Maimai_folders, gekichu_folders, Utage_folders, Chinese_folders, Unidentifiedfolders = [],[],[],[],[],[],[],[],[]
    for root, dirs, files in os.walk(root_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            maidata_path = os.path.join(folder_path, 'maidata.txt')
            
            if os.path.isfile(maidata_path):
                lv_7_value, title_value = parse_maidata(maidata_path)
                if lv_7_value:
                    print(f"Title: {title_value}\nGenre: UTAGE\nFolder: {folder}\n")
                    Utage_titles.append(title_value)
                    Utage_folders.append(folder)
                    continue
                matchFound = False
                for genre, song_list in title_to_Genre.items():
                    if title_value in song_list or folder in song_list:
                        print(f"Title: {title_value}\nGenre: {genre}\nFolder: {folder}\n")
                        matchFound = True
                        match genre:
                            case "POPS＆ANIME":
                                Pop_titles.append(title_value)
                                Pop_folders.append(folder)
                            case "niconico＆VOCALOID":
                                Vocaloid_titles.append(title_value)
                                Vocaloid_folders.append(folder)
                            case "TOUHOUProject":
                                Touhou_titles.append(title_value)
                                Touhou_folders.append(folder)
                            case "GAME&VARIETY":
                                variety_titles.append(title_value)
                                variety_folders.append(folder)
                            case "maimai":
                                Maimai_titles.append(title_value)
                                Maimai_folders.append(folder)
                            case "ONGEKI&CHUNITHM":
                                gekichu_titles.append(title_value)
                                gekichu_folders.append(folder)
                            case _:
                                continue 
                        break
                    else:
                        continue
                if not matchFound:
                    if title_value in genre_manualCheckJSON:
                        getGenre = genre_manualCheckJSON[title_value]
                        match getGenre:
                            case "POPS＆アニメ":
                                print(f"Title: {title_value}\nGenre: {getGenre}\nFolder: {folder}\n")
                                Pop_titles.append(title_value)
                                Pop_folders.append(folder)
                            case "niconico＆ボーカロイド":
                                print(f"Title: {title_value}\nGenre: {getGenre}\nFolder: {folder}\n")
                                Vocaloid_titles.append(title_value)
                                Vocaloid_folders.append(folder)
                            case "東方Project":
                                print(f"Title: {title_value}\nGenre: {getGenre}\nFolder: {folder}\n")
                                Touhou_titles.append(title_value)
                                Touhou_folders.append(folder)
                            case "ゲーム＆バラエティ":
                                print(f"Title: {title_value}\nGenre: {getGenre}\nFolder: {folder}\n")
                                variety_titles.append(title_value)
                                variety_folders.append(folder)
                            case "maimai":
                                print(f"Title: {title_value}\nGenre: {getGenre}\nFolder: {folder}\n")
                                Maimai_titles.append(title_value)
                                Maimai_folders.append(folder)
                            case "オンゲキ＆CHUNITHM":
                                print(f"Title: {title_value}\nGenre: {getGenre}\nFolder: {folder}\n")
                                gekichu_titles.append(title_value)
                                gekichu_folders.append(folder)
                            case "中国流行乐":
                                print(f"Title: {title_value}\nGenre: {getGenre}\nFolder: {folder}\n")
                                Chinese_titles.append(title_value)
                                Chinese_folders.append(folder)
                            case "宴会場":
                                print(f"Title: {title_value}\nGenre: {getGenre}\nFolder: {folder}\n")
                                Utage_titles.append(title_value)
                                Utage_folders.append(folder)
                            case _:
                                print(f"{title_value} found in manual check, value empty, @venb304 please update manualCheck.json")
                                Unidentifiedtitles.append(title_value)
                else:
                    continue

    length = len((Pop_titles+Vocaloid_titles+Touhou_titles+variety_titles+Maimai_titles+gekichu_titles+Utage_titles+Chinese_titles+Unidentifiedtitles))
    

    checkLog = open("logging/checkingLog.txt","w", encoding="utf-8-sig")
    checkLog.write("Check only Log for genres, the following are the folders that are matched to the genre\n")
    checkLog.write(f"Total number of charts Identified: {length}\n")
    checkLog.write("Pop and Anime | POPS＆アニメ:\n")
    for item in Pop_titles:
        checkLog.write(f'\t"{item}":"",\n')
    checkLog.write("Niconico and Vocaloid | niconico＆ボーカロイド:\n")
    for item in Vocaloid_titles:
        checkLog.write(f'\t"{item}":"",\n')
    checkLog.write("Touhou Project | 東方Project:\n")
    for item in Touhou_titles:
        checkLog.write(f'\t"{item}":"",\n')
    checkLog.write("Game and Variety | ゲーム＆バラエティ:\n")
    for item in variety_titles:
        checkLog.write(f'\t"{item}":"",\n')
    checkLog.write("maimai:\n")
    for item in Maimai_titles:
        checkLog.write(f'\t"{item}":"",\n')
    checkLog.write("Ongeki and Chunithm | オンゲキ＆CHUNITHM:\n")
    for item in gekichu_titles:
        checkLog.write(f'\t"{item}":"",\n')
    checkLog.write("Utage | 宴会場:\n")
    for item in Utage_titles:
        checkLog.write(f'\t"{item}":"",\n')
    checkLog.write("Chinese Pop | 中国流行乐:\n")
    for item in Chinese_titles:
        checkLog.write(f'\t"{item}":"",\n')
    checkLog.write("\nUnidentified:\n")
    for item in Unidentifiedtitles:
        checkLog.write(f'\t"{item}":"",\n')

    checkLog.write("If no charts falls under unidentified, then the collections are supported and is able to be reorganized properly and automatically.\n")
    checkLog.close()
    print("\nChecking complete, See checkingLog.txt in logging folder for results\n")
    generate_manifest(Pop_folders, catcode, 0)
    generate_manifest(Vocaloid_folders, catcode, 1)
    generate_manifest(Touhou_folders, catcode, 2)
    generate_manifest(variety_folders, catcode, 3)
    generate_manifest(Maimai_folders, catcode, 4)
    generate_manifest(gekichu_folders, catcode, 5)
    generate_manifest(Utage_folders, catcode, 6)
    generate_manifest(Chinese_folders, catcode, 7)
    generate_manifest(Unidentifiedfolders, catcode, 8)
    print("\nManifest Generation complete, See Collection Folder for results\n")
    

def generate_manifest(folder_name_list, catcode, genreCode):
    if folder_name_list:
        os.makedirs('Collection/'+catcode[genreCode], exist_ok=True)
        manifest = open("Collection/"+catcode[genreCode]+"/manifest.json", "w", encoding="utf-8-sig")
        reformated_list = str(folder_name_list).replace("'", "\"")
        manifest.write("{\"name\": \"" + catcode[genreCode] + "\", \"levelIds\": " + reformated_list + "}")
        manifest.close

title_to_Genre = {
    "POPS＆ANIME": [],
    "niconico＆VOCALOID": [],
    "TOUHOUProject": [],
    "GAME&VARIETY": [],
    "maimai": [],
    "ONGEKI&CHUNITHM": []    
}

maimaiSongInfoJSON = []
genre_manualCheckJSON = []

genre_manualCheckURL = "https://raw.githubusercontent.com/VenB304/AstroDX-Collection-Reorganizer/main/data/genre_manualCheck.json"
maimai_JP_songlist_URL = "https://maimai.sega.jp/data/maimai_songs.json"
maimai_JP_songlist_other_URL = "https://raw.githubusercontent.com/VenB304/AstroDX-Collection-Reorganizer/main/data/maimai_songs.json"

maimaiSongInfoJSON, genre_manualCheckJSON = parse_JSON_Database()

catcode = [["POPS＆アニメ", "niconico＆ボーカロイド", "東方Project", "ゲーム＆バラエティ", "maimai", "オンゲキ＆CHUNITHM", "宴会場", "中国流行乐","UNIDENTIFIED"],["POPS＆ANIME", "niconico＆VOCALOID", "TOUHOU Project", "GAME＆VARIETY", "maimai", "ONGKEI＆CHUNITHM", "UTAGE", "CHINESE-POP","UNIDENTIFIED"]]

running = True

while running:
    print("\nWhat do you wanna do")
    print("[1] Check and Generate manifest.json files now")
    print("[2] Manually Check and append Unidentified")
    print("[0] Exit")
    choice = str(input("\nChoice: "))
    match choice:
        case "1":
            print("This program assumes the path you are entering is the \"Levels\" Folder of the game through an ftp server from the device and has root access")
            print("Due to your installed levels/charts, only matched titles or folder names is able to be manually put in to a genre, if you have a level/chart that you know the genre to, please add it manually after this program is successful")
            root_path = input("Enter the path of levels folder/charts: ")
            chosenLang = False
            catLang = None
            while not chosenLang:
                print("Genre Language")
                print(f"[1] | {catcode[0]}")
                print(f"[2] | {catcode[1]}")
                catLang = str(input("Enter choice: "))
                if catLang in ["1","2"]:
                    chosenLang = True
            check_and_List(root_path, genre_manualCheckJSON, catcode[int(catLang)-1])
            

        case "0":
            print("Goodbye")
            exit()
        case _:
            print("Invalid Choice")
