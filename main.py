from Views.tkinter_interface import TKInterInterface
from Views.cli_interface import CLI_Interface

def main():
    #user_view = TKInterInterface()
    user_view = CLI_Interface()
    user_view.run()


    print('Done!')
    exit()


if __name__ == '__main__':
    main()
