import dbus
import enum
from datetime import datetime

"""
Battery monitor using dbus.
Sources:
 * http://askubuntu.com/questions/113490/
 * http://upower.freedesktop.org/docs/Device.html
 * http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html [not up to date !!]
 KDE Sources:
 * https://techbase.kde.org/Development/Tutorials/Plasma5/QML2/GettingStarted
Related projects
 * https://techbase.kde.org/Development/Tutorials/Plasma4/PythonPlasmoid
 * Temp & Battery Applet [kde4]
   http://kde-look.org/content/show.php/Temperature?content=158782
Graph export [TODO]
 * Both projects above use SignalPlotter which has a non-merged port in:
  https://projects.kde.org/projects/frameworks/plasma-framework/repository/entry/src/declarativeimports/plasmaextracomponents/qml/SignalPlotter.qml?rev=bshah%2Fplotter-qml
  discussion in: http://comments.gmane.org/gmane.comp.kde.devel.core/82432
 * KWidgetAddons 5 has kplotting:
   http://api.kde.org/frameworks-api/frameworks5-apidocs/kplotting/html/classKPlotWidget.html
 * ...which is in pykde5:
   https://projects.kde.org/projects/kde/kdebindings/python/pykde5/repository/revisions/master/entry/sip/kplotting/kplotwidget.sip
 * Artikulate uses org.kde.charts 0.1 which has a QtQuick2 port [?]
   https://projects.kde.org/projects/kde/kdeedu/artikulate/repository/revisions/master/entry/src/qml/TrainerCourseStatistics.qml
 * see also kqmlgraphplugin ?

"""

# qdbus --literal --system org.freedesktop.UPower
#  /org/freedesktop/UPower/devices/battery_BAT0
#  org.freedesktop.UPower.Device.GetHistory rate 86400 1440 | sed 's/],/]\n/g'

# noinspection PyArgumentList
State = enum.Enum('State', names={'Unknown': 0, 'Charging': 1, 'Discharging': 2})


def main():
    bus = dbus.SystemBus()
    bat0 = bus.get_object('org.freedesktop.UPower', '/org/freedesktop/UPower/devices/battery_BAT0')
    # bat0._introspect_method_map
    # bat0_dev_iface = dbus.Interface(bat0, 'org.freedesktop.UPower.Device')
    # bat0_dev_iface.GetHistory('rate', 86400, 1440)
    get_hist = bat0.get_dbus_method('GetHistory', dbus_interface='org.freedesktop.UPower.Device')
    hist = get_hist('rate', 86400, 1440)
    for (timestamp, rate, state_int) in hist:
        dt = datetime.fromtimestamp(timestamp)
        state = State(state_int)
        print(dt, rate, state)
        # FIXME this fails becasue states are wrong... Find them in the doc/code ?
