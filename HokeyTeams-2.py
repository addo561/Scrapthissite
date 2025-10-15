import csv
import requests
from bs4 import BeautifulSoup
import time
import datetime
from pathlib import Path

def get_data(url: str,save=False):
    """Scrape team stats (name, year, wins, losses, win%) from a paginated site.

    Parameters:
        url : the website  you want to scrape
        save : to save data in file format(csv)

    Returns:
        list: [[title], [team_name, year, wins, losses, win%], ...]
    """
    res = requests.get(url) # get access to  website
    if res.status_code == 200: #check if website  is scrappable
        print('You can scrape ✅')

    soup = BeautifulSoup(res.text, 'html.parser') #set res content as text  and pass in the parser
    title = soup.find('h1').find(string=True, recursive=False).strip() #get first text from this tag ,dont go throw rest of the tags
    data = [title]
    classes = ['name', 'year', 'wins', 'losses', 'pct text-success'] #things to scrap
    page_id = 2  # pagination counter

    while url:
        time.sleep(0.5)  # time to scrap next page (intervals)
        print(f'Extracting data from {url}')
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        # find all team rows
        for t in soup.find_all('tr', class_='team'):
            row = [t.find(class_=c).get_text().strip() if t.find(class_=c) else None for c in classes] #for each  class extract text and  remove leading  and trailing spaces
            if all(row):
                row[2], row[3], row[4] = int(row[2]), int(row[3]), float(row[4])  # cast values(change to a preferrred datatype)
                data.append(row)

        # check for "Next" button
        next_page = soup.find('a', {'aria-label': 'Next'})
        url = f'https://www.scrapethissite.com/pages/forms/?page_num={page_id}' if next_page and 'disabled' not in next_page.get('class', []) else None
        page_id += 1 # increase id to change page number

        #store data  in csv file
    if save:
      dir = Path(__file__).resolve().parent
      output_dir = dir/'output.csv'
      with output_dir.open('w',newline='')  as f: # open file as f and  write to it (file name = output.csv)
          title = 'Name Year Wins Losses Win%' # set column names
          writer = csv.writer(f) # save  data(col names) in  file (write  to  it )
          writer.writerow(title.split()) #split each  individual string to lists
          writer.writerows(data[1:])#save rest of data excluding title or col names
      print(f'Saved data as csv in  {output_dir}')    

    return data
if __name__ == '__main__':
  url = 'https://www.scrapethissite.com/pages/forms/?page_num=1'
  data = get_data(url,save=True)

