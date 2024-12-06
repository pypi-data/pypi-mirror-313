
import os
from abc import ABCMeta
from abc import abstractmethod
import tkinter as tk
from tkinter import filedialog
from loguru import logger
from nobvisual.nob2nstruct import visual_treenob

from opentea.noob.asciigraph import nob_asciigraph
from opentea.gui_forms.utils import quit_dialog
from opentea.gui_forms.constants import toggle_verbose
from opentea.gui_forms.generic_widgets import TextConsole


# TODO: about in md instead?
ABOUT = """
This is GUI FORMS, front ends provided by OpenTEA.

OpenTEA is an open source python package to help
the setup of complex softwares.
OpenTEA is currently developed at Cerfacs by the COOP team.
Meet us at coop@cerfacs.fr.
"""


class DefaultMenubar:
    """The main munubar on the top of the screen"""
    def __init__(self, otroot):
        self.otroot = otroot
        self.menus = []
        self._add_menus()

    @property
    def menubar(self):
        if len(self.menus) == 0:
            return None
        return self.menus[-1].master

    def _add_menus(self):
        self.add_menu(FileMenu(self.otroot))
        self.add_menu(DebugMenu(self.otroot, menubar=self.menubar))
        self.add_menu(HelpMenu(self.otroot, menubar=self.menubar))

    def add_menu(self, menu):
        self.menus.append(menu)

    def activate(self):
        self.otroot.tksession.configure(menu=self.menubar)


class _Menu(tk.Menu, metaclass=ABCMeta):

    def __init__(self, otroot, label, menubar=None, **kwargs):
        if menubar is None:
            menubar = tk.Menu()

        super().__init__(menubar, tearoff=0, **kwargs)
        menubar.add_cascade(label=label, menu=self)

        self.otroot = otroot
        self._add_items()
        self._bind_items()

    @property
    def root(self):
        return self.otroot.tksession

    @abstractmethod
    def _add_items(self):
        pass

    def _bind_items(self):
        pass


class FileMenu(_Menu):

    def __init__(self, otroot, label='File', **kwargs):
        super().__init__(otroot, label, **kwargs)

    def _add_items(self):

        self.add_command(label="Load  (Ctrl+O)", image=self.otroot.icons["load"],
                         compound="left", command=self.on_load)

        self.add_command(label="Save as (Ctrl+S)", image=self.otroot.icons["save"],
                         compound="left", command=self.on_save_as)

        self.add_separator()

        self.add_command(label="Quit   (Ctrl+W)", image=self.otroot.icons["quit"],
                         compound="left", command=self.on_quit)

    def _bind_items(self):
        self.root.bind("<Control-o>", self.on_load)
        self.root.bind("<Control-s>", self.on_save_as)
        self.root.bind("<Control-w>", self.on_quit)

    def on_load(self, event=None):
        """Load data in current application."""
        file = filedialog.askopenfilename(
            title="Select file",
            filetypes=(("YAML files", "*.yml"), ("YAML files", "*.yaml"),
                       ("all files", "*.*"))
        )
        if file != "":
            self.otroot.load_project(file)

    def on_save_as(self, event=None):
        """Save data in current application."""
        filename = filedialog.asksaveasfilename(
            title="Select a new location for your project",
            defaultextension=".yml",
            filetypes=(("YAML files", "*.yml"), ("all files", "*.*"))
        )

        if filename == '':
            return

        self.otroot.data_file = os.path.abspath(filename)
        self.otroot.save_project()

        # TODO: why to change dir?
        # os.chdir(os.path.dirname(filename))

    def on_quit(self, event=None):
        """Quit full application from the menu."""

        quit_dialog()


class DebugMenu(_Menu):

    def __init__(self, otroot, label='Debug', **kwargs):
        super().__init__(otroot, label, **kwargs)

    def _add_items(self):

        self.add_command(label="Show tree", image=self.otroot.icons["tree"],
                         compound="left", command=self.on_show_tree)

        self.add_command(label="Show circular map", image=self.otroot.icons["tree"],
                         compound="left", command=self.on_show_circular)
        self.add_command(label="Show status map", image=self.otroot.icons["tree"],
                         compound="left", command=self.on_show_status)
        self.add_command(label="Toggle verbose log",
                         compound="left", command=self.on_toggle_verbose)


    def _bind_items(self):
        self.root.bind("<Control-h>", self.on_show_tree)


    def on_toggle_verbose(self, event=None):
        """Toggle verbose mode in terminal
        """
        toggle_verbose()
            


    def on_show_tree(self, event=None):
        toplevel = tk.Toplevel(self.root)
        toplevel.title("Tree View")
        toplevel.transient(self.root)

        memory = tk.StringVar(value=nob_asciigraph(self.otroot.get()))

        TextConsole(toplevel, memory, search=True)

    def on_show_circular(self, event=None):
        """Show memory with nobvisual.
        """
        # TODO: data or project_file?

        title = f'Current memory of {self.otroot.data_file}'

        visual_treenob(self.otroot.get(), title=title)


    def on_show_status(self, event=None):
        """Show memory with nobvisual.
        """
        # TODO: data or project_file?

        title = f'Current memory of {self.otroot.data_file}'

        dict_status= {
            "root": {
                "status": 0,
                "children": {}
            }
        }

        def rec_status(node, dict_status_holder):
            for child in node.children.values():
                dict_status_holder[child.name]= {
                    "status": child.status,
                    "children": {}
                }
                rec_status(child,dict_status_holder[child.name]["children"])
            

        rec_status(self.otroot._form, dict_status)

        visual_treenob(dict_status, title=title)


class HelpMenu(_Menu):

    def __init__(self, otroot, label='Help', **kwargs):
        super().__init__(otroot, label, **kwargs)

    def _add_items(self):

        self.add_command(label="About", image=self.otroot.icons["about"],
                         compound="left", command=self.on_about)

    def on_about(self):
        toplevel = tk.Toplevel(self.root)
        toplevel.title("About")
        toplevel.transient(self.root)

        memory = tk.StringVar(value=ABOUT)

        TextConsole(toplevel, memory)
