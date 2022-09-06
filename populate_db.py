from app.common.utils import (get_random_dni_customers_list, get_random_size, get_random_ingredient,
                              get_random_beverage, get_random_names_list, get_random_address_customers_list,
                              get_random_address_customers_list, get_random_order, get_random_order_detail,
                              get_random_phone_customers_list)
from sqlalchemy import create_engine, MetaData

import os
import random


def insert_random_item(table_name, position):
    data = dict()
    table = None
    
    if table_name == 'size':
        data = get_random_size(position)
        table = meta_data.tables['size']
    elif table_name == 'beverage':
        data = get_random_beverage(position)
        table = meta_data.tables['beverage']
    else:
        data = get_random_ingredient(position)
        table = meta_data.tables['ingredient']
    
    new_data_db = table.insert().values(data).return_defaults()
    result = new_data_db.execute()
    return result.inserted_primary_key_rows[0]


def insert_order_order_detail_data(data, table_name):
    table = meta_data.tables[table_name]
    new_data_db = table.insert().values(data).return_defaults()
    result = new_data_db.execute()
    return result.inserted_primary_key_rows[0]


def get_element_by_id(table_name, id):
    query_text = f"select * from {table_name} where _id = {id}"
    result = connection.execute(query_text).fetchall()
    return dict(result[0])


def get_elements_by_random_id(table_name, id_list):
    elements_number = random.randint(1, len(id_list))
    elements = []

    for _ in range(elements_number):
        position = random.randint(0, len(id_list)-1)
        choosed_element = get_element_by_id(table_name, id_list[position])
        elements.append(choosed_element)
    return elements


def calculate_price(size, ingredients, beverages):
    total_price = size['price']
    
    for ingredient in ingredients:
        total_price += ingredient['price']
    for beverage in beverages:
        total_price += beverage['price']
        
    return total_price


def insert_order_order_detail_element(sizes_id,
                                      ingredients_id,
                                      beverages_id,
                                      customers_names,
                                      customers_dni,
                                      customers_phones,
                                      customers_address):
     # select one size for the order
    size_id = random.choice(sizes_id)
    size = get_element_by_id('size', size_id) 
    
    # get ingredients and beverage by id (random)
    ingredients = get_elements_by_random_id('ingredient', ingredients_id)
    beverages =get_elements_by_random_id('beverage', beverages_id)
    
    total_price = calculate_price(size, ingredients, beverages)
    order_data = get_random_order(customers_names[random.randint(0, len(customers_names)-1)],
                                       customers_dni[random.randint(0, len(customers_dni)-1)],
                                       customers_phones[random.randint(0, len(customers_phones)-1)],
                                       customers_address[random.randint(0, len(customers_address)-1)],
                                       total_price,
                                       size['_id'])
    
    order_id = insert_order_order_detail_data(order_data, 'order')
    
    # generate order detail
    for ingredient in ingredients:
        order_detail_data = get_random_order_detail(ingredient['price'], order_id[0], ingredient['_id'], None, None)
        insert_order_order_detail_data(order_detail_data, 'order_detail')
    
    for beverage in beverages:
        order_detail_data = get_random_order_detail(None, order_id[0], None, beverage['price'], beverage['_id'])
        insert_order_order_detail_data(order_detail_data, 'order_detail')


def populate_table(elements_number, table_name):
    elements_id = []
    
    for index in range(elements_number):
        if table_name == 'beverage':
            id = insert_random_item('beverage', index)
        elif table_name == 'ingredient':
            id = insert_random_item('ingredient', index)
        else:
            id = insert_random_item('size', index)
        elements_id.append(id[0])
    
    return elements_id


def populate_table_order_order_detail(order_number,
                                      sizes_id,
                                      ingredients_id,
                                      beverages_id,
                                      customers_names,
                                      customers_dni,
                                      customers_phones,
                                      customers_address):
    
    for _ in range(order_number):
        
        insert_order_order_detail_element(sizes_id,
                                          ingredients_id,
                                          beverages_id,
                                          customers_names,
                                          customers_dni,
                                          customers_phones,
                                          customers_address)


def populate_database(customers_number,
                      size_number,
                      ingredient_number,
                      beverage_number,
                      order_number):
    
    customers_names = get_random_names_list(customers_number)
    customers_dni = get_random_dni_customers_list(customers_number)
    customers_phones = get_random_phone_customers_list(customers_number)
    customers_address = get_random_address_customers_list(customers_number)
    
    sizes_id = populate_table(size_number, 'size')
    ingredients_id = populate_table(ingredient_number, 'ingredient')
    beverages_id = populate_table(beverage_number, 'beverage')
    
    populate_table_order_order_detail(order_number,
                                      sizes_id,
                                      ingredients_id,
                                      beverages_id,
                                      customers_names,
                                      customers_dni,
                                      customers_phones,
                                      customers_address)
    

if __name__ == "__main__":
    
    BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pizza.sqlite'), echo=False)
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    meta_data = MetaData(bind=engine)
    MetaData.reflect(meta_data)
    connection = engine.connect()
    
    populate_database(15, 5, 10, 5, 150)
