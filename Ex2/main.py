import random
import tkinter as tk
from tkinter import messagebox

def fetch_jokes(filepath):
    """
    Reads jokes from a file and returns a list of (question, answer) pairs.
    Each joke should be separated using a '?' character.
    """
    jokes_list = []
    try:
        with open(filepath, 'r') as f:
            for entry in f:
                if '?' in entry:
                    question, answer = entry.strip().split('?', 1)
                    jokes_list.append((question.strip() + "?", answer.strip()))
    except FileNotFoundError:
        messagebox.showerror("File Error", "Couldn't find the jokes file. Check the file path.")
    except Exception as err:
        messagebox.showerror("Error", f"Problem reading jokes: {err}")
    return jokes_list

def show_joke():
    """
    Randomly picks and displays a joke.
    """
    if loaded_jokes:
        chosen_joke = random.choice(loaded_jokes)
        question, answer = chosen_joke
        question_label.config(text=question)
        answer_button.config(state=tk.NORMAL, command=lambda: show_answer(answer))
    else:
        question_label.config(text="No jokes to show. Please check your joke file!")

def show_answer(answer_text):
    """
    Shows the punchline when the button is clicked.
    """
    punchline_display.config(text=answer_text)
    answer_button.config(state=tk.DISABLED)

# Initialize the main window
window = tk.Tk()
window.title("Joke Teller")
window.geometry("500x300")
window.resizable(False, False)

# Load the jokes
loaded_jokes = fetch_jokes("randomJokes.txt")

# Set up the GUI
header = tk.Label(window, text="Joke Teller", font=("Helvetica", 20, "bold"), pady=10)
header.pack()

question_label = tk.Label(window, text="Press below for a joke!", font=("Helvetica", 14), wraplength=450, pady=20)
question_label.pack()

answer_button = tk.Button(window, text="Show Punchline", state=tk.DISABLED, font=("Helvetica", 12))
answer_button.pack(pady=10)

punchline_display = tk.Label(window, text="", font=("Helvetica", 14, "italic"), wraplength=450, pady=20)
punchline_display.pack()

new_joke_btn = tk.Button(window, text="Get a Joke", font=("Helvetica", 12), command=show_joke)
new_joke_btn.pack(pady=20)

# Launch the window
window.mainloop()
