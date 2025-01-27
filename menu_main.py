import pathlib
from menu import Menu


class MenuMain(Menu):  # MenuMain inheriting Menu
    def __init__(self) -> None:
        super().__init__(options=[
            {"description": "Scan PDF", "action": self.scanPDF},
            {"description": "Say world", "action": self.sayWorld},
        ])
        # self.help_menu = MenuHelp()
        return None

    def scanPDF(self) -> None:
        print("Scaning")

        # đọc file pdf
        # lấy trang đầu có dc họ tên và ngày sinh
        #  
        return None

    def sayWorld(self) -> None:
        print("World!")
        return None
