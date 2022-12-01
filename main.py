from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import json 

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)

    password = "".join(password_list)
    # for char in password_list:
    #     password += char

    passwordEntry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

fileEntry=""

def add():
    website = websiteEntry.get()
    username = usernameEntry.get()
    password = passwordEntry.get()
    new_data = {
        website: {
        "username": username,
        "password": password,
        }   
    }

    if len(website) ==0 or len(username)==0 or len(password)==0:
        messagebox.showerror(title="", message="One or more of the fields is empty.")
    else:
        isConfirmed = messagebox.askokcancel(title="", message = "Confirmation", detail=(f"These are the details you've provided:\n Website: {website}\n Username: {username}\n Password: {password}"))
    
        if isConfirmed:
            try:
                with open ("data.json", mode = "r") as file:
                    # Reading old data
                    data = json.load(file)
                    # Updating old data
                    data.update(new_data)
                # Saving updated data
                with open ("data.json", mode="w") as file:
                    json.dump(data, file, indent = 4)
            except FileNotFoundError:
                # Create new file
                with open ("data.json", mode="w") as file:
                    json.dump(new_data, file, indent = 4)
            finally:
                websiteEntry.delete(0, END)
                passwordEntry.delete(0, END)

# ---------------------------- PASSWORD SEARCH ------------------------------- #

def password_search():
    website = websiteEntry.get()

    try:
        with open ("data.json", mode = "r") as file:
            data = json.load(file)
        
        if website in data:
            username = data[website]["username"]
            password = data[website]["password"]
            websiteFound = messagebox.showinfo(title="", message=website, detail=(f"Username: {username} \n Password: {password}"))
        else:
            websiteNotFound = messagebox.showerror(title="", message="Error", detail = (f"{website} does not exist. Please try againl"))
    except FileNotFoundError:
        websiteNotFound = messagebox.showerror(title="", message="Error", detail = (f"{website} does not exist. Please try againl"))


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)


# canvas setup
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(140, 100, image=logo)
canvas.grid(row=0, column=1)


# labels
websiteLabel = Label(text="Website:")
websiteLabel.grid(row=1, column=0)

usernameLabel = Label(text="Username/Email:")
usernameLabel.grid(row=2, column=0)

passwordLabel = Label(text="Password:")
passwordLabel.grid(row=3, column=0)


# entries
websiteEntry = Entry()
websiteEntry.grid(row=1, column=1, sticky="ew")
websiteEntry.focus()

usernameEntry = Entry()
usernameEntry.grid(row=2, column=1, columnspan=2, sticky="ew")

passwordEntry = Entry()
passwordEntry.grid(row=3, column=1, sticky="ew")


# buttons
generateButton = Button(text="Generate Password", command=generate_password)
generateButton.grid(row=3, column=2)

addButton = Button(text="Add", width=35, command=add)
addButton.grid(row=4, column=1, columnspan=2, sticky="ew")

searchButton = Button(text="Search", command = password_search)
searchButton.grid(row=1, column=2, sticky="ew")



window.mainloop()
