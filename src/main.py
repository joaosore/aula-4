import yaml

from .api.scid import API_SCID
from classes.api.ieee import API_IEEE

from classes.format.ieee import FORMAT_IEEE
from classes.format.scid import FORMAT_SCID


with open('config.yaml', 'r') as file:
  config = yaml.safe_load(file)

  mode = config['mode']

  if(mode == 'Extract'):
    
    scope = config['scope']

    if(scope == "IEEE"):
      url = config['api_ieee']['url']
      path = config['api_ieee']['path']
      key = config['api_ieee']['key']
      max_records = config['apapi_ieeei']['max_records']
      table = config['api_ieee']['table']
      page = config['api_ieee']['page']

      search = config['search']
      operator = config['operator']
      
      api = API_IEEE(url, path, key, max_records, search, operator, table, page)
      api.extract()

    if(scope == "SCID"):
      url = config['api2']['url']
      path = config['api2']['path']
      key = config['api2']['key']
      count = config['api2']['count']
      table = config['api2']['table']
      page = config['api2']['page']
      httpAccept = config['api2']['httpAccept']

      search = config['search']
      operator = config['operator']
      
      api = API_SCID(url, path, key, count, search, operator, table, page, httpAccept)
      api.extract()

  if(mode == 'SQLile'):

    scope = config['scope']

    if(scope == "IEEE"):

      f = FORMAT_IEEE("./raw/IEEE/", "local", "ieee_articles")
      f.load()

    if(scope == "SCID"):

      f = FORMAT_SCID("./raw/SCID/", "local", "icid_articles")
      f.load()