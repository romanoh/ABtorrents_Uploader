import os
import re
import fnmatch
import time
import logging

file_path = ''

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
nfofile = None


def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, mode="r", encoding="utf-8", errors='ignore') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results


# nfo Path
nfo_filename = None
folder_path = "T:\\Robert Gott - The Port Fairy Murders"


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                # nfo_filename = os.path.join(basename)
                nfo_filename = os.path.join(root, basename)  # Para full path
                yield nfo_filename


if file_path == '':
    for nfofile in find_files(folder_path, '*.nfo'):
        logger_nfo.info('Found NFO source: %s', nfofile)
    for nfofile in find_files(folder_path, '*.txt'):
        logger_nfo.info('Found TXT source: %s', nfofile)

    if nfofile is None:
        logger_nfo.warning('NFO file not present...')
        nfofile = "No NFO present"
    else:
        pass

else:
    logger_nfo.info('Metadata will be made from audio file metadata.')
    pass
# -------------------------------------------------------------------------------
search_album = 'Title:'
search_author = 'Author:'
try:
    search_narr = 'Read By:'
except NameError:
    search_narr = 'Narrator:'
search_copyright = 'Copyright:'
search_genre = 'Genre:'
search_duration = 'Duration:'
search_publisher = 'Publisher:'
search_unabridged = 'Unabridged:'
try:
    search_series = 'Series'

except NameError:
    search_series = 'Series Name:'
try:
    search_series_num = 'Series'
except NameError:
    search_series_num = 'Position in Series:'
search_release = 'Release:'
search_size = 'Size:'

time.sleep(1)
logger_nfo.info('Searching Author...')
# search author
matched_lines = search_string_in_file(nfofile, search_author)
logger_nfo.info('Total Matched lines: %s', len(matched_lines))
for elem in matched_lines:
    linha = elem[0]
    author = elem[1]
# remove everything after :
nfo_author = re.sub(r'^[^:]*:', r'', author).lstrip().title()
time.sleep(1)
logger_nfo.info('Author found: %s', nfo_author)
time.sleep(1)

logger_nfo.info('Searching Title book...')
time.sleep(1)
# search title
matched_lines2 = search_string_in_file(nfofile, search_album)
logger_nfo.info('Total Matched lines: %s', len(matched_lines2))
for elem2 in matched_lines2:
    linha2 = elem2[0]
    title = elem2[1]
# remove (Unabridged)
nfo_album = re.sub(r'(Unabridged)', r'', title)
# remove - Book 1
nfo_album = re.sub(r'- Book 1', r'', nfo_album)
# retirar tudo antes do char :
nfo_album = re.sub(r'^[^:]*:', r'', nfo_album).lstrip().title()
logger_nfo.info('Book found: %s', nfo_album)

logger_nfo.info('Searching narrator...')
time.sleep(1)
# search_narrator
matched_lines5 = search_string_in_file(nfofile, search_narr)
if not matched_lines5:
    logger_nfo.warning('Narrator not Found!')
    nfo_narr2 = None
else:
    logger_nfo.info('Total Matched lines: %s', len(matched_lines5))
    for elem5 in matched_lines5:
        linha5 = elem5[0]
        narr = elem5[1]
    # retirar tudo antes do char : / o .title() serve para meter a 1a letra grande.
    nfo_narr = re.sub(r'^[^:]*: ', r'', narr).lstrip().title()
    nfo_narr = re.sub(r'\(series-part\) ', r'', nfo_narr)
    logger_nfo.info('Narrator found: %s', nfo_narr)
    time.sleep(1)

# search_series
logger_nfo.info('Searching Series...')
time.sleep(1)
matched_lines7 = search_string_in_file(nfofile, search_series)
if not matched_lines7:
    logger_nfo.warning('Series not Found!')
    nfo_series = None
else:
    logger_nfo.info('Total Matched lines: %s', len(matched_lines7))
    for elem7 in matched_lines7:
        linha7 = elem7[0]
        series7 = elem7[1]
        print (elem7[1])
    # retirar tudo antes do char : / o .title() serve para meter a 1a letra grande.
    num_serie = re.search('([0-9]+)', series7)
    num_serie = num_serie.group()
    nfo_series = re.sub(r'\d+', r'', series7).lstrip()
    logger_nfo.info('Series found: %s', nfo_series)
    try:
        logger_nfo.info('Series number found: %s', num_serie)
    except:
        logger_nfo.info('No Series number found!')
        pass
    time.sleep(1)

# search_genre Type
logger_nfo.info('Searching Genre...')
time.sleep(1)
matched_lines8 = search_string_in_file(nfofile, search_genre)
if not matched_lines8:
    logger_nfo.warning('Genre not Found!')
    nfo_genre = None
