"""Play script for pong game. Handles initial user interaction"""
# import mechanics
from time import sleep


def response() -> str:
    """Handles user input resonpses"""
    return input('(y)es/(n)o: ').lower().strip()  # I'm lazy


def blink_dots() -> str:
    """My attempt to make dots appear to blink in order"""
    pass


sleep(1)
print('Hello?')
sleep(1.5)
print('Is anyone there?\033[5m...\033[0m')
sleep(1.5)
res1 = response()
print('\033[5m....\033[0m')
sleep(1.5)
if not res1 == 'y':
    print('I must be hallucinating then\033[5m....\033[0m')
    sleep(2)
    quit()
else:
    print('I\'m glad I\'m not alone.')

    sleep(1.5)

    name = input('What shall I call you then dear friend? ').strip()
    while not name:
        name = input('I really do need your name: ').strip()
    while name.isalnum and (name.isnumeric()):
        print('Invalid input.Let\'s try that again.')
        name = input('What\'s your name?: ').strip()
    name = name.capitalize()

    print('\033[5m....\033[0m')
    sleep(1.5)
    print(f'Would you like to play my game {name}?\nIts a pong game.')
    res2 = response()
    print('\033[5m....\033[0m')
    sleep(1)

    if not res2 == 'y':
        print(f'Sorry to bother you then.')
        print('Bye\033[5m....\033[0m')
        sleep(2)
        quit()
    else:
        print('Great!!')
        print('The controls are (a,d) and (left-arrow, right-arrow) to move and\n(up-arrow, down-arrow)to change the ball speed')
        print('\033[5m....\033[0m')
        sleep(1.5)
        print('What speed would you like to play at?')
        sp = input('(S)low, (M)edium or (F)ast?: ').lower()
        sleep(1.5)
        print('Okay here we go!!!')

        import mechanics
        mechanics.play(sp)
