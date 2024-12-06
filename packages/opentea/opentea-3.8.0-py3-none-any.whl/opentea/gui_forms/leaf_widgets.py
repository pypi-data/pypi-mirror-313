"""
Leaf widgets :
==============

Leaves are the lower part to the graph,
at the tip of the branches.
Most of these widget are entries.

Entries:
--------

The generic node EntryNode is the basis for all
single line inputs:

 - numbers
 - integers
 - strings

Additional content can be shown to give info
in the case of validation rules.

Booleans:
---------

This is tranlated to a single Checkbox

Choices:
--------

The choice widget corresponds to the Schema enum property.
This is tranlated to radiobuttons in the form.

FleBrowser:
-----------

This special entry check that the content is a file,
and add a browsing dialog to select the file.

Documentation and Description (DEPRECATED):
-------------------------------------------

Kept fo backward compatibility,
docuementation and descriptions are wats to display strings
in the forms.

Prefer now the documentation and description attributes
in the blocks.

Comments:
---------

Comments are multiline textfields
They can also be usefull for feedbach in disabled mode.

Lists:
------

List corresponds to arrays of parameters,
shown aslist of entries.
These list cannot take dependency links for the moments.

Without a fixed dimension,
specified with "MaxItemns" and "MinItems" attributes in the SCHEMA,
a +/- dialog is shown to extend or crop the list.

"""

import os
import operator
import abc

import tkinter
from tkinter import (
    ttk,
    Variable,
    StringVar,
    BooleanVar,
    Toplevel,
    Text,
    Entry,
    Listbox,
    filedialog,
    Menu,
    messagebox,
)

from nob import Nob

from opentea.gui_forms._base import OTTreeElement
from opentea.gui_forms._exceptions import (
    GetException,
    SetException,
)
from opentea.gui_forms.constants import (
    PARAMS,
    WIDTH_UNIT,
    LINE_HEIGHT,
    IMAGE_DICT,
)

from opentea.gui_forms.generic_widgets import TextConsole
from opentea.gui_forms.utils import (
    create_description,
    get_tkroot,
)
from opentea.gui_forms.soundboard import play_switch

from loguru import logger

# TODO: ot_require in widgets should make them disable
# TODO: does it make sense to use a tkvar everywhere? or an equivalent
# TODO: root_frame -> master_frame/holder
# TODO: implement ctrl-Z for validation?

# TODO: bring create_widget and set default to _LeafWidget?
# TODO: create opentea variables


