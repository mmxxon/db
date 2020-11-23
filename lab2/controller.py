from consolemenu import ConsoleMenu, SelectionMenu, Screen
from consolemenu.items import FunctionItem

from config import *
from database import DB

db = DB(db_user, None, db_host, db_port, db_database)

columns = {
    "Customer": (
        "customer_id",
        "seller_id",
        "name",
        "surname",
        "phone",
        "email",
    ),
    "Order": (
        "order_id",
        "product_id",
        "customer_id",
        "payment_type",
        "delivery",
        "count",
    ),
    "Product": ("product_id", "name", "category", "price"),
    "Seller": ("seller_id", "name", "surname", "salary"),
    "SellerProduct": ("link_id", "product_id", "seller_id"),
}


def process_data(name, data, page, nested=None):
    if isinstance(data, Exception):
        Screen().input(f"DError: {data}")
        return
    subtitle = "".join(f"{i} " for i in columns[name])
    arr = [f" Page {page - 1}", f" Page {page + 1}"]
    for en in data:
        arr.append(" ".join(map(str, en)))
    sel = SelectionMenu.get_selection(arr, subtitle)
    if sel in range(2, len(arr)):
        subtitle = ""
        for i in range(len(columns[name])):
            subtitle += f"{columns[name][i]}: {data[sel - 2][i]}; "
        menu = ConsoleMenu("Item actions", subtitle)
        if name == "Seller" and nested == None:
            menu.append_item(
                FunctionItem("Find products", find_products, [data[sel - 2][0], 1])
            )
        elif name == "Product" and nested == None:
            menu.append_item(
                FunctionItem("Find sellers", find_sellers, [data[sel - 2][0], 1])
            )
        menu.append_item(
            FunctionItem("Edit", update, [name, columns[name][0], data[sel - 2][0]])
        )
        menu.append_item(
            FunctionItem("Delete", delete, [name, columns[name][0], data[sel - 2][0]])
        )
        menu.show()
    elif sel < 2:
        return sel + 1


def find_all(name):
    try:
        page = 1
        per_page = 15
        while True:
            data = db.find_all(name, (page - 1) * per_page, per_page)
            proc = process_data(name, data, page)
            if proc == 1 and page > 1:
                page -= 1
            elif proc == 2:
                page += 1
            else:
                break
    except Exception as e:
        Screen().input("\n".join([f"CError: {e}", "Press any key to continue..."]))


def find_exact(name, col=None):
    try:
        page = 1
        per_page = 15
        if col == None:
            col = columns[name][
                SelectionMenu.get_selection(
                    [i for i in columns[name]],
                    show_exit_option=False,
                    title="Choose column to search",
                )
            ]
        val = Screen().input("Enter search: ")
        while True:
            data = db.find_by_col(name, col, val, (page - 1) * per_page, per_page)
            proc = process_data(name, data, page)
            if proc == 1 and page > 1:
                page -= 1
            elif proc == 2:
                page += 1
            else:
                break
    except Exception as e:
        Screen().input("\n".join([f"CError: {e}", "Press any key to continue..."]))


def find_like(name):
    try:
        page = 1
        per_page = 15
        col = columns[name][
            SelectionMenu.get_selection(
                [i for i in columns[name]],
                show_exit_option=False,
                title="Choose column to search",
            )
        ]
        val = Screen().input("Enter search: ")
        while True:
            data = db.find_like(name, col, val, (page - 1) * per_page, per_page)
            proc = process_data(name, data, page)
            if proc == 1 and page > 1:
                page -= 1
            elif proc == 2:
                page += 1
            else:
                break
    except Exception as e:
        Screen().input("\n".join([f"CError: {e}", "Press any key to continue..."]))


def find_products(sel_id, nested):
    try:
        page = 1
        per_page = 15
        while True:
            data = db.find_products(sel_id, (page - 1) * per_page, per_page)
            proc = process_data("Product", data, page, nested)
            if proc == 1 and page > 1:
                page -= 1
            elif proc == 2:
                page += 1
            else:
                break
    except Exception as e:
        Screen().input("\n".join([f"CError: {e}", "Press any key to continue..."]))


