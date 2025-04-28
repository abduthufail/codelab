import random
import time
from tkinter import Tk, Label, Button, Entry, StringVar, messagebox

class QuizApp:
    def _init_(self, master):
        self.master = master
        self.master.title("Arithmetic Challenge")
        self.master.geometry("420x320")

        # Game state variables
        self.points = 0
        self.current_q = 0
        self.max_questions = 10
        self.value1 = 0
        self.value2 = 0
        self.sign = ""
        self.solution = 0
        self.timer_start = time.time()

        self.level = StringVar(value="1")

        # Interface elements
        Label(master, text="Arithmetic Challenge", font=("Verdana", 22)).pack(pady=10)
        Label(master, text="Choose your difficulty:", font=("Verdana", 12)).pack()

        Button(master, text="Beginner (1-digit)", command=lambda: self.begin_quiz(1)).pack(pady=5)
        Button(master, text="Intermediate (2-digit)", command=lambda: self.begin_quiz(2)).pack(pady=5)
        Button(master, text="Expert (4-digit)", command=lambda: self.begin_quiz(3)).pack(pady=5)

        self.prompt_label = Label(master, text="", font=("Verdana", 14))
        self.prompt_label.pack(pady=10)

        self.user_input = StringVar()
        self.input_entry = Entry(master, textvariable=self.user_input, font=("Verdana", 12))
        self.input_entry.pack()

        self.submit_btn = Button(master, text="Submit", command=self.validate_answer, state="disabled")
        self.submit_btn.pack(pady=10)

        self.response_label = Label(master, text="", font=("Verdana", 12))
        self.response_label.pack(pady=5)

        self.track_label = Label(master, text="", font=("Verdana", 10))
        self.track_label.pack(pady=5)

    def get_random_number(self, level):
        if level == 1:
            return random.randint(1, 9)
        elif level == 2:
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)

    def choose_sign(self):
        return random.choice(['+', '-'])

    def begin_quiz(self, level):
        self.level = level
        self.points = 0
        self.current_q = 0
        self.timer_start = time.time()
        self.submit_btn.config(state="normal")
        self.load_question()

    def load_question(self):
        if self.current_q < self.max_questions:
            self.value1 = self.get_random_number(self.level)
            self.value2 = self.get_random_number(self.level)
            self.sign = self.choose_sign()

            if self.sign == '-' and self.value1 < self.value2:
                self.value1, self.value2 = self.value2, self.value1

            if self.sign == '+':
                self.solution = self.value1 + self.value2
            else:
                self.solution = self.value1 - self.value2

            self.prompt_label.config(text=f"Compute: {self.value1} {self.sign} {self.value2}")
            self.user_input.set("")
            self.response_label.config(text="")
            self.track_label.config(text=f"Question {self.current_q + 1} of {self.max_questions}")
        else:
            self.finish_quiz()

    def provide_feedback(self, answer):
        if answer == self.solution:
            self.response_label.config(text="That's correct!", fg="green")
        else:
            self.response_label.config(text=f"Oops! The right answer was {self.solution}.", fg="red")

    def validate_answer(self):
        try:
            answer = int(self.user_input.get())
        except ValueError:
            self.response_label.config(text="Enter a valid number!", fg="red")
            return

        self.provide_feedback(answer)

        if answer == self.solution:
            self.points += 10

        self.current_q += 1
        self.master.after(1000, self.load_question)

    def finish_quiz(self):
        total_time = time.time() - self.timer_start
        self.prompt_label.config(text="")
        self.input_entry.pack_forget()
        self.submit_btn.pack_forget()
        self.response_label.config(text="")

        messagebox.showinfo("Finished!", f"Score: {self.points}/100\nTime: {total_time:.2f} seconds")
        self.show_final_grade()

    def show_final_grade(self):
        rating = ""
        note = ""

        if self.points >= 90:
            rating = "A+"
            note = "Outstanding work!"
        elif self.points >= 80:
            rating = "A"
            note = "Great effort!"
        elif self.points >= 70:
            rating = "B"
            note = "Well done!"
        elif self.points >= 60:
            rating = "C"
            note = "Good attempt!"
        else:
            rating = "D"
            note = "Keep practicing!"

        self.response_label.config(text=f"Grade: {rating}\n{note}")
        self.track_label.config(text="Try again?")
        Button(self.master, text="Play Again", command=self.restart_quiz).pack(pady=10)

    def restart_quiz(self):
        self.master.destroy()
        launch()

def launch():
    root = Tk()
    game = QuizApp(root)
    root.mainloop()

if _name_ == "_main_":
    launch()
