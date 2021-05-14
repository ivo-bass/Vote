from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton, MDRoundFlatButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen

from get_ballot import get_ballot
from get_preferences import get_preferences
from get_results import get_results
from write_to_db import write_vote_to_db, write_preference_to_db


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
        self.theme_text_color = "Error"
        self.bg_color = app.theme_cls.primary_color
        app.vote = self.text
        app.preference = None
        app.root.get_screen('voting').ids.vote_btn.disabled = False
        app.root.get_screen('voting').ids.preferences_grid.clear_widgets()
        app.root.get_screen('voting').draw_preferences()
        app.root.get_screen('voting').activate_preferences(self.text)

    def deselect(self):
        self.is_selected = False
        self.theme_text_color = "Primary"
        self.bg_color = [0, 0, 0, 0]
        app.vote = None

    def on_press(self):
        for item in VotingWindow.list_items:
            if item.is_selected:
                item.deselect()
        self.select()


class PreferenceButton(MDRoundFlatButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 16
        self.disabled = True
        self.is_selected = False

    def select(self):
        self.theme_text_color = "Error"
        self.md_bg_color = app.theme_cls.primary_color
        self.is_selected = True
        app.preference = self.text

    def deselect(self):
        self.theme_text_color = "Primary"
        self.md_bg_color = [0, 0, 0, 0]
        self.is_selected = False
        app.preference = None

    def on_press(self):
        if not self.disabled:
            for item in VotingWindow.preference_buttons:
                if item.is_selected:
                    item.deselect()
            self.select()


class VotingWindow(MDScreen):
    list_items = []
    preference_buttons = []

    def draw_preferences(self):
        VotingWindow.preference_buttons = []
        self.ids.preferences_grid.clear_widgets()
        for i in range(101, 119):
            new_button = PreferenceButton(text=str(i))
            self.ids.preferences_grid.add_widget(new_button)
            self.preference_buttons.append(new_button)
        if app.vote:
            self.activate_preferences(app.vote)


    def draw_candidates(self):
        if not app.vote:
            ballot = get_ballot()
            for digit, candidate in ballot:
                string = f"({digit}) {candidate}"
                new_list_item = ListItem(text=string)
                self.ids.scroll.add_widget(new_list_item)
                self.list_items.append(new_list_item)
            last_item = ListItem(text="Не подкрепям никого.")
            self.ids.scroll.add_widget(last_item)
            self.list_items.append(last_item)

    def activate_preferences(self, party_name):
        current_preferences = {}
        all_preferences = get_preferences()
        if party_name in all_preferences:
            current_preferences = all_preferences[party_name]
        for btn in self.preference_buttons:
            if btn.text in current_preferences.keys():
                btn.disabled = False
            else:
                btn.disabled = True


    def on_enter(self, *args):
        self.ids.scroll_view.scroll_y = 1
        app.is_final_vote = False
        self.ids.vote_btn.disabled = app.vote is None
        self.draw_candidates()
        self.draw_preferences()



    def vote(self):
        vote_text = app.vote
        pref_name = get_preferences()[app.vote][app.preference]
        preference_text = "Без избрана преференция" if not app.preference \
            else f"С преференция:\n({app.preference}) {pref_name}"
        choice_text = f"{vote_text}\n\n{preference_text}"
        self.manager.get_screen('submit').ids.submit_label.text = \
            f"Вие избрахте:\n\n{choice_text}\n\nПотвърждавате ли направения избор?"

        app.root.current = "submit"
        self.manager.transition.direction = "left"


class SubmitWindow(MDScreen):
    def submit(self):
        if app.is_final_vote:
            write_vote_to_db(app.vote)
            write_preference_to_db(app.vote, app.preference)
        self.clear_current_state()
        self.restart()

    def clear_current_state(self):
        app.vote = None
        app.preference = None
        app.is_final_vote = False
        VotingWindow.list_items = []
        VotingWindow.preference_buttons = []
        self.manager.get_screen('voting').ids.scroll.clear_widgets()
        self.manager.get_screen('voting').ids.preferences_grid.clear_widgets()
        self.manager.get_screen('entry').ids.pin_input.text = ''

    def restart(self):
        app.root.current = "entry"
        self.manager.transition.direction = "right"


class WindowManager(ScreenManager):
    pass


class VoteApp(MDApp):
    ADMIN_PINS = ("7878",)
    VOTER_PINS = ("0000", "1111", "9999")

    status = "ГЛАСУВАНЕТО НЕ Е АКТИВНО"
    is_voting_started = False
    is_final_vote = False
    vote = None
    preference = None

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("vote.kv")


if __name__ == '__main__':
    app = VoteApp()
    app.run()
