
import os
from glob import glob
import inspect
import platform
from loguru import logger
from PIL import (
    ImageTk,
    Image,
)


# BG_COLOR = '#%02x%02x%02x' % (220, 218, 213)
WIDTH_UNIT = 400
LINE_HEIGHT = 22
BASE_DIR = inspect.getfile(inspect.currentframe())
BASE_DIR = os.path.dirname(os.path.abspath(BASE_DIR))


IMAGE_DICT = dict()
PARAMS = dict()


# pylint: disable=global-statement
def set_constants(tksession, calling_dir, theme):
    """Set top Tk objet"""
    global PARAMS
    PARAMS["top"] = tksession
    PARAMS["calling_dir"] = calling_dir

    if theme not in ["alt", "aqua", "clam", "classic", "default"]:
        print(theme + " theme not supported. Fallback to clam...")
        theme = "clam"

    PARAMS["theme"] = theme
    if theme == "alt":
        bgc = (224, 224, 224)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = "#%02x%02x%02x" % (
            bgc[0] - 7,
            bgc[1] - 7,
            bgc[2] - 7,
        )
    if theme == "aqua":
        bgc = (240, 240, 240)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = "#%02x%02x%02x" % (
            bgc[0] - 7,
            bgc[1] - 7,
            bgc[2] - 7,
        )
    if theme == "clam":
        bgc = (220, 218, 213)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = PARAMS["bg"]
    if theme == "classic":
        bgc = (224, 224, 224)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = "#%02x%02x%02x" % (
            bgc[0] - 6,
            bgc[1] - 6,
            bgc[2] - 6,
        )
    if theme == "default":
        bgc = (220, 218, 213)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = "#%02x%02x%02x" % (
            bgc[0] - 3,
            bgc[1] - 1,
            bgc[2] + 4,
        )

    bgc_dark = tuple([int(0.3 * i) for i in bgc])
    PARAMS["bg_dark"] = "#%02x%02x%02x" % bgc_dark
    PARAMS["hl_bg"] = '#ffe785'  # highlight background color
    PARAMS["verbose_log"] = False

def set_system():
    global PARAMS
    PARAMS["sys"] = platform.system()


def toggle_verbose():
    global PARAMS
    if PARAMS["verbose_log"] is False:
        PARAMS["verbose_log"]= True
        logger.info("Switching verbose mode on...")
    else:
        PARAMS["verbose_log"]= False
        logger.info("Switching verbose mode off...")

# pylint: disable=global-statement
def load_icons():
    """Load icons.

    Load all ./otinker_images/*_icon.gif as icons

    Returns :
    ---------
    load_icons : dictionnary of ImageTk objects
    """
    global IMAGE_DICT
    icons_dir = os.path.join(BASE_DIR, "images")
    icons_pattern = "_icon.gif"
    icons_files = glob("%s/*%s" % (icons_dir, icons_pattern))
    icons = dict()
    for k in icons_files:
        key = os.path.basename(k).replace(icons_pattern, "")
        im = Image.open(k).convert('RGBA')
        icons[key] = ImageTk.PhotoImage(im)
        IMAGE_DICT[key] = icons[key]
    return icons


def config_style(style):
    """Style configuration of widgets"""
    style.configure("Highlighted.TMenubutton", background=PARAMS['hl_bg'])
    style.configure('Highlighted.TRadiobutton', background=PARAMS['hl_bg'])
    style.configure('Highlighted.TLabel', background=PARAMS['hl_bg'])
    style.configure('Highlighted.TEntry', fieldbackground=PARAMS['hl_bg'])
    style.configure('Linkable.TLabel', foreground="blue")
    style.configure('Status.TLabel', foreground='red')

    style.map('TCombobox', fieldbackground=[('readonly', '#FFFFFF')],
                foreground=[('readonly', '#000000')],
                selectforeground=[('readonly', '#000000')],
                selectbackground=[('readonly', '#FFFFFF')])
    style.map('Highlighted.TCombobox', fieldbackground=[('readonly', PARAMS['hl_bg'])],
                selectforeground=[('readonly', '#000000')],
                selectbackground=[('readonly', PARAMS['hl_bg'])])