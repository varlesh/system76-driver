#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Fixes Suspend and Hibernate on System76 machines
import os
import fileinput
import time
import ubuntuversion

today = time.strftime('%Y%m%d_h%Hm%Ms%S')

class acpi1():
    def install(self):
        
        """Configures S1 sleep"""
        os.system('sudo cp /etc/default/acpi-support /etc/default/acpi-support_sys76backup_%s' % today)
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/acpi-support /etc/default/acpi-support')
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/89-brightup.sh /etc/acpi/resume.d/89-brightup.sh')
        os.system('sudo cp /etc/acpi/resume.d/60-asus-wireless-led.sh /etc/acpi/resume.d/60-asus-wireless-led.sh_sys76backup_%s' % today)
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/60-asus-wireless-led.sh /etc/acpi/resume.d/60-asus-wireless-led.sh')
        
    def describe(self):
        return "Suspend configuration"
    
class acpi2():
    def install(self):
        
        """Configures S3 sleep"""
        os.system('sudo cp /etc/default/acpi-support /etc/default/acpi-support_sys76backup_%s' % today)
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/gazv3/acpi-support /etc/default/acpi-support')
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/89-brightup.sh /etc/acpi/resume.d/89-brightup.sh')
        os.system('sudo cp /etc/acpi/resume.d/60-asus-wireless-led.sh /etc/acpi/resume.d/60-asus-wireless-led.sh_sys76backup_%s' % today)
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/60-asus-wireless-led.sh /etc/acpi/resume.d/60-asus-wireless-led.sh')
    
    def describe(self):
        return "Suspend configuration"
    
class acpi3():
    def install(self):
        
        """Configures S1 sleep on Ubuntu 7.10"""
        os.system('sudo cp /etc/default/acpi-support /etc/default/acpi-support_sys76backup_%s' % today)
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/gutsy/acpi-support /etc/default/acpi-support')
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/89-brightup.sh /etc/acpi/resume.d/89-brightup.sh')
        os.system('sudo cp /etc/acpi/resume.d/60-asus-wireless-led.sh /etc/acpi/resume.d/60-asus-wireless-led.sh_sys76backup_%s' % today)
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/60-asus-wireless-led.sh /etc/acpi/resume.d/60-asus-wireless-led.sh')
    
    def describe(self):
        return "Suspend configuration"

class acpi4():
    def install(self):
        
        """Removes script used to temporarily fix Suspend with DRM on daru3
        Bug was fixed in Ubuntu"""
        os.system('sudo rm /etc/pm/sleep.d/00CPU')
        
    def describe(self):
        return "Remove old suspend configuration"
    
class daru2():
    def install(self):
        
        """Fix dsdt tables in daru2"""
        
        # Determine running kernel version
        b = os.popen('uname -r')
        try:
            uname = b.readline().strip()
        finally:
            b.close()
        kernel = uname
        
        os.system('sudo sh /opt/system76/system76-driver/src/acpi/initrd-add-dsdt.sh /boot/initrd.img-%s /opt/system76/system76-driver/src/acpi/daru2/DSDT.aml' % kernel)
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/daru2/DSDT.aml /etc/initramfs-tools/DSDT.aml')
        
        '''The ec_intr=0 option passes the embedded controller interupt
        to the kernel at boot.  On Ubuntu 7.10 the option fixes acpi
        battery notification problems.'''
        
        os.system('sudo cp /boot/grub/menu.lst /boot/grub/menu.lst_sys76backup_%s' % today)
        
        grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
        for line in grub_menu:
            print line.replace(' ec_intr=0',''),
        grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
        for line in grub_menu:
            print line.replace('splash','splash ec_intr=0'),
        
    def describe(self):
        return "DSDT table for DarU2"
        
class osiNotWindows():
    def install(self):
        
        # Kernel parameter tells the BIOS that the system is not Windows 2006
        
        os.system('sudo cp /boot/grub/menu.lst /boot/grub/menu.lst_sys76backup_%s' % today)
        
        grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
        for line in grub_menu:
            print line.replace(' acpi_osi="!Windows 2006"',''),
        grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
        for line in grub_menu:
            print line.replace('splash','splash acpi_osi="!Windows 2006"'),
    
    def describe(self):
        return "Linux BIOS descripton"
            
class lemu1():
    def install(self):
        
        # Kernel parameter tells the BIOS that the OS is Linux
        
        os.system('sudo cp /etc/default/grub /etc/default/grub_sys76backup_%s' % today)
        
        grub_menu = fileinput.input('/etc/default/grub', inplace=1)
        for line in grub_menu:
            print line.replace(' acpi_os_name=Linux acpi_osi=',''),
        grub_menu = fileinput.input('/etc/default/grub', inplace=1)
        for line in grub_menu:
            print line.replace('splash','splash acpi_os_name=Linux acpi_osi='),
        os.system('sudo update-grub')
    
    def describe(self):
        return "Linux BIOS descroption"
    
