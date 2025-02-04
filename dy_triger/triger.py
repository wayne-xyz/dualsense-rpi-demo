import pydualsense as ds


def trigger():
    controller= ds.pydualsense()
    controller.init()



    controller.close()

    pass