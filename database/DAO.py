from database.DB_connect import DBConnect
from model.category import Category
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from categories c"

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi(categoria):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from products p where category_id = %s"

        cursor.execute(query, (categoria,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArchi(categoria, start, end, mappa):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """with nodi as (
                    select *
                    from products p 
                    where category_id = %s),
                    possibili as (
                    select oi.* 
                    from order_items oi , orders o 
                    where o.order_id = oi.order_id 
                    and o.order_date between %s and %s
                    and oi.product_id in (select product_id from nodi))
                    select distinct p1.product_id as o1,  p2.product_id as o2
                    from possibili p1, possibili p2
                    where p1.product_id > p2.product_id"""

        cursor.execute(query, (categoria,start, end,))

        for row in cursor:
            results.append((mappa[row['o1']], mappa[row['o2']]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPesi(categoria, start, end):

        conn = DBConnect.get_connection()

        results = {}

        cursor = conn.cursor(dictionary=True)
        query = """select product_id , count(*) as numVendite, sum(quantity) as numPezzi
                    from order_items oi , orders o 
                    where o.order_id = oi.order_id 
                    and o.order_date between %s and %s
                    and oi.product_id in (select product_id
                                            from products p 
                                            where category_id = %s)
                    group by product_id """

        cursor.execute(query, (start, end, categoria,))

        for row in cursor:
            results[row['product_id']] = [row['numVendite'], row['numPezzi']]

        cursor.close()
        conn.close()
        return results
