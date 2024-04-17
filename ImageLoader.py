class ImageLoader:
    def __init__(self):
        self.image_root_path = "imgs/"

    def load_logo(self):
        return self.image_root_path + "logo.png"

    def load_exit_btn(self):
        return self.image_root_path + "btn_exit.png"

    def load_background(self):
        return self.image_root_path + "back_img.jpg"

    def load_hands(self):
        return self.image_root_path + "hands.png"

    def load_reset_btn(self):
        return self.image_root_path + "reset.png"
