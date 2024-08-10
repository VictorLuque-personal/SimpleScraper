import re
import unittest
import sys
import os.path as path
from bs4 import BeautifulSoup

sys.path.insert(0, path.join(path.dirname(path.dirname(path.abspath(__file__))), 'Code'))

import scraper, filtering, storage_manager

# This is duplicated code due to the local scope of the original function
def get_prefix_number(s: str):
    """ Gets the number placed at the beginning of a string """
    idx = 0
    
    if s == "discuss": # No comments yet
      return idx
    
    for c in s:
      if not c.isdigit():
        break
      idx += 1
    
    if idx == 0:
      raise ValueError("The string does not start with a number")
    
    return int(s[:idx])

def has_more_than_5_words(s: str):
  """ Returns true if and only if the string has more than 5 words. Excluding
  symbols """
  
  # I assume that what you meant in the statement of the exercise is that I 
  # have to exclude 1 length strings that are symbols. I apologize if it was
  # not the meaning you wrote in "consider only the spaced words and exclude 
  # any symbols".
  clean_str = re.sub(r'[^\w\s]', '', s).split()
  # regular expressions library gives me the \w to filter words, so in human
  # words: this expression substitutes by a blank '' all the things that are
  # NOT words \w or whitespaces \s. I explain it just in case

  return len(clean_str) > 5

class ScraperTesting(unittest.TestCase):
  """ I am writing here all the unit tests for the scraper """
  
  def test_scraper_init_and_eq(self):
    scraper_object = scraper.ScraperTechnicalTest()
    self.assertEqual(scraper.ScraperTechnicalTest(), scraper_object)
    self.assertEqual(scraper_object.url, "https://news.ycombinator.com/")
  
  def test_scraper_local_prefix_num(self):
    self.assertEqual(get_prefix_number("102fjbnsdf"), 102)
    self.assertEqual(get_prefix_number("discuss"), 0)
    with self.assertRaises(ValueError):
      get_prefix_number("bnsdf")
    with self.assertRaises(ValueError):
      get_prefix_number("bns7df")
    self.assertEqual(get_prefix_number("4 5 6 7 8"), 4)
    self.assertEqual(get_prefix_number("34."), 34)
  
  def test_scraper_get_data(self):
    html = ""
    with open("html.txt", "r") as f:
      html = f.read()
    # This is the html of Hacer News of 10th august at 7pm CEST
    
    scraper_obj = scraper.ScraperTechnicalTest()
    
    self.assertEqual(len(scraper_obj.get_data()), 30)
    
class FilteringTesting(unittest.TestCase):
  """ Unit tests for the filterer class """
  
  def test_more5_words(self):
    self.assertEqual(has_more_than_5_words("This is - a self-explained example"), False)
    self.assertEqual(has_more_than_5_words(" - % / sjd hello three"), False)
    self.assertEqual(has_more_than_5_words("() 4 words has this"), False)
    self.assertEqual(has_more_than_5_words("() 6 words has this example string"), True)
    self.assertEqual(has_more_than_5_words("This one, instead, has exactly 7 words"), True)
    
  def test_filter_one(self):
    data = { 1: ("first title", 50, 5), 2: ("second title that is very large", 150, 1),
            3: ("third title shorter than last", 100, 7), 4: ("fourth title is going to be the larger in number of words", 200, 10),
            }
    
    filterer = filtering.Filterer()
    self.assertEqual(len(filterer.filtering_data(data,filtering.Filterer.FilterCriteria.FIRST)), 2)
    self.assertEqual(len(filterer.filtering_data(data,filtering.Filterer.FilterCriteria.SECOND)), 2)
    self.assertEqual(list(filterer.filtering_data(data,filtering.Filterer.FilterCriteria.FIRST))[0], 4)
    self.assertEqual(list(filterer.filtering_data(data,filtering.Filterer.FilterCriteria.SECOND))[0], 3)
  
if __name__ == "__main__":
  unittest.main()
