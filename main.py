#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
#https://medium.com/@richdayandnight/a-simple-tutorial-on-how-to-document-your-python-project-using-sphinx-and-rinohtype-177c22a15b5b

from photo import Photo
import os
import shutil
import datetime
from os import walk

def converter(date_time):
    """
    Converti une date (format string) vers une date (format string) mais en changeant certain caracteres
    :param date_time: Date au format string
    :return: la date au format string en remplacant ':' par "" et " " par "_"
    """
    format = '%Y:%m:%d_'  # The format
    #datetime_str = datetime.datetime.strptime(date_time, format)
    datetime_str = date_time.replace(":","")
    datetime_str = datetime_str.replace(" ","_")
    return datetime_str

def get_year(date_time):
    """
    Converti une date (format string) vers une date (format string) mais en changeant certain caracteres
    :param date_time: Date au format string
    :return: la date au format string en remplacant ':' par "" et " " par "_"
    """
    datetime_str = date_time.split("_")
    return datetime_str[0][:4]

def get_month(date_time):
    datetime_str = date_time.split("_")
    return datetime_str[0][4:6]

def get_allfiles(directory):
    file_list = []
    for (repertoire, sousRepertoires, fichiers) in walk(directory):
        if not sousRepertoires:
            for file in fichiers:
                # print(repertoire + "/" + fichier)
                file_list.append(repertoire + "/" + file)
    return file_list

# MaPhoto_FullPath = "/home/seb/Images/PourTestDeTrieRenomage/2018_10_27__17_46_44.JPG"
# MaPhoto = Photo(MaPhoto_FullPath)
# print(MaPhoto.get_PhotoName())
# print(MaPhoto.get_PhotoBaseName())
# print(MaPhoto.get_PhotoExtention())
# print(MaPhoto.get_PhotoPath())

#Declaration du chemin ou se trouve les photos
Path_Photo = "/home/seb/Images/PourTestDeTrieRenomage"
#Declaration des extention prise a prendre en compte
image_ext = ['.jpg', '.jpeg', 'cr2', 'cr3' 'nef', 'dng']

#On recupere toute les photos du repertoire
#image_files = [ifile for ifile in os.listdir(Path_Photo)
#               if os.path.splitext(ifile)[1].lower() in image_ext]
#on recupere les photos du repertoire et des sous repertoire
image_files = get_allfiles(Path_Photo)

#Pour toutes les photos
for image_file in image_files:
    image_pathfile = os.path.normpath(image_file)
    #MaPhoto = Photo(Path_Photo + "/" + image_file)
    MaPhoto = Photo(image_pathfile)
    PhotoExtention = MaPhoto.get_PhotoExtention()
    PhotoPath = MaPhoto.get_PhotoPath()
    print("Photo Source : " + MaPhoto.get_PhotoFullPathName())
    #Si la photo n'a pas de data EXIF
    if MaPhoto.labeled == None:
        #print(MaPhoto.get_PhotoFullPathName() + " No Exif In this file")
        NouveauPathDePhoto = PhotoPath + "/" + "_A_TRIER_MANUELLEMENT"
        NouveauNomDePhoto = NouveauPathDePhoto + "/" + MaPhoto.get_PhotoName()
    #Si la photo a des data EXIF
    else:
        #MaPhoto.print_PhotoExif()
        #Si la photo n'a pas de date dans les data EXIF
        if MaPhoto.get_PhotoExifLabelValue("DateTimeOriginal") == None:
            print("Photo Move To >>>>>  NoExifInformationAvailable")
            NouveauPathDePhoto = Path_Photo + "/" + "_A_TRIER_MANUELLEMENT"
            NouveauNomDePhoto = NouveauPathDePhoto + "/" + MaPhoto.get_PhotoName()

        else:
            #ON recupere le year et le month de la date de la photo avec le EXIF
            DateConverti = converter(MaPhoto.get_PhotoExifLabelValue("DateTimeOriginal"))
            PhotoYear = get_year(DateConverti)
            PhotoMonth = get_month(DateConverti)

            #Si la photo a des data de geolocalisation dans EXIF
            GpsTags = MaPhoto.get_geotagging()
            if GpsTags != None:
                GpsCoord = MaPhoto.get_coordinates(GpsTags)
                MaPhoto.get_GpsElement(GpsCoord)
                PhotoVille = MaPhoto.get_GpsElementVille()
                PhotoRegion = MaPhoto.get_GpsElementRegion()
                NouveauPathDePhoto = Path_Photo + "/" + PhotoYear + "/" + PhotoMonth + "/" + PhotoVille
                NouveauNomDePhoto = NouveauPathDePhoto + "/" + DateConverti + PhotoExtention
            else:
                print("Pas de coordone GPS")
                #NouveauPathDePhoto = PhotoPath + "/" + "_A_TRIER_MANUELLEMENT"
                NouveauPathDePhoto = Path_Photo + "/" + PhotoYear + "/" + PhotoMonth
                #NouveauNomDePhoto = NouveauPathDePhoto + "/" + MaPhoto.get_PhotoName()
                NouveauNomDePhoto = NouveauPathDePhoto + "/" + DateConverti + PhotoExtention

        print("Photo Move To >>>>>  " + NouveauNomDePhoto)
        if not os.path.exists(NouveauPathDePhoto):
            print("Creation du repertoire : " + NouveauPathDePhoto)
            os.makedirs(NouveauPathDePhoto)
        shutil.move(MaPhoto.get_PhotoFullPathName(), NouveauNomDePhoto)