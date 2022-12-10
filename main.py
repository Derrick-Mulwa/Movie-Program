import mysql.connector
import subprocess
import os
import humanize
import mariadb

path = r"C:\Users\Administrator\Downloads\Bien - Inauma (kichwahits.com).mp3"


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Firefly."
)

print("Connected to Database successfully!")

mycursor = db.cursor()


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
    with open(path, "rb") as file:
        media = file.read()
    sqlStatement = "INSERT INTO image_store.stored_media(DESCRIPTION, SIZE, FILE_TYPE, MEDIA) VALUES (%s,%s,%s,%s)"
    mycursor.execute(sqlStatement, (details[0], details[1], details[2], media))
    db.commit()


def playMedia(path):
    pgfiles = os.environ["ProgramFiles"]

    vlcpath = ""
    for root, dirs, files in os.walk(pgfiles):
        for f in files:
            name = os.path.join(root, f)
            vlc = name[-7:]
            if vlc == "vlc.exe":
                vlcpath = name



    subprocess.Popen([vlcpath, path])

# mycursor.execute('set global max_allowed_packet=671088640')

path = r"C:\Users\Administrator\Downloads\Bien - Inauma (kichwahits.com).mp3"
pathb = r"C:\Users\Administrator\Desktop\Random projects\Image store\vid.mkv"
upload_to_DB(pathb)


