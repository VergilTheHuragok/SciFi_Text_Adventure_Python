import pygame

from configs import get_value, add_from_dict, get_config_dict

default_fonts = {"FONTS":
                     {"Default":
                          {"name": "monospace",
                           "size": 20,
                           "color": (255, 255, 255),
                           }
                      }
                 }

fonts = {}


def get_font_dict(font_name):
    """Updates font dict to include font object and returns dict"""
    global fonts
    if font_name not in fonts:
        # Update fonts if not in list
        add_from_dict(
            default_fonts)  # Update config to include all default fonts
        fonts = get_config_dict()[
            "FONTS"]  # Update fonts list to include conf fonts
        if font_name not in fonts:
            # Font missing from default)_fonts/config
            raise Exception("Font: '" + font_name + "' not found in fonts list")
    # font_name is in fonts
    if "font object" not in fonts[font_name]:
        # Need to add pygame font object to font's dict, has not been created yet

        # Get/add each necessary variable to fonts dict
        if "bold" not in fonts[font_name]:
            fonts[font_name]["bold"] = False
        font_bold = fonts[font_name]["bold"]

        if "italic" not in fonts[font_name]:
            fonts[font_name]["italic"] = False
        font_italic = fonts[font_name]["italic"]

        if "size" not in fonts[font_name]:
            fonts[font_name]["size"] = fonts["Default"]["size"]
        font_size = fonts[font_name]["size"]

        if "color" not in fonts[font_name]:
            fonts[font_name]["color"] = fonts["Default"]["color"]

        if "highlight color" not in fonts[font_name]:
            fonts[font_name]["highlight color"] = None

        try:
            # Create the font
            font = pygame.font.SysFont(font_name, font_size, font_bold,
                                       font_italic)
        except OSError:
            if font_name == "Default":
                raise Exception("Default font could not be loaded. "
                                "Change in config.")
            # Font is not default, use default instead
            print("Could not load font: '" + font_name + ",' using Default "
                                                         "font instead.")
            font = get_font_dict("Default")["font object"]
        fonts[font_name]["font object"] = font

    return fonts[font_name]


class Text(object):
    """Stores variables and methods for displaying pygame text"""

    def __init__(self, text, font_name=None, hover_text_list=None):
        self.text = text
        self.whole = text
        self.font_name = font_name
        self.hover_text_list = hover_text_list
        self.pos = None
        self.label = None
        self.width = None
        self.height = None

    def copy(self, text=None):
        """Returns a copy of the text object with new text"""
        if isinstance(text, type(None)):
            text = self.text
        new_text = Text(text, self.font_name, self.hover_text_list)
        new_text.whole = self.whole
        return

    def break_newlines(self):
        words = self.text.split("\n")
        new_texts = []
        i = 0
        for word in words:
            newline = ""
            if len(words) > 1:
                newline = "\n"
            new_texts.append(self.copy(word + newline))  # TODO: Finish breaking into new line words
            i += 1

    def get_dimensions(self):
        """Returns dimensions of text, generates new dimensions if necessary"""
        if isinstance(self.width, type(None)):
            font = get_font_dict(self.font_name)["font object"]
            self.width, self.height = font.get_size(self.text)
        return self.width, self.height

    def get_label(self):
        """Generates if necessary and returns a label"""
        if isinstance(self.label, type(None)):
            font_dict = get_font_dict(self.font_name)
            font = font_dict["font object"]
            self.label = font.render(self.text.strip(), 1, font_dict["color"],
                                     font_dict["highlight color"])

        return self.label

    def clear_for_pickle(self):
        """Clears the label in order to not mess with the pickling process"""
        self.label = None

    def render(self, display, pos):
        """Renders text to given display"""
        self.pos = pos
        display.blit(self.get_label(), pos)

    def is_hovered(self, mouse_pos):
        """Checks whether text is being hovered"""
        if isinstance(self.pos, type(None)):
            print("Warning: Text not yet rendered when click attempted")
            # TODO: Does this ever occur and is it a problem?
            return False
        width, height = self.get_dimensions()
        if self.pos[0] <= mouse_pos[0] <= self.pos[0] + width:
            if self.pos[1] <= mouse_pos[1] <= self.pos[1] + height:
                return True
        return False

    def get_hover_text(self):
        return self.hover_text_list


class Textbox:

    def __init__(self, name, x_pin, y_pin, x2_pin, y2_pin):
        self.name = name
        self.x_pin = x_pin
        self.y_pin = y_pin
        self.x2_pin = x2_pin
        self.y2_pin = y2_pin

        self.text_list = []
        self.lines = []
        self.line_num = 0

        self.width = None
        self.height = None
        self.screen_width = None
        self.screen_height = None

        # TODO: Allow saving of multiple self.lines for easily redisplaying tooltips?

    def add_text_list(self, text_list):
        self.text_list += text_list
        self.wrap()

    def get_dimensions(self):
        if isinstance(self.width, type(None)):
            raise Exception("Access to dimensions attempted before rendering "
                            "for textbox: '" + self.name + ".'")
        return self.width, self.height

    def update_dimensions(self, display):
        # Update dimensions if necessary
        width = display.get_width()
        height = display.get_height()
        changed = False
        if width != self.screen_width:
            # Width has been changed
            self.screen_width = width
            self.width = (self.x2_pin * width) - (self.x_pin * width)
            changed = True
        if height != self.screen_height:
            # Width has been changed
            self.screen_height = height
            self.height = (self.y2_pin * height) - (self.y_pin * height)
            changed = True
        if changed:
            self.rewrap()

    def render(self, display):
        self.update_dimensions(display)  # Will always rewrap on first render

    def check_line_num(self):
        if self.line_num >= len(self.lines):
            self.line_num = len(self.lines) - 1
            if self.line_num < 0:
                self.line_num = 0

    def rewrap(self):
        """Rewraps all lines in the event of a resolution change."""
        for line in self.lines:
            for text in line:
                self.text_list.insert(0, text)
        self.lines = []
        self.wrap()

    def check_line_can_fit(self, text):
        """Checks whether given text can fit in last line"""
        if self.lines[-1][-1].text.endswidth("\n"):
            return False  # Last line ended with new line char
        width = 0
        for _text in self.lines[-1]:
            width += _text.get_dimensions()[0]
        if width + text.get_dimensions()[0] <= self.width:
            return True
        return False

    def wrap(self):
        while len(self.text_list) > 0:
            text = self.text_list.pop(0)
            # TODO: Break newlines somewhere, somehow
            if text.get_dimensions()[1] > self.screen_height:
                print("Cannot display text: '" + text.text + "' as it does not "
                                                             "fit on screen.")
                continue  # Do not display text larger than screen size
            if self.check_line_can_fit(text):
                self.lines[-1].append(text)
                continue  # Text added to previous line
            # TODO: Finish wrapping
