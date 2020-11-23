from consolemenu.items import FunctionItem, SubmenuItem

from controller import *
from config import debug_mode

main_title = "Main Menu"
main_subtitle = ""
if debug_mode:
    main_subtitle = " (debug on)"
    open("log", "w").close()

main_menu = ConsoleMenu(main_title, main_subtitle)

customer_menu = ConsoleMenu("Customer Menu")
order_menu = ConsoleMenu("Order Menu")
product_menu = ConsoleMenu("Product Menu")
seller_menu = ConsoleMenu("Seller Menu")
seller_product = ConsoleMenu("Seller to Product Menu")

menus = [
    (customer_menu, "Customer"),
    (order_menu, "Order"),
    (product_menu, "Product"),
    (seller_menu, "Seller"),
    (seller_product, "SellerProduct"),
]

for menu, string in menus:
    menu.append_item(FunctionItem("Find All", find_all, [string]))
    menu.append_item(FunctionItem("Exact search", find_exact, [string]))
    menu.append_item(FunctionItem("Like search", find_like, [string]))
    menu.append_item(FunctionItem("Insert", insert, [string]))
    menu.append_item(FunctionItem("Delete", delete, [string]))
    menu.append_item(FunctionItem("Update", update, [string]))
    menu.append_item(FunctionItem("Generate", generate, [string]))
    menu.append_item(FunctionItem("Clear", clear, [string]))

product_menu.append_item(
    FunctionItem("Find all sellers", find_exact, ["SellerProduct", "product_id"])
)
seller_menu.append_item(
    FunctionItem("Find all products", find_exact, ["SellerProduct", "seller_id"])
)
for menu, string in menus:
    main_menu.append_item(SubmenuItem(menu.title, menu, main_menu))

main_menu.append_item(FunctionItem("Generate all", generate))
main_menu.append_item(FunctionItem("Clear all", clear))
