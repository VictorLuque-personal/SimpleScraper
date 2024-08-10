from Code import scraper, filtering, storage_manager
import os.path as path
import argparse

if __name__ == "__main__":
  
  parser = argparse.ArgumentParser(prog="Simple Web Scraper",
            description="A web scraper for Hacker News that filters with two criteria",)
  
  parser.add_argument('--filter', type=int,
                      help="""Can be 1 or 2 to choose the filter criteria. If the argument is not used, the search will not have a criteria""")
  parser.add_argument('--save', type=bool, help="If used, saves the query in the database")
  parser.add_argument('--show', type=bool, help="If used, gets the last query in the database and shows it in the console")
  parser.add_argument('--path', type=str, default = path.join(path.dirname(path.abspath(__file__)), 'Storage', 'storage.db'),
                      help="The path for the database to save the data. The deafult is the one in the Storage folder")
  
  args = parser.parse_args()
  
  # Create the scraper object
  scraper_obj = scraper.ScraperTechnicalTest()
  filterer = filtering.Filterer()
  
  # Get the data
  data = scraper_obj.get_data()
  
  if args.filter == 1:
    print("hola")
    data = filterer.filtering_data(data, filtering.Filterer.FilterCriteria.FIRST)
  elif args.filter == 2:
    print("hola2")
    data = filterer.filtering_data(data, filtering.Filterer.FilterCriteria.SECOND)
  
  storage = storage_manager.StorageManager(args.path)
  
  if args.save:
    storage.save_data(data, filtering.Filterer.FilterCriteria.SECOND.value)
  
  if args.show:
    print(len(storage.get_last_query()))
  
  storage.close_connection()
