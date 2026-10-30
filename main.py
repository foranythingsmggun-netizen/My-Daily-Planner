__version__ = "1.0.0"

import json
from pathlib import Path

from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

SCHEDULE = [
    ("2:30–8:30 AM", "Sleep", "6h", "Sleep"),
    ("8:30–9:00 AM", "Freshen up", "30m", "Personal"),
    ("9:00–9:15 AM", "Music", "15m", "Personal"),
    ("9:15–9:35 AM", "Breakfast", "20m", "Personal"),
    ("9:35 AM–12:35 PM", "Study Session 1", "3h", "Study"),
    ("12:35–1:05 PM", "Bath", "30m", "Personal"),
    ("1:05–1:35 PM", "Lunch", "30m", "Personal"),
    ("1:35–2:15 PM", "Free time", "40m", "Personal"),
    ("2:15–5:15 PM", "Study Session 2", "3h", "Study"),
    ("5:15–5:35 PM", "Walk", "20m", "Personal"),
    ("5:35–6:35 PM", "Gaming Session 1", "1h", "Gaming"),
    ("6:35–8:35 PM", "Study Session 3", "2h", "Study"),
    ("8:35–9:15 PM", "Dinner", "40m", "Personal"),
    ("9:15–10:15 PM", "Editing Session 1", "1h", "Editing"),
    ("10:15 PM–12:15 AM", "Study Session 4", "2h", "Study"),
    ("12:15–1:15 AM", "Gaming Session 2", "1h", "Gaming"),
    ("1:15–2:15 AM", "Editing Session 2", "1h", "Editing"),
    ("2:15–2:30 AM", "Wind down", "15m", "Personal"),
]

COLORS = {
    "Study": (0.12, 0.55, 0.35, 1),
    "Sleep": (0.15, 0.35, 0.72, 1),
    "Gaming": (0.43, 0.27, 0.72, 1),
    "Editing": (0.78, 0.24, 0.48, 1),
    "Personal": (0.55, 0.40, 0.16, 1),
}

