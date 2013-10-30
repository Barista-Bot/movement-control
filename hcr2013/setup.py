#!/usr/bin/env python
#
# Copyright (c) 2012, 2013 Miguel Sarabia del Castillo
# Imperial College London
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
import os
import subprocess
import inspect
import pwd
import shutil
import stat
import dbus
import uuid
import urllib2

# CONSTANTS
#===============================================================================
VERSION = "0.30"

PACKAGE_LIST = [
    "openjdk-7-jdk",
    "doxygen",
    "autotools-dev",
    "build-essential",
    "cmake",
    "cmake-qt-gui",
    "cpp",
    "libboost-all-dev", 
    "subversion",
    "git-core",
    "mercurial",
    "ros-hydro-desktop-full",
    "ros-hydro-opencv2",
    "ros-hydro-joystick-drivers",
    "ros-hydro-hokuyo-node",
    "ros-hydro-sicktoolbox",
    "ros-hydro-openni*",
    "ros-hydro-p2os*",
    "ros-hydro-stage-ros",
    "ros-hydro-pocketsphinx",
    "ros-hydro-audio-common",
    "python-pygame",
    "python-scipy " ,
    "python-numpy",
    "openssh-server",
    "meld",
    "qtcreator",
    "eclipse",
    "libeigen3-dev",
    "icub" ]

JOYSTICK_UDEV = 'KERNEL=="js?", SUBSYSTEM=="input", ATTRS{name}=="DragonRise Inc.   Generic   USB  Joystick  ", MODE="666"\n'

HOKUYO_UDEV = 'KERNEL=="ttyACM*", SUBSYSTEM=="tty", ATTRS{product}=="URG-Series USB Driver", MODE="777"\n'

PIONEER_UDEV  = 'KERNEL=="ttyUSB*", SUBSYSTEM=="tty", ATTRS{product}=="USB HS SERIAL CONVERTER", MODE="777"\n'

PUB_KEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDEi+WaG3lccZV7I98X6SRwbl3/BeRUaFfudx8VCh/7hUnU6VesWayZhwbWM11HNBViLetmsxbSvgOwLorL1Dcuozn/+gw/+CMrFSsdt9EBYm/Pinew8H8SzBNyj/PNtcAGVF4gYIoaO/JQjaTXjKmoj7vE9AnwCT5ROUXXwjI1lv1BT2F+GB5W0tMesAG6qU5aRUn4F17855Raz2kChEfZxfOKMgwYygGIWqDJK5DEz88snWNvYtrafRSQrQFha+y0+EQ3y8nFbnAytqtUe40R6ik5j25soKTBRof68Qq39WxLye4G31lZZWrH+F6ZcvDJeuh8E96uwe8xQnvbx33h human@prlsummerschool'

