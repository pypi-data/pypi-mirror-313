
import requests
from bs4 import BeautifulSoup
from docutils.nodes import description

from gempaterkini import exstrasi_data, tampilkan_data

"""
method =  fungsi/function
field/atribut = variabel
constructor = method yang dipanggil pertama kali saat objek diciptakan gunakan
untuk mendeklarasikan semua field pada class ini

"""

class bencana :
    def __init__(self, url, description ):
        self.description = description
        self.result = None
        self.url = url
    def scraping_data(self):
        pass

    def tampilkan_data(self):
        pass
    def tampilkan_keterangan(self):
        print(f'under construction', (self.description))

    def run(self):
        self.scraping_data()
        self.tampilkan_data()





class gempaTerkini(bencana):
    def __init__(self, url):
        super(gempaTerkini, self).__init__(url,'to get the latest earthquake in indonesia from BMKG.go.id')



    def scraping_data(self):  # data akan disimpan pada reprpsitory pypi
        try:
            content = requests.get(self.url)
        except Exception:
            return None

        if content.status_code == 200:
            # print(content.text)
            soup = BeautifulSoup(content.text, 'html.parser')
            # print(soup.prettify())
            result = soup.find('span', {'class': 'waktu'})
            result = result.text.split(', ')
            tanggal = result[0]
            waktu = result[1]

            result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            result = result.findChildren('li')

            i = 0
            magnitude = None
            kedalaman = None
            koordinat = None
            ls = None
            bt = None
            lokasi = None
            dirasakan = None

            for res in result:
                print(i, res)
                if i == 1:
                    magnitude = res.text
                elif i == 2:
                    kedalaman = res.text
                elif i == 3:
                    koordinat = res.text.split(' - ')
                    ls = koordinat[0]
                    bt = koordinat[1]
                elif i == 4:
                    lokasi = res.text
                elif i == 5:
                    dirasakan = res.text

                i = i + 1

            hasil = dict()
            hasil['tanggal'] = tanggal
            hasil['waktu'] = waktu
            hasil['magnitude'] = magnitude
            hasil['kedalaman'] = kedalaman
            hasil['koordinat'] = {'ls': ls, 'bt': bt}
            hasil['lokasi'] = lokasi
            hasil['dirasakan'] = dirasakan
            self.result = (hasil)
        else:
            return None

    def tampilkan_data(self):
        if self.result is None:
            print("tidak bisa menemukan gempa terkini")

            return
        print("Gempa Terakhir berdasarkan BMKG")
        print(f"Tanggal = {self.result['tanggal']}")
        print(f"Waktu = {self.result['waktu']}")
        print(f"Magnitudo = {self.result['magnitude']}")
        print(f"kedalaman = {self.result['kedalaman']}")
        print(f"koordinat : LS = {self.result['koordinat']['ls']}, BT = {self.result['koordinat']['bt']}")
        print(f"lokasi = {self.result['lokasi']}")
        print(f"Dirasakan = {self.result['dirasakan']}")

class banjirTerkini(bencana):
    def __init__(self, url):
        super(banjirTerkini, self).__init__(url, 'not yet implemented')


if __name__ == '__main__':
    gempa_indonesia = gempaTerkini("https://bmkg.go.id")
    print(f'Aplikasi Utama menggunakan package yang memiliki deskripsi {gempa_indonesia.description}')
    gempa_indonesia.tampilkan_keterangan()
    gempa_indonesia.run()

    banjir_indonesia = banjirTerkini("not yet")
    banjir_indonesia.tampilkan_keterangan()
    banjir_indonesia.run()


    daftar_bencana = [gempa_indonesia, banjir_indonesia]
    print('\n List Bencana')
    for ben in daftar_bencana:
        ben.tampilkan_keterangan()


    # gempa_dunia = gempaTerkini("https://bmkg.go.id")
    # print('Deskripsi class gempa dunia', gempa_dunia.description)
    # gempa_dunia.run()
