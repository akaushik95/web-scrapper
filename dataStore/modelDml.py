# This file contains the dml functions of model
# Since we are using file as storage writing and reading are the required operations.

import csv
import os

class StorageDml: 
    async def writeToFile(data, transaction_id = 'default'):
        try:
            filepath =  os.getcwd()+'/dataStore/localstorage.csv'
            with open(filepath, mode='a', newline='') as file:
                writer = csv.writer(file)
                for product in data:
                    writer.writerow([transaction_id, product['name'], product['price'], product['image_uri']])
            print('Data saved successfully')
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

        

    async def readFromFile():
        filepath =  os.getcwd()+'/dataStore/localstorage.csv'
        objects_list = []
        with open(filepath, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                objects_list.append({
                    'transaction_id': row['request_id'],
                    'name': row['name'],
                    'price': row['price'],
                    'image_uri': row['image_uri']
                })
        return objects_list