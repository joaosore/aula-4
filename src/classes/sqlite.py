
import sqlite3

class SQLITE:

  def __init__(self, db, table):
    self.db = db
    self.table = table
    self.con = sqlite3.connect(self.db)
    self.cur = self.con.cursor()

  def create(self, query):
    self.cur.execute("CREATE TABLE IF NOT EXISTS " + self.table + " (" + query + ")")

  def insert(self, query, values):
    i = 0
    while(i < len(query)):
      self.cur.execute(query[i], values[i])
      self.con.commit()
      i = i + 1