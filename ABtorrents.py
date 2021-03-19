import time
from torf import Torrent
import PySimpleGUI as sg
import mutagen
from mutagen import File
from mutagen.id3 import ID3
import fnmatch
import shutil
import os
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
from mutagen.mp4 import MP4
import re
import configparser
from pathlib import Path
import codecs
import sys
import logging

script_version = 'Beta v.0.3 - ABtorrents uploader Helper'
script_version_short = 'Beta v.0.3'

# set up logging to file -------------------------------------------------------------------
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)-8s%(asctime)s %(name)-12s %(message)s',
                    datefmt='%d-%m-%y (%H:%M)',
                    filename='log.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s%(asctime)s %(name)-8s %(message)s', "%H:%M:%S")
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

logger_config = logging.getLogger('config')
logger_path = logging.getLogger('paths')
logger_torrent = logging.getLogger('torrent')
logger_nfo = logging.getLogger('nfo')
logger_audio = logging.getLogger('audiofile')
logger_meta = logging.getLogger('Mp3 meta')
logger_meta2 = logging.getLogger('Mb4 meta')
logger_cover = logging.getLogger('cover')
logger_internet = logging.getLogger('site')

# END set up logging to file ----------------------------------------------------------------

# Set variables
nfo_author = ''
nfo_narr = ''
nfo_album = ''
nfo_series = ''
num_serie = ''
nfo_audio = ''
nfo_bitrate = ''
nfo_sub = ''
nfo_genre = ''
nfo_year = ''
nfo_asin = ''
nfo_publisher = ''
nfo_copy = ''
nfo_link = ''
nfo_desc = ''
nfo_encoder = ''
nfo_full = ''
nfo_comm = ''
nfo_duration = ''
nfo_unabridged = ''
nfo_release = ''
nfo_size = ''
nfo_url = ''
nfo_notes = ''


# If error pauses script---------------------------------------------------
def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("An error as appeared, press any key and enter to exit.")
    sys.exit(-1)


sys.excepthook = show_exception_and_exit
# END If error pauses script-----------------------------------------------


# Log Version--------------------------------------------------------------
logging.info('Script Version: %s', script_version)
# END Log Version----------------------------------------------------------

# Config-------------------------------------------------------------------
# update the config file
config = configparser.ConfigParser()

# Config ini File
if not os.path.exists('config.ini'):  # if it is not present

    config.add_section('FOLDERS')
    config.add_section('LOGIN')

    config['FOLDERS']['torrent_folder'] = "0"
    config['FOLDERS']['folder_path'] = "0"
    config['FOLDERS']['torrent_file'] = "0"

    config['LOGIN']['firefox_profile'] = "0"
    config['LOGIN']['username'] = "0"
    config['LOGIN']['password'] = "0"

    logger_config.info('Ini Config file was created: config.ini')

    config.write(open('config.ini', 'w'))

    torrent_file_path = config['FOLDERS']['torrent_folder']  # to make folders
    torrent_file = config['FOLDERS']['torrent_file']  # make files
    login_session = config['LOGIN']['firefox_profile']  # profile firefox link
    login_username = config['LOGIN']['username']
    login_password = config['LOGIN']['password']
else:
    # if config file present:
    logger_config.info('The config.ini file is present.')

    config.read(r'config.ini')

    torrent_file_path = config['FOLDERS']['torrent_folder']
    torrent_file = config['FOLDERS']['torrent_file']
    login_session = config['LOGIN']['firefox_profile']
    login_username = config['LOGIN']['username']
    login_password = config['LOGIN']['password']

# END Config-----------------------------------------------------------------

# Paths to file/folder-------------------------------------------------------
folder_path = None
file_path = None

logger_path.info('Please enter your folder or file...')

# Choose torrent folder
sg.theme('Dark Blue 3')  # please make your windows colorful
layout = [[sg.Text('Here you can choose folder or file to make a torrent.')],
          [sg.Text('Later you can choose a path for the .torrent if not in config.')],
          [sg.Text('Folder:', size=(10, 1)), sg.InputText(), sg.FolderBrowse()],
          [sg.Text('File:', size=(10, 1)), sg.InputText(), sg.FileBrowse()],
          [sg.Submit(), sg.Cancel()]]
window = sg.Window(script_version_short, layout, icon=r"favicon.ico", finalize=True)

event, values = window.read()
if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
    logger_path.warning('You have canceled or closed the window the script will now close...')
    window.read(timeout=3000)
    raise SystemExit(0)
window.close()

if values[0] == '' and values[1] == '':
    sg.popup_error('You did not enter anything, so exit is in order!')
    logger_path.warning('All the paths were empty, the script will now close...')
    raise SystemExit(0)

else:
    # values[0] is the variable for the folder path
    folder_path = values[0]  # get the data from the values dictionary

    if folder_path == '':
        pass
    else:
        logger_path.info('Folder path was set: %s', folder_path)

    # values[1] is the variable for the file path
    file_path = values[1]  # get the data from the values dictionary

    if file_path == '':
        pass
    else:
        logger_path.info('File path is: %s', file_path)

# if the file path as nothing create the the torrent from folder torrent
if file_path == '':
    logger_torrent.info('Creating Torrent from folder...please wait')

    # Make torrent from folder
    t = Torrent(path=folder_path,
                trackers=['https://abtorrents.me:2910/announce'],
                comment='In using this torrent you are bound by the ABTorrents Confidentiality Agreement '
                        'By Law')
    # Exclude nfo files
    t.exclude_globs.append('*.nfo')

    t.private = True

    # animation = ["■□□□□□□□□□", "■■□□□□□□□□", "■■■□□□□□□□", "■■■■□□□□□□",
    #              "■■■■■□□□□□", "■■■■■■□□□□", "■■■■■■■□□□", "■■■■■■■■□□",
    #              "■■■■■■■■■□", "■■■■■■■■■■"]

    animation = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]

    for i in range(len(animation)):
        time.sleep(0.2)
        # sys.stdout.write("\r" + animation[i % len(animation)] + "\n")
        # sys.stdout.flush()
        stt = animation[i % len(animation)]
        logger_torrent.info('Creating torrent: %s', stt)
        t.generate()

    # define the name of the directory
    # get the folder name to make the torrent name
    torrent_folder = Path(folder_path).stem  # get only the file with extension

    # if the config file as no folder path to save the .torrent create one
    if torrent_file_path == '0':
        # Choose .torrent folder
        sg.theme('Dark Blue 3')  # please make your windows colorful
        layout = [[sg.Text('Here you can choose folder to save the .torrent file.')],
                  [sg.Text('Folder', size=(10, 1)), sg.InputText(), sg.FolderBrowse()],
                  [sg.Submit(), sg.Cancel()]]
        window = sg.Window(script_version_short, layout, icon=r"favicon.ico")

        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            sys.exit()
        window.close()

        # if the box text as nothing quit
        if values[0] == '':
            sg.popup_error('You did not enter anything, so exit is in order.')
            sys.exit()
        else:
            path_to_torrent = values[0]

            # update the config file
            config = configparser.ConfigParser()
            my_config = Path('config.ini')  # Path of your .ini file
            config.read(my_config)
            config.set('FOLDERS', 'torrent_folder', path_to_torrent)  # Updating existing entry
            # config.set('FOLDERS', 'day', 'sunday')  # Writing new entry
            config.write(my_config.open("w"))

    else:
        path_to_torrent = torrent_file_path

    file = path_to_torrent + '/' + torrent_folder + '.torrent'
    if os.path.exists(file):
        os.remove(file)
        logger_torrent.info('Deleting old .torrent file present.')

    else:
        pass

    t.write(path_to_torrent + '/' + torrent_folder + '.torrent')
    logger_torrent.info('The .torrent file is created.')
    newadded = torrent_folder


