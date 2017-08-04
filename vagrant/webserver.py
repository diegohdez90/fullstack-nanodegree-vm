from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi


engine = create_engine('sqlite:///restaurant.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith('/hello'):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "Hello !"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
				output += "<h2>What would you like me to say</h2>"
				output += "<input type='text' name='message'>"
				output += "<input type='submit' value='Submit'>"
				output += "</form>"
				output += "</body></html>"

				self.wfile.write(output)

				print output
				return 
			if self.path.endswith('/hola'):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "Hola!"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
				output += "<h2>What would you like me to say</h2>"
				output += "<input type='text' name='message'>"
				output += "<input type='submit' value='Submit'>"
				output += "</form>"
				output += "</body></html>"

				self.wfile.write(output)

				print output
				return 

			if self.path.endswith('/restaurants'):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				restaurants = session.query(Restaurant).all()
				output = ""
				output += "<html><body>"
				output += "<a href='/restaurants/new'>Create a new Restaurant</a><br>"
				for r in restaurants:
					output +=  r.name
					output += "<br>"
					output += "<a href='restaurants/%s/edit'>Edit</a>"%r.id
					output += "<br>"
					output += "<a href='restaurants/%s/delete'>Delete</a>"%r.id
					output += "<br>"
				output += "</body></html>"

				self.wfile.write(output)

				return 

				
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Make a new restaurant</h1>"
				output += "<form method='POST' action='/restaurants/new' enctype='multipart/form-data' >"
				output += "<input type='text' name='restaurant'>"
				output += "<input type='submit' value='Create Restaurant'>"
				output += "</form>" 
				output += "</body></html>"
				self.wfile.write(output)
				print output


			if self.path.endswith("/edit"):
				editPath = self.path.split('/')
				
				restaurant = session.query(Restaurant).filter_by(id = editPath[2]).one()
				
				if restaurant != []:
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h1>%s</h1>"%restaurant.name
					output += "<form method='POST' action='/restaurants/%s/edit' enctype='multipart/form-data' >"%restaurant.id
					output += "<input type='text' name='restaurant' placeholder='%s'>"%restaurant.name
					output += "<input type='submit' value='Edit Restaurant'>"
					output += "</form>" 
					output += "</body></html>"
					self.wfile.write(output)
					print output

			if self.path.endswith('/delete'):
				deletePath = self.path.split('/')
				deleteRestaurant = session.query(Restaurant).filter_by(id = deletePath[2]).one()
				if deleteRestaurant != []:
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h1> Are you sure you want delete %s Restaurant</h1>"%deleteRestaurant.name
					output += "<form method='POST' action='/restaurants/%s/delete' enctype='multipart/form-data' >"%deleteRestaurant.id
					output += "<input type='submit' value='Delete Restaurant'>"
					output += "</form>" 
					output += "</body></html>"
					self.wfile.write(output)
					print output

		except IOError:
			self.send_error('404',"File not fountd %s "%self.path)

	def do_POST(self):
		try:
			if self.path.endswith('/restaurants/new'):
				
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('Content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile,pdict)
					restaurantName = fields.get('restaurant')
					print "Get Restaurant"

				restaurantEntry = Restaurant(name = restaurantName[0])
				session.add(restaurantEntry)
				session.commit() 
				print 'Commit restaurant'

				self.send_response(301)
				self.send_header('Content-type','text/html')
				self.send_header('Location','/restaurants')
				self.end_headers()
				return

			if self.path.endswith('/edit'):
				editForm = self.path.split('/')
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('Content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile,pdict)
					restaurantName = fields.get('restaurant')
					print "Get Restaurant to Edit"
					print restaurantName
					idRestaurant = editForm[2]
					print idRestaurant

				restaurantEdit = session.query(Restaurant).filter_by(id = idRestaurant).one()
				print restaurantEdit
				if restaurantEdit!=[]:
					print restaurantEdit.name
					restaurantEdit.name = restaurantName[0]
					session.add(restaurantEdit)
					session.commit()
					print 'Restaurant edited'
					self.send_response(301)
					self.send_header('Content-type','text/html')
					self.send_header('Location','/restaurants')
					self.end_headers()
					return
			if self.path.endswith('/delete'):
				deleteForm = self.path.split('/')
				deleteRestaurant = session.query(Restaurant).filter_by(id = deleteForm[2]).one()
				if deleteRestaurant:
					session.delete(deleteRestaurant)
					session.commit()
					print 'Restaurant Delete'
					self.send_response(301)
					self.send_header('Content-type','text/html')
					self.send_header('Location','/restaurants')
					self.end_headers()
					return
		except:
			pass

def main():
	try:
		port = 8089
		server = HTTPServer(('',port),webServerHandler)
		print "Webserver is running on the port %s "%port
		server.serve_forever()

	except KeyboardInterrupt:
		print '^C to stop server'
		server.socket.close()

if __name__ == '__main__':
	main()