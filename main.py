from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
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
    is_empty = True

    def on_enter(self, *args):
        app.is_final_vote = False

        self.ids.vote_btn.disabled = app.vote["number"] is None

        if self.is_empty:
            ballot = get_ballot(FILE_PATH)
            for digit, candidate in ballot:
                string = digit + " :  " + candidate

                # box = MDGridLayout(rows=1, cols=2)

                checkbox = MDCheckbox(group="group", pos_hint=(1, None), halign="right")
                item = MDLabel(text=string, size=(20, 20), pos_hint=(0.5, None))
                # name = MDLabel(text=candidate, pos_hint=(0.5, None))

                # box.add_widget(checkbox)
                # box.add_widget(number)

                self.ids.grid.add_widget(checkbox)
                self.ids.grid.add_widget(item)

                self.rows[checkbox] = (digit, candidate)
            self.is_empty = False


    def vote(self):
        choice = None
        for checkbox, info in VotingWindow.rows.items():
            if checkbox.active:
                choice = checkbox
                break

        number = self.rows[choice][0]
        name = self.rows[choice][1]

        choice_text = f"{number}: {name}"
        self.manager.get_screen('submit').ids.submit_label.text = \
            f"Вие избрахте:\n\n{choice_text}\n\nПотвърждавате ли направения избор?"

        app.vote["number"] = number
        app.vote["name"] = name

        app.root.current = "submit"
        self.manager.transition.direction = "left"


class SubmitWindow(MDScreen):

    @staticmethod
    def write_to_db():
        app.is_final_vote = True
        print(app.vote)
        pass


class WindowManager(ScreenManager):
    pass


class VoteApp(MDApp):
    ADMIN_PINS = ("7878",)
    VOTER_PINS = ("0000", "1111", "9999")

    is_final_vote = False
    vote = {"number": None, "name": None}

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("vote.kv")


if __name__ == '__main__':
    app = VoteApp()
    app.run()
