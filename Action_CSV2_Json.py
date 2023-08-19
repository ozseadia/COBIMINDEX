# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 09:01:19 2023

@author: OzSea
"""

import csv
import json
import pandas as pd
from tkinter import filedialog
import tkinter as tk
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
     
    # create a dictionary
    data = {}
    # 
    # Open a csv reader called DictReader
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    csvFilePath = filedialog.askopenfilename(title= "Please select Library file")
    with open(csvFilePath, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
    
    #csvReader=pd.read_excel(csvFilePath)     
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
    #for i in range(len(csvReader)):         
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['id']
            data[key] = rows
 
    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data,ensure_ascii=False, indent=4))
         
# Driver Code
 
# Decide the two file paths according to your
# computer system
csvFilePath = r'Names.csv'
jsonFilePath = r'Actions.json'
 
# Call the make_json function
make_json(csvFilePath, jsonFilePath)