import mysql.connector
import subprocess
import os
import humanize
import mariadb

try:
    with open("text.txt", "r") as file:
        file = file.read()
        password = ("".join([file[i] for i in range(len(file)) if i % 2 != 0]))


    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Firefly."
    )

    mycursor = db.cursor()
except:
    print("There was an error connecting to server. Please ensure you have a steady network and restart the program.\n"
          "If the problem persists, contact customer support.")


def startdb():
    try:
        with open("text.txt", "r") as file:
            file = file.read()
            password = ("".join([file[i] for i in range(len(file)) if i % 2 != 0]))

        db = mysql.connector.connect(
            host="fireflydb.cmec70j7uxlm.ap-northeast-1.rds.amazonaws.com",
            user="Firefly",
            password=password
        )

        mycursor = db.cursor()
        return True
    except:
        return False


def create_Database():

    sqlStatement = f"DROP DATABASE IF EXISTS image_store;" \
                   f"CREATE DATABASE image_store;" \
                   f"USE image_store;" \
                   f"CREATE TABLE stored_media(" \
                   f"MEDIA_ID INT PRIMARY KEY AUTO_INCREMENT," \
                   f"DESCRIPTION VARCHAR(1000) NOT NULL," \
                   f"SIZE VARCHAR(50)," \
                   f"FILE_TYPE VARCHAR(20)," \
                   f"MEDIA LONGBLOB NOT NULL" \
                   f");"

    mycursor.execute(sqlStatement)


def newuser():
    mycursor.execute("SHOW DATABASES")
    databases = [i[0] for i in mycursor]

    return False if "image_store" in databases else True


def get_path_details(path):

    findExtension = False
    fileExtension = ""
    i=1
    j=0
    findfilename = False

    if os.path.exists(path) is False:
        return "Path entered doesn't exist"

    maximum = len(path)
    while (findExtension is False) and maximum>=j:
        if path[-i:-(i-1)] == ".":
            fileExtension=path[-(i-1):]
            findExtension = True
        else:
            i+=1
            j+=1

    if j>maximum:
        return "Invalid file!"
    else:
        filename = os.path.basename(path)
        filename = filename[:-i]

    size = humanize.naturalsize(os.stat(path).st_size)

    return filename, size, fileExtension


def upload_to_DB(path):

    details = get_path_details(path)
    if details == "Invalid file!":
        return  "Invalid file!"
    elif details == "Path entered doesn't exist":
        return "Path entered doesn't exist"


    with open(path, "rb") as file:
        media = file.read()

    #mycursor.execute('set global max_allowed_packet=1073741824')
    sqlStatement = "INSERT INTO image_store.stored_media(DESCRIPTION, SIZE, FILE_TYPE, MEDIA) VALUES (%s,%s,%s,%s)"
    mycursor.execute(sqlStatement, (details[0], details[1], details[2], media))
    db.commit()

    return True


def get_from_DB(ID):

    sqlStatement = "SELECT DESCRIPTION, FILE_TYPE, MEDIA FROM image_store.stored_media WHERE MEDIA_ID = %s"
    mycursor.execute(sqlStatement, (ID,))

    data = [i for i in mycursor][0]
    current_directory = os.getcwd()
    downloads_dir = fr"{current_directory}/Downloads"
    if os.path.exists(downloads_dir) is False:
        os.mkdir(downloads_dir)

    path = fr"{downloads_dir}/{data[0]}.{data[1]}"

    media = data[2]

    with open(path, "wb") as myfile:
        myfile.write(media)

    print("Media downloaded successfully!")
    return path


def playMedia(path):

    print("Initializing VLC to play downloaded media!")
    pgfiles = os.environ["ProgramFiles"]

    vlcpath = ""
    for root, dirs, files in os.walk(pgfiles):
        for f in files:
            name = os.path.join(root, f)
            vlc = name[-7:]
            if vlc == "vlc.exe":
                vlcpath = name

    subprocess.Popen([vlcpath, path])


def getMovies():
    mycursor.execute("USE image_store;")
    sqlstatement = f"SELECT MEDIA_ID, DESCRIPTION,SIZE FROM image_store.stored_media;"
    mycursor.execute(sqlstatement)
    return [i for i in mycursor]


def DisplayMovies(movieslist):
    lista = ['MOVIE ID', 'MEDIA NAME/DESCRIPTION', 'SIZE']
    gap = '   '

    heading = f'{lista[0]:10s}{gap}{lista[1]:115s}{gap}{lista[2]:8}'
    print(f"=" * 140)
    print(heading)
    print('=' * 140)

    for listb in movieslist:
        content = f'{str(listb[0]):10s}{gap}{listb[1]:115s}{gap}{str(listb[2]):8}'
        line = "-" * 140
        print(content)
        print(line)


