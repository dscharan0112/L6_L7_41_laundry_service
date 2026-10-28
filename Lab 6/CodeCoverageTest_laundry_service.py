import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


# ---------- extra_weight_charge ----------
def test_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_unknown_garment_type():
    with pytest.raises(ValueError):
        extra_weight_charge("curtain", 3, "standard", False)


def test_negative_weight():
    with pytest.raises(ValueError):
        extra_weight_charge("regular", -1, "standard", False)


def test_member_gets_extra_allowance():
    # regular member: included 5 + 2 = 7, extra = 1, rate 30
    assert extra_weight_charge("regular", 8, "standard", True) == 30


def test_express_small_extra():
    # included 5, extra 2, express rate 50
    assert extra_weight_charge("regular", 7, "express", False) == 100


def test_standard_large_extra():
    # extra 11 > 10, rate 30 + 15 = 45
    assert extra_weight_charge("regular", 16, "standard", False) == 495


def test_express_large_extra():
    # extra 11 > 10, rate 50 + 15 + 10 = 75
    assert extra_weight_charge("regular", 16, "express", False) == 825


# ---------- order_acceptable ----------
def test_order_acceptable():
    assert order_acceptable(10, 20, False) is True


def test_delicate_order_limit():
    assert order_acceptable(2, 5, True) is True


def test_order_too_heavy():
    assert order_acceptable(30, 10, False) is False


# ---------- dropoff_status ----------
def test_dropoff_accepted_plain():
    assert dropoff_status(60, False, False) == "accepted"


def test_dropoff_accepted_bedding_express():
    assert dropoff_status(120, True, True) == "accepted"


def test_dropoff_late():
    assert dropoff_status(45, False, False) == "late"


def test_dropoff_rejected():
    assert dropoff_status(10, False, False) == "rejected"
