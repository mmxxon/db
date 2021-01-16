def print_menu():
    choice = 0
    while not (int(choice) in range(1, 24)):
        print("Select an option")
        print("1. Find seller")
        print("2. Find product")
        print("3. Find customer")
        print("4. Find order")
        print("5. Find seller product")
        print("6. Find product seller")
        print("7. Find sellers")
        print("8. Find products")
        print("9. Find customers")
        print("10. Find orders")
        print("11. Add seller")
        print("12. Add product")
        print("13. Add customer")
        print("14. Add order")
        print("15. Update seller")
        print("16. Update product")
        print("17. Update customer")
        print("18. Update order")
        print("19. Delete seller")
        print("20. Delete product")
        print("21. Delete customer")
        print("22. Delete order")
        print("23. Exit ")
        choice = input("Enter your choice:")
    return choice


def get_id():
    id = input("ID: ")
    return int(id)


def add_seller():
    ent = {}
    ent["name"] = input("Enter name:")
    ent["surname"] = input("Enter surname:")
    ent["salary"] = input("Enter salary:")
    return ent


def add_product():
    ent = {}
    ent["name"] = input("Enter name:")
    ent["category"] = input("Enter category:")
    ent["price"] = input("Enter price:")
    return ent


def add_customer():
    ent = {}
    ent["name"] = input("Enter name:")
    ent["surname"] = input("Enter surname:")
    ent["phone"] = input("Enter phone:")
    ent["email"] = input("Enter email:")
    return ent


def add_order():
    ent = {}
    ent["product_id"] = input("Enter product id:")
    ent["customer_id"] = input("Enter customer id:")
    ent["payment_type"] = input("Enter payment_type:")
    ent["delivery"] = input("Enter delivery:")
    ent["count"] = input("Enter count:")
    return ent
