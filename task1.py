from datetime import datetime, timedelta
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))


    def remove_phone(self, phone):
        record_phone = self.find_phone(phone)
        if record_phone:  
            self.phones.remove(record_phone)
            return "phone removed"
        return "Phone not found" 

    def edit_phone(self, old_phone, new_phone):
        record_phone = self.find_phone(old_phone)
        if record_phone:  
            record_phone.value = new_phone
            return "phone changed"
        return "Phone not found."

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        print("Phone not found.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def show_birthday(self):
        return self.birthday


    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        record = self.find(name)
        if record:
            del self.data[name]
            return "contact deleted"
        return "contact not found"
    def birthdays(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        birthdays_next_week = {}
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                birthday_date = birthday_date.replace(year=today.year)
                if today <= birthday_date < next_week:
                    day_week = birthday_date.strftime("%A")
                    if day_week in birthdays_next_week:
                        birthdays_next_week[day_week].append(record.name.value)
                    else:
                        birthdays_next_week[day_week] = [record.name.value]
        return birthdays_next_week
        
    
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command arguments."

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts: AddressBook):
    name, phone = args
    print(name, phone)
    record_obj = Record(name)
    record_obj.add_phone(phone)
    contacts.add_record(record=record_obj)
    return "Contact added."

@input_error
def show_all(args, contacts):
    if not contacts:
        return "no contacts"
    people = ""
    for name, record in contacts.data.items():
        people += f"{record}"
    return people

@input_error
def change_contact(args, contacts: AddressBook):
    name, old_phone, new_phone = args
    record_obj = contacts.find(name)
    if record_obj:
        record_obj.edit_phone(old_phone, new_phone)
        return "Contact updated"
    return "phone not found"

@input_error
def show_phone(args, contacts):
    name = args[0]
    record_obj = contacts.find(name)
    if record_obj:
        phones = ",".join(record_obj.phones)
        return f"{phones}"
    
@input_error
def add_birthday(args, contacts):
    name, birthday = args
    record_obj = contacts.find(name)
    if record_obj:
        record_obj.add_birthday(birthday)
        return "birthday added"
    return "contact noy found"

@input_error
def show_birthday(args, contacts):
    name = args[0]
    record_obj = contacts.find(name)
    if record_obj:
        return f"{record_obj.birthday}"
    return "contact not found"

@input_error
def birthdays(args, contacts):
    res = ""
    for day_week, names in contacts.birthdays().items():
        res += f"{day_week}: {', '.join(names)} \n"
    return res


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "all":
            print(show_all(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "show-all-birthdays":
            print(birthdays(args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