def find_sellers(prod_id, nested):
    try:
        page = 1
        per_page = 15
        while True:
            data = db.find_sellers(prod_id, (page - 1) * per_page, per_page)
            proc = process_data("Seller", data, page, nested)
            if proc == 1 and page > 1:
                page -= 1
            elif proc == 2:
                page += 1
            else:
                break
    except Exception as e:
        Screen().input("\n".join([f"CError: {e}", "Press any key to continue..."]))


def insert(name):
    try:
        cols = []
        vals = []
        val = 0
        Screen().println('Enter columns, text values must be surrounded by "\'"')
        Screen().println("Empty lines will be ignored")
        for i in range(1, len(columns[name])):
            col = columns[name][i]
            val = Screen().input(f"{(col)}: ")
            if bool(val and not val.isspace()):
                cols.append(col)
                vals.append(val)
        en = db.insert(name, cols, vals)
        if isinstance(en, Exception):
            Screen().input(f"Derror: {en}")
            return
        if name == "Seller":
            prod_ids = Screen().input("Enter products id's, separated by commas: ")
            ens_arr = []
            for prod_id in prod_ids.split(","):
                ens_arr.append(
                    f"""(
                    { prod_id },
                    { str(en[0][0]) }
                )"""
                )
            ens = db.insert("SellerProduct", ["product_id", "seller_id"], [ens_arr])
            if isinstance(ens, Exception):
                Screen().input(f"Derror: {ens}")
                return
            else:
                Screen().println(f"Inserted { len(ens) } items")
        elif name == "Product":
            sell_ids = Screen().input("Enter sellers id's, separated by commas: ")
            ens_arr = []
            for sell_id in sell_ids.split(","):
                ens_arr.append(
                    f"""(
                    { sell_id },
                    { str(en[0][0]) }
                )"""
                )
            ens = db.insert(
                "SellerProduct",
                ["seller_id", "product_id"],
                [ens_arr],
            )
            if isinstance(ens, Exception):
                Screen().input(f"Derror: {ens}")
                return
            else:
                Screen().println(f"Inserted { ens } items")
    except Exception as e:
        Screen().input("\n".join([f"CError: {e}", "Press any key to continue..."]))


def delete(name, col_search=None, val_search=None):
    try:
        if col_search == None:
            col_search = columns[name][
                SelectionMenu.get_selection(
                    [i for i in columns[name]],
                    show_exit_option=False,
                    title="Choose column to search",
                )
            ]
        if val_search == None:
            val_search = Screen().input("Enter value to delete: ")
        ens = db.delete(name, col_search, val_search)
        if isinstance(ens, Exception):
            Screen().input(f"Derror: { ens }")
            return
        else:
            Screen().input(f"Deleted { ens } items")
    except Exception as e:
        Screen().input("\n".join([f"CError: {e}", "Press any key to continue..."]))


def update(name, col_search=None, val_search=None):
    try:
        cols = []
        vals = []
        val = 0
        if col_search == None:
            col_search = columns[name][
                SelectionMenu.get_selection(
                    [i for i in columns[name]],
                    show_exit_option=False,
                    title="Choose column to search",
                )
            ]
        if val_search == None:
            val_search = Screen().input("Enter value to update: ")
        Screen().println('Enter columns, text values must be surrounded by "\'"')
        Screen().println("Empty lines will be ignored")
        for i in range(1, len(columns[name])):
            col = columns[name][i]
            val = Screen().input(f"{(col)}: ")
            if bool(val and not val.isspace()):
                cols.append(col)
                vals.append(val)
        ens = db.update(name, cols, vals, col_search, val_search)
        if isinstance(ens, Exception):
            Screen().input(f"Derror: {ens}")
            return
        else:
            Screen().input(f"Updated { ens } items")
    except Exception as e:
        Screen().input("\n".join([f"CError: {e}", "Press any key to continue..."]))


