from flask import Flask, render_template
from mockData import get_mock_restaurant_data, get_single_mock_restaurant_data,\
                     get_mock_menu_items_data, get_single_mock_menu_item_data
app = Flask(__name__)

# restaurant mock data
restaurant = get_single_mock_restaurant_data()
restaurants = get_mock_restaurant_data()

# menu items mock data
items = get_mock_menu_items_data()
item = get_single_mock_menu_item_data()

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
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/')
def newRestaurant():
    return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    selected_restaurant = None
    error = None
    for restaurant in restaurants:
        if (int(restaurant['id']) == restaurant_id):
            selected_restaurant = restaurant
    
    if not selected_restaurant:
        error = 'There is no such restaurant'
    
    return render_template("editRestaurant.html", restaurant = selected_restaurant, error = error)

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
