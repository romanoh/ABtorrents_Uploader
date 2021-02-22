import os
import re
import fnmatch
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui


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
folder_path = "T:\\Uvi Poznansky - Twisted.M4B"


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                # nfo_filename = os.path.join(basename)
                nfo_filename = os.path.join(root, basename)  # Para full path
                yield nfo_filename


for nfo_filename in find_files(folder_path, '*.nfo'):
    print('INFO: Found source NFO to process:', nfo_filename)

if not nfo_filename:
    print('ERROR: Not Found NFO to process, exit program.')
    quit()

search_author = 'Author:'
search_album = 'Title:'
search_narr = 'Read By:'
search_copyright = 'Copyright:'
search_genre = 'Genre:'
search_duration = 'Duration:'
search_publisher = 'Publisher:'
search_unabridged = 'Unabridged:'
search_release = 'Release:'

time.sleep(1)
print('INFO: Searching Author...')
# buscar author
matched_lines = search_string_in_file(nfo_filename, search_author)
print('Total Matched lines : ', len(matched_lines))
for elem in matched_lines:
    linha = elem[0]
    author = elem[1]
# retirar tudo antes do char :
nfo_author = re.sub(r'^[^:]*:', r'', author).lstrip().title()
time.sleep(1)
print('INFO: Author found:', nfo_author)
time.sleep(1)
# raise SystemExit(0)


print('INFO: Searching Album...')
time.sleep(2)
# buscar title
matched_lines2 = search_string_in_file(nfo_filename, search_album)
print('Total Matched lines : ', len(matched_lines2))
for elem2 in matched_lines2:
    linha2 = elem2[0]
    title = elem2[1]
# remove (Unabridged)
nfo_album = re.sub(r'(Unabridged)', r'', title)
# remove - Book 1
nfo_album = re.sub(r'- Book 1', r'', nfo_album)
# retirar tudo antes do char :
nfo_album = re.sub(r'^[^:]*:', r'', nfo_album).lstrip().title()
print('INFO: Album found:', nfo_album)
time.sleep(3)

print('INFO: Searching narrator...')
time.sleep(1)
# search_narrator
matched_lines5 = search_string_in_file(nfo_filename, search_narr)
if not matched_lines5:
    print('INFO: Narrator not Found!')
    nfo_narr2 = None
else:
    print('Total Matched lines : ', len(matched_lines5))
    for elem5 in matched_lines5:
        linha5 = elem5[0]
        narr = elem5[1]
    # retirar tudo antes do char : / o .title() serve para meter a 1a letra grande.
    nfo_narr = re.sub(r'^[^:]*: ', r'', narr).lstrip().title()
    nfo_narr = re.sub(r'\(series-part\) ', r'', nfo_narr)
    print('INFO: Narrator found:', nfo_narr)
    time.sleep(1)

# search_genre Type
print('INFO: Searching Genre...')
time.sleep(1)
matched_lines8 = search_string_in_file(nfo_filename, search_genre)
if not matched_lines8:
    print('INFO: Genre not Found!')
    nfo_genre = None
else:
    print('Total Matched lines : ', len(matched_lines8))
    for elem8 in matched_lines8:
        linha8 = elem8[0]
        genre = elem8[1]
    # retirar tudo antes do char : / o .title() serve para meter a 1a letra grande.
    nfo_genre = re.sub(r'^[^:]*: ', r'', genre).lstrip()
    nfo_genre = re.sub(r'\(tmp_Genre2\) ', r'', nfo_genre)
    print('INFO: Genre Type found:', nfo_genre)
    time.sleep(1)

# search_genre Copyright
print('INFO: Searching Copyright...')
time.sleep(1)
matched_lines10 = search_string_in_file(nfo_filename, search_copyright)
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
matched_lines11 = search_string_in_file(nfo_filename, search_duration)
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
matched_lines12 = search_string_in_file(nfo_filename, search_publisher)
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

# search_Publisher Publisher
print('INFO: Searching Unabridged...')
time.sleep(1)
matched_lines13 = search_string_in_file(nfo_filename, search_unabridged)
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
matched_lines14 = search_string_in_file(nfo_filename, search_release)
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


