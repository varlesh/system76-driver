#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Main frontend - Legacy GTK2 Version

import os
import sys
import time
import gobject
import restore
import model
import system
import drivers
import ubuntuversion
import detect
import getpass

try:
     import pygtk
     pygtk.require("2.0")
except:
      pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
SYS76LOGO_IMAGE = os.path.join(IMAGEDIR, 'logo.png')
SYS76SQUARE_LOGO = os.path.join(IMAGEDIR, 'logoSQUARE.png')
WINDOW_ICON = os.path.join(IMAGEDIR, '76icon.svg')

class aboutDlg:
    """Shows the about dialog box"""

    def __init__(self, datadir):
        #setup the glade file
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'aboutDialog')

    def run(self):
        """Loads the about Dialog"""
        self.dlg = self.wTree.get_widget("aboutDialog")
        self.square_logo = gtk.gdk.pixbuf_new_from_file(os.path.join(SYS76SQUARE_LOGO))
        self.icon = gtk.gdk.pixbuf_new_from_file(os.path.join(WINDOW_ICON))
        self.dlg.set_logo(self.square_logo)
        self.dlg.set_icon(self.icon)
        self.dlg.set_version(ubuntuversion.driver())
        
        #run the dialog      
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()
        
class aptErrorDlg:
    """Shows another package manager running dialog"""
    
    def __init__(self, datadir):
        #setup the glade file
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'aptRunning')
        
    def run(self):
        """Loads the apt running Dialog"""
        self.dlg = self.wTree.get_widget("aptRunning")
        self.icon = gtk.gdk.pixbuf_new_from_file(os.path.join(WINDOW_ICON))
        self.dlg.set_icon(self.icon)
        
        #run the dialog      
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()
        
class archiveCreated:
    """Shows archive created dialog"""
    
    def __init__(self, datadir):
        #setup the glade file
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'logArchiveCreated')
        
    def run(self):
        """Loads the archive created Dialog"""
        self.dlg = self.wTree.get_widget("logArchiveCreated")
        self.icon = gtk.gdk.pixbuf_new_from_file(os.path.join(WINDOW_ICON))
        self.dlg.set_icon(self.icon)
        
        #run the dialog      
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()
        
class connectDlg:
    """Shows no connection dialog"""
    
    def __init__(self, datadir):
        #setup the glade file
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'noConnection')
        
    def run(self):
        """Loads the no connection Dialog"""
        self.dlg = self.wTree.get_widget("noConnection")
        self.icon = gtk.gdk.pixbuf_new_from_file(os.path.join(WINDOW_ICON))
        self.dlg.set_icon(self.icon)
        
        #run the dialog      
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()

def supported(datadir):
    """
    This function will determine System76 and Ubuntu
    Version support and run appropriate functions
    """
    modelname = model.determine_model()
    version = ubuntuversion.release()
    
    if version == ('8.04.1'):
        version = '8.04'
    
    if version != '6.06' and version != '6.10' and version != '7.04' and version != '7.10' and version != '8.04' and version != '8.10' and version != '9.04' and version != '9.10' and version != '10.04' and version != '10.10' and version != '11.04':
        notsupported = unsupported(datadir);
        notsupported.run()
    elif modelname == ('nonsystem76'):
        notsupported = unsupported(datadir);
        notsupported.run()
    else:
        ui = System76Driver(datadir)
        ui.run()

