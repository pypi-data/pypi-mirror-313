
from __future__ import annotations #Needed to use same type as the enclosing class in typing
import abc

from opentea.gui_forms._exceptions import GetException

class OTTreeElement(metaclass=abc.ABCMeta):
    """The common aspect btw nodeWidgets and treeWidgets"""
    def __init__(self, schema: dict, parent:OTTreeElement, name: dict):
        self.schema = schema
        self.parent = parent
        self.name = name

        self.children = dict() 
        # Contains 
        # { 
        #     child_name : child_node,
        #     child_name2 : child_node2,
        #     child_name3 : child_node3,
        # }
        
        # When you create the element, it adds itself to its parent familly
        self.parent.add_child(self)
        self.my_root_tab_widget = parent.my_root_tab_widget
        # This must precede _handle_dependency()
 
        # Dependencies elements (flags ot_require)
        self.slaves = []
        self.master = None
        self.dependent = self._handle_dependency()   # AD :  WTF, does not look healthy
        
        # THE STATUS (loads of work to sort this out)
        self._status = None

    ####################
    # Status handling "a la Luis"
    # TODO : ADN, est ce qu'on a vraiment besoin de properties et getters ici?
    ##################
    @property
    def status(self) -> int:
        """Return status as a property"""
        return self._get_status()

    @status.setter
    def status(self, status)-> int:
        """Update the status"""
        return self._set_status(status)

    def _get_status(self)-> int:
        """private to return status"""
        return self._status

    def _set_status(self, status):
        """private to update status
        
        BUT, parents also are updated!!! 
        Recusively giong up into parents
        """
        self._update_parent_status(status)
        # if status == self._status:
        #     return # Shortcut if status has not changed
        # CAVEAT ADN :  ca ne marche pas comme prevu
        # si on fait ca les status ne sont plus propagés dans l'IHM
        self._status = status
        self.on_update_status()

    def _update_parent_status(self, status: int):
        """Change the status of ancestors
        
        I still do not get why we must count the invalid and temps

        WARNING: this recursivity is not infinite because
        root parent redefines the status property!!!
        
        """
        if status == -1:
            self.parent._status_invalid += 1
        elif status == 0:
            self.parent._status_temp += 1

        if self._status == -1:
            self.parent._status_invalid -= 1
        elif self._status == 0:
            self.parent._status_temp -= 1

        self.parent.status = self.parent.status
    ############################

    ############################
    # SCHEMA proxys
    @property
    def properties(self):
        """Return the properties of schema"""
        return self.schema.get("properties", [])

    @property
    def _type(self):
        """Retrun the type of the schema"""
        return self.schema['type']
    ############################
    
    def add_child(self, child):
        """How to add a children to the element
        
        initially one could thik this is limited to nodes, but here the catch:
        present here because complex leaves like lists can have whild widgets"""
        self.children[child.name] = child



    @abc.abstractmethod
    def get(self):
        """What to do when a value must be retreived from a widget"""
        pass

    @abc.abstractmethod
    def set(self, value):
        """What to do when a value must be stored in a widget"""
        if value == self.get(): #There should be this at all "def set():""
            return
        pass

    def _handle_dependency(self):
        """Configure for a dependency. Element is the slave in this case"""
        if 'ot_require' not in self.schema:
            return False

        master_name = self.schema.get('ot_require')
        self.my_root_tab_widget.add_dependency(master_name, self)

        return True

    def _add_dependent(self, slave, data=None):
        """
        Addition of one dependency


        Add object slave to list of dependent slaves
        state to object who the master is
        ask for a set() of the slave according to data
        """
        self.slaves.append(slave)
        slave.master = self

        if data is not None:
            slave.set(data)

    def add_dependents(self, slaves):
        """
        Add all slaves , PLUS set data to these slaves
        """
        try:
            data = self.get()
        except GetException:
            data = None

        for slave in slaves:
            self._add_dependent(slave, data)

    
    def set_slaves(self, value):
        """Trigger a set() in each slave"""
        for slave in self.slaves:
            slave.set(value)

    def _reset_master(self):
        """Used in case of destroy() method"""
        if self.master is None:
            return
        self.master.slaves.remove(self)
        self.master = None

    def get_child_by_name(self, name: str) -> OTTreeElement:
        """Recursive method to find a child in the tree
        
        Used for the declaration of dependencies in otroot.
        """
        # check if child is at this level
        for child in self.children.values():
            if child.name == name:
                return child

        # check children
        for child in self.children.values():
            child_ = child.get_child_by_name(name)

            if child_ is not None:
                return child_

        return None

    def on_update_status(self):
        """Additional operations to perform when updating status.

        Redefined in XOR, Multiples , and Tabs,
        Redefined in Leaves
        """
        pass

    @abc.abstractmethod
    def validate(self):
        """This action is usually recursive when Redefined
        
        This is the validate action of a tab.
        
        By default nothing happen!!!"""

        pass
        
    def validate_children(self):
        """Asks for validation of children"""
        for child in self.children.values():
            child.validate()
    
    def validate_slaves(self):
        """Asks for validation of slaves"""
        for slave in self.slaves:
            slave.validate()
