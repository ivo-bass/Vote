import os

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.list import ILeftBodyTouch, OneLineIconListItem, OneLineListItem, OneLineAvatarListItem, \
    OneLineRightIconListItem, CheckboxRightWidget, IRightBodyTouch, MDCheckbox, ILeftBody, ContainerSupport, \
    OneLineAvatarIconListItem
from kivymd.uix.screen import MDScreen


from ballot import get_ballot
from write_to_db import write_to_db


class AdminWindow(MDScreen):
    pass


class EntryWindow(MDScreen):
    def clear_field(self):
        self.ids.pin_input.text = ''

    def btn_press(self, digit):
        if len(self.ids.pin_input.text) >= 4:
            return
        self.ids.pin_input.text += digit


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    pass


class LeftCheckbox(MDCheckbox, ILeftBodyTouch):
    pass


class VotingWindow(MDScreen):
    rows = {}
    is_empty = True

    def on_enter(self, *args):
        app.is_final_vote = False
        self.ids.vote_btn.disabled = app.vote is None

        if self.is_empty:
            ballot = get_ballot()
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

        app.vote = number

        app.root.current = "submit"
        self.manager.transition.direction = "left"


class SubmitWindow(MDScreen):
    @staticmethod
    def submit():
        if app.is_final_vote:
            write_to_db(app.vote)
        app.stop()


class WindowManager(ScreenManager):
    pass


class VoteApp(MDApp):
    ADMIN_PINS = ("7878",)
    VOTER_PINS = ("0000", "1111", "9999")

    is_final_vote = False
    vote = None

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("vote.kv")


if __name__ == '__main__':
    app = VoteApp()
    app.run()
