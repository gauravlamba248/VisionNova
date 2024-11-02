from PIL import ImageEnhance


class Pillow_enhancer:
    def __init__(self) -> None:
        self.enhancer_classes = {
            "sharpness": ImageEnhance.Sharpness,
            "color": ImageEnhance.Color,
            "brightness": ImageEnhance.Brightness,
            "contrast": ImageEnhance.Contrast,
        }

    def enhance(self, image, enhancement_type, factor):
        enhancer = self.enhancer_classes[enhancement_type](image)
        return enhancer.enhance(factor)
