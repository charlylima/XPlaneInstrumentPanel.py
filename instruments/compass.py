from piHud import Gauge,Config

class Compass(Gauge.Gauge):
    def __init__(self, parent):
        config = Config.Config(
          _title          = "Mag Heading", 
          _min            = 0,
          _max            = 360,
          _redline        = None,
          _scale_step     = 90,
          _scale_mult     = 1)
        super(Compass, self).__init__(parent,config)

