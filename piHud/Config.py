from collections import OrderedDict

class Config():
    def __init__(self,
                 _title          = None,
                 _min            = None,
                 _max            = None,
                 _redline        = None,
                 _scale_step     = None,
                 _scale_mult     = None,
                 ):

        self.data = OrderedDict([
            ("sensor",      ""          ),
            ("type",        None        ),
            ("title",       _title      ),
            ("x",           0           ),
            ("y",           0           ),
            ("w",           None        ), # default sizes are set by each widget's sizeHint()
            ("h",           None        ),
            ("min",         _min        ),
            ("max",         _max        ),
            ("redline",     _redline    ),
            ("numerals",    True        ),
            ("scale_step",  _scale_step ),
            ("scale_mult",  _scale_mult ),
            ("buffer_size", None),
            ("color",       "#FFFFFF"), 
            ("redline_color", "#FF0000"), 
            ("font_size",   30),
            ("note_font_size", 20),
            ])

    def clone(self):
        c = Config()
        c.data = OrderedDict(self.data) # copy the data
        return c


    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            raise KeyError("'%s' is not a valid config key" % key)


    def __setitem__(self, key, value):
        if key in self.data:
            self.data[key] = value
        else:
            raise KeyError("'%s' is not a valid config key" % key)


    def __contains__(self, key):
        return key in self.data


    def __iter__(self):
        for key in self.data:
            yield key

