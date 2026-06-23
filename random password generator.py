import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


# Password history
history = []


# Character sets

UPPER = string.ascii_uppercase
LOWER = string.ascii_lowercase
NUMBERS = string.digits
SYMBOLS = string.punctuation


AMBIGUOUS = "0Ool1I"



# Generate Password

def generate_password():

    length = length_var.get()


    if length < 8:

        messagebox.showerror(
            "Error",
            "Password length must be at least 8"
        )

        return



    characters = ""

    selected = []



    if upper_var.get():

        characters += UPPER
        selected.append(UPPER)


    if lower_var.get():

        characters += LOWER
        selected.append(LOWER)


    if number_var.get():

        characters += NUMBERS
        selected.append(NUMBERS)


    if symbol_var.get():

        characters += SYMBOLS
        selected.append(SYMBOLS)



    if len(selected) < 2:

        messagebox.showerror(
            "Error",
            "Select at least two character types"
        )

        return



    if ambiguous_var.get():

        characters = ''.join(
            c for c in characters
            if c not in AMBIGUOUS
        )



    # Guarantee selected character types

    password = []


    for group in selected:

        available = ''.join(
            c for c in group
            if not ambiguous_var.get()
            or c not in AMBIGUOUS
        )

        password.append(
            secrets.choice(available)
        )



    # Fill remaining length

    for i in range(length-len(password)):

        password.append(
            secrets.choice(characters)
        )



    # Shuffle securely

    secrets.SystemRandom().shuffle(password)


    result = ''.join(password)



    password_entry.delete(0,tk.END)

    password_entry.insert(0,result)



    check_strength(result)



    # Copy automatically

    pyperclip.copy(result)



    # History

    history.append(result)


    if len(history) > 5:

        history.pop(0)



    history_box.delete(
        1,
        tk.END
    )


    for item in history:

        history_box.insert(
            tk.END,
            item
        )



# Strength Checker

def check_strength(password):

    score = 0


    if len(password)>=8:
        score +=1


    if len(password)>=12:
        score +=1


    if any(c.isupper() for c in password):
        score+=1


    if any(c.islower() for c in password):
        score+=1


    if any(c.isdigit() for c in password):
        score+=1


    if any(c in SYMBOLS for c in password):
        score+=1



    if score <=2:

        strength="Weak"

    elif score <=4:

        strength="Medium"

    else:

        strength="Strong"



    strength_label.config(
        text="Strength: "+strength
    )



# ---------------- GUI ----------------


window=tk.Tk()

window.title(
    "Random Password Generator"
)

window.geometry(
    "500x600"
)



tk.Label(
    window,
    text="Password Generator",
    font=("Arial",20)
).pack(pady=10)



# Length

tk.Label(
    window,
    text="Password Length"
).pack()


length_var=tk.IntVar(
    value=12
)


tk.Scale(
    window,
    from_=8,
    to=50,
    orient="horizontal",
    variable=length_var
).pack()



# Options

upper_var=tk.BooleanVar(value=True)

lower_var=tk.BooleanVar(value=True)

number_var=tk.BooleanVar(value=True)

symbol_var=tk.BooleanVar(value=True)



tk.Checkbutton(
    window,
    text="Uppercase Letters",
    variable=upper_var
).pack()


tk.Checkbutton(
    window,
    text="Lowercase Letters",
    variable=lower_var
).pack()


tk.Checkbutton(
    window,
    text="Numbers",
    variable=number_var
).pack()


tk.Checkbutton(
    window,
    text="Symbols",
    variable=symbol_var
).pack()



# Ambiguous

ambiguous_var=tk.BooleanVar()


tk.Checkbutton(
    window,
    text="Exclude ambiguous characters (0,O,l,1)",
    variable=ambiguous_var
).pack()



# Password display

password_entry=tk.Entry(
    window,
    width=40,
    font=("Arial",12)
)

password_entry.pack(pady=10)



# Button

tk.Button(
    window,
    text="Generate Password",
    command=generate_password
).pack()



# Strength

strength_label=tk.Label(
    window,
    text="Strength:"
)

strength_label.pack(pady=10)



# History

tk.Label(
    window,
    text="Last 5 Passwords"
).pack()


history_box=tk.Listbox(
    window,
    width=40
)

history_box.pack()



window.mainloop()