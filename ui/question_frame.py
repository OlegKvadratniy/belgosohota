import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

class QuestionFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.questions = []
        self.current_question_index = 0
        self.user_answers = []  # Store user's answers for each question
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)  # Options frame row
        
        # Progress bar and label
        self.progress_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.progress_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        # Progress info frame
        self.progress_info = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        self.progress_info.grid(row=0, column=0, sticky="ew")
        self.progress_info.grid_columnconfigure((0,1,2), weight=1)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_info,
            text="Вопрос 0 из 0",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#1f6aa5", "#4dabf7")
        )
        self.progress_label.grid(row=0, column=0, sticky="w", padx=10)
        
        # Help button for explanation
        self.help_button = ctk.CTkButton(
            self.progress_info,
            text="❓ Помощь (X)",
            command=self.toggle_explanation,
            width=120,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        self.help_button.grid(row=0, column=2, sticky="e", padx=10)
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=8,
            corner_radius=4
        )
        self.progress_bar.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")
        self.progress_bar.set(0)
        
        # Question text frame with background
        self.question_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=("gray90", "gray20"),
            corner_radius=10
        )
        self.question_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.question_frame.grid_columnconfigure(0, weight=1)
        
        self.question_text = ctk.CTkTextbox(
            self.question_frame,
            font=ctk.CTkFont(size=18, weight="bold"),
            wrap="word",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            activate_scrollbars=False,
            border_width=0,
            height=80
        )
        self.question_text.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")
        
        # Options frame
        self.options_frame = ctk.CTkFrame(self.main_frame)
        self.options_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.options_frame.grid_columnconfigure(0, weight=1)
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        
        self.check_button = ctk.CTkButton(
            self.button_frame,
            text="Проверить ответ",
            command=self.check_answer,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            fg_color=("#1f6aa5", "#4dabf7"),
            hover_color=("#144870", "#2E8BC0")
        )
        self.check_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Explanation frame (initially hidden)
        self.explanation_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#FFF4E6", "#3D2E1F"),
            corner_radius=10,
            border_width=1,
            border_color=("#FFA500", "#8B6914")
        )
        self.explanation_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.explanation_frame.grid_columnconfigure(0, weight=1)
        self.explanation_frame.grid_remove()  # Hide initially
        
        self.explanation_text = ctk.CTkTextbox(
            self.explanation_frame,
            font=ctk.CTkFont(size=14),
            wrap="word",
            fg_color="transparent",
            text_color=("#664D03", "#FFE0B2"),
            activate_scrollbars=False,
            border_width=0,
            height=60
        )
        self.explanation_text.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")
        
        # State variables
        self.answer_checked = False
        self.option_vars = []  # For radiobuttons or checkboxes
        self.option_buttons = []  # To store the actual button widgets
        self.option_labels = []  # Labels for option text (wrapping support)
        self.option_frames = []  # Frames wrapping each option
        self.current_question_data = None  # Store current question for explanation
    
    def set_questions(self, questions):
        """Set the questions to be used in this frame."""
        self.questions = questions
        self.current_question_index = 0
        self.user_answers = [None] * len(questions)
        self.answer_checked = False
        self.load_question()
    
    def load_question(self):
        """Load the current question and update UI."""
        if not self.questions or self.current_question_index >= len(self.questions):
            # No more questions, go to results
            self.controller.show_frame("ResultsFrame")
            return
        
        self.current_question_data = self.questions[self.current_question_index]
        question_data = self.current_question_data
        
        # Update progress
        progress_text = f"Вопрос {self.current_question_index + 1} из {len(self.questions)}"
        self.progress_label.configure(text=progress_text)
        self.progress_bar.set((self.current_question_index) / len(self.questions))
        
        # Update question text
        self.question_text.configure(state="normal")
        self.question_text.delete("1.0", "end")
        self.question_text.insert("1.0", question_data['question'])
        self.question_text.configure(state="disabled")
        
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Reset option vars and buttons
        self.option_vars = []
        self.option_buttons = []
        self.option_labels = []
        self.option_frames = []
        self.feedback_label = None
        
        # Create options based on is_multiple with numbered prefixes
        options = question_data['options']
        is_multiple = question_data['is_multiple']
        
        for i, option_text in enumerate(options):
            numbered_text = f"{i + 1}. {option_text}"
            opt_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
            opt_frame.grid(row=i, column=0, padx=15, pady=4, sticky="ew")
            opt_frame.grid_columnconfigure(1, weight=1)
            self.option_frames.append(opt_frame)
            
            if is_multiple:
                var = tk.BooleanVar(value=False)
                widget = ctk.CTkCheckBox(
                    opt_frame,
                    text="",
                    variable=var,
                    font=ctk.CTkFont(size=14),
                    corner_radius=5,
                    border_width=2
                )
                widget.grid(row=0, column=0, sticky="w")
                
                label = ctk.CTkLabel(
                    opt_frame,
                    text=numbered_text,
                    font=ctk.CTkFont(size=14),
                    wraplength=620,
                    justify="left"
                )
                label.grid(row=0, column=1, padx=(8, 0), sticky="w")
                label.bind("<Button-1>", lambda e, v=var: v.set(not v.get()))
                
                self.option_vars.append(var)
                self.option_buttons.append(widget)
                self.option_labels.append(label)
            else:
                var = tk.StringVar(value="")
                widget = ctk.CTkRadioButton(
                    opt_frame,
                    text="",
                    variable=var,
                    value=str(i),
                    font=ctk.CTkFont(size=14),
                    border_width_checked=6,
                    radiobutton_width=20,
                    radiobutton_height=20
                )
                widget.grid(row=0, column=0, sticky="w")
                
                label = ctk.CTkLabel(
                    opt_frame,
                    text=numbered_text,
                    font=ctk.CTkFont(size=14),
                    wraplength=620,
                    justify="left"
                )
                label.grid(row=0, column=1, padx=(8, 0), sticky="w")
                label.bind("<Button-1>", lambda e, v=var, idx=i: v.set(str(idx)))
                
                self.option_vars.append(var)
                self.option_buttons.append(widget)
                self.option_labels.append(label)
        
        # Reset button state
        self.check_button.configure(text="Проверить ответ", state="normal")
        self.answer_checked = False
        
        # Hide explanation
        self.explanation_frame.grid_remove()
        self.explanation_text.configure(state="normal")
        self.explanation_text.delete("1.0", "end")
        self.explanation_text.configure(state="disabled")
    
    def check_answer(self):
        """Check the user's answer and show result."""
        if self.answer_checked:
            # If already checked, move to next question
            self.current_question_index += 1
            self.load_question()
            return
        
        question_data = self.questions[self.current_question_index]
        correct_indices = set(question_data['correct_answers'])
        
        # Get user's selected indices
        user_indices = set()
        for i, var in enumerate(self.option_vars):
            if question_data['is_multiple']:
                if var.get():
                    user_indices.add(i)
            else:
                if var.get() != "":
                    user_indices.add(int(var.get()))
        
        # Store user answer
        self.user_answers[self.current_question_index] = user_indices
        
        # Check if correct
        is_correct = (user_indices == correct_indices)
        
        # Update UI to show result
        self.show_result(is_correct, question_data)
        
        # Update button text
        self.check_button.configure(text="Следующий вопрос", state="normal")
        self.answer_checked = True
    
    def show_result(self, is_correct, question_data):
        """Show the result of the answer check."""
        is_multiple = question_data['is_multiple']
        correct_indices = set(question_data['correct_answers'])
        
        # Get user-selected indices for highlighting
        user_selected = set()
        for i, var in enumerate(self.option_vars):
            if is_multiple:
                if var.get():
                    user_selected.add(i)
            else:
                if var.get() != "":
                    user_selected.add(int(var.get()))
        
        # Mark each option visually and add ✓ / ✗ symbols
        options = question_data['options']
        for i, option_widget in enumerate(self.option_buttons):
            label = self.option_labels[i]
            opt_frame = self.option_frames[i]
            # Reconstruct base text: remove any existing ✓/✗
            current_text = label.cget("text")
            for sym in [" ✅", " ❌", " ✓", " ✗"]:
                if current_text.endswith(sym):
                    current_text = current_text[:-len(sym)]
                    break
            
            if i in correct_indices and i in user_selected:
                label.configure(
                    text=f"{current_text} ✅",
                    text_color=("#0F5A38", "#A8E6CF")
                )
                opt_frame.configure(fg_color=("#2CC985", "#1A7A4D"))
                option_widget.configure(
                    fg_color=("#2CC985", "#1A7A4D")
                )
                if not is_multiple:
                    option_widget.configure(
                        border_width_checked=6,
                        hover_color=("#2CC985", "#1A7A4D")
                    )
            elif i in correct_indices and i not in user_selected:
                label.configure(
                    text=f"{current_text} ✅",
                    text_color=("#0F5A38", "#A8E6CF")
                )
                opt_frame.configure(fg_color=("#2CC985", "#1A7A4D"))
                option_widget.configure(
                    fg_color=("#2CC985", "#1A7A4D")
                )
                if not is_multiple:
                    option_widget.configure(
                        border_width_checked=6,
                        hover_color=("#2CC985", "#1A7A4D")
                    )
            elif i in user_selected and i not in correct_indices:
                label.configure(
                    text=f"{current_text} ✗",
                    text_color=("#FADBD8", "#F5B7B1")
                )
                opt_frame.configure(fg_color=("#FF5555", "#A33A3A"))
                option_widget.configure(
                    fg_color=("#FF5555", "#A33A3A")
                )
                if not is_multiple:
                    option_widget.configure(
                        border_width_checked=6,
                        hover_color=("#FF5555", "#A33A3A")
                    )
            else:
                pass
        
        # Show feedback label
        if is_correct:
            feedback_text = "✅ Правильно!"
            feedback_color = ("#2CC985", "#1A7A4D")
        else:
            correct_texts = [f"{i+1}. {options[i]}" for i in correct_indices]
            feedback_text = f"❌ Неверно. Правильный ответ: {', '.join(correct_texts)}"
            feedback_color = ("#FF5555", "#A33A3A")
        
        # Remove old feedback label if it exists
        if hasattr(self, 'feedback_label') and self.feedback_label is not None:
            self.feedback_label.destroy()
        
        self.feedback_label = ctk.CTkLabel(
            self.options_frame,
            text=feedback_text,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=feedback_color,
            wraplength=650
        )
        self.feedback_label.grid(row=len(question_data['options']), column=0, padx=20, pady=10, sticky="ew")
        
        # Show explanation
        explanation = question_data['explanation']
        self.explanation_text.configure(state="normal")
        self.explanation_text.delete("1.0", "end")
        self.explanation_text.insert("1.0", f"💡 {explanation}")
        self.explanation_text.configure(state="disabled")
        self.explanation_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
    
    def select_option(self, index):
        """Select/toggle the option at the given index via keyboard."""
        if index < 0 or index >= len(self.option_vars):
            return
        if self.answer_checked:
            return
        question_data = self.current_question_data
        if question_data is None:
            return
        is_multiple = question_data['is_multiple']
        if is_multiple:
            var = self.option_vars[index]
            var.set(not var.get())
        else:
            for i, var in enumerate(self.option_vars):
                if i == index:
                    var.set(str(i))
                else:
                    var.set("")

    def toggle_explanation(self, event=None):
        """Toggle the explanation frame visibility."""
        if self.current_question_data and 'explanation' in self.current_question_data:
            self.explanation_text.configure(state="normal")
            self.explanation_text.delete("1.0", "end")
            self.explanation_text.insert("1.0", f"💡 {self.current_question_data['explanation']}")
            self.explanation_text.configure(state="disabled")
        
        if self.explanation_frame.winfo_ismapped():
            self.explanation_frame.grid_remove()
        else:
            self.explanation_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
            self.explanation_frame.lift()
    
    def get_score(self):
        """Calculate the current score."""
        if not self.questions:
            return 0
        correct_count = 0
        for i, question in enumerate(self.questions):
            correct_indices = set(question['correct_answers'])
            user_indices = set()
            if self.user_answers[i] is not None:
                user_indices = self.user_answers[i]
            if user_indices == correct_indices:
                correct_count += 1
        return correct_count