else:
    logger_nfo.info('Total Matched lines: %s', len(matched_lines8))
    for elem8 in matched_lines8:
        linha8 = elem8[0]
        genre = elem8[1]
    # retirar tudo antes do char : / o .title() serve para meter a 1a letra grande.
    nfo_genre = re.sub(r'^[^:]*: ', r'', genre).lstrip()
    nfo_genre = re.sub(r'\(tmp_Genre2\) ', r'', nfo_genre)
    logger_nfo.info('Genre Type found: %s', nfo_genre)
    time.sleep(1)

# search_genre Copyright
print('INFO: Searching Copyright...')
time.sleep(1)
matched_lines10 = search_string_in_file(nfofile, search_copyright)
if not matched_lines10:
    print('INFO: Copyright not Found!')
    nfo_copyright = None
else:
    print('Total Matched lines : ', len(matched_lines10))
    for elem10 in matched_lines10:
        linha10 = elem10[0]
        copy = elem10[1]
    # retirar tudo antes do char : / o .title() serve para meter a 1a letra grande.
    nfo_copy = re.sub(r'^[^:]*: ', r'', copy).lstrip()
    print('INFO: Copyright found:', nfo_copy)
    time.sleep(1)

# search_durtion Duration
print('INFO: Searching Duration...')
time.sleep(1)
matched_lines11 = search_string_in_file(nfofile, search_duration)
if not matched_lines11:
    print('INFO: Duration not Found!')
    nfo_duration = None
else:
    print('Total Matched lines : ', len(matched_lines11))
    for elem11 in matched_lines11:
        linha11 = elem11[0]
        dura = elem11[1]
    # retirar tudo antes do char : / o .title() serve para meter a 1a letra grande.
    nfo_duration = re.sub(r'^[^:]*: ', r'', dura).lstrip()
    print('INFO: Duration found:', nfo_duration)
    time.sleep(1)

# search_Publisher Publisher
print('INFO: Searching Publisher...')
time.sleep(1)
matched_lines12 = search_string_in_file(nfofile, search_publisher)
if not matched_lines12:
    print('INFO: Publisher not Found!')
    nfo_publisher = None
else:
    print('Total Matched lines : ', len(matched_lines12))
    for elem12 in matched_lines12:
        linha12 = elem12[0]
        publi = elem12[1]
    # retirar tudo antes do char :.
    nfo_publisher = re.sub(r'^[^:]*: ', r'', publi).lstrip()
    print('INFO: Publisher found:', nfo_publisher)
    time.sleep(1)

# search_unabridged
print('INFO: Searching Unabridged...')
time.sleep(1)
matched_lines13 = search_string_in_file(nfofile, search_unabridged)
if not matched_lines13:
    print('INFO: Unabridged not Found!')
    nfo_unabridged = None
else:
    print('Total Matched lines : ', len(matched_lines13))
    for elem13 in matched_lines13:
        linha13 = elem13[0]
        unabridged = elem13[1]
    # retirar tudo antes do char :.
    nfo_unabridged = re.sub(r'^[^:]*: ', r'', unabridged).lstrip()
    print('INFO: Unabridged found:', nfo_unabridged)
    time.sleep(1)

# search_Release Release
print('INFO: Searching Release...')
time.sleep(1)
matched_lines14 = search_string_in_file(nfofile, search_release)
if not matched_lines14:
    print('INFO: Release not Found!')
    nfo_release = None
else:
    print('Total Matched lines : ', len(matched_lines14))
    for elem14 in matched_lines14:
        linha14 = elem14[0]
        release = elem14[1]
    # retirar tudo antes do char :.
    nfo_release = re.sub(r'^[^:]*: ', r'', release).lstrip()
    print('INFO: Release found:', nfo_release)
    time.sleep(1)

# search_Release Release
print('INFO: Searching Size...')
time.sleep(1)
matched_lines20 = search_string_in_file(nfofile, search_size)
if not matched_lines20:
    print('INFO: Size not Found!')
    nfo_size = None
else:
    print('Total Matched lines : ', len(matched_lines20))
    for elem20 in matched_lines20:
        linha20 = elem20[0]
        size = elem20[1]
    # retirar tudo antes do char :.
    nfo_size = re.sub(r'^[^:]*: ', r'', size).lstrip()
    print('INFO: Size found:', nfo_size)
    time.sleep(1)

search_desc = 'Description'
# search_desc
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
            # logger_nfo.info('Description: %s', join)
            print(join)
        else:
            print('No description found.')
