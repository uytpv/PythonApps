from menu_main import MenuMain


class Main:
    def __init__(self) -> None:
        # 1. Initialize
        main_menu = MenuMain()
        # 2. Operate
        main_menu.start()
        # 3. Cleanup
        return None


if __name__ == "__main__":
    app = Main()
