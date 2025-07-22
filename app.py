from flask import Flask, render_template, request, redirect, url_for, flash
from store import Store

app = Flask(__name__)
app.secret_key = 'your_secret_key'
store = Store()

@app.route('/')
def home():
    products = store.get_all_products()
    return render_template('home.html', products=products)

@app.route('/view', methods=['GET'])
def view_products():
    query = request.args.get('query', '').lower()
    all_products = store.get_all_products()

    if query:
        filtered_products = [p for p in all_products if query in p['name'].lower()]
    else:
        filtered_products = all_products

    return render_template('view_product.html', products=filtered_products)
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']

        store.add_product(name, float(price), int(quantity))
        
        flash('Product added successfully!')
        return redirect(url_for('view_products'))

    return render_template('add_product.html')

@app.route('/update', methods=['GET', 'POST'])
def update_product_page():
    if request.method == 'POST':
        product_id = int(request.form['id'])
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        store.update_product(product_id, name, price, quantity)
        flash('Product updated successfully!')
        return redirect(url_for('update_product_page'))
    return render_template('update_product.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_product_page():
    if request.method == 'POST':
        try:
            product_id = int(request.form['id'])
            product = store.get_product_by_id(product_id)
            if product:
                store.remove_product(product_id)
                flash("Product deleted successfully!")
                return redirect(url_for('delete_product_page'))
            else:
                flash("Product not found.")
                return redirect(url_for('delete_product_page'))
        except ValueError:
            flash("Invalid ID entered.")
            return redirect(url_for('delete_product_page'))
    return render_template('delete_product.html')


@app.route('/sell', methods=['GET', 'POST'])
def sell_product_page():
    if request.method == 'POST':
        product_id = int(request.form['id'])
        sale_date = request.form['sale_date']
        sale_quantity = int(request.form['sale_quantity'])
        success, message = store.sell_product(product_id, sale_date, sale_quantity)
        if success:
            flash('Product sold successfully!')
            return redirect(url_for('sell_product_page'))
        else:
            return render_template('sell_product.html', error=message)
    return render_template('sell_product.html')

if __name__ == '__main__':
    app.run(debug=True)
