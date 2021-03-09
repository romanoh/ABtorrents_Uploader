import os
import re
import fnmatch
import time
import logging

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

file = "Y:\\Genre Fiction\\Emerald O'Brien\\ 2020. What She Found (64kb)\\000-emerald_obrien_-_what_she_found-audiobook-web-en-2020-oldswe_int.nfo"

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

logger_nfo = logging.getLogger('nfo')
# --------------------------------------------------------------------
logger_nfo.info('Starting looking for NFO file....')


# Book Title
_title = ["Title", "mahal"]
logger_nfo.info('Searching Title book...')
with open(file, "r+") as file1:
    fileline1 = file1.readlines()
    for x in _title:  # <--- Loop through the list to check
        for line in fileline1:  # <--- Loop through each line
            line = line.casefold() # <--- Set line to lowercase
            if x.casefold() in line:
                logger_nfo.info('Line found with word: %s', x)
                nfo_album = line

                # remove (Unabridged)
                nfo_album = re.sub(r'(Unabridged)', r'', nfo_album)
                # remove everything before :
                nfo_album = re.sub(r'^[^:]*:', r'', nfo_album).lstrip().title()
                # splitting if title as series
                nfo_album2 = nfo_album.split(' - ')
                try:
                    nfo_album = nfo_album2[1]
                    nfo_series = nfo_album2[0]
                    logger_nfo.info('Found Book Title: %s', nfo_album)
                except:
                    logger_nfo.info('Found Book Title: %s', nfo_album)

if nfo_album == '':
    logger_nfo.warning('Book Title not found.')


# Book Author
_author = ["Author", "mahal"]
logger_nfo.info('Searching Author book...')
with open(file, "r+") as file1:
    fileline1 = file1.readlines()
    for x in _author:  # <--- Loop through the list to check
        for line in fileline1:  # <--- Loop through each line
            line = line.casefold()  # <--- Set line to lowercase
            if x.casefold() in line:
                logger_nfo.info('Line found with word: %s', x)
                nfo_author = line

                # remove everything before :
                nfo_author = re.sub(r'^[^:]*:', r'', nfo_author).lstrip().title()
                logger_nfo.info('Author Found: %s', nfo_author)
if nfo_author == '':
    logger_nfo.warning('Author not found.')

# Book Narrator
_narrator = ["Read by", "Narrator"]
logger_nfo.info('Searching Narrator...')
with open(file, "r+") as file1:
    fileline1 = file1.readlines()
    for x in _narrator:  # <--- Loop through the list to check
        for line in fileline1:  # <--- Loop through each line
            line = line.casefold()  # <--- Set line to lowercase
            if x.casefold() in line:
                logger_nfo.info('Line found with word: %s', x)
                nfo_narr = line

                # remove everything before :
                nfo_narr = re.sub(r'^[^:]*:', r'', nfo_narr).lstrip().title()
                logger_nfo.info('Narrator Found: %s', nfo_narr)
if nfo_narr == '':
    logger_nfo.warning('Narrator not found.')

# Book Series
_series = ["Series", "mahal"]
logger_nfo.info('Searching Series...')
with open(file, "r+") as file1:
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
                    logger_nfo.info('Series Found: %s', nfo_series)
                else:
                    pass

if nfo_series == '':
    logger_nfo.warning('Series not found.')
else:

    try:
        num_serie2 = nfo_series.split(' Book ')
        num_serie = num_serie2[1]
        logger_nfo.info('Series number found: %s', num_serie)
    except:
        logger_nfo.warning('Series number not Found!')

    nfo_series = re.sub(r' Book 1', r'', nfo_series)
    nfo_series = re.sub(r' Book 2', r'', nfo_series)
    nfo_series = re.sub(r' Book 3', r'', nfo_series)
    nfo_series = re.sub(r' Book 4', r'', nfo_series)
    logger_nfo.info('Series Found: %s', nfo_series)

