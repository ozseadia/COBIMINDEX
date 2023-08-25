# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 23:59:59 2023

@author: OzSea
"""
import os
import shutil
import webbrowser
import time

#url = 'http://ec2-3-123-19-109.eu-central-1.compute.amazonaws.com:8080/api/v1/export_data/excel'

url='http://ec2-3-69-87-195.eu-central-1.compute.amazonaws.com:8080/api/v1/export_data/excel'
webbrowser.open_new(url)
time.sleep(30)
shutil.move(r'C:\Users\OzSea.LAPTOP-LLBIIFTU\Downloads\data.xlsx', r'G:\Oz\fiveer\Dani_Velinchick\KrohnApp\python_codes\COBIMINDEX\Data\data.xlsx')
