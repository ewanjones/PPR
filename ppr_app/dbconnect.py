import MySQLdb
import gc

class Database():
	def __init__(self):
		self.c, self.conn = self.connect()


	def connect(self):
		conn = MySQLdb.connect(user="root",
							   passwd='Cross1994',
							   db="ppr")
		c =  conn.cursor()
		return c, conn


	def closeConnection(self, c, conn):
		self.c.close()
		self.conn.close()
		gc.collect()
