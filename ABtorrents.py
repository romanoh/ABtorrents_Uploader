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

script_version = 'Beta v.0.2.7 - ABtorrents uploader Helper'
script_version_short = 'Beta v.0.2.7'

# set up logging to file
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


# If error pauses script
def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)


sys.excepthook = show_exception_and_exit
# END If error pauses script

# ------------------------------------------------------------
# Log Version
logging.info('Script Version: %s', script_version)

# ------------------------------------------------------------

# Config
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

    logger_config.info('Ini Config file created.')

    config.write(open('config.ini', 'w'))

    torrent_file_path = config['FOLDERS']['torrent_folder']  # to make folders
    torrent_file = config['FOLDERS']['torrent_file']  # make files
    login_session = config['LOGIN']['firefox_profile']  # profile firefox link
else:
    logger_config.info('The config.ini is present.')

    config.read(r'config.ini')

    torrent_file_path = config['FOLDERS']['torrent_folder']
    torrent_file = config['FOLDERS']['torrent_file']
    login_session = config['LOGIN']['firefox_profile']
# ----------------------------------------------------------------------------
# Paths
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
    logger_path.info('Folder path was set: %s', folder_path)

    # values[1] is the variable for the file path
    file_path = values[1]  # get the data from the values dictionary
    logger_path.info('File path: %s', file_path)

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
        sys.stdout.write("\r" + animation[i % len(animation)] + "\n")
        sys.stdout.flush()
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

# para terminar o script
# raise SystemExit(0)
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# find Nfo
logger_nfo.info('Starting looking for NFO file(s)....')


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
        logger_nfo.info('Found NFO audio source: %s', nfofile)

    if nfofile is None:
        logger_nfo.warning('NFO file not present...')
        nfofile = "No NFO present"
    else:
        pass

else:
    logger_nfo.info('Metadata will be made from audio file metadata.')
    pass

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# Find audio files

print("INFO: Starting looking for audio file(s)....")
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
        print('INFO: Found MP3 audio source:', audio_filename)
    for audio_filename in find_files(folder_path, '*.m4b'):
        print('INFO: Found M4B audio source:', audio_filename)
else:
    audio_filename = file_path

if not audio_filename:
    print('ERROR: Audio files not present...')
