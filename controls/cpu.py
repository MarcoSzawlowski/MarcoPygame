from controls.controller import *
from player.players import *


class CPU(Controller):
    def __init__(self, char, action):
        super(CPU, self).__init__(char)
        self.actionstate = action

    def handle_input(self):
        if self.actionstate == "jump":
            if self.mychar.state == 0:
                self.mychar.jump()
            elif self.mychar.state == 2:
                self.mychar.jump()

    def action(self, type):
        self.actionstate = type