if num_serie == '':
    # Book series number
    _number = ["Position", "sfdsfdsfsd"]
    logger_nfo.info('Searching Series number...')
    with open(file, "r+") as file1:
        fileline1 = file1.readlines()
        for x in _number:  # <--- Loop through the list to check
            for line in fileline1:  # <--- Loop through each line
                line = line.casefold()  # <--- Set line to lowercase
                if x.casefold() in line:
                    logger_nfo.info('Line found with word: %s', x)
                    num_serie = line

                    # remove everything before :
                    num_serie = re.sub(r'^[^:]*:', r'', num_serie).lstrip().title()
                    logger_nfo.info('Narrator Found: %s', num_serie)
    if num_serie == '':
        logger_nfo.warning('Series number not found.')
else:
    pass

# Book Genre
_genre = ["Genre", "wrwrwr"]
logger_nfo.info('Searching Genre...')
with open(file, "r+") as file1:
    fileline1 = file1.readlines()
    for x in _genre:  # <--- Loop through the list to check
        for line in fileline1:  # <--- Loop through each line
            line = line.casefold()  # <--- Set line to lowercase
            if x.casefold() in line:
                logger_nfo.info('Line found with word: %s', x)
                nfo_genre = line

                # remove everything before :
                nfo_genre = re.sub(r'^[^:]*:', r'', nfo_genre).lstrip().title()
                logger_nfo.info('Genre Found: %s', nfo_genre)
if nfo_genre == '':
    logger_nfo.warning('Genre not found.')

# Book Copyright
_copy = ["Copyright", "dfdfg"]
logger_nfo.info('Searching Copyright...')
with open(file, "r+") as file1:
    fileline1 = file1.readlines()
    for x in _copy:  # <--- Loop through the list to check
        for line in fileline1:  # <--- Loop through each line
            line = line.casefold()  # <--- Set line to lowercase
            if x.casefold() in line:
                logger_nfo.info('Line found with word: %s', x)
                nfo_copy = line

                # remove everything before :
                nfo_copy = re.sub(r'^[^:]*:', r'', nfo_copy).lstrip().title()
                logger_nfo.info('Copyright Found: %s', nfo_copy)
if nfo_copy == '':
    logger_nfo.warning('Copyright not found.')

# Book Duration
_dura = ["Duration", "dfdfg"]
logger_nfo.info('Searching Duration...')
with open(file, "r+") as file1:
    fileline1 = file1.readlines()
    for x in _dura:  # <--- Loop through the list to check
        for line in fileline1:  # <--- Loop through each line
            line = line.casefold()  # <--- Set line to lowercase
            if x.casefold() in line:
                logger_nfo.info('Line found with word: %s', x)
                nfo_duration = line

                # remove everything before :
                nfo_duration = re.sub(r'^[^:]*:', r'', nfo_duration).lstrip().title()
                logger_nfo.info('Duration Found: %s', nfo_duration)
if nfo_duration == '':
    logger_nfo.warning('Duration not found.')

# Book Publisher
_publisher = ["Publisher", "etret"]
logger_nfo.info('Searching Narrator...')
with open(file, "r+") as file1:
    fileline1 = file1.readlines()
    for x in _publisher:  # <--- Loop through the list to check
        for line in fileline1:  # <--- Loop through each line
            line = line.casefold()  # <--- Set line to lowercase
            if x.casefold() in line:
                logger_nfo.info('Line found with word: %s', x)
                nfo_publisher = line

                # remove everything before :
                nfo_publisher = re.sub(r'^[^:]*:', r'', nfo_publisher).lstrip().title()
                logger_nfo.info('Publisher Found: %s', nfo_publisher)
if nfo_publisher == '':
    logger_nfo.warning('Publisher not found.')

# Book unbridged
_uno = ["Unbridged", "yertret"]
logger_nfo.info('Searching Unbridged...')
with open(file, "r+") as file1:
    fileline1 = file1.readlines()
    for x in _uno:  # <--- Loop through the list to check
        for line in fileline1:  # <--- Loop through each line
            line = line.casefold()  # <--- Set line to lowercase
            if x.casefold() in line:
                logger_nfo.info('Line found with word: %s', x)
                nfo_unabridged = line

                # remove everything before :
                nfo_unabridged = re.sub(r'^[^:]*:', r'', nfo_unabridged).lstrip().title()
                logger_nfo.info('Unbridged Found: %s', nfo_unabridged)
if nfo_unabridged == '':
    logger_nfo.warning('Unbridged not found.')
