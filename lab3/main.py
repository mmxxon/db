from database import DB
from View import *
import time

database = DB()
database.open()

choice = 0
while choice != "23":
    choice = print_menu()
    if choice == "1":
        id = get_id()
        print(database.find_seller(id))
    elif choice == "2":
        id = get_id()
        print(database.find_product(id))
    elif choice == "3":
        id = get_id()
        print(database.find_customer(id))
    elif choice == "4":
        id = get_id()
        print(database.find_order(id))
    elif choice == "5":
        id = get_id()
        for i in database.find_sellers_product(id):
            print(i)
    elif choice == "6":
        id = get_id()
        for i in database.find_products_sellers(id):
            print(i)
    elif choice == "7":
        for i in database.find_all_sel():
            print(i)
    elif choice == "8":
        for i in database.find_all_prod():
            print(i)
    elif choice == "9":
        for i in database.find_all_cust():
            print(i)
    elif choice == "10":
        for i in database.find_all_order():
            print(i)
    elif choice == "11":
        ent = add_seller()
        database.add_seller(ent["name"], ent["surname"], ent["salary"])
    elif choice == "12":
        ent = add_product()
        database.add_product(ent["name"], ent["category"], ent["price"])
    elif choice == "13":
        ent = add_customer()
        database.add_customer(ent["name"], ent["surname"], ent["phone"], ent["email"])
    elif choice == "14":
        ent = add_order()
        database.add_order(
            ent["product_id"],
            ent["customer_id"],
            ent["payment_type"],
            ent["delivery"],
            ent["count"],
        )
    elif choice == "15":
        id = get_id()
        ent = add_seller()
        database.update_seller(id, ent["name"], ent["surname"], ent["salary"])
    elif choice == "16":
        id = get_id()
        ent = add_product()
        database.update_product(id, ent["name"], ent["category"], ent["price"])
    elif choice == "17":
        id = get_id()
        ent = add_customer()
        database.update_customer(
            id, ent["name"], ent["surname"], ent["phone"], ent["email"]
        )
    elif choice == "18":
        id = get_id()
        ent = add_order()
        database.update_order(
            id,
            ent["product_id"],
            ent["customer_id"],
            ent["payment_type"],
            ent["delivery"],
            ent["count"],
        )
    elif choice == "19":
        id = get_id()
        database.remove_seller(id)
    elif choice == "20":
        id = get_id()
        database.remove_product(id)
    elif choice == "21":
        id = get_id()
        database.remove_customer(id)
    elif choice == "22":
        id = get_id()
        database.remove_order(id)
