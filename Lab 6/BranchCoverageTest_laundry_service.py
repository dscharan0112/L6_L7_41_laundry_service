import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


# =====================================================
# extra_weight_charge  (every decision True AND False)
# =====================================================
def test_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_exactly_included_weight_is_free():
    # boundary: extra == 0
    assert extra_weight_charge("regular", 5, "standard", False) == 0


def test_zero_weight_is_valid():
    # boundary: weight 0 is not negative
    assert extra_weight_charge("delicate", 0, "standard", False) == 0


@pytest.mark.parametrize("garment", ["curtain", "", "REGULAR"])
def test_unknown_garment_type(garment):
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge(garment, 3, "standard", False)


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -1, "standard", False)


def test_member_regular_gets_two_extra_kg():
    # included 5 + 2 = 7, extra 1, rate 30
    assert extra_weight_charge("regular", 8, "standard", True) == 30


def test_member_delicate_gets_two_extra_kg():
    # included 3 + 2 = 5, extra 1, rate 30
    assert extra_weight_charge("delicate", 6, "standard", True) == 30


def test_member_bedding_gets_no_bonus():
    # included stays 8, extra 2, rate 30
    assert extra_weight_charge("bedding", 10, "standard", True) == 60


def test_non_member_no_bonus():
    # included 5, extra 1, rate 30
    assert extra_weight_charge("regular", 6, "standard", False) == 30


def test_standard_rate_small_extra():
    assert extra_weight_charge("regular", 7, "standard", False) == 60


def test_express_rate_small_extra():
    # extra 2, rate 50
    assert extra_weight_charge("regular", 7, "express", False) == 100


def test_extra_exactly_ten_no_surcharge():
    # boundary: extra == 10 is NOT > 10, standard rate 30
    assert extra_weight_charge("regular", 15, "standard", False) == 300


def test_extra_just_over_ten_standard():
    # extra 11, rate 30 + 15 = 45
    assert extra_weight_charge("regular", 16, "standard", False) == 495


def test_extra_just_over_ten_express():
    # extra 11, rate 50 + 15 + 10 = 75
    assert extra_weight_charge("regular", 16, "express", False) == 825


# =====================================================
# order_acceptable
# =====================================================
def test_order_acceptable():
    assert order_acceptable(10, 20, False) is True


def test_delicate_within_limit():
    assert order_acceptable(2, 5, True) is True


def test_delicate_over_limit():
    assert order_acceptable(2, 6, True) is False


def test_order_too_heavy():
    assert order_acceptable(26, 10, False) is False


def test_order_exactly_max_weight_and_items():
    # boundaries: weight 25 allowed, items 40 allowed
    assert order_acceptable(25, 40, False) is True


def test_order_too_many_items():
    assert order_acceptable(10, 41, False) is False


# =====================================================
# dropoff_status
# =====================================================
def test_accepted_no_bedding_no_express():
    assert dropoff_status(60, False, False) == "accepted"


def test_late_no_bedding_no_express_upper():
    assert dropoff_status(59, False, False) == "late"


def test_late_no_bedding_no_express_lower():
    # boundary: cutoff - 20 = 40
    assert dropoff_status(40, False, False) == "late"


def test_rejected_no_bedding_no_express():
    assert dropoff_status(39, False, False) == "rejected"


def test_accepted_with_bedding():
    # cutoff 90
    assert dropoff_status(90, True, False) == "accepted"


def test_bedding_not_enough_time_for_accepted():
    assert dropoff_status(89, True, False) == "late"


def test_accepted_express_only():
    # cutoff 60 + 30 = 90
    assert dropoff_status(90, False, True) == "accepted"


def test_late_express_only():
    assert dropoff_status(70, False, True) == "late"


def test_rejected_express_only():
    assert dropoff_status(69, False, True) == "rejected"


def test_accepted_bedding_and_express():
    # cutoff 90 + 30 = 120
    assert dropoff_status(120, True, True) == "accepted"


def test_late_bedding_and_express():
    assert dropoff_status(100, True, True) == "late"


def test_rejected_bedding_and_express():
    assert dropoff_status(99, True, True) == "rejected"
