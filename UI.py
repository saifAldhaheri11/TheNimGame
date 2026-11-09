# This file contains the graphical interface
import math
import time
import tkinter as tk

import game
import scoring
import sound
from scoreboard import Scoreboard
from session import DIFFICULTIES, GameSession


# Interface colors
BACKGROUND = "#081C14"
PANEL = "#19432F"
BOARD = "#246348"
GOLD = "#FFD54A"
WHITE = "#FFFFFF"
LIGHT = "#DCEDE3"
BORDER = "#79AD90"

# A colored button made from a label
class ColorButton:

    def __init__(
        self,
        parent,
        text,
        command,
        primary=False,
        value=None,
        width=0
    ):
        self.command = command
        self.value = value
        self.primary = primary
        self.selected = False
        self.enabled = True
        self.hovered = False
        self.focused = False

        self.widget = tk.Label(
            parent,
            text=text,
            font=("Helvetica", 13, "bold"),
            padx=18,
            pady=10,
            width=width,
            cursor="hand2",
            highlightthickness=3,
            takefocus=True
        )

        self.widget.bind("<Button-1>", self.click)
        self.widget.bind("<space>", self.key_press)
        self.widget.bind("<Enter>", self.mouse_enter)
        self.widget.bind("<Leave>", self.mouse_leave)
        self.widget.bind("<FocusIn>", self.focus_in)
        self.widget.bind("<FocusOut>", self.focus_out)

        self.paint()

    # Update the button colors
    def paint(self):
        background = PANEL
        text = WHITE
        border = BORDER

        if self.primary or self.selected:
            background = GOLD
            text = BACKGROUND

        if self.hovered or self.focused:
            border = GOLD

            if self.primary or self.selected:
                background = "#FFE789"
            else:
                background = "#2D6848"

        if not self.enabled:
            background = "#263F32"
            text = "#CCDCD2"
            border = "#557762"

        self.widget.configure(
            bg=background,
            fg=text,
            highlightbackground=border,
            highlightcolor=border,
            takefocus=self.enabled
        )

        if self.enabled:
            self.widget.configure(cursor="hand2")
        else:
            self.widget.configure(cursor="")

    def set_enabled(self, enabled):
        self.enabled = enabled
        self.paint()

    def set_selected(self, selected):
        self.selected = selected
        self.paint()

    def set_text(self, text):
        self.widget.configure(text=text)

    # Run the action, with an optional value
    def activate(self):
        if self.enabled:
            if self.value is None:
                self.command()
            else:
                self.command(self.value)

    def click(self, event):
        if self.enabled:
            self.widget.focus_set()
            self.activate()

        return "break"

    def key_press(self, event):
        self.activate()
        return "break"

    def mouse_enter(self, event):
        self.hovered = True
        self.paint()

    def mouse_leave(self, event):
        self.hovered = False
        self.paint()

    def focus_in(self, event):
        self.focused = True
        self.paint()

    def focus_out(self, event):
        self.focused = False
        self.paint()


# An on/off switch with a title and a short description
class ToggleSwitch:

    def __init__(
        self, parent, title, note, variable, scale=1.0,
        on_change=None
    ):
        self.variable = variable
        self.on_change = on_change
        self.scale = scale
        self.focused = False

        self.widget = tk.Frame(
            parent,
            bg=parent.cget("bg"),
            cursor="hand2",
            takefocus=True,
            highlightthickness=2,
            highlightbackground=parent.cget("bg"),
            highlightcolor=GOLD
        )

        text = tk.Frame(self.widget, bg=parent.cget("bg"))
        text.pack(side="left", fill="x", expand=True, padx=(4, 30))

        tk.Label(
            text, text=title, bg=parent.cget("bg"), fg=WHITE,
            font=("Helvetica", 15, "bold"), anchor="w"
        ).pack(anchor="w")

        tk.Label(
            text, text=note, bg=parent.cget("bg"), fg=LIGHT,
            font=("Helvetica", 11), anchor="w"
        ).pack(anchor="w")

        self.width = int(56 * scale)
        self.height = int(30 * scale)

        self.switch = tk.Canvas(
            self.widget,
            width=self.width,
            height=self.height,
            bg=parent.cget("bg"),
            highlightthickness=0
        )
        self.switch.pack(side="right", padx=4)

        for widget in (self.widget, text, self.switch) + tuple(
            text.winfo_children()
        ):
            widget.bind("<Button-1>", self.toggle)

        self.widget.bind("<space>", self.toggle)
        self.widget.bind("<Return>", self.toggle)

        self.paint()

    # Draw the pill-shaped track and the round knob
    def paint(self):
        canvas = self.switch
        canvas.delete("all")

        on = self.variable.get()
        w, h = self.width, self.height
        r = h / 2
        track = GOLD if on else "#3B5A4A"

        canvas.create_oval(0, 0, h, h, fill=track, outline="")
        canvas.create_oval(w - h, 0, w, h, fill=track, outline="")
        canvas.create_rectangle(r, 0, w - r, h, fill=track, outline="")

        pad = 3 * self.scale
        x = w - h if on else 0

        canvas.create_oval(
            x + pad, pad, x + h - pad, h - pad,
            fill=WHITE if on else LIGHT,
            outline=""
        )

    def toggle(self, event=None):
        self.variable.set(not self.variable.get())
        self.widget.focus_set()
        self.paint()

        if self.on_change is not None:
            self.on_change()

        return "break"


