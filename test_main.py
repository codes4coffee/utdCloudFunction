import pytest
import main
import hashlib

master_hash = hashlib.md5(str.encode('[{"structure": "Parking Structure 1", "parking_green-5": 0, "parking_gold-4": 155, "parking_gold-3": 112, "parking_orange-3": 41, "parking_orange-2": 114, "parking_purple-2": 41, "parking_pay_by_space-1": 91}, {"structure": "Parking Structure 3", "parking_green-5": 0, "parking_gold-4": 166, "parking_gold-3": 102, "parking_orange-3": 65, "parking_orange-2": 108, "parking_purple-1": 32, "parking_pay_by_space-1": 33}, {"structure": "Parking Structure 4", "parking_green-5": 0, "parking_gold-4": 243, "parking_gold-3": 235, "parking_orange-2": 198, "parking_purple-2": 28, "parking_purple-1": 10, "parking_pay_by_space-1": 136}]'))

def test_getParkingSpaces():
    resp = main.getParkingSpaces("Test")
    body = resp.get_data()
    test_hash = hashlib.md5(body).hexdigest()
    assert test_hash == master_hash.hexdigest()
