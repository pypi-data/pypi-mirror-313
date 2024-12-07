# piwiPre

piwiPre is a python/windows tool to prepare pictures and video for piwigo (and any other album management), 
and maintain the piwigo album and database

It was initially developed for a piwigo instance running on a remote server such as a Synology NAS, 
while the 'photo' and 'thumbnails' directories are accessible from a PC where piwiPre is run, 
but it can run on many other configurations. 

Many features can be useful even when piwigo is not used.

piwiPre executes the following tasks:

1. Read configuration files and command-line argument to insure a high level of configuration.

2. Process new pictures/video on the local host in the TRIAGE directory and copy them on the piwigo server
   - process copy of content and leave original unmodified
   - convert most (managed by python) pictures formats to JPG
   - convert most (managed by ffmpeg) video formats to MP4
   - realign picture rotation, according to EXIF data
   - perform correction on picture/video dates according to settings
   - insert metadata (copyright, instructions, author) in the JPEG IPTC or MP4 file
   - rename pictures according to a user-defined scheme
   - replace by '_' characters that piwigo does not support in filenames
   - avoid collision of filenames
   - create the corresponding sub-album in piwigo, inserted in the increasing order of subdirectories
   - put updated copies into ALBUM, through file copy, NFS or ssh/sftp
   - build piwigo thumbnails, even for video
   - copy thumbnails to the appropriate location, through file copy, NFS or ssh/sftp
   - self-configure ALBUM for maintenance
   - update the piwigo SQL database with metadata and MD5 checksum

3. Maintain ALBUM 
   - work only on selected directories
   - Ensure the directory is aligned with the current configuration
   - Insert pictures and video in the piwigo database, with metadata, md5 checksum and author
   - Update the information stored in the piwigo database
   
4. log intensively the actions

piwiPre comes with:
   - a Windows installer: pwpInstaller.exe, with and without Graphical User Interface (--gui true)
   - a GUI that can be used to configure and/or run the program : piwiPre --gui true
   - cmdline versions of piwiPre and pwpInstaller 
   - a python version of pwpConfigurator, that runs on Linux and Windows
   - Python source code, 
   - a Python library downloadable from Pypi, 
   - Windows Executable versions
   - 74 configuration items
   - a complete user documentation in English and French (see bellow)
   - test coverage at 95% of the code

## what piwiPre does *not*

piwiPre does not manage synology thumbnails created by Synology file-station in @eaDir directories,
which is not a concern because those thumbnails are small (less than 500KB).


## How to get piwiPre

- Python module on Pypi : https://pypi.org/project/piwiPre
- Python source on gitlab: https://gitlab.com/fabien_battini/piwiPre
- Windows installer and one-file exes on gitlab artifacts: https://fabien_battini.gitlab.io/piwipre/html/download.html


# How to use piwiPre (short)

1. Copy new pictures and videos from your cameras to the TRIAGE directory.

2. Create subdirectories is TRIAGE according to your taste
   - The name of the subdirectory will be a base for the new filename of pictures
   - move files into one of those.

3. Optionally edit the pictures in TRIAGE with digiKam, gimp or other image processing tool.

4. If you want managed files to be written to a remote piwigo server, then you need a piwiPre.ini configuration file.
   - If it does not exist, create one by running 'piwiPre --gui true'
   - If ALBUM, THUMBNAILS and AUTO-CONFIG directories are accessible, album, thumbnails and auto-config should be set.
   - If the sql database is accessible, sql-user, sql-pwd, sql-host, sql-port should be set. 
   - You may want to change the (english speaking) default values for month-name, copyright, instructions.
   
5. Run piwiPre

6. Results:
   - pictures have metadata inserted
   - picture rotation is reset to default
   - Files are renamed according to directories, dates
   - the thumbnails are generated
   - the corresponding sub-album has been created in piwigo, inserted in the increasing order of subdirectories
   - files have been copied to ALBUM
   - piwigo database is updated
   - so, the corresponding pictures should be visible in piwigo without further action
   - piwiPre.log holds an exhaustive log
   
# piwiPre as a tool

piwiPre is also a command-line tool, with command-line options.
For more information:

``piwiPre --help
  or python -m piwiPre --help
``

# Documentation

Documentation is built using Sphinx https://www.sphinx-doc.org/

Documentation is generated in https://fabien_battini.gitlab.io/piwipre/html/
This process is achieved automatically through gitlab CI pipelines.

gitlab: https://gitlab.com/fabien_battini/piwipre

doc : https://fabien_battini.gitlab.io/piwipre/html/ 

test coverage: https://fabien_battini.gitlab.io/piwipre/html/htmlcov/index.html  

pypi: https://pypi.org/project/piwipre/

LinkedIN: https://www.linkedin.com/in/fabien-battini-supelec/
