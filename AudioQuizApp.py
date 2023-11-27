import json
import tkinter as tk
from tkinter import messagebox, font as tkfont, ttk
from PIL import Image, ImageTk
import pygame


class AudioQuizApp:
    def __init__(self, root):
        self.root = root
        root.title("Audio Quality Quiz")

        style = ttk.Style()
        style.theme_use("clam")

        pygame.init()
        pygame.mixer.init()

        self.customFont = tkfont.Font(family="Helvetica", size=12)

        self.questions = self.load_questions()
        self.show_menu()

    def load_questions(self):
        with open("questions.json", "r") as file:
            return json.load(file)

    def add_question(self):
        # Create a new window for adding a question
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Question")

        ttk.Label(add_window, text="Title:").pack()
        title_entry = ttk.Entry(add_window)
        title_entry.pack()

        tk.Label(add_window, text="Audio Clip 1:").pack()
        clip1_entry = tk.Entry(add_window)
        clip1_entry.pack()

        tk.Label(add_window, text="Audio Clip 2:").pack()
        clip2_entry = tk.Entry(add_window)
        clip2_entry.pack()

        tk.Label(add_window, text="Audio Clip 3:").pack()
        clip3_entry = tk.Entry(add_window)
        clip3_entry.pack()

        tk.Label(add_window, text="Correct Answer (0, 1, or 2):").pack()
        correct_entry = tk.Entry(add_window)
        correct_entry.pack()

        tk.Label(add_window, text="Album Cover Path (optional):").pack()
        cover_entry = tk.Entry(add_window)
        cover_entry.pack()

        def submit_new_question():
            title = title_entry.get()
            clips = [clip1_entry.get(), clip2_entry.get(), clip3_entry.get()]
            correct = int(correct_entry.get())
            cover = cover_entry.get()
            new_question = {
                "title": title,
                "clips": clips,
                "correct": correct,
                "cover": cover,
            }
            self.questions.append(new_question)

            with open("questions.json", "w") as file:
                json.dump(self.questions, file, indent=4)

            add_window.destroy()

        submit_button = tk.Button(
            add_window, text="Add Question", command=submit_new_question
        )
        submit_button.pack()

    def show_menu(self):
        self.menu_frame = tk.Frame(self.root, padx=10, pady=10)
        self.menu_frame.pack(padx=10, pady=10)

        menu_title = tk.Label(
            self.menu_frame,
            text="Welcome to the Audio Quality Quiz",
            font=tkfont.Font(size=16, weight="bold"),
        )
        menu_title.pack(pady=(0, 20))

        start_button = tk.Button(
            self.menu_frame,
            text="Start Quiz",
            command=self.start_quiz,
            font=self.customFont,
        )
        start_button.pack(pady=5)

        add_button = tk.Button(
            self.menu_frame,
            text="Add A Question",
            command=self.add_question,
            font=self.customFont,
        )
        add_button.pack(pady=5)

    def start_quiz(self):
        self.menu_frame.destroy()
        self.setup_quiz()

    def setup_quiz(self):
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(padx=10, pady=10)

        self.title_label = tk.Label(
            self.frame, text="", font=tkfont.Font(size=16, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))

        self.current_question = 0
        self.setup_question(self.current_question)

    def setup_question(self, question_index):
        for widget in self.frame.winfo_children():
            if widget != self.title_label:
                widget.destroy()

        question = self.questions[question_index]
        self.title_label.config(text=question["title"])
        self.clips = question["clips"]
        self.correct_answer = question["correct"]
        self.cover_path = question["cover"]

        self.build_ui()

    def build_ui(self):
        if len(self.cover_path) >= 1:
            cover_image = Image.open(self.cover_path)
            cover_image = cover_image.resize((200, 200))
            self.cover_photo = ImageTk.PhotoImage(cover_image)
            cover_label = tk.Label(self.frame, image=self.cover_photo)
            cover_label.pack(pady=10)

        for i, clip in enumerate(self.clips):
            play_button = tk.Button(
                self.frame,
                text=f"Play Clip {i+1}",
                command=lambda c=clip: self.play_audio(c),
                font=self.customFont,
            )
            play_button.pack(pady=5)

        instruction_label = tk.Label(
            self.frame,
            text="Select the clip with the highest quality:",
            font=self.customFont,
        )
        instruction_label.pack(pady=(20, 10))

        self.var = tk.StringVar(value="-1")
        for i in range(len(self.clips)):
            radio_button = tk.Radiobutton(
                self.frame,
                text=f"Clip {i+1}",
                variable=self.var,
                value=i,
                font=self.customFont,
            )
            radio_button.pack()

        submit_button = tk.Button(
            self.frame,
            text="Submit Answer",
            command=self.check_answer,
            font=self.customFont,
        )
        submit_button.pack(pady=20)

    def play_audio(self, clip):
        pygame.mixer.music.load(clip)
        pygame.mixer.music.play(loops=0)

    def check_answer(self):
        pygame.mixer.music.stop()

        if int(self.var.get()) == self.correct_answer:
            messagebox.showinfo("Result", "Correct!")
            self.current_question += 1
            if self.current_question < len(self.questions):
                self.setup_question(self.current_question)
            else:
                messagebox.showinfo("Quiz Finished", "You have completed the quiz!")
                self.root.destroy()
        else:
            messagebox.showinfo("Result", "Incorrect. Try again!")


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioQuizApp(root)
    root.mainloop()
