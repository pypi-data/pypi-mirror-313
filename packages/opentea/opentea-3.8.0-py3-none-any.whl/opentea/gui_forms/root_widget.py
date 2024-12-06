"""
The root widget
===============

The root widget is the fisrt called by otinker.
It corresponds to the firts node ot the SCHEMA.

At the root widget, the whole window is created.
The root host the main Tab-notebook,
and if necessary the wiew 3D tab.

Tabs callbacks:
===============

As tabs callbacks can change any part of the memory,
These callbacks are passed down to the root widget,
trigerring two subprocesses.

Execute:
--------

Execute is about memory modification.
The callback associated shows the following singature:

nested object > callback > nested object

Update_3d_view:
---------------

Update_3d_view is about 3D feedback.
The callback associated shows the following singature:

nested object, 3D scene > callback > 3D scene

"""

from __future__ import annotations
import abc
from copy import deepcopy
from tkinter import ttk, Tk

import yaml


from tiny_3d_engine.engine import Engine3D

from opentea.gui_forms.constants import (
    PARAMS,
    load_icons,
    set_system,
    config_style,
)


from opentea.gui_forms.node_widgets import (
    OTNodeWidget,
    OTTabWidget,
)
from opentea.gui_forms.menus import DefaultMenubar

from opentea.gui_forms.soundboard import play_door
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from opentea.gui_forms.acquisition2d import InteractivelineDrawer


class OTRoot:
    def __init__(
        self,
        schema: dict,
        tksession: Tk,
        style: str,
        data_file: str,
        tab_3d: callable = None,
        tab_2d: callable = None,
        acq_2d: callable = None,
        paraview_exec: str = None,
    ):
        # TODO: clear tmp_dir and delete at the end (.tmp?)
        # Compatibility with OOTTeeWidget
        self.name = "root"
        self.my_root_tab_widget = None  # See OTTreeElement to undestand this one (ADN)
        self.schema = schema
        self.tksession = tksession
        self.data_file = None  # The current data file to store the project

        #########

        # ADN : Todo, remove this horror!
        self._status_temp = 0
        self._status_invalid = 0  # Due to _update_parent_status()
        self.status = 0

        # Configuration of appearance
        self.global_config(style)
        self.set_menubar()
        play_door()
        # ===========================

        self.root_tab = RootTabWidget(self.schema, self, data_file)

        if tab_3d not in [None, False, True]:
            self.root_tab.view3d = add_viewer_3d(
                self, callback_3d=tab_3d, paraview_exec=paraview_exec
            )
        if tab_2d not in [None, False, True]:
            self.root_tab.view2d = add_viewer_2d(self, callback_2d=tab_2d)
        self.acq_2d = False
        if acq_2d not in [
            None,
        ]:
            self.acq_2d = True
            self.root_tab.acq2d = add_acquisition_2d(self, callback_2d_acq=acq_2d)

        if data_file is not None:
            self.load_project(data_file)

    @property
    def properties(self):
        # TODO: check if this is required
        return self.schema.get("properties", {})

    def global_config(self, style):
        """Main configurations for root widget"""
        self.icons = load_icons()
        set_system()
        config_style(style)
        self.tksession.columnconfigure(0, weight=1)
        self.tksession.rowconfigure(0, weight=1)

        self.frame = ttk.Frame(self.tksession, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky="news")

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", padx=2, pady=3, expand=True)

        # self._set_title()

    def set_menubar(self):
        """Start the menubar on the top of the screen"""
        self._menubar = DefaultMenubar(self)
        self._menubar.activate()
        # self._menubars = [self._menubar]

    def mainloop(self):
        """Start the mainloop

        usefull when testing to NOT start the mainloop
        """
        self.tksession.mainloop()

    def get(self):
        """How Opentea Save the project"""
        return self.root_tab.get()

    def set(self, data):
        """How Opentea Update the project"""
        return self.root_tab.set(data)

    def save_project(self):
        """How Opentea Save the project"""
        print("Main save projects")
        state = self.root_tab.get()
        if self.acq_2d:
            data = self.root_tab.acq2d.get()
            state.update({"acquisition": data})

        with open(self.data_file, "w") as fout:
            yaml.safe_dump(state, fout)

    def load_project(self, data_file):
        """How Opentea load the project"""
        print("Main load projects")

        if data_file is None:
            return
        print("df", data_file)
        self.data_file = data_file
        with open(data_file, "r") as fin:
            state = yaml.safe_load(fin)

        if state is None:
            return

        if self.acq_2d:
            if "acquisition" in state:
                self.root_tab.acq2d.set(state["acquisition"])
                del state["acquisition"]

        self.tksession.title(data_file)
        self.root_tab.set(state)

    def add_child(self, child: RootTabWidget):
        """Necessary to behave llike an OTTreeElement

        Called when creating the child RootTabWidget

        Because "
        When you create the element, it adds itself to its parent familly
        self.children[child.name] = child"

        """
        pass
        # indeed no need to update this
        # ADN : really I hate when OO forces you to add void methods
        #  to make it work
        # self.root_tab = child


