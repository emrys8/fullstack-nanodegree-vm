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

def getRestaurantData():
    all_restaurants = session.query(Restaurant).all()
    return all_restaurants

def get_general_styles():
    return '\
    html { font-family: Helvetica, Arial, sans-serif; } \
    body { width: 70% } \
    a { color: #1187b2; } a:link, a:visited { a:color: ##1187b2; } \
    form input { padding: 0.8em 0.5em; margin-right: 10px; font-size: 1em } \
    form input[type=text] { width: 300px } \
    '

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                styles = get_general_styles()
                output += "<html><head><style>%s</style></head><body>" % styles
                output += "<h1>Restaurants</h1>"
                all_restaurants = getRestaurantData()

                for restaurant in all_restaurants:
                    output += "<h3>" + restaurant.name + "</h3>"
                    output += "<p><a href='%s/edit'>Edit</a></p>" % restaurant.id
                    output += "<p><a href='#'>Delete</a></p>"
                
                # a link to create new restaurants
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
                num_regexp = re.compile(r'\d+')
                restaurant_id = re.search(num_regexp, self.path).group(0)

                # get the restaurant with the given id
                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

                # populate page & form with details of the restaurant
                output += "<h1>%s</h1>" % restaurant.name
                output += '''<form method='POST' enctype='multipart/form-data'
                action = '/'><div>
                <input type='text' name='restaurant_name' placeholder='%s'>
                <input type='submit' value='Rename'>
                </div></form>''' % restaurant.name
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):

        print (self.path)

        try:
            if self.path.endswith("/restaurants/create"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                print (ctype)
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_name')
                    # print (messagecontent)
                    # create a new Restaurant
                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                
                output = ""
                styles = get_general_styles()
                output += "<html><head><style>%s</style></head><body>" % styles
                output += "<hr><h1>A new restaurant with the name: %s has been created successfully</h1><hr>" % newRestaurant.name
                output += "</body></html>"
                self.wfile.write(output)
                # print output
                return
                    
                
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
