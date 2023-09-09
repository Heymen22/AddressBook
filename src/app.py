import pickle


class AddressBook:
    def __init__(self, contacts=None):
        if contacts is None:
            contacts = {}
        self._contacts = contacts

    def add_contact(self, name, email):
        if name in self._contacts:
            return f"Контакт с именем {name} уже существует."
        self._contacts[name] = email
        return f"Контакт с именем {name} создан"

    def modify_contact(self, name, email):
        if name not in self._contacts:
            return f"Контакт с именем {name} не найден."
        self._contacts[name] = email
        return f"Контакт с именем {name} теперь имеет email: {email}"

    def delete_contact(self, name):
        if name not in self._contacts:
            return f"Контакт с именем {name} не найден."
        del self._contacts[name]
        return f"Контакт с именем {name} удален"

    def list_contacts(self):
        if len(self._contacts) == 0:
            return "Список контактов пуст!"
        return "\n".join([f"{key}: {value}" for key, value in self._contacts.items()])

    def __enter__(self):
        try:
            with open('../data/addressbook.data', 'rb') as f:
                self._contacts = pickle.load(f)
        except EOFError:
            print('[LOG] Файл с данными пуст. Создаем пустую адресную книгу.')
            self._contacts = {}
        except pickle.UnpicklingError:
            print('[LOG] Файл с данными поврежден. Пустую книгу.')
            self._contacts = {}
        except FileNotFoundError:
            print('[LOG] Файл не найден. Создаем пустую книгу.')
            self._contacts = {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open('../data/addressbook.data', 'xb') as f:
            pickle.dump(self._contacts, f)
            print("Адресная книга успешно сохранена")


if __name__ == "__main__":
    with AddressBook() as address_book:
        while True:
            command = input('> ')
            if command == 'add':
                name = input('Enter name: ')
                email = input('Enter email: ')
                print(address_book.add_contact(name, email))
            elif command == 'modify':
                name = input('Enter name: ')
                email = input('Enter modified email: ')
                print(address_book.modify_contact(name, email))
            elif command == 'delete':
                name = input('Enter name: ')
                print(address_book.delete_contact(name))
            elif command == 'list':
                print(address_book.list_contacts())
            elif command == 'exit':
                break
            else:
                print('Неизвестная команда')
