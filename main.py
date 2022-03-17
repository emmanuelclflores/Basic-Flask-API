import requests
import json
from flask import Flask
from datetime import datetime

app = Flask(__name__)

BASE_URL = "https://jsonmock.hackerrank.com/api"

def retrieve_params():
    try:
        with open("./ENV.json", 'r') as f:
            params = json.load(f)
        
            # Retrieve  attributes from JSON file
            start_discount_time =  params["start_discount_time"]
            end_discount_time =  params["end_discount_time"]   
            discount = params["discount"]  
            
            # Validate time params        
            # Validate format and convert to stripped datetime objects
            start_discount_time = datetime.strptime(start_discount_time, "%H:%M").time()
            end_discount_time = datetime.strptime(end_discount_time, "%H:%M").time()
            
            # Validate that start_discount_time <= end_discount_time
            if start_discount_time > end_discount_time:
                raise Exception("Start time must be before end time")
                        
            # Validate discount params     
            if discount < 0 or discount > 1:
                raise Exception("Discount must be between 0 and 1 (inclusive)")
             
    except Exception as exc:
    
        print(exc)
        
        # Default values
        start_discount_time = datetime.strptime("00:00", "%H:%M").time()
        end_discount_time = datetime.strptime("23:59", "%H:%M").time()
        discount = 0.5
        
    params = { "start_discount_time": start_discount_time, "end_discount_time": end_discount_time, "discount": discount}
    
    return params



@app.route('/api/<barcode>')
def get_discounted_price(barcode):
    # Accept a barcode
        
    # Retreve params from ENV file
    params = retrieve_params()  
    start_discount_time =  params["start_discount_time"]
    end_discount_time =  params["end_discount_time"]
    discount = params["discount"]
    
    url = f"{BASE_URL}/inventory?barcode={barcode}"
    res = requests.get(url)
    product = res.json()
    
    current_time = datetime.today().time()
    
    # Validate timeframe
    if current_time >= start_discount_time and current_time <= end_discount_time:        
        # Apply discount
        product['data'][0]['price'] *= 1 - discount   
    # Otherwise, do not apply discount (display as is directly from store API)
    
    return product

# # Sanity check
# print(get_discounted_price(74001755))