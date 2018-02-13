from flask import Flask, request, url_for, redirect, render_template, jsonify, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from database_setup import Base, Restaurant, MenuItem

# set up database and bind to it
engine = create_engine('sqlite:///restaurant_menu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
app.secret_key = 'secret_key'

def getCourses():
    courses = set(['Entree', 'Dessert', 'Appetizer', 'Entree', 'Beverages'])
    courses = list(courses)
    courses.sort()
    return courses

# Making an API endpoint
@app.route('/restaurants/JSON')
def restaurantJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants = [r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/JSON')
def restaurantDetailJSON(restaurant_id):
    try:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        return jsonify(Restaurant = [restaurant.serialize])
    except Exception:
        return jsonify({'message': 'restaurant with the specified id does not exist', 'success': False, 'error': True})

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    try:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
        return jsonify(MenuItems = [i.serialize for i in items])
    except Exception:
        return jsonify({'message': 'restaurant with the specified id does not exist', 'success': False, 'error': True})

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuDetailJSON(restaurant_id, menu_id):
    try:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        item = session.query(MenuItem).filter_by(restaurant_id=restaurant.id, id=menu_id).one()
        return jsonify(Menu=[item.serialize])

    except Exception:
        return jsonify({'message': 'restaurant or menu with the specified id does not exist', 'success': False, 'error': True })

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    # get all restaurants
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if (request.method == 'POST'):
        if (request.form['name'] == ''):
            # user enters no restaurant name, redirect back to 'showRestaurants' page
            return redirect(url_for('showRestaurants'))
        else:
            newRestaurant = Restaurant(name = request.form['name'])
            session.add(newRestaurant)
            session.commit()
            flash('New Restaurant created successfully')
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    # print (restaurant)
    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant = restaurant)

@app.route('/restaurants/search', methods=['GET'])
def findRestaurant():
    restaurant = session.query(Restaurant).filter_by(name = request.args.to_dict()['q']).one()
    return redirect(url_for('showMenu', restaurant_id = restaurant.id))

    # will add better and more robust search functionality

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()

    if menu_items != []:
        return render_template('menu.html', items=menu_items, restaurant=restaurant)
    else:
        return render_template('menu.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        new_menu_item = MenuItem(name = request.form['name'], price = request.form['price'],
                                course = request.form['course'], description = request.form['description'],
                                restaurant_id = restaurant_id)
        session.add(new_menu_item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        courses = getCourses()
        return render_template('newMenuItem.html', restaurant = restaurant, courses = courses)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(restaurant_id = restaurant.id, id = menu_id).one()
    
    if request.method == 'POST':
        menu_item.name = request.form['name']
        menu_item.price = request.form['price']
        menu_item.course = request.form['course']
        menu_item.description = request.form['description']
        session.add(menu_item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        courses = getCourses()
        return render_template('editMenuItem.html', menu = menu_item, menu_course = menu_item.course, courses = courses, restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(restaurant_id = restaurant.id, id = menu_id).one()

    if request.method == 'POST':
        session.delete(menu_item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', menu=menu_item, restaurant = restaurant)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
