import psycopg2
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from models import *


class DB:
    def __init__(self):
        self.s = None

    def open(self):
        try:
            DATABASE_URI = "postgres://xon@localhost:5432/postgres"
            engine = create_engine(DATABASE_URI)
            Session = sessionmaker(engine)
            self.s = Session()
            print("Connect")
        except (Exception, exc.SQLAlchemyError) as error:
            print("Can`t connect to data base", error)

    def close(self):
        self.s.close()

    def find_seller(self, id):
        try:
            query = self.s.query(Seller).get(id)
            print(query)
            if query:
                return query
            else:
                return "Error"
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def find_product(self, id):
        try:
            query = self.s.query(Product).get(id)
            print(query)
            if query:
                return query
            else:
                return "Error"
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def find_customer(self, id):
        try:
            query = self.s.query(Customer).get(id)
            print(query)
            if query:
                return query
            else:
                return "Error"
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def find_order(self, id):
        try:
            query = self.s.query(Order).get(id)
            print(query)
            if query:
                return query
            else:
                return "Error"
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def find_sellers_product(self, seller_id):
        try:
            query = self.s.query(Seller).get(seller_id).product
            self.s.commit()
            if query:
                return query
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def find_products_sellers(self, id):
        try:
            query = self.s.query(Product).get(id).seller
            self.s.commit()
            if query:
                return query
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def find_all_sel(self):
        try:
            query = self.s.query(Seller).all()
            self.s.commit()
            if query:
                return query
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def find_all_prod(self):
        try:
            query = self.s.query(Product).all()
            self.s.commit()
            if query:
                return query
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def find_all_cust(self):
        try:
            query = self.s.query(Customer).all()
            self.s.commit()
            if query:
                return query
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def find_all_order(self):
        try:
            query = self.s.query(Order).all()
            self.s.commit()
            if query:
                return query
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def find_all_selpr(self):
        try:
            query = self.s.query(SellerProduct).all()
            self.s.commit()
            if query:
                return query
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def add_seller(self, name, surname, salary):
        try:
            query = Seller(name, surname, salary)
            self.s.add(query)
            self.s.commit()
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()
        else:
            return "Add is successful"

    def add_product(self, name, category, price):
        try:
            query = Product(name, category, price)
            self.s.add(query)
            self.s.commit()
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()
        return "Add is successful"

    def add_order(self, product_id, customer_id, payment_type, delivery, count):
        try:
            query = Order(product_id, customer_id, payment_type, delivery, count)
            self.s.add(query)
            self.s.commit()
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()
        return "Add is successful"

    def add_customer(self, name, surname, phone, email):
        try:
            query = Customer(name, surname, phone, email)
            self.s.add(query)
            self.s.commit()
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()
        return "Add is successful"

    def update_seller(self, id, name, surname, salary):
        try:
            self.s.query(Seller).filter_by(id).update(
                {Seller.name: name, Seller.surname: surname, Seller.salary: salary}
            )
            self.s.commit()
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()
        else:
            return "Update is successful"

    def update_product(self, id, name, category, price):
        try:
            self.s.query(Product).filter_by(id).update(
                {Product.name: name, Product.category: category, Product.price: price}
            )
            self.s.commit()
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()
        else:
            return "Update is successful"

    def update_customer(self, id, name, surname, phone, email):
        try:
            self.s.query(Customer).filter_by(id).update(
                {
                    Customer.name: name,
                    Customer.surname: surname,
                    Customer.phone: phone,
                    Customer.email: email,
                }
            )
            self.s.commit()
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()
        else:
            return "Update is successful"

    def update_order(self, id, product_id, customer_id, payment_type, delivery, count):
        try:
            self.s.query(Order).filter_by(id).update(
                {
                    Order.product_id: product_id,
                    Order.customer_id: customer_id,
                    Order.payment_type: payment_type,
                    Order.delivery: delivery,
                    Order.count: count,
                }
            )
            self.s.commit()
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()
        else:
            return "Update is successful"

    def remove_seller(self, id):
        try:
            query = self.find_seller(id)
            if type(query) is not Seller:
                return "Can`t find id"
            self.s.delete(query)
            self.s.commit()
            return "Delete is successful"
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def remove_product(self, id):
        try:
            query = self.find_product(id)
            if type(query) is not Product:
                return "Can`t find id"
            self.s.delete(query)
            self.s.commit()
            return "Delete is successful"
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def remove_customer(self, id):
        try:
            query = self.find_customer(id)
            if type(query) is not Customer:
                return "Can`t find id"
            self.s.delete(query)
            self.s.commit()
            return "Delete is successful"
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()

    def remove_order(self, id):
        try:
            query = self.find_order(id)
            if type(query) is not Order:
                return "Can`t find id"
            self.s.delete(query)
            self.s.commit()
            return "Delete is successful"
        except (Exception, exc.SQLAlchemyError) as error:
            self.s.rollback()
