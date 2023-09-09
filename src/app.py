import os
import pickle


class AddressBook:
    def __init__(self, contacts=None):
        if contacts is None:
            contacts = {}
        self._contacts = contacts

    def add_contact(self, name, email):
        if name in self._contacts:
            print('Такое уже есть!')
            return
        self._contacts[name] = email

    def modify_contact(self, name, email):
        self._contacts[name] = email

    def delete_contact(self, name):
        del self._contacts[name]

    def list_contacts(self):
        return "\n".join([f"{key}: {value}" for key, value in self._contacts.items()])


if __name__ == "__main__":

    if not os.path.isfile('../data/addressbook.data'):
        with open('../data/addressbook.data', 'xb') as f:
            pass
    with open('../data/addressbook.data', 'rb') as f:
        try:
            contacts = pickle.load(f)
        except EOFError as e:
            print('Не удалось загрузить данные из файла ../data/addressbook.data. '
                  'Создаем пустой словарик.')  # Заменить на лог
            contacts = {}

    address_book = AddressBook(contacts)
    while True:
        command = input('> ')
        if command == 'add':
            name = input('Enter name: ')
            email = input('Enter email: ')
            address_book.add_contact(name, email)
        elif command == 'modify':
            name = input('Enter name: ')
            email = input('Enter modified email: ')
            address_book.modify_contact(name, email)
        elif command == 'delete':
            name = input('Enter name: ')
            address_book.delete_contact(name)
        elif command == 'list':
            print(address_book.list_contacts())
        elif command == 'exit':
            with open('../data/addressbook.data', 'wb') as f:
                pickle.dump(address_book._contacts, f)
            quit()
        else:
            print('Unknown command')
