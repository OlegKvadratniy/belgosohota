import customtkinter as ctk
from ui.main_menu_frame import MainMenuFrame
from ui.question_frame import QuestionFrame
from ui.results_frame import ResultsFrame
from utils.question_loader import QuestionLoader

class HuntExamApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("🎯 Подготовка к охотничьему экзамену")
        self.geometry("900x700")
        self.minsize(750, 550)
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("system")  # Follow system theme
        ctk.set_default_color_theme("blue")
        
        # Configure grid for the root window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Initialize question loader
        self.question_loader = QuestionLoader("questions.json")
        
        # Container for frames
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        
        # Dictionary to hold frames
        self.frames = {}
        
        # Create and store frames
        for F in (MainMenuFrame, QuestionFrame, ResultsFrame):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Reference to the question frame for score retrieval
        self.question_frame = None
        
        # Track current mode for results display
        self.current_mode_name = 'menu'  # 'menu', 'topic', or 'exam'
        
        # Show main menu first
        self.show_frame("MainMenuFrame")
    
    def show_frame(self, frame_name):
        """Show a frame by raising it to the top"""
        # Clean up all bindings
        self.unbind("<Key-x>")
        self.unbind("<Key-X>")
        self.unbind("<Return>")
        for key in "123456789":
            self.unbind(f"<Key-{key}>")
        
        frame = self.frames[frame_name]
        frame.tkraise()
        
        # If showing main menu, bind keyboard shortcuts 1-4 for topics, 5 for exam, 6 for all
        if frame_name == "MainMenuFrame":
            self.bind("<Key-1>", lambda e: frame.start_topic_training(1))
            self.bind("<Key-2>", lambda e: frame.start_topic_training(2))
            self.bind("<Key-3>", lambda e: frame.start_topic_training(3))
            self.bind("<Key-4>", lambda e: frame.start_topic_training(4))
            self.bind("<Key-5>", lambda e: frame.start_exam())
            self.bind("<Key-6>", lambda e: frame.start_all_questions())
        
        # If showing question frame, load questions based on current mode and keep reference
        if frame_name == "QuestionFrame":
            qf = self.frames["QuestionFrame"]
            self.bind("<Key-x>", lambda e: qf.toggle_explanation())
            self.bind("<Key-X>", lambda e: qf.toggle_explanation())
            self.bind("<Return>", lambda e: qf.check_answer())
            self.bind("<KP_Enter>", lambda e: qf.check_answer())
            for i in range(1, 10):
                self.bind(f"<Key-{i}>", lambda e, idx=i-1: qf.select_option(idx))
            questions = self.question_loader.get_questions_for_mode()
            frame.set_questions(questions)
            self.question_frame = frame
        
        # If showing results frame, calculate score from question frame
        if frame_name == "ResultsFrame":
            if self.question_frame is not None:
                score = self.question_frame.get_score()
                total = len(self.question_frame.questions) if self.question_frame.questions else 10
                mode = self.current_mode_name
                frame.update_results(score, total, mode)
            else:
                frame.update_results(0, 10, 'topic')

if __name__ == "__main__":
    app = HuntExamApp()
    # Center window on screen
    app.update_idletasks()
    width = 900
    height = 700
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f'{width}x{height}+{x}+{y}')
    app.mainloop()