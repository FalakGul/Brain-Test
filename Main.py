import tkinter as tk
from tkinter import messagebox
import random
import time

# Global Variables
score = 0
current_question = 0
questions_set = []
start_time = 0
highest_scores = {"basic": 0, "intermediate": 0, "advanced": 0}
lowest_scores = {"basic": float('inf'), "intermediate": float('inf'), "advanced": float('inf')}

def load_questions(level):
    questions = []
    filename = f"{level}_questions.txt"
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                question = parts[0]
                options = [option.strip() for option in parts[1:5]]
                answer = parts[5].strip()  # Ensure there's no extra whitespace
                questions.append((question, options, answer))
    except FileNotFoundError:
        messagebox.showerror("Error", f"Question file '{filename}' not found.")
        return None
    return questions

def load_scores():
    try:
        with open("highest_scores.txt", "r") as file:
            for line in file:
                level, score = line.strip().split(":")
                highest_scores[level] = int(score)
        with open("lowest_scores.txt", "r") as file:
            for line in file:
                level, score = line.strip().split(":")
                lowest_scores[level] = int(score)
    except FileNotFoundError:
        pass

def save_scores():
    with open("highest_scores.txt", "w") as file:
        for level, score in highest_scores.items():
            file.write(f"{level}:{score}\n")
    with open("lowest_scores.txt", "w") as file:
        for level, score in lowest_scores.items():
            file.write(f"{level}:{score}\n")

def start_quiz():
    selected_level = level_var.get()
    if selected_level:
        global questions_set, start_time, current_question, score
        questions_set = load_questions(selected_level)
        if questions_set:
            start_time = time.time()
            score = 0
            current_question = 0
            show_question()
            intro_label.pack_forget()
            level_label.pack_forget()
            level_frame.pack_forget()
            start_button.pack_forget()
            timer_label.pack(pady=10)  # Display timer label
            update_timer()  # Start updating the timer
    else:
        messagebox.showerror("Error", "Please select a difficulty level.")

def show_question():
    global current_question
    if current_question < len(questions_set):
        question_data = questions_set[current_question]
        question_label.config(text=question_data[0], font=('Arial', 14), wraplength=400)
        question_label.pack(pady=20)
        option_var.set(None)
        for i, option in enumerate(question_data[1]):
            option_buttons[i].config(text=option, value=option, font=('Arial', 12), padx=20, pady=5)
            option_buttons[i].pack(pady=5)
        submit_button.config(font=('Arial', 12))
        submit_button.pack(pady=20)
    else:
        end_quiz()

def update_timer():
    elapsed_time = int(time.time() - start_time)
    timer_label.config(text=f"Time: {elapsed_time} seconds", font=('Arial', 12))
    root.after(1000, update_timer)

def submit_answer():
    global current_question, score
    selected_option = option_var.get()
    correct_answer = questions_set[current_question][2]
    print(f"Selected: '{selected_option}', \t\tCorrect: '{correct_answer}'")  # Debug statement
    if selected_option == correct_answer:
        score += 10  # Fixed score for each correct answer
    current_question += 1
    for btn in option_buttons:
        btn.pack_forget()
    submit_button.pack_forget()
    show_question()

def end_quiz():
    global score
    elapsed_time = int(time.time() - start_time)
    messagebox.showinfo("Quiz Finished", f"Your final score is: {score}. Total time taken: {elapsed_time} seconds.")
    level = level_var.get()
    if score > highest_scores[level]:
        highest_scores[level] = score
        messagebox.showinfo("New High Score!", f"Congratulations! You achieved a new high score for {level} level.")
    if score < lowest_scores[level]:
        lowest_scores[level] = score
        messagebox.showinfo("New Low Score!", f"Congratulations! You achieved a new low score for {level} level.")
    save_scores()
    reset_quiz()

def reset_quiz():
    intro_label.pack(pady=20)
    level_label.pack(pady=10)
    level_frame.pack(pady=10)
    start_button.pack(pady=10)
    question_label.pack_forget()
    for btn in option_buttons:
        btn.pack_forget()
    submit_button.pack_forget()
    timer_label.pack_forget()

def show_leaderboard():
    messagebox.showinfo("Leaderboard", f"Highest Scores:\nBasic: {highest_scores['basic']}\nIntermediate: {highest_scores['intermediate']}\nAdvanced: {highest_scores['advanced']}\n\nLowest Scores:\nBasic: {lowest_scores['basic']}\nIntermediate: {lowest_scores['intermediate']}\nAdvanced: {lowest_scores['advanced']}")

# Initialize the main window
root = tk.Tk()
root.title("Brain Test Challenge")
root.configure(background='#FFD1DC')
root.geometry("550x500")

# Create widgets
intro_label = tk.Label(root, text="Welcome to Brain Test Challenge!", font=('Arial', 16))
intro_label.pack(pady=20)

level_label = tk.Label(root, background='#FFD1DC' , text="Choose your level:", font=('Arial', 14))
level_label.pack(pady=10)

level_frame = tk.Frame(root, borderwidth=3 ,background="#CDC3E3" , relief='solid')
level_frame.pack(pady=10)

level_var = tk.StringVar()

basic_button = tk.Radiobutton(level_frame, background="#CDC3E3", text="Basic", variable=level_var, value='basic', font=('Arial', 12))
basic_button.pack(side=tk.LEFT, padx=10)

medium_button = tk.Radiobutton(level_frame, background="#CDC3E3" ,  text="Intermediate", variable=level_var, value='intermediate', font=('Arial', 12))
medium_button.pack(side=tk.LEFT, padx=10)

hard_button = tk.Radiobutton(level_frame,background="#CDC3E3" , text="Advanced", variable=level_var, value='advanced', font=('Arial', 12))
hard_button.pack(side=tk.LEFT, padx=10)

question_label = tk.Label(root, text="", font=('Arial', 14), wraplength=400)

option_var = tk.StringVar()

option_buttons = [tk.Radiobutton(root, text="", variable=option_var, value="", font=('Arial', 12))
                  for _ in range(4)]

submit_button = tk.Button(root, text="Submit", command=submit_answer, font=('Arial', 12))

timer_label = tk.Label(root, text="", font=('Arial', 12))

start_button = tk.Button(root, text="Start Quiz", background="#CF9FFF", command=start_quiz, font=('Arial', 12))
start_button.pack(pady=10)

leaderboard_button = tk.Button(root, text="Leaderboard", background="#CF9FFF", command=show_leaderboard, font=('Arial', 12))
leaderboard_button.pack(pady=10)

# Load scores from files
load_scores()

# Start the main loop
root.mainloop()
