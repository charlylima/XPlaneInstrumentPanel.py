from piHud import Gauge,Config

class Altimeter(Gauge.Gauge):
    def __init__(self, parent):
        config = Config.Config(
          _title          = "ft", 
          _min            = 0,
          _max            = 10000,
          _redline        = None,
          _scale_step     = 1000,
          _scale_mult     = 1000)
        super(Altimeter, self).__init__(parent,config)

