import tkinter as tk
import json
import os
import winsound  # Windows only
from pydub import AudioSegment
from pydub.playback import play

# Load questions
with open('final_mcqs.json', 'r') as f:
    questions = json.load(f)

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("MCQ Quiz")
        self.master.geometry("750x500")
        self.master.configure(bg="#3e2723")

        self.question_index = 0
        self.score = 0
        self.user_answer = tk.StringVar(value="__none__")

        self.setup_widgets()
        self.display_question()

    def setup_widgets(self):
        self.header_label = tk.Label(
            self.master, text="", font=("Helvetica", 16, "bold"),
            bg="#3e2723", fg="#fbe9e7", justify="center"
        )
        self.header_label.pack(pady=(20, 5))

        self.question_label = tk.Label(
            self.master, text="", font=("Helvetica", 13),
            wraplength=680, justify="center", bg="#3e2723", fg="#fbe9e7"
        )
        self.question_label.pack(pady=(0, 15))

        self.options_frame = tk.Frame(self.master, bg="#3e2723")
        self.options_frame.pack()

        self.option_buttons = []
        for _ in range(4):
            rb = tk.Radiobutton(
                self.options_frame, text="", variable=self.user_answer,
                value="", font=("Helvetica", 11), anchor='w', justify="left",
                bg="#3e2723", fg="#fbe9e7", selectcolor="#004d40",
                activebackground="#3e2723", activeforeground="#fbe9e7",
                command=self.check_answer, indicatoron=True
            )
            rb.pack(anchor='w', pady=4, padx=20)
            self.option_buttons.append(rb)

        self.feedback_label = tk.Label(
            self.master, text="", font=("Helvetica", 11, "italic"),
            bg="#3e2723", fg="#fbe9e7", wraplength=700, justify="center"
        )
        self.feedback_label.pack(pady=(12, 8))

        self.next_button = tk.Button(
            self.master, text="Next Question", font=("Helvetica", 11, "bold"),
            bg="#00695c", fg="white", activebackground="#004d40",
            activeforeground="white", relief="flat",
            command=self.next_question
        )
        self.next_button.pack(pady=10)
        self.next_button.pack_forget()

    def display_question(self):
        self.user_answer.set("__none__")
        self.feedback_label.config(text="")
        self.next_button.pack_forget()

        question = questions[self.question_index]
        self.header_label.config(text=f"Topic: {question['header']}")
        self.question_label.config(text=f"Q{self.question_index + 1}: {question['question']}")

        for i, option in enumerate(question['options']):
            self.option_buttons[i].config(text=option, value=option, state='normal')

    def check_answer(self):
        selected = self.user_answer.get()
        if selected == "__none__":
            return

        correct = questions[self.question_index]['answer']

        for rb in self.option_buttons:
            rb.config(state='disabled')

        if selected.lower() == correct.lower():
            self.score += 1
            self.feedback_label.config(text="✅ Correct!", fg="#80cbc4")
            winsound.PlaySound("correct.wav", winsound.SND_FILENAME)
        else:
            self.feedback_label.config(text=f"❌ Wrong! Correct answer: {correct}", fg="#ff8a65")
            # Load and reduce volume
            sound = AudioSegment.from_wav("wrong.wav")
            quieter_sound = sound - 20
            temp_path = "temp_wrong.wav"
            quieter_sound.export(temp_path, format="wav")
            winsound.PlaySound(temp_path, winsound.SND_FILENAME)
            os.remove(temp_path)  # cleanup



        self.next_button.pack(pady=10)

    def next_question(self):
        self.question_index += 1
        if self.question_index < len(questions):
            self.display_question()
        else:
            self.show_final_score()

    def show_final_score(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        result = f"🎉 Quiz Finished!\n\nYour Score: {self.score} / {len(questions)}"
        tk.Label(
            self.master, text=result, font=("Helvetica", 16, "bold"),
            bg="#3e2723", fg="#fbe9e7", wraplength=700, justify="center"
        ).pack(pady=60)
        if self.score < (len(questions) / 2):
            winsound.PlaySound("retry.wav", winsound.SND_FILENAME)
            pass

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