class System76Driver:
    """This is the System76Driver application"""

    def __init__(self, datadir):
        
    #Set directory
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'mainWindow')

        #load logos
        self.system76logo = gtk.gdk.pixbuf_new_from_file(os.path.join(SYS76LOGO_IMAGE))
        self.wTree.get_widget('system76logo').set_from_pixbuf(self.system76logo)
        self.icon = gtk.gdk.pixbuf_new_from_file(os.path.join(WINDOW_ICON))
        self.wTree.get_widget('mainWindow').set_icon(self.icon)

        #Grab our widgets
        self.sysName = self.wTree.get_widget("sysName")
        self.sysModel = self.wTree.get_widget("sysModel")
        self.sysProcessor = self.wTree.get_widget("sysProcessor")
        self.sysMemory = self.wTree.get_widget("sysMemory")
        self.sysHardDrive = self.wTree.get_widget("sysHardDrive")

        #Create our dictionary and connect it
        dic = {"on_mainWindow_destroy" : gtk.main_quit
                , "on_about_clicked" : self.on_about_clicked
                , "on_close_clicked" : gtk.main_quit
                , "on_create_clicked" : self.on_create_clicked
                , "on_driverInstall_clicked" : self.on_driverInstall_clicked
                , "on_restore_clicked" : self.on_restore_clicked}
        self.wTree.signal_autoconnect(dic)
        
        #Grab the data
        modelname = model.determine_model()
        systemname = system.name()
        
        #Change the labels
        self.sysName.set_label(systemname)
        self.sysModel.set_label(modelname)
        
    def on_about_clicked(self, widget):
    
        #Calls aboutDlg class to display dialog
        aboutDialog = aboutDlg(datadir);
        aboutDialog.run()
        
    def on_create_clicked(self, widget):
        
        #Creates an archive of common support files and logs
        
        username = getpass.getuser()
        
        today = time.strftime('%Y%m%d_h%Hm%Ms%S')
        modelname = model.determine_model()
        version = ubuntuversion.release()
        
        os.mkdir('/tmp/system_logs_%s' % today)
        TARGETDIR = '/tmp/system_logs_%s' % today
        
        fileObject = file('/tmp/system_logs_%s/systeminfo.txt' % today, 'wt')
        fileObject.write('System76 Model: %s\n' % modelname)
        fileObject.write('OS Version: %s\n' % version)
        fileObject.close()
        os.system('sudo dmidecode > %s/dmidecode' % TARGETDIR)
        os.system('lspci -vv > %s/lspci' % TARGETDIR)
        os.system('sudo lsusb -vv > %s/lsusb' % TARGETDIR)
        os.system('cp /etc/X11/xorg.conf %s/' % TARGETDIR)
        os.system('cp /etc/default/acpi-support %s/' % TARGETDIR)
        os.system('cp /var/log/daemon.log %s/' % TARGETDIR)
        os.system('cp /var/log/dmesg %s/' % TARGETDIR)
        os.system('cp /var/log/messages %s/' % TARGETDIR)
        os.system('cp /var/log/syslog %s/' % TARGETDIR)
        os.system('cp /var/log/Xorg.0.log %s/' % TARGETDIR)
        os.system('tar -zcvf logs.tar %s/' % TARGETDIR)
        os.system('cp logs.tar /home/%s/' % username)
        
        archiveCreatedDialog = archiveCreated(datadir);
        archiveCreatedDialog.run()

    def on_driverInstall_clicked(self, widget):
        
        #Check if another package manager is running
        aptrunning = detect.aptcheck()
        
        #Grab internet connection test
        connection = detect.connectivityCheck()
        
        #Calls drivers module when user clicks Driver Install button
        if connection == "noConnectionExists":
            notConnected = connectDlg(datadir);
            notConnected.run()
        elif aptrunning == "running":
            aptError = aptErrorDlg(datadir);
            aptError.run()
        else:
            drivers.start()

    def on_restore_clicked(self, widget):
        
        #Check if another package manager is running
        aptrunning = detect.aptcheck()
        
        #Grab internet connection test
        connection = detect.connectivityCheck()
        
        #Calls restore module when user clicks Restore button
        if connection == "noConnectionExists":
            notConnected = connectDlg(datadir);
            notConnected.run()
        elif aptrunning == "running":
            aptError = aptErrorDlg(datadir);
            aptError.run()
        else:
            restore.start()

    def run(self):
        gtk.main()
        
class unsupported:
    """Shows the Unsupported dialog box"""

    def __init__(self, datadir):
        #setup the glade file
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'unsupported')

    def run(self):
        """Loads the unsupported Dialog"""
        self.dlg = self.wTree.get_widget("unsupported")
        
        #run the dialog      
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()

if __name__ == "__main__":
    datadir = os.path.join(os.path.dirname(__file__),'.')
    supported(datadir)
