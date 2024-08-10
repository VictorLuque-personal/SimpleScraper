from Code import scraper, filtering, storage_manager
import os.path as path

if __name__ == "__main__":
  
  # Create the scraper object
  scraper_obj = scraper.ScraperTechnicalTest()
  filterer = filtering.Filterer()
  
  # Get the data
  data = scraper_obj.get_data()
  filtered_data = filterer.filtering_data(data, filtering.Filterer.FilterCriteria.FIRST)
  filtered_data = filterer.filtering_data(data, filtering.Filterer.FilterCriteria.SECOND)
  
  db_path = path.join(path.dirname(path.abspath(__file__)), 'Storage', 'storage.db')
  
  storage = storage_manager.StorageManager(db_path)
  storage.save_data(filtered_data, filtering.Filterer.FilterCriteria.SECOND.value)
  print(storage.get_last_query())
  storage.close_connection()
