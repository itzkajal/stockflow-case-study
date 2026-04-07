# stockflow-case-study
# Part 3 – Low Stock Alerts API

## Endpoint

GET /api/companies/{company_id}/alerts/low-stock

This endpoint returns products that are running low in stock for a given company.

---

## Business Logic

The API checks:

- Products with stock below threshold
- Only products with recent sales (last 30 days)
- Multiple warehouses per company
- Supplier information for reordering

---

## Assumptions

- Each product has a predefined low stock threshold
- Sales activity is checked for last 30 days
- Inventory is stored per warehouse
- Supplier is mapped to product

---

## Edge Cases Handled

- No recent sales → no alert
- Zero stock → alert generated
- Missing warehouse → skipped
- Multiple warehouses supported

---

## Example Response
