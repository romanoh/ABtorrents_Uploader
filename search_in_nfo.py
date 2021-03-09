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
folder_path = "Y:\\Genre Fiction\\Emerald O'Brien\\ 2020. What She Found (64kb)"


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

search_publisher = 'Publisher:'
search_unabridged = 'Unabridged:'


search_release = 'Release:'
search_size = 'Size:'

# --------------------------------------------------------------------------



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
            nfo_desc = join
            # logger_nfo.info('Description: %s', join)
            print(join)
        # else:
        # print('No description found.')