class PlannerApp(App):
    def build(self):
        self.title = "My Daily Planner"
        Window.clearcolor = (0.055, 0.07, 0.11, 1)
        self.state_file = Path(self.user_data_dir) / "progress.json"
        self.completed = self.load_progress()

        root = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))

        header = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(76), spacing=dp(3))
        header.add_widget(Label(text="[b]MY DAILY PLANNER[/b]", markup=True,
                                font_size="23sp", color=(1,1,1,1), halign="left"))
        header.add_widget(Label(text="24-HOUR PRODUCTIVITY PLAN", font_size="11sp",
                                color=(0.65,0.72,0.82,1), halign="left"))
        root.add_widget(header)

        summary = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(118))
        cards = [
            ("10 HOURS", "STUDY", COLORS["Study"]),
            ("6 HOURS", "SLEEP", COLORS["Sleep"]),
            ("2 HOURS", "GAMING", COLORS["Gaming"]),
            ("2 HOURS", "EDITING", COLORS["Editing"]),
        ]
        for big, small, color in cards:
            card = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(2))
            card.canvas.before.clear()
            from kivy.graphics import Color, RoundedRectangle
            with card.canvas.before:
                Color(*color)
                card.bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(12)])
            card.bind(pos=lambda w, p, c=card: setattr(c.bg, "pos", p),
                      size=lambda w, s, c=card: setattr(c.bg, "size", s))
            card.add_widget(Label(text=f"[b]{big}[/b]", markup=True, font_size="20sp"))
            card.add_widget(Label(text=small, font_size="11sp"))
            summary.add_widget(card)
        root.add_widget(summary)

        self.progress_label = Label(text="", size_hint_y=None, height=dp(25),
                                    color=(0.9,0.94,1,1), halign="left")
        root.add_widget(self.progress_label)
        self.progress = ProgressBar(max=len(SCHEDULE), value=len(self.completed),
                                    size_hint_y=None, height=dp(12))
        root.add_widget(self.progress)

        filters = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(5))
        for name in ["All", "Study", "Gaming", "Editing", "Personal", "Sleep"]:
            btn = Button(text=name, font_size="11sp", background_normal="",
                         background_color=(0.18,0.25,0.36,1))
            btn.bind(on_release=lambda b, n=name: self.show_filter(n))
            filters.add_widget(btn)
        root.add_widget(filters)

        self.scroll = ScrollView()
        self.items = GridLayout(cols=1, spacing=dp(7), size_hint_y=None, padding=(0, dp(3)))
        self.items.bind(minimum_height=self.items.setter("height"))
        self.scroll.add_widget(self.items)
        root.add_widget(self.scroll)

        bottom = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
        reset = Button(text="RESET TODAY", background_normal="",
                       background_color=(0.28,0.32,0.40,1))
        reset.bind(on_release=self.reset_progress)
        bottom.add_widget(reset)
        root.add_widget(bottom)

        self.show_filter("All")
        return root

    def load_progress(self):
        try:
            return set(json.loads(self.state_file.read_text()))
        except Exception:
            return set()

    def save_progress(self):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(sorted(self.completed)))

    def update_progress(self):
        n = len(self.completed)
        self.progress.value = n
        self.progress_label.text = f"DAILY PROGRESS: {n}/{len(SCHEDULE)} ACTIVITIES  •  {round(n/len(SCHEDULE)*100)}%"

    def show_filter(self, category):
        self.items.clear_widgets()
        for index, (time, task, duration, kind) in enumerate(SCHEDULE):
            if category != "All" and kind != category:
                continue
            done = index in self.completed
            row = BoxLayout(size_hint_y=None, height=dp(66), padding=dp(7), spacing=dp(8))
            from kivy.graphics import Color, RoundedRectangle
            with row.canvas.before:
                Color(0.12,0.15,0.21,1)
                bg = RoundedRectangle(pos=row.pos, size=row.size, radius=[dp(10)])
            row.bind(pos=lambda w,p,bg=bg: setattr(bg,"pos",p),
                     size=lambda w,s,bg=bg: setattr(bg,"size",s))
            tick = Button(text="✓" if done else "○", size_hint_x=None, width=dp(44),
                          background_normal="", background_color=COLORS[kind],
                          font_size="20sp")
            tick.bind(on_release=lambda b, i=index: self.toggle(i, category))
            labels = BoxLayout(orientation="vertical", spacing=dp(1))
            labels.add_widget(Label(text=f"[b]{task}[/b]", markup=True, font_size="14sp",
                                    halign="left", valign="middle", color=(0.92,0.95,1,1)))
            labels.add_widget(Label(text=time, font_size="11sp", halign="left",
                                    color=(0.65,0.72,0.82,1)))
            dur = Label(text=duration, size_hint_x=None, width=dp(48),
                        font_size="12sp", color=(0.9,0.9,0.95,1))
            row.add_widget(tick)
            row.add_widget(labels)
            row.add_widget(dur)
            self.items.add_widget(row)
        self.update_progress()

    def toggle(self, index, category):
        if index in self.completed:
            self.completed.remove(index)
        else:
            self.completed.add(index)
        self.save_progress()
        self.show_filter(category)

    def reset_progress(self, *_):
        content = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        content.add_widget(Label(text="Reset all today's completed activities?"))
        buttons = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        popup = Popup(title="Confirm reset", content=content, size_hint=(0.85,0.3))
        yes = Button(text="RESET")
        no = Button(text="CANCEL")
        buttons.add_widget(yes)
        buttons.add_widget(no)
        content.add_widget(buttons)
        yes.bind(on_release=lambda *_: (self.completed.clear(), self.save_progress(),
                                        self.show_filter("All"), popup.dismiss()))
        no.bind(on_release=popup.dismiss)
        popup.open()

if __name__ == "__main__":
    PlannerApp().run()
