import re
from enum import Enum

class Filterer():
  
  class FilterCriteria(Enum):
    FIRST = 1
    SECOND = 2
  
  def filtering_data(self, data: dict, criteria: FilterCriteria):
    """ Filter entries of the dictionary with the chosen filter criteria. Being
    the first and the second criteria of the exercise statement """
    
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
  
    def sort_criteria_first(elem):
      if elem[1][2] == None: # For the non commented yet
        return 0
      return elem[1][2] # the number of comments
    
    def sort_criteria_second(elem):
      if elem[1][1] == None: # For the non scored yet
        return 0
      return elem[1][1] # the score
    
    filtered_data = []
    if (criteria == self.FilterCriteria.FIRST):
      # News with more than 5 words in the title by number of comments
      filtered_data = list(filter(lambda item: has_more_than_5_words(item[1][0]), data.items()))
      filtered_data.sort(reverse=True, key=sort_criteria_first)
      # assuming descendent order
    elif (criteria == self.FilterCriteria.SECOND):
      # News with less than or equal to 5 words in the title by score
      filtered_data = list(filter(lambda item: not has_more_than_5_words(item[1][0]), data.items()))
      filtered_data.sort(reverse=True, key=sort_criteria_second)
      # assuming descendent order
    
    return dict(filtered_data)
