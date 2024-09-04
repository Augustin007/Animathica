# from ..Level import Tutorial, Level_Select
# from ..Canvas import canvas, library, space
# Flow of the game.
from .concept import Demo
from ..Calculator import Calculator_Test
settings: dict[str, int]= {}

Menu: dict[str, dict] = {
        'Main Menu' : {
            'Tutorial': [False, lambda: print('Tutorial not implimented yet')],
            'Level Select': [False, lambda: print('Level Select not implimented yet')],
            'Constructive Mode': [False, lambda: print('Constructive not implimented yet')],
            'Omnipotent Mode': [False, lambda: print('Omnipotent not implimented yet')],
            'Settings': [False, lambda: print('Settings not implimented yet')],
            'Exit': [True, lambda: 1],
            },
        'Temporary Demo Menu' : {
            'Canvas Demonstration': [True, Demo],
            'Calculator Test': [True, Calculator_Test]
            }
        }
Menuindex = []
for _, section in Menu.items():
    for _, (_, Function) in section.items():
        Menuindex.append(Function)

def Tutorial():
    print('Tutorial not implemented yet')

def display_menu():
    index = 0
    for section, menu in Menu.items():
        print(section)
        for name, (implemented, option) in menu.items():
           print(f'{index}. {name}', end='')
           index += 1
           if implemented:
               print()
               continue
           print(' Not Implemented')
        print('---')

def Menuit():
    display_menu()
    x = input()
    while not x.isnumeric() and int(x) < len(Menuindex):
        print(f'\nInvalid Input, expected a number from 0 to {len(Menuindex)}, try again!\n')
        x = input()
    return Menuindex[int(x)]

def main():
    print('Welcome to Animathica Demo!')
    while True:         
        Choice = Menuit()
        Current = Choice()
        if Current:
            return
