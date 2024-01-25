from __future__ import annotations

import random
import datetime

import sys

from Lab_6.database import Database
from Lab_6.user import User
from Lab_6.helpers.messages import get_commands_list, ROLES
from Lab_6.helpers.input_manager import Input


class Terminal:

    def __init__(self):
        self.__prompt: str | None = None
        self.__user: User | None = None
        self.__db: Database | None = None

    def start(self):
        """Entry point of CLI"""

        self.__user = User(str(0), 'Guest', ROLES[1])
        self.__db = Database()

        self.list_command()

        while True:
            self.__prompt = input(f'{self.__user.username}: ').lower()
            comm = Input.command_parse(self.__prompt, self.__user.role)

            if comm == 'list':
                self.list_command()
            elif comm == 'sign in':
                self.sign_in_command()
            elif comm == 'sign up':
                self.sign_up_command()
            elif comm == 'sign out':
                self.sign_out_command()
            elif comm == 'services':
                self.services_command()
            elif comm == 'reviews':
                self.reviews_command()
            elif comm == 'staff':
                self.staff_command()
            elif comm == 'clinic info':
                self.clinic_info_command()
            elif comm == 'med card':
                self.med_card_command()
            elif comm == 'order':
                self.order_command()
            elif comm == 'audit':
                self.audit_command()
            elif comm == 'check med card':
                self.check_med_card_command()
            elif comm == 'edit med card':
                self.edit_card_command()
            elif comm == 'diagnose':
                self.edit_diagnose()
            elif comm == 'bank':
                self.view_bank_command()
            elif comm == 'exit':
                sys.exit()
            else:
                print(comm)

    def list_command(self):

        if self.__user.role == ROLES[1]:
            print(get_commands_list('GUEST_COMMANDS'))
        elif self.__user.role == ROLES[2]:
            print(get_commands_list('PATIENT_COMMANDS'))
        elif self.__user.role == ROLES[3]:
            print(get_commands_list('STAFF_COMMANDS'))
        elif self.__user.role == ROLES[4]:
            print(get_commands_list('SUPERUSER_COMMANDS'))

    def sign_in_command(self):
        username = Input.get_valid_username('Username: ')
        password = Input.get_valid_password()

        response = self.__db.sign_in(username, password)

        if response is None:
            print('\nError signing in\n')

        if response.__len__() == 0:
            print('\nUsername or password is not valid\n')
            return

        self.__user.username = response[0]

        is_staff = response[1]
        is_superuser = response[2]

        self.assign_role(is_staff, is_superuser)

    def sign_out_command(self):
        self.__user.username = 'Guest'
        self.__user.role = ROLES[1]

    def sign_up_command(self):
        first_name = Input.get_valid_username('First_name: ')
        last_name = Input.get_valid_username('Last_name: ')
        username = Input.get_valid_username('Username: ')
        password = Input.get_valid_password()
        email = Input.get_valid_username('Email: ')
        age = int(input('Age: '))
        phone = int(input('Phone: '))

        response = self.__db.sign_up(first_name, last_name, username, password, email, age, phone)

        if response:
            print("User successfully signed up.")
            self.__user.username = username
            self.__user.role = ROLES[2]
        else:
            print(f"Error signing up user")

    def assign_role(self, is_staff: bool, is_superuser: bool):
        if is_staff is False and is_superuser is False:
            self.__user.role = ROLES[2]
        elif is_staff is True and is_superuser is False:
            self.__user.role = ROLES[3]
        elif is_staff is False and is_superuser is True:
            self.__user.role = ROLES[4]

    def services_command(self):
        amount = self.get_table_len('service')
        services = self.__db.get_data('service', amount, 'price')

        print('\n\n')
        for index, service in enumerate(services, start=1):
            print(f'   ********** Service #{index} **********')
            print(f'Name: {service[0]}')
            print(f'Price: {service[2]}')
            print(f'Content: {service[1]}\n\n')

    def reviews_command(self):
        amount = self.get_table_len('reviews')
        reviews = self.__db.get_data('reviews', amount, 'rating')

        avg_rate = 0

        print('\n\n')
        for index, review in enumerate(reviews, start=1):
            print(f'   ********** Review #{index} **********')
            print(f'Patient: {review[1]}')
            print(f'Content: {review[2]}')
            print(f'Rating: {review[3]}\n\n')

            avg_rate += int(review[3])

        avg_rate /= reviews.__len__()

        print(f'Average rate: {avg_rate}\n\n')

    def get_table_len(self, table_name: str):
        response = self.__db.table_len(table_name)

        if response is None:
            print(f"Error getting table length")
            return

        print(f'\nFound {response} records.')

        return Input.get_value_in_range('How many to display? ', 1, response)

    def clinic_info_command(self):
        print('\nName: BSUIR')
        print('Address: Hikalo, 9')
        print('Phone: +375-29-777-77-77\n')

    def staff_command(self):
        amount = self.get_table_len('staff')
        staff = self.__db.get_staff(amount)

        print('\n\n')
        for index, doctor in enumerate(staff, start=1):
            print(f' Doctor #{doctor[0]}')
            print(f'Status: {doctor[1]}')
            print(f'Phone: {doctor[2]}\n\n')

    def med_card_command(self):
        general = self.__db.get_med_card_general(self.__user.username)

        if general is None:
            print('\nError retrieving generals')

        print(f'\n\n***** Medical_card for {self.__user.username}  *****\n')
        print(f'Patient #{self.__user.username}')
        print(f'Gender: {general[0]}')
        print(f'Height: {general[1]}')
        print(f'Weight: {general[2]}')
        print(f'Address: {general[3]}\n')

        diseases = self.__db.get_med_card_disease(self.__user.username)

        if diseases is None:
            print('\nError retrieving generals')

        for index, disease in enumerate(diseases, start=1):
            print(f'Disease #{disease[1]}')
            print(f'Treatment: {disease[2]}\n\n')

    def order_command(self):
        services = self.__db.get_table_service()
        response = self.__db.table_len('service')
        response_staff = self.__db.table_len('staff')
        staff = self.__db.get_staff(response_staff)
        print('\n\n')
        for index, service in enumerate(services, start=1):
            print(f'   ********** Service #{index} **********')
            print(f'Name: {service[0]}')
            print(f'Price: {service[2]}')

        serv_num = Input.get_value_in_range('Choose service ', 1, response)
        service_order = ""
        for index, service in enumerate(services, start=1):
            if index == serv_num:
                service_order = service[0]
                break

        print('\n\n')
        for index, doctor in enumerate(staff, start=1):
            print(f'   ********** Doctor #{index} **********')
            print(f'Doctor #{doctor[0]}')
            print(f'Status: {doctor[1]}')

        doctor_num = Input.get_value_in_range('Choose doctor ', 1, response_staff)
        for index, doctor in enumerate(staff, start=1):
            if index == doctor_num:
                doctor_order = doctor[3]

        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)

        formatted_time = f"{random_hour:02d}:{random_minute:02d}:{random_second:02d}"
        formatted_date = tomorrow.strftime("%Y-%m-%d")
        print('\n\n')
        print(service_order)
        print(doctor_order)
        print(formatted_time)
        print(formatted_date)

        response_order = self.__db.order_ticket(formatted_time, formatted_date, doctor_order, self.__user.username,
                                                service_order)

        if response_order:
            print("User successfully signed up.")

    def audit_command(self):
        audit = self.__db.get_audit()

        for index, record in enumerate(audit, start=1):
            print(f'   ********** Record #{index} **********')
            print(f'Patient: {record[0]}')
            print(f'Doctor: {record[1]}')
            print(f'Service: {record[2]}')
            print(f'Price: {record[3]}')
            print(f'Date: {record[4]}')
            print(f'Time: {record[5]}\n\n')

    def check_med_card_command(self):
        patient = Input.get_valid_username('Username: ')

        general = self.__db.get_med_card_general(patient)

        if general is None:
            print('\nError retrieving generals')

        print(f'\n\n***** Medical_card for {patient}  *****\n')
        print(f'Patient #{patient}')
        print(f'Gender: {general[0]}')
        print(f'Height: {general[1]}')
        print(f'Weight: {general[2]}')
        print(f'Address: {general[3]}\n')

        diseases = self.__db.get_med_card_disease(patient)

        if diseases is None:
            print('\nError retrieving generals')

        for index, disease in enumerate(diseases, start=1):
            print(f'Disease #{disease[1]}')
            print(f'Treatment: {disease[2]}\n\n')

    def edit_card_command(self):
        patient = Input.get_valid_username('Username: ')
        gender = input('Gender: ')
        height = float(input('Height: '))
        weight = float(input('Weight: '))
        address = input('Address: ')

        response_edit = self.__db.edit_card(patient, gender, height, weight, address)

        if response_edit:
            print("<--success-->")

    def edit_diagnose(self):
        patient = Input.get_valid_username('Username: ')

        response = self.__db.table_len('disease')
        diseases = self.__db.get_data('disease', response, 'name')

        print('\n\n')
        for index, disease in enumerate(diseases, start=1):
            print(f'   ********** Disease #{index} **********')
            print(f'Name: {disease[0]}')

        dis_num = Input.get_value_in_range('Choose disease ', 1, response)
        dis_card = ""
        for index, disease in enumerate(diseases, start=1):
            if index == dis_num:
                dis_card = disease[0]
                break

        print(patient)
        print(dis_card)

        general = self.__db.get_med_card_general(patient)
        med_card = general[4]

        response_diagnose = self.__db.diagnose(dis_card, med_card)

        if response_diagnose:
            print("<--success-->")

    def view_bank_command(self):
        amount = self.get_table_len('bank')
        bank = self.__db.get_data('bank', amount, 'total_price')

        print('\n\n')
        for index, check in enumerate(bank, start=1):
            print(f'   ********** Check #{index} **********')
            print(f'Doctor: {check[0]}')
            print(f'Email: {check[1]}')
            print(f'Services_count: {check[2]}')
            print(f'Total price: {check[3]}\n')