# An ordinary class that contains the window
class NimApp:

    def __init__(self):
        # Fix blurry text on Windows: tell Windows this app handles
        # high-DPI screens itself instead of stretching a small image
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError, ImportError):
            pass  # Not Windows, or an older Windows version

        self.window = tk.Tk()
        self.window.title("The NIM Game - Intro to AI Project")
        self.window.configure(bg=BACKGROUND)

        # Screen scale: 1.0 at 100% Windows scaling, 1.5 at 150%
        self.scale = max(1.0, self.window.winfo_fpixels("1i") / 96)
        self.turn_started = None

        width = min(
            self.px(1100),
            self.window.winfo_screenwidth() - 40
        )
        height = min(
            self.px(860),
            self.window.winfo_screenheight() - 80
        )
        self.window.geometry(f"{width}x{height}")
        self.window.minsize(
            min(self.px(900), width),
            min(self.px(700), height)
        )

        self.difficulty = "Medium"
        self.first_player = "Player"
        self.starting_objects = game.INITIAL_OBJECTS

        self.scoreboard = Scoreboard()

        self.screen = "menu"
        self.session = None
        self.dialog = None

        self.selected = set()
        self.ai_highlight = set()
        self.focus_match = None
        self.hovered_match = None

        self.pending = None
        self.buttons = []

        self.animations = tk.BooleanVar(
            master=self.window,
            value=True
        )
        self.sound = tk.BooleanVar(
            master=self.window,
            value=True
        )

        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.bind("<Return>", self.enter_key)
        self.window.bind("<Escape>", self.escape_key)

        self.show_menu()

    # Convert a size in pixels at 100% scaling to this screen
    def px(self, value):
        return int(value * self.scale)

    # Play a sound effect if sounds are turned on
    def play(self, name):
        if self.sound.get():
            sound.play(name, self.window)

    # Keep the existing main.py working
    def mainloop(self):
        self.window.mainloop()

    # Create a label
    def label(
        self,
        parent,
        text,
        size=14,
        color=WHITE,
        bold=False
    ):
        weight = "normal"

        if bold:
            weight = "bold"

        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color,
            font=("Times", size, weight)
        )

    # Create and remember a button
    def button(
        self,
        parent,
        text,
        command,
        primary=False,
        value=None,
        width=0
    ):
        button = ColorButton(
            parent,
            text,
            command,
            primary,
            value,
            width
        )

        self.buttons.append(button)
        return button

    # Stop an unfinished AI action
    def cancel_pending(self):
        if self.pending is not None:
            self.window.after_cancel(self.pending)
            self.pending = None

    # Clear the window for a new page.
    # Every page is drawn inside the same window, no popups.
    def shell(self, title=None, back=None):
        self.cancel_pending()

        for widget in self.window.winfo_children():
            widget.destroy()

        self.buttons = []
        self.dialog = None

        # Only menu pages get a top bar, the game uses the full window
        if title is not None:
            header = tk.Frame(
                self.window,
                bg=BACKGROUND,
                padx=28,
                pady=14
            )
            header.pack(fill="x")

            if back is not None:
                self.button(
                    header,
                    "\u2190  Back",
                    back
                ).widget.pack(side="left", padx=(0, 18))

            self.label(
                header,
                title,
                30,
                bold=True
            ).pack(side="left")

            tk.Frame(
                self.window,
                bg=BORDER,
                height=1
            ).pack(fill="x")

        self.body = tk.Frame(
            self.window,
            bg=BACKGROUND
        )
        self.body.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=16
        )

    # Start page
    def show_menu(self):
        self.screen = "menu"
        self.shell()

        content = tk.Frame(self.body, bg=BACKGROUND)
        content.place(relx=0.5, rely=0.45, anchor="center")

        art = tk.Canvas(
            content,
            width=self.px(200),
            height=self.px(78),
            bg=BACKGROUND,
            highlightthickness=0
        )
        art.pack(pady=(0, 8))

        for x, y in ((66, 18), (100, 5), (134, 18)):
            self.draw_match(
                art, self.px(x), self.px(y), self.px(48)
            )

        self.label(
            content,
            "The NIM Game",
            44,
            bold=True
        ).pack()

        self.label(
            content,
            "Take the last match and you lose.",
            15,
            LIGHT
        ).pack(pady=(0, 26))

        pages = (
            ("PLAY", self.show_setup, True),
            ("Settings", self.show_settings, False),
            ("How to Play", self.show_rules, False),
            ("Stats", self.show_stats, False),
            ("Quit", self.close, False)
        )

        first = None

        for text, command, primary in pages:
            button = self.button(
                content,
                text,
                command,
                primary=primary,
                width=22
            )
            button.widget.pack(pady=6, ipady=2)

            if first is None:
                first = button

        first.widget.focus_set()

    # Play page: choose every game setting, then start
    def show_setup(self):
        self.screen = "setup"
        self.shell("Game Setup", self.show_menu)

        content = tk.Frame(self.body, bg=BACKGROUND)
        content.place(relx=0.5, rely=0.45, anchor="center")

        self.label(
            content,
            "Difficulty",
            22,
            bold=True
        ).pack(pady=(0, 10))

        # Difficulty choices
        grid = tk.Frame(content, bg=BACKGROUND)
        grid.pack()

        self.difficulty_buttons = {}

        for index, level in enumerate(DIFFICULTIES):
            button = self.button(
                grid,
                level,
                self.choose_difficulty,
                value=level,
                width=16
            )

            button.widget.grid(
                row=index // 2,
                column=index % 2,
                padx=8,
                pady=6,
                ipady=3
            )

            self.difficulty_buttons[level] = button

        self.label(
            content,
            "Who starts?",
            22,
            bold=True
        ).pack(pady=(18, 8))

        # Starting player choices
        choices = tk.Frame(content, bg=BACKGROUND)
        choices.pack()

        self.first_buttons = {}

        for player, text in (("Player", "You"), ("AI", "AI")):
            button = self.button(
                choices,
                text,
                self.choose_first,
                value=player,
                width=10
            )

            button.widget.pack(side="left", padx=6)
            self.first_buttons[player] = button

        self.opening_note = self.label(
            content, "", 12, LIGHT
        )
        self.opening_note.pack(pady=6)

        self.label(
            content,
            "Starting matches",
            22,
            bold=True
        ).pack(pady=(10, 4))

        self.label(
            content,
            f"Minimum: {game.MIN_OBJECTS}  |  "
            f"Maximum: {game.MAX_OBJECTS}",
            12,
            LIGHT
        ).pack()

        controls = tk.Frame(content, bg=BACKGROUND)
        controls.pack(pady=10)

        self.minus_button = self.button(
            controls, "-", self.change_count,
            value=-1, width=3
        )
        self.minus_button.widget.pack(side="left", padx=8)

        self.count_number = self.label(
            controls, "", 28, GOLD, True
        )
        self.count_number.configure(width=3)
        self.count_number.pack(side="left", padx=10)

        self.plus_button = self.button(
            controls, "+", self.change_count,
            value=1, width=3
        )
        self.plus_button.widget.pack(side="left", padx=8)

        self.reset_button = self.button(
            controls,
            f"Reset to {game.INITIAL_OBJECTS}",
            self.reset_count
        )
        self.reset_button.widget.pack(side="left", padx=(18, 0))

        self.start_button = self.button(
            content,
            "Start Game",
            self.start_game,
            primary=True,
            width=29
        )
        self.start_button.widget.pack(pady=(22, 0))

        self.choose_difficulty(self.difficulty)
        self.choose_first(self.first_player)
        self.update_count()

    def choose_difficulty(self, level):
        self.difficulty = level

        for name, button in self.difficulty_buttons.items():
            button.set_selected(name == level)

    def choose_first(self, player):
        self.first_player = player

        for name, button in self.first_buttons.items():
            button.set_selected(name == player)

        text = ""

        if player == "AI":
            text = "The AI's opening move is random."

        self.opening_note.configure(text=text)

    # Show the match count and its button limits
    def update_count(self):
        self.count_number.configure(
            text=str(self.starting_objects)
        )

        self.minus_button.set_enabled(
            self.starting_objects > game.MIN_OBJECTS
        )
        self.plus_button.set_enabled(
            self.starting_objects < game.MAX_OBJECTS
        )

    def change_count(self, amount):
        new_count = self.starting_objects + amount

        if game.MIN_OBJECTS <= new_count <= game.MAX_OBJECTS:
            self.starting_objects = game.initialize_game(new_count)

        self.update_count()

    def reset_count(self):
        self.starting_objects = game.INITIAL_OBJECTS
        self.update_count()

    # Settings page
    def show_settings(self):
        self.screen = "settings"
        self.shell("Settings", self.show_menu)

        content = tk.Frame(self.body, bg=BACKGROUND)
        content.place(relx=0.5, rely=0.35, anchor="center")

        panel = tk.Frame(
            content,
            bg=PANEL,
            padx=self.px(28),
            pady=self.px(10),
            highlightthickness=1,
            highlightbackground=BORDER
        )
        panel.pack()

        options = (
            (
                "Animate AI moves",
                "Highlight the AI's matches before removing them",
                self.animations
            ),
            (
                "Sound effects",
                "Play sounds for selecting, moves, wins and losses",
                self.sound
            )
        )

        for index, (title, note, variable) in enumerate(options):
            if index > 0:
                tk.Frame(
                    panel, bg=BORDER, height=1
                ).pack(fill="x")

            ToggleSwitch(
                panel, title, note, variable, self.scale,
                on_change=lambda: self.play("click")
            ).widget.pack(fill="x", pady=self.px(12))

        self.label(
            content,
            "Difficulty, first player and match count "
            "are chosen on the PLAY page.",
            13,
            LIGHT
        ).pack(pady=(20, 0))

    # How to Play page: picture cards for each rule
    def show_rules(self):
        self.screen = "rules"
        self.shell("How to Play", self.show_menu)

        grid = tk.Frame(self.body, bg=BACKGROUND)
        grid.place(relx=0.5, rely=0.5, anchor="center")

        cards = (
            (
                "1. One pile of matches",
                "The game starts with one pile\n"
                "(15 by default, 5 to 30 on the PLAY page).",
                self.picture_pile
            ),
            (
                "2. Take 1, 2 or 3",
                "Click matches to select them,\n"
                "then press Remove matches.",
                self.picture_select
            ),
            (
                "3. Take turns",
                "You and the AI take turns.\n"
                "If the AI starts, its first move is random.",
                self.picture_turns
            ),
            (
                "4. Don't take the last one",
                "Whoever removes the last match\n"
                "LOSES the game.",
                self.picture_last
            ),
            (
                "5. Score points",
                "Best move +100, other move +20,\n"
                "speed up to +50, win +500, x difficulty.",
                self.picture_score
            ),
            (
                "6. Keyboard",
                "Tab to the board, arrows to move,\n"
                "Space select, Enter remove, Esc clear.",
                self.picture_keys
            )
        )

        for index, (title, text, draw) in enumerate(cards):
            card = tk.Frame(
                grid,
                bg=PANEL,
                padx=self.px(14),
                pady=self.px(12),
                highlightthickness=1,
                highlightbackground=BORDER
            )
            card.grid(
                row=index // 3,
                column=index % 3,
                padx=self.px(8),
                pady=self.px(8),
                sticky="nsew"
            )

            picture = tk.Canvas(
                card,
                width=self.px(250),
                height=self.px(120),
                bg=BOARD,
                highlightthickness=0
            )
            picture.pack()
            draw(picture, self.px(250), self.px(120))

            self.label(
                card, title, 15, GOLD, True
            ).pack(anchor="w", pady=(self.px(10), 2))

            caption = self.label(card, text, 12, LIGHT)
            caption.configure(justify="left")
            caption.pack(anchor="w")

    # Small pictures for the How to Play cards
    def picture_row(self, canvas, width, height, count,
                    selected=(), y=None, size=None):
        size = size or height * 0.55
        y = (height - size) / 2 if y is None else y
        gap = width / (count + 1)

        for index in range(count):
            self.draw_match(
                canvas,
                gap * (index + 1),
                y,
                size,
                selected=index in selected
            )

    def picture_pile(self, canvas, width, height):
        self.picture_row(canvas, width, height, 7)

    def picture_select(self, canvas, width, height):
        self.picture_row(
            canvas, width, height, 5, selected=(3, 4)
        )
        canvas.create_text(
            width * 0.83, height * 0.9,
            text="selected", fill=GOLD,
            font=("Helvetica", 10, "bold")
        )

    def picture_turns(self, canvas, width, height):
        def badge(x, text, fill, color):
            canvas.create_rectangle(
                x - self.px(40), height / 2 - self.px(20),
                x + self.px(40), height / 2 + self.px(20),
                fill=fill, outline=BORDER, width=2
            )
            canvas.create_text(
                x, height / 2, text=text, fill=color,
                font=("Times", 15, "bold")
            )

        badge(width * 0.25, "You", GOLD, BACKGROUND)
        badge(width * 0.75, "AI", PANEL, WHITE)

        for direction in (-1, 1):
            y = height / 2 + direction * self.px(32)
            start, end = width * 0.38, width * 0.62

            if direction > 0:
                start, end = end, start

            canvas.create_line(
                start, y, end, y,
                fill=WHITE, width=3, arrow="last",
                arrowshape=(10, 12, 5)
            )

    def picture_last(self, canvas, width, height):
        size = height * 0.6
        self.draw_match(canvas, width / 2, height * 0.18, size)

        # Red cross over the last match
        cross = self.px(26)
        center_y = height * 0.18 + size / 2

        for dx in (-1, 1):
            canvas.create_line(
                width / 2 - cross, center_y - cross * dx,
                width / 2 + cross, center_y + cross * dx,
                fill="#FF4F5E", width=6, capstyle="round"
            )

        canvas.create_text(
            width / 2, height * 0.9,
            text="LOSE", fill="#FF8A93",
            font=("Helvetica", 12, "bold")
        )

    def picture_score(self, canvas, width, height):
        canvas.create_text(
            width / 2, height * 0.32,
            text="1,950", fill=GOLD,
            font=("Times", 30, "bold")
        )
        canvas.create_text(
            width / 2, height * 0.68,
            text="* best move   +100",
            fill=WHITE,
            font=("Courier", 12, "bold")
        )
        canvas.create_text(
            width / 2, height * 0.86,
            text="fast choice  +50",
            fill=LIGHT,
            font=("Courier", 11)
        )

    def picture_keys(self, canvas, width, height):
        keys = (
            ("Tab", 0.17, 0.3), ("←", 0.42, 0.3),
            ("→", 0.58, 0.3), ("Esc", 0.83, 0.3),
            ("Space", 0.3, 0.7), ("Enter", 0.7, 0.7)
        )

        for text, fx, fy in keys:
            x, y = width * fx, height * fy
            half = self.px(30 if len(text) > 2 else 18)

            canvas.create_rectangle(
                x - half, y - self.px(17),
                x + half, y + self.px(17),
                fill=BACKGROUND, outline=BORDER, width=2
            )
            canvas.create_text(
                x, y, text=text, fill=WHITE,
                font=("Helvetica", 11, "bold")
            )

    # Stats page: wins, losses and high scores for every difficulty
    def show_stats(self):
        self.screen = "stats"
        self.shell("Stats", self.show_menu)

        content = tk.Frame(self.body, bg=BACKGROUND)
        content.place(relx=0.5, rely=0.4, anchor="center")

        table = tk.Frame(content, bg=PANEL, padx=26, pady=18)
        table.pack()

        headings = (
            "Difficulty", "Wins", "Losses", "Win rate", "High score"
        )

        for column, text in enumerate(headings):
            self.label(
                table, text, 16, GOLD, True
            ).grid(row=0, column=column, padx=16, pady=(0, 8))

        rows = [
            (level, record["wins"], record["losses"], record["best"])
            for level, record in self.scoreboard.scores.items()
        ]
        rows.append(
            ("Total",)
            + self.scoreboard.totals()
            + (self.scoreboard.best_overall(),)
        )

        for row, (name, wins, losses, best) in enumerate(
            rows, start=1
        ):
            played = wins + losses
            rate = f"{100 * wins / played:.0f}%" if played else "-"
            bold = name == "Total"

            for column, value in enumerate(
                (name, wins, losses, rate, f"{best:,}")
            ):
                self.label(
                    table,
                    str(value),
                    15,
                    WHITE if not bold else GOLD,
                    bold
                ).grid(row=row, column=column, padx=16, pady=3)

        self.button(
            content,
            "Reset scores",
            self.reset_scores
        ).widget.pack(pady=(20, 0))

    def reset_scores(self):
        def reset():
            self.scoreboard.reset()
            self.show_stats()

        self.confirm(
            "Reset scores",
            "Clear the win/loss record for every difficulty?",
            reset
        )

    # Create the game screen
    def start_game(self):
        self.session = GameSession(
            self.difficulty,
            self.first_player,
            self.starting_objects
        )

        self.selected.clear()
        self.ai_highlight.clear()
        self.focus_match = None
        self.hovered_match = None

        # Scoring for this game
        self.score = scoring.ScoreKeeper(self.difficulty)
        self.move_notes = {}
        self.turn_started = time.monotonic()

        self.screen = "game"
        self.shell()

        # Packed first on the right so the board fills the rest
        self.build_side_panel()

        starter = "You started"

        if self.first_player == "AI":
            starter = "AI started"

        self.label(
            self.body,
            f"({self.difficulty})  |  {starter}",
            13,
            GOLD
        ).pack(anchor="w")

        # Turn indicators
        turn = tk.Frame(self.body, bg=BACKGROUND)
        turn.pack(pady=(6, 4))

        self.you_badge = self.label(
            turn, "  You  ", 16, bold=True
        )
        self.you_badge.pack(
            side="left",
            padx=3,
            ipadx=18,
            ipady=7
        )

        self.ai_badge = self.label(
            turn, "  AI  ", 16, bold=True
        )
        self.ai_badge.pack(
            side="left",
            padx=3,
            ipadx=18,
            ipady=7
        )

        self.turn_label = self.label(
            self.body, "", 13, GOLD, True
        )
        self.turn_label.pack(pady=4)

        self.count_label = self.label(
            self.body, "", 29, bold=True
        )
        self.count_label.pack(pady=(0, 12))

        # Matchstick board
        self.board = tk.Canvas(
            self.body,
            bg=BOARD,
            height=300,
            takefocus=True,
            highlightthickness=2,
            highlightbackground=BORDER,
            highlightcolor=GOLD
        )
        self.board.pack(
            fill="both",
            expand=True,
            padx=35
        )

        self.board.bind("<Configure>", self.draw_board)
        self.board.bind("<Button-1>", self.click_board)
        self.board.bind("<Motion>", self.hover_board)
        self.board.bind("<Leave>", self.leave_board)
        self.board.bind("<FocusIn>", self.board_focus)
        self.board.bind("<FocusOut>", self.draw_board)
        self.board.bind("<space>", self.select_focused)

        for key in ("Left", "Right", "Up", "Down"):
            self.board.bind(
                "<" + key + ">",
                self.navigate_board
            )

        self.selection_label = self.label(self.body, "")
        self.selection_label.pack(pady=(12, 7))

        # Move controls
        actions = tk.Frame(self.body, bg=BACKGROUND)
        actions.pack()

        self.remove_button = self.button(
            actions,
            "Remove matches",
            self.remove_selected,
            primary=True,
            width=24
        )
        self.remove_button.widget.pack(
            side="left",
            padx=8
        )

        self.clear_button = self.button(
            actions,
            "Clear selection",
            self.clear_selection
        )
        self.clear_button.widget.pack(
            side="left",
            padx=8
        )

        self.feedback = self.label(
            self.body, "", 12, LIGHT
        )
        self.feedback.pack(pady=9)

        bottom = tk.Frame(self.body, bg=BACKGROUND)
        bottom.pack(fill="x", pady=(3, 0))

        self.button(
            bottom,
            "Leave Game",
            self.back_to_menu
        ).widget.pack(side="left")

        self.button(
            bottom,
            "Restart Game",
            self.restart
        ).widget.pack(side="right")

        self.refresh()

        if self.session.current_player == "AI":
            self.pending = self.window.after(
                650,
                self.ai_turn
            )

    # Side panel with this difficulty's record and the move history
    def build_side_panel(self):
        side = tk.Frame(
            self.body,
            bg=PANEL,
            padx=16,
            pady=12,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        side.pack(side="right", fill="y", padx=(16, 0))

        self.label(
            side, "Score", 16, bold=True
        ).pack(anchor="w")

        self.score_label = self.label(side, "0", 26, GOLD, True)
        self.score_label.pack(anchor="w")

        self.label(
            side,
            f"x{self.score.multiplier:g} for {self.session.difficulty}",
            12,
            LIGHT
        ).pack(anchor="w")

        tk.Frame(
            side, bg=BORDER, height=1
        ).pack(fill="x", pady=12)

        self.label(
            side, f"Record vs {self.session.difficulty}", 16, bold=True
        ).pack(anchor="w")

        self.record_label = self.label(side, "", 14, GOLD, True)
        self.record_label.pack(anchor="w", pady=(2, 0))

        tk.Frame(
            side, bg=BORDER, height=1
        ).pack(fill="x", pady=12)

        self.label(
            side, "Move history", 16, bold=True
        ).pack(anchor="w")

        history = tk.Frame(side, bg=PANEL)
        history.pack(fill="both", expand=True, pady=(6, 0))

        scrollbar = tk.Scrollbar(history)
        scrollbar.pack(side="right", fill="y")

        self.history_list = tk.Listbox(
            history,
            width=26,
            bg=BACKGROUND,
            fg=WHITE,
            font=("Courier", 12),
            borderwidth=0,
            highlightthickness=0,
            activestyle="none",
            selectbackground=BACKGROUND,
            selectforeground=WHITE,
            takefocus=False,
            yscrollcommand=scrollbar.set
        )
        self.history_list.pack(side="left", fill="both", expand=True)
        scrollbar.configure(command=self.history_list.yview)

        self.update_record()

    def update_record(self):
        record = self.scoreboard.scores[self.session.difficulty]
        self.record_label.configure(
            text=f"Wins {record['wins']}   Losses {record['losses']}"
        )

    def update_score(self):
        self.score_label.configure(
            text=f"{self.score.total():,}"
        )

    def update_history(self):
        self.update_score()
        self.history_list.delete(0, "end")

        for number, player, removed, left in self.session.history:
            who = "You" if player == "Player" else "AI"
            note = ""

            if number in self.move_notes:
                points, on_path = self.move_notes[number]
                star = "*" if on_path else " "
                note = f" {star}+{points}"

            self.history_list.insert(
                "end",
                f"{number:>2}. {who:<3} -{removed} ({left:>2}){note}"
            )

            if player == "AI":
                self.history_list.itemconfigure(
                    "end", fg=GOLD
                )

        self.history_list.see("end")

    # Draw a match and its glow
    def draw_match(
        self,
        canvas,
        x,
        y,
        height,
        selected=False,
        hovered=False,
        focused=False
    ):
        width = max(7, height * 0.12)

        # Shadow
        canvas.create_line(
            x + 4, y + 14,
            x + 4, y + height + 3,
            fill="#103B29",
            width=width + 5,
            capstyle="round"
        )

        # Hover or selection glow
        if selected or hovered:
            colors = (
                "#3C8961",
                "#72C393",
                "#BEFFCE"
            )

            if selected:
                colors = (
                    "#99782B",
                    "#E8B938",
                    "#FFE873"
                )

            for color, spread in zip(colors, (12, 7, 3)):
                canvas.create_line(
                    x, y + 5,
                    x, y + height - 3,
                    fill=color,
                    width=width + spread * 2,
                    capstyle="round"
                )

                canvas.create_oval(
                    x - width * 0.8 - spread,
                    y - 3 - spread,
                    x + width * 0.8 + spread,
                    y + width * 1.8 + spread,
                    fill=color,
                    outline=""
                )

        # Wooden stem
        wood = "#F3C776"

        if selected:
            wood = "#FFE09A"

        canvas.create_rectangle(
            x - width / 2, y + 10,
            x + width / 2, y + height,
            fill=wood,
            outline="#BA8D43"
        )

        canvas.create_line(
            x - width / 4, y + 14,
            x - width / 4, y + height - 3,
            fill="#FFF2C4",
            width=max(2, width / 3)
        )

        # Red head
        canvas.create_oval(
            x - width * 0.8, y - 3,
            x + width * 0.8, y + width * 1.8,
            fill="#EE3547",
            outline="#AD2032",
            width=2
        )

        canvas.create_oval(
            x - width * 0.4, y,
            x + width * 0.15, y + width * 0.6,
            fill="#FF9299",
            outline=""
        )

        if focused:
            canvas.create_rectangle(
                x - width - 17, y - 19,
                x + width + 17, y + height + 15,
                outline=WHITE,
                dash=(4, 4),
                width=2
            )

    # Keep the matches in their original positions
    def draw_board(self, event=None):
        if self.screen != "game":
            return

        self.board.delete("all")

        width = self.board.winfo_width()
        height = self.board.winfo_height()

        self.columns = 5

        if self.session.starting_objects > 15:
            self.columns = 6

        rows = math.ceil(
            self.session.starting_objects / self.columns
        )
        row_height = height / rows
        match_height = min(self.px(100), row_height * 0.58)

        self.hitboxes = {}

        for match in self.session.matches:
            row = match // self.columns
            column = match % self.columns

            x = width * (column + 1) / (self.columns + 1)
            y = (
                row_height * row
                + (row_height - match_height) / 2
            )

            selected = (
                match in self.selected
                or match in self.ai_highlight
            )

            if selected:
                y -= 4

            hovered = (
                self.human_turn()
                and match == self.hovered_match
            )

            focused = (
                self.window.focus_get() == self.board
                and match == self.focus_match
            )

            self.draw_match(
                self.board,
                x,
                y,
                match_height,
                selected,
                hovered,
                focused
            )

            self.hitboxes[match] = (
                x - self.px(25), y - self.px(12),
                x + self.px(25), y + match_height + self.px(12)
            )

    def human_turn(self):
        return (
            self.screen == "game"
            and self.dialog is None
            and not self.session.winner
            and self.session.current_player == "Player"
        )

    def hit_match(self, x, y):
        for match, bounds in self.hitboxes.items():
            left, top, right, bottom = bounds

            if left <= x <= right and top <= y <= bottom:
                return match

        return None

    def click_board(self, event):
        if self.human_turn():
            match = self.hit_match(event.x, event.y)

            if match is not None:
                self.focus_match = match
                self.board.focus_set()
                self.toggle_match(match)

    def hover_board(self, event):
        match = None

        if self.human_turn():
            match = self.hit_match(event.x, event.y)

        if match != self.hovered_match:
            self.hovered_match = match
            self.draw_board()

        cursor = ""

        if match is not None:
            cursor = "hand2"

        self.board.configure(cursor=cursor)

    def leave_board(self, event):
        self.hovered_match = None
        self.board.configure(cursor="")
        self.draw_board()

    # Keyboard controls for the board
    def board_focus(self, event):
        if (
            self.focus_match not in self.session.matches
            and self.session.matches
        ):
            self.focus_match = self.session.matches[0]

        self.draw_board()

    def navigate_board(self, event):
        matches = self.session.matches

        if matches:
            index = 0

            if self.focus_match in matches:
                index = matches.index(self.focus_match)

            steps = {
                "Left": -1,
                "Right": 1,
                "Up": -self.columns,
                "Down": self.columns
            }

            self.focus_match = matches[
                (index + steps[event.keysym]) % len(matches)
            ]
            self.draw_board()

        return "break"

    def select_focused(self, event):
        if (
            self.human_turn()
            and self.focus_match in self.session.matches
        ):
            self.toggle_match(self.focus_match)

        return "break"

    # Select up to three matches
    def toggle_match(self, match):
        if (
            not self.human_turn()
            or match not in self.session.matches
        ):
            return

        if match in self.selected:
            self.selected.remove(match)
            self.play("deselect")

        elif len(self.selected) < 3:
            self.selected.add(match)
            self.play("select")

        else:
            self.feedback.configure(
                text="Three matches selected. "
                     "Deselect one to choose another."
            )
            return

        self.feedback.configure(text="")
        self.refresh()

    def clear_selection(self, event=None):
        if self.human_turn():
            self.selected.clear()
            self.feedback.configure(text="")
            self.refresh()

    # Format the match count
    def match_text(self, count):
        if count == 1:
            return "1 match"

        return f"{count} matches"

    # Show the latest count and turn
    def refresh(self):
        player = self.human_turn()

        self.you_badge.configure(bg=PANEL, fg=LIGHT)
        self.ai_badge.configure(bg=PANEL, fg=LIGHT)

        turn = "AI'S TURN"
        selection = "AI is choosing..."

        if player:
            self.you_badge.configure(
                bg=GOLD,
                fg=BACKGROUND
            )
            turn = "YOUR TURN"
            selection = f"{len(self.selected)} of 3 selected"

        else:
            self.ai_badge.configure(
                bg=GOLD,
                fg=BACKGROUND
            )

        self.turn_label.configure(text=turn)

        self.count_label.configure(
            text=self.match_text(self.session.remaining)
            + " remaining"
        )

        self.selection_label.configure(text=selection)
        self.update_history()

        text = "Remove matches"

        if self.selected:
            text = "Remove " + self.match_text(
                len(self.selected)
            )

        self.remove_button.set_text(text)

        enabled = player and len(self.selected) > 0

        self.remove_button.set_enabled(enabled)
        self.clear_button.set_enabled(enabled)
        self.draw_board()

    # Complete the player move
    def remove_selected(self):
        if not self.human_turn() or not self.selected:
            return

        count = len(self.selected)
        remaining_before = self.session.remaining
        seconds = time.monotonic() - self.turn_started

        self.session.remove(
            sorted(self.selected),
            "Player"
        )

        # Score the move: best-path bonus and speed bonus
        points, on_path = self.score.add_move(
            remaining_before, count, seconds
        )
        self.move_notes[self.session.moves_played] = (
            points, on_path
        )

        self.selected.clear()
        self.hovered_match = None
        self.play("remove")

        text = (
            f"You removed {self.match_text(count)} "
            f"in {seconds:.1f}s.  +{points} points"
        )

        if on_path:
            text += "  (best move!)"

        self.feedback.configure(text=text)

        self.refresh()

        if self.session.winner:
            self.show_result()

        else:
            delay = 50

            if self.animations.get():
                delay = 650

            self.pending = self.window.after(
                delay,
                self.ai_turn
            )

    # Ask the existing AI for its move
    def ai_turn(self):
        self.pending = None

        if self.screen != "game" or self.session.winner:
            return

        count = self.session.choose_ai_move()

        self.ai_choices = self.session.matches[-count:]
        self.ai_highlight = set(self.ai_choices)

        self.draw_board()

        delay = 1

        if self.animations.get():
            delay = 550

        self.pending = self.window.after(
            delay,
            self.finish_ai_move
        )

    # Remove the highlighted AI matches
    def finish_ai_move(self):
        self.pending = None
        count = len(self.ai_choices)

        self.session.remove(self.ai_choices, "AI")
        self.ai_highlight.clear()

        self.feedback.configure(
            text="AI removed " + self.match_text(count) + "."
        )

        self.play("ai_move")
        self.turn_started = time.monotonic()
        self.refresh()

        if self.session.winner:
            self.show_result()

    # Show the winner and replay buttons
    def show_result(self):
        self.cancel_pending()
        self.screen = "result"

        player_won = self.session.winner == "Player"
        self.score.finish(player_won)
        total = self.score.total()

        new_best = self.scoreboard.record(
            self.session.difficulty,
            self.session.winner,
            total
        )
        self.update_record()
        self.update_score()
        self.play("win" if player_won else "lose")

        self.turn_label.configure(text="GAME OVER")
        self.selection_label.configure(text="")

        self.remove_button.set_enabled(False)
        self.clear_button.set_enabled(False)

        title = "AI WINS"
        reason = "You took the last match."

        if self.session.winner == "Player":
            title = "YOU WIN!"
            reason = "The AI took the last match."

        card = self.card(self.board)

        self.label(
            card, title, 32, bold=True
        ).pack(pady=10)

        self.label(
            card, reason, 15
        ).pack(pady=(0, 10))

        self.label(
            card, f"Score: {total:,}", 24, GOLD, True
        ).pack()

        details = (
            f"Best moves: {self.score.best_count} of "
            f"{self.score.player_moves}   |   "
            f"x{self.score.multiplier:g} {self.session.difficulty}"
        )

        if new_best:
            details += "\nNew high score!"

        self.label(
            card, details, 13, LIGHT
        ).pack(pady=(2, 16))

        self.button(
            card,
            "Play Again",
            self.start_game,
            primary=True,
            width=22
        ).widget.pack(pady=5)

        self.button(
            card,
            "Change Setup",
            self.show_setup,
            width=22
        ).widget.pack(pady=5)

        self.button(
            card,
            "Main Menu",
            self.show_menu,
            width=22
        ).widget.pack(pady=5)

    # A bordered box drawn on top of the page
    def card(self, over):
        card = tk.Frame(
            self.body if over is None else over.master,
            bg=BACKGROUND,
            highlightbackground=GOLD,
            highlightthickness=2,
            padx=40,
            pady=22
        )
        card.place(
            in_=over if over is not None else self.body,
            relx=0.5,
            rely=0.5,
            anchor="center"
        )
        card.lift()
        return card

    # Yes/No question shown inside the game window
    def confirm(self, title, question, on_yes):
        if self.dialog is not None:
            return

        # Pause the AI and the move timer while the question is open
        was_waiting = self.pending is not None
        self.cancel_pending()
        opened = time.monotonic()

        over = self.board if self.screen == "game" else None
        self.dialog = self.card(over)

        self.label(
            self.dialog, title, 26, bold=True
        ).pack(pady=(4, 8))

        self.label(
            self.dialog, question, 15
        ).pack(pady=(0, 18))

        choices = tk.Frame(self.dialog, bg=BACKGROUND)
        choices.pack()

        def yes():
            self.close_dialog()
            on_yes()

        def no():
            self.close_dialog()

            if self.turn_started is not None:
                self.turn_started += time.monotonic() - opened

            if was_waiting and self.screen == "game":
                self.pending = self.window.after(
                    300, self.ai_turn
                )

        self.dialog_no = no

        no_button = self.button(choices, "No", no, width=10)
        no_button.widget.pack(side="left", padx=8)

        self.button(
            choices, "Yes", yes, primary=True, width=10
        ).widget.pack(side="left", padx=8)

        no_button.widget.focus_set()

        if self.screen == "game":
            self.refresh()

    def close_dialog(self):
        if self.dialog is not None:
            self.buttons = [
                button
                for button in self.buttons
                if button.widget.winfo_exists()
                and not str(button.widget).startswith(
                    str(self.dialog)
                )
            ]
            self.dialog.destroy()
            self.dialog = None

            if self.screen == "game":
                self.refresh()

    def restart(self):
        if self.screen == "game":
            self.confirm(
                "Restart Game",
                "Restart this game?",
                self.start_game
            )
        else:
            self.start_game()

    def back_to_menu(self):
        if self.screen == "game":
            self.confirm(
                "Leave Game",
                "Leave this game and go to the main menu?",
                self.show_menu
            )
        else:
            self.show_menu()

    def close(self):
        def quit_game():
            self.cancel_pending()
            self.window.destroy()

        if self.screen == "game":
            self.confirm(
                "Quit",
                "Quit in the middle of this game?",
                quit_game
            )
        else:
            quit_game()

    def enter_key(self, event):
        focused = self.window.focus_get()

        for button in self.buttons:
            if focused == button.widget:
                button.activate()
                return "break"

        if self.dialog is not None:
            return "break"

        if self.screen == "setup":
            self.start_game()

        elif self.human_turn():
            self.remove_selected()

        return "break"

    def escape_key(self, event):
        if self.dialog is not None:
            self.dialog_no()

        elif self.screen == "game":
            self.clear_selection()

        elif self.screen in ("setup", "settings", "rules", "stats"):
            self.show_menu()

        return "break"
