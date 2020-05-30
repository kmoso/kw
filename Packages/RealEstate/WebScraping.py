import requests
import bs4
import json
import argparse

class WebScraping(object):
    
    def __init__(self):
        super().__init__()

        self.METROSCUBICOS = 'metroscubicos'
        self.INMUEBLES24 = 'inmuebles24'

        my_parser = argparse.ArgumentParser(description='Real Estate Web scraping')
        my_parser.add_argument('--sts', action='store',
                                        default="metroscubicos",
                                        help='Indica el origen de datos, [' + self.METROSCUBICOS + ', ' + self.INMUEBLES24 + ']')
        my_parser.add_argument('--url', action='store',
                                        default="https://listado.metroscubicos.com/santa-luc%C3%ADa-reacomodo#D[A:santa-luc%C3%ADa-reacomodo]",
                                        help='Indica el url principal de la página')
        my_parser.add_argument('--ofn', action='store',
                                        default="test_m3.txt",
                                        help='Indica el archivo de salida')
        my_parser.add_argument('--debug',   action='store',
                                            default="N",
                                            help='Mostrar mensajes de debug, [S/N]')
        my_parser.add_argument('--version', action='version', version='%(prog)s 1.0')
        my_parameters = my_parser.parse_args()

        json_file_name = 'ws_parameters.json'
        self.source_to_scrape = my_parameters.sts
        self.main_url = my_parameters.url
        self.root_url = my_parameters.url[0:my_parameters.url.find("/",9)]
        self.output_file_name = my_parameters.ofn
        self.debug = my_parameters.debug

        # open json file to get page ID and token
        with open(json_file_name, 'r') as f:
            data = json.load(f)

#        self.main_url = data['app']['sources'][source_to_scrape]['main_url']
#        self.root_url = data['app']['sources'][self.source_to_scrape]['root_url']
#        self.output_file_name = data['app']['sources'][source_to_scrape]['output_file_name']
#        self.debug = data['app']['sources'][source_to_scrape]['debug']
        self.delimiter = data['app']['delimiter']
        
        if self.debug == 'Y':
            print('In WebScraping')
            print(self.main_url)
            print('Parameters')
            print(my_parameters)
            print(self.root_url)
            
    def write_file(self, p_line):
        self.output_file.write(p_line + "\n")

    def next_page(self, p_soup):
        new_url = 'None'
        if self.source_to_scrape == self.METROSCUBICOS:
            pag_container = p_soup.find_all("a", class_="andes-pagination__link prefetch")
            if self.debug == 'Y':
                print('Type: ' + str(type(pag_container)) + ' with ' + str(len(pag_container)) + ' elements')
            for item in pag_container:
                new_url = item.get('href')
            if self.debug == 'Y':
                print(new_url)
        elif self.source_to_scrape == self.INMUEBLES24:
            pag_container = p_soup.find_all("li", class_="pag-go-next")
            if self.debug == 'Y':
                print('Type: ' + str(type(pag_container)) + ' with ' + str(len(pag_container)) + ' elements')
            for item in pag_container:
                new_url = self.root_url + item.findChild("a")['href']
        return new_url
    
    def get_url(self, p_data_links, p_id, p_initial_id):
        item_url = p_data_links[p_id-p_initial_id]['href']
        return item_url

    def read_website(self, p_url):
        if self.debug == 'Y':
            print('In read_website')
        
        url_to_search = p_url
        k = 0 # To manage the counter accross pages
        prices_list = list()
        
        if self.source_to_scrape == self.METROSCUBICOS:
            line = "Id" + self.delimiter + "Moneda" + self.delimiter + "Precio" + self.delimiter + "Dirección" + self.delimiter + "Tipo" + self.delimiter + \
            "M2" + self.delimiter + "URL"
        elif self.source_to_scrape == self.INMUEBLES24:
            line = "Id" + self.delimiter + "URL" + self.delimiter + "Descripción" + self.delimiter + "Precio" + self.delimiter + \
            "Terreno" + self.delimiter + "Construcción" + self.delimiter + "Recámaras" + self.delimiter + \
            "Baños" + self.delimiter + "Estacionamiento"
        self.write_file(line)
        
        while url_to_search != 'None':
            print('Searching ' + url_to_search)
            page = requests.get(url_to_search)
            soup = bs4.BeautifulSoup(page.content, 'html.parser')
            if self.source_to_scrape == self.METROSCUBICOS:
                data_block = soup.find_all("div", class_="item__info")
                data_links = soup.find_all("a", class_="item__info-link")
                if self.debug == 'Y':
                    print('data_block type: ' + str(type(data_block)) + ' with ' + str(len(data_block)) + ' elements')
                    print('data_links type: ' + str(type(data_links)) + ' with ' + str(len(data_links)) + ' elements')

                for i, item in enumerate(data_block):
                    prices = item.find_all("span", class_="price__symbol")
                    pricev = item.find_all("span", class_="price__fraction")
                    title = item.find_all("div", class_="item__title")
                    htype = item.find_all("p", class_="item__info-title")
                    descr = item.find_all("div", class_="item__attrs")
                    item_url = self.get_url(data_links, i+k, k)
                    line = str(i+k+1) + self.delimiter + prices[0].contents[0] + self.delimiter + pricev[0].contents[0] + self.delimiter + title[0].contents[0] + self.delimiter + htype[0].contents[0] + self.delimiter + descr[0].contents[0] + self.delimiter + item_url
                    self.write_file(line)

                    if self.debug == 'Y':
                        print(f'{str(i+k+1)} {self.delimiter} {prices[0].contents[0]} {self.delimiter} {pricev[0].contents[0]} {self.delimiter} {title[0].contents[0]} {self.delimiter} {htype[0].contents[0]} {self.delimiter} {descr[0].contents[0]} {self.delimiter} {item_url}')
            elif self.source_to_scrape == self.INMUEBLES24:
                data_block = soup.find_all("div", class_="posting-info")
                data_links = soup.find_all("a", class_="go-to-posting")
                data_prices = soup.find_all("span", class_="first-price")
                
                if self.debug == 'Y':
                    print('data_block type: ' + str(type(data_block)) + ' with ' + str(len(data_block)) + ' elements')
                    print('data_links type: ' + str(type(data_links)) + ' with ' + str(len(data_links)) + ' elements')
                    print('data_prices type: ' + str(type(data_prices)) + ' with ' + str(len(data_prices)) + ' elements')

                for i, item in enumerate(data_prices):
                    item_price = item.text
                    prices_list.append(item_price)
                    
                for i, item in enumerate(data_block):
                    item_anchor = item.find_all("a", class_="go-to-posting")
                    item_features_ul = item.find_all("ul", class_="main-features go-to-posting")
                    item_description_div = item.find_all("div", class_="posting-description go-to-posting")
                    item_url = self.get_url(data_links, i+k, k)
                    line = str(i+k+1) + self.delimiter + self.root_url + item_anchor[0]["href"] + self.delimiter + \
                            item_description_div[0].text.strip().replace("\t"," ") + self.delimiter + \
                            prices_list[i] + self.delimiter + item_features_ul[0].text.strip().replace("\n",self.delimiter)
                    self.write_file(line)

                    if self.debug == 'Y':
                        print(f'{str(i+k+1)} {self.delimiter} {self.root_url + item_anchor[0]["href"] } {self.delimiter} {item_description_div[0].text.strip()} {self.delimiter} {item_features_ul[0].text} {self.delimiter}')

            url_to_search = self.next_page(soup)
            k = i + k + 1
