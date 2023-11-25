# BackEnd
# OOP-DBMS Joint Collaboration Final Project
# Advanced Computer Programming Final Project
# *****, Mico
# BSIT - 2102/2104        | BATSTATEU-The National Engineering University


"""
        since this is open to the public, i will try to describe
        every part of this code.
                                                    - C0mi (Mico)
"""

# modules required to connect python to mysql
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb
import barcode
from barcode.writer import ImageWriter
import os

def connection():
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        password='',
        db='supplychaindb'
    )
    return conn


def create_database_and_tables():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS supplychaindb")
        conn.commit()

        cursor.execute("USE supplychaindb")
        conn.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companytbl (
                companyID VARCHAR(10),
                companyName VARCHAR(255),
                companyAddress VARCHAR(255),
                companyContact VARCHAR(255),
                PRIMARY KEY (companyID)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS manufacturertbl (
                manufacturerID VARCHAR(10),
                manufacturerName VARCHAR(255),
                manufacturerAddress VARCHAR(255),
                manufacturerContact VARCHAR(255),
                PRIMARY KEY (manufacturerID)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS producttbl (
                productID VARCHAR(10),
                productName VARCHAR(255),
                stock INT(11),
                productPrice DECIMAL(10,2),
                manufacturerID VARCHAR(10),
                retailerID VARCHAR(10),
                PRIMARY KEY (productID),
                FOREIGN KEY (manufacturerID) REFERENCES manufacturertbl(manufacturerID),
                FOREIGN KEY (retailerID) REFERENCES retailertbl(retailerID)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS retailertbl (
                retailerID VARCHAR(10),
                retailerName VARCHAR(255),
                retailerAddress VARCHAR(255),
                retailerContact VARCHAR(255),
                companyID VARCHAR(10),
                PRIMARY KEY (retailerID),
                FOREIGN KEY (companyID) REFERENCES companytbl(companyID)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT,
                profile_picture_path TEXT, 
                PRIMARY KEY (username)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS barcodetbl (
                productID VARCHAR(10),
                barcodePath TEXT,
                PRIMARY KEY (productID),
                FOREIGN KEY (productID) REFERENCES producttbl(productID)
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

    except MySQLdb.Error as err:
        print(f"Error: {err}")


def check_and_create_database():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SHOW DATABASES LIKE 'supplychaindb'")
        database_exists = cursor.fetchone()

        if not database_exists:
            create_database_and_tables()

        conn.commit()
        cursor.close()
        conn.close()

    except MySQLdb.Error as err:
        print(f"Error: {err}")


def authenticate_user(username, password):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            stored_password = existing_user[1]
            if password == stored_password:
                return True
        else:
            return False

        cursor.close()
        conn.close()

    except MySQLdb.Error as err:
        print(f"Error: {err}")

    return False


def get_profile_picture_path(username):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT profile_picture_path FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            return result[0]

    except MySQLdb.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()


    return "pfp/placeholder_profile.png"


def register_user(username, password, profile_picture_path):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return False, "Username already exists."
        else:
            cursor.execute("INSERT INTO users (username, password, profile_picture_path) VALUES (%s, %s, %s)",
                           (username, password, profile_picture_path))
            conn.commit()
            return True, "User registered successfully."

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return False, f"Error: {err}"

    finally:
        cursor.close()
        conn.close()


def fetch_manufacturer_data():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM manufacturertbl")
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    except MySQLdb.Error as err:
        print(f"Error: {err}")

    return []


def fetch_manufacturer_ids():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT manufacturerID FROM manufacturertbl")
        manufacturer_ids = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return manufacturer_ids

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return []


def fetch_company_data():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM companytbl")
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    except MySQLdb.Error as err:
        print(f"Error: {err}")

    return []


def fetch_company_ids():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT companyID FROM companytbl")
        company_ids = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return company_ids

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return []


def fetch_retailer_data():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM retailertbl")
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    except MySQLdb.Error as err:
        print(f"Error: {err}")

    return []


def fetch_product_data():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM producttbl")
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    except MySQLdb.Error as err:
        print(f"Error: {err}")

    return []


def fetch_product_ids():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT productID FROM producttbl")
        product_ids = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return product_ids

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return []


def fetch_retailer_ids():
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT retailerID FROM retailertbl")
        retailer_ids = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return retailer_ids
    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return []


def add_manufacturer_data(manufacturer_id, manufacturer_name, manufacturer_address, manufacturer_contact):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT manufacturerID FROM manufacturertbl WHERE manufacturerID = %s", (manufacturer_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            return False, "Manufacturer ID already exists."
        else:
            cursor.execute(
                "INSERT INTO manufacturertbl (manufacturerID, manufacturerName, manufacturerAddress, "
                "manufacturerContact) VALUES (%s, %s, %s, %s)",
                (manufacturer_id, manufacturer_name, manufacturer_address, manufacturer_contact))
            conn.commit()
            return True, "Manufacturer added successfully."

    except MySQLdb.Error as err:
        return False, f"Error: {err}"

    finally:
        cursor.close()
        conn.close()


def add_company_data(company_id, company_name, company_address, company_contact):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT companyID FROM companytbl WHERE companyID = %s", (company_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            return False, "Company ID already exists."
        else:
            cursor.execute(
                "INSERT INTO companytbl (companyID, companyName, companyAddress, companyContact) VALUES (%s, %s, %s, "
                "%s)",
                (company_id, company_name, company_address, company_contact))
            conn.commit()
            return True, "Company added successfully."

    except MySQLdb.Error as err:
        return False, f"Error: {err}"

    finally:
        cursor.close()
        conn.close()


def add_retailer_data(retailer_id, retailer_name, retailer_address, retailer_contact, retailer_company_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT retailerID FROM retailertbl WHERE retailerID = %s", (retailer_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            return False, "Retailer ID already exists!"
        else:
            cursor.execute(
                "INSERT INTO retailertbl (retailerID, retailerName, retailerAddress, retailerContact, companyID) "
                "VALUES (%s, %s, %s, %s, %s)",
                (retailer_id, retailer_name, retailer_address, retailer_contact, retailer_company_id))
            conn.commit()
            return True, "Retailer added successfully!"

        cursor.close()
        conn.close()

    except MySQLdb.Error as err:
        print(f"Error: {err}")

    return False


def add_product_data(product_id, product_name, stock, product_price, product_manufacturer_id, product_retailer_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT productID FROM producttbl WHERE productID = %s", (product_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            return False, "Product ID already exists!"
        else:
            cursor.execute(
                "INSERT INTO producttbl (productID, productName, stock, productPrice, manufacturerID, "
                "retailerID) VALUES (%s, %s, %s, %s, %s, %s)",
                (product_id, product_name, stock, product_price, product_manufacturer_id, product_retailer_id))
            conn.commit()


            success, message = generate_and_save_barcode(product_id)

            if success:
                return True, "Product added successfully. " + message
            else:
                return False, "Product added, but barcode generation failed. " + message

    except MySQLdb.Error as err:
        print(f"Error: {err}")

    return False, "Error adding product."

def generate_and_save_barcode(product_id):
    try:
        code = barcode.get_barcode_class('code128')
        generated_code = code(product_id, writer=ImageWriter())

        barcode_path = f"barcodes/{product_id}"

        generated_code.save(barcode_path)

        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO barcodetbl (productID, barcodePath) VALUES (%s, %s)",
                       (product_id, barcode_path))
        conn.commit()

        cursor.close()
        conn.close()

        return True, f"Barcode generated and saved successfully. Path: {barcode_path}"

    except Exception as e:
        print(f"Error: {e}")
        return False, f"Error: {e}"

def update_manufacturer_data(manufacturer_id, manufacturer_name, manufacturer_address, manufacturer_contact):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT manufacturerID FROM manufacturertbl WHERE manufacturerID = %s", (manufacturer_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            cursor.execute(
                "UPDATE manufacturertbl SET manufacturerName = %s, manufacturerAddress = %s, manufacturerContact = %s "
                "WHERE manufacturerID = %s",
                (manufacturer_name, manufacturer_address, manufacturer_contact, manufacturer_id))
            conn.commit()
            return True, "Manufacturer updated successfully."
        else:
            return False, "Manufacturer not found."

        cursor.close()
        conn.close()

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return False, f"Error: {err}"


def update_company_data(company_id, company_name, company_address, company_contact):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT companyID FROM companytbl WHERE companyID = %s", (company_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            cursor.execute(
                "UPDATE companytbl SET companyName = %s, companyAddress = %s, companyContact = %s WHERE companyID = %s",
                (company_name, company_address, company_contact, company_id))
            conn.commit()
            return True, "Company updated successfully."
        else:
            return False, "Company not found."

        cursor.close()
        conn.close()

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return False, f"Error: {err}"


def update_retailer_data(retailer_id, retailer_name, retailer_address, retailer_contact, retailer_company_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT retailerID FROM retailertbl WHERE retailerID = %s", (retailer_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            cursor.execute(
                "UPDATE retailertbl SET retailerName = %s, retailerAddress = %s, retailerContact = %s, companyID = %s "
                "WHERE retailerID = %s",
                (retailer_name, retailer_address, retailer_contact, retailer_company_id, retailer_id))
            conn.commit()
            return True, "Retailer updated successfully."
        else:
            return False, "Retailer not found."

        cursor.close()
        conn.close()

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return False, f"Error: {err}"


def update_product_data(product_id, product_name, stock, product_price, product_manufacturer_id,
                        product_retailer_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT productID FROM producttbl WHERE productID = %s", (product_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            cursor.execute(
                "UPDATE producttbl SET productName = %s, stock = %s, productPrice = %s, manufacturerID = %s, "
                "retailerID = %s WHERE productID = %s",
                (product_name, stock, product_price, product_manufacturer_id, product_retailer_id, product_id))
            conn.commit()
            return True, "Product updated successfully."
        else:
            return False, "Product not found."

        cursor.close()
        conn.close()

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return False, f"Error: {err}"


def delete_manufacturer_data(manufacturer_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM manufacturertbl WHERE manufacturerID = %s", (manufacturer_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return True, "Manufacturer deleted successfully."

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return False, f"Error: {err}"


def delete_company_data(company_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM companytbl WHERE companyID = %s", (company_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return True, "Company deleted successfully."

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return False, f"Error: {err}"


def delete_retailer_data(retailer_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM retailertbl WHERE retailerID = %s", (retailer_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return True, "Retailer deleted successfully."

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return False, f"Error: {err}"


def delete_product_data(product_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT barcodePath FROM barcodetbl WHERE productID = %s", (product_id,))
        barcode_path = cursor.fetchone()

        if barcode_path:
            barcode_path = barcode_path[0]

            cursor.execute("DELETE FROM barcodetbl WHERE productID = %s", (product_id,))
            conn.commit()

            cursor.execute("DELETE FROM producttbl WHERE productID = %s", (product_id,))
            conn.commit()


            if os.path.exists(barcode_path + ".png"):
                os.remove(barcode_path + ".png")

            return True, "Product and barcode deleted successfully."

        else:

            cursor.execute("DELETE FROM producttbl WHERE productID = %s", (product_id,))
            conn.commit()

            return True, "Product deleted successfully. Barcode path not found."

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return False, f"Error: {err}"

    finally:
        cursor.close()
        conn.close()


