#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os.path import basename
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import reverse_geocoder as rg


class Photo:
    """Classe permettant de renomer et organiser les photos grace aux EXIF
    """

    def __init__(self, FullPathName):
        """Pour l'instant, on ne va définir qu'un seul attribut"""
        self.FullPathName = FullPathName
        file_basename, self.Photo_Extention = os.path.splitext(self.FullPathName)
        self.Photo_Name = basename(self.FullPathName)
        self.PhotoBaseName = self.Photo_Name.replace(self.get_PhotoExtention(), "")
        self.Photo_Path = self.FullPathName.replace("/" + basename(self.FullPathName), "")
        self.PhotoExif = None
        self.__get_exif()
        self.labeled = None
        if self.Is_ExifExistInPhoto():
            self.__get_labeled_exif()

    def get_PhotoName(self):
        """
        Donne le nom du fichier photo

        :Example:
        >>MaPhoto = Photo("/home/DC1.JPG")
        >>print(MaPhoto.get_PhotoName())
        DC1.JPG

        :return:
        """
        return self.Photo_Name

    def get_PhotoBaseName(self):
        return self.PhotoBaseName

    def get_PhotoExtention(self):
        return self.Photo_Extention

    def get_PhotoPath(self):
        return self.Photo_Path

    def get_PhotoFullPathName(self):
        return self.FullPathName

    def __get_exif(self):
        image = Image.open(self.FullPathName)
        image.verify()
        self.PhotoExif = image._getexif()

    def Is_ExifExistInPhoto(self):
        if not self.PhotoExif:
            return False
        else:
            return True

    def __get_labeled_exif(self):
        if not self.PhotoExif:
            raise ValueError("No EXIF metadata found")
        self.labeled = {}
        for (key, val) in self.PhotoExif.items():
            self.labeled[TAGS.get(key)] = val

    def print_PhotoExif(self):
        """
        Affiche tous les TAG Exif ainsi que leur valeur pour la photo
        :return: na
        """
        if not self.PhotoExif:
            raise ValueError("No EXIF metadata found")
        self.__get_exif()
        self.__get_labeled_exif()
        for label in self.labeled:
            print(label + "  : " + str(self.labeled[label]))

    def get_PhotoExifLabelValue(self, ExifLabel):
        """
        Donne la valeur exif du label
        :param ExifLabel: Label Exif (voir les label grace a la methode print_ExifTagItem)
        :return: Valeur du label Exif de la photo
        """
        if not self.PhotoExif:
            raise ValueError("No EXIF metadata found")
        self.__get_labeled_exif()
        for label in self.labeled:
            if label == ExifLabel:
                return self.labeled[ExifLabel]


    def print_ExifTagItem(self):
        """
        Affiche dans le terminal tous les noms de TAG Exif
        :return: na
        """
        if not self.PhotoExif:
            raise ValueError("No EXIF metadata found")
        for (idx, tag) in TAGS.items():
            print(tag)

    def get_geotagging(self):
        """
        Donne les informations du TAG Exif GPS de la photo
        :return: Ensemble des informations GPS de la photo
        """
        if not self.PhotoExif:
            #raise ValueError("No EXIF metadata found")
            return None
        geotagging = {}
        for (idx, tag) in TAGS.items():
            if tag == 'GPSInfo':
                if idx not in self.PhotoExif:
                    #raise ValueError("No EXIF geotagging found")
                    return None
                for (key, val) in GPSTAGS.items():
                    if key in self.PhotoExif[idx]:
                        geotagging[val] = self.PhotoExif[idx][key]
        return geotagging

    def __get_decimal_from_dms(self, dms, ref):
        """
        Methode prive pour retourne les coordonne en decimale
        :param dms: Coordonee GPS
        :param ref: Coordonee GPS De Reference
        :return: Coordonee GPS en decimale
        """
        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1] / 60.0
        seconds = dms[2][0] / dms[2][1] / 3600.0
        if ref in ['S', 'W']:
            degrees = -degrees
            minutes = -minutes
            seconds = -seconds
        return round(degrees + minutes + seconds, 5)

    def get_coordinates(self, geotags):
        """
        Donne les valeur GPS de coordone Latitude et Longitude
        :param geotags: Coordone GPS
        :return: Coordonne GPS Latitude et Longitude
        """
        lat = self.__get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
        lon = self.__get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
        return (lat,lon)

    def get_GpsElement(self, coordinates):
        self.GpsElements = rg.search(coordinates,mode=1) # default mode = 2

    def get_GpsElementVille(self):
        return self.GpsElements[0]["name"]

    def get_GpsElementRegion(self):
        return self.GpsElements[0]["admin1"]
