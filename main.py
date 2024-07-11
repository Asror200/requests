from threading import Thread
from requests import get
import psycopg2


producy_url = get('https://dummyjson.com/products')
data = {'database': 'sql', 
        'user': 'postgres',
        'port': 5432, 
        'password': 4444, 
        'host': 'localhost'}

class Product:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(**data)

    def __enter__(self):
        self.cursor = self.conn.cursor()
        return self.conn , self.cursor


    @staticmethod
    def create_table():
        create_table_query = '''CREATE TABLE IF NOT EXISTS product(
                                id SERIAL PRIMARY KEY,
                                title VARCHAR(300) NOT NULL,
                                description TEXT,
                                category VARCHAR(100) NOT NULL,
                                price FLOAT4 NOT NULL,
                                discountPercentage FLOAT4 NOT NULL,
                                rating FLOAT4 NOT NULL,
                                stock INT NOT NULL,
                                tags TEXT NOT NULL,

                                sku VARCHAR(100) NOT NULL,
                                weight INT NOT NULL);'''
        return create_table_query


    @staticmethod
    def add_information():
        add_information_query = '''INSERT INTO product(title, description, category, 
                                                        price, discountPercentage, 
                                                        rating, stock, tags, sku, weight)
                                                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        
        return add_information_query
    @staticmethod
    def get_products():
        get_all_product_query = '''select * from product;'''
        return get_all_product_query

    
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.close()
            print('Closing...')
        except Exception as close_exception:
            if not exc_val:
                raise close_exception
        if exc_val:
            raise exc_val
    

product = Product()
try:
    with product as (conn, cursor):
        while True:
            
            choose: str = input('0 : creat table\n1 : add information\n2 : show database\nq : exit\nEnter your choice: ').capitalize()
           
            if choose == '0':
                query = Product.create_table()
                cursor.execute(query)
                conn.commit()
                print('Table created Successfully')
            elif choose == '1':
                query = Product.add_information()
                data = producy_url.json()['products']
                count = 0
                for info in data:
                    cursor.execute(query,(info['title'], info['description'],
                                        info['category'], info['price'], 
                                        info['discountPercentage'], info['rating'],
                                            info['stock'], info['tags'],
                                            info['sku'], info['weight']))
                    conn.commit()
                    count += 1
                print(f'{count} products added successfully')
            elif choose == '2':
                query = Product.get_products()
                cursor.execute(query)
                data = cursor.fetchall()
                count = 0
                for info in data:
                    count += 1
                    print(info)
                print(f'there are {count} products in the database')
            elif choose == 'Q':
                break
            else:
                print('Invalid choice, try again')

except Exception as e:
    raise e