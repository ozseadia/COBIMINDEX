# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 11:20:21 2023

@author: OzSea
"""

import random
import openpyxl
import string
import pandas as pd

def generate_random_numbers(count):
    random_numbers = []
    for _ in range(count):
        random_number = random.randint(100000, 999999)
        random_numbers.append(random_number)
    return random_numbers

def generate_random_password(length=4):
    characters = string.ascii_uppercase + string.digits # + string.punctuation string.ascii_letters
    password = ''.join(random.choice(characters) for _ in range(length))
    return password    


def save_to_excel(numbers_list, file_path):
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    for row_idx, number in enumerate(numbers_list, start=1):
        sheet.cell(row=row_idx, column=1, value=number)

    workbook.save(file_path)
    

if __name__ == "__main__":
    # Generate a list of 300 random 6-digit numbers
    random_numbers_list = generate_random_numbers(300)
    
    num_passwords = 300
    passwords_list = []

    for _ in range(num_passwords):
        password = generate_random_password()
        passwords_list.append(password)
    

    # Save the list to an Excel file
    excel_file_path = "random_numbers1.xlsx"
    TotalList=list()
    
    
    for i in range(300):
        TotalList.append([random_numbers_list[i],passwords_list[i]])
        
    DataFrame=pd.DataFrame(TotalList,columns=['acount', 'password'])    
    #save_to_excel( DataFrame, excel_file_path)
    DataFrame.to_excel(excel_file_path, index=False)

    print("Random numbers have been generated and saved to 'random_numbers.xlsx'.")









