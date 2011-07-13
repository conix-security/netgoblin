#!/usr/bin/python
# coding: utf8



#+---------------------------------------------- 
#| Global Imports
#+----------------------------------------------
import gtk
import pango
import gobject
import re
import pygtk
import logging

pygtk.require('2.0')

#+---------------------------------------------- 
#| Local Imports
#+----------------------------------------------
from ..Common import ConfigurationParser
from ..Sequencing.TreeViews import TreeGroupGenerator

#+---------------------------------------------- 
#| Configuration of the logger
#+----------------------------------------------
loggingFilePath = ConfigurationParser.ConfigurationParser().get("logging", "path")
logging.config.fileConfig(loggingFilePath)


#+---------------------------------------------- 
#| UIDumpingMessage :
#|     GUI for message dumping process
#| @author     : {gbt,fgy}@amossys.fr
#| @version    : 0.2
#+---------------------------------------------- 
class UIDumpingMessage:

    
    #+---------------------------------------------- 
    #| Called when user select a new trace
    #+----------------------------------------------
    def new(self):
        pass

    def update(self):
        pass
    
    def clear(self):
        pass

    def kill(self):
        pass
    
    #+---------------------------------------------- 
    #| updateGroups :
    #|  update the content of the UI with new groups
    #| @param groups: list of all groups 
    #+----------------------------------------------   
    def updateGoups(self, groups):
        self.groups = groups
        self.treeGroupGenerator.groups = self.groups
        self.treeGroupGenerator.default()       
        
        
    #+---------------------------------------------- 
    #| Constructor :
    #| @param groups: list of all groups 
    #+----------------------------------------------   
    def __init__(self, zob):
        # create logger with the given configuration
        self.log = logging.getLogger('netzob.Dumping.UIDumpingMessage.py')
        self.log.debug("Starting the UI Dumping GUI")
        
        self.groups = []
        self.selectedGroup = None
        
        
        # First we create an VPaned which hosts the two main children
        self.panel = gtk.VPaned()        
        self.panel.show()
        
        # Creation of the two children
        self.box_top = gtk.HBox(False, spacing=0)
        self.box_content = gtk.HBox(False, spacing=0)
        
        # includes the two children
        self.panel.add(self.box_top)
        self.panel.add(self.box_content)

        self.box_top.set_size_request(-1, -1)
        self.box_content.set_size_request(-1, -1)

        self.box_top.show()
        self.box_content.show()
        
#        # Create the top hbox content
#        self.topFrame = gtk.Frame()
#        self.topFrame.show()
#        self.box_top.add(self.topFrame)
        
        # Create the treeview
        self.treeGroupGenerator = TreeGroupGenerator.TreeGroupGenerator(self.groups)
        self.treeGroupGenerator.initialization()
        self.box_top.pack_start(self.treeGroupGenerator.getScrollLib(), True, True, 0)
        self.treeGroupGenerator.getTreeview().connect("cursor-changed", self.groupSelected) 
        
        
        # Create the content hbox content
        self.bottomFrame = gtk.Frame()
        self.bottomFrame.show()
        self.box_content.add(self.bottomFrame)
        
        # Insert the textarea in a scolledWindow in the content box
        sw = gtk.ScrolledWindow()
        self.textarea = gtk.TextView()
        self.textarea.show()
        self.textarea.set_editable(False)
        sw.add(self.textarea)
        sw.show()
        self.bottomFrame.add(sw)

    def groupSelected(self, treeview):
        (modele, iter) = treeview.get_selection().get_selected()
        if(iter):
            if(modele.iter_is_valid(iter)):
                idGroup = modele.get_value(iter, 0)
                self.selectedGroup = idGroup
                self.updateTextArea()
                

    def updateTextArea(self):
        if self.selectedGroup == None :
            self.log.debug("No selected group")
            self.textarea.get_buffer().set_text("Select a group to see its XML definition")

        else :
            found = False
            for group in self.groups :
                if str(group.getID()) == self.selectedGroup :
                    self.textarea.get_buffer().set_text(group.getXMLDefinition())
                    found = True
            if found == False :
                self.log.warning("Impossible to retrieve the group having the id {0}".format(str(self.selectedGroup)))
                