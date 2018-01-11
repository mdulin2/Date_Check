import requests
import re
from string import punctuation
from libwayback import WaybackCrawler, WaybackRetriever
import pywb

#Tries to use the wayback method to look for the first usage of the page/site
#Under construction...
def last_resort(url_fun):
    crawler = WaybackCrawler("www.sjtu.edu.cn")
    crawler.parse(live=False)

    # The `results` of crawler instance contains a dict data structure with
    # a "year" number being the key and a list of page addresses being the value.

    ret = crawler.results

    # Based on the result of crawler, ie a specific page address, you can use
    # retriever to download and save it in yor file system:

    retriever = WaybackRetriever()

    for year in ret:
        for url in ret[year]:
            retriever.save_page(url, "saved_file")


#Takes out all html tags from the webpage
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, ' ', raw_html)
  return cleantext

#Takes off all of the punctuation out of the string
def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

def setup_page(url):
    source = str(url.encode('UTF-8'))
    r = requests.get(source)
    #site = "t t t Nov 5 '08"
    site = str(r.text.encode('UTF-8'))
    site = cleanhtml(site)
    return site

#The physcial function that gets the date from the webpage
def get_date_alpha(url_fun,month_dict):
    site = setup_page(url_fun)
    site = strip_punctuation(site)
    site = site.split()
    date_list = list()
    for word_index in range(len(site)):
        word = site[word_index]

        #checks to see if the word is a month
        for item in month_dict:
            if(month_dict[item][0] == word or item == word):
                before = fix_number(site[word_index-1])
                after = fix_number(site[word_index+1])

                #ie.: 4 Jan 2017
                if(before.isdigit() and (len(before) == 1 or len(before) == 2 or len(before) == 4)):
                    if(after.isdigit() and (len(after) == 1 or len(after) == 2 or len(after) == 4)):
                        #print before, word, after
                        date_list.append((before,word,after))

                #i.e: Jan 4 2017
                elif(after.isdigit() and (len(after) ==1 or len(after) == 2 or len(after) == 4)):
                    possible_year = site[word_index+2]
                    if(possible_year.isdigit()):
                        #print word,after,possible_year
                        date_list.append((word,after,possible_year))
    return date_list
    """
    Going to need a section here for dates like 1/2/3122/
    Could also do a check on year/day/month ranges
    """


#The the date in a numerical format, if possible.
def get_date_num(url_fun):
    site = setup_page(url_fun)
    #site = "1/2/3  1/4/2019 tttttt"
    match=re.compile(r'(\d+/\d+/\d+)')
    dates = list()
    if(match == None):
        return []
    else:
        for values in re.findall(match,site):
            dates.append(values)
    return dates

#Gets the guess on what the date actually is.
def find_date(date_list):
    if(len(date_list) == 0):
        return "No entries Found..."
    return date_list[0]

#Parses all of the number suffix's out of the dates.
def fix_number(value):
    value = value.replace("st","")
    value = value.replace("nd","")
    value = value.replace("rd","")
    value = value.replace("th","")
    return value

def date_finder(url_fun,month_dict):
    dates1 = get_date_alpha(url_fun,month_dict)
    dates2 = get_date_num(url_fun)
    # will be the wayback machine here at some point!
    # the wayback machine will be able to verify if the date is correct.

    print find_date(dates1)
    print find_date(dates2)
    #print find_date(dates2)

#Check these urls to make sure nothing has been broken!
def test_urls(month_dict):
    print("Running Tests...")
    url_lst = list()
    url_lst.append("https://moxie.org/blog/")
    url_lst.append("https://krebsonsecurity.com/2018/01/microsofts-jan-2018-patch-tuesday-lowdown/")
    url_lst.append("https://www.youtube.com/watch?v=nP0-RWD6WRQ")
    url_lst.append("https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python")

    for url in url_lst:
        dates = get_date_alpha(url,month_dict)
        print find_date(dates)
        assert(len(dates) > 0)
    print("Finish Tests!")

def wayback_view(url_fun):
    #url = "https://web.archive.org/web/*/" + url_fun
    #source = str(url.encode('UTF-8'))
    #r = requests.get(source)
    #site = "t t t Nov 5 '08"
    #site = str(r.text.encode('UTF-8'))
    #site = cleanhtml(site)
    pass
def main():
    month_dict = dict()
    month_dict["January"] = ("Jan",31,1)
    month_dict["February"] = ("Feb",29,2)
    month_dict["March"] = ("Mar",31,3)
    month_dict["April"] = ("Apr",30,4)
    month_dict["May"] = ("May",31,5)
    month_dict["June"] = ("June",31,6)
    month_dict["July"] = ("Jul",31,7)
    month_dict["August"] = ("Aug",31,8)
    month_dict["September"] = ("Sept",30,9)
    month_dict["October"] = ("Oct",31,10)
    month_dict["November"] = ("Nov",30,11)
    month_dict["December"] = ("Dec",31,12)

    wayback_view("google.com")
    #print(get_date_num('http://www.vh1.com/shows/americas-next-top-model'))
    #url = str(raw_input("Give me an url that I should check: "))
    #last_resort("https://moxie.org/blog/")
    #dates = date_finder(url,month_dict)


main()
