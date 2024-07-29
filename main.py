import json
from tkinter import *
from tkinter import messagebox

import pyperclip


def password_generator():

    if len(password_entry.get().strip()) > 0 :
        password_entry.delete(0, END)
    from random import shuffle, choice, randint
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)
    final_pass = "".join(password_list)
    pyperclip.copy(final_pass)

    password_entry.insert(0, final_pass)
    messagebox.showinfo(title="", message="Password generated successfully.\n"
                                          "Password copied to clipboard")


def save():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    new_data = {
        website: {
                  "email": email,
                  "password": password
                  }
    }
    if website.strip() == "" or password.strip() == "":
        messagebox.showinfo(title="Oops", message="There are empty fields, fill them out!")


    else:
        # is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\n "
        #                                                       f"Email: {email}\n "
        #                                                       f"Password: {password}\n "
        #                                                       f"Is it ok to save?")
        # if is_ok:
        #     line = website + "   |   " + email + "   |   " + password + "\n"
        try:
            with open("data.json", mode='r') as data_file:
                # Read data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                #Create json file and write to it
                json.dump(new_data, data_file, indent=4)

        except json.JSONDecodeError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            # Update existing data
            data.update(new_data)
            with open("data.json", mode="w") as data_file:
                # Write updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

def search():
    found = False
    if website_entry.get().strip() == "":
        messagebox.showinfo(message="website field cannot be empty")
    else:
        website_name = website_entry.get().strip()
        try:
            with open("data.json", mode="r") as database:
                database_dic = json.load(database)
        except FileNotFoundError:
            messagebox.showinfo(message="error 404, no file or data found")

        except json.JSONDecodeError:
            messagebox.showinfo(message="NO data found.")
        else:
            for website, email_pass in database_dic.items():
                if website_name == website:
                    found = True
                    wanted_username = email_pass["email"]
                    wanted_password = email_pass["password"]

            if found:
                messagebox.showinfo(title="Website Found",
                                    message=f"Email/Username: {wanted_username}\n"
                                            f"Password: {wanted_password}\n"
                                            f"Password copied to clipboard")
                pyperclip.copy(wanted_password)
                found = False
            else:
                messagebox.showinfo(title="Oops", message=f"{website_name} Not Found")


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# WEBSITE SHIT
website_label = Label(text="Website: ")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username: ")
email_label.grid(row=2, column=0)

password_label = Label(text="Password: ")
password_label.grid(row=3, column=0)
#############################################################

website_entry = Entry(width=30)
website_entry.grid(row=1, column=1, columnspan=1)
website_entry.focus()

email_entry = Entry(width=25)
email_entry.grid(row=2, column=1, columnspan=1)
email_entry.insert(0, "")  # Default email inserted in the beginning

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, columnspan=1)

# Buttons
generate_password_button = Button(text="Generate Password", command=password_generator  )
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", command=search)
search_button.grid(row=1, column=2)


window.mainloop()
