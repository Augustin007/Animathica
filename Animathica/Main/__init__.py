# from ..Level import Tutorial, Level_Select
# from ..Canvas import canvas, library, space
# Flow of the game.
from .concept import Demo
from ..Calculator import Calculator_Test
settings = {}

Menu = [
        lambda: print('Tutorial not implimented yet'),
        lambda: print('Level Select not implimented yet'),
        lambda: print('Constructive not implimented yet'),
        lambda: print('Omnipotent not implimented yet'),
        lambda: print('Settings not implimented yet'),
        lambda: 'Exit',
        Demo,
        Calculator_Test
        ]
def Tutorial():
    print('Tutorial not implemented yet')


def main():
    while True:
        print('''Welcome to Animathica Demo!
Main Menu:
Please select a mode
0. Tutorial (Not Implemented)
1. Level Select (Not Implemented)
2. Constructive Mode (Not Implemented)
3. Omnipotent Mode (Not Implemented)
4. Settings (Not Implemented)
5. Exit (Not Implemented)
---
Temporary Demos:
6. Canvas Demonstration
7. Calculator Test
              ''')
        x = input()
        while not (x.isnumeric() and 0 <= int(x)<=7):
            print('Invalid input, try again')
            x = input()
        Choice = Menu[int(x)]
        Current = Choice()
        if Current == 'Exit':
            return
        # Technically should be all async and stuff and display, but this is more for keeping it straight in my head.
        # Choice = DisplayMenu.mainloop() (modes: Tutorial, Level Select, Constructive, Omnipotent, + settings? And exit). This function displays the menu and returns the correct mode.
        # if Choice == Exit: break
        # Current = Choice.mainloop() # Choose specific level.
        # Back = Current.mainloop()
        # Do we make this a while loop?
        pass