PRIV_KEY = r"""-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAxIvlmht5XHGVeyPfF+kkcG5d/wXkVGhX7ncfFQof+4VJ1OlX
rFmsmYcG1jNdRzQVYi3rZrMW0r4DsC6Ky9Q3LqM5//oMP/gjKxUrHbfRAWJvz4p3
sPB/EswTco/zzbXABlReIGCKGjvyUI2k14ypqI+7xPQJ8Ak+UTlF18IyNZb9QU9h
fhgeVtLTHrABuqlOWkVJ+Bde/OeUWs9pAoRH2cXzijIMGMoBiFqgySuQxM/PLJ1j
b2La2n0UkK0BYWvstPhEN8vJxW5wMrarVHuNEeopOY9ubKCkwUaH+vEKt/VsS8nu
Bt9ZWWVqx/hemXLwyXrofBPersHvMUJ728d94QIDAQABAoIBAHSpZRtX+203rjZt
UFps9EgX+osJAEJpvOe6pSRj4h/1OaG672NJxv1J/HDgBBnjfF3OS8+ltYJZbu8A
cToTOL3h/OdHkEXYD2ffJLx7AwADYcKaufi4h3Ss1U5Gy7vqiZQ4N7aYFuEDfAz8
Rj/7Kij3R8jb4ZosomSrzh0HE65iapeSV7p04sa/FxM5vR13ReGQo/36kpW5BbcQ
7Q04EQiI7mq/HqRD/jb8dLAJo3O1Wu2tqj8W63z6bjJsPB8Ty213RXj8kmX1cGbg
qObg0G/1gtQUEKyOzYZEdoIfcXKea0/T0qUK0fo0URPa952jtbpQ7jltBLDmcYZi
R5YalRECgYEA45G2AC8Ho8zvk33Cj5Zi4MB1pNdfax6mhf6o7dudqHzh66jr3juN
0GGAreywzzIOrD+EsnTW6ERTH+r6K1wNcWmRl2ZAHbLWMlApMBCoVEPA4tY+wqqv
1euE2K7hAGzKudibBEZV5rH22p8cfB7jTA1KXpZa9OQtIl33L7TH7GMCgYEA3Rn+
hWuEN356Jso5cNSrR4EugZLDX5woSfun43xeA0+O08LBLoABPIfI5JcnQpPvBykp
6Fv2ugsifC72NV7lsOh1Q/f9ylQW8xIB91vftDTqvMGP3qM5Xoe4LT1wptrKeHGO
jtLZRLZKMC53Mv/laTQT15BOZI2sZY0dqki7NesCgYEAzTJYH/ZIN0TVSfL9+qcp
5WrlKYwiN97dXLlx7Xg3wvNIa0xX0n10tE8Wzr07+Lg0TtC/gIKmPa1OHtusVGie
noMIirHiYmUdiySI3xRGFCU7yc5RrQpnnsbNdOzLaayvZ8COlt4tGuWhpyQNdUYM
wkjBpGSDA4qzv+dmuheSpe0CgYBk4HBE1Uosu5Ll0cwlU5KV/DWIvrpPDANBxgTS
gLKwFgNXUHstSQ/HWzhoOyKZeL9M6BYLwrGuLlhcilyg+xwW++hMy3/KaVVTL3sg
LZXCNYaH+lQ2wwfwvkFkuqyEJDzOeRkOxtqERBtTIlAWP7SerDkFV/y8Wfs3Fgxb
3fU0YwKBgHNMqueSFo3DkPhyhEFkjPiREMYuElpl6mpk9apWVxy4lBRemB41RNyI
8tQbTWAMM8MA03WjGQgrShEFOkju1OvbxLPqIUuad5/IUXlRljbHzzrX0CsS02jw
SYTo77Sgr5BvikZkQWWJrskCkLwFGuOabOiXO5vODGuJYru/qXq8
-----END RSA PRIVATE KEY-----"""


#Init on main
SCRIPT_PATH = None
ID = None

# CLASS FOR TERMINAL COLOURS
#===============================================================================
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


# HELPER FUNCTIONS
#===============================================================================
def report( msg ):
    print( bcolors.OKBLUE + " * " + msg + bcolors.ENDC )

def execute(program):
    returnCode =  subprocess.call( program, shell=True)
    
    # Make sure everything went fine
    if returnCode != 0:
        raise Exception(
            "Execution of " + program + " failed with return code " + str(returnCode)
            )

def execute_ros( program ):
    return execute("bash -c 'source /opt/ros/hydro/setup.bash && " + program + "'")
    
def net_address(a,b,c,d):
    return dbus.UInt32( a +(b*(2**8) )+ (c*(2**16)) + (d*(2**24)) )
    
def get_wifi_name():
    return "HCRwifi"
    
def get_computer_id():
    hostname = os.uname()[1]
    return int( hostname.replace("prl-", "") )


# INSTALLATION ROUTINES
#===============================================================================

# Documentation:
# http://projects.gnome.org/NetworkManager/developers/api/09/ref-settings.htm
# Examples:
# http://cgit.freedesktop.org/NetworkManager/NetworkManager/tree/examples/python
def setup_wifi():
    wifi_name = get_wifi_name()
    
    setting_connection = dbus.Dictionary({
        'type': '802-11-wireless',
        'uuid': str(uuid.uuid4()), #This generates a random uuid
        'id': wifi_name,
        'autoconnect': True
        })
    
    setting_wifi = dbus.Dictionary({
        'ssid': dbus.ByteArray(wifi_name),
        'mode': 'infrastructure'
        })
    
    addresses = dbus.Array(
        [net_address(10,10,10,ID), dbus.UInt32(24L), net_address(10,10,10,254)],
        signature=dbus.Signature('u')
        )
    dns = dbus.Array(
        [net_address(8,8,8,8), net_address(8,8,4,4)],
        signature=dbus.Signature('u')
        )
    
    setting_ip4 = dbus.Dictionary({
        'addresses': dbus.Array([addresses], signature=dbus.Signature('au')),
        'dns': dns,
        'method': 'manual'
        })
        
    setting_ip6 = dbus.Dictionary({'method': 'ignore'})
    
    connection = dbus.Dictionary({
        'connection': setting_connection,
        '802-11-wireless': setting_wifi,
        'ipv4': setting_ip4,
        'ipv6': setting_ip6
        })
        
    bus = dbus.SystemBus()

    proxy = bus.get_object (
        "org.freedesktop.NetworkManager",
        "/org/freedesktop/NetworkManager/Settings"
        )
    settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")

    settings.AddConnection(connection)

