import customtkinter as ctk
import tkinter as tk
import math
import random

class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=("gray85", "gray17"))  # Light/dark background
        self.controller = controller
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main container with padding
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure((0,1,2), weight=1)
        
        # Title with decorative elements
        self.title_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        self.title_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.title_frame, 
            text="🎯 Подготовка к охотничьему экзамену 🎯",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#1f6aa5", "#4dabf7")
        )
        self.title_label.grid(row=0, column=0, pady=10)
        
        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="Выберите тему для тренировки или пройдите полный экзамен",
            font=ctk.CTkFont(size=16),
            text_color=("gray40", "gray60")
        )
        self.subtitle_label.grid(row=1, column=0, pady=(0, 10))
        
        # Topic buttons with icons and better styling
        self.topic_buttons_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.topic_buttons_frame.grid(row=1, column=0, sticky="ew")
        self.topic_buttons_frame.grid_columnconfigure((0,1), weight=1, uniform="topic")
        
        # Topic data with emojis
        topics = [
            ("Тема 1\nОхотничьи и охраняемые\nдикие животные", 1, "🦌"),
            ("Тема 2\nПравила охоты и ведения\nохотничьего хозяйства", 2, "📜"),
            ("Тема 3\nОрудия охоты", 3, "🔫"),
            ("Тема 4\nОказание первой помощи\nпри несчастных случаях", 4, "🏥")
        ]
        
        for i, (text, topic_id, emoji) in enumerate(topics):
            btn = ctk.CTkButton(
                self.topic_buttons_frame,
                text=f"{emoji}\n{text}",
                command=lambda tid=topic_id: self.start_topic_training(tid),
                height=80,
                font=ctk.CTkFont(size=16),
                fg_color=("gray80", "gray25"),
                hover_color=("gray70", "gray30"),
                border_width=2,
                border_color=("gray60", "gray40"),
                corner_radius=10
            )
            btn.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
        
        # Exam button with special styling
        self.exam_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.exam_frame.grid(row=2, column=0, pady=(30, 0), sticky="ew")
        self.exam_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.exam_button = ctk.CTkButton(
            self.exam_frame,
            text="🚀 ЭКЗАМЕН (2+3+3+2)\nПроверить свои знания",
            command=self.start_exam,
            height=70,
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=("#D35B58", "#E87370"),
            hover_color=("#C77C78", "#FF8A8A"),
            border_width=2,
            border_color=("#B44A48", "#D35B58"),
            corner_radius=15
        )
        self.exam_button.grid(row=0, column=0, padx=(20, 5), pady=10, sticky="ew")
        
        self.test_button = ctk.CTkButton(
            self.exam_frame,
            text="🔬 Тест (2 вопроса)\nПроверить анимацию",
            command=self.start_test,
            height=70,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            border_width=2,
            border_color=("gray60", "gray40"),
            corner_radius=15
        )
        self.test_button.grid(row=0, column=1, padx=(5, 20), pady=10, sticky="ew")
        
        # All questions button
        self.all_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.all_frame.grid(row=3, column=0, pady=(15, 0), sticky="ew")
        self.all_frame.grid_columnconfigure(0, weight=1)

        self.all_button = ctk.CTkButton(
            self.all_frame,
            text="📚 Все вопросы (251)",
            command=self.start_all_questions,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#4682B4", "#5B9BD5"),
            hover_color=("#36648B", "#4A8CBF"),
            border_width=2,
            border_color=("#36648B", "#3A7CBD"),
            corner_radius=10
        )
        self.all_button.grid(row=0, column=0, padx=20, pady=5, sticky="ew")

        # Per-topic all-questions row
        self.topic_all_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.topic_all_frame.grid(row=4, column=0, pady=(2, 0), sticky="ew")
        self.topic_all_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="topic_all")

        topic_all_labels = ["🦌 Тема 1", "📜 Тема 2", "🔫 Тема 3", "🏥 Тема 4"]
        for i, (text, tid) in enumerate(zip(topic_all_labels, (1, 2, 3, 4))):
            btn = ctk.CTkButton(
                self.topic_all_frame,
                text=text,
                command=lambda t=tid: self.start_topic_all(t),
                height=35,
                font=ctk.CTkFont(size=13),
                fg_color=("gray78", "gray27"),
                hover_color=("gray68", "gray35"),
                border_width=1,
                border_color=("gray60", "gray40"),
                corner_radius=8
            )
            btn.grid(row=0, column=i, padx=6, pady=4, sticky="ew")

        # Keyboard shortcut hint
        self.hint_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=("gray90", "gray20"),
            corner_radius=8
        )
        self.hint_frame.grid(row=5, column=0, pady=(10, 5), sticky="ew")
        self.hint_frame.grid_columnconfigure(0, weight=1)
        
        self.hint_label = ctk.CTkLabel(
            self.hint_frame,
            text="⌨️ Быстрые клавиши: 1 • 2 • 3 • 4 — тема,  5 — экзамен,  6 — все вопросы",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("gray50", "gray60")
        )
        self.hint_label.grid(row=0, column=0, padx=15, pady=8)
        
        # Confetti state
        self.confetti_pieces = []
        self.confetti_active = False

        # Add a decorative footer
        self.footer_label = ctk.CTkLabel(
            self.main_container,
            text="Удачной подготовки! 🍀",
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color=("gray50", "gray50")
        )
        self.footer_label.grid(row=6, column=0, pady=(10, 0))
    
    def start_topic_training(self, topic_id):
        self.stop_confetti()
        self.controller.question_loader.current_mode = ('topic', topic_id)
        self.controller.current_mode_name = 'topic'
        self.controller.show_frame("QuestionFrame")
    
    def start_exam(self):
        self.stop_confetti()
        self.controller.question_loader.current_mode = ('exam', None)
        self.controller.current_mode_name = 'exam'
        self.controller.show_frame("QuestionFrame")

    def start_test(self):
        self.stop_confetti()
        self.controller.question_loader.current_mode = ('test', None)
        self.controller.current_mode_name = 'test'
        self.controller.show_frame("QuestionFrame")

    def start_all_questions(self):
        self.stop_confetti()
        self.controller.question_loader.current_mode = ('all', None)
        self.controller.current_mode_name = 'all'
        self.controller.show_frame("QuestionFrame")

    def start_topic_all(self, topic_id):
        self.stop_confetti()
        self.controller.question_loader.current_mode = ('topic_all', topic_id)
        self.controller.current_mode_name = 'topic_all'
        self.controller.show_frame("QuestionFrame")

    # --- Firecracker confetti burst ---

    def start_confetti(self):
        if self.confetti_active:
            return
        self.confetti_active = True

        self.palette = [
            "#FF6B6B", "#FF4757", "#FFD93D", "#FFA502",
            "#6BCB77", "#2ED573", "#4D96FF", "#3742FA",
            "#A29BFE", "#F368E0", "#FF9FF3", "#00D2D3",
            "#FECA57", "#FF6348", "#7BED9F", "#70A1FF"
        ]

        self.confetti_pieces = []
        self.frame_w = 900
        self.frame_h = 700

        for _ in range(3):
            self._burst()
        self._animate_confetti()

    def stop_confetti(self):
        self.confetti_active = False
        for p in self.confetti_pieces:
            if 'widget' in p and p['widget'] is not None:
                p['widget'].destroy()
        self.confetti_pieces = []

    def _burst(self):
        if not self.confetti_active:
            return
        cx = random.randint(150, self.frame_w - 150)
        cy = random.randint(self.frame_h - 100, self.frame_h - 30)
        for _ in range(random.randint(20, 30)):
            angle = random.uniform(-85, 85)
            speed = random.uniform(8, 18)
            size = random.randint(4, 8)
            color = random.choice(self.palette)
            widget = tk.Frame(
                self,
                width=size,
                height=size,
                bg=color,
                highlightthickness=0
            )
            self.confetti_pieces.append({
                'widget': widget,
                'x': cx, 'y': cy,
                'dx': math.sin(math.radians(angle)) * speed,
                'dy': -abs(math.cos(math.radians(angle)) * speed) - random.uniform(3, 7),
                'color': color,
                'life': 1.0,
            })

    def _animate_confetti(self):
        if not self.confetti_active:
            return
        gravity = 0.3
        drag = 0.97
        remaining = 0

        for p in self.confetti_pieces[:]:
            p['dx'] *= drag
            p['dy'] += gravity
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['life'] -= 0.05

            if p['life'] <= 0:
                if p['widget'] is not None:
                    p['widget'].destroy()
                    p['widget'] = None
                continue

            remaining += 1
            widget = p['widget']
            if widget is not None:
                widget.configure(bg=self._fade_color(p['color'], p['life']))
                widget.place(x=int(p['x']), y=int(p['y']))

        if remaining > 0:
            self.after(25, self._animate_confetti)
        else:
            self.stop_confetti()

    @staticmethod
    def _fade_color(hex_color, life):
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        f = min(1.0, max(0, life))
        # fade towards the frame background color (gray85 / gray17)
        bg_val = 0xD9  # light mode
        if ctk.get_appearance_mode() == "Dark":
            bg_val = 0x2B
        r = int(r * f + bg_val * (1 - f))
        g = int(g * f + bg_val * (1 - f))
        b = int(b * f + bg_val * (1 - f))
        return f"#{r:02x}{g:02x}{b:02x}"