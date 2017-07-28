#!/usr/bin/env python

from optparse import OptionParser
from lxml import html
import requests
import sys

def parse_arguments():
    parser = OptionParser(usage="usage: %prog URL [word]")
    (options, args) = parser.parse_args()
    if (len(args) < 1 or len(args) > 2):
        parser.error("wrong number of arguments")
    return args

def connect_site(url):
    #page = requests.get('https://www.bose.com/en_us/careers.html')
    try:
        page = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    return page


#given a HTML/XML doc/tree this method counts the num occurences of the word
def count_words(html, word):
    # Could not get this to work
    #search_string = '//span[contains(@class, "bose-navBarFoldout2016__menuitemLabel") and text() = "speakers"]'
    #list = html.xpath(search_string)
    #span_count = len(list)

    search_string = "//a[contains(@href,\"%s\")]/@href" % word
    list = html.xpath(search_string)
    href_count = len(list)
    #print(list)
    #print("href_count = ", href_count)
    return href_count


def main():
    total_word_count = 0
    args = parse_arguments()
    if len(args) == 1:
        url = args[0]
        word = 'speakers'
    elif len(args) == 2:
        url = args[0]
        word = args[1]
    # url is something like https://www.bose.com/en_us/careers.html
    page = connect_site(url)
    tree = html.fromstring(page.content)
    total_word_count += count_words(tree, word)
    print("The word occurs: ", total_word_count)
    #print("Total occurences of %s in URL: %s is %d.", word, url, total_word_count)

if __name__ == '__main__':
    main()