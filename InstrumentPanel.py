import sys
from PyQt4 import QtGui, QtCore
import Gauge
import Config

from XPlaneUdp import XPlaneUdp


class InstrumentPanel(QtGui.QWidget):
  knots_to_kmh = 1.852
  
  def __init__(self, parent=None):
    super(InstrumentPanel, self).__init__(parent)
    self.xplane = None
    self.instr = {} 
    self.instr["speed"] = None
    self.instr["alt"] = None

    # QT Layout
    self.setStyleSheet("background-color:black;")
    layout = QtGui.QGridLayout(self);
    self.setLayout(layout);

    # XPlane network connection
    self.xplane = XPlaneUdp.XPlaneUdp()
    print("watch out for running xplane in network...")
    beacon = self.xplane.FindIp()
    print("found it: {}".format(beacon["IP"]))
    self.xplane.AddDataRef("sim/flightmodel/position/indicated_airspeed", freq=10)
    self.xplane.AddDataRef("sim/flightmodel/misc/h_ind", freq=10)

    # speed widget
    config = Config.Config(
      _title          = "km/h",
      _min            = 0,
      _max            = 250,
      _redline        = 200,
      _scale_step     = 25,
      _scale_mult     = 1)
    self.instr["speed"] = Gauge.Gauge(None, config)
    self.instr["speed"].dataref = "sim/flightmodel/position/indicated_airspeed"
    self.instr["speed"].dataref_corrfactor = self.knots_to_kmh
    layout.addWidget(self.instr["speed"],0,0)

    # altitude widget
    config = Config.Config(
      _title          = "ft", 
      _min            = 0,
      _max            = 10000,
      _redline        = None,
      _scale_step     = 1000,
      _scale_mult     = 1000)
    self.instr["alt"] = Gauge.Gauge(None, config)
    self.instr["alt"].dataref = "sim/flightmodel/misc/h_ind"
    layout.addWidget(self.instr["alt"],0,1)

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
