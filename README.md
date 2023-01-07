# WELCOME TO DERRICK'S MOVIE PROGRAM 

This program is designed to create a database that stores media files which can be accessed by users. The database can be either an online database or a local one, depending on the user's preference.

## Features
* Create a database of media files
* Upload and delete media files from the database (developer mode only)
* Retrieve/download media files from the database
* Automatically play media files with VLC media player once downloaded

## Getting Started
To use this program, you will need to have Python 3 and the VLC media player installed on your computer.The program uses the folowing modules/packages:
* mysql.connector
* subprocess
* os
* humanize
* mariadb

To start the program, navigate to the directory where the program is located and run the following command: python main.py
You will be prompted to press any key. If you press any key, you will enter normal user mode, which allows you to retrieve/download media files from the database. If you enter **1000**, you will enter developer mode, which allows you to upload and delete media files from the database.

## Using the Program
* Normal User Mode: In normal user mode, you can retrieve/download media files from the database by following the prompts in the program. Once you have downloaded a media file, the program will automatically start the VLC media player and play the file for you.

* Developer Mode: In developer mode, you can upload and delete media files from the database by following the prompts in the program. You will need to provide the file path for the media file you want to upload or delete.

#END
