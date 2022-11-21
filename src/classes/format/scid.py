
import yaml
import os
import json

from classes.sqlite import SQLITE

class FORMAT_SCID:
  
  def __init__(self, path, db, table):
    self.path = path
    self.db = db
    self.table = table

    with open('config.yaml', 'r') as file:
      config = yaml.safe_load(file)
      self.core = config['data']

  def authors(self, data):

    authors = ""

    if(data != None):
      data = data['author']
      for x in data:
        if(data.index(x) != 0):
          authors = authors + ", "
        
        if type(x) is str:
          authors = authors + x
        else:
          authors = authors + x['$']
    
    return authors

  def fix_columns(self, data):
    data_format = {}

    for col in self.core:
      if col in data.keys():
        data_format[col] = data[col]

    if "prism:doi" in data.keys():
        data_format["doi"] = data['prism:doi']

    if "authors" in data.keys():
        data_format["author"] = self.authors(data['authors'])

    if "prism:volume" in data.keys():
        data_format["year"] = data['prism:volume']
    
    if "prism:publicationName" in data.keys():
        data_format["address"] = data['prism:publicationName']

    if "prism:url" in data.keys():
        data_format["url"] = data['prism:url']

    if "dc:title" in data.keys():
        data_format["booktitle"] = data['dc:title']

    if "start_page" in data.keys():
        data_format["pages"] = f"{data['prism:startingPage']},{data['prism:endingPage']}"
    
    data_format["publisher"] = ""
    data_format["numpages"] = ""
    data_format["keywords"] = ""
    data_format["location"] = ""
    data_format["series"] = ""

    return data_format

  def query(self, values):
    columns = ', '.join(values.keys())
    placeholders = ', '.join('?' * len(values))
    query = 'INSERT INTO {} ({}) VALUES ({})'.format(self.table, columns, placeholders)
    values = [int(x) if isinstance(x, bool) else x for x in (values.values())]

    return [
      query,
      values,
      columns
    ]

  def CountFiles(self):
    files = folders = 0
    for _, dirnames, filenames in os.walk(self.path):
        files += len(filenames)
        folders += len(dirnames)
    return files

  def load(self):
    page = 1
    while (page <= self.CountFiles()):
      with open(str(self.path) + 'page_'+ str(page) +'.json') as f:
        print(f"SCID - Page {page} de {self.CountFiles()}")
        data = json.load(f)
        self.save(data['search-results']['entry'])
        page = page + 1

  def save(self, data):
    i = 0

    list_query = []
    list_values = []
    list_columns = []
    
    while(i < len(data)):
      sql = self.query(self.fix_columns(data[i]))
      list_query.append(sql[0])
      list_values.append(sql[1])
      list_columns.append(sql[2])
      i = i + 1

    con = SQLITE(db = self.db + ".db", table = self.table)
    con.create(query = list_columns[0])

    con.insert(query = list_query, values = list_values)