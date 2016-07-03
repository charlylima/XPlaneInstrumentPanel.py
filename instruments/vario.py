from piHud import Gauge,Config

class Variometer(Gauge.Gauge):
    def __init__(self, parent):
        config = Config.Config(
          _title          = "m/s", 
          _min            = -5,
          _max            = 5,
          _redline        = None,
          _scale_step     = 1,
          _scale_mult     = 1)
        super(Variometer, self).__init__(parent,config)

