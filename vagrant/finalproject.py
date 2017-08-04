from flask import Flask,render_template,request,redirect,url_for,flash,jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurant.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

session = DBSession()

@app.route('/restaurants/JSON')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants = [r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id,menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItem = item.serialize)



@app.route('/')
@app.route('/restaurants')
@app.route('/restaurant')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html',restaurants = restaurants)

@app.route('/restaurant/new',methods=['GET','POST'])
def newRestaurant():
	if request.method == "POST":
		newRestaurant = Restaurant(name = request.form['nameRestaurant'])
		session.add(newRestaurant)
		session.commit()
		flash('New Restaurant created!')
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method=='POST':
		if request.form['nameRestaurant']:
			restaurant.name = request.form['nameRestaurant']
			session.add(restaurant)
			session.commit()
			flash('Restaurant Successfully Edited!')
			return redirect(  url_for('showRestaurants') )
	else:
		return render_template('editRestaurant.html',restaurant=restaurant,restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/delete',methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method=='POST':
		session.delete(restaurant)
		session.commit()
		flash('Restaurant Successfully Delete!')
		return redirect(  url_for('showRestaurants') )
	else:
		return render_template('deleteRestaurant.html',restaurant=restaurant,restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)

	return render_template('menu.html',restaurant=restaurant,items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new',methods = ['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		if request.form['name'] and request.form['description'] and request.form['price'] and request.form['course']:
			newMenu = MenuItem(name = request.form['name'],
				description = request.form['description'],
				price = request.form['price'],
				course = request.form['course'],
				restaurant_id = restaurant_id)
			session.add(newMenu)
			session.commit()
			flash('New Item Created!')
			return redirect( url_for('showMenu',restaurant_id=restaurant_id) )
	else:
		return render_template('newmenuitem.html',restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method=="POST":
		if request.form['name'] and request.form['description'] and request.form['price'] and request.form['course']:
			item.name = request.form['name']
			item.description = request.form['description']
			item.price = request.form['price']
			item.course = request.form['course']
			session.add(item)
			session.commit()
			flash('Menu Item Successfully  Edited!')
			return redirect( url_for('showMenu',restaurant_id=restaurant_id) )
	else:
		return render_template('editmenuitem.html',restaurant_id=restaurant_id,menu=item,menu_id=item.id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == "POST":
		session.delete(item)
		session.commit()
		flash('Menu Item Successfully Delete!')
		return redirect( url_for('showMenu',restaurant_id=restaurant_id) )
	else:
		return render_template('deletemenuitem.html',restaurant_id=restaurant_id,menu=item,menu_id=item.id)




if __name__ == '__main__':
	app.secret_key = "super_secret_key"
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)