def getUserinput():
    DisplayMovies(getMovies())
    userinput = input("Enter Movie ID: ")
    getInput = False

    while getInput is False:
        try:
            userinput = int(userinput)
            mycursor.execute("SELECT MAX(MEDIA_ID) FROM image_store.stored_media;")
            maximus = [i for i in mycursor][0][0]
            if userinput > maximus:
                continue
            else:
                getInput = True
        except:
            userinput = input("Invalid Media ID! Please enter a valid Movie ID: ")

    return userinput


def updatedb(path, mediaID):
    print("Initializing update...")

    valid = get_path_details(path)
    if type(valid) != tuple:
        print("Invalid path or file type!")
    else:
        filename = valid[0]
        size = valid[1]
        fileExtension = valid[2]

        with open(path, "rb") as file:
            media = file.read()
        sqlstatement = f"UPDATE image_store.stored_media SET " \
                       f"DESCRIPTION = '{filename}', " \
                       f"SIZE = '{size}', " \
                       f"FILE_TYPE = '{fileExtension}', " \
                       f"MEDIA = %s " \
                       f"WHERE MEDIA_ID = {mediaID};"

        print("Uploading database. This will take some time...")

        mycursor.execute("set global max_allowed_packet=1073741824;")

        mycursor.execute(sqlstatement, (media,))
        db.commit()
        print("Update complete!")


def developer():
    exit_admin_menu = False
    print("Welcome to Admin menu!")
    while exit_admin_menu is False:

        choseAction = False
        while choseAction is False:
            action = input("Choose the task to perform.\n"
                           "1. New user initialization.\n"
                          "2. Upload new media to database.\n"
                          "3. Replace/Update media in database.\n"
                          "4. Exit\n"
                          "Select Action: ")

            maxPick = 4
            try:
                action = int(action)
                if action <= maxPick:
                    choseAction = True
                elif action == maxPick:
                    exit_admin_menu = True
                    return True
                else:
                    print("Invalid choice! Choose a valid task!")

            except:
                print("Invalid choice! Choose a valid task!")


        if action == 1:
            try:
                caution = input("\nIf you have an existing database, it will be deleted and a new one created. \n"
                                "Press 1 to proceed or any other key to abort: ")
                if caution == "1":
                    create_Database()
                    print("\nDatabase created successfully! Restart the program to access full admin privileges")

            except:
                print("There was an issue creating Database! Check your network connection and restart the program.\n"
                      "If the issue persists, contact customer support.")


        elif action == 2:
            to_mainmenu = False
            while to_mainmenu is False:
                path = input("Enter path of the media to upload: ")
                status = upload_to_DB(path)
                if status == True:
                    ifExit = input("Media uploaded successfully.\n"
                              "Press 1 to upload another file or press any other key to go back to admin menu:")
                else:
                    ifExit = input("Unsupported file or incorrect path. \n"
                              "Press 1 to re-enter correct file path or any other key to go back to admin menu: ")

                if ifExit != "1":
                    to_mainmenu = True

        elif action == 3:
            to_mainmenu = False
            while to_mainmenu is False:
                DisplayMovies(getMovies())
                media_id = input("Enter movie ID for the media you'd like to update/replace: ")
                mycursor.execute("SELECT MAX(MEDIA_ID) FROM image_store.stored_media;")
                maximus = [i for i in mycursor][0][0]
                try:
                    media_id = int(media_id)
                    if media_id > maximus:
                        print("Invalid MEDIA ID! Please enter a valid Movie ID: ")
                        continue
                    else:
                        path = input("Enter path of the media to upload: ")
                        status = os.path.exists(path)
                        if status == True:
                            updatedb(path, media_id)
                            ifExit = input("Media updated successfully.\n"
                                      "Press 1 to update another file or press any other key to go back to admin menu:")

                        else:
                            ifExit = input("Unsupported file or incorrect path. \n"
                                      "Press 1 to re-enter correct file path or any other key to go back to admin menu: ")

                        if ifExit == "1":
                            continue
                        else:
                            to_mainmenu = True
                except:
                    ifExit = input("Invalid MEDIA ID! Please enter a valid Media ID. \n"
                                   "Press 1 to re-enter correct Media ID or any other key to go back to admin menu ||: ")
                    if ifExit == "1":
                        continue
                    else:
                        to_mainmenu = True



        elif action == 4:
            exit_admin_menu = True

    return True


def normalUser():
    database = startdb()
    if startdb is False:
        print("There was an error connecting to the server. Check your internet connection and restart the program.\n"
              "If the issue persists contact support!")
    else:
        movie = getUserinput()
        moviePath = get_from_DB(movie)
        playMedia(moviePath)


if __name__ == '__main__':
    exit = False

    while exit is False:
        user = input("Welcome to Firefly Movies! Press any key to continue: ")
        if user == "1024":
            exit = developer()
        else:
            print("Initializing. Please wait...")
            normalUser()



