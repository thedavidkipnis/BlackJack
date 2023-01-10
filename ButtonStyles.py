import arcade

red_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": arcade.color.BLACK,
            "bg_color": arcade.color.REDWOOD,

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.RED,  # also used when hovered
            "font_color_pressed": arcade.color.RED,
        }


disabled_button = {
            "font_name": ("calibri", "arial"),
            "font_size": 20,
            "font_color": arcade.color.BLACK,
            "border_width": 2,
            "border_color": arcade.color.GREEN,
            "bg_color": arcade.color.GREEN,

            # used if button is pressed
            "bg_color_pressed": arcade.color.GREEN,
            "border_color_pressed": arcade.color.GREEN,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
}