BCM = None
OUT = "OUT"
IN = 1
LOW = 0


def setmode(mode=None):
    print("set the mode to {}".format(mode))


def setup(num=None, output=None):
    print("set up num {} with output{}".format(num, output))


def output(num=None, out_level=None):
    print("output num {} with level {}".format(num, out_level))


def cleanup():
    pass