else:
    musicfile = audio_filename  # path to audio files
    f = mutagen.File(musicfile)
    samplerate = f.info.sample_rate
    print(samplerate)

    # if it is not MP3 move to MP4
    try:
        audio = ID3(musicfile)  # path: path to file
        # Here is the info from de audio file MP3
        print('INFO MP3: MP3 found.')

        # album/title
        try:
            nfo_album = audio['TALB'].text[0]

            # if it as a : in the album name
            try:
                nfo_album = nfo_album.split(':')[0]
            except:
                pass

            try:
                nfo_sub = nfo_album.split(':')[1]
                print('INFO MP3: Album Subtitle:', nfo_sub)
            except:
                nfo_sub = ''

            # remove the initial numbers from album name
            nfo_album = re.sub('^[\d-]*\s*', '', nfo_album)
            print('INFO MP3: Album:', nfo_album)
        except:
            print('INFO MP3: No Album found')
            nfo_album = ''

        if nfo_sub == '':
            try:
                nfo_sub = audio['TIT3'].text[0]
                print('INFO MP3: Album Subtitle:', nfo_sub)
            except:
                pass
        else:
            pass

        try:
            # Artist/author
            nfo_author = audio['TPE1'].text[0]
            print('INFO MP3: Author:', nfo_author)
            # correct format of author(ex: A. B. Mark)
            nfo_author = re.sub(r'(?<=[A-Z])\.?\s?(?![a-z])', r'. ', nfo_author)

        except:
            print('INFO MP3: This Audiobook as No Author, probably no tags are present.')
            print('ERROR MP3: No need for this script. Quiting.')
            time.sleep(4)
            sys.exit()

        # Narrator/composer
        try:
            nfo_narr = audio['TCOM'].text[0]
            print('INFO MP3: Narrator:', nfo_narr)
            # correct format of narrator(ex: A. B. Mark)
            nfo_narr = re.sub(r'(?<=[A-Z])\.?\s?(?![a-z])', r'. ', nfo_narr)
        except:
            print('INFO MP3: This Audiobook as No Narrator')
            nfo_narr = ' '

        # Genre
        try:
            nfo_genre = audio['TCON'].text[0]
            print('INFO MP3: Genre:', nfo_genre)
        except:
            print('ERROR MP3: No GENRE found')
            nfo_genre = ' '

        # Year
        try:
            nfo_year = audio['TDRC'].text[0]
            print('INFO MP3: Year:', nfo_year)
        except:
            print('ERROR: No Year Found found')
            nfo_year = ' '

        # Series
        try:
            nfo_series = audio['TXXX:SERIES'].text[0]
            print('INFO MP3: Series:', nfo_series)
        except:
            print('INFO MP3: This Audiobook as No series')
            nfo_series = ''

        # Series number
        try:
            num_serie = audio['TXXX:series-part'].text[0]
            print('INFO MP3: Series part:', num_serie)
        except:
            print('ERROR MP3: No series number found')
            num_serie = ''

        # Asin
        try:
            nfo_asin = audio['TXXX:Asin'].text[0]
            print('INFO MP3: Asin:', nfo_asin)
        except:
            print('ERROR MP3: No Asin found')
            nfo_asin = ''

        # Copyright
        try:
            nfo_copy = audio['TPUB'].text[0]
            print('INFO MP3: Copyright:', nfo_copy)
        except:
            nfo_copy = ''

        try:
            nfo_link = audio['TXXX:WOAS'].text[0]
            print('INFO MP3: Link:', nfo_link)
        except:
            print('ERROR MP3: No Link found')
            nfo_link = ''

        # Description
        try:
            nfo_desc = audio['COMM::eng'].text[0]
            print('INFO MP3: Description:', nfo_desc)
        except:
            print('ERROR MP3: No Description found')
            nfo_desc = ''

        # File Type
        nfo_audio = f.mime[0]
        print('INFO MP3: File type:', nfo_audio)

        # bitrate
        nfo_bitrate = int(f.info.bitrate / 1000)
        print('INFO MP3: Bitrate:', nfo_bitrate, 'kbps')

        # Encoder
        try:
            nfo_encoder = audio['TSSE'].text[0]
            print('INFO MP3: Encoder:', nfo_encoder)
        except:
            print('ERROR: No Encoder found')
            nfo_encoder = ''

        nfo_full = f.info.pprint()
        print('INFO MP3: Full audio stream information:', nfo_full)


    except:
        # MP4
        mp4_audio = MP4(musicfile)  # path: path to file
        # no tag in MB4
        nfo_encoder = ''

        # Here is the info from de audio file MP4(mb4)
        try:
            nfo_album = mp4_audio['\xa9alb']
            print('INFO MB4: Album:', nfo_album[0])
            nfo_album = nfo_album[0]

            # if it as a : in the album name
            try:
                nfo_album = nfo_album.split(':')[0]
            except:
                pass

            try:
                nfo_sub = nfo_album.split(':')[1]
                print('INFO MB4: Album Subtitle:', nfo_sub)
            except:
                nfo_sub = ''

            # see if it has number at start
            num_serie2 = re.search('([0-9]+)', nfo_album)
            try:
                num_serie3 = num_serie2.group()
            except:
                num_serie3 = ''
            nfo_album = re.sub('^[\d-]*\s*', '', nfo_album)


        except:
            print('INFO MB4: No album found.')
            nfo_album = ''

        if nfo_sub == '':
            try:
                nfo_sub = audio['TIT3'].text[0]
                print('INFO MB4: Album Subtitle:', nfo_sub)
            except:
                pass
        else:
            pass

        # Artist/author
        nfo_author = mp4_audio['\xa9ART']
        print('INFO MB4: Author:', nfo_author[0])
        nfo_author = nfo_author[0]
        # correct format of author(ex: A. B. Mark)
        nfo_author = re.sub(r'(?<=[A-Z])\.?\s?(?![a-z])', r'. ', nfo_author)

        # Narrator
        try:
            nfo_narr = mp4_audio['\xa9wrt']
            print('INFO MB4: Narrator:', nfo_narr[0])
            nfo_narr = nfo_narr[0]
            # correct format of narrator(ex: A. B. Mark)
            nfo_narr = re.sub(r'(?<=[A-Z])\.?\s?(?![a-z])', r'. ', nfo_narr)
        except:
            print('INFO MB4: No Narrator found.')
            nfo_narr = ''

        # Genre
        try:
            nfo_genre = mp4_audio['\xa9gen']
            print('INFO MB4: Genre:', nfo_genre[0])
            nfo_genre = nfo_genre[0]
        except:
            print('INFO MB4: No Genre found.')
            nfo_genre = ''

        # Year
        try:
            nfo_year = mp4_audio['\xa9day']
            print('INFO MB4: Year:', nfo_year[0])
            nfo_year = nfo_year[0]
        except:
            print('INFO MB4: No Year found.')
            nfo_year = ''

        # Asin
        try:
            nfo_asin = mp4_audio['----:com.apple.iTunes:ASIN']
            print('INFO MB4: Asin:', nfo_asin[0].decode('utf8'))
            nfo_asin = nfo_asin[0].decode('utf8')
        except:
            print('INFO MB4: No Asin.')
            nfo_asin = ''

        # Copyright
        try:
            nfo_copy = mp4_audio['\xa9pub']
            print('INFO MB4: Copyright:', nfo_copy[0])
            nfo_copy = nfo_copy[0]
        except:
            print('INFO MB4: No Copyright.')
            nfo_copy = ''

        # Series
        try:
            nfo_series = mp4_audio['----:com.apple.iTunes:SERIES']
            print('INFO MB4: Series(1):', nfo_series[0].decode('utf8'))
            nfo_series = nfo_series[0].decode('utf8')
        except:
            print('INFO MB4: No Series(1) found...')
            nfo_series = ''

        if not nfo_series:
            try:
                nfo_series = mp4_audio['\xa9grp']
                nfo_series = nfo_series[0]
                print('INFO MB4: Series(2) found:', nfo_series[0])
            except:
                print('INFO MB4: No Series(2) found...')
                nfo_series = ''

        # se a serie for igual ao autor move along
        if nfo_series == nfo_author:
            nfo_series = ''
            print('INFO MB4: Series(2) found but is the same as author...removed')
        else:
            pass

        try:
            num_serie = mp4_audio['----:com.apple.iTunes:series-part']
            print('INFO MB4: Series number:', num_serie[0].decode('utf8'))
            num_serie = num_serie[0].decode('utf8')
        except:
            num_serie = ''
            print('INFO MB4: Series number(1) not found.')

        if not num_serie:
            num_serie = num_serie3
            print('INFO MB4: Series number(2) found:', num_serie)
        else:
            num_serie = ''
            print('INFO MB4: Series number(2) not found.')

        # Link
        try:
            nfo_link = mp4_audio['----:com.apple.iTunes:WWWAUDIOFILE']
            print('INFO MB4: Link:', nfo_link[0].decode('utf8'))
            nfo_link = nfo_link[0].decode('utf8')
        except:
            print('INFO MB4: No Link.')
            nfo_link = ''

        # File Type
        nfo_audio = f.mime[0]
        print('INFO MB4: File Type:', nfo_audio)

        # bitrate
        nfo_bitrate = int(f.info.bitrate / 1000)
        print('INFO MB4: bitrate:', nfo_bitrate)

        # desc
        try:
            nfo_desc = mp4_audio['desc']
            print('INFO MB4: Description:', nfo_desc[0])
            nfo_desc = nfo_desc[0]
        except:
            print('INFO MB4: No Description.')
            nfo_desc = ''

        nfo_full = f.info.pprint()
        print('INFO MB4: Full audio stream information:', nfo_full)
        time.sleep(3)

