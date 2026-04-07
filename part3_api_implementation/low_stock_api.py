from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Mock data (assumed database records)
products = [
    {
        "id": 1,
        "name": "Widget A",
        "sku": "WID-001",
        "threshold": 20,
        "supplier": {
            "id": 101,
            "name": "Supplier Corp",
            "contact_email": "orders@supplier.com"
        }
    }
]

warehouses = [
    {
        "id": 10,
        "company_id": 1,
        "name": "Main Warehouse"
    }
]

inventory = [
    {
        "product_id": 1,
        "warehouse_id": 10,
        "quantity": 5
    }
]

sales = [
    {
        "product_id": 1,
        "date": datetime.now() - timedelta(days=5),
        "quantity": 2
    }
]


@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    alerts = []

    for item in inventory:
        product = next((p for p in products if p["id"] == item["product_id"]), None)
        warehouse = next((w for w in warehouses if w["id"] == item["warehouse_id"] and w["company_id"] == company_id), None)

        if not product or not warehouse:
            continue

        # check recent sales (last 30 days)
        recent_sales = [
            s for s in sales
            if s["product_id"] == product["id"]
            and s["date"] >= datetime.now() - timedelta(days=30)
        ]

        if not recent_sales:
            continue

        threshold = product["threshold"]
        current_stock = item["quantity"]

        if current_stock <= threshold:
            avg_daily_sales = sum(s["quantity"] for s in recent_sales) / 30
            days_until_stockout = int(current_stock / avg_daily_sales) if avg_daily_sales > 0 else 0

            alerts.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "sku": product["sku"],
                "warehouse_id": warehouse["id"],
                "warehouse_name": warehouse["name"],
                "current_stock": current_stock,
                "threshold": threshold,
                "days_until_stockout": days_until_stockout,
                "supplier": product["supplier"]
            })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })


if __name__ == "__main__":
    app.run(debug=True)