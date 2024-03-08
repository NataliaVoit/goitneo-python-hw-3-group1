def get_birthdays_per_week(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        birthdays_next_week = {}
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                if today <= birthday_date < next_week:
                    day_week = birthday_date.strftime("%A")
                    if day_week in birthdays_next_week:
                        birthdays_next_week[day_week].append(record.name.value)
                    else:
                        birthdays_next_week[day_week] = [record.name.value]
        return birthdays_next_week


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            if len(args) != 3:
                print("Invalid command arguments.")
                continue
            name, phone = args[0], args[1]
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print("Contact added.")
        elif command == "change":
            if len(args) != 2:
                print("Invalid command arguments.")
                continue
            name, new_phone = args
            record = book.find(name)
            if record:
                record.edit_phone(record.phones[0].value, new_phone)
            else:
                print("Contact not found.")
        elif command == "phone":
            if len(args) != 1:
                print("Invalid command arguments.")
                continue
            name = args[0]
            record = book.find(name)
            if record:
                print(record.phones[0])
            else:
                print("Contact not found.")
        elif command == "all":
            for record in book.data.values():
                print(record)
        elif command == "add-birthday":
            if len(args) != 2:
                print("Invalid command arguments.")
                continue
            name, birthday = args
            record = book.find(name)
            if record:
                record.add_birthday(birthday)
            else:
                print("Contact not found.")
        elif command == "show-birthday":
            if len(args) != 1:
                print("Invalid command arguments.")
                continue
            name = args[0]
            record = book.find(name):
            if record and record.birthday:
                print(record.birthday)
            else:
                print("Contact not found or birthday not set.")
        elif command == "birthdays":
            birthdays = book.get_birthdays_per_week()
            for day, names in birthdays.items():
                print(f"{day}: {', '.join(names)}")
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
