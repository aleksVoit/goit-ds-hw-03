from mongo_connection import db # type: ignore
from typing import Dict, Any
from pymongo.errors import PyMongoError

cats_collection = db.cats # type: ignore

def add_cat(cat: Dict[Any, Any]): # type: ignore
    try:
        cats_collection.insert_one({'name': cat['name'], # type: ignore
                        'age': cat['age'],
                        'features': cat['features']})
    except PyMongoError as e:
        print(e)
    
def read_cats():  # type: ignore
    try:
        cats_list = list(cats_collection.find({})) # type: ignore
        print('read cats ', cats_list) # type: ignore
    except PyMongoError as e:
        print(e)

def read_cat(name: str):
    try:
        cat = cats_collection.find_one({'name': name}) # type: ignore
        print('read cat', cat) # type: ignore
    except PyMongoError as e:
        print(e)

def update_age(name: str, age: int):
    try:
        cats_collection.update_one(
            {'name': f'{name}'},
            {'$set': {'age': age}}
        )
    except PyMongoError as e:
        print(e)

def add_feature(name: str, feature: str):
    try:
        cats_collection.update_one(
            {'name': f'{name}'},
            {'$push': {'features': feature}}
        )
    except PyMongoError as e:
        print(e)

def del_by_name(name: str):
    try:
        cats_collection.delete_one(
            {'name': name}
        )
    except PyMongoError as e:
        print(e)

def delete_all_cats():
    try:
        cats_collection.delete_many({})
    except PyMongoError as e:
        print(e)


if __name__ == '__main__':
    # add_cat({'name':'Murzik', 'age': 3, 'features': ['lazy', 'stinky']})
    # update_age('Barsik', 5)
    # add_feature('Barsik', 'play')
    # del_by_name('Barsik')
    # delete_all_cats()
    # read_cat('Barsik')
    # read_cats()
    pass
