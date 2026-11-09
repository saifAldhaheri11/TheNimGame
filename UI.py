# This file contains the graphical interface
import math
import tkinter as tk
from tkinter import messagebox

import game
from session import DIFFICULTIES, GameSession


# Interface colors
BACKGROUND = "#081C14"
PANEL = "#19432F"
BOARD = "#246348"
GOLD = "#FFD54A"
CREAM = "#FFFFFF"
MUTED = "#DCEDE3"
BORDER = "#79AD90"

# Interface fonts
TITLE_FONT = "Times"
BUTTON_FONT = "Helvetica"


# A button that displays our colors on macOS
class GlowButton(tk.Label):

    def __init__(
        self,
        parent,
        text,
        command,
        primary=False,
        **kwargs
    ):
        self.command = command
        self.inside = False
        self.focused = False

        self.normal_background = GOLD if primary else PANEL
        self.normal_foreground = BACKGROUND if primary else CREAM

        super().__init__(
            parent,
            text=text,
            bg=self.normal_background,
            fg=self.normal_foreground,
            font=(BUTTON_FONT, 13, "bold"),
            padx=18,
            pady=10,
            relief="flat",
            borderwidth=0,
            highlightthickness=3,
            highlightbackground=BORDER,
            highlightcolor=GOLD,
            disabledforeground="#CCDCD2",
            cursor="hand2",
            takefocus=True,
            **kwargs
        )

        # Mouse controls
        self.bind(
            "<Enter>",
            lambda event: self.set_hover(True)
        )
        self.bind(
            "<Leave>",
            lambda event: self.set_hover(False)
        )
        self.bind("<Button-1>", self.mouse_press)
        self.bind("<ButtonRelease-1>", self.mouse_release)

        # Keyboard controls
        self.bind(
            "<FocusIn>",
            lambda event: self.set_focus(True)
        )
        self.bind(
            "<FocusOut>",
            lambda event: self.set_focus(False)
        )
        self.bind("<space>", self.keyboard_press)

    # Keep the colors when the button changes
    def configure(self, cnf=None, **kwargs):
        if isinstance(cnf, dict):
            kwargs = {**cnf, **kwargs}

        elif cnf is not None:
            return super().configure(cnf, **kwargs)

        if not kwargs:
            return super().configure()

        if "bg" in kwargs:
            self.normal_background = kwargs["bg"]

        if "fg" in kwargs:
            self.normal_foreground = kwargs["fg"]

        result = super().configure(**kwargs)

        self.paint()
        return result

    config = configure

    # Show normal, highlighted, or disabled colors
    def paint(self):
        disabled = self.cget("state") == "disabled"

        background = self.normal_background
        foreground = self.normal_foreground
        border = BORDER

        if disabled:
            background = "#263F32"
            foreground = "#CCDCD2"
            border = "#557762"

        elif self.inside or self.focused:
            if background == GOLD:
                background = "#FFE789"
            else:
                background = "#2D6848"

            border = GOLD

        super().configure(
            bg=background,
            fg=foreground,
            highlightbackground=border,
            highlightcolor=border,
            cursor="" if disabled else "hand2"
        )

    def set_hover(self, value):
        self.inside = value
        self.paint()

    def set_focus(self, value):
        self.focused = value
        self.paint()

    def mouse_press(self, event):
        if self.cget("state") != "disabled":
            self.focus_set()

    def mouse_release(self, event):
        if (
            0 <= event.x < self.winfo_width()
            and 0 <= event.y < self.winfo_height()
        ):
            self.invoke()

    def keyboard_press(self, event):
        self.invoke()
        return "break"

    # Run the button action
    def invoke(self):
        if self.cget("state") != "disabled":
            return self.command()


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
        self.starting_objects = game.INITIAL_OBJECTS

        self.session = None
        self.screen = "setup"

        self.selected = set()
        self.ai_highlight = set()

        self.focus_match = None
        self.hovered_match = None
        self.pending = None

        self.animations = tk.BooleanVar(value=True)
        self.sound = tk.BooleanVar(value=False)

        self.protocol("WM_DELETE_WINDOW", self.close)

        self.bind("<Return>", self.enter_key)
        self.bind(
            "<Escape>",
            lambda event: self.clear_selection()
        )

        self.show_setup()

    # Create a label
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
        return GlowButton(
            parent,
            text,
            command,
            primary=primary,
            **kwargs
        )

    # Cancel a pending AI action
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

    # Create the top bar
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
        ).pack(side="right", padx=(12, 0))

        self.button(
            header,
            "How to Play",
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
        grid = tk.Frame(content, bg=BACKGROUND)
        grid.pack()

        self.difficulty_buttons = {}

        for index, level in enumerate(DIFFICULTIES):
            button = self.button(
                grid,
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
        choices = tk.Frame(content, bg=BACKGROUND)
        choices.pack()

        self.first_buttons = {}

        for value, text in (("Player", "You"), ("AI", "AI")):
            button = self.button(
                choices,
                text,
                lambda choice=value: self.set_first(choice),
                width=10
            )

            button.pack(side="left", padx=6)
            self.first_buttons[value] = button

        self.opening_note = self.label(
            content,
            "",
            size=12,
            color=MUTED
        )
        self.opening_note.pack(pady=8)

        self.count_note = self.label(
            content,
            "",
            size=15,
            color=GOLD
        )
        self.count_note.pack(pady=(0, 10))

        self.update_count_note()

        self.button(
            content,
            "Start Game",
            self.start_game,
            primary=True,
            width=29
        ).pack(pady=8)

        self.set_difficulty(self.difficulty)
        self.set_first(self.first_player)

    # Show the starting match count
    def update_count_note(self):
        if self.screen == "setup":
            self.count_note.configure(
                text=f"Starting matches: {self.starting_objects}"
            )

    # Highlight the selected difficulty
    def set_difficulty(self, value):
        self.difficulty = value

        for level, button in self.difficulty_buttons.items():
            selected = level == value

            button.configure(
                bg=GOLD if selected else PANEL,
                fg=BACKGROUND if selected else CREAM
            )

    # Highlight the selected starting player
    def set_first(self, value):
        self.first_player = value

        for player, button in self.first_buttons.items():
            selected = player == value

            button.configure(
                bg=GOLD if selected else PANEL,
                fg=BACKGROUND if selected else CREAM
            )

        self.opening_note.configure(
            text=(
                "The AI's opening move is random."
                if value == "AI"
                else ""
            )
        )

    # Start a new game
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
        turn = tk.Frame(self.body, bg=BACKGROUND)
        turn.pack(pady=(6, 4))

        self.you_badge = self.label(
            turn,
            "  You  ",
            size=16,
            bold=True,
            padx=18,
            pady=7
        )
        self.you_badge.pack(side="left", padx=3)

        self.ai_badge = self.label(
            turn,
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

        # Mouse controls
        self.board.bind(
            "<Configure>",
            lambda event: self.draw_board()
        )
        self.board.bind("<Button-1>", self.click_board)
        self.board.bind("<Motion>", self.hover_board)
        self.board.bind("<Leave>", self.leave_board)

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
        focused=False,
        hovered=False
    ):
        width = max(7, height * 0.12)

        # Draw the shadow
        canvas.create_line(
            x + 4,
            y + 14,
            x + 4,
            y + height + 3,
            fill="#103B29",
            width=width + 5,
            capstyle="round"
        )

        # Light up hovered and selected matches
        if selected or hovered:
            if selected:
                colors = (
                    "#99782B",
                    "#E8B938",
                    "#FFE873"
                )
            else:
                colors = (
                    "#3C8961",
                    "#72C393",
                    "#BEFFCE"
                )

            for color, spread in zip(colors, (12, 7, 3)):
                canvas.create_line(
                    x,
                    y + 5,
                    x,
                    y + height - 3,
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

        # Draw the wooden stem
        canvas.create_rectangle(
            x - width / 2,
            y + 10,
            x + width / 2,
            y + height,
            fill="#FFE09A" if selected else "#F3C776",
            outline="#BA8D43"
        )

        canvas.create_line(
            x - width / 4,
            y + 14,
            x - width / 4,
            y + height - 3,
            fill="#FFF2C4",
            width=max(2, width / 3)
        )

        # Draw the red head
        canvas.create_oval(
            x - width * 0.8,
            y - 3,
            x + width * 0.8,
            y + width * 1.8,
            fill="#FF5360" if selected else "#EE3547",
            outline="#AD2032",
            width=2
        )

        canvas.create_oval(
            x - width * 0.4,
            y,
            x + width * 0.15,
            y + width * 0.6,
            fill="#FF9299",
            outline=""
        )

        # Show keyboard focus
        if focused:
            canvas.create_rectangle(
                x - width - 17,
                y - 19,
                x + width + 17,
                y + height + 15,
                outline=CREAM,
                dash=(4, 4),
                width=2
            )

    # Arrange up to 30 matches on one board
    def draw_board(self):
        if self.screen != "game":
            return

        self.board.delete("all")

        width = self.board.winfo_width()
        height = self.board.winfo_height()

        if self.session.starting_objects <= 15:
            self.columns = 5
        else:
            self.columns = 6

        rows = math.ceil(
            self.session.starting_objects / self.columns
        )

        row_height = height / rows
        match_height = min(100, row_height * 0.58)

        self.hitboxes = {}

        for match in self.session.matches:
            row, column = divmod(match, self.columns)

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

            focused = (
                self.focus_get() == self.board
                and match == self.focus_match
            )

            hovered = (
                self.human_turn()
                and match == self.hovered_match
            )

            self.draw_match(
                self.board,
                x,
                y,
                match_height,
                selected,
                focused,
                hovered
            )

            # Make matches easier to click
            self.hitboxes[match] = (
                x - 25,
                y - 12,
                x + 25,
                y + match_height + 12
            )

    # Find the match under the mouse
    def hit_match(self, x, y):
        for match, bounds in self.hitboxes.items():
            left, top, right, bottom = bounds

            if left <= x <= right and top <= y <= bottom:
                return match

        return None

    # Check whether the player can move
    def human_turn(self):
        return (
            self.screen == "game"
            and not self.session.winner
            and self.session.current_player == "Player"
        )

    # Handle a clicked match
    def click_board(self, event):
        if self.human_turn():
            match = self.hit_match(event.x, event.y)

            if match is not None:
                self.focus_match = match
                self.board.focus_set()
                self.toggle_match(match)

    # Light up the match under the mouse
    def hover_board(self, event):
        if self.human_turn():
            match = self.hit_match(event.x, event.y)
        else:
            match = None

        self.board.configure(
            cursor="hand2" if match is not None else ""
        )

        if match != self.hovered_match:
            self.hovered_match = match
            self.draw_board()

    # Clear the hover highlight
    def leave_board(self, event):
        self.hovered_match = None
        self.board.configure(cursor="")
        self.draw_board()

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

        if matches:
            if self.focus_match in matches:
                index = matches.index(self.focus_match)
            else:
                index = 0

            steps = {
                "Left": -1,
                "Right": 1,
                "Up": -self.columns,
                "Down": self.columns
            }

            index = (
                index + steps[event.keysym]
            ) % len(matches)

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
        if (
            not self.human_turn()
            or match not in self.session.matches
        ):
            return

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
        player = self.human_turn()

        self.you_badge.configure(
            bg=GOLD if player else PANEL,
            fg=BACKGROUND if player else MUTED
        )

        self.ai_badge.configure(
            bg=PANEL if player else GOLD,
            fg=MUTED if player else BACKGROUND
        )

        self.turn_label.configure(
            text="YOUR TURN" if player else "AI'S TURN"
        )

        count = self.session.remaining
        word = "match" if count == 1 else "matches"

        self.count_label.configure(
            text=f"{count} {word} remaining"
        )

        if player:
            selection_text = f"{len(self.selected)} of 3 selected"
        else:
            selection_text = "AI is choosing..."

        self.selection_label.configure(
            text=selection_text
        )

        count = len(self.selected)

        if count:
            word = "match" if count == 1 else "matches"
            text = f"Remove {count} {word}"
        else:
            text = "Remove matches"

        state = (
            "normal"
            if player and count
            else "disabled"
        )

        self.remove_button.configure(
            text=text,
            state=state
        )
        self.clear_button.configure(state=state)

        self.draw_board()

    # Confirm the player move
    def remove_selected(self):
        if not self.human_turn() or not self.selected:
            return

        count = len(self.selected)

        self.session.remove(
            sorted(self.selected),
            "Player"
        )

        self.selected.clear()
        self.hovered_match = None

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

    # Highlight and remove the AI matches
    def ai_turn(self):
        if self.screen != "game" or self.session.winner:
            return

        count = self.session.choose_ai_move()

        # Match positions do not affect the AI decision
        chosen = self.session.matches[-count:]

        self.ai_highlight = set(chosen)
        self.draw_board()

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

    # Show the winner
    def show_result(self):
        self.cancel_pending()
        self.screen = "result"

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

        won = self.session.winner == "Player"

        self.label(
            card,
            "YOU WIN!" if won else "AI WINS",
            size=32,
            bold=True
        ).pack(pady=10)

        explanation = (
            "The AI took the last match."
            if won
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

    # Return to setup
    def back_to_setup(self):
        confirmed = self.confirm_leave(
            "Back to setup",
            "Leave this game? "
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

        if isinstance(focused, GlowButton):
            focused.invoke()

        elif self.screen == "setup":
            self.start_game()

        elif self.human_turn():
            self.remove_selected()

        return "break"

    # Create a popup window
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
            padx=30,
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

        x = self.winfo_rootx() + 100
        y = self.winfo_rooty() + 100

        window.geometry(f"+{x}+{y}")

        return window, frame

    # Show the rules
    def show_rules(self):
        window, frame = self.dialog("How to Play")

        text = (
            "Choose 1-30 starting matches in Settings.\n"
            "The default is 15. All matches belong to one pile.\n\n"
            "Take turns removing 1, 2, or 3 matches.\n"
            "Whoever takes the last match loses.\n\n"
            "Click any matches to select them.\n"
            "Click again to deselect, then press Remove.\n"
            "You can select across all rows.\n\n"
            "If AI starts, its opening move is random.\n\n"
            "Keyboard: Tab to the board, arrows to move,\n"
            "Space to select, Enter to remove, Esc to clear."
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

        window.bind(
            "<Return>",
            lambda event: window.destroy()
        )

    # Show the settings
    def show_settings(self):
        window, frame = self.dialog("Settings")

        # Lock the count while a game is active
        locked = self.screen == "game"

        # Keep changes separate until Done is pressed
        draft = tk.IntVar(value=self.starting_objects)

        self.label(
            frame,
            "Starting matches",
            size=19,
            bold=True
        ).pack(pady=(0, 8))

        self.label(
            frame,
            "Default: 15  |  Minimum: 1  |  Maximum: 30",
            size=12,
            color=MUTED
        ).pack()

        controls = tk.Frame(frame, bg=BACKGROUND)
        controls.pack(pady=15)

        # Update the count display and buttons
        def update_count():
            count_label.configure(text=str(draft.get()))

            minus.configure(
                state=(
                    "disabled"
                    if locked or draft.get() <= 1
                    else "normal"
                )
            )

            plus.configure(
                state=(
                    "disabled"
                    if locked or draft.get() >= game.MAX_OBJECTS
                    else "normal"
                )
            )

        # Increase or decrease the count
        def change_count(amount):
            if not locked:
                new_count = draft.get() + amount
                new_count = max(
                    1,
                    min(game.MAX_OBJECTS, new_count)
                )

                draft.set(new_count)
                update_count()

        minus = self.button(
            controls,
            "-",
            lambda: change_count(-1),
            width=3
        )
        minus.pack(side="left", padx=8)

        count_label = self.label(
            controls,
            str(draft.get()),
            size=28,
            color=GOLD,
            bold=True,
            width=3
        )
        count_label.pack(side="left", padx=10)

        plus = self.button(
            controls,
            "+",
            lambda: change_count(1),
            width=3
        )
        plus.pack(side="left", padx=8)

        self.count_controls = (minus, plus)

        # Restore the default count
        def reset_count():
            if not locked:
                draft.set(game.INITIAL_OBJECTS)
                update_count()

        reset = self.button(
            frame,
            "Reset to 15",
            reset_count
        )
        reset.pack(pady=(0, 10))

        if locked:
            reset.configure(state="disabled")

            self.label(
                frame,
                "Match count is locked during a game.",
                size=13,
                color=GOLD
            ).pack(pady=(0, 12))

        update_count()

        tk.Frame(
            frame,
            bg=BORDER,
            height=1
        ).pack(fill="x", pady=10)

        # Animation and sound settings
        options = (
            ("Animate AI moves", self.animations),
            ("Selection sound", self.sound)
        )

        for title, variable in options:
            tk.Checkbutton(
                frame,
                text=title,
                variable=variable,
                font=(BUTTON_FONT, 14),
                bg=BACKGROUND,
                fg=CREAM,
                selectcolor=PANEL,
                activebackground=BACKGROUND,
                activeforeground=GOLD,
                highlightcolor=GOLD,
                padx=10,
                pady=10
            ).pack(anchor="w")

        # Save the count only outside an active game
        def save():
            if not locked and self.screen != "game":
                self.starting_objects = game.initialize_game(
                    draft.get()
                )

                self.update_count_note()

            window.destroy()

        self.button(
            frame,
            "Done",
            save,
            primary=True
        ).pack(pady=(18, 0))

        window.bind(
            "<Return>",
            lambda event: save()
        )