class RootTabWidget(OTNodeWidget, metaclass=abc.ABCMeta):
    def __init__(self, schema: dict, parent: OTRoot, datafile: str = None):
        self.title = "RootTabWidget"
        # self.data_file = datafile
        self.view3d = None
        self.view2d = None

        super().__init__(schema, parent, "RootTabWidget")

        self.my_root_tab_widget = self
        self._config_frame()

        # specific attributes to handle dependents
        self._global_dependents = dict()
        self._dependents = self._global_dependents
        self._xor_dependents = dict()
        self._xor_level = 0
        self._dependent_names = set()

        self._initialize_tabs()

    #########################################
    # Dependencies with nested XOR
    # Lots to unpack and comment
    def prepare_to_receive_xor_dependents(self):
        self._xor_level += 1
        self._dependents = self._xor_dependents

    def assign_xor_dependents(self):
        self._xor_level -= 1

        if self._xor_level == 0:
            self.assign_dependents()
            self._dependents = self._global_dependents

    def add_dependency(self, master_name, slave):
        """Include a reactive dependency of one widget to the other

        If node1 have an ot_require for node2,
        node1 slave is added to node2 slave list, and node2 is the master.
        """
        slaves_list = self._dependents.get(master_name, [])

        self._dependents[master_name] = slaves_list

        self._dependent_names.add(slave.name)

        # TODO : ADN to me this is not used at all!
        slaves_list.append(slave)

    def assign_dependents(self):
        # find by name and add dependency
        for master_name, slaves in self._dependents.items():
            master = self.get_child_by_name(master_name)
            if master is None:
                msg = f"Dependency error, -{master_name}- was not found in your Schema"
                raise RuntimeError(msg)
            master.add_dependents(slaves)

        # reset dependents
        self._dependents.clear()

    ############################################

    ############################
    # ADN NEEDED TO REDEFINE
    # @property
    # def status(self):
    #     return self._get_status()

    # @status.setter
    # def status(self, status):
    #     if status == self._status:
    #         return
    #     self._status = status
    ###################################

    def _config_frame(self):
        """Configuration of the present widget"""
        self.frame = ttk.Frame(self.parent.frame)
        self.parent.notebook.add(self.frame, text=self.title)
        self.notebook = ttk.Notebook(self.frame, name="tab_nb")
        self.notebook.pack(fill="both", padx=2, pady=3, expand=True)

    def _initialize_tabs(self):
        """Addition of child tabs"""
        for tab_name, tab_obj in self.properties.items():
            OTTabWidget(tab_obj, self, tab_name)  # goes to children when creating tab

        self.assign_dependents()

        # set saved state
        # self.load_project(self.data_file)

        # validate
        self.validate()

    # def load_project_main_tab(self, state):
    #     print("Secondary load projects")
    #     self.set(state)

    # def save_project_main_tab(self):
    #     print("Secondary save projects")
    #     # if self.data_file is None:
    #     #     raise NotImplementedError
    #     return self.get()

    def _get_validated(self):
        return {tab.name: tab.status for tab in self.children.values()}

    def get(self) -> dict:
        """Add the metavidget setter to the basic get"""
        data_ = super().get()
        return data_

    def set(self, data):
        """Add the metavidget setter to the basic set"""

        data_ = deepcopy(data)
        super().set(data_)