def generate(name=None):
    try:
        count = ""
        string = ""
        while not count.isdigit():
            count = Screen().input("Enter count: ")
        if name is None:
            ret = db.generate(count)
            if isinstance(ret, Exception):
                Screen().input(f"Gerror: {ret}")
                return
            string = f"Generated {ret[0]} sel, {ret[1]} prod. {ret[2]} sel-prod rel, {ret[3]} cust, {ret[4]} orders"
        elif name is "Seller":
            ret = db.generate_seller(count)
            if isinstance(ret, Exception):
                Screen().input(f"Gerror: {ret}")
                return
            string = f"Generated {ret} sellers"
        elif name is "Product":
            ret = db.generate_product(count)
            if isinstance(ret, Exception):
                Screen().input(f"Gerror: {ret}")
                return
            string = f"Generated {ret} products"
        elif name is "SellerProduct":
            ret = db.generate_selpr(count)
            if isinstance(ret, Exception):
                Screen().input(f"Gerror: {ret}")
                return
            string = f"Generated {ret} seller-product relations"
        elif name is "Order":
            ret = db.generate_order(count)
            if isinstance(ret, Exception):
                Screen().input(f"Gerror: {ret}")
                return
            string = f"Generated {ret} orders"
        elif name is "Customer":
            ret = db.generate_customer(count)
            if isinstance(ret, Exception):
                Screen().input(f"Gerror: {ret}")
                return
            string = f"Generated {ret} customers"
        Screen().input(string)
    except Exception as e:
        Screen().input("\n".join([f"CError: {e}", "Press any key to continue..."]))


def clear(name=None):
    try:
        string = ""
        answer = Screen().input("Are you sure?(yes/no): ")
        if answer != "yes":
            Screen().input(answer)
            return
        if name is None:
            ret = db.clear()
            if isinstance(ret, Exception):
                Screen().input(f"Gerror: {ret}")
                return
            ret2 = db.reset_serial()
            if isinstance(ret2, Exception):
                Screen().input(f"Gerror: {ret2}")
                return
            string = f"Deleted all"
        elif name is "Seller":
            ret = db.clear(name)
            if isinstance(ret, Exception):
                Screen().input(f"Gerror: {ret}")
                return
            ret2 = db.reset_serial(0)
            if isinstance(ret2, Exception):
                Screen().input(f"Gerror: {ret2}")
                return
            string = f"Deleted {ret} sellers"
        elif name is "Product":
            ret = db.clear(name)
            if isinstance(ret, Exception):
                Screen().input(f"Gerror: {ret}")
                return
            ret2 = db.reset_serial(1)
            if isinstance(ret2, Exception):
                Screen().input(f"Gerror: {ret2}")
                return
            string = f"Deleted {ret} products"
        elif name is "SellerProduct":
            ret = db.clear(name)
            if isinstance(ret, Exception):
                Screen().input(f"Gerror: {ret}")
                return
            ret2 = db.reset_serial(2)
            if isinstance(ret2, Exception):
                Screen().input(f"Gerror: {ret2}")
                return
            string = f"Deleted {ret} sel-pr relations"
        elif name is "Order":
            ret = db.clear(name)
            if isinstance(ret, Exception):
                Screen().input(f"Gerror: {ret}")
                return
            ret2 = db.reset_serial(3)
            if isinstance(ret2, Exception):
                Screen().input(f"Gerror: {ret2}")
                return
            string = f"Deleted {ret} orders"
        elif name is "Customer":
            ret = db.clear(name)
            if isinstance(ret, Exception):
                Screen().input(f"Gerror: {ret}")
                return
            ret2 = db.reset_serial(4)
            if isinstance(ret2, Exception):
                Screen().input(f"Gerror: {ret2}")
                return
            string = f"Deleted {ret} customers"
        Screen().input(string)
    except Exception as e:
        Screen().input("\n".join([f"CError: {e}", "Press any key to continue..."]))
