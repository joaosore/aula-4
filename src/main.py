import yaml
from classes.api import API

with open('config.yaml', 'r') as file:
  config = yaml.safe_load(file)

  url = config['api']['url']
  path = config['api']['path']
  key = config['api']['key']
  max_records = config['api']['max_records']

  search = config['search']
  operator = config['operator']

  api = API(url, path, key, max_records, search, operator)

api.connect()

# con = sqlite3.connect("ieee.db")
# cur = con.cursor()
# res = cur.execute("SELECT * FROM articles")


# print(res.fetchall())


