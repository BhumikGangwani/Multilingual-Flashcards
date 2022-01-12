from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6" # Flashcard background

# global variables
card = {}
to_learn = {}
cur_lang = "fr"

# Read from the file that contains words in French that user doesn't know
try:
    df = pd.read_csv("data/to_learn.csv")
except FileNotFoundError:
    old_df = pd.read_csv("data/french_words.csv")
    to_learn = old_df.to_dict(orient="records")
else:
    to_learn = df.to_dict(orient="records")


# ---------------------------- DISPLAY CARDS ------------------------------- #

# Moves to the next French word
def next_card():
    global card, cur_lang
    card = random.choice(to_learn)
    cur_lang = "en"
    flip_card()


# Flips the flashcard from English to French or French to English
def flip_card():
    global cur_lang
    if cur_lang == "fr":
        cur_lang = "en"
        canvas.itemconfig(language, text="English", fill="white")
        canvas.itemconfig(word, text=card["English"], fill="white")
        canvas.itemconfig(background, image=back_img)
    else:
        cur_lang = "fr"
        canvas.itemconfig(language, text="French", fill="black")
        canvas.itemconfig(word, text=card["French"], fill="black")
        canvas.itemconfig(background, image=front_img)


# ---------------------------- SAVE CORRECT WORDS ------------------------------- #
def remove_correct():
    to_learn.remove(card)
    to_learn_df = pd.DataFrame(to_learn)
    # noinspection PyTypeChecker
    to_learn_df.to_csv("data/to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title(string="Multilingual Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
background = canvas.create_image(400, 263, image=front_img)
language = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_answer_image = PhotoImage(file="images/wrong.png")
wrong_answer_button = Button(image=wrong_answer_image, bg=BACKGROUND_COLOR, command=next_card)
wrong_answer_button.grid(row=1, column=0)

correct_answer_image = PhotoImage(file="images/right.png")
correct_answer_button = Button(image=correct_answer_image, bg=BACKGROUND_COLOR, command=remove_correct)
correct_answer_button.grid(row=1, column=1)

flip_button = Button(text="Flip", bg=BACKGROUND_COLOR, width=7, height=2, font=8, command=flip_card)
flip_button.place(x=370, y=550)

next_card()

window.mainloop()
