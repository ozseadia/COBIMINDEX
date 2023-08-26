# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 22:48:53 2023

@author: OzSea
"""

import requests
from seleniumrequests import Edge
r=requests.get("http://ec2-3-123-19-109.eu-central-1.compute.amazonaws.com:8080/api/v1/export_data/excel")
url="http://ec2-3-123-19-109.eu-central-1.compute.amazonaws.com:8080/api/v1/export_data/excel"
webdriver = Edge()
response = webdriver.request('GET', url)

print(r.text) 
#requests.post(url, data = myInput)