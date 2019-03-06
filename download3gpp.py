# author : Mohit Narula
# add the function of Incremental download The latest 3gpp protocol by huiwu

from urllib.request import urlopen, Request
import sys
import re
import zipfile
import os
import subprocess
try:
    import requests
except ImportError or ModuleNotFoundError:
    where_is_python = sys.executable
    where_is_python_re = re.match(r'(.*)\\(.*)', where_is_python)
    os.chdir(where_is_python_re.group(1))
    p2 = subprocess.Popen('pip install requests')
    p2.wait()
    p2.kill()
    import requests

try:
    from bs4 import BeautifulSoup as bs
except ModuleNotFoundError or ImportError:
    os.chdir(where_is_python_re.group(1))
    p1 = subprocess.Popen('pip install beautifulsoup4')
    p1.wait()
    p1.kill()
    from bs4 import BeautifulSoup as bs


spec_url_list = ["http://www.3gpp.org/ftp/Specs/latest/Rel-16/38_series/",
            "http://www.3gpp.org/ftp/Specs/latest/Rel-16/37_series/",
            "http://www.3gpp.org/ftp/Specs/latest/Rel-15/38_series/",
            "http://www.3gpp.org/ftp/Specs/latest/Rel-15/37_series/"]

where_to_save = "C:\\temp2"
spec_base_url = "http://www.3gpp.org"
pip_file_path = "https://bootstrap.pypa.io/get-pip.py"


def specter():
    '''
    This is the actual brains of the code,
    3GPP.org is scraped for 38 series specs
    all the specs are downloaded and unzipped
    to hardcoded C:\temp2 location
    '''
    alreadyexistlist = []

    for item in os.listdir(where_to_save):
        if item.endswith(".zip"):
            alreadyexistlist.append(item)

    for spec_url in spec_url_list:
        req1 = Request(spec_url, headers={'User-Agent': 'Chrome'})
        html_obj = urlopen(req1)
        html_obj_read = html_obj.read()
        soup = bs(html_obj_read, 'html.parser')
        a_link_list = [link for link in soup.find_all("a")]

        print("\nDownloading all 3GPP 5G NR specs from {}.. Please Wait..!".
            format(spec_url))

        if not os.path.exists(where_to_save):
            os.makedirs(where_to_save)

        for item in a_link_list[1:]:
            a_link_re = re.match(r'<a href="(.*)">(.*)</a>',
                                str(item))
    
            file_re = re.match(r'(.*)/(.*)', str(a_link_re.group(1)))

            file = file_re.group(2)

            findfile = False
            for item in alreadyexistlist:

                if item == file:
                    findfile = True
                    continue

                item_re =  re.match(r'(\d{4,6})((?:-\d{0,3})*)-(\w*)\.zip', str(item))
                file2_re = re.match(r'(\d{4,6})((?:-\d{0,3})*)-(\w*)\.zip', str(file))
                print(item)
                print(file)
                if file2_re.group(1) == item_re.group(1) and file2_re.group(2) == item_re.group(2):
                    if file2_re.group(3) > item_re.group(3):
                        alreadyexistlist.remove(item)
                        findfile = False
                        continue
                    else :
                        findfile = True

            if findfile == False:
                print("download: ",file)
                r = requests.get(spec_base_url+a_link_re.group(1))
                os.chdir(where_to_save)
                with open(file_re.group(2), 'wb') as outputfile:
                    outputfile.write(r.content)
                alreadyexistlist.append(file) 

    print("\nAll specs are downloaded @ {}\n."
          "\nHappy Reading..!".format(where_to_save))


if __name__ == "__main__":
    specter()

