"""Text and Textboxes"""
import pygame

default_font_name = "monospace"  # TODO: Make configs
default_color = (255, 255, 255)
default_font_size = 50

default_font = []


class Font:
    """Stores font variables and methods for using fonts"""

    def __init__(self, font_dict=None):
        self.name = None
        self.size = None
        self.color = None
        self.highlight_color = None
        self.bold = None
        self.italic = None

        if not isinstance(font_dict, type(None)):
            if "Name" in font_dict:
                self.name = font_dict["Name"]
            if "Size" in font_dict:
                self.size = font_dict["Size"]
            if "Color" in font_dict:
                self.color = font_dict["Color"]
            if "Highlight Color" in font_dict:
                self.highlight_color = font_dict["Highlight Color"]
            if "Bold" in font_dict:
                self.bold = font_dict["Bold"]
            if "Italic" in font_dict:
                self.italic = font_dict["Italic"]

        self.font = None

        self.update()

    def clear_font(self):
        self.font = None

    def update(self, force_update=False):
        """Updates font if necessary or specified"""
        if isinstance(self.color, type(None)):
            self.color = default_color
        if isinstance(self.size, type(None)):
            self.size = default_font_size
        if isinstance(self.font, type(None)) or force_update:
            try:
                self.font = pygame.font.SysFont(self.name, self.size,
                                                self.bold, self.italic)
            except OSError:
                print(
                    "Could not load font " + self.name + ", using default")
                self.name = default_font_name
                self.font = pygame.font.SysFont(self.name, self.size,
                                                self.bold, self.italic)

    def get_label(self, text):
        """Returns a pygame label for blitting to display"""
        return self.get_font().render(text.strip(), 1, self.color,
                                      self.highlight_color)

    def get_font(self):
        """Returns the pygame font object generated from stored variables"""
        self.update()
        return self.font

    def get_size(self, text):
        return self.get_font().size(text)


class Text:
    """Stores variables and methods for displaying pygame text"""

    def __init__(self, text, font=None):
        self.text = text

        self.font = font

        self.pos = None
        self.label = None

        self.update_font()

    def update_font(self):
        """Creates font from defaults if font is None"""
        if isinstance(self.font, type(None)):
            print("Warning: Font not provided")
            self.font = Font(*default_font)

    def get_label(self, force_new=False):
        """Generates if necessary and returns a label"""
        if isinstance(self.label, type(None)) or force_new:
            self.label = self.font.get_label(self.text)
        return self.label

    def render(self, display, pos):
        """Renders text to given display"""
        self.pos = pos
        display.blit(self.get_label(), pos)

    def is_hovered(self, mouse_pos):
        """Checks whether text is being hovered"""
        if isinstance(self.pos, type(None)):
            print("Warning: Text not yet rendered when click attempted")
            return False
        width, height = self.font.get_size(self.text)
        if self.pos[0] <= mouse_pos[0] <= self.pos[0] + width:
            if self.pos[1] <= mouse_pos[1] <= self.pos[1] + height:
                return True
        return False


class Line:
    pass
