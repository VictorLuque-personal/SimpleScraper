from Code import scraper, filtering, storage_manager

if __name__ == "__main__":
  
  # Create the scraper object
  scraper_obj = scraper.ScraperTechnicalTest()
  filterer = filtering.Filterer()
  
  # Get the data
  data = scraper_obj.get_data()
  filtered_data = filterer.filtering_data(data, filtering.Filterer.FilterCriteria.FIRST)
  print(len(filtered_data))
  filtered_data = filterer.filtering_data(data, filtering.Filterer.FilterCriteria.SECOND)
  print(len(filtered_data))
