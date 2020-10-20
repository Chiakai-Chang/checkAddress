# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 13:11:45 2020

@author: Chiakai
"""

import geocoder

keyword = '臺中市南屯區文心路2段202號'

g = geocoder.arcgis(keyword)
r = g.json

lat = r.get('lat')
lng = r.get('lng')

#經緯度換googlemap網址
url = f'https://www.google.com.tw/maps/search/{lat},{lng}/@{lat},{lng},17z?hl=zh-TW'
r['googleMapUrl'] = url                    