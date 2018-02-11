from flask import Flask, request, url_for, redirect, render_template
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from database_setup import Base, Restaurant, MenuItem

# set up database and bind to it
engine = create_engine('sqlite:///restaurant_menu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

def getCourses(items):
    """[summary]
    
    Arguments:
        items {[list]} -- [A list of menu items dicts]
    
    Returns:
        [list] -- [a list of unique ordered menu item courses]
    """

    courses = set(item.get('course') for item in items) # we need a unique set of menu item courses
    courses = list(courses)  # converting the set to a list so we can sort it.
    courses.sort()

    return courses

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    # get all restaurants
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if (request.method == 'POST'):
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if (request.method == 'POST'):
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    selected_restaurant = None
    for restaurant in restaurants:
        if (restaurant.get('id') == str(restaurant_id)):
            selected_restaurant = restaurant
    
    return render_template('deleteRestaurant.html', restaurant = selected_restaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    # get the menu items for the restaurant with the given id
    selected_item = selected_restaurant = None
    for item in items:
        if (int(item['id']) == restaurant_id):
            selected_item = item
    
    return render_template('menu.html', item = selected_item, restaurant = selected_restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
    # return "This page is for making a new menu item for restaurant %s" % restaurant_id
    courses = getCourses(items)
    return render_template('newMenuItem.html', restaurants = restaurants, courses = courses)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    # return "This page is for editing menu item %s" % menu_id
    menu_item = menu_course = None
    for item in items:
        if item.get('id') == str(menu_id):
            menu_item = item
            menu_course = item['course']

    courses = getCourses(items)
    return render_template('editMenuItem.html', menu = menu_item, menu_course = menu_course, courses = courses)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    # return "This page is for deleting menu item %s" % menu_id
    menu_item = None
    for item in items:
        if item.get('id') == str(menu_id):
            menu_item = item
    
    return render_template('deleteMenuItem.html', menu = menu_item)



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)