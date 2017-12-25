#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

class Contact:
    def __init__(self, name, phone_number, e_mail, addr):
        self.name = name
        self.phone_number = phone_number
        self.e_mail = e_mail
        self.addr = addr

    def print_info(self):
        print("Name: ", self.name)
        print("Phone Number: ", self.phone_number)
        print("E-mail: ", self.e_mail)
        print("Address: ", self.addr)

def set_contact():
    name = raw_input("Name: ")
    phone_number = raw_input("Phone Number: ")
    e_mail = raw_input("E-mail: ")
    addr = raw_input("Address: ")
    contact= Contact(name, phone_number, e_mail, addr)
    return contact

def print_menu():
    print("1. 연락처 입력")
    print("2. 연락처 출력")
    print("3. 연락처 삭제")
    print("4. 종료")
    menu = raw_input("메뉴선택: ")
    return int(menu)

def print_contact(contact_list):
    print(dir())
    for contact in contact_list:
        print(contact)
        print(contact.__class__)
        contact.print_info()
        #Contact.print_info()

def delete_contact(contact_list, name):
    for i, contact in enumerate(contact_list):
        if contact.name == name:
            del contact_list[i]

def store_contact(contact_list):
    f = open("contact_db.txt", "wt")
    for contact in contact_list:
        f.writelines(contact.name)
        f.write(contact.phone_number + '\n')
        f.write(contact.e_mail + '\n')
        f.write(contact.addr + '\n')
    f.close()

def run():
    contact_list = []
    while 1:
        menu = print_menu()
        if menu == 1:
            contact = set_contact()
            contact_list.append(contact)
        elif menu == 2:
            for contact in contact_list:
                contact.print_info()
            print('===============')
            print_contact(contact_list)
            print('===============')
        elif menu == 3:
            name = raw_input('name = ')
            delete_contact(contact_list, name)
        elif menu == 4:
            store_contact(contact_list)
            break

if __name__ == "__main__":
    run()