from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import re

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from database_setup import Restaurant, MenuItem, Base

# connect to database
engine = create_engine('sqlite:///restaurantmenu.db')

# bind the engine to the metadata of the Base class
Base.metadata.bind = engine

# a DB session
DBSession = sessionmaker(bind=engine)

session = DBSession()

def get_general_styles():
    return '\
    html { font-family: Helvetica, Arial, sans-serif; } \
    body { width: 70% } \
    a { color: #1187b2; } a:link, a:visited { a:color: ##1187b2; } \
    form input { padding: 0.8em 0.5em; margin-right: 10px; font-size: 1em } \
    form input[type=text] { width: 300px } \
    '

def get_restaurant_id(path):
    num_regexp = re.compile(r'\d+')
    restaurant_id = re.search(num_regexp, path).group(0)
    return restaurant_id

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                all_restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Contype-type', 'text/html')
                self.end_headers()

                output = ""
                styles = get_general_styles()
                output += "<html><head><style>%s</style></head><body>" % styles
                output += "<h1>Restaurants</h1>"
                
                for restaurant in all_restaurants:
                    output += "<h3>" + restaurant.name + "</h3>"
                    output += "<p><a href='%s/edit'>Edit</a></p>" % restaurant.id
                    output += "<p><a href='%s/delete'>Delete</a></p>" % restaurant.id

                output += "<p><a href='/restaurants/create' target='_blank'>Make a New Restaurant Here</a></p>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/create"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                styles = get_general_styles()
                output += "<html><head><style>%s</style></head><body>" % styles
                output += "<h1>Make A New Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/create'><div>
                <input type='text' name='restaurant_name' placeholder='New Restaurant Name'><input type='submit' value='Create'>
                </div></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                styles = get_general_styles()
                output += "<html><head><style>%s</style><body>" % styles
                # get the the id from the url
                
                restaurant_id = get_restaurant_id(self.path)

                # get the restaurant with the given id
                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

                # populate page & form with details of the restaurant
                output += "<h1>%s</h1>" % restaurant.name
                output += '''<form method='POST' enctype='multipart/form-data'
                action = '/%s/edit'><div>
                <input type='text' name='restaurant_name' placeholder='%s'>
                <input type='submit' value='Rename'>
                </div></form>''' % (restaurant.id, restaurant.name)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                styles = get_general_styles()
                output += "<html><head><style>%s</style><body>" % styles

                restaurant_id = get_restaurant_id(self.path)
                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

                output += "<h2>Are you sure you want to delete %s</h2>" % restaurant.name
                output += "<form method='POST' action='/%s/delete' enctype='multipart/form-data'><div>\
                <input type='hidden' name='restaurant_name' value=%s><input type='submit' value='Delete'></div></form>" % (restaurant.id, restaurant.id)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):

        try:
            if self.path.endswith("/restaurants/create"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                # print (ctype)
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_name')
                    # print (messagecontent)
                    # create a new Restaurant
                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', 'restaurants')
                    self.end_headers()
                    self.wfile.write(output)
                    # print output
                    return

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                
                if ctype == 'multipart/form-data':

                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_name')

                    # get the id of the restaurant
                    restaurant_id = get_restaurant_id(self.path)
                    
                    # get the restaurant with the given id
                    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

                    old_name = restaurant.name

                    # update restaurant name
                    restaurant.name = messagecontent[0]

                    session.add(restaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')

                    self.end_headers()
                    return
            
            if self.path.endswith("/delete"):

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_name')

                    # get the restaurant and delete
                    restaurant_id = messagecontent[0]
                    print (restaurant_id)

                    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                    
                    session.delete(restaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
