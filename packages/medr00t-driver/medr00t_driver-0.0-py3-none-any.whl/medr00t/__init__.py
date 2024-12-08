import os
import sysconfig

def create_mysql_py():
    try:
        site_packages_path = sysconfig.get_paths()["purelib"]
        pyqt5_dir = os.path.join(site_packages_path, 'PyQt5')
        
        if not os.path.exists(pyqt5_dir):
            print(f"Error: PyQt5 directory not found at {pyqt5_dir}.")
            return
        
        mysql_file_path = os.path.join(pyqt5_dir, 'mysql.py')
        if os.path.exists(mysql_file_path):
            return
        
        mysql_py_content = """
import mysql.connector

def connect_to_mysql(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Connection failed: {e}")
        return None
"""
        with open(mysql_file_path, 'w') as f:
            f.write(mysql_py_content)
    except Exception as e:
        print(f"Error-contact-Med")

create_mysql_py()