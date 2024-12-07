from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class MyTourClass(BaseCase):
    def test_google_tour(self):
        self.open("https://www.google.com/")
        self.wait_for_element('[role="listbox"]')
        self.type('input[name="q"]', "GitHub\n")
        self.wait_for_element("#search")
        self.open("https://www.google.com/maps/@42.3591234,-71.0915634,15z")
        self.wait_for_element("#searchboxinput")
        self.wait_for_element("#minimap")
        self.wait_for_element("#zoom")
