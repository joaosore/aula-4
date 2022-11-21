
import requests
import yaml
import json
import math

from classes.sqlite import SQLITE

class API_IEEE:
  
  def __init__(self, url, path, key, max_records, search, operator, table, page):
    self.url = url
    self.path = path
    self.key = key
    self.max_records = max_records
    self.search = search
    self.operator = operator
    self.table = table
    self.page = page

    with open('config.yaml', 'r') as file:
      config = yaml.safe_load(file)
      self.core = config['data']

  def start_record(self, total_records):
    pages = math.ceil(int(total_records) / int(self.max_records))
    return pages

  def querytext(self):
    arr = len(self.search)

    querytext = ""
    if(arr == 0):
      raise Exception("Não foi informado um texto para pesquisa")

    if(arr >= 1):
      for text in self.search:
        if(self.search.index(text) != 0):
          querytext = querytext + " " + self.operator + " "

        querytext = querytext + text
    
    return querytext

  def payload(self, start_record = 1):
    return {
      "querytext": self.querytext(),
      "apikey": self.key,
      "max_records": self.max_records,
      "start_record": start_record
    }

  def getUrl(self, page, pages):
    print(f"Extraindo página {page} de {pages}: IEEE")
    r = requests.get(url = self.url + self.path, params = self.payload(total_records = page))
    data = r.json()

    # self.save(data = articles)
    with open(f'./raw/IEEE/page_{page}.json', 'w+', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)

  def authors(self, data):
    authors = ""
    for x in data:
      if(data.index(x) != 0):
        authors = authors + ", "

      authors = authors + x['full_name']

    return authors

  def filter_columns(self, data):
    data_format = {}
    for x in self.core:
        if x in data:
          data_format[x] = data[x]
        else:
          if(x == 'author'):
            data_format[x] = self.authors(data['authors']['authors'])
          elif(x == 'year'):
            data_format[x] = data['publication_year']
          elif(x == 'address'):
            # data_format[x] = data['conference_location']
            data_format[x] = ""
          elif(x == 'url'):
            data_format[x] = data['html_url']
          elif(x == 'booktitle'):
            data_format[x] = data['publication_title']
          elif(x == 'pages'):
            data_format[x] = f"{data['start_page']},{data['end_page']}"
          else:
            data_format[x] = ''
    
    return data_format

  def extract(self):
    r = requests.get(url = self.url + self.path, params = self.payload())
    data = r.json()
    total_records = data['total_records']
    
    pages = self.start_record(total_records)

    page = self.page
    while(page <= pages):
      self.getUrl(page, pages)
      page = page + 1;

  def query(self, values):
    columns = ', '.join(values.keys())
    placeholders = ', '.join('?' * len(values))
    query = 'INSERT INTO {} ({}) VALUES ({})'.format(self.table, columns, placeholders)
    values = [int(x) if isinstance(x, bool) else x for x in (values.values())]
    return [query, values]

  def save(self, data):
    i = 0
    list_query = []
    list_values = []
    while(i < len(data)):
      [query, values] = self.query(self.filter_columns(data[i]))
      list_query.append(query)
      list_values.append(values)
      i = i + 1

    con = SQLITE(db = "ieee.db", table = self.table)
    con.insert(query = list_query, values = list_values)