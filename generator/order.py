from time import sleep
from datetime import datetime
import json
import os
import random
import logging
from sys import stdout


logging.basicConfig(level=logging.INFO, stream=stdout,
                    format="%(levelname)s %(asctime)s: %(message)s ")


def generate_order(id):
    customer_gender = random.choice(('male', 'female'))
    with open('../files/samples/names.json') as file:
        names = json.load(file)
        customer_name = f'{random.choice(names["names"][customer_gender])} {random.choice(names["surnames"][customer_gender])}'
    with open("../files/samples/addresses.json") as file:
        addresses = json.load(file)
        address_dict = random.choice(addresses)
        address = f'{address_dict["street"]}, {address_dict["house"]}, {address_dict["city"]}'
    restaurant_id = random.randint(1, 20)
    contact_number = "+7" + \
        "".join([str(random.randint(0, 9)) for _ in range(9)])
    items = generate_order_items()
    status = "Preparing"
    return {
        "orderid": id,
        "customername": customer_name,
        "deliveryaddress": address,
        "contactnumber": contact_number,
        "restaurantid": restaurant_id,
        "items": items,
        "status": status
    }


def generate_order_items():
    items_list = list()
    with open("../files/samples/items.json") as file:
        items = json.load(file)
    for _ in range(random.randint(1, 6)):
        while True:
            item = random.choice(items["items"])
            if all(x["item_id"] != item["item_id"] for x in items_list):
                break

        quantity = random.randint(1, 5)
        items_list.append({"item_id": item["item_id"],
                           "item_name": item["name"],
                           "quantity": quantity,
                           "price": item["price"]*quantity})
    return items_list


if __name__ == "__main__":
    latest_id = 1
    while True:
        creation_time = datetime.strftime(datetime.now(), '%d-%m-%Y_%H:%M:%S')
        filename = f"order_{latest_id}_{creation_time}.json"
        with open(f"../files/orders/{filename}", "w") as file:
            order = generate_order(latest_id)
            json.dump(order, file, ensure_ascii=False, indent=4)
        latest_id += 1
        logging.info(f'successfully generated new file {filename}')
        sleep(random.randint(10, 30))
