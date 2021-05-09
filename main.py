from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDCheckbox

import os

from ballot import get_ballot

FILE_NAME = 'ballot.csv'

CWD_PATH = os.path.abspath(os.getcwd())
FILE_PATH = os.path.join(CWD_PATH, FILE_NAME)


class AdminWindow(MDScreen):
    pass


class EntryWindow(MDScreen):
    def clear(self):
        self.ids.pin_input.text = ''

    def btn_press(self, digit):
        if len(self.ids.pin_input.text) >= 4:
            return
        self.ids.pin_input.text += digit


class VotingWindow(MDScreen):
    rows = {}

    def on_enter(self, *args):
        ballot = get_ballot(FILE_PATH)
        for digit, candidate in ballot:
            box = MDGridLayout(rows=1, cols=2)

            checkbox = MDCheckbox(group="group", size=(6, 6), pos_hint=(0, None))
            number = MDLabel(text=digit, size=(20, 20))

            box.add_widget(checkbox)
            box.add_widget(number)

            name = MDLabel(text=candidate, pos_hint=(0.5, None))

            self.ids.grid.add_widget(box)
            self.ids.grid.add_widget(name)

            VotingWindow.rows[checkbox] = (number.text, name.text)

    def on_leave(self, *args):
        self.ids.grid.clear_widgets()
        VotingWindow.rows = {}

    def vote(self):
        choice = None
        is_valid = False
        for checkbox, info in VotingWindow.rows.items():
            if checkbox.active:
                choice = checkbox
                is_valid = True
                break

        if not is_valid:
            pass  # TODO: error msg for missing choice


        number = VotingWindow.rows[choice][0]
        name = VotingWindow.rows[choice][1]

        choice_text = f"{number}: {name}"
        self.manager.get_screen('submit').ids.submit_label.text = \
            f"Вие избрахте:\n\n{choice_text}\n\nПотвърждавате ли направения избор?"

        app.vote["number"] = number
        app.vote["name"] = name


class SubmitWindow(MDScreen):
    @staticmethod
    def write_to_db():
        print(app.vote)
        pass


class WindowManager(ScreenManager):
    pass


class VoteApp(MDApp):
    ADMIN_PINS = ("7878",)
    VOTER_PINS = ("0000", "1111", "9999")

    vote = {"number": None, "name": None}

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("vote.kv")


if __name__ == '__main__':
    app = VoteApp()
    app.run()
