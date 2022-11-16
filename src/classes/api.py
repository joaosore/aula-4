
import requests
import sqlite3
import yaml

class API:
  
  def __init__(self, url, path, key, max_records, search, operator):
    self.url = url
    self.path = path
    self.key = key
    self.max_records = max_records
    self.search = search
    self.operator = operator

    with open('config.yaml', 'r') as file:
      config = yaml.safe_load(file)
      self.data = config['data']

  def start_record(self, total_records):
    pages = int(total_records / self.max_records)
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
    r = requests.get(url = self.url + self.path, params = self.payload())
    data = r.json()
    articles = data['articles']

    self.sqlite(data = articles)

  def authors(self, data):
    authors = ""
    for x in data:
      if(data.index(x) != 0):
        authors = authors + ", "

      authors = authors + x['full_name']

    return authors

  def data_format(self, data):
    data_format = {}
    for x in self.data:
        if x in data:
          data_format[x] = data[x]
        else:
          if(x == 'author'):
            data_format[x] = self.authors(data['authors']['authors'])
          elif(x == 'year'):
            data_format[x] = data['publication_year']
          elif(x == 'address'):
            data_format[x] = data['conference_location']
          elif(x == 'url'):
            data_format[x] = data['html_url']
          elif(x == 'booktitle'):
            data_format[x] = data['publication_title']
          elif(x == 'pages'):
            data_format[x] = f"{data['start_page']},{data['end_page']}"
          else:
            data_format[x] = ''
    
    return data_format

  def formartDataToInsert(self, values):
    columns = ', '.join(values.keys())
    placeholders = ', '.join('?' * len(values))
    query = 'INSERT INTO articles ({}) VALUES ({})'.format(columns, placeholders)
    values = [int(x) if isinstance(x, bool) else x for x in (values.values())]
    return [query, values]

  def sqlite(self, data):
    con = sqlite3.connect("ieee.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS articles (author, title, year, isbn, publisher, address, url, doi, abstract, booktitle, pages, numpages, keywords, location, series)")
    i = 0
    while(i < len(data)):
      sql = self.formartDataToInsert(self.data_format(data[i]))
      cur.execute(sql[0], sql[1])
      con.commit()
      i = i + 1

  def connect(self):
    r = requests.get(url = self.url + self.path, params = self.payload())
    data = r.json()
    total_records = data['total_records']
    articles = data['articles']
    
    pages = self.start_record(total_records)
    print(f"Extraindo página 1 de {pages}: IEEE")

    self.sqlite(data = articles)

    i = 2
    while(i <= pages):
      self.getUrl(i, pages)
      i = i + 1
    