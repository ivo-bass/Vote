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


class NumpadButton(MDFillRoundFlatButton):
    pass


class EntryWindow(MDScreen):

    def clear_field(self):
        self.ids.pin_input.text = ''

    def btn_press(self, digit):
        if len(self.ids.pin_input.text) >= 4:
            return
        self.ids.pin_input.text += digit


class ListItem(OneLineListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_selected = False

    def select(self):
        self.is_selected = True
        self.bg_color = app.theme_cls.primary_color
        app.vote = self.text
        app.root.get_screen('voting').ids.vote_btn.disabled = False

    def deselect(self):
        self.is_selected = False
        self.bg_color = [0, 0, 0, 0]
        app.vote = None

    def on_press(self):
        for item in VotingWindow.list_items:
            if item.is_selected:
                item.deselect()
        self.select()


class VotingWindow(MDScreen):
    list_items = []

    def on_enter(self, *args):
        app.is_final_vote = False
        self.ids.vote_btn.disabled = app.vote is None

        ballot = get_ballot()
        for digit, candidate in ballot:
            string = digit + " : " + candidate
            new_list_item = ListItem(text=string)
            self.ids.scroll.add_widget(new_list_item)
            self.list_items.append(new_list_item)


    def vote(self):
        choice_text = app.vote
        self.manager.get_screen('submit').ids.submit_label.text = \
            f"Вие избрахте:\n\n{choice_text}\n\nПотвърждавате ли направения избор?"

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
