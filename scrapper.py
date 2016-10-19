import nltk
import enchant
from bs4 import BeautifulSoup
import urllib
import re
from collections import Counter
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

dictionary = enchant.Dict("en_US")
list_of_valid_english_words = []
testimonials_wordsList_lower = []
list_of_nouns = []

url = urllib.urlopen('http://www.profittools.net/testimonials/').read()
soup = BeautifulSoup(url, 'html.parser')
testimonials = soup.findAll('blockquote')
testimonials_Unicode = unicode.join(u'\n',map(unicode,testimonials))
# Removing the tags and also converting Unicode strings to regular strings
testimonials_String = re.sub('<[A-Za-z\/][^>]*>', '', testimonials_Unicode.encode('ascii', 'ignore'))
# Converting it to a list of words
testimonials_wordsList = re.compile('\w+').findall(testimonials_String)

for word in testimonials_wordsList:
    testimonials_wordsList_lower.append(word.lower())

for word in testimonials_wordsList_lower:
    if dictionary.check(word):
        list_of_valid_english_words.append(word)

text = nltk.Text(list_of_valid_english_words)
list_of_tagged_tuples = nltk.pos_tag(text)

for tuples in list_of_tagged_tuples:
    if tuples[1] == 'NN':
        list_of_nouns.append(tuples[0])

list_with_frequencies = Counter(list_of_nouns)

most_frequently_used_noun = list_with_frequencies.most_common(1)[0][0]

print "The most frequently used noun is " + most_frequently_used_noun

# Using selenium to find the no of articles returned by the most frequently used noun

browser = webdriver.Firefox()
browser.get('http://www.profittools.net/testimonials/')
search_field_query = most_frequently_used_noun
search_box_id = 's'
search_button_path = "//input[@value='Search']"

search_field_element = WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_id(search_box_id))
search_button_element = WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_xpath(search_button_path))

search_field_element.clear()
search_field_element.send_keys(search_field_query)
search_button_element.click()

the_results_string = browser.find_element_by_xpath("//*[@id='article-content-narrow']/h1")
unicode_to_string_results = the_results_string.get_attribute('innerHTML').encode('ascii', 'ignore')

results = int(filter(str.isdigit, unicode_to_string_results))

browser.close()

print "The no of articles returned by the search are " + str(results)