import pickle
import argparse

parser = argparse.ArgumentParser(prog=__package__, description="Адресная книга. Позволяет удобно сохранять контакты.")
subparsers = parser.add_subparsers(title="Команды: ", description="Доступные виды комманд", dest='command')

add_parser = subparsers.add_parser("add", description="Добавляет контакт")
add_parser.add_argument("name", help="Имя нового контакта")
add_parser.add_argument("email", help="Email нового контакта")

modify_parser = subparsers.add_parser("modify", description="Изменяет контакт")
modify_parser.add_argument("name", help="Имя контакта для изменения")
modify_parser.add_argument("name", help="Новый email контакта")

list_parser = subparsers.add_parser("list", description="Выводит список всех контактов")

delete_parser = subparsers.add_parser("delete", description="Удаляет контакт")
delete_parser.add_argument("name", help="Имя контакта для удаления")


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
            with open('../data/addressbook.data', 'rb') as f:
                pass
            print('[LOG] Файл не найден. Создаем пустую книгу.')
            self._contacts = {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open('../data/addressbook.data', 'wb') as f:
            pickle.dump(self._contacts, f)
            print("Адресная книга успешно сохранена")


if __name__ == "__main__":
    with AddressBook() as address_book:
        args = parser.parse_args()
        if args.command == "add":
            print(address_book.add_contact(args.name, args.email))
        elif args.command == 'modify':
            print(address_book.modify_contact(args.name, args.email))
        elif args.command == 'delete':
            print(address_book.delete_contact(args.name))
        elif args.command == 'list':
            print(address_book.list_contacts())
        else:
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
