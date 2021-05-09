from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, ILeftBodyTouch, OneLineAvatarListItem, \
    OneLineIconListItem
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


class ListItemWithCheckbox(OneLineIconListItem):
    pass


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    def on_press(self):
        pass



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
                new_list_item = ListItemWithCheckbox(text=string)
                self.ids.scroll.add_widget(new_list_item)

                self.rows[new_list_item.ids.check] = (digit, candidate)

            self.is_empty = False


    def vote(self):
        choice = None

        for list_item in self.ids.scroll.children:
            if list_item.ids.check.active:
                choice = list_item.ids.check
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
