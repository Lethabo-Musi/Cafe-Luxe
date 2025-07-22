import sqlite3

DATABASE = 'inventory_store.db'

class Store:
    def get_connection(self):
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  # to get dictionary-style rows
        return conn

    def add_product(self, name, price, quantity):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO product (name, price, quantity) VALUES (?, ?, ?)",
                       (name, price, quantity))
        conn.commit()
        conn.close()

    def get_all_products(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        conn.close()
        return products

    def get_product_by_id(self, product_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product WHERE id=?", (product_id,))
        product = cursor.fetchone()
        conn.close()
        return product

    def update_product(self, product_id, name, price, quantity):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE product SET name=?, price=?, quantity=? WHERE id=?",
                       (name, price, quantity, product_id))
        conn.commit()
        conn.close()

    def remove_product(self, product_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM product WHERE id=?", (product_id,))
        conn.commit()
        conn.close()

    def sell_product(self, product_id, sale_date, sale_quantity):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, quantity FROM product WHERE id=?", (product_id,))
        product = cursor.fetchone()
        if product:
            name, price, quantity = product
            if quantity >= sale_quantity:
                sale_total = price * sale_quantity
                cursor.execute("INSERT INTO sales (sale_date, name, sale_quantity) VALUES (?, ?, ?)",
                               (sale_date, name, sale_quantity))
                new_quantity = quantity - sale_quantity
                cursor.execute("UPDATE product SET quantity=? WHERE id=?", (new_quantity, product_id))
                conn.commit()
                conn.close()
                return True, f"Sold {sale_quantity} units of {name} for {sale_total}."
            else:
                conn.close()
                return False, "Not enough quantity available."
        else:
            conn.close()
            return False, "Product not found."
