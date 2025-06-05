import sys
from pathlib import Path

# Add the personal_shopper module to path
sys.path.append(str(Path(__file__).resolve().parents[1] / "complex-agents" / "personal_shopper"))

from database import CustomerDatabase


def _create_db(tmp_path):
    return CustomerDatabase(str(tmp_path / "test.db"))


def test_get_or_create_customer(tmp_path):
    db = _create_db(tmp_path)
    cid1 = db.get_or_create_customer("John", "Doe")
    assert isinstance(cid1, int)
    cid2 = db.get_or_create_customer("John", "Doe")
    assert cid1 == cid2


def test_add_order_and_get_customer_orders(tmp_path):
    db = _create_db(tmp_path)
    cid = db.get_or_create_customer("Jane", "Smith")
    order1 = {"items": [{"name": "Widget", "quantity": 2, "price": 9.99}]}
    order2 = {"items": [{"name": "Gadget", "quantity": 1, "price": 19.99}]}

    oid1 = db.add_order(cid, order1)
    oid2 = db.add_order(cid, order2)

    orders = db.get_customer_orders(cid)
    assert len(orders) == 2
    returned_ids = {o["id"] for o in orders}
    assert returned_ids == {oid1, oid2}
    details = [o["details"] for o in orders]
    assert any(item["name"] == "Widget" for o in details for item in o["items"])
    assert any(item["name"] == "Gadget" for o in details for item in o["items"])


def test_get_customer_order_history(tmp_path):
    db = _create_db(tmp_path)
    cid = db.get_or_create_customer("Alice", "Wonder")
    db.add_order(cid, {"items": [{"name": "Book", "quantity": 1}]})

    history = db.get_customer_order_history("Alice", "Wonder")
    assert "Order history for Alice Wonder" in history
    assert "Book" in history
