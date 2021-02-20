Beta v.0.2.6
[20.02.21] CHG: A small change to the progress bar and layout.

Beta v.0.2.5 - ABtorrents uploader Helper
[18.02.21] NEW: Added Progress Bar in creating torrent.
[18.02.21] NEW: If Tag Album as something after ":" remove it.
[18.02.21] NEW: Add subtitle album tag if present to description.
[18.02.21] FIX: Fix in ID3 numbers at start Album.
[18.02.21] FIX: Error handling if cover image not present or tag corrupt.
[18.02.21] CHG: A small change to the subtitle description.
[17.02.21] FIX: Small fixes in series.

Beta v.0.2.4 - ABtorrents uploader Helper
[16.02.21] NEW: Delete metadata .txt file when done.
[16.02.21] NEW: Delete any old .torrent same name.
[16.02.21] FIX: Bug with the series number.
[16.02.21] FIX: Bug renaming torrent if present.
[16.02.21] FIX: Clear text box series number before new number.
[16.02.21] FIX: Add 0 to text box series number if none.
[16.02.21] FIX: Bitrate range duplicate.
[16.02.21] FIX: Initial ï»¿ found in Description fixed(using utf-8-sig).

Beta v.0.2.3 - ABtorrents uploader Helper
14.02.2021
NEW: The description is not the nfo now, but metadata from audiofile.
NEW: Delete metadata .txt file when done.
CHG: Several improvements to description.

Beta v.0.2.2 - ABtorrents uploader Helper
13.02.2021
New: Exclude from .torrent nfo file.(ABtorrents Rule)
Improve: The description is not the nfo now, but metadata from audiofile.(wip)
New: Correct format for Author and narrator (ex: A. G. Mark) using regex.


Beta v.0.2.1 - Console appearance version - ABtorrents uploader Helper
12.02.2021
Fix: Some fixes
Fix: Some fixes for Single file

Beta v.0.2 - Console appearance version - ABtorrents uploader Helper
09.02.2021
New: Console!
Fix: Some fixes for Single file
Fix: several fixes

Beta v.0.1 - Abtorrentes uploader helper
First Beta


----------------------------------------------------------------------------------------
TODO:
other internet explorers, just not firefox.
getting the data for metadata from torrent site.


----------------------------------------------------------------------------------------

Instructions/helper(this will be improved in time):

1. You choose the folder or file to make the torrent.
2. It creates a file config.ini, with the folder/file paths and firefox session for later use.
you can change the data directly in the file.
3. Choose the .torrent path.
4: It searches for audio files and image.
5. It gets audio file for the metadata and image to upload,
if config file not there it asks for session(this can be changed for password and username).
6. It opens firefox
7. It checks in the author and narrator if it is present, by putting it in, if it is present no harm done,
important for now i have only made it for one narrator and one author(working on it).
8.Then goes for main page and fills all the stuff, ofc there is work to be done especially in the Genre section.
9. You have to check all the stuff to be ok to upload.

It is an helper not all automatic