#===============================================================================

def connect_wifi():
    execute("nmcli con up id " + get_wifi_name() + " --timeout 20"  )

#===============================================================================

# Taken from:
# http://stackoverflow.com/a/3764660
def check_internet():
    try:
        #Try connecting to google
        response=urllib2.urlopen('http://www.google.com',timeout=20)
    except urllib2.URLError as err:
        raise Exception( "No internet connection. URLError: " + str(err) )
    
def set_hosts():
    with open("/etc/hosts", "a") as hosts:
        hosts.write("\n# HCR Tutorials hosts\n")
        for i in range(1,15):
            if i == ID:
                continue
            hosts.write("10.10.10." + str(i) + "     prl-" + str(i) + "\n")
        
#===============================================================================

def create_temp():
    temp_dir = os.path.join(SCRIPT_PATH, "temp")
    remove_temp()
    os.mkdir( temp_dir )
    
def remove_temp():
    temp_dir = os.path.join(SCRIPT_PATH, "temp")
    if os.path.exists( temp_dir ):
        shutil.rmtree( temp_dir )


#===============================================================================

def install_packages():
    packages = ""
    for package in PACKAGE_LIST:
        packages = packages + package + " "
    
    execute("apt-get install -y --allow-unauthenticated " + packages)

#===============================================================================

def ubuntu_upgrade():
    execute("apt-get dist-upgrade -y --allow-unauthenticated")

#===============================================================================

def ubuntu_update():
    execute("apt-get update -y")

#===============================================================================
    
def ubuntu_autoremove():
    execute("apt-get autoremove -y")

#===============================================================================
    
def add_ros_repo():
    execute("sh -c 'echo \"deb http://packages.ros.org/ros/ubuntu precise main\" > /etc/apt/sources.list.d/ros-latest.list'")
    
    execute("wget http://packages.ros.org/ros.key -O - | sudo apt-key add -")

#===============================================================================

def add_icub_repo():
    execute("sh -c 'echo \"deb http://www.icub.org/ubuntu precise contrib/science\" > /etc/apt/sources.list.d/icub.list'")

#===============================================================================

def setup_local():
    #List all users in the system
    for user in pwd.getpwall():
        #Normal users under ubuntu
        if user.pw_uid >= 1000 and user.pw_uid < 65534:
            
            bashrc_path = os.path.abspath(user.pw_dir + "/.bashrc")            
            
            if os.path.isfile(bashrc_path):
                with open(bashrc_path, "a") as bashrc:
                    report("Adding ROS/NaoQi environment variables for " + user.pw_name)
                    bashrc.write("\n# ROS environment variables\n")
                    bashrc.write("source /opt/ros/hydro/setup.bash\n")
                    bashrc.write("export ROS_WORKSPACE=$HOME/catkin_ws\n")
                    bashrc.write("export ROS_IP=10.10.10."+str(ID)+"\n")
                    bashrc.write("export LIBGL_ALWAYS_SOFTWARE=1\n")   
            else:
                print(
                    bcolors.WARNING + 
                    " * Warning: .bashrc NOT found for user " + 
                    user.pw_name +
                    " under " +
                    user.pw_dir +
                    bcolors.ENDC
                    )
              
            catkin_ws_path = os.path.abspath( user.pw_dir + "/catkin_ws")
            
            if not os.path.exists( catkin_ws_path ):
                report("Creating catkin workspace for " + user.pw_name )
                os.mkdir( catkin_ws_path )
                os.mkdir( catkin_ws_path + "/src")
                os.chdir( catkin_ws_path + "/src")
                execute_ros("catkin_init_workspace")
                
                os.chown( catkin_ws_path, user.pw_uid, user.pw_gid )
                os.chown( catkin_ws_path + "/src", user.pw_uid, user.pw_gid )
            
            report("Installing SSH keys for "  + user.pw_name )
            ssh_path = os.path.abspath(user.pw_dir + "/.ssh")
            pubkey_path = os.path.abspath( ssh_path + "/id_rsa.pub")
            privkey_path = os.path.abspath( ssh_path + "/id_rsa")
            
            
            if not os.path.exists( ssh_path ):
                os.mkdir( ssh_path )
                os.chown( ssh_path, user.pw_uid, user.pw_gid )
                os.chmod( ssh_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR )
            
            with open(pubkey_path, "w") as pubkey:
                pubkey.write(PUB_KEY)
            
            # Owned by user (not by root)
            os.chown( pubkey_path, user.pw_uid, user.pw_gid)
            os.chmod( pubkey_path, stat.S_IRUSR | stat.S_IWUSR )
                
            with open(privkey_path, "w") as privkey:
                privkey.write(PRIV_KEY)
            
            # Owned by user (not by root)
            os.chown( privkey_path, user.pw_uid, user.pw_gid)
            os.chmod( privkey_path, stat.S_IRUSR | stat.S_IWUSR )
                
            report("Cloning HCR tutorial repository for "  + user.pw_name)
            os.chdir(user.pw_dir)
            
            # This is complicated because we need to run as user,
            # and also we need to specify the ssh protocol to accept bitbucket's
            # remote key
            execute(
                'sudo -u ' + user.pw_name + 
                ' hg clone --ssh "ssh -oStrictHostKeyChecking=no"'+
                ' ssh://hg@bitbucket.org/personal_robotics/hcr2013'
                )
                
