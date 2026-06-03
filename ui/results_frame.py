import customtkinter as ctk
import tkinter as tk
import math
import random

class ResultsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=("gray85", "gray17"))
        self.controller = controller
        self.confetti_pieces = []
        self.confetti_active = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="📊 Результаты тестирования",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=("#1f6aa5", "#4dabf7")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(30, 10))

        # Score display - green prominent table
        self.score_table = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#CCF5D3", "#1A5C2A"),
            corner_radius=15,
            border_width=3,
            border_color=("#2ECC71", "#27AE60")
        )
        self.score_table.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.score_table.grid_columnconfigure(0, weight=1)

        self.score_label = ctk.CTkLabel(
            self.score_table,
            text="",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#1A5C2A", "#CCF5D3")
        )
        self.score_label.grid(row=0, column=0, padx=20, pady=20)

        # Result badge
        self.badge_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#E8F8F0", "#1A4D2E"),
            corner_radius=12,
            border_width=2,
            border_color=("#2ECC71", "#1ABC9C")
        )
        self.badge_frame.grid(row=2, column=0, padx=40, pady=5, sticky="ew")
        self.badge_frame.grid_columnconfigure(0, weight=1)

        self.badge_label = ctk.CTkLabel(
            self.badge_frame,
            text="",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#1A5C2A", "#A8E6CF")
        )
        self.badge_label.grid(row=0, column=0, padx=20, pady=12)

        # Motivational message
        self.message_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color=("gray40", "gray60"),
            wraplength=500
        )
        self.message_label.grid(row=3, column=0, padx=20, pady=10)

        # Button frame
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, padx=20, pady=(20, 30), sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.retry_button = ctk.CTkButton(
            self.button_frame,
            text="🔄 Пройти еще раз",
            command=self.retry,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            fg_color=("#1f6aa5", "#4dabf7"),
            hover_color=("#144870", "#2E8BC0")
        )
        self.retry_button.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="ew")

        self.menu_button = ctk.CTkButton(
            self.button_frame,
            text="🏠 В главное меню",
            command=self.go_to_menu,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        self.menu_button.grid(row=0, column=1, padx=(10, 20), pady=10, sticky="ew")

        # Confetti state

    def update_results(self, score, total_questions=10, mode='topic'):
        """Update the results display."""
        if total_questions <= 0:
            total_questions = 10

        errors = total_questions - score
        percentage = (score / total_questions) * 100
        passed = (errors <= 1)  # 1 error max for pass

        # Update score
        self.score_label.configure(
            text=f"Правильных ответов: {score} из {total_questions}\n"
                 f"({percentage:.0f}%) — ошибок: {errors}"
        )

        badge_labels = {
            'exam': ("ЭКЗАМЕН", "🏆", "❌"),
            'test': ("ТЕСТ", "✅", "❌"),
            'topic': ("ТЕМА", "✅", "❌"),
            'topic_all': ("ТЕМА (ВСЕ ВОПРОСЫ)", "✅", "❌"),
            'all': ("ВСЕ ВОПРОСЫ", "✅", "❌"),
        }
        label, ok_icon, fail_icon = badge_labels.get(mode, badge_labels['topic'])

        if passed:
            badge_color = ("#2ECC71", "#1ABC9C")
            badge_text = f"{ok_icon} {label} СДАН{'А' if mode in ('topic', 'topic_all') else ''}! {ok_icon}"
            if errors == 0:
                message = "Идеально! Ни одной ошибки! 🎉🥳"
            else:
                message = "Отличный результат! Допущена всего 1 ошибка. 🥳"
        else:
            badge_color = ("#E74C3C", "#C0392B")
            badge_text = f"{fail_icon} {label} НЕ СДАН{'А' if mode in ('topic', 'topic_all') else ''} {fail_icon}"
            message = f"Допущено {errors} ошибок. Для сдачи нужно не более 1 ошибки. Повторите материал!"

        self.badge_frame.configure(
            fg_color=("#FADBD8", "#3D1A1A") if not passed else ("#D5F5E3", "#1A4D2E"),
            border_color=badge_color
        )
        self.badge_label.configure(text=badge_text, text_color=badge_color)
        self.message_label.configure(text=message)

        # Stop previous confetti if any
        self.stop_confetti()

        # Start confetti burst on perfect score (0 errors)
        if errors == 0:
            self.start_confetti()

    def retry(self):
        self.stop_confetti()
        self.controller.show_frame("QuestionFrame")

    def go_to_menu(self):
        had_confetti = self.confetti_active
        self.stop_confetti()
        if had_confetti:
            self.controller.frames["MainMenuFrame"].start_confetti()
        self.controller.show_frame("MainMenuFrame")

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
            widget = tk.Frame(self, width=size, height=size, bg=color, highlightthickness=0)
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
        bg_val = 0xD9 if ctk.get_appearance_mode() == "Light" else 0x2B
        r = int(r * f + bg_val * (1 - f))
        g = int(g * f + bg_val * (1 - f))
        b = int(b * f + bg_val * (1 - f))
        return f"#{r:02x}{g:02x}{b:02x}"