else:
    logger_torrent.info('Creating Torrent...please wait.')

    # make .torrent single file
    t = Torrent(path=file_path,
                trackers=['https://abtorrents.me:2910/announce'],
                comment='In using this torrent you are bound by the ABTorrents Confidentiality Agreement '
                        'By Law')
    t.private = True
    # animation = ["■□□□□□□□□□", "■■□□□□□□□□", "■■■□□□□□□□", "■■■■□□□□□□",
    #              "■■■■■□□□□□", "■■■■■■□□□□", "■■■■■■■□□□", "■■■■■■■■□□",
    #              "■■■■■■■■■□", "■■■■■■■■■■"]

    animation = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]

    for i in range(len(animation)):
        time.sleep(0.2)
        sys.stdout.write("\r" + animation[i % len(animation)] + "\n")
        sys.stdout.flush()
        t.generate()

    # get the file name to make the torrent name

    if torrent_file == '0':
        # Choose .torrent folder
        sg.theme('Dark Blue 3')  # please make your windows colorful
        layout = [[sg.Text('Here you can choose folder to save the .torrent file.')],
                  [sg.Text('Folder:', size=(10, 1)), sg.InputText(), sg.FolderBrowse()],
                  [sg.Submit(), sg.Cancel()]]
        window = sg.Window(script_version_short, layout, icon=r"favicon.ico")

        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            logger_torrent.warning('The script will now close...')
            time.sleep(3)
            sys.exit()
        window.close()

        if values[0] == '':
            sg.popup_error('You did not enter anything, so exit is in order.')
            sys.exit()
        else:
            path_to_torrent_file = values[0]
            logger_torrent.info('Path to torrent file: %s', path_to_torrent_file)

            # update the config file
            config = configparser.ConfigParser()
            my_config = Path('config.ini')  # Path of your .ini file
            config.read(my_config)
            config.set('FOLDERS', 'torrent_file', path_to_torrent_file)  # Updating existing entry
            # config.set('FOLDERS', 'day', 'sunday')  # Writing new entry
            config.write(my_config.open("w"))
            # torrent_file = Path(path_to_torrent_file).stem  # only the file name

    else:
        path_to_torrent_file = torrent_file
        logger_torrent.info('File path: %s', path_to_torrent_file)

    file_path2 = Path(file_path).stem  # only the file name
    t.write(path_to_torrent_file + '/' + file_path2 + '.torrent')
    logger_torrent.info('The file was created.')
    newadded = file_path2
# END Paths to file/folder-----------------------------------------------------

# para terminar o script
# raise SystemExit(0)


# Find NFO Nfo------------------------------------------------------------------
logger_nfo.info('Starting looking for NFO file(s)....')
nfofile = None


# nfo files Path
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                # nfo_filename = os.path.join(basename)
                nfofile = os.path.join(root, basename)  # Para full path
                yield nfofile


