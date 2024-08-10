import requests
from bs4 import BeautifulSoup

# TODO: create a class with the attributes, the init for the url and all of 
# that and a method to get the 30 list of tuples with the info

class ScraperTechnicalTest:
  
  def __init__(self):
    # URL to get the content
    self.url = "https://news.ycombinator.com/"
    # Actually getting the content with GET request
    self.response = requests.get(self.url)
    # I will be using BeautifulSoup that I googled it is currently one of the most 
    # used scrapers and it is simple
    self.scraper = BeautifulSoup(self.response.content, 'lxml')
  
  def get_data(self):
    """ Gets the data needed for the exercise in a dictionary with the ranks as
    keys and the rest of data as value """
    
    def get_prefix_number(s: str):
      """ Gets the number placed at the beginning of a string """
      idx = 0
      
      if s == "discuss": # No comments yet
        return idx
      
      for c in s:
        if not c.isdigit():
          break
        idx += 1
      
      return int(s[:idx])
    
    # All the information I want is placed in the table that you can follow with 
    # the next find expression. I would find it by some attribute but it does not 
    # have any :/
    table = self.scraper.find('table', attrs={'id': 'hnmain'}).find_all('tr', recursive=False)[2].find('table')
    # Just in case it fails
    if table == None:
      raise ValueError("Could not find the table of news")
    
    # the next is a pity due to the table organization, and I need two different 
    # queries to get all the information
    title_rows = table.select('tr.athing')
    points_comments_rows = table.select('td.subtext')
    
    # due to the divided query results I want rely on the order but separate the 
    # searches by id of the elements to be more safe creating the data (but less 
    # efficient consequently)
    data = {} # Initialize to a dictionary
    for row in title_rows:
      row_id = row['id']
      rank = int(get_prefix_number(row.find('span', class_="rank").text))
      # the first direct child of the span found that is an 'a' has the text of
      # the title:
      title = next(row.find('span', class_="titleline").children).text
      score = None
      comments = None
      for row in points_comments_rows:
        aux = row.find('span', attrs={'id':"score_"+row_id})
        if aux != None:
          score = get_prefix_number(aux.text)
          # This is a mess, there are two links with the same href and no 
          # distinctive attributes (they are identical except for the text of 
          # course) and I want the second one
          comments = get_prefix_number(row.find_all('a', attrs={'href':"item?id="+row_id})[1].text)
      
      data[rank] = (title, score if score != None else 0, comments if comments != None else 0)
    
    return data

# TODO: test to know if the length of both row varaibles is the same, and to 
# test if the ids (e.g. you can find it on the scores and for the rows it is 
# the id of the element itself)
