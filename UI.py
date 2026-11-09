# This file contains the graphical interface
import tkinter as tk
from tkinter import messagebox

from session import DIFFICULTIES, GameSession


# Interface colors
BACKGROUND = "#071f1b"
PANEL = "#10392e"
BOARD = "#12533c"
GOLD = "#edc466"
CREAM = "#fff0cd"
MUTED = "#aac1af"
BORDER = "#365d4c"

# Interface fonts
TITLE_FONT = "Palatino"
BUTTON_FONT = "Helvetica"


class NimApp(tk.Tk):

    # Initialize the application
    def __init__(self):
        super().__init__()

        self.title("Nim - Matchstick Game")
        self.geometry("1040x850")
        self.minsize(800, 720)
        self.configure(bg=BACKGROUND)

        self.difficulty = "Medium"
        self.first_player = "Player"

        self.session = None
        self.screen = "setup"

        self.selected = set()
        self.ai_highlight = set()
        self.focus_match = None

        self.pending = None
        self.hitboxes = {}

        self.animations = tk.BooleanVar(value=True)
        self.sound = tk.BooleanVar(value=False)

        self.protocol("WM_DELETE_WINDOW", self.close)

        self.bind("<Return>", self.enter_key)
        self.bind("<Escape>", lambda event: self.clear_selection())

        self.show_setup()

    # Create a text label
    def label(
        self,
        parent,
        text,
        size=14,
        color=CREAM,
        bold=False,
        **kwargs
    ):
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color,
            font=(
                TITLE_FONT,
                size,
                "bold" if bold else "normal"
            ),
            **kwargs
        )

    # Create a button
    def button(
        self,
        parent,
        text,
        command,
        primary=False,
        **kwargs
    ):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=(
                BUTTON_FONT,
                12,
                "bold" if primary else "normal"
            ),
            bg=GOLD if primary else PANEL,
            fg=BACKGROUND if primary else CREAM,
            activebackground="#f7d78e" if primary else BORDER,
            activeforeground=BACKGROUND if primary else CREAM,
            disabledforeground="#718779",
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightbackground=BORDER,
            highlightcolor=GOLD,
            padx=20,
            pady=11,
            cursor="hand2",
            **kwargs
        )

    # Cancel an unfinished AI action
    def cancel_pending(self):
        if self.pending is not None:
            self.after_cancel(self.pending)
            self.pending = None

    # Schedule an action without freezing the window
    def later(self, delay, callback):
        self.cancel_pending()

        def run():
            self.pending = None
            callback()

        self.pending = self.after(delay, run)

    # Create the shared page layout
    def shell(self):
        self.cancel_pending()

        for child in self.winfo_children():
            child.destroy()

        header = tk.Frame(
            self,
            bg=BACKGROUND,
            padx=28,
            pady=14
        )
        header.pack(fill="x")

        self.label(
            header,
            "NIM",
            size=34,
            bold=True
        ).pack(side="left")

        self.button(
            header,
            "Settings",
            self.show_settings
        ).pack(side="right", padx=(10, 0))

        self.button(
            header,
            "Rules",
            self.show_rules
        ).pack(side="right")

        tk.Frame(
            self,
            bg=BORDER,
            height=1
        ).pack(fill="x")

        self.body = tk.Frame(self, bg=BACKGROUND)
        self.body.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=16
        )

    # Show the setup screen
    def show_setup(self):
        self.screen = "setup"
        self.shell()

        content = tk.Frame(self.body, bg=BACKGROUND)
        content.pack(expand=True)

        # Draw decorative matches
        art = tk.Canvas(
            content,
            width=200,
            height=78,
            bg=BACKGROUND,
            highlightthickness=0
        )
        art.pack(pady=(0, 8))

        for x, y in ((66, 18), (100, 5), (134, 18)):
            self.draw_match(art, x, y, 48)

        self.label(
            content,
            "Choose your difficulty",
            size=25,
            bold=True
        ).pack(pady=(0, 14))

        # Difficulty buttons
        difficulty_frame = tk.Frame(content, bg=BACKGROUND)
        difficulty_frame.pack(fill="x")

        self.difficulty_buttons = {}

        for index, level in enumerate(DIFFICULTIES):
            button = self.button(
                difficulty_frame,
                level,
                lambda value=level: self.set_difficulty(value),
                width=16
            )

            button.grid(
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
            size=21,
            bold=True
        ).pack(pady=(14, 8))

        # Starting player buttons
        first_frame = tk.Frame(content, bg=BACKGROUND)
        first_frame.pack()

        self.first_buttons = {}

        for player, text in (("Player", "You"), ("AI", "AI")):
            button = self.button(
                first_frame,
                text,
                lambda value=player: self.set_first(value),
                width=10
            )

            button.pack(side="left", padx=6)
            self.first_buttons[player] = button

        self.opening_note = self.label(
            content,
            "",
            size=12,
            color=MUTED
        )
        self.opening_note.pack(pady=9)

        self.button(
            content,
            "Start Game",
            self.start_game,
            primary=True,
            width=29
        ).pack(pady=8)

        self.button(
            content,
            "How to Play",
            self.show_rules
        ).pack(pady=6)

        self.set_difficulty(self.difficulty)
        self.set_first(self.first_player)

    # Update the selected difficulty
    def set_difficulty(self, value):
        self.difficulty = value

        for level, button in self.difficulty_buttons.items():
            selected = level == value

            button.configure(
                bg=GOLD if selected else PANEL,
                fg=BACKGROUND if selected else CREAM,
                text=level
            )

    # Update the starting player
    def set_first(self, value):
        self.first_player = value

        for player, button in self.first_buttons.items():
            selected = player == value

            button.configure(
                bg=GOLD if selected else PANEL,
                fg=BACKGROUND if selected else CREAM
            )

        if value == "AI":
            self.opening_note.configure(
                text="The AI's opening move is random."
            )
        else:
            self.opening_note.configure(text="")

    # Start a new game
    def start_game(self):
        self.session = GameSession(
            self.difficulty,
            self.first_player
        )

        self.selected.clear()
        self.ai_highlight.clear()
        self.focus_match = None

        self.screen = "game"
        self.shell()

        # Show the selected settings
        badges = tk.Frame(self.body, bg=BACKGROUND)
        badges.pack(fill="x")

        self.label(
            badges,
            self.difficulty,
            size=13,
            color=GOLD
        ).pack(side="left")

        starting_text = (
            "  |  You started"
            if self.first_player == "Player"
            else "  |  AI started"
        )

        self.label(
            badges,
            starting_text,
            size=13,
            color=MUTED
        ).pack(side="left")

        # Show whose turn it is
        turn_frame = tk.Frame(self.body, bg=BACKGROUND)
        turn_frame.pack(pady=(6, 4))

        self.you_badge = self.label(
            turn_frame,
            "  You  ",
            size=16,
            bold=True,
            padx=18,
            pady=7
        )
        self.you_badge.pack(side="left", padx=3)

        self.ai_badge = self.label(
            turn_frame,
            "  AI  ",
            size=16,
            bold=True,
            padx=18,
            pady=7
        )
        self.ai_badge.pack(side="left", padx=3)

        self.turn_label = self.label(
            self.body,
            "",
            size=13,
            color=GOLD,
            bold=True
        )
        self.turn_label.pack(pady=4)

        self.count_label = self.label(
            self.body,
            "",
            size=29,
            bold=True
        )
        self.count_label.pack(pady=(0, 12))

        # Create the matchstick board
        self.board = tk.Canvas(
            self.body,
            bg=BOARD,
            highlightthickness=2,
            highlightbackground=BORDER,
            highlightcolor=GOLD,
            height=300,
            takefocus=True
        )

        self.board.pack(
            fill="both",
            expand=True,
            padx=62
        )

        # Mouse controls
        self.board.bind(
            "<Configure>",
            lambda event: self.draw_board()
        )
        self.board.bind("<Button-1>", self.click_board)
        self.board.bind("<Motion>", self.hover_board)
        self.board.bind(
            "<Leave>",
            lambda event: self.board.configure(cursor="")
        )

        # Keyboard controls
        for key in ("Left", "Right", "Up", "Down"):
            self.board.bind(
                "<" + key + ">",
                self.navigate_board
            )

        self.board.bind("<space>", self.select_focused)
        self.board.bind("<FocusIn>", self.board_focus)
        self.board.bind(
            "<FocusOut>",
            lambda event: self.draw_board()
        )

        self.selection_label = self.label(
            self.body,
            "",
            size=14
        )
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
        self.remove_button.pack(side="left", padx=8)

        self.clear_button = self.button(
            actions,
            "Clear selection",
            self.clear_selection
        )
        self.clear_button.pack(side="left", padx=8)

        self.feedback = self.label(
            self.body,
            "",
            size=12,
            color=MUTED
        )
        self.feedback.pack(pady=9)

        # Navigation controls
        bottom = tk.Frame(self.body, bg=BACKGROUND)
        bottom.pack(fill="x", pady=(3, 0))

        self.button(
            bottom,
            "Back to setup",
            self.back_to_setup
        ).pack(side="left")

        self.button(
            bottom,
            "Restart",
            self.restart
        ).pack(side="right")

        self.refresh()

        if self.session.current_player == "AI":
            self.later(650, self.ai_turn)

    # Draw one matchstick
    @staticmethod
    def draw_match(
        canvas,
        x,
        y,
        height,
        selected=False,
        focused=False
    ):
        width = max(8, height * 0.12)

        # Show keyboard focus
        if focused:
            canvas.create_rectangle(
                x - width - 8,
                y - 8,
                x + width + 8,
                y + height + 8,
                outline=CREAM,
                dash=(3, 3)
            )

        # Draw the shadow
        canvas.create_line(
            x + 3,
            y + 14,
            x + 3,
            y + height,
            fill="#063326",
            width=width + 4,
            capstyle="round"
        )

        # Highlight selected matches
        if selected:
            canvas.create_line(
                x,
                y + 8,
                x,
                y + height - 3,
                fill=GOLD,
                width=width + 10,
                capstyle="round"
            )

            canvas.create_oval(
                x - width * 0.8 - 4,
                y - 7,
                x + width * 0.8 + 4,
                y + width * 1.8 + 4,
                fill=GOLD,
                outline=GOLD
            )

        # Draw the wooden stem
        canvas.create_rectangle(
            x - width / 2,
            y + 10,
            x + width / 2,
            y + height,
            fill="#e6b866",
            outline="#b58747"
        )

        canvas.create_line(
            x - width / 4,
            y + 14,
            x - width / 4,
            y + height - 3,
            fill="#ffe3a2",
            width=max(2, width / 3)
        )

        # Draw the red match head
        canvas.create_oval(
            x - width * 0.8,
            y - 3,
            x + width * 0.8,
            y + width * 1.8,
            fill="#d52c38",
            outline="#a41d2d",
            width=2
        )

        canvas.create_oval(
            x - width * 0.4,
            y,
            x + width * 0.15,
            y + width * 0.6,
            fill="#fa6970",
            outline=""
        )

    # Draw all remaining matches
    def draw_board(self):
        if self.screen != "game":
            return

        self.board.delete("all")

        width = self.board.winfo_width()
        height = self.board.winfo_height()

        self.hitboxes = {}

        row_height = height / 3
        match_height = min(100, row_height * 0.67)

        for match in self.session.matches:
            row, column = divmod(match, 5)

            x = width * (column + 1) / 6
            y = (
                row_height * row
                + (row_height - match_height) / 2
            )

            selected = (
                match in self.selected
                or match in self.ai_highlight
            )

            if selected:
                y -= 5

            focused = (
                self.focus_get() == self.board
                and match == self.focus_match
            )

            self.draw_match(
                self.board,
                x,
                y,
                match_height,
                selected,
                focused
            )

            # Make matches easier to click
            self.hitboxes[match] = (
                x - 24,
                y - 10,
                x + 24,
                y + match_height + 10
            )

    # Find the match under the mouse
    def hit_match(self, x, y):
        for match, bounds in self.hitboxes.items():
            left, top, right, bottom = bounds

            if left <= x <= right and top <= y <= bottom:
                return match

        return None

    # Check whether the player can make a move
    def human_turn(self):
        return (
            self.screen == "game"
            and not self.session.winner
            and self.session.current_player == "Player"
        )

    # Handle a match being clicked
    def click_board(self, event):
        if not self.human_turn():
            return

        match = self.hit_match(event.x, event.y)

        if match is not None:
            self.focus_match = match
            self.board.focus_set()
            self.toggle_match(match)

    # Change the cursor over available matches
    def hover_board(self, event):
        match = self.hit_match(event.x, event.y)

        if self.human_turn() and match is not None:
            self.board.configure(cursor="hand2")
        else:
            self.board.configure(cursor="")

    # Set the first keyboard selection
    def board_focus(self, event):
        if self.focus_match not in self.session.matches:
            self.focus_match = next(
                iter(self.session.matches),
                None
            )

        self.draw_board()

    # Move between matches with the arrow keys
    def navigate_board(self, event):
        matches = self.session.matches

        if not matches:
            return "break"

        if self.focus_match in matches:
            index = matches.index(self.focus_match)
        else:
            index = 0

        steps = {
            "Left": -1,
            "Right": 1,
            "Up": -5,
            "Down": 5
        }

        index = (index + steps[event.keysym]) % len(matches)
        self.focus_match = matches[index]

        self.draw_board()
        return "break"

    # Select the focused match with Space
    def select_focused(self, event):
        if (
            self.human_turn()
            and self.focus_match in self.session.matches
        ):
            self.toggle_match(self.focus_match)

        return "break"

    # Select or deselect a match
    def toggle_match(self, match):
        if match in self.selected:
            self.selected.remove(match)

        elif len(self.selected) < 3:
            self.selected.add(match)

        else:
            self.feedback.configure(
                text="Three matches selected. "
                     "Deselect one to choose another."
            )
            return

        self.feedback.configure(text="")

        if self.sound.get():
            self.bell()

        self.refresh()

    # Clear the selected matches
    def clear_selection(self):
        if self.human_turn():
            self.selected.clear()
            self.feedback.configure(text="")
            self.refresh()

    # Update the game screen
    def refresh(self):
        player_turn = self.human_turn()

        self.you_badge.configure(
            bg=GOLD if player_turn else PANEL,
            fg=BACKGROUND if player_turn else MUTED
        )

        self.ai_badge.configure(
            bg=PANEL if player_turn else GOLD,
            fg=MUTED if player_turn else BACKGROUND
        )

        self.turn_label.configure(
            text="YOUR TURN" if player_turn else "AI'S TURN"
        )

        count = self.session.remaining
        match_word = "match" if count == 1 else "matches"

        self.count_label.configure(
            text=f"{count} {match_word} remaining"
        )

        if player_turn:
            selection_text = f"{len(self.selected)} of 3 selected"
        else:
            selection_text = "AI is choosing..."

        self.selection_label.configure(text=selection_text)

        selected_count = len(self.selected)

        if selected_count:
            word = "match" if selected_count == 1 else "matches"
            button_text = f"Remove {selected_count} {word}"
        else:
            button_text = "Remove matches"

        can_remove = player_turn and selected_count > 0

        self.remove_button.configure(
            text=button_text,
            state="normal" if can_remove else "disabled"
        )

        self.clear_button.configure(
            state="normal" if can_remove else "disabled"
        )

        self.draw_board()

    # Confirm the player's move
    def remove_selected(self):
        if not self.human_turn() or not self.selected:
            return

        count = len(self.selected)

        self.session.remove(
            sorted(self.selected),
            "Player"
        )

        self.selected.clear()

        word = "match" if count == 1 else "matches"

        self.feedback.configure(
            text=f"You removed {count} {word}."
        )

        self.refresh()

        if self.session.winner:
            self.show_result()
        else:
            delay = 650 if self.animations.get() else 50
            self.later(delay, self.ai_turn)

    # Handle the AI turn
    def ai_turn(self):
        if self.screen != "game" or self.session.winner:
            return

        count = self.session.choose_ai_move()

        # The AI chooses a count; the UI chooses which matches to show
        chosen = self.session.matches[-count:]

        self.ai_highlight = set(chosen)
        self.draw_board()

        # Remove the matches after highlighting them
        def finish():
            self.session.remove(chosen, "AI")
            self.ai_highlight.clear()

            word = "match" if count == 1 else "matches"

            self.feedback.configure(
                text=f"AI removed {count} {word}."
            )

            self.refresh()

            if self.session.winner:
                self.show_result()

        delay = 550 if self.animations.get() else 1
        self.later(delay, finish)

    # Show the game result
    def show_result(self):
        self.cancel_pending()
        self.screen = "result"

        player_won = self.session.winner == "Player"

        self.turn_label.configure(text="GAME OVER")
        self.selection_label.configure(text="")
        self.remove_button.configure(state="disabled")

        card = tk.Frame(
            self.body,
            bg=BACKGROUND,
            highlightbackground=GOLD,
            highlightthickness=2,
            padx=40,
            pady=22
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.label(
            card,
            "YOU WIN!" if player_won else "AI WINS",
            size=32,
            bold=True
        ).pack(pady=10)

        explanation = (
            "The AI took the last match."
            if player_won
            else "You took the last match."
        )

        self.label(
            card,
            explanation,
            size=15
        ).pack(pady=(0, 18))

        self.button(
            card,
            "Play Again",
            self.start_game,
            primary=True,
            width=22
        ).pack(pady=5)

        self.button(
            card,
            "Change Settings",
            self.show_setup,
            width=22
        ).pack(pady=5)

    # Confirm before leaving an unfinished game
    def confirm_leave(self, title, question):
        if self.screen != "game":
            return True

        return messagebox.askyesno(
            title,
            question,
            parent=self
        )

    # Restart with the same settings
    def restart(self):
        confirmed = self.confirm_leave(
            "Restart game",
            "Restart this game? "
            "Your current progress will be lost."
        )

        if confirmed:
            self.start_game()

    # Return to the setup screen
    def back_to_setup(self):
        confirmed = self.confirm_leave(
            "Back to setup",
            "Leave this game and return to setup? "
            "Your current progress will be lost."
        )

        if confirmed:
            self.show_setup()

    # Close the application
    def close(self):
        confirmed = self.confirm_leave(
            "Close Nim",
            "Close this game? "
            "Your current progress will be lost."
        )

        if confirmed:
            self.cancel_pending()
            self.destroy()

    # Handle the Enter key
    def enter_key(self, event):
        focused = self.focus_get()

        if isinstance(focused, tk.Button):
            focused.invoke()

        elif self.screen == "setup":
            self.start_game()

        elif self.human_turn():
            self.remove_selected()

        return "break"

    # Create a small popup window
    def dialog(self, title):
        window = tk.Toplevel(self)

        window.title(title)
        window.configure(bg=BACKGROUND)
        window.resizable(False, False)
        window.transient(self)
        window.grab_set()

        frame = tk.Frame(
            window,
            bg=BACKGROUND,
            padx=32,
            pady=24
        )
        frame.pack(fill="both", expand=True)

        self.label(
            frame,
            title,
            size=26,
            bold=True
        ).pack(pady=(0, 18))

        window.bind(
            "<Escape>",
            lambda event: window.destroy()
        )

        window.bind(
            "<Return>",
            lambda event: window.destroy()
        )

        window.update_idletasks()

        x = self.winfo_rootx() + 160
        y = self.winfo_rooty() + 120

        window.geometry(f"+{x}+{y}")

        return window, frame

    # Show the game rules
    def show_rules(self):
        window, frame = self.dialog("How to Play")

        text = (
            "Start with 15 matches in one pile.\n\n"
            "Take turns removing 1, 2, or 3 matches.\n"
            "Whoever takes the last match loses.\n\n"
            "Click any matches to select them.\n"
            "Click again to deselect, then press Remove.\n"
            "You can select across all rows.\n\n"
            "If AI starts, its opening move is random.\n\n"
            "Keyboard controls:\n"
            "Tab: move between controls\n"
            "Arrow keys: move between matches\n"
            "Space: select or deselect a match\n"
            "Enter: confirm removal\n"
            "Escape: clear the selection"
        )

        self.label(
            frame,
            text,
            size=15,
            justify="left"
        ).pack(pady=(0, 20))

        self.button(
            frame,
            "Got it",
            window.destroy,
            primary=True
        ).pack()

    # Show the interface settings
    def show_settings(self):
        window, frame = self.dialog("Settings")

        options = (
            ("Animate AI moves", self.animations),
            ("Selection sound", self.sound)
        )

        for title, variable in options:
            tk.Checkbutton(
                frame,
                text=title,
                variable=variable,
                font=(BUTTON_FONT, 13),
                bg=BACKGROUND,
                fg=CREAM,
                selectcolor=PANEL,
                activebackground=BACKGROUND,
                activeforeground=GOLD,
                highlightcolor=GOLD,
                padx=12,
                pady=12
            ).pack(anchor="w")

        self.button(
            frame,
            "Done",
            window.destroy,
            primary=True
        ).pack(pady=(20, 0))