if file_path == '':
    for nfofile in find_files(folder_path, '*.nfo'):
        logger_nfo.info('Found NFO metadata source: %s', nfofile)
    for nfofile in find_files(folder_path, '*.txt'):
        logger_nfo.info('Found TXT metadata source: %s', nfofile)

    if nfofile is None:
        logger_nfo.warning('NFO file is not present...')
        nfofile = "No NFO present"
    else:
        # Book Title
        _title = ["Title:", "Title.."]
        logger_nfo.info('Searching Title book...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _title:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        nfo_album = line
                        # remove (Unabridged)
                        nfo_album = re.sub(r' \(unabridged\)', r'', nfo_album)
                        # remove everything before :
                        nfo_album = re.sub(r'^[^:]*:', r'', nfo_album).lstrip().title()
                        # splitting if title as series
                        nfo_album2 = nfo_album.split(' - ')
                        try:
                            nfo_album = nfo_album2[1]
                            nfo_series = nfo_album2[0]
                            logger_nfo.info('Found Book Title: %s', nfo_album.rstrip("\n"))
                        except:
                            logger_nfo.info('Found Book Title: %s', nfo_album.rstrip("\n"))

        if nfo_album == '':
            logger_nfo.warning('Book Title not found.')

        # Book Author
        _author = ["Author:", "Author.."]
        logger_nfo.info('Searching Author book...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _author:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        nfo_author = line

                        # remove everything before :
                        nfo_author2 = re.sub(r'^[^:]*:', r'', nfo_author).lstrip().title()
                        logger_nfo.info('Author Found: %s', nfo_author2.rstrip("\n"))
        if nfo_author == '':
            logger_nfo.warning('Author not found.')

        # Book Narrator
        _narrator = ["Read by:", "Narrator:", "Read by.."]
        logger_nfo.info('Searching Narrator...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _narrator:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        nfo_narr = line

                        # remove everything before :
                        nfo_narr = re.sub(r'^[^:]*:', r'', nfo_narr).lstrip().title()
                        logger_nfo.info('Narrator Found: %s', nfo_narr.rstrip("\n"))
                        # if two narrators
                        try:
                            nfo_split_narr = nfo_narr.split(", ")
                            nfo_split_narr1 = nfo_split_narr[0]
                            nfo_split_narr2 = nfo_split_narr[1]
                            nfo_split_narr3 = nfo_split_narr[2]
                            nfo_split_narr4 = nfo_split_narr[3]
                            print(nfo_split_narr[0])
                        except:
                            pass

        if nfo_narr == '':
            logger_nfo.warning('Narrator not found.')

        # Book Series
        _series = ["Series:", "Series Name:"]
        logger_nfo.info('Searching Series...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _series:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        if nfo_series == '':
                            nfo_series = line

                            # remove everything before :
                            nfo_series = re.sub(r'^[^:]*:', r'', nfo_series).lstrip().title()
                            logger_nfo.info('Series Found: %s', nfo_series.rstrip("\n"))
                        else:
                            pass

        if nfo_series == '':
            logger_nfo.warning('Series not found.')
        else:

            try:
                num_serie2 = nfo_series.split(' Book ')
                num_serie = num_serie2[1]
                logger_nfo.info('Series number found: %s', num_serie.rstrip("\n"))
            except:
                logger_nfo.warning('Series number not Found!')

            nfo_series = re.sub(r' Book 1', r'', nfo_series)
            nfo_series = re.sub(r' Book 2', r'', nfo_series)
            nfo_series = re.sub(r' Book 3', r'', nfo_series)
            nfo_series = re.sub(r' Book 4', r'', nfo_series)
            nfo_series = re.sub(r' Book 5', r'', nfo_series)
            nfo_series = re.sub(r' Book 6', r'', nfo_series)
            nfo_series = re.sub(r' Book 7', r'', nfo_series)
            nfo_series = re.sub(r' Book 8', r'', nfo_series)
            logger_nfo.info('Series Found: %s', nfo_series)

        if num_serie == '':
            # Book series number
            _number = ["Position in", "sfdsfdsfsd"]
            logger_nfo.info('Searching Series number...')
            with open(nfofile, "r+") as file1:
                fileline1 = file1.readlines()
                for x in _number:  # <--- Loop through the list to check
                    for line in fileline1:  # <--- Loop through each line
                        line = line.casefold()  # <--- Set line to lowercase
                        if x.casefold() in line:
                            logger_nfo.info('Line found with word: %s', x)
                            num_serie = line

                            # remove everything before :
                            num_serie = re.sub(r'^[^:]*:', r'', num_serie).lstrip().title()
                            logger_nfo.info('Series number Found: %s', num_serie.rstrip("\n"))
            if num_serie == '':
                logger_nfo.warning('Series number not found.')
        else:
            pass

        # Book Genre
        _genre = ["Genre:", "GENRE.."]
        logger_nfo.info('Searching Genre...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _genre:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        nfo_genre = line

                        # remove everything before :
                        nfo_genre = re.sub(r'^[^:]*:', r'', nfo_genre).lstrip().title()
                        logger_nfo.info('Genre Found: %s', nfo_genre.rstrip("\n"))
        if nfo_genre == '':
            logger_nfo.warning('Genre not found.')

        # Book Copyright
        _copy = ["Copyright:", "Copyright.."]
        logger_nfo.info('Searching Copyright...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _copy:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        nfo_copy = line

                        # remove everything before :
                        nfo_copy = re.sub(r'^[^:]*:', r'', nfo_copy).lstrip().title()
                        logger_nfo.info('Copyright Found: %s', nfo_copy.rstrip("\n"))
        if nfo_copy == '':
            logger_nfo.warning('Copyright not found.')

        # Book Duration
        _dura = ["Duration:", "Time:", 'TiME..', "Duration.."]
        logger_nfo.info('Searching Duration...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _dura:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        nfo_duration = line

                        # remove everything before :
                        nfo_duration = re.sub(r'^[^:]*:', r'', nfo_duration).lstrip().title()
                        logger_nfo.info('Duration Found: %s', nfo_duration.rstrip("\n"))
        if nfo_duration == '':
            logger_nfo.warning('Duration not found.')

        # Book Publisher
        _publisher = ["Publisher:", "PUBLiSHER.."]
        logger_nfo.info('Searching Publisher...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _publisher:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        nfo_publisher = line

                        # remove everything before :
                        nfo_publisher = re.sub(r'^[^:]*:', r'', nfo_publisher).lstrip().title()
                        logger_nfo.info('Publisher Found: %s', nfo_publisher.rstrip("\n"))
        if nfo_publisher == '':
            logger_nfo.warning('Publisher not found.')

        # Book unbridged
        _uno = ["Unabridged:", "Unabridged.."]
        logger_nfo.info('Searching Unbridged...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _uno:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        nfo_unabridged = line

                        # remove everything before :
                        nfo_unabridged = re.sub(r'^[^:]*:', r'', nfo_unabridged).lstrip().title()
                        logger_nfo.info('Unbridged Found: %s', nfo_unabridged.rstrip("\n"))
        if nfo_unabridged == '':
            logger_nfo.warning('Unbridged not found.')

        # Book Release
        _release = ["Release:", "STOREDATE..", "Release.."]
        logger_nfo.info('Searching Release...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _release:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        nfo_release = line
                        # remove everything before :
                        nfo_release = re.sub(r'^[^:]*:', r'', nfo_release).lstrip().title()
                        if not nfo_release:
                            pass
                        else:
                            logger_nfo.info('Release Found: %s', nfo_release.rstrip("\n"))
        if nfo_release == '':
            logger_nfo.warning('Release not found.')

        # Book size
        _size = ["Size:", "SiZE.."]
        logger_nfo.info('Searching Size...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _size:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        nfo_size = line

                        # remove everything before :
                        nfo_size = re.sub(r'^[^:]*:', r'', nfo_size).lstrip().title()
                        logger_nfo.info('Size Found: %s', nfo_size.rstrip("\n"))
        if nfo_size == '':
            logger_nfo.warning('Size not found.')

        # Book url
        _url = ["URL:", "URL.."]
        logger_nfo.info('Searching Url...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _url:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        nfo_url = line

                        # remove everything before :
                        nfo_url = re.sub(r'^[^:]*:', r'', nfo_url).lstrip().title()
                        logger_nfo.info('Url Found: %s', nfo_url.rstrip("\n"))
        if nfo_url == '':
            logger_nfo.warning('Url Not Found.')

        # Book notes
        _notes = ["Note(s):", "Note(s)..", "Note:"]
        logger_nfo.info('Searching Notes...')
        with open(nfofile, "r+") as file1:
            fileline1 = file1.readlines()
            for x in _notes:  # <--- Loop through the list to check
                for line in fileline1:  # <--- Loop through each line
                    line = line.casefold()  # <--- Set line to lowercase
                    if x.casefold() in line:
                        logger_nfo.info('Line found with word: %s', x)
                        nfo_notes = line

                        # remove everything before :
                        nfo_notes = re.sub(r'^[^:]*:', r'', nfo_notes).lstrip().title()
                        logger_nfo.info('Note Found: %s', nfo_notes.rstrip("\n"))
        if nfo_notes == '':
            logger_nfo.warning('Note Not Found.')

        # Description
        copy = False
        with open(nfofile, "r") as saveoutput:
            for line in saveoutput:
                if 'Description' in line:
                    copy = True
                # if line.startswith('-'):
                #     copy = False
                if copy:
                    items = (format(line.strip()) for line in saveoutput)
                    join = '\n'.join(items)
                    join = re.sub(r'Description:', r'', join)
                    join = re.sub(r' ==', r'', join)
                    nfo_desc = join
                    # logger_nfo.info('Description: %s', join)
                    logger_nfo.info('Description Found: %s', nfo_desc.rstrip("\n"))
                # else:
                # print('No description found.')

else:
    logger_nfo.info('Metadata will be made from audio file metadata.')
    pass
# END Find NFO------------------------------------------------------------------


# Find audio files--------------------------------------------------------------
logger_audio.info('Starting looking for audio file(s)....')

audio_filename = None


# audio files Path
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                # nfo_filename = os.path.join(basename)
                audio_filename = os.path.join(root, basename)  # Para full path
                yield audio_filename


if file_path == '':
    for audio_filename in find_files(folder_path, '*.mp3'):
        logger_audio.info('Found MP3 audio source: %s', audio_filename)
    for audio_filename in find_files(folder_path, '*.m4b'):
        logger_audio.info('Found M4B audio source: %s', audio_filename)
    for audio_filename in find_files(folder_path, '*.mp4'):
        logger_audio.info('Found MP4 audio source: %s', audio_filename)

else:
    audio_filename = file_path

if not audio_filename:
    logger_audio.error('Audio files not present...')
else:
    f = mutagen.File(audio_filename)
    # samplerate = f.info.sample_rate
    # print(samplerate)

    # if it is not MP3 move to MP4
    try:
        audio = ID3(audio_filename)  # path: path to file
        # Here is the info from de audio file MP3
        logger_audio.info('Audio files MP3 found....')

        # album/title
        try:
            nfo_album = audio['TALB'].text[0]
            # if it as a : in the album name
            logger_meta.info('Album title: %s', nfo_album)

            nfo_album = nfo_album.split(':')[0]
            if nfo_album == nfo_album:
                logger_meta.info('No (:) char found.')
            else:
                logger_meta.info('Removing Everything after (:) %s', nfo_album)
                logger_meta.info('Album title: %s', nfo_album)

            # Subtitle
            try:
                nfo_sub = nfo_album.split(':')[1]
                logger_meta.info('Album Subtitle: %s', nfo_sub)
            except:
                logger_meta.info('No Subtitle found.')

            # remove the initial numbers from album name
            nfo_album = re.sub('^[\d-]*\s*', '', nfo_album)
            logger_meta.info('Final album tag: %s', nfo_album)
        except:
            logger_meta.warning('Album title not found.')

        if nfo_sub == '':
            try:
                nfo_sub = audio['TIT3'].text[0]
                logger_meta.info('Album Subtitle: %s', nfo_sub)
            except:
                pass
        else:
            pass

        try:
            # Artist/author
            nfo_author = audio['TPE1'].text[0]
            # correct format of author(ex: A. B. Mark)
            nfo_author = re.sub(r'(?<=[A-Z])\.?\s?(?![a-z])', r'. ', nfo_author)
            logger_meta.info('Author: %s', nfo_author)
        except:
            logger_meta.warning('This Audiobook as No Author, probably no tags are present.')

        # Narrator/composer
        try:
            nfo_narr = audio['TCOM'].text[0]
            # correct format of narrator(ex: A. B. Mark)
            nfo_narr = re.sub(r'(?<=[A-Z])\.?\s?(?![a-z])', r'. ', nfo_narr)
            logger_meta.info('Narrator: %s', nfo_narr)
            try:
                nfo_split_narr = nfo_narr.split(", ")
                nfo_split_narr1 = nfo_split_narr[0]
                nfo_split_narr2 = nfo_split_narr[1]
                nfo_split_narr3 = nfo_split_narr[2]
                nfo_split_narr4 = nfo_split_narr[3]
                print(nfo_split_narr[0])

            except:
                pass
        except:
            logger_meta.info('Narrator not found.')

        # if author iqual to narrator get data from nfo.
        if nfo_author == nfo_narr:
            nfo_author = nfo_author2
        else:
            pass

        # Genre
        if nfo_genre == 'Audiobook' or nfo_genre == '':
            try:
                nfo_genre = audio['TCON'].text[0]
                logger_meta.info('Genre: %s', nfo_genre)
            except:
                pass
        else:
            logger_meta.info('No GENRE found.')

        # Year
        try:
            nfo_year = audio['TDRC'].text[0]
            logger_meta.info('Year: %s', nfo_year)
        except:
            logger_meta.info('No Year Found.')

        # Series
        try:
            nfo_series = audio['TXXX:SERIES'].text[0]
            logger_meta.info('Series: %s', nfo_series)
        except:
            logger_meta.info('No series found.')

        # Series number
        try:
            num_serie = audio['TXXX:series-part'].text[0]
            logger_meta.info('Series part: %s', num_serie)
        except:
            logger_meta.info('No series number found.')

        # Asin
        try:
            nfo_asin = audio['TXXX:Asin'].text[0]
            logger_meta.info('Asin: %s', nfo_asin)
        except:
            logger_meta.info('No Asin number found.')

        # Publisher
        try:
            nfo_publisher = audio['TPUB'].text[0]
            logger_meta.info('Publisher: %s', nfo_publisher)
        except:
            logger_meta.warning('Publisher not found.')

        # copyright
        try:
            nfo_copy = audio['TCOP'].text[0]
            logger_meta.info('Copyright: %s', nfo_copy)
        except:
            logger_meta.warning('copyright not found.')

        # Link
        try:
            nfo_link = audio['WOAF'].text[0]
            logger_meta.info('Link: %s', nfo_link)
        except:
            logger_meta.warning('Link not found.')

        # Description
        try:
            nfo_desc = audio['COMM::eng'].text[0]
            logger_meta.info('Description: %s', nfo_desc)
        except:
            logger_meta.warning('Description not found.')

        # File Type
        nfo_audio = f.mime[0]
        logger_meta.info('File type: %s', nfo_audio)

        # bitrate
        nfo_bitrate = int(f.info.bitrate / 1000)
        logger_meta.info('Bitrate: %s kbps', nfo_bitrate)

        # Encoder
        try:
            nfo_encoder = audio['TENC'].text[0]
            logger_meta.info('Encoder: %s', nfo_encoder)
        except:
            logger_meta.warning('Encoder not found.')

        nfo_full = f.info.pprint()
        logger_meta.info('Full audio stream information:: %s', nfo_full)

    except:
        # MP4
        mp4_audio = MP4(audio_filename)  # path: path to file
        # no tag in MB4

        # Here is the info from de audio file MP4(mb4)
        try:
            nfo_album = mp4_audio['\xa9alb']
            logger_meta2.info('Album: %s', nfo_album[0])
            nfo_album = nfo_album[0]

            # if it as a : in the album name
            try:
                nfo_album = nfo_album.split(':')[0]
                logger_meta2.info('(:) char found.')
            except:
                pass

            try:
                nfo_sub = nfo_album.split(':')[1]
                logger_meta2.info('Album Subtitle: %s', nfo_sub)
            except:
                logger_meta2.info('Album Subtitle not found.')

            # see if it has number at start
            num_serie2 = re.search('([0-9]+)', nfo_album)
            try:
                num_serie3 = num_serie2.group()
            except:
                num_serie3 = ''
            nfo_album = re.sub('^[\d-]*\s*', '', nfo_album)


        except:
            logger_meta2.warning('Book name not found.')

        if nfo_sub == '':
            try:
                nfo_sub = audio['TIT3'].text[0]
                logger_meta2.info('Book Subtitle: %s', nfo_sub)
            except:
                pass
        else:
            pass

        # Artist/author
        nfo_author = mp4_audio['\xa9ART']
        logger_meta2.info('Author: %s', nfo_author[0])
        nfo_author = nfo_author[0]
        # correct format of author(ex: A. B. Mark)
        nfo_author = re.sub(r'(?<=[A-Z])\.?\s?(?![a-z])', r'. ', nfo_author)

        # Narrator
        try:
            nfo_narr = mp4_audio['\xa9wrt']
            logger_meta2.info('Narrator: %s', nfo_narr[0])
            nfo_narr = nfo_narr[0]
            # correct format of narrator(ex: A. B. Mark)
            nfo_narr = re.sub(r'(?<=[A-Z])\.?\s?(?![a-z])', r'. ', nfo_narr)
            try:
                nfo_split_narr = nfo_narr.split(", ")
                nfo_split_narr1 = nfo_split_narr[0]
                nfo_split_narr2 = nfo_split_narr[1]
                nfo_split_narr3 = nfo_split_narr[2]
                nfo_split_narr4 = nfo_split_narr[3]
                print(nfo_split_narr[0])
            except:
                pass
        except:
            logger_meta2.warning('Narrator not found.')

        # if author iqual to narrator get data from nfo.
        if nfo_author == nfo_narr:
            nfo_author = nfo_author2
            logger_meta2.warning('Author the same as narrator, getting data from nfo file.')
        else:
            pass

        # Genre
        if nfo_genre == 'Audiobook' or nfo_genre == '':
            try:
                nfo_genre = mp4_audio['\xa9gen']
                logger_meta2.info('Genre: %s', nfo_genre[0])
                nfo_genre = nfo_genre[0]
            except:
                pass
        else:
            logger_meta2.warning('Genre not found.')

        # Year
        try:
            nfo_year = mp4_audio['\xa9day']
            logger_meta2.info('Year: %s', nfo_year[0])
            nfo_year = nfo_year[0]
        except:
            logger_meta2.warning('Year not found.')

        # Asin
        try:
            nfo_asin = mp4_audio['----:com.apple.iTunes:Asin']
            nfo_asin = nfo_asin[0].decode('utf8')
            logger_meta2.info('Asin: %s', nfo_asin)
        except:
            logger_meta2.warning('Asin not found.')

        # Publisher
        try:
            nfo_publisher = mp4_audio['----:com.apple.iTunes:Publisher']
            nfo_publisher = nfo_publisher[0].decode('utf8')
            logger_meta2.info('Publisher: %s', nfo_publisher)
        except:
            logger_meta2.warning('Publisher not found.')

        # Publisher2
        if nfo_publisher == '':
            try:
                nfo_publisher = mp4_audio['\xa9pub']
                nfo_publisher = nfo_publisher[0].decode('utf8')
                logger_meta2.info('Publisher(2): %s', nfo_publisher)
            except:
                logger_meta2.warning('Publisher(2) not found.')
        else:
            pass

        # Copyright
        try:
            nfo_copy = mp4_audio['cprt']
            nfo_copy = nfo_copy[0]
            logger_meta2.info('Copyright: %s', nfo_copy)
        except:
            logger_meta2.warning('Copyright not found.')

        # Series
        try:
            nfo_series = mp4_audio['----:com.apple.iTunes:SERIES']
            nfo_series = nfo_series[0].decode('utf8')
            logger_meta2.info('Series(1): %s', nfo_series)
        except:
            logger_meta2.warning('Series(1) not found.')

        if nfo_series == '':
            try:
                nfo_series = mp4_audio['\xa9grp']
                nfo_series = nfo_series[0]
                logger_meta2.info('Series(2) found: %s', nfo_series)
            except:
                logger_meta2.warning('Series(2) not found.')

        # If series iqual author move along
        if nfo_series == nfo_author:
            nfo_series = ''
            logger_meta2.warning('Series(2) found but is the same as author...removed.')
        else:
            pass

        try:
            num_serie = mp4_audio['----:com.apple.iTunes:series-part']
            num_serie = num_serie[0].decode('utf8')
            logger_meta2.info('Series number(1): %s', num_serie)
        except:
            logger_meta2.warning('Series number(1) not found.')

        if num_serie == '':
            num_serie = num_serie3
            logger_meta2.info('Series number(2): %s', num_serie)

        else:
            logger_meta2.warning('Series number(2) not found.')

        # Link
        try:
            nfo_link = mp4_audio['----:com.apple.iTunes:WWWAUDIOFILE']
            nfo_link = nfo_link[0].decode('utf8')
            logger_meta2.info('Link: %s', nfo_link)
        except:
            logger_meta2.warning('Link not found.')

        try:
            nfo_comm = mp4_audio['\xa9cmt']
            nfo_comm = nfo_comm[0]
            logger_meta2.info('Comment: %s', nfo_comm)
        except:
            logger_meta2.warning('Comment not found.')

        # File Type
        nfo_audio = f.mime[0]
        logger_meta2.info('File Type: %s', nfo_audio)

        # bitrate
        nfo_bitrate = int(f.info.bitrate / 1000)
        logger_meta2.info('Bitrate: %s', nfo_bitrate)

        # desc
        try:
            nfo_desc = mp4_audio['desc']
            logger_meta2.info('Description: %s', nfo_desc[0])
            nfo_desc = nfo_desc[0]
        except:
            logger_meta2.warning('Description not found.')

        nfo_full = f.info.pprint()
        logger_meta2.info('Full audio stream information: %s', nfo_full)
        time.sleep(3)

# End script
# raise SystemExit(0)

# Find image file ---------------------------------------------------------
logger_cover.info('Starting looking for Image Cover file(s)....')
image_filename = None


# audio files Path
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                # nfo_filename = os.path.join(basename)
                image_filename = os.path.join(root, basename)  # Para full path
                yield image_filename


for image_filename in find_files(folder_path, '*.jpeg'):
    logger_cover.info('Found Image JPEG: %s', image_filename)
for image_filename in find_files(folder_path, '*.jpg'):
    logger_cover.info('Found Image JPG: %s', image_filename)
for image_filename in find_files(folder_path, '*.png'):
    logger_cover.info('Found Image PNG: %s', image_filename)

if image_filename is None:
    logger_cover.warning('Cover Image is not present...it will be created.')
    afile = File(audio_filename)

    if audio_filename.endswith(('.mp3', '.MP3', '.Mp3')):
        # for mp3
        try:
            artwork = afile.tags['APIC:'].data
        except:
            artwork = ''
    else:
        # for mp4
        try:
            artwork = afile.tags['covr'][0]
        except:
            artwork = ''

    # if no single file torrent
    if file_path == "":
        path_to_image = folder_path
    else:
        path_to_image = os.path.dirname(file_path)

    if artwork == '':
        logger_cover.error('Cover Images not possible to create, not present or tag corrupt.')
        pass
    else:
        with open(path_to_image + '/' + newadded.replace('/', '-') + '.jpg', 'wb') as img:
            img.write(artwork)
            logger_cover.info('Image Created to folder: %s', path_to_image)
            time.sleep(3)

    for image_filename in find_files(folder_path, '*.jpg'):
        logger_cover.info('Image from created image:: %s', image_filename)
        time.sleep(3)
else:
    pass
# END Find image file ---------------------------------------------------------

# Login -----------------------------------------------------------------------
logger_internet.info('Opening firefox and login. Please wait...')
if login_session == '0':
    logger_internet.warning('Firefox session not present...write your url.')
    # Choose firefox session folder
    sg.theme('Dark Blue 3')  # please make your windows colorful
    layout = [[sg.Text('Here you can enter the firefox session.')],
              [sg.Text('Get it by writing the Url from about:profiles in the address bar.')],
              [sg.Text('Profile', size=(10, 1)), sg.InputText()],
              [sg.Submit(), sg.Cancel()]]
    window = sg.Window(script_version_short, layout,
                       icon=r"favicon.ico")

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        sys.exit()
    login_session = values[0]
    window.close()

    if login_session == '':
        sg.popup_error('You did not enter anything, so exit is in order.')
        sys.exit()
    else:
        fp = webdriver.FirefoxProfile(login_session)
        # update the config file
        config = configparser.ConfigParser()
        my_config = Path('config.ini')  # Path of your .ini file
        config.read(my_config)
        config.set('LOGIN', 'firefox_profile', login_session)  # Updating existing entry
        # config.set('FOLDERS', 'day', 'sunday')  # Writing new entry
        config.write(my_config.open("w"))


else:
    fp = webdriver.FirefoxProfile(login_session)

driver = webdriver.Firefox(fp, service_log_path=os.devnull)  # Webdriver no log
driver.get("https://www.abtorrents.me/upload_audiobook.php")

# primeiro fazemos login no site
# usernameStr = 'romano'
# passwordStr = 'xxxxxxxxxx'
#
# username = driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div/form/table/tbody/tr[1]/td[2]/input')
# username.send_keys(usernameStr)
#
# password = driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div/form/table/tbody/tr[2]/td[2]/input')
# password.send_keys(passwordStr)
#
# # carregar no X para entrar
# nextButton = driver.find_element_by_xpath("//input[@name='submitme' and @value='X']")
# nextButton.click()
# # exemplo para opcoes a escolher
# # driver.find_element_by_xpath("//select[@name='element_name']/option[text()='option_text']").click()

# END Login -----------------------------------------------------------------------


# Author internet--------------------------------------------------------------------------
# Change to author
button_author = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/div[1]/ul/li[1]/a")
button_author.click()
logger_internet.info('Adding the Author to the database...')
time.sleep(4)

# Writing author
author_name = driver.find_element_by_name('add_author')
author_name.send_keys(nfo_author)
time.sleep(4)

# Pressing X to load
author_button = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/form/h3[4]/input[2]")
author_button.click()
time.sleep(4)

# Narrator internet--------------------------------------------------------------------------

if nfo_split_narr:
    # Change to narrator Link
    narrator_button = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/div/ul/li[4]/a")
    narrator_button.click()
    logger_internet.info('Adding the Narrator to the database...')
    time.sleep(4)

    # Writing Narrator
    narrator_name = driver.find_element_by_name('add_narrator')
    narrator_name.send_keys(nfo_split_narr1)
    time.sleep(3)

    # Pressing X to load
    nextButton3 = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/form/h3[4]/input[2]")
    nextButton3.click()
    time.sleep(4)

    # Writing Narrator
    narrator_name = driver.find_element_by_name('add_narrator')
    narrator_name.send_keys(nfo_split_narr2)
    time.sleep(3)

    # Pressing X to load
    nextButton3 = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/form/h3[4]/input[2]")
    nextButton3.click()
    time.sleep(4)
else:

    # Change to narrator Link
    narrator_button = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/div/ul/li[4]/a")
    narrator_button.click()
    logger_internet.info('Adding the Narrator to the database...')
    time.sleep(4)

    # Writing Narrator
    narrator_name = driver.find_element_by_name('add_narrator')
    narrator_name.send_keys(nfo_narr)
    time.sleep(3)

    # Pressing X to load
    nextButton3 = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/form/h3[4]/input[2]")
    nextButton3.click()
    time.sleep(4)
# END Narrator internet--------------------------------------------------------------------------

# Change to Upload Page--------------------------------------------------------
upload_Button = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/div/ul/li[1]/a")
upload_Button.click()
logger_internet.info('Changing to the upload web page...')
# END Change to Upload Page----------------------------------------------------

# Torrent file --------------------------------------------------------------
# Change Torrent Name
time.sleep(3)
logger_internet.info('Changing the name of .torrent file to title name.')
t_path = path_to_torrent + '/' + newadded + '.torrent'
b_path = path_to_torrent + '/' + nfo_album + '.torrent'
try:
    os.rename(t_path, b_path)
except:
    logger_internet.warning('Impossible to rename, file already present.')
    window.read(timeout=3000)
# END Change Torrent Name


# Select torrent file --------------------------------------------------------
logger_internet.info('Uploading .torrent file...')
file_upload = WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.ID, "torrent"))
)
file_upload.send_keys(os.path.abspath(b_path))

# END Torrent file -----------------------------------------------------------


# Cover image upload----------------------------------------------------------
time.sleep(3)
if not image_filename:
    logger_internet.warning('Image cover not found...')
    image_filename = None
else:
    logger_internet.info('Uploading image cover...')
    image_filename = image_filename.replace('/', '\\')  # substituir o \ por /
    driver.find_element_by_id("droppable").click()  # This opens the windows file selector
    time.sleep(4)
    pyautogui.write(image_filename)
    time.sleep(4)
    pyautogui.press('enter')
    time.sleep(6)
# END cover image upload-------------------------------------------------------


# Write serie name-----------------------------------------------------------
logger_internet.info('Writing Series name...')
AB_title = driver.find_element_by_name('series')
nfo_series = nfo_series.replace("Series", "")
AB_title.send_keys(nfo_series)
# END Write serie name-------------------------------------------------------

# Write Series number---------------------------------------------------------
logger_internet.info('Writing Series number...')
time.sleep(2)
driver.find_element_by_name('booknumber').clear()
time.sleep(1)
ab_num_serie = driver.find_element_by_name('booknumber')

if num_serie == '':
    logger_internet.warning('Series number not found...')
    ab_num_serie.send_keys('')
else:
    num_serie = num_serie.replace("Book ", "")
    if num_serie == '':
        num_serie = 0
    else:
        pass
    ab_num_serie.send_keys(num_serie)
time.sleep(2)
# END Write Series number---------------------------------------------------------


# Write Author---------------------------------------------------------
logger_internet.info('Writing Author...')
pyautogui.press('tab', presses=1)
# driver.find_element_by_name("author[]").click()  # This opens the windows file selector
pyautogui.write(nfo_author)
time.sleep(4)
pyautogui.press('enter')
# END Write author---------------------------------------------------------

# narrator
logger_internet.info('Writing Narrator(s)...')
pyautogui.press('tab')
# #driver.find_element_by_name("narrator[]").click()  # This opens the windows file selector
if nfo_split_narr:
    pyautogui.write(nfo_split_narr1)
    time.sleep(4)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.write(nfo_split_narr2)
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(2)
    try:
        pyautogui.write(nfo_split_narr3)
        time.sleep(2)
        pyautogui.press('enter')
    except:
        pass
else:
    pyautogui.write(nfo_narr)
    time.sleep(4)
    pyautogui.press('enter')

# --------------------------------------------------------------------------

# audiotype
logger_internet.info('Writing audio type...')
time.sleep(2)
nfo_audio = nfo_audio.replace('audio/', '').upper()
if nfo_audio == 'MP4':
    nfo_audio = 'M4B'

if not nfo_audio:
    nfo_audio = "MP3"
    logger_internet.info('File type was replace by the default: %s', nfo_audio)

driver.find_element_by_xpath("//select[@name='audiotype']/option[text()='" + nfo_audio + "']").click()

# <option value=''>(choose one)
# <option value='MP3' >MP3
# <option value='M4B' >M4B
# <option value='M4A' >M4A
# <option value='WAV' >WAVE
# <option value='FLAC' >FLAC
# <option value='OGG' >OGG
# <option value='AAC' >AAC
# <option value='WMA' >WMA

# --------------------------------------------------------------------------
# bitrate
logger_internet.info('Writing bitrate...')
time.sleep(2)
# add kbps to output
kbps = 'kbps'
# range 20 to 34kbps
range34 = range(20, 35)
range48 = range(44, 49)
range96 = range(80, 97)
range62 = range(62, 63)
range64 = range(64, 65)
range192 = range(185, 193)
range128 = range(119, 129)
range125588 = '125588'

if nfo_bitrate == range128:
    nfo_bitrate = '128'
if nfo_bitrate == range34:
    nfo_bitrate = '32'
if nfo_bitrate == range48:
    nfo_bitrate = '48'
if nfo_bitrate == range96:
    nfo_bitrate = '96'
if nfo_bitrate == range64:
    nfo_bitrate = '64'
if nfo_bitrate == range192:
    nfo_bitrate = '192'
if nfo_bitrate == range62:
    nfo_bitrate = '62'
if nfo_bitrate == range125588:
    nfo_bitrate = '128'

nfo_bitrate = str(nfo_bitrate) + kbps

matches = (
    '16kbps', '32kbps', '48kbps', '56kbps', '62kbps', '64kbps', '96kbps', '128kbps', '192kbps', '256kbps',
    '320kbps',
    'VBR',
    'Unknown')
if nfo_bitrate in matches:
    driver.find_element_by_xpath("//select[@name='bitrate']/option[text()='" + nfo_bitrate + "']").click()
else:
    nfo_bitrate = 'Unknown'
    driver.find_element_by_xpath("//select[@name='bitrate']/option[text()='" + nfo_bitrate + "']").click()
time.sleep(2)
# --------------------------------------------------------------------------
# Description box
logger_internet.info('Writing to description box...')

# create a file to write the metadata
meta = codecs.open('metadata_' + nfo_album + '.txt', 'w', 'utf-8-sig')

meta.write('[center]')
meta.write(
    '[color=#FF9933]\U00002B50...::**::... [/color][font=Comic Sans MS][size=5][color=#CCFF00]' + nfo_album + '[/color][/size][/font][color=#FF9933] ...::**::...\U00002B50[/color]' + '\n')

if nfo_sub == '':
    pass
else:
    meta.write('[color=#CCFF00]' + nfo_sub + '[/color]' + '\n' + '\n')

meta.write('Author: ' + nfo_author + '\n')

if nfo_split_narr:
    meta.write('Narrator: ' + nfo_split_narr1 + '\n')
    meta.write('Narrator: ' + nfo_split_narr2 + '\n')
else:
    meta.write('Narrator: ' + nfo_narr + '\n')

meta.write('Genre: ' + nfo_genre + '\n')
meta.write('Year: ' + str(nfo_year) + '\n')

if nfo_duration == '':
    pass
else:
    meta.write('Duration: ' + nfo_duration + '\n')

if nfo_asin == '':
    pass
else:
    meta.write('Asin: ' + nfo_asin + '\n')

if nfo_publisher == '':
    pass
else:
    meta.write('Publisher: ' + nfo_publisher)

if nfo_copy == '':
    pass
else:
    meta.write('Copyright: ' + nfo_copy)

if nfo_unabridged == '':
    pass
else:
    meta.write('Unabridged: ' + nfo_unabridged)

if nfo_release == '':
    pass
else:
    meta.write('Release: ' + nfo_release)

if nfo_size == '':
    pass
else:
    meta.write('Size: ' + nfo_size)

if nfo_notes == '':
    pass
else:
    meta.write('Notes(s): ' + nfo_notes)

if nfo_comm == '':
    pass
else:
    if nfo_comm == nfo_desc:
        pass
    else:
        meta.write('Comment: ' + nfo_comm + '\n')

if nfo_link == '':
    pass
else:
    meta.write('Link: ' + nfo_link + '\n' + '\n')

if nfo_url == '':
    pass
else:
    meta.write('Url: ' + nfo_url + '\n' + '\n')

meta.write(
    '\n' + '[color=#FF9933]\U00002B50...::**::... [/color][color=#faa702][size=5][b]Book Description[/b][/size][/color][color=#FF9933]...::**::...\U00002B50[/color]' + '\n' + '\n')
meta.write(str(nfo_desc) + '\n' + '\n')

if nfo_series == '':
    pass
else:
    meta.write('Series: ' + nfo_series + '\n')
    meta.write('Series N.: ' + num_serie + '\n')
meta.write('----------------------------' + '\n')

nfo_encoder = re.sub(r'\([^)]*\)', '', nfo_encoder)
if nfo_encoder == '':
    pass
else:
    meta.write('Encoder: ' + nfo_encoder + '\n')

meta.write('File Type: ' + nfo_audio + '\n')
meta.write('Bitrate: ' + nfo_bitrate + '\n')
meta.write('Technical: ' + nfo_full + '\n')
meta.write('[size=1]' + script_version + '[/size]')
meta.write('[/center]')
meta.close()

# Write all data from file to description box
file = 'metadata_' + nfo_album + '.txt'
with open(file, 'r', encoding='utf-8-sig') as f:
    data = f.readlines()

elem = driver.find_element_by_xpath(
    "/html/body/div/div[1]/table/tbody/tr/td/div[2]/form/table/tbody/tr[12]/td[2]/div/div/textarea")
elem.send_keys(data, '\n')
time.sleep(3)

# Genre --------------------------------------------------------------------
logger_internet.info('Writing Genre...')
list_romance = ['Romance']
if re.compile('|'.join(list_romance), re.IGNORECASE).search(
        nfo_genre):  # re.IGNORECASE is used to ignore case
    nfo_genre = 'Romance'

list_horror = ['Horror', 'Zombie', 'Apocalypse', 'Post-Apocalyptic']
if re.compile('|'.join(list_horror), re.IGNORECASE).search(
        nfo_genre):  # re.IGNORECASE is used to ignore case
    nfo_genre = 'Horror'

list_crime = ['Genre Fiction', 'Crime', 'Thriller', 'Mystery', 'Audiobook']
if re.compile('|'.join(list_crime), re.IGNORECASE).search(
        nfo_genre):  # re.IGNORECASE is used to ignore case
    nfo_genre = 'Crime/Thriller/Mystery'

list_action = ['Action', 'Adventure']
if re.compile('|'.join(list_action), re.IGNORECASE).search(
        nfo_genre):  # re.IGNORECASE is used to ignore case
    nfo_genre = 'Action/Adventure'

list_action = ['Science Fiction', 'Sci-fi']
if re.compile('|'.join(list_action), re.IGNORECASE).search(
        nfo_genre):  # re.IGNORECASE is used to ignore case
    nfo_genre = 'Science Fiction'

list_fantasy = ['Fantasy']
if re.compile('|'.join(list_fantasy), re.IGNORECASE).search(
        nfo_genre):  # re.IGNORECASE is used to ignore case
    nfo_genre = 'Fantasy'

list_western = ['Western']
if re.compile('|'.join(list_western), re.IGNORECASE).search(
        nfo_genre):  # re.IGNORECASE is used to ignore case
    nfo_genre = 'Western'

matches_genre = (
    'Action/Adventure',
    'Adult/Erotica',
    'Biography/Memoirs',
    'Business',
    'Childrens',
    'Comics',
    'Computers',
    'Crime/Thriller/Mystery',
    'Fantasy-General',
    'Fantasy-Youth',
    'Files',
    'Foreign Language',
    'General Fiction',
    'Historical Fiction',
    'History',
    'Horror',
    'Humor (Comedy)',
    'Literature',
    'Mystery',
    'Non-Fiction',
    'Radio Drama',
    'Romance',
    'Sci-Fi Apocalypse',
    'Science',
    'Science Fiction',
    'Self Improvement',
    'Suspense',
    'Talk Radio',
    'Urban Fantasy',
    'Western')

if nfo_genre in matches_genre:
    driver.find_element_by_xpath("//select[@name='type']/option[text()='" + nfo_genre + "']").click()
else:
    nfo_genre = 'Horror'
    driver.find_element_by_xpath("//select[@name='type']/option[text()='" + nfo_genre + "']").click()

# Delete the metadata txt file ---------------------------------------------
time.sleep(2)
logger_internet.info('The .txt file was deleted...')
if os.path.exists(file):
    os.remove(file)
else:
    logger_internet.info('The metadata txt file does not exist...')

# Move files ---------------------------------------------------------------
# # Passar o folder do torrent para o o disco dos torrents para semear bem
# print('INFO: Moving the files/folder to the torrent folder to seed T:')
# time.sleep(4)
#
# def move_all_files_in_dir(srcdir, dstdir):
#     # Check if both the are directories
#     if os.path.isdir(srcdir) and os.path.isdir(dstdir):
#         # Iterate over all the files in source directory
#         for filePath in glob.glob(srcdir + '\*'):
#             # Move each file to destination Directory
#             shutil.move(filePath, dstdir)
#     else:
#         print("srcDir & dstDir should be Directories")
#
# time.sleep(4)
# if not folder_path:
#     move_all_files_in_dir(file_path, 'T:')
#     print("File Moved to T:")
# else:
#     move_all_files_in_dir(folder_path, 'T:')
#     print("Folder Moved to T:")
#
#
logging.info('End of script, please check values before pressing the button to upload.')
logging.info('Thank you for using %s', script_version)

# window.read(timeout=10000)
# Console close
input("Press press a word/number and Enter to Quit...")
