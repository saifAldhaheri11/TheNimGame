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


# An ordinary class that contains the window
class NimApp:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("The NIM Game - Intro to AI Project")
        self.window.geometry("1040x850")
        self.window.minsize(800, 720)
        self.window.configure(bg=BACKGROUND)

        self.difficulty = "Medium"
        self.first_player = "Player"
        self.starting_objects = game.INITIAL_OBJECTS

        self.screen = "setup"
        self.session = None

        self.selected = set()
        self.ai_highlight = set()
        self.focus_match = None
        self.hovered_match = None

        self.pending = None
        self.popup = None
        self.buttons = []

        self.animations = tk.BooleanVar(
            master=self.window,
            value=True
        )
        self.sound = tk.BooleanVar(
            master=self.window,
            value=False
        )

        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.bind("<Return>", self.enter_key)
        self.window.bind("<Escape>", self.clear_selection)

        self.show_setup()

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

    # Build the shared top bar
    def shell(self):
        self.cancel_pending()

        for widget in self.window.winfo_children():
            widget.destroy()

        self.popup = None
        self.buttons = []

        header = tk.Frame(
            self.window,
            bg=BACKGROUND,
            padx=28,
            pady=14
        )
        header.pack(fill="x")

        self.label(
            header,
            "The NIM Game",
            34,
            bold=True
        ).pack(side="left")

        self.button(
            header,
            "Settings",
            self.show_settings
        ).widget.pack(side="right", padx=(12, 0))

        self.button(
            header,
            "How to Play",
            self.show_rules
        ).widget.pack(side="right")

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

    # Show the setup screen
    def show_setup(self):
        self.screen = "setup"
        self.shell()

        content = tk.Frame(self.body, bg=BACKGROUND)
        content.pack(expand=True)

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
            25,
            bold=True
        ).pack(pady=(0, 14))

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
            21,
            bold=True
        ).pack(pady=(14, 8))

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
        self.opening_note.pack(pady=8)

        self.count_note = self.label(
            content, "", 15, GOLD
        )
        self.count_note.pack(pady=(0, 10))

        self.update_count_note()

        self.button(
            content,
            "Start Game",
            self.start_game,
            primary=True,
            width=29
        ).widget.pack(pady=8)

        self.choose_difficulty(self.difficulty)
        self.choose_first(self.first_player)

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

    def update_count_note(self):
        if self.screen == "setup":
            self.count_note.configure(
                text=f"Starting matches: {self.starting_objects}"
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

        self.screen = "game"
        self.shell()

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
            self.back_to_setup
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
        match_height = min(100, row_height * 0.58)

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
                x - 25, y - 12,
                x + 25, y + match_height + 12
            )

    def human_turn(self):
        return (
            self.screen == "game"
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
            self.window.bell()

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

        self.session.remove(
            sorted(self.selected),
            "Player"
        )

        self.selected.clear()
        self.hovered_match = None

        self.feedback.configure(
            text="You removed " + self.match_text(count) + "."
        )

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

        self.refresh()

        if self.session.winner:
            self.show_result()

    # Show the winner and replay buttons
    def show_result(self):
        self.cancel_pending()
        self.screen = "result"

        self.turn_label.configure(text="GAME OVER")
        self.selection_label.configure(text="")

        self.remove_button.set_enabled(False)
        self.clear_button.set_enabled(False)

        card = tk.Frame(
            self.body,
            bg=BACKGROUND,
            highlightbackground=GOLD,
            highlightthickness=2,
            padx=40,
            pady=22
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        title = "AI WINS"
        reason = "You took the last match."

        if self.session.winner == "Player":
            title = "YOU WIN!"
            reason = "The AI took the last match."

        self.label(
            card, title, 32, bold=True
        ).pack(pady=10)

        self.label(
            card, reason, 15
        ).pack(pady=(0, 18))

        self.button(
            card,
            "Play Again",
            self.start_game,
            primary=True,
            width=22
        ).widget.pack(pady=5)

        self.button(
            card,
            "Change Settings",
            self.show_setup,
            width=22
        ).widget.pack(pady=5)

    # Confirm before leaving an unfinished game
    def confirm_leave(self, title, question):
        if self.screen != "game":
            return True

        return messagebox.askyesno(
            title,
            question,
            parent=self.window
        )

    def restart(self):
        if self.confirm_leave(
            "Restart Game",
            "Restart this game? "
        ):
            self.start_game()

    def back_to_setup(self):
        if self.confirm_leave(
            "Leave Game",
            "Leave this game? "
        ):
            self.show_setup()

    def close(self):
        if self.confirm_leave(
            "Close Game",
            "Close this game? "
        ):
            self.cancel_pending()
            self.window.destroy()

    def enter_key(self, event):
        focused = self.window.focus_get()

        for button in self.buttons:
            if focused == button.widget:
                button.activate()
                return "break"

        if self.screen == "setup":
            self.start_game()

        elif self.human_turn():
            self.remove_selected()

        return "break"

    # Create a popup window
    def make_popup(self, title):
        self.close_popup()

        self.popup = tk.Toplevel(self.window)
        self.popup.title(title)
        self.popup.configure(bg=BACKGROUND)
        self.popup.resizable(False, False)
        self.popup.transient(self.window)
        self.popup.grab_set()

        self.popup.protocol(
            "WM_DELETE_WINDOW",
            self.close_popup
        )
        self.popup.bind("<Escape>", self.close_popup)

        x = self.window.winfo_rootx() + 100
        y = self.window.winfo_rooty() + 100
        self.popup.geometry(f"+{x}+{y}")

        frame = tk.Frame(
            self.popup,
            bg=BACKGROUND,
            padx=30,
            pady=24
        )
        frame.pack(fill="both", expand=True)

        self.label(
            frame, title, 26, bold=True
        ).pack(pady=(0, 18))

        return frame

    def close_popup(self, event=None):
        if self.popup is not None:
            self.buttons = [
                button
                for button in self.buttons
                if button.widget.winfo_toplevel() != self.popup
            ]

            self.popup.destroy()
            self.popup = None

        return "break"

    # Show the rules
    def show_rules(self):
        frame = self.make_popup("How to Play")

        text = (
            "- Choose 5-30 starting matches in Settings.\n"
            "- Take turns removing 1, 2, or 3 matches.\n"
            "- Whoever takes the last match loses.\n"
            "- Click matches to select or deselect them.\n"
            "- You can select across all rows.\n"
            "- Press Remove to confirm your move.\n"
            "- If AI starts, its opening move is random.\n"
            "- All matchsticks belong to one pile.\n"
            "- Keyboard: (Tab) to the board, (arrows) to move,\n"
            "(space) to select, (Enter) to remove, (Esc) to clear."
        )

        rules = self.label(frame, text, 15)
        rules.configure(justify="left")
        rules.pack(pady=(0, 20))

        self.button(
            frame,
            "Got it",
            self.close_popup,
            primary=True
        ).widget.pack()

        self.popup.bind("<Return>", self.close_popup)

    # Show settings and prepare an editable count
    def show_settings(self):
        frame = self.make_popup("Settings")

        self.count_locked = self.screen == "game"
        self.settings_count = self.starting_objects

        self.label(
            frame,
            "Starting matches",
            19,
            bold=True
        ).pack(pady=(0, 8))

        self.label(
            frame,
            f"Minimum: {game.MIN_OBJECTS}  |  "
            f"Maximum: {game.MAX_OBJECTS}",
            12,
            LIGHT
        ).pack()

        controls = tk.Frame(frame, bg=BACKGROUND)
        controls.pack(pady=15)

        self.minus_button = self.button(
            controls,
            "-",
            self.change_count,
            value=-1,
            width=3
        )
        self.minus_button.widget.pack(
            side="left",
            padx=8
        )

        self.settings_number = self.label(
            controls, "", 28, GOLD, True
        )
        self.settings_number.configure(width=3)
        self.settings_number.pack(
            side="left",
            padx=10
        )

        self.plus_button = self.button(
            controls,
            "+",
            self.change_count,
            value=1,
            width=3
        )
        self.plus_button.widget.pack(
            side="left",
            padx=8
        )

        self.reset_button = self.button(
            frame,
            "Reset to 15",
            self.reset_count
        )
        self.reset_button.widget.pack(pady=(0, 10))

        if self.count_locked:
            self.label(
                frame,
                "Match count is locked during a game.",
                13,
                GOLD
            ).pack(pady=(0, 12))

        self.update_settings_count()

        tk.Frame(
            frame,
            bg=BORDER,
            height=1
        ).pack(fill="x", pady=10)

        options = (
            ("Animate AI moves", self.animations),
            ("Selection sound", self.sound)
        )

        for text, variable in options:
            tk.Checkbutton(
                frame,
                text=text,
                variable=variable,
                font=("Helvetica", 14),
                bg=BACKGROUND,
                fg=WHITE,
                selectcolor=PANEL,
                activebackground=BACKGROUND,
                activeforeground=GOLD,
                highlightcolor=GOLD,
                padx=10,
                pady=10
            ).pack(anchor="w")

        self.button(
            frame,
            "Done",
            self.save_settings,
            primary=True
        ).widget.pack(pady=(18, 0))

        self.popup.bind("<Return>", self.save_settings)

    # Update the number and its button limits
    def update_settings_count(self):
        self.settings_number.configure(
            text=str(self.settings_count)
        )

        self.minus_button.set_enabled(
            not self.count_locked
            and self.settings_count > game.MIN_OBJECTS
        )

        self.plus_button.set_enabled(
            not self.count_locked
            and self.settings_count < game.MAX_OBJECTS
        )

        self.reset_button.set_enabled(
            not self.count_locked
        )

    def change_count(self, amount):
        if not self.count_locked and self.screen != "game":
            new_count = self.settings_count + amount

            if game.MIN_OBJECTS <= new_count <= game.MAX_OBJECTS:
                self.settings_count = new_count

            self.update_settings_count()

    def reset_count(self):
        if not self.count_locked and self.screen != "game":
            self.settings_count = game.INITIAL_OBJECTS
            self.update_settings_count()

    # Save the starting count, never an active game's count
    def save_settings(self, event=None):
        if not self.count_locked and self.screen != "game":
            self.starting_objects = game.initialize_game(
                self.settings_count
            )
            self.update_count_note()

        self.close_popup()
        return "break"