from easybpy.easybpy import rotation, location


class BlenderTransformUtils:
    @staticmethod
    def copy_location_and_rotation(from_object, to_object):
        r = rotation(from_object)
        t = location(from_object)
        location(to_object, [t[0], t[1], t[2]])
        rotation(to_object, [r[0], r[1], r[2]])