# para terminar o script
# raise SystemExit(0)
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# find image file

print("INFO.IMG: Starting looking for Cover file(s)....")
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
    print('INFO img: Found Image named JPEG:', image_filename)
for image_filename in find_files(folder_path, '*.jpg'):
    print('INFO img: Found Image named JPG:', image_filename)
for image_filename in find_files(folder_path, '*.png'):
    print('INFO img: Found Image named PNG:', image_filename)

if image_filename is None:
    print('ERROR.IMG: Cover Images are not present...it will be created.')
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
        print('ERROR.IMG: Cover Images not possible to create, not present or tag corrupt.')
        pass
    else:
        with open(path_to_image + '/' + newadded.replace('/', '-') + '.jpg', 'wb') as img:
            img.write(artwork)
            print('INFO-img.created: Image Created to folder named:', path_to_image)
            time.sleep(3)

    for image_filename in find_files(folder_path, '*.jpg'):
        print('INFO-IMG: Image found from created image:', image_filename)
        time.sleep(3)
else:
    pass

# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# Login
print('INFO-Internet: Opening firefox and login. Please wait...')
if login_session == '0':
    print('INFO LOGIN: no Firefox session present...')
    # Choose firefox session folder
    sg.theme('Dark Blue 3')  # please make your windows colorful
    layout = [[sg.Text('Here you can enter the firefox session.')],
              [sg.Text('Get it by writing about:profiles in the address bar.')],
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

# --------------------------------------------------------------------------

# mudar para autor
button_author = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/div[1]/ul/li[1]/a")
button_author.click()
print('INFO: Writing the Author...')
time.sleep(4)

# para meter autor
author_name = driver.find_element_by_name('add_author')
author_name.send_keys(nfo_author)
time.sleep(4)

# carregar no X para carregar
author_button = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/form/h3[4]/input[2]")
author_button.click()
time.sleep(4)
# --------------------------------------------------------------------------
# para meter narrator

# passar para narrator
narrator_button = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/div/ul/li[4]/a")
narrator_button.click()
print('INFO: Writing the Narrator...')
time.sleep(4)

narrator_name = driver.find_element_by_name('add_narrator')
narrator_name.send_keys(nfo_narr)
time.sleep(3)

# carregar no X para carregar
nextButton3 = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/form/h3[4]/input[2]")
nextButton3.click()
time.sleep(4)
# --------------------------------------------------------------------------
upload_Button = driver.find_element_by_xpath("/html/body/div/div[1]/table/tbody/tr/td/div/ul/li[1]/a")
upload_Button.click()
print('INFO: Changing to the upload page...')

# --------------------------------------------------------------------------
time.sleep(3)
print('INFO-Torrent: Changing the name of torrent.')

t_path = path_to_torrent + '/' + newadded + '.torrent'
b_path = path_to_torrent + '/' + nfo_album + '.torrent'
try:
    os.rename(t_path, b_path)
except:
    print('ERROR RENAME: Impossible to rename file aready present.')
    window.read(timeout=3000)
# --------------------------------------------------------------------------

# selecionar o torrent file
file_upload = WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.ID, "torrent"))
)
file_upload.send_keys(os.path.abspath(b_path))

