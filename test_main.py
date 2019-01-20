import pytest
import main
import hashlib

master_hash = hashlib.md5(str.encode('[{"structure": "Parking Structure 1", "hasInfo": true, "green": 0, "gold": 267, "orange": 155, "purple": 41, "pay_by_space": 91}, {"structure": "Parking Structure 3", "hasInfo": true, "green": 0, "gold": 268, "orange": 173, "purple": 32, "pay_by_space": 33}, {"structure": "Parking Structure 4", "hasInfo": true, "green": 0, "gold": 478, "orange": 198, "purple": 38, "pay_by_space": 136}]'))

def test_getParkingSpaces():
    resp = main.getParkingSpaces("Test")
    body = resp.get_data()
    print (body)
    test_hash = hashlib.md5(body).hexdigest()
    assert test_hash == master_hash.hexdigest()
