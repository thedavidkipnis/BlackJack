import arcade
import arcade.gui
import ButtonStyles as bs


class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class PlayerSelectionButton(arcade.gui.UIFlatButton):
    def __init__(self,
                 x: float = 0,
                 y: float = 0,
                 width: float = 100,
                 height: float = 50,
                 text="",
                 size_hint=None,
                 size_hint_min=None,
                 size_hint_max=None,
                 style=None,
                 num=None,
                 **kwargs):
        super().__init__(x, y, width, height, text, size_hint, size_hint_min, size_hint_max, style)
        self.num = num

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        print(self.num)
        arcade.close_window()


class SetupMenu(arcade.Window):
    def __init__(self, screen_width, screen_height, title):
        super().__init__(screen_width, screen_height, title)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.GREEN)

        self.v_box = arcade.gui.UIBoxLayout()
        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        selection_label = arcade.gui.UIFlatButton(text="Select # of Players", style=bs.disabled_button, width=300, height=100)
        self.v_box.add(selection_label.with_space_around(bottom=20))

        for i in range(1, 5):
            selection_button = PlayerSelectionButton(text=str(i), width=100, height=100, num=i, style=bs.red_style)
            self.h_box.add(selection_button.with_space_around(right=20, left=20))

        self.v_box.add(self.h_box.with_space_around(bottom=100))

        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    # Draws the setup menu
    def on_draw(self):
        self.clear()
        self.manager.draw()




def main():
    # TODO: get screen size from os for setup menu
    setup_window = SetupMenu(600, 800, "Black Jack Setup")
    setup_window.run()
    setup_window = SetupMenu(800, 600, "Black Jack")
    setup_window.run()


if __name__ == "__main__":
    main()