# --------------------------------------------------------------------------

# introduzir o titulo do audiobook na pagina dos uploads
# AB_title = driver.find_element_by_xpath('//*[@id="name"]')
# AB_title.send_keys(nfo_album)

# --------------------------------------------------------------------------

# Subir a imagem
time.sleep(3)
if not image_filename:
    print('ERROR: No IMAGE found')
    image_filename = None
else:
    image_filename = image_filename.replace('/', '\\')  # substituir o \ por /
    driver.find_element_by_id("droppable").click()  # This opens the windows file selector
    time.sleep(4)
    pyautogui.write(image_filename)
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(8)
# --------------------------------------------------------------------------

# introduzir o nome da serie do audiobook na pagina dos uploads
AB_title = driver.find_element_by_name('series')
nfo_series = nfo_series.replace("Series", "")
AB_title.send_keys(nfo_series)

# --------------------------------------------------------------------------

# series number
time.sleep(2)
driver.find_element_by_name('booknumber').clear()
time.sleep(1)
ab_num_serie = driver.find_element_by_name('booknumber')

if num_serie == '':
    print('INFO: No Series Number...')
    ab_num_serie.send_keys('')
else:
    num_serie = num_serie.replace("Book ", "")
    if num_serie == '':
        num_serie = 0
    else:
        pass
    ab_num_serie.send_keys(num_serie)