class _LeafWidget(OTTreeElement, metaclass=abc.ABCMeta):
    """Factory for OpenTea Widgets."""

    def __init__(self, schema, parent, name, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested dict object
        root_frame :  a Tk object were the widget will be grafted
        holder_nlines : integer
            custom number of lines for holder
        """
        # TODO: should root frame be passed? homogenize with OTNodeWidget
        # TODO: can we have a LeafWidget without labels? (e.g. _ListEntry) (config?)
        super().__init__(schema, parent, name)

        self.title = self.schema.get("title", f'#{self.name}')
        self.state = self.schema.get("state", "normal")
        
        self._init_previous_value()
        self._create_common_leaf_widgets(root_frame)
        self._define_var()
        self._create_widgets()
        self._set_default()


    def _create_common_leaf_widgets(self, root_frame):
        r""" declare The base layout for our widgets

        root_frame
        ┌────────────────────────┐
        │                        │
        │ self._desc───────────┐ │
        │ │                    │ │
        │ └────────────────────┘ │
        │                        │
        │ self._holder─────────┐ │....(rely=0)
        │ │.label ne│nw        │ │
        │ │         │          │ │
        │ │         │          │ │
        │ └─────────┴──────────┘ │....(rely=1)
        │           .            │
        └────────────────────────┘
                    .(relx=0.5)
        """
        self._holder = ttk.Frame(root_frame,
                                 name=self.name,
                                 width=WIDTH_UNIT,
                                 height=LINE_HEIGHT)

        if self.state != "hidden":
            if "description" in self.schema:
                self._desc = create_description(root_frame, self.schema['description'],
                                            size=1, side='top')
            self._holder.pack(side="top", fill="x")

        self._label = ttk.Label(self._holder, text=self.title,
                                wraplength=int(0.5 * WIDTH_UNIT))
        self._label.place(relx=0.5, rely=0., anchor="ne")

        
    def _define_var(self):
        pass

    def _init_previous_value(self):
        self.previous_value = None

    def _create_widgets(self):
        pass

    def _set_default(self):
        if self.dependent:
            return
        self.set(self._get_default())

    def _get_default(self):
        return self.schema.get('default', '')

    def validate(self):
        if self.status == 0:
            self.status = 1
            self.validate_slaves()

    def on_value_change(self, *args):
        self.status = int(self.previous_value == self.get())

    def on_update_status(self):
        self._update_widgets_style()
        if self.status == 1:
            self.previous_value = self.get()

    def _update_widgets_style(self):
        pass

    def destroy(self):
        self._update_parent_status(1)
        self._holder.destroy()
        self._reset_master()


class OTHidden(_LeafWidget):

    def __init__(self, schema, parent, name, root_frame):
        # schema['state'] = 'hidden'
        # if "description" in schema:
        #     del schema['description']

        super().__init__(schema, parent, name, root_frame)


    def _define_var(self):
        self.tkvar = Variable()
        self.tkvar.trace('w', self.on_value_change)

    def get(self):
        return self.tkvar.get()

    def set(self, value):
        self.tkvar.set(value)


class _OTEntry(_LeafWidget, metaclass=abc.ABCMeta):
    """Factory for OpenTea Entries."""

    def _define_var(self):
        self.tkvar = Variable()
        self.tkvar.trace('w', self.on_value_change)

    def get(self):
        return self.tkvar.get()

    def set(self, value):
        #logger.info(f"set triggered on leaf {self.name}...")
        self.tkvar.set(value)

    def _create_widgets(self):
        self._entry = Entry(self._holder,
                            textvariable=self.tkvar,
                            borderwidth=0,
                            exportselection=False,
                            foreground="black",
                            background=self._get_entry_color())

        self._entry.place(relx=0.5, rely=1., anchor="sw")

        if self.state == "disabled" or self.dependent:
            self._config_disabled()

    def _config_disabled(self):
        """ Set the appearance of the entry to disbled color scheme"""
        self._entry.configure(
            highlightbackground=PARAMS["bg"],
            disabledbackground=PARAMS["bg"],
            disabledforeground=PARAMS["bg_dark"],
            state="disabled")

    def _get_entry_color(self):
        if self.status == 1:
            return 'white'

        return PARAMS['hl_bg']

    def _update_widgets_style(self):
        self._entry.configure(background=self._get_entry_color())


class _OTNumericEntry(_OTEntry, metaclass=abc.ABCMeta):

    def _create_widgets(self):
        super()._create_widgets()
        self._config_status_label()

    def _config_status_label(self):
        # change size and replace
        self._holder.config(height=2 * LINE_HEIGHT)
        self._entry.place(relx=0.5, rely=0.5, anchor="sw")
        self._label.place(relx=0.5, rely=0.5, anchor="se")

        self._status_lbl = ttk.Label(self._holder, text="no status yet",
                                     style='Status.TLabel', compound='left')

        self._bounds = [self.schema.get('minimum', -float('inf')),
                        self.schema.get('maximum', float('inf'))]
        self._exclusive_bounds = [self.schema.get("exclusiveMinimum", False),
                                  self.schema.get("exclusiveMaximum", False)]

        self._status_lbl.place(relx=1., rely=0.5, anchor="ne")

    def _reset_status_label(self):
        self._status_lbl.config(text='', image='')

    def _get_default(self):
        value = self.schema.get('default', None)

        if value is not None:
            return value

        # set a valid default value
        value = 0.0
        if 'minimum' in self.schema:
            value = self.schema['minimum']
            if self._exclusive_bounds[0]:
                if self._type == 'integer':
                    value += 1
                else:
                    value *= 1.1
        elif 'maximum' in self.schema:
            value = self.schema['maximum']
            if self._exclusive_bounds[1]:
                if self._type == 'integer':
                    value -= 1
                else:
                    value *= 0.9

        return value

    @abc.abstractmethod
    def str2type(self, value):
        pass

    def on_update_status(self):
        super().on_update_status()
        if self.status >= 0:
            self._reset_status_label()

    def get(self):
        try:
            return self.str2type(self.tkvar.get())
        except ValueError:
            raise GetException()

    def set(self, value):
        try:
            value = self.str2type(value)
            self.tkvar.set(value)

        except ValueError:
            raise SetException()

    def on_value_change(self, *args):

        # check type
        cur_value = self._check_type()
        if cur_value is None:  # error raised due to bad type
            return

        self.set_slaves(cur_value)

        if self.previous_value == cur_value:
            self.status = 1
            return

        # other validation
        if not self._validate_value(cur_value):
            return

        self.status = 0

    def _check_type(self):

        # check type
        try:
            return self.get()
        except GetException:
            error_msg = f'Invalid input "{self._entry.get()}"'
            self._update_invalid_status_label(error_msg)

        return None

    def _validate_value(self, value):
        # check bounds
        error_msg = self._check_bounds(value)
        if error_msg:
            self._update_invalid_status_label(error_msg)
            return False

        return True

    def _check_bounds(self, value):
        """Validate rules on entries."""
        str_operators = ['<', '>']
        operators = [operator.le, operator.ge]
        for lim, exclusive, operator_, str_operator in zip(
                self._bounds, self._exclusive_bounds, operators, str_operators):
            if operator_(value, lim):
                if not exclusive and value == lim:
                    continue

                return f"Invalid: {'=' if exclusive else ''}{str_operator}{lim}"

        return ""

    def _update_invalid_status_label(self, error_msg):
        self._status_lbl.config(
            text=error_msg, image=IMAGE_DICT['invalid'])
        self.status = -1


class OTInteger(_OTNumericEntry):

    def str2type(self, value):
        return int(value)


class OTString(_OTEntry):
    pass


class OTNumber(_OTNumericEntry):

    def str2type(self, value):
        return float(value)


class OTBoolean(_LeafWidget):

    def _define_var(self):
        self.tkvar = BooleanVar()
        self.tkvar.trace('w', self.on_value_change)

    def _create_widgets(self):
        self._label.place(relx=0.5, rely=0.5, anchor="e")
        self._cbutt = ttk.Checkbutton(self._holder,
                                      variable=self.tkvar,
                                      command=play_switch)
        self._cbutt.place(relx=0.5, rely=0.5, anchor="w")

    def _get_default(self):
        return self.schema.get('default', False)

    def get(self):
        return self.tkvar.get()

    def set(self, value):
        try:
            self.tkvar.set(bool(value))
        except ValueError:
            raise SetException()

    def _update_widgets_style(self):
        style = 'Highlighted.TLabel' if self.status != 1 else 'TLabel'
        self._label.configure(style=style)


class _OTChoiceAbstract(_LeafWidget, metaclass=abc.ABCMeta):
    # TODO: think about type -> OTVariable development

    def __init__(self, schema, parent, name, root_frame):
        super().__init__(schema, parent, name, root_frame)
        self._label.place(relx=0.5, rely=1, anchor="se")

    def _define_var(self):
        self.tkvar = StringVar()
        self.tkvar.trace('w', self.on_value_change)

    @abc.abstractmethod
    def _create_widgets(self):
        pass

    def _get_default(self):
        value = self.schema.get('default', None)

        if value is None:
            # TODO: check OT_DYN
            value = self.schema.get('enum', [''])[0]
        return value

    def get(self):
        return self.tkvar.get()

    def set(self, value):
        self.tkvar.set(value)


class OTChoice:

    def __new__(self, schema, parent, name, root_frame):

        if 'enum' in schema:
            if len(schema["enum"]) > 5:
                return _OTChoiceCombo(schema, parent, name, root_frame)
            else:
                return _OTChoiceRadio(schema, parent, name, root_frame)
        elif "ot_dyn_choice" in schema:
            return _OTChoiceDynamic(schema, parent, name, root_frame)


class _OTChoiceRadio(_OTChoiceAbstract):

    def __init__(self, schema, parent, name, root_frame):
        self.rad_btns = {}
        super().__init__(schema, parent, name, root_frame)

    def _create_widgets(self):
        self._pack_with_radiobuttons()

    def _pack_with_radiobuttons(self):
        """Radiobutton version of the widget"""
        n_lines = max(len(self.schema["enum"]), 1)
        self._holder.config(height=n_lines * LINE_HEIGHT)
        rel_step = 1. / n_lines
        current_rely = 1 * rel_step

        
        titles = self.schema.get('enum_titles', self.schema["enum"])

        for value, title in zip(self.schema["enum"], titles):
            rad_btn = ttk.Radiobutton(
                self._holder,
                text=title,
                value=value,
                variable=self.tkvar,
                command=play_switch
            )
            rad_btn.place(
                relx=0.5,
                rely=current_rely,
                anchor="sw")
            self.rad_btns[value] = rad_btn
            current_rely += rel_step
        
        self._holder.configure(relief="sunken", padding=2)

        self._label.place(relx=0.5, rely=int(0.5*current_rely), anchor="e")


    def _update_widgets_style(self):
        if self.status == 1:
            self._reset_background_color()
        else:
            self._highlight_background_color()

    def _highlight_background_color(self):
        val = self.get()
        for name, rad_btn in self.rad_btns.items():
            style = 'Highlighted.TRadiobutton' if name == val else 'TRadiobutton'
            rad_btn.configure(style=style)

    def _reset_background_color(self):
        for rad_btn in self.rad_btns.values():
            rad_btn.configure(style='TRadiobutton')


class _OTChoiceCombo(_OTChoiceAbstract):
    """OT choices widget."""

    def _create_widgets(self):
        options = self.schema.get('enum')
        self._pack_with_combobox(options)

    def _pack_with_combobox(self, option):
        """Combobox version of the widget"""

        self.combo = ttk.Combobox(
            self._holder,
            values=option,
            textvariable=self.tkvar,
            state='readonly',
            postcommand=play_switch)
        self.combo.place(relx=0.5, rely=1, anchor="sw")

    def _update_widgets_style(self):
        style = 'TCombobox' if self.status == 1 else 'Highlighted.TCombobox'
        self.combo.configure(style=style)


class OTFileBrowser(_LeafWidget):

    def __init__(self, schema, parent, name, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, parent, name, root_frame)

        self._filter = []
        self._isdirectory = False

        if 'ot_filter' in schema:
            filters = schema['ot_filter']
            if 'directory' in filters:
                self._isdirectory = True
            else:
                for ext in filters:
                    filetype = (f"{ext} files", f"*.{ext}")
                    self._filter.append(filetype)

    def _define_var(self):
        self.tkvar = StringVar()
        self.tkvar.trace('w', self.on_value_change)

    def _create_widgets(self):

        self._label.place(relx=0.5, rely=0.5, anchor="e")
        self._holder.config(height=2 * LINE_HEIGHT)

        self._entry = ttk.Entry(self._holder,
                                textvariable=self.tkvar,
                                state='disabled',
                                foreground='black',
                                justify="right")
        self._entry.place(relx=0.5, rely=0.5, relwidth=0.4, anchor="sw")

        self._scroll = ttk.Scrollbar(self._holder, orient="horizontal",   command=self.__scrollHandler)
        self._scroll.place(relx=0.5, rely=0.5, relwidth=0.4, anchor="nw")
        self._entry.configure(xscrollcommand=self._scroll.set)

        self._btn = ttk.Button(self._holder,
                               image=IMAGE_DICT['load'],
                               width=0.1 * WIDTH_UNIT,
                               compound='left',
                               style='clam.TLabel',
                               command=self._browse)

        self._btn.place(relx=0.9, rely=0.5, anchor="w")

    def __scrollHandler(self, *L):
        """Callback for entry scrollbar """
        op, howMany = L[0], L[1]
        if op == 'scroll':
            units = L[2]
            self._entry.xview_scroll(howMany, units)
        elif op == 'moveto':
            self._entry.xview_moveto(howMany)

    def _browse(self, event=None):
        """Browse directory or files."""
        cur_path = self.get()

        if self._isdirectory:
            path = filedialog.askdirectory(title=self.title)
        else:
            path = filedialog.askopenfilename(title=self.title,
                                              filetypes=self._filter)

        if path == "":
            return

        path = os.path.relpath(path)
        if path != cur_path:
            self.tkvar.set(path)

    def _update_widgets_style(self):
        style = 'TEntry' if self.status == 1 else 'Highlighted.TEntry'
        self._entry.configure(style=style)

    def get(self):
        return self.tkvar.get()

    def set(self, value):
        self.tkvar.set(value)


class _OTChoiceDynamic(_OTChoiceCombo):
    """This particular class is for choosing among a variable set of option
    
    Example: select a patch name among a list found in an external file
    """

    def set(self, value):
        """Reconfigure the options when set"""
        tree = Nob(self.my_root_tab_widget.get())
        key = self.schema["ot_dyn_choice"]
        options = tree[key][:]
        self._pack_with_combobox(options)
        super().set(value)



class OTDocu(_LeafWidget):

    def __init__(self, schema, parent, name, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, parent, name, root_frame)
        self.root = get_tkroot(root_frame)

        self._dialog = None

    def _define_var(self):
        # Toddo (ADN UHHHHHH?, pkoi une Tk var dans un texte de documentation?)
        self.tkvar = StringVar()
        self.tkvar.trace('w', self.on_value_change)

    def _create_widgets(self):
        self._btn = ttk.Button(self._holder,
                               width=0.01 * WIDTH_UNIT,
                               compound='center',
                               image=IMAGE_DICT['docu'],
                               style='clam.TLabel',
                               command=self._popup_dialog)
        self._btn.place(relx=0.9, rely=0.5, anchor="center")
        self._holder.pack_configure(side="bottom", fill="x")

    def _popup_dialog(self):
        """Display content of documentation string."""
        # TODO: need to be reviewed (but deprecated)
        self._dialog = Toplevel(self.root)
        self._dialog.transient(self.root)
        self._dialog.title('Documentation')
        self._dialog.grab_set()

        self._dialog.bind("<Control-w>", self._destroy_dialog)
        self._dialog.bind("<Escape>", self._destroy_dialog)
        self._dialog.protocol("WM_DELETE_WINDOW", self._destroy_dialog)

        dlg_frame = ttk.Frame(self._dialog,
                              width=3 * WIDTH_UNIT,
                              height=3 * WIDTH_UNIT)
        dlg_frame.pack(side="top", fill="both", expand=True)
        dlg_frame.grid_propagate(False)
        dlg_frame.grid_rowconfigure(0, weight=1)
        dlg_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(dlg_frame)
        scrollbar.pack(side='right', fill='y')

        text_wd = Text(
            dlg_frame,
            wrap='word',
            yscrollcommand=scrollbar.set,
            borderwidth=0.02 * WIDTH_UNIT,
            relief="sunken")

        # Example of formatting
        text_wd.tag_configure('bold', font=('Times', 14, 'normal'))
        text_wd.insert("end", self.tkvar.get(), 'bold')
        text_wd.config(state='disabled')
        text_wd.pack()
        scrollbar.config(command=text_wd.yview)

    def _destroy_dialog(self, event=None):
        """Destroying dialog."""
        self.root.focus_set()
        self._dialog.destroy()
        self._dialog = None

    def get(self):
        """Void return."""
        return self.tkvar.get()

    def set(self, value):
        """Set value to documentation content."""
        self.tkvar.set(value)


class OTDescription(_LeafWidget):

    def __init__(self, schema, parent, name, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, parent, name, root_frame)
        self._holder.pack_configure(side="bottom", fill="x")

    def _define_var(self):
        # Toddo (ADN UHHHHHH?, pkoi une Tk var dans un texte de documentation?)
        self.tkvar = StringVar()
        self.tkvar.trace('w', self.on_value_change)

    def _create_widgets(self):
        self._label.config(justify="left",
                           textvariable=self.tkvar,
                           wraplength=WIDTH_UNIT * 0.8)
        self._label.pack(side="bottom")

    def get(self):
        return self.tkvar.get()

    def set(self, value):
        self.tkvar.set(value)


class OTComment(_LeafWidget):

    def __init__(self, schema, parent, name, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        state = schema.get('state', 'normal')
        self.disabled = state == 'disabled'

        super().__init__(schema, parent, name, root_frame)

        self._holder.pack_configure(side="top", fill="x")

        self._holder.bind('<Enter>', self._unbind_global_scroll)
        self._holder.bind('<Leave>', self._bind_global_scroll)

    def _define_var(self):
        self.tkvar = StringVar()
        self.tkvar.trace('w', self.on_value_change)

    def _create_widgets(self):
        height = self.schema.get("height", 6)

        self.text_console = TextConsole(self._holder,
                                        self.tkvar,
                                        height=height,
                                        width=10,
                                        disabled=self.disabled)

    def _bind_global_scroll(self, *args):
        self._holder.event_generate('<<bind_global_scroll>>')

    def _unbind_global_scroll(self, *args):
        self._holder.event_generate('<<unbind_global_scroll>>')

    def get(self):
        return self.tkvar.get().rstrip()

    def set(self, value):
        self.text_console.set_text(value)  # variable gets set automatically

    def _update_widgets_style(self):
        if self.disabled:
            return

        bgcolor = 'white' if self.status == 1 else PARAMS['hl_bg']
        fgcolor = 'black' if self.status == 1 else PARAMS['bg_dark']
        self.text_console.configure(background=bgcolor)
        self.text_console.configure(foreground=fgcolor)


class OTEmpty(_LeafWidget):
    """OT widget for unimplemented types."""

    def _create_widgets(self):
        self.status = 0
        if self.schema.get("ot_type", None) != 'void':
            return

        info = []
        for item in ["name", "title", "type", "ot_type"]:
            if item in self.schema:
                info.append(f'{item} = {self.schema[item]}')

        self._label.configure(text="\n".join(info))
        self._label.pack(side="top", padx=2, pady=2)

        self._holder.forget()

    def get(self):
        return None

    def set(self, *args, **kwargs):
        pass


class _OTAbstractList(_LeafWidget, metaclass=abc.ABCMeta):
    """Class to handle LISTS
    
    In the memory a list is a Python Lists
    But for the GUI, the list containes subleaves with specific behavior
    We loose here the usual perfect mapping btw memory and GUI"""

    def _init_previous_value(self):
        self.previous_value = []

    def _create_widgets(self):
        self.entrylistholder = ttk.Frame(self._holder)
        self.entrylistholder.place(
            relwidth=0.5,
            relx=0.5,
            rely=0.0,
            anchor="nw"
        )
        self._configure_popup_menu()

    def _get_default(self):
        # TODO: simplify after defining variable

        # get value
        item_type = self.schema['items'].get('type')
        value = self.schema['items'].get('default', None)

        if value is None:
            # TODO: missing handling of bounded values
            # TODO: missing handling of string duplication
            type2val = {'string': '',
                        'number': 0.0,
                        'integer': 0}
            value[item_type] = type2val[item_type]

        # number of repeats
        n_reps = min(1, self.schema.get('maxItems', 1))
        n_reps = max(n_reps, self.schema.get('minItems', 1))

        return [value] * n_reps

    def _configure_popup_menu(self):
        self.popup_menu = Menu(self.entrylistholder, tearoff=False)  # binding in tv bindings

        self._add_popup_commands()

        self.entrylistholder.bind('<Enter>', self._activate_popup)
        self.entrylistholder.bind('<Leave>', self._deactivate_popup)

    @abc.abstractmethod
    def _add_popup_commands(self):
        pass

    def _activate_popup(self, *args):
        self.entrylistholder.bind_all("<Button-2>", self.on_right_click)

    def _deactivate_popup(self, *args):
        self.entrylistholder.unbind_all("<Button-2>")

    def on_right_click(self, event):
        self.popup_menu.tk_popup(event.x_root, event.y_root)

    def on_copy(self, *args):
        copy_str = ', '.join([str(value) for value in self.get()])
        root = get_tkroot(self._holder)
        root.clipboard_clear()
        root.clipboard_append(copy_str)

    def _resize_holder(self, n_lines):
        self._holder.config(height=n_lines * LINE_HEIGHT)


class _ListEntry(_LeafWidget):
    """The default SUBwidget entry for lists
    
    This is packed Inside an OTList."""

    def __init__(self, schema, parent, holder, previous_value=None):
        """Additions to _LeafWidget init """
        self._previous_value = previous_value
        self._holder = holder
        super().__init__(schema, parent, None, holder)

    ### VUE
    def _create_widgets(self):
        """REdefine WITHOUT recalling _create_widgets() from LeafWidget!"""
        
        self.entry = ttk.Entry(self._holder, textvariable=self.tkvar,
                               exportselection=False)
        self.entry.pack(side="top")

        self.entry.bind('<FocusIn>', self.on_entry_focus)

    def _update_widgets_style(self):
        """REdefine WITHOUT recalling _create_widgets() from LeafWidget!"""
        
        style = 'TEntry' if self.status == 1 else 'Highlighted.TEntry'
        self.entry.configure(style=style)
    
    def _get_status_error_msg(self):
        return f'Invalid input "{self.entry.get()}"'

    def on_entry_focus(self, event):
        """If user focus on a cell, 
        
        and cell is invalid, update List error message
        else make it void
        """
        if self.status == -1:
            self.parent._update_invalid_status_label(self._get_status_error_msg())
        else:
            self.parent._update_status_label()

    # TODO : AD simplify this stuff
    # We add code to remove a bahavior, this is a bad practice
    # Reader cannot rely on what they have read before
    # The MindLoad is just crazy man!
    def _create_common_leaf_widgets(self, *args):
        """Remove the usual creation of widgets"""
        pass

    ### MODEL
    @property
    def item_type(self):
        return self.schema['type']

    def _init_previous_value(self):
        self.previous_value = self._previous_value

    def str2type(self, value):
        """Strongly type the value entered by the user"""
        if self.item_type == 'number':
            return float(value)
        elif self.item_type == 'integer':
            return int(value)
        else:
            return str(value)

    def _define_var(self):
        # TODO: variable dependent on schema
        self.tkvar = Variable()
        self.tkvar.trace('w', self.on_value_change)

    def on_value_change(self, *args):
        """Callback if value change"""
        
        try:
            value = self.get()
            if self.previous_value == value:
                self.status = 1
            else:
                self.status = 0

        except GetException:
            self.status = -1
            self.parent._update_invalid_status_label(self._get_status_error_msg())



    ### CONTROL
    def get(self):
        """opentea GET method"""
        try:
            return self.str2type(self.tkvar.get())
        except ValueError:
            raise GetException()

    def set(self, value):
        """opentea SET method"""
        
        try:
            self.tkvar.set(self.str2type(value))
        except ValueError:
            raise SetException()


    def destroy(self):
        self._update_parent_status(1)  # to update variables in parent

        self.entry.destroy()


class OTDynamicList(_OTAbstractList):
    """List controlled by the user"""

    def __init__(self, schema, parent, name, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        parent: ???
        name: name to be added
        root_frame :  a Tk object were the widget will be grafted
        """
        self._status_invalid = 0
        self._status_temp = 0

        # TODO: any way to avoid having this special case?
        self.empty_widget = None

        # TODO: can this be removed?
        self.item_type = schema["items"]["type"]

        self.min_items = schema.get('minItems', float("-inf"))
        self.max_items = schema.get('maxItems', float("inf"))

        super().__init__(schema, parent, name, root_frame)
   
    ### Vue
    def _create_widgets(self):
        """Add more to _OTAbstractList._create_widgets"""
        super()._create_widgets()
        self._config_status_label()
        self._config_buttons()

    @property
    def resizable(self):
        """True if list can change size"""
        return self.min_items != self.max_items

    def _config_status_label(self):
        self._status_lbl = ttk.Label(
            self._holder, text="no status yet", style='Status.TLabel',
            compound='left')
        relx = 0.9 if self.resizable else 1.
        self._status_lbl.place(relx=relx, rely=1.0, anchor="se")

    def _config_buttons(self):
        """Initialise entry."""
        if not self.resizable:
            return

        self.additem_bt = ttk.Button(self._holder,
                                     text="+",
                                     command=self.on_add_item)
        self.delitem_bt = ttk.Button(self._holder,
                                     text="-",
                                     command=self.on_del_item)

        self.additem_bt.place(relwidth=0.05,
                              relx=0.95,
                              rely=1.0, anchor="se")
        self.delitem_bt.place(relwidth=0.05,
                              relx=1,
                              rely=1.0, anchor="se")

    def _add_popup_commands(self):
        """Re-define _OTAbstractList void method """
        self.popup_menu.add_command(label='Copy', command=self.on_copy)
        self.popup_menu.add_command(label='Paste', command=self.on_paste)

    def _resize_holder(self):
        """Adjust holder size to intern variable"""
        n_lines = max(2, 1 + len(self.variables))
        if self.resizable:
            n_lines += 0.5  # otherwise buttons overlap last entry
        super()._resize_holder(n_lines)

    def create_void_entry(self):
        """Add new entry to holder"""
        if self.empty_widget is not None:
            return

        label = ttk.Label(self.entrylistholder, text="void")
        label.pack(side="top")
        self.empty_widget = label


    def on_paste(self, *args):
        """Callback on paste"""
        try:
            paste_str = get_tkroot(self._holder).clipboard_get()
        except tkinter._tkinter.TclError:
            paste_str = ""

        if not paste_str:
            messagebox.showwarning(message='Nothing to paste')
            return

        paste_ls = [value.strip() for value in paste_str.split(',')]

        # validate clipboard
        # TODO: need to find alternative way to check clipboard (is_valid?)
        var = self.variables[0] if self.variables else _ListEntry(
            self, self.entrylistholder, self.item_type)
        for value in paste_ls:
            try:
                var.str2type(value)
            except ValueError:
                message = f"Invalid clipboard:\n'{paste_str}'"
                messagebox.showwarning(message=message)
                return

        # paste clipboard
        self.set(paste_ls)
    
    def on_add_item(self):
        """callback Add an item at the end of the array.
        """
        # TODO: can this be simplified based on new way of handling values?
        if len(self.variables) == self.max_items:
            return

        self._add_item()

    def on_del_item(self):
        """Callback Delete item at the end of the array.
        """
        if len(self.variables) == self.min_items:
            return

        self.remove_items(1)

    def _update_invalid_status_label(self, error_msg):
        self._status_lbl.config(
            text=error_msg,
            image=IMAGE_DICT['invalid'])

    def _update_status_label(self):
        n_err = self._get_number_of_errors()
        if n_err == 0:
            self._status_lbl.config(text='', image='')
        else:
            error_msg = f'Contains {n_err} invalid input(s)'
            self._update_invalid_status_label(error_msg)

    ### Model

    def _define_var(self):
        self.variables = []

    def _get_status(self):
        """Return status ID"""
        if self._status_invalid:
            return -1

        if self._status_temp or not self._check_previous_value():
            return 0

        return 1

    def _check_previous_value(self):
        """ True if content of memory equals to previous values"""
        values = self.get()

        if len(self.previous_value) != len(values):
            return False

        for val, cmp_val in zip(self.previous_value, values):
            if val != cmp_val:
                return False

        return True

    # TODO : unsure what this does
    def clear_empty_widget(self):
        """Remove empty widget"""
        if self.empty_widget is None:
            return

        self.empty_widget.destroy()
        self.empty_widget = None

    def _get_previous_item_value(self, index):
        """Return previous value of one list entry"""
        try:
            return self.previous_value[index]
        except IndexError:
            return None

    def _add_item(self, value=None):
        """Add an item internally"""
        # TODO: change on add item to get None

        previous_value = self._get_previous_item_value(len(self.variables))
        new_entry = _ListEntry(self.schema['items'], self, self.entrylistholder,
                               previous_value)
        if value is not None:
            new_entry.set(value)

        self.clear_empty_widget()
        self._resize_holder()

    def remove_items(self, n_items=None):
        """Delete some items
        
        del all items if n_items is None"""

        if not self.variables:
            return

        if n_items is None:
            n_items = len(self.variables)

        i = 0
        while i < n_items:
            var = self.variables.pop()
            var.destroy()
            i += 1

        self._resize_holder()

        if len(self.variables) == 0:
            self.create_void_entry()

    def _get_number_of_errors(self):
        """Hem, remove_items is nb of errors"""
        return self._status_invalid

    def on_update_status(self):
        """Callback if status is updated
        
        WARNING: trigger deppendency setter"""
        self._update_status_label()

        if self.status != -1:
            self.set_slaves(self.get())

    def add_child(self, child):
        """New child to list"""
        self.variables.append(child)

    ### Controls
    def set(self, values):
        """Opentea SET method"""
        n_set_elems = len(values)
        if n_set_elems < self.min_items:
            for _ in range(self.min_items - n_set_elems):
                values.append(None)  # will use default

        elif n_set_elems > self.max_items:
            values = values[:self.max_items]

        n_set_elems = len(values)
        n_vars = len(self.variables)


        # TODO : simplify this following update in 3 steps
        # Doing like this may leave some history
        # Prefer delete all then recreate some

        # delete excess items
        if n_vars > n_set_elems:
            n_del = n_vars - n_set_elems
            self.remove_items(n_del)

        # update existing
        for variable, value in zip(self.variables, values):
            variable.set(value)

        # create new
        for i in range(n_vars, n_set_elems):
            self._add_item(values[i])

    def get(self):
        """Opentea GET method"""
        
        return [var.get() for var in self.variables]

    def validate(self):
        """Opentea VALIDATE method"""
        
        if self.status != 0:
            return

        self.previous_value = self.get()

        for var in self.variables:
            var.status = 1

        self.validate_slaves()



class OTStaticList(_OTAbstractList):
    """List NOT controlled bby the user
    
    created if ot_require or disabled"""
    
    ### Vue 
    def _configure_listbox(self):
        """Packing elements"""
        nlines = 6
        self._resize_holder(nlines)

        scrollbar = ttk.Scrollbar(self.entrylistholder, orient='vertical')

        self.lbx = Listbox(
            self.entrylistholder,
            height=nlines,
            yscrollcommand=scrollbar.set)
        self.lbx.configure(
            state="disabled",
            highlightbackground=PARAMS["bg"],
            background=PARAMS["bg"],
            disabledforeground=PARAMS["bg_dark"])

        scrollbar.config(command=self.lbx.yview)
        scrollbar.pack(side='right', fill='y')
        self.lbx.pack(side="top", fill="both", pady=2)
        self.lbx.bind('<Enter>', self._unbind_global_scroll)
        self.lbx.bind('<Leave>', self._bind_global_scroll)

    def _bind_global_scroll(self, *args):
        """Enable scroll if pointer in widget"""
        self.lbx.event_generate('<<bind_global_scroll>>')

    def _unbind_global_scroll(self, *args):
        """Disable scroll if pointer in widget"""
        self.lbx.event_generate('<<unbind_global_scroll>>')

    def _update_listbox(self):
        """Change appearence according to internal variable"""
        self.lbx.configure(state="normal")

        self.lbx.delete(0, 'end')
        for item in self.variable:
            self.lbx.insert("end", item)

        self.lbx.configure(state="disabled")

    ### Model
    def _define_var(self):
        self._variable = []

    def _create_widgets(self):
        """Add to _create_widgets"""
        super()._create_widgets()
        self._configure_listbox()

    @property
    def variable(self):
        return self._variable

    @variable.setter
    def variable(self, values):
        """Add additional behavior to the setter of variable"""
        self.status = int(self._compare_previous(values))

        self._variable = values
        self._update_listbox()
        self.set_slaves(values)

    def _compare_previous(self, values):
        """True if values identical to previous values"""
        if len(values) != len(self.previous_value):
            return False
        for val, new_val in zip(self.previous_value, values):
            if val != new_val:
                return False
        return True


    def _add_popup_commands(self):
        """Re-define _OTAbstractList void method """
        self.popup_menu.add_command(label='Copy', command=self.on_copy)


    def on_update_status(self):
        """Callback if status is updated
        
        WARNING: trigger deppendency setter"""
        #self._update_status_label()
        if self.status != -1:
            self.set_slaves(self.get())

    ### Control
    def get(self):
        """Opentea GET method"""
        return self.variable

    def set(self, value):
        """Opentea SET method
        By assigning we trigger the variable __setter__ 
        """
        self.variable = list(value)

    def validate(self):
        if self.status != 0:
            return

        self.previous_value = self.get()
        self.status = 1
        self.validate_slaves()
