from flask import Flask, render_template
app = Flask(__name__)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/')
def newRestaurant():
    return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    # find the restaurant with the given id in the url
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

    # for restaurant in restaurants:
    #     if (restaurant['id'] == restaurant_id):
    #         selected_restaurant = restaurant

    for item in items:
        if (int(item['id']) == restaurant_id):
            selected_item = item
    
    return render_template('menu.html', item = selected_item, restaurant = selected_restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
    # return "This page is for making a new menu item for restaurant %s" % restaurant_id
    # selected_restaurant = None
    # for restaurant in restaurants:
    #     if (restaurant.get(restaurant_id) == str(restaurant_id)):
    #         selected_restaurant = restaurant


    # we need unique set of menu item courses so we use set comprehension
    courses = set(item.get('course') for item in items)
    courses = list(courses) # converting the set to a list so we can sort it.
    courses.sort()
    
    return render_template('newMenuItem.html', restaurants = restaurants, courses = courses)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    # return "This page is for editing menu item %s" % menu_id
    menu_item = None
    menu_course = None
    for item in items:
        if item.get('id') == str(menu_id):
            menu_item = item
            menu_course = item['course']

    courses = set(item.get('course') for item in items)
    courses = list(courses) # converting the set to a list so we can sort it.
    courses.sort()
    print (courses)

    return render_template('editMenuItem.html', menu = menu_item, menu_course = menu_course, courses = courses)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "This page is for deleting menu item %s" % menu_id



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