time.sleep(2)
# --------------------------------------------------------------------------

# author
pyautogui.press('tab', presses=1)
# driver.find_element_by_name("author[]").click()  # This opens the windows file selector
pyautogui.write(nfo_author)
time.sleep(4)
pyautogui.press('enter')
# --------------------------------------------------------------------------
# narrator
pyautogui.press('tab')
# #driver.find_element_by_name("narrator[]").click()  # This opens the windows file selector
pyautogui.write(nfo_narr)
time.sleep(4)
pyautogui.press('enter')

# --------------------------------------------------------------------------

# audiotype

time.sleep(2)
nfo_audio = nfo_audio.replace('audio/', '').upper()
if nfo_audio == 'MP4':
    nfo_audio = 'M4B'

print('INFO: File type:', nfo_audio)
if not nfo_audio:
    nfo_audio = "MP3"
    print('INFO: File type was replace by default:', nfo_audio)

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
time.sleep(2)
# add kbps to output
kbps = 'kbps'
# range 20 to 34kbps
range34 = range(20, 35)
range48 = range(44, 49)
range96 = range(90, 97)
range62 = range(62, 63)
range64 = range(64, 65)
range192 = range(185, 193)
range128 = range(120, 129)

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
# if nfofile == "No NFO present":
meta = codecs.open('metadata_' + nfo_album + '.txt', 'w', 'utf-8-sig')
meta.write(
    '[color=#FF9933]...::**::... [/color][font=Comic Sans MS][size=5][color=#CCFF00]' + nfo_album + '[/color][/size][/font][color=#FF9933] ...::**::...[/color]' + '\n')

if nfo_sub == '':
    pass
else:
    meta.write('[color=#CCFF00]' + nfo_sub + '[/color]' + '\n')

meta.write('Author: ' + nfo_author + '\n')
meta.write('Narrator: ' + nfo_narr + '\n')
meta.write('Genre: ' + nfo_genre + '\n')
meta.write('Year: ' + str(nfo_year) + '\n')
if nfo_asin == '':
    pass
else:
    meta.write('Asin: ' + nfo_asin + '\n')

if nfo_copy == '':
    pass
else:
    meta.write('Copyright: ' + nfo_copy + '\n')

if nfo_link == '':
    pass
else:
    meta.write('Link: ' + nfo_link + '\n' + '\n')

meta.write(
    '\n' + '[color=#FF9933]...::**::... [/color][color=#faa702][size=5][b]Book Description[/b][/size][/color][color=#FF9933]...::**::... [/color]' + '\n')
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
meta.write('Full technical: ' + nfo_full + '\n')
meta.write('[size=1]' + script_version + '[/size]')
meta.close()

file = 'metadata_' + nfo_album + '.txt'
with open(file, 'r', encoding='utf-8-sig') as f:
    data = f.readlines()

elem = driver.find_element_by_xpath(
    "/html/body/div/div[1]/table/tbody/tr/td/div[2]/form/table/tbody/tr[12]/td[2]/div/div/textarea")
elem.send_keys(data, '\n')
time.sleep(2)

# --------------------------------------------------------------------------
# Genre
list_romance = ['Romance']
if re.compile('|'.join(list_romance), re.IGNORECASE).search(
        nfo_genre):  # re.IGNORECASE is used to ignore case
    nfo_genre = 'Romance'

list_horror = ['Horror', 'Zombie', 'Apocalypse']
if re.compile('|'.join(list_horror), re.IGNORECASE).search(
        nfo_genre):  # re.IGNORECASE is used to ignore case
    nfo_genre = 'Horror'

list_crime = ['Genre Fiction', 'Crime', 'Thriller', 'Mystery']
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

# --------------------------------------------------------------------------

# delete the metadata txt file
time.sleep(2)
print('INFO CLEAN: Delete .txt file.')
if os.path.exists(file):
    os.remove(file)
else:
    print("INFO CLEAN: The metadata txt file does not exist")

#     # Move files
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
print('INFO: End of script, please check values before pressing the button to upload.')

# window.read(timeout=10000)
# Console close
input("Press Enter to Quit...")
