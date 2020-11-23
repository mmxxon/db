#!python
from controller import db
from view import main_menu

if __name__ == "__main__":
    main_menu.show()
    db.close()
