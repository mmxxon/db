import psycopg2
from config import debug_mode


class DB:
    def __init__(self, user, password, host, port, db):
        try:
            self.user = user
            self.password = password
            self.host = host
            self.port = port
            self.db = db
            self.connect = None
            self.cursor = None
            self.connect = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.db,
            )
            self.connect.autocommit = True
            self.cursor = self.connect.cursor()
            print("Connection established")
        except Exception as e:
            input(f"Error: {e}")

    def __query_exec__(self, query: str):
        if debug_mode:
            with open("log", "a") as myFile:
                myFile.write(query + "---\n")
        self.cursor.execute(query)

    def __query_pag__(self, query, offset, count, sort, sortcol):
        if offset != None:
            query += f" OFFSET {str(offset)}"
        if count != None:
            query += f" LIMIT {str(count)}"
        if sort == 1 and sortcol != None:
            query += f" ORDER BY {sortcol} ASC"
        elif sort == 2 and sortcol != None:
            query += f" ORDER BY {sortcol} DESC"
        query += ";"
        self.__query_exec__(query)

    def close(self):
        if self.connect:
            self.cursor.close()
            self.connect.close()
            print("Connection closed")

    def find_all(self, entity, offset=None, count=None, sort=None, sortcol=None):
        try:
            query = f"""
            SELECT
                *
            FROM
                public."{ entity }"
            """
            self.__query_pag__(query, offset, count, sort, sortcol)
            return self.cursor.fetchall()
        except Exception as e:
            return e

    def find_by_col(
        self, entity, col, val, offset=None, count=None, sort=None, sortcol=None
    ):
        try:
            query = f"""
            SELECT
                *
            FROM
                public."{ entity }"
            WHERE
                { col } = '{ val }'
            """
            self.__query_pag__(query, offset, count, sort, sortcol)
            return self.cursor.fetchall()
        except Exception as e:
            return e

    def find_like(
        self, entity, col, val, offset=None, count=None, sort=None, sortcol=None
    ):
        try:
            query = f"""
            SELECT
                *
            FROM
                public."{ entity }" WHERE { col } LIKE '%{ val }%'
            """
            self.__query_pag__(query, offset, count, sort, sortcol)
            return self.cursor.fetchall()
        except Exception as e:
            return e

    def insert(self, entity, cols, vals):
        try:
            query = f"""
            INSERT INTO
                public."{entity}" ({ ", ".join(cols) })
            VALUES
                ({ ", ".join(vals) });
            """
            self.__query_exec__(query)
            return self.cursor.rowcount
        except Exception as e:
            return e

    def delete(self, entity, col, val):
        try:
            query = f"""
            DELETE FROM
                public."{entity}"
            WHERE
                { col } = '{ val }';
            """
            self.__query_exec__(query)
            return self.cursor.rowcount
        except Exception as e:
            return e

    def update(self, entity, cols, vals, wh_c, wh_v):
        try:
            query = f"""
            UPDATE
                public."{ entity }"
            SET
                ({ ", ".join(cols) }) = ROW({ ", ".join(vals) })
            WHERE
                { wh_c } = '{ wh_v }'
            """
            self.__query_exec__(query)
            return self.cursor.rowcount
        except Exception as e:
            return e

    def find_products(self, sel_id, offset=None, count=None, sort=None, sortcol=None):
        try:
            query = f"""
            SELECT
                public."Product".*
            FROM
            (
                select
                *
                FROM
                "SellerProduct"
                WHERE
                seller_id = { sel_id }
            ) AS selpr
            INNER JOIN
                "Product"
            ON
                selpr.product_id = "Product".product_id
            """
            self.__query_pag__(query, offset, count, sort, sortcol)
            return self.cursor.fetchall()
        except Exception as e:
            return e

    def find_sellers(self, prod_id, offset=None, count=None, sort=None, sortcol=None):
        try:
            query = f"""
            SELECT
                "Seller".*
            FROM
            (
                SELECT
                    *
                FROM
                    "SellerProduct"
                WHERE
                    product_id = { prod_id }
            ) AS selpr
            INNER JOIN
                "Seller"
            ON
                selpr.seller_id = "Seller".seller_id
            """
            self.__query_pag__(query, offset, count, sort, sortcol)
            return self.cursor.fetchall()
        except Exception as e:
            return e

    def generate_seller(self, count):
        try:
            query = f"""
            INSERT INTO
                public."Seller" (name, surname, salary)
            SELECT
                md5(random() :: text) as name,
                md5(random() :: text) as surname,
                trunc(random() * 30000) as salary
            FROM
                generate_series(1, {count})
            """
            self.__query_exec__(query)
            return self.cursor.rowcount
        except Exception as e:
            return e

    def generate_product(self, count):
        try:
            query = f"""
            INSERT INTO
                public."Product" (name, category, price)
            SELECT
                md5(random() :: text) as name,
                md5(random() :: text) as category,
                trunc(random() * 15000) as price
            FROM
                generate_series(1, {count})
            """
            self.__query_exec__(query)
            return self.cursor.rowcount
        except Exception as e:
            return e

    def generate_order(self, count):
        try:
            query = f"""
            WITH test_count AS (
                SELECT
                    generate_series(1, {count}) as id
                )
            INSERT INTO
                "Order"(product_id, customer_id, payment_type, delivery, count)
            SELECT
                (
                    SELECT
                    "Product".product_id
                    FROM
                    "Product"
                    WHERE
                    tc.id IS NOT NULL
                    ORDER BY
                    random()
                    LIMIT
                    1
                ) as product_id,
                (
                    SELECT
                    "Customer".customer_id
                    FROM
                    "Customer"
                    WHERE
                    tc.id IS NOT NULL
                    ORDER BY
                    random()
                    LIMIT
                    1
                ) as customer_id,
                    trunc(random() * 5) as payment_type,
                    (round(random())::int)::boolean as delivery,
                    trunc(random() * 40) as count
            FROM
                test_count tc
            """
            self.__query_exec__(query)
            return self.cursor.rowcount
        except Exception as e:
            return e

    def generate_customer(self, count):
        try:
            query = f"""
            WITH test_count AS (
                SELECT
                    generate_series(1, {count}) as id
                )
            INSERT INTO
                "Customer"(seller_id, name, surname, phone, email)
            SELECT
                (
                    SELECT
                    "Seller".seller_id
                    FROM
                    "Seller"
                    WHERE
                    tc.id IS NOT NULL
                    ORDER BY
                    random()
                    LIMIT
                    1
                ) as seller_id,
                md5(random() :: text) as name,
                md5(random() :: text) as surname,
                (
                    SELECT
                    format(
                        '(%s%s%s) %s%s%s-%s%s%s%s',
                        a [1],
                        a [2],
                        a [3],
                        a [4],
                        a [5],
                        a [6],
                        a [7],
                        a [8],
                        a [9],
                        a [10]
                    )
                    FROM
                    (
                        SELECT
                        ARRAY (
                            SELECT
                            trunc(random() * 10) :: int
                            FROM
                            generate_series(1, 10)
                            WHERE
                                tc.id IS NOT NULL
                        ) AS a
                    ) as sub
                ) as phone,
                md5(random() :: text) || '@gmail.com' as email
            FROM
                test_count tc
            """
            self.__query_exec__(query)
            return self.cursor.rowcount
        except Exception as e:
            return e

    def generate_selpr(self, count):
        try:
            query = f"""
            WITH test_count AS (
                SELECT
                    generate_series(1, { count }) as id
            )
            INSERT INTO
                "SellerProduct" (seller_id, product_id)
            SELECT
                (
                    SELECT
                    "Seller".seller_id
                    FROM
                    "Seller"
                    WHERE
                    tc.id IS NOT NULL
                    ORDER BY
                    random()
                    LIMIT
                    1
                ), (
                    SELECT
                    "Product".product_id
                    FROM
                    "Product"
                    WHERE
                    tc.id IS NOT NULL
                    ORDER BY
                    random()
                    LIMIT
                    1
                )
            FROM
                test_count tc
            """
            self.__query_exec__(query)
            return self.cursor.rowcount
        except Exception as e:
            return e

    def generate(self, count):
        try:
            arr = []
            arr.append(self.generate_seller(count))
            arr.append(self.generate_product(count))
            arr.append(self.generate_selpr(count))
            arr.append(self.generate_customer(count))
            arr.append(self.generate_order(count))
            return arr
        except Exception as e:
            return e

    def clear(self, name=None):
        try:
            query = "TRUNCATE TABLE "
            if name is None:
                query += '"Seller", "Product", "SellerProduct", "Order", "Customer"'
            else:
                query += f'"{name}"'
            self.__query_exec__(query)
            return self.cursor.rowcount
        except Exception as e:
            return e

    def reset_serial(self, num=None):
        try:
            ser = [
                "Seller_seller_id_seq",
                "Product_product_id_seq",
                "SellerProduct_link_id_seq",
                "Order_order_id_seq",
                "Customer_customer_id_seq",
            ]
            arr = []
            if num is None:
                arr = ser
            else:
                arr = [ser[num]]
            for i in arr:
                self.__query_exec__(f'ALTER SEQUENCE "{i}" RESTART WITH 1')
            return 1
        except Exception as e:
            return e
