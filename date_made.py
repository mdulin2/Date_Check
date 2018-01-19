#Trademarked by Maxwell Dulin

import requests
import re
from string import punctuation
from libwayback import WaybackCrawler, WaybackRetriever

#Takes out all html tags from the webpage
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, ' ', raw_html)
  return cleantext

#Takes off all of the punctuation out of the string
def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

#does the basic parsing for the page
def setup_page(url):
    source = str(url.encode('UTF-8'))
    r = requests.get(source)
    site = str(r.text.encode('UTF-8'))
    #site = "Jan 05 2017"
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
                        print before, word, after,
                        date_list.append((str(before),str(word),str(after)))

                #i.e: Jan 4 2017
                elif(after.isdigit() and (len(after) ==1 or len(after) == 2 or len(after) == 4)):

                    possible_year = site[word_index+2]
                    if(possible_year.isdigit()):
                        #print word,after,possible_year
                        date_list.append((str(word),str(after),str(possible_year)))
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

#reformats the date with the number scheme to be tested
def reformat_date(dates):
    format_date = list()
    for item in dates:
        division = item.split("/")
        format_date.append((division[0],division[1], division[2]))
    return format_date

#could do some checks based on dates...
def date_finder(url_fun,month_dict):

    #two modes for input: html page and pdf
    #pdf...
    dates1 = get_date_alpha(url_fun,month_dict)
    dates2 = get_date_num(url_fun)
    dates2 = reformat_date(dates2)
    # will be the wayback machine here at some point!
    # the wayback machine will be able to verify if the date is correct.
    #dates2 = [("1","2","2017"),("1","2","2017"),("1","2","2017")]
    dates1,dates2 = fix_dates(dates1,dates2)
    if(len(dates1) < 2):
        counter = len(dates1)
    else:
        counter = 2

    print
    print "How do these dates look to you?"
    for i in range(counter):
        print dates1[i]

    if(len(dates2) < 2):
        counter = len(dates2)
    else:
        counter = 2
    for i in range(counter):
        print dates2[i]

    print "Go check the page for these dates! One of these is likely!"

#Returns two lists, each has completely legal dates.
def fix_dates(stack1,stack2):
    dates1 = list()
    dates2 = list()
    for date in stack1:
        if(is_valid_date(date,1)):
            dates1.append(date)

    for date in stack2:
        if(is_valid_date(date,2)):
            dates2.append(date)
    return dates1,dates2

#Checks to see if the date looks valid for a date on the website/article
def is_valid_date(date,format_type):
    """
    format_type: (1) for the string dates(May 26,2017)
    format_type: (2) for the integer datess(1/2/1222)
    """

    #for the values with strings
    spot1 = date[0] #day/month
    spot2 = date[1] #day/month
    spot3 = date[2] #year

    #string dates
    if(format_type == 1):
        if(ord(spot1[0]) >= ord('A') and ord('z') >= ord(spot1[0]) ):
            spot2 =int(spot2)
            if(spot2 > 31 or spot2 < 1):
                return False

        elif(ord(spot2[0]) >= ord('A') and ord('z') >= ord(spot2[0])):
            spot1 = int(spot1)
            if(spot1 > 31 or spot1 < 1):
                return False
        else:
            return False
    #integer dates
    elif(format_type == 2):
        spot1 = int(spot1)
        spot2 = int(spot2)
        if(spot1 <= 12 and spot1 >= 1):
            if(spot2 > 31):
                return False
        elif(spot2 <= 12 and spot2 >=1):
            if(spot1 > 31):
                return False
        else:
            return False

    #Checks to see if the year is valid
    spot3 = int(spot3)
    if((spot3 <= 2019 and spot3 >= 1939) or
        (spot3 <= 19 and spot3 >= 00) or
        (spot3 <= 99 and spot3 >40)):
        return True
    return False
    #for the values with just values


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
        #print find_date(dates)
        assert(len(dates) > 0)
    print("Finish Tests!")

#Wil have a working wayback machine API in order to find the first date that this
#website page appeared on the internet.
def wayback_view(url_fun):
    pass

def main():

    #need to remake this dictionary.
    month_dict = dict()
    month_dict["January"] = ("Jan",31,1)
    month_dict["February"] = ("Feb",29,2)
    month_dict["March"] = ("Mar",31,3)
    month_dict["April"] = ("Apr",30,4)
    month_dict["May"] = ("May",31,5)
    month_dict["June"] = ("Jun",31,6)
    month_dict["July"] = ("Jul",31,7)
    month_dict["August"] = ("Aug",31,8)
    month_dict["September"] = ("Sept",30,9)
    month_dict["Sep"] = ("Sep",30,13)
    month_dict["October"] = ("Oct",31,10)
    month_dict["November"] = ("Nov",30,11)
    month_dict["December"] = ("Dec",31,12)


    #print(is_valid_date(['May','1','00'],1))
    #print(get_date_num('http://www.vh1.com/shows/americas-next-top-model'))
    #test_urls(month_dict)
    #test_urls(month_dict)
    url = str(raw_input("Give me an url that I should check: "))
    #url = "https://www.youtube.com/watch?v=r33bH3Jioq8"
    date_finder(url,month_dict)


main()
