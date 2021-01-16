from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Customer(Base):
    __tablename__ = "Customer"
    customer_id = Column(Integer, nullable=False, primary_key=True)
    seller_id = Column(
        Integer, ForeignKey("Seller.seller_id", ondelete="CASCADE"), nullable=False
    )
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    order = relationship("Order", backref=backref("Cust"))

    def __init__(self, name, surname, phone, email):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email

    def __repr__(self):
        print(
            f"{str(self.name)}, {str(self.surname)}, {str(self.phone)}, {str(self.email)}"
        )


class Order(Base):
    __tablename__ = "Order"
    order_id = Column(Integer, nullable=False, primary_key=True)
    product_id = Column(
        Integer, ForeignKey("Product.product_id", ondelete="CASCADE"), nullable=False
    )
    customer_id = Column(
        Integer, ForeignKey("Customer.customer_id", ondelete="CASCADE"), nullable=False
    )
    payment_type = Column(Integer, nullable=False)
    delivery = Column(Boolean, nullable=False)
    count = Column(Integer, nullable=False)

    def __init__(self, product_id, customer_id, payment_type, delivery, count):
        self.product_id = product_id
        self.customer_id = customer_id
        self.payment_type = payment_type
        self.delivery = delivery
        self.count = count

    def __repr__(self):
        print(
            f"{str(self.product_id)}, {str(self.customer_id)}, {str(self.payment_type)}, {str(self.delivery)}, {str(self.count)}"
        )


SellerProduct = Table(
    "SellerProduct",
    Base.metadata,  # type: ignore
    Column("product_id", Integer, ForeignKey("Product.product_id")),
    Column("seller_id", Integer, ForeignKey("Seller.seller_id")),
)


class Product(Base):
    __tablename__ = "Product"
    product_id = Column(Integer, nullable=False, primary_key=True)
    name = Column(Text, nullable=False)
    category = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    seller = relationship("Seller", secondary=SellerProduct, backref=backref("Product"))
    order = relationship("Order", backref=backref("Order"))

    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price

    def __repr__(self):
        print(f"{str(self.name)}, {str(self.category)}, {str(self.price)}")


class Seller(Base):
    __tablename__ = "Seller"
    seller_id = Column(Integer, nullable=False, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    salary = Column(Integer, nullable=False)
    product = relationship(
        "Product", secondary=SellerProduct, backref=backref("sellers")
    )
    customer = relationship("Customer", backref=backref("Sellers"))

    def __init__(self, name, surname, salary):
        self.name = name
        self.surname = surname
        self.salary = salary

    def __repr__(self):
        print(f"{str(self.name)}, {str(self.surname)}, {str(self.salary)}")