# ====================================================================
# Viewers
# ====================================================================


def add_viewer_2d(otroot: OTRoot, callback_2d: callable):
    """Injection of a viewer 2D to opentea"""
    title = "2D View"
    view2d_fr = ttk.Frame(otroot.notebook, name=title)
    otroot.notebook.add(view2d_fr, text=title)
    viewer = Viewer2D(view2d_fr, otroot, callback_2d=callback_2d)
    return viewer


def add_viewer_3d(otroot: OTRoot, callback_3d: callable, paraview_exec: str):
    title = "3D view"
    view3d_fr = ttk.Frame(otroot.notebook, name=title)
    otroot.notebook.add(view3d_fr, text=title)
    viewer = Viewer3D(
        view3d_fr, otroot, callback_3d=callback_3d, paraview_exec=paraview_exec
    )
    return viewer


def add_acquisition_2d(otroot: OTRoot, callback_2d_acq: callable):
    title = "2D acq"
    view2da_fr = ttk.Frame(otroot.notebook, name=title)
    otroot.notebook.add(view2da_fr, text=title)
    viewer = InteractivelineDrawer(view2da_fr, otroot, callback_2d_acq=callback_2d_acq)
    return viewer


class Viewer2D:
    def __init__(self, master: ttk.Frame, otroot: OTRoot, callback_2d: callable):
        self.otroot = otroot
        self.callback_2d = callback_2d

        # Header frame to refresh
        _header_frame = ttk.Frame(master)
        _header_frame.pack(side="top", fill="both", padx=2, pady=3)
        refresh2d = ttk.Button(
            _header_frame, text="refresh2d", command=self.refresh_2d_view
        )
        refresh2d.pack(side="top")

        # Create a Frame to hold the plot
        _frame = ttk.Frame(master)
        _frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Create the Matplotlib figure and axes
        _fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = _fig.add_subplot(111)
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")

        # Embed the figure into the Tkinter frame
        self.canvas = FigureCanvasTkAgg(_fig, master=_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Add the Matplotlib Navigation Toolbar
        _toolbar = NavigationToolbar2Tk(self.canvas, _frame)
        _toolbar.update()
        _toolbar.pack(side="bottom", fill="x")

    def refresh_2d_view(self):
        self.ax.clear()
        self.callback_2d(self.ax, self.otroot.get())
        self.canvas.draw()


class Viewer3D(Engine3D):
    def __init__(
        self,
        master: ttk.Frame,
        otroot: OTRoot,
        callback_3d: callable,
        paraview_exec: str = None,
    ):
        super().__init__(
            root=master, width=1000, height=650, background=PARAMS["bg_dark"]
        )
        self.otroot = otroot
        self.callback_3d = callback_3d
        self.paraview_exec = paraview_exec

        _header_frame = ttk.Frame(master)
        _header_frame.pack(side="top", fill="both", padx=2, pady=3)
        refresh3d = ttk.Button(
            _header_frame, text="Refresh view", command=self.refresh_3d_view
        )
        refresh3d.pack(side="left")
        if self.paraview_exec is not None:
            open_para = ttk.Button(
                _header_frame, text="Open in Paraview", command=self.open_in_paraview
            )
            open_para.pack(side="left")

    def refresh_3d_view(self):
        new_scene = self.callback_3d(self.otroot.get())
        self.clear()
        self.update(new_scene)
        self.render()

    def open_in_paraview(self):
        import subprocess

        scene = self.callback_3d(self.otroot.get())
        scene.del_part("axis")  # No need to show axes in paraview
        scene.dump("scene")
        ensight_case_file = "./scene.case"
        try:
            # Build the command to run ParaView
            command = [self.paraview_exec, ensight_case_file]
            # Use subprocess to open ParaView
            subprocess.Popen(command)
            print(f"Opened ParaView with file: {ensight_case_file}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to open ParaView: {e}")
        except FileNotFoundError:
            print("ParaView executable not found. Check the path.")
        except Exception as e:
            print(f"An error occurred: {e}")
