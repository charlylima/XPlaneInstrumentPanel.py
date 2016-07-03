import sys
from PyQt4 import QtGui, QtCore
from XPlaneUdp import XPlaneUdp
from piHud import Gauge, Config
from instruments import speedometer
from instruments import altimeter
from instruments import compass
from instruments import vario

class InstrumentPanel(QtGui.QWidget):
  knots_to_kmh = 1.852
  ms_to_ftmin = 196.85
  
  def __init__(self, parent=None):
    super(InstrumentPanel, self).__init__(parent)
    self.xplane = None
    self.instr = {} 

    # QT Layout
    self.setStyleSheet("background-color:black;")
    layout = QtGui.QGridLayout(self);
    self.setLayout(layout);

    # speed widget
    instr = speedometer.Speedometer(self)
    instr.dataref = "sim/flightmodel/position/indicated_airspeed"
    instr.dataref_corrfactor = self.knots_to_kmh
    layout.addWidget(instr,0,1)
    self.instr["speed"] = instr

    # artificial horizone

    # altitude widget
    instr = altimeter.Altimeter(self)
    instr.dataref = "sim/flightmodel/misc/h_ind"
    layout.addWidget(instr,0,2)
    self.instr["alt"] = instr

    # turn and pitch coordinator

    # compass widget
    instr = compass.Compass(self)
    instr.dataref = "sim/flightmodel/position/mag_psi"
    layout.addWidget(instr,1,1)
    self.instr["compass"] = instr

    # variometer widget
    instr = vario.Variometer(self)
    instr.dataref = "sim/flightmodel/position/vh_ind"
    layout.addWidget(instr,1,2)
    self.instr["vario"] = instr
    
    # XPlane network connection
    self.xplane = XPlaneUdp.XPlaneUdp()
    print("watch out for running xplane in network...")
    beacon = self.xplane.FindIp()
    print("found it: {}".format(beacon["IP"]))
    for instr in self.instr.values():
      self.xplane.AddDataRef(instr.dataref, freq=10)

    # timer
    self.timer = QtCore.QTimer();
    self.timer.pyqtConfigure(timeout=self.updateInstrument)
    self.timer.start(50);

  def updateInstrument(self):
    """ On Timer: """
    """ Get XPlane DataRef Value from network and set it in the GUI Widgets. """

    # get values from xplane
    values = self.xplane.GetValues()

    # update GUI
    for instr in self.instr.values():
      if hasattr(instr, "dataref_corrfactor"): 
        instr.value = instr.dataref_corrfactor * values[instr.dataref]
      else:
        instr.value = values[instr.dataref]
      instr.update()

if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  panel = InstrumentPanel()
  panel.show()
  sys.exit(app.exec_())
