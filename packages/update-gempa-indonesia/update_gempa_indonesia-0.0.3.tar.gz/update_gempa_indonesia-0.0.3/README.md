# latest-indonesia-earthquake
this package will get the latest earthquake from BMKG -Meteorology, Climatology, and Geophysics Agency

## HOW IT WORKS ?

This package uses beautifllsoup4 and a request which will produce a jSON file output that is ready to be used for web 
or mobile applications



## HOW to use?

paste this code to file main.py

"""
import gempaterkini

if __name__ == '__main__':
     result = gempaterkini.exstrasi_data()
     gempaterkini.tampilkan_data(result)
"""

## this code i use oop 
"""
from gempaterkini.gempaUPDATE import gempaTerkini

if __name__ == '__main__':
    gempa_indonesia = gempaTerkini("https://bmkg.go.id")
    print('Deskripsi class gempa indonesia', gempa_indonesia.description)
    gempa_indonesia.run()
"""
