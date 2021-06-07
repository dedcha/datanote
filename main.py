from Imports import *
from Subclass import *

class mainapp(App):

    home_screen = homescrn(name='home')
    data_screen = datascrn(name='data')
    
    def changeScreenToData(self):
        self.sm.switch_to(self.data_screen)
    def changeScreenToHome(self):
        self.sm.switch_to(self.home_screen)
    
    def scrnManag(self, *args):
        if self.sm.current == 'home':
            self.data_screen.remove_widget(BoxM())
            self.home_screen.add_widget(BoxL())
        if self.sm.current == 'data':
            self.home_screen.remove_widget(BoxL())
            self.data_screen.add_widget(BoxM())

    def build(self):
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(self.home_screen)
        self.sm.add_widget(self.data_screen)

        self.home_screen.add_widget(BoxL())
        self.data_screen.add_widget(BoxM())
        #self.scrnManag()

        #self.data_screen.add_widget(self.data_menu)
        #Clock.schedule_once(self.scrnManag, 1)

        self.sm.current = 'home'

        return self.sm
if __name__ == '__main__':
    mainapp().run()
