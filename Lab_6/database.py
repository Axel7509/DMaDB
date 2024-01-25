from datetime import datetime

import psycopg2


class Database:

    def __init__(self):
        self.__connection = psycopg2.connect(
            host='localhost',
            port='5432',
            dbname='test',
            user='postgres',
            password='qwerty'
        )
        self.__cursor = self.__connection.cursor()

    def sign_in(self, username: str, password: str) -> tuple:
        """
        :return: tuple of strings: username, is_staff, is_superuser
        """

        try:
            query = "SELECT * FROM patient WHERE username = %s AND password = %s;"

            self.__cursor.execute(query, (username, password))

            response = self.__cursor.fetchone()

            if response:
                return response[0], False, False
            else:

                query_2 = "SELECT * FROM staff WHERE email = %s AND password = %s;"

                self.__cursor.execute(query_2, (username, password))

                response_2 = self.__cursor.fetchone()

                if response_2:
                    if response_2[5] == "Admin":
                        return response_2[2], False, True
                    else:
                        return response_2[2], True, False
                else:
                    return tuple()
        except Exception as e:
            return None

    def sign_up(self, first_name: str, last_name: str, username: str, password: str,
                email: str, age: int, phone: int) -> bool:
        try:
            query = "insert into patient (first_name, last_name, username, password, email," \
                    " age, phone) values (%s, %s, %s, %s, %s, %s, %s);"

            self.__cursor.execute(query, (first_name, last_name, username, password, email, age, phone))
            self.__connection.commit()

            return True

        except Exception as e:
            self.__connection.rollback()
            print(e)
            return False

    def table_len(self, table_name: str) -> int:
        try:
            query = f"SELECT COUNT(*) FROM {table_name};"
            self.__cursor.execute(query)
            row_count = self.__cursor.fetchone()[0]

            return row_count

        except Exception as e:
            return None

    def get_data(self, table_name: str, amount: int, order_by: str) -> list:
        try:
            query = f"SELECT * FROM {table_name} ORDER BY {order_by} DESC LIMIT {amount};"
            self.__cursor.execute(query)
            response = self.__cursor.fetchall()

            return response

        except Exception as e:
            return None

    def get_table_service(self):
        try:
            query = f"SELECT * FROM service ORDER BY price DESC;"
            self.__cursor.execute(query)
            response = self.__cursor.fetchall()

            return response

        except Exception as e:
            return None

    def get_staff(self, amount: int) -> list:
        try:
            query = "SELECT " \
                    "CONCAT(first_name,' ', last_name) as doctor, " \
                    "status, " \
                    "phone, " \
                    "email " \
                    "from " \
                    f"staff LIMIT {amount};"

            self.__cursor.execute(query)
            response = self.__cursor.fetchall()

            return response

        except Exception as e:
            print(e)
            return None

    def get_med_card_general(self, username: str):
        try:
            query = f"""
                select 
                    gender,
                    height,
                    weight,
                    address,
                    card_id
                from 
                    medical_card
                where patient = '{username}' """
            self.__cursor.execute(query)
            response = self.__cursor.fetchone()

            return response

        except Exception as e:
            print(e)
            return None

    def get_med_card_disease(self, username: str):
        try:
            query = f"""
                  select 
                        patient,
                        disease.name,
                        treatment.description
                    from 
                        medical_card
                        join disease_med_card on card_id = med_card_id
                        join disease on disease.name =  disease_med_card.name
                        join treatment on disease.treatment_id = treatment.treatment_id
                    where patient = '{username}'; """
            self.__cursor.execute(query)
            response = self.__cursor.fetchall()

            return response

        except Exception as e:
            print(e)
            return None

    def order_ticket(self, time: str, date: str, doctor: str, patient: str,
                     service: str) -> bool:
        try:
            query = "INSERT INTO ticket (time, date, doctor, patient, service) " \
                    "VALUES (%s, %s, %s, %s, %s);"

            self.__cursor.execute(query, (time, date, doctor, patient, service))
            self.__connection.commit()

            return True

        except Exception as e:
            self.__connection.rollback()
            print(e)
            return False


    def get_audit(self):
        try:
            query = "select * from audit;"
            self.__cursor.execute(query)
            response = self.__cursor.fetchall()

            return response

        except Exception as e:
            return None

    def diagnose(self, name: str, med_card: str,) -> bool:
        try:
            query = "INSERT INTO disease_med_card (name, med_card_id) " \
                    "VALUES (%s, %s);"

            self.__cursor.execute(query, (name, med_card))
            self.__connection.commit()

            return True

        except Exception as e:
            self.__connection.rollback()
            print(e)
            return False

    def edit_card(self, patient: str, gender: str, height: float, weight: float, address: str) -> bool:
        try:
            query = f"CALL update_med_card('{patient}', '{gender}', {height}, {weight}, '{address}');"

            self.__cursor.execute(query)
            self.__connection.commit()

        except Exception as e:
            self.__connection.rollback()
            print(e)
            return False

