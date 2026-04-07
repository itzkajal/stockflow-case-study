# Part 2 – Database Design

## Overview

This system supports companies managing inventory across multiple warehouses. 
Products can exist in multiple warehouses, suppliers provide products, and 
inventory changes should be tracked. Some products can also be bundles.

---

## Tables

### Company
- id (PK)
- name
- created_at
- updated_at

Stores companies using the platform.

---

### Warehouse
- id (PK)
- company_id (FK → Company.id)
- name
- location
- created_at

A company can have multiple warehouses.

---

### Product
- id (PK)
- name
- sku (UNIQUE)
- price (decimal)
- is_bundle (boolean)
- created_at
- updated_at

SKU is unique across the platform.

---

### Inventory
- id (PK)
- product_id (FK → Product.id)
- warehouse_id (FK → Warehouse.id)
- quantity
- updated_at

Tracks quantity of product in each warehouse.

---

### Supplier
- id (PK)
- name
- contact_email
- phone

Stores supplier information.

---

### ProductSupplier
- id (PK)
- product_id (FK → Product.id)
- supplier_id (FK → Supplier.id)

A product can have multiple suppliers.

---

### InventoryHistory
- id (PK)
- inventory_id (FK → Inventory.id)
- change_amount
- reason
- created_at

Used to track inventory updates.

---

### ProductBundle
- id (PK)
- parent_product_id (FK → Product.id)
- child_product_id (FK → Product.id)
- quantity

Used for bundle products.

---

## Relationships

Company → Warehouses  
Warehouse → Inventory  
Product → Inventory  
Product → Supplier  
Product → Bundle items  

---

## Indexes and Constraints

- SKU should be unique  
- Index on product_id in inventory  
- Index on warehouse_id in inventory  
- Unique (product_id, warehouse_id)

---

## Missing Requirements

- Is SKU unique per company or globally?  
- Can products have multiple suppliers?  
- How is low stock threshold defined?  
- Should bundles reduce child inventory automatically?  
- Do we support warehouse transfers?  

---

## Design Decisions

- Separate inventory table supports multi warehouse
- Inventory history tracks stock changes
- Product bundle table supports bundle products
- Product supplier mapping allows flexibility