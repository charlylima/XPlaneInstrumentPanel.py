from piHud import Gauge,Config

class Speedometer(Gauge.Gauge):
    def __init__(self, parent):
        config = Config.Config(
          _title          = "km/h",
          _min            = 0,
          _max            = 250,
          _redline        = 200,
          _scale_step     = 25,
          _scale_mult     = 1)
        super(Speedometer, self).__init__(parent,config)