#===============================================================================

def setup_udev_rules():
    with open("/etc/udev/rules.d/89-joystick.rules", "w") as udev_file:
        udev_file.write( JOYSTICK_UDEV)
    with open("/etc/udev/rules.d/90-hokuyo.rules", "w") as udev_file:
        udev_file.write( HOKUYO_UDEV )
    with open("/etc/udev/rules.d/91-pioneer.rules", "w") as udev_file:
        udev_file.write( PIONEER_UDEV )

#===============================================================================

def blacklist_linux_kinect():
	execute("sh -c 'echo \"blacklist gspca_kinect\n\" > /etc/modprobe.d/blacklist-kinect.conf'")
	
#===============================================================================
def reinstall_nite():
    #Get into the right directory
    os.chdir(os.path.join(SCRIPT_PATH, "temp") )
    
    report("Downloading NITE")
    execute("wget http://www.openni.org/wp-content/uploads/2012/12/NITE-Bin-Linux-x64-v1.5.2.21.tar.zip")
    execute("unzip NITE-Bin-Linux-x64-v1.5.2.21.tar.zip")
    execute("tar xvjf NITE-Bin-Linux-x64-v1.5.2.21.tar.bz2")
    
    report("Installing NITE")
    os.chdir("NITE-Bin-Dev-Linux-x64-v1.5.2.21")
    execute("./install.sh")

#===============================================================================
# MAIN: ENTRY POINT
#===============================================================================
if __name__ == "__main__":
    print(
        bcolors.HEADER +
        "HCR Tutorials Ubuntu Setup Tool\n" +
        "--------------------------------\n" +
        bcolors.ENDC
        )
    report("VERSION: " + VERSION )
        
    try:
        SCRIPT_PATH = os.path.abspath( 
            os.path.dirname( 
                inspect.getfile( inspect.currentframe() ) 
                )
            )
        report( "Running from: " + SCRIPT_PATH )
        
        if not os.geteuid()==0:
            raise Exception("Only root can run this script")
        
        
        ID = get_computer_id()
        report("Computer id = " + str(ID) )
           
        report("Creating temporary directory")
        create_temp()
        
        report("Creating wifi connection")
        setup_wifi()
                
        report("Connecting to wifi")
        connect_wifi()
        
        report("Checking internet connectivity")
        check_internet()

        report("Setting /etc/hosts")
        set_hosts()

        report("Adding ROS repository")
        add_ros_repo()
        
        report("Adding iCub repository")
        add_icub_repo()
        
        report("Updating apt-get package cache")
        ubuntu_update()
        
        report("Upgrading Ubuntu")
        ubuntu_upgrade()
        
        report("Installing required packages")
        install_packages()
        
        report("Auto-removing no-longer required packages")
        ubuntu_autoremove()
        
        report("Setting up udev rules")
        setup_udev_rules()
         
        report("Blacklisting Native Kinect driver" )
        blacklist_linux_kinect()
        
        report("Re-installing NITE")
        reinstall_nite()
        
        report("Configuring user-level settings")
        setup_local()
        
        report("Cleaning temporary files")
        remove_temp()
        
        report("All operations successfully completed!")
        os.chdir(SCRIPT_PATH)
        
        report("Rebooting system!\n")
        execute("reboot")

    except Exception as e:
        print(bcolors.FAIL + " * There was an error: " + str(e) + bcolors.ENDC)
        exit(-1)
