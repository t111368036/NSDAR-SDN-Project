from DBControll.DBConnection import DBConnection

class UserTable:
    def insert_a_user(self, user_vlan,user_ip, user_mac, user_path, user_type):
        command = "INSERT INTO user_table (user_vlan, user_ip, user_mac, user_path, user_type) VALUES  ('{}', '{}', '{}', '{}', '{}');".format(user_vlan, user_ip, user_mac, user_path, user_type)
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def pop_all_user(self):
        command = "SELECT * FROM user_table"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['user_ip'] for row in record_from_db]
    
    def pop_user_info(self, user_ip):
        command = "SELECT * FROM user_table WHERE user_ip='{}';".format(user_ip)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchone()

        return {'user_ip': record_from_db['user_ip'], 'user_mac': record_from_db['user_mac'], 'user_vlan': record_from_db['user_vlan'], 'user_path': record_from_db['user_path'], 'user_type': record_from_db['user_type']}

    def delete_user(self, user_ip):
        command = "DELETE FROM user_table WHERE user_ip='{}';".format(user_ip)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()