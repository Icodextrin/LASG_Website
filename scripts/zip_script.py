import zipfile
import os


def unzip_all_files(path):
    for file in os.listdir(path):  # get the list of files
        if zipfile.is_zipfile(path + "/" + file):  # if it is a zipfile, extract it
            with zipfile.ZipFile(path + "/" + file) as item:  # treat the file as a zip
                item.extractall(path + "/json/")  # extract it in the working directory
