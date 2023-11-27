import json
import tkinter as tk
from tkinter import messagebox, font as tkfont, ttk
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
import pygame
import shutil
import os


class AudioQuizApp:
    def __init__(self, root):
        self.first_try_correct_count = 0
        self.attempted = False

        self.root = root
        root.title("Audio Quality Quiz")

        root.configure(bg="#2a2b2a")

        pygame.init()
        pygame.mixer.init()

        self.customFont = tkfont.Font(family="Helvetica", size=12)

        self.questions = self.load_questions()
        self.show_menu()

    def load_questions(self):
        with open("questions.json", "r") as file:
            return json.load(file)

    def add_question(self):
        add_window = ctk.CTkToplevel(self.root)
        add_window.title("Add New Question")
        style = ttk.Style(add_window)
        style.configure("Custom.TLabel", background="#252425", foreground="white")
        ttk.Label(add_window, text="Title:", style="Custom.TLabel").pack()
        title_entry = tk.Entry(add_window, bg='grey', fg='white')
        title_entry.pack()

        def select_audio_file(entry):
            file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
            if file_path:
                destination = os.path.join('audio', os.path.basename(file_path))
                shutil.copy(file_path, destination)
                entry.delete(0, tk.END)
                entry.insert(0, destination)

        def select_image_file(entry):
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
            if file_path:
                destination = os.path.join('images', os.path.basename(file_path))
                shutil.copy(file_path, destination)
                entry.delete(0, tk.END)
                entry.insert(0, destination)

        ttk.Label(add_window, text="Audio Clip 1:", style="Custom.TLabel").pack()
        clip1_entry = tk.Entry(add_window, bg='grey', fg='white')
        clip1_entry.pack()
        clip1_button = ctk.CTkButton(add_window, text="Select File", command=lambda: select_audio_file(clip1_entry))
        clip1_button.pack(pady='5px')

        ttk.Label(add_window, text="Audio Clip 2:", style="Custom.TLabel").pack()
        clip2_entry = tk.Entry(add_window, bg='grey', fg='white')
        clip2_entry.pack()
        clip2_button = ctk.CTkButton(add_window, text="Select File", command=lambda: select_audio_file(clip2_entry))
        clip2_button.pack(pady='5px')

        ttk.Label(add_window, text="Audio Clip 3:", style="Custom.TLabel").pack()
        clip3_entry = tk.Entry(add_window, bg='grey', fg='white')
        clip3_entry.pack()
        clip3_button = ctk.CTkButton(add_window, text="Select File", command=lambda: select_audio_file(clip3_entry))
        clip3_button.pack(pady='5px')

        ttk.Label(add_window, text="Correct Answer (0, 1, or 2):", style="Custom.TLabel").pack()
        correct_entry = tk.Entry(add_window, bg='grey', fg='white')
        correct_entry.pack()

        ttk.Label(add_window, text="Album Cover Path (optional):", style="Custom.TLabel").pack()
        cover_entry = tk.Entry(add_window, bg='grey', fg='white')
        cover_entry.pack()
        cover_button = ctk.CTkButton(add_window, text="Select File", command=lambda: select_image_file(cover_entry))
        cover_button.pack(pady='5px')

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

        submit_button = ctk.CTkButton(add_window, text="Add Question", command=submit_new_question, fg_color='green', text_color='white')
        submit_button.pack(pady='15px')


    def show_menu(self):
        self.menu_frame = ctk.CTkFrame(self.root)
        self.menu_frame.pack(padx="10px", pady="10px")

        menu_title = ctk.CTkLabel(
            self.menu_frame,
            text="Welcome to the Audio Quality Quiz",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        menu_title.pack(pady=(0, 20))

        start_button = ctk.CTkButton(
            self.menu_frame,
            text="Start Quiz",
            command=self.start_quiz,
        )
        start_button.pack(pady=5)

        add_button = ctk.CTkButton(
            self.menu_frame,
            text="Add A Question",
            command=self.add_question,
        )
        add_button.pack(pady=5)

    def start_quiz(self):
        self.menu_frame.destroy()
        self.setup_quiz()

    def setup_quiz(self):
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.title_label = tk.Label(
            self.frame, text="", font=tkfont.Font(size=16, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))

        self.current_question = 0
        self.setup_question(self.current_question)

    def setup_question(self, question_index):
        self.attempted = False
        for widget in self.frame.winfo_children():
            if widget != self.title_label:
                widget.destroy()

        question = self.questions[question_index]
        self.title_label.config(text=question["title"], bg="#2a2b2a", fg="white")
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
            play_button = ctk.CTkButton(
                self.frame,
                text=f"Play Clip {i+1}",
                command=lambda c=clip: self.play_audio(c),
            )
            play_button.pack(pady=5)

        instruction_label = ctk.CTkLabel(
            self.frame,
            text="Select the clip with the highest quality:",
        )
        instruction_label.pack(pady=(20, 10))

        self.var = tk.StringVar(value="-1")
        for i in range(len(self.clips)):
            radio_button = tk.Radiobutton(
                self.frame,
                activebackground="green",
                text=f"Clip {i+1}",
                variable=self.var,
                value=i,
                font=self.customFont,
                bg="#2a2b2a",
                fg="white",
                selectcolor="#1e6aa4",
            )
            radio_button.pack()

        submit_button = ctk.CTkButton(
            self.frame,
            text="Submit Answer",
            command=self.check_answer,
        )
        submit_button.pack(pady=20)

    def play_audio(self, clip):
        pygame.mixer.music.load(clip)
        pygame.mixer.music.play(loops=0)

    def check_answer(self):
        pygame.mixer.music.stop()

        selected_answer = int(self.var.get())
        if selected_answer == self.correct_answer:
            if not self.attempted:
                self.first_try_correct_count += 1
                self.attempted = True
            messagebox.showinfo("Result", "Correct!")
            self.current_question += 1
            if self.current_question < len(self.questions):
                self.setup_question(self.current_question)
            else:
                self.show_results()
                self.root.destroy()
        else:
            messagebox.showinfo("Result", "Incorrect. Try again!")
            self.attempted = True

    def show_results(self):
        messagebox.showinfo(
            "Quiz Finished",
            f"You have completed the quiz!\n"
            f"Results: {(self.first_try_correct_count/len(self.questions)) * 100}%\n{self.first_try_correct_count} out of {len(self.questions)} correct",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioQuizApp(root)
    root.mainloop()