class os_linux():
    def install(self):
        
        # Kernel parameter tells the BIOS that the OS is Linux
        
        os.system('sudo cp /etc/default/grub /etc/default/grub_sys76backup_%s' % today)
        
        grub_menu = fileinput.input('/etc/default/grub', inplace=1)
        for line in grub_menu:
            print line.replace(' acpi_os_name=Linux acpi_osi=Linux',''),
        grub_menu = fileinput.input('/etc/default/grub', inplace=1)
        for line in grub_menu:
            print line.replace('splash','splash acpi_os_name=Linux acpi_osi=Linux'),
        os.system('sudo update-grub')
    
    def describe(self):
        return "Linux BIOS description"
        
class star1():
    def install(self):
        
        # Fix pciehp for SD card reader
        version = ubuntuversion.release()
        
        if version == ('9.04'):
            os.system('sudo cp /boot/grub/menu.lst /boot/grub/menu.lst_sys76backup_%s' % today)
            
            grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
            for line in grub_menu:
                print line.replace(' pciehp.pciehp_force=1',''),
            grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
            for line in grub_menu:
                print line.replace('splash','splash pciehp.pciehp_force=1'),
        elif version == ('9.10'):
            os.system('sudo cp /etc/default/grub /etc/default/grub_sys76backup_%s' % today)
            
            grub_menu = fileinput.input('/etc/default/grub', inplace=1)
            for line in grub_menu:
                print line.replace(' pciehp.pciehp_force=1',''),
            grub_menu = fileinput.input('/etc/default/grub', inplace=1)
            for line in grub_menu:
                print line.replace('splash','splash pciehp.pciehp_force=1'),
            os.system('sudo update-grub')
        elif version == ('10.04'):
            os.system('sudo cp /etc/default/grub /etc/default/grub_sys76backup_%s' % today)
            
            grub_menu = fileinput.input('/etc/default/grub', inplace=1)
            for line in grub_menu:
                print line.replace(' pciehp.pciehp_force=1',''),
            grub_menu = fileinput.input('/etc/default/grub', inplace=1)
            for line in grub_menu:
                print line.replace('splash','splash pciehp.pciehp_force=1'),
            os.system('sudo update-grub')
    
    def describe(self):
        return "Star1 card reader driver"
        
class star2():
    def install(self):
        """Fix Synaptic touchpad wakeup after resume from suspend"""
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/70_star2_touchpad /etc/pm/sleep.d/70_star2_touchpad')
        os.system('sudo chmod +x /etc/pm/sleep.d/70_star2_touchpad')
        
    def describe(self):
        return "Synaptic Trackpad suspend fix"
    
class sdCardBug():
    def install(self):
        
        """Fix suspend when a SD card is inserted - removes sd card related modules before suspend"""
        os.system('sudo rm /etc/pm/config.d/suspend_modules')
        os.system('echo "SUSPEND_MODULES=\"sdhci sdhci_pci\"" | sudo tee -a /etc/pm/config.d/suspend_modules')
        os.system('sudo chmod +x /etc/pm/config.d/suspend_modules')
        
    def describe(self):
        return "SD card reader suspend fix"
    
class xhcihcdModule():
    def install(self):
        """Unload the NEC USB 3.0 module prior to suspend"""
        os.system('sudo rm /etc/pm/config.d/suspend_modules')
        os.system('echo "SUSPEND_MODULES=\"xhci-hcd\"" | sudo tee -a /etc/pm/config.d/suspend_modules')
        os.system('sudo chmod +x /etc/pm/config.d/suspend_modules')
        
    def describe(self):
        return "USB 3 suspend fix"
    
class pcie_aspm():
    def install(self):
        
        """Fix ethernet and freezes when AC is unplugged and replugged
        while ethernet is plugged in. Caused by PCIe ASPM."""
        
        os.system('sudo cp /etc/default/grub /etc/default/grub_sys76backup_%s' % today)
        
        grub_menu = fileinput.input('/etc/default/grub', inplace=1)
        for line in grub_menu:
            print line.replace(' pcie_aspm=off',''),
        grub_menu = fileinput.input('/etc/default/grub', inplace=1)
        for line in grub_menu:
            print line.replace('splash','splash pcie_aspm=off'),
        os.system('sudo update-grub')
    
    def describe(self):
        return "Ethernet instability fixes"
    