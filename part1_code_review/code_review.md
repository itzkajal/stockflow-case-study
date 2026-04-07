# Part 1 – Code Review & Debugging  

## Issues I found in the given code  

### 1. SKU is not checked for uniqueness  
The API directly creates a product using the given SKU without checking if it already exists. In a real system, SKU should be unique. If duplicates are allowed, it can create confusion in tracking products and inventory.  

### 2. Product is tied to only one warehouse  
In the current code, the product is created along with a warehouse_id. But according to the requirements, a product can exist in multiple warehouses. This design makes it difficult to manage the same product across different locations.  

### 3. No validation for input data  
The code assumes all fields like `name`, `sku`, `price`, and `initial_quantity` are always present. If any of these are missing, the API may crash. There should be proper validation and default values to avoid runtime errors.  

### 4. Separate database commits  
There are two separate `commit()` calls — one for product and one for inventory. If the second operation fails, the product will still be saved, which leads to inconsistent data. Both operations should be part of a single transaction.  

### 5. No error handling  
The code does not handle any exceptions. For example, if a duplicate SKU is inserted or database fails, the API will return a server error instead of a proper message.  

---

## Updated Code (Flask)

```python
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from app import db
from models import Product, Inventory

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    try:
        # Create product
        product = Product(
            name=data.get('name'),
            sku=data.get('sku'),
            price=data.get('price', 0.0)  # default price
        )

        db.session.add(product)
        db.session.flush()  # get product.id before commit

        # Create inventory for warehouse
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=data.get('warehouse_id'),
            quantity=data.get('initial_quantity', 0)
        )

        db.session.add(inventory)
        db.session.commit()

        return jsonify({
            "message": "Product created successfully",
            "product_id": product.id
        })

    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "SKU already exists"
        }), 400