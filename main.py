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
from get_results import get_results
from write_to_db import write_to_db


class ResultsWindow(MDScreen):
    def on_enter(self, *args):
        results = get_results()
        counter = 0
        for name, votes in results:
            counter += 1
            string = f"{counter}.  {name} => {votes}бр. гласове"
            new_list_item = OneLineListItem(text=string)
            self.ids.results_list.add_widget(new_list_item)


class AdminWindow(MDScreen):
    @staticmethod
    def power_off():
        app.stop()

    def start_elections(self):
        app.is_voting_started = True
        app.status = "АКТИВНО ГЛАСУВАНЕ"
        self.manager.get_screen('entry').ids.pin_input.text = ''
        self.manager.get_screen('entry').ids.status.title = app.status
        app.root.current = "entry"
        self.manager.transition.direction = "right"

    def end_elections(self):
        app.is_voting_started = False
        self.print_results()

    def print_results(self):
        app.root.current = "results"
        self.manager.transition.direction = "left"


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
    def submit(self):
        if app.is_final_vote:
            write_to_db(app.vote)
        self.manager.get_screen('entry').ids.pin_input.text = ''
        app.root.current = "entry"
        self.manager.transition.direction = "left"


class WindowManager(ScreenManager):
    pass


class VoteApp(MDApp):
    ADMIN_PINS = ("7878",)
    VOTER_PINS = ("0000", "1111", "9999")

    status = "ГЛАСУВАНЕТО НЕ Е АКТИВНО"
    is_voting_started = False
    is_final_vote = False
    vote = None

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("vote.kv")


if __name__ == '__main__':
    app = VoteApp()
    app.run()
