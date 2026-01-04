from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
DATA_FILE = 'products.json'

# --- HARDCODED STORES ---
stores = [
    {"id": "Sekayu", "name": "Toko Musi Baru Sekayu", "phone": "628123456789"},
    {"id": "Simpang Patal", "name": "Toko Musi Baru Simpang Patal", "phone": "628987654321"},
    {"id": "Simpang Prabumulih", "name": "Toko Musi Baru Simpang Prabumulih", "phone": "628987654321"},
]

def load_data():
    if not os.path.exists(DATA_FILE):
        # Default product with stock for each store
        initial_data = [{
            "id": "1", 
            "name": "Example Item", 
            "price": "100", 
            "image": "https://via.placeholder.com/150",
            "stocks": {"jkt": 10, "bali": 5} # Store-specific stock
        }]
        save_data(initial_data)
        return initial_data
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    products = load_data()
    return render_template('index.html', products=products, stores=stores)

@app.route('/admin-portal')
def admin():
    products = load_data()
    return render_template('admin.html', products=products, stores=stores)

@app.route('/update_stock', methods=['POST'])
def update_stock():
    products = load_data()
    p_id = request.form.get("product_id")
    store_id = request.form.get("store_id")
    new_qty = int(request.form.get("new_stock"))
    
    for p in products:
        if p['id'] == p_id:
            p['stocks'][store_id] = new_qty
            break
    save_data(products)
    return redirect(url_for('admin'))

@app.route('/add_new_item', methods=['POST'])
def add_new_item():
    products = load_data()
    
    # Safely calculate the next ID number
    if not products:
        new_id = "1"
    else:
        # Convert all current IDs to numbers to find the maximum
        new_id = str(max([int(p['id']) for p in products]) + 1)
    
    # Create empty stock for all branches
    initial_stocks = {s['id']: 0 for s in stores}
    
    new_item = {
        "id": new_id,
        "name": request.form.get("name"),
        "price": request.form.get("price"),
        "image": request.form.get("image"),
        "stocks": initial_stocks # Must be plural 'stocks'
    }
    products.append(new_item)
    save_data(products)
    return redirect(url_for('admin'))

@app.route('/delete_item/<p_id>')
def delete_item(p_id):
    products = load_data()
    products = [p for p in products if p['id'] != p_id]
    save_data(products)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # host='0.0.0.0' artinya website kamu terbuka untuk perangkat lain di jaringan yang sama
    app.run(host='0.0.0.0', port=5000, debug=True)