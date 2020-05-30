# Double check how this is going to work in AWS
import sys
sys.path.append(r'C:\Git\kw\Packages')

from RealEstate.WebScraping import WebScraping

def main():
    print('Start')
    app = WebScraping()
    app.output_file = open(app.output_file_name,"w+")
    app.read_website(app.main_url)
    app.output_file.close()
    print('End')

if __name__ == '__main__':
    main()