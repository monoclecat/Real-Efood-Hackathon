import json


def imageRecognition(base64):
    # call MC Vision API and parse data
    test_json = {
         "address": "",
         "city": "",
         "plz": "",
         "products": {
           "BEB,FLEISCH": {
             "amount": 1,
             "price": "2,16"
           },
           "BLUTWURST 4009": {
             "amount": 1,
             "price": "2,99"
           },
           "HAUSMACHER BLUT\"UR": {
             "amount": 1,
             "price": "2,99"
           },
           "HAUSMACHER LEBERUU": {
             "amount": "2",
             "price": "5,98"
           },
           "KETCHUP": {
             "amount": 1,
             "price": "1,69"
           },
           "KOELLN HUESLI": {
             "amount": 1,
             "price": "5,79"
           },
           "LAYS CHIPS 1759": {
             "amount": "2",
             "price": "1,58"
           },
           "RPF-ELUEIN PUR": {
             "amount": "2",
             "price": "0,50"
           }
         },
         "timestamp": "2017-12-07 19:43:00"
        }
    return test_json
