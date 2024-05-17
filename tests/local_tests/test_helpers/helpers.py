""" Main helpers. """
class Helpers:
    """ Main helper class. """

    @staticmethod
    def add_field_by_conditions(checkbox_widget, value):
        """ Return value depends on chackbox value. """
        if checkbox_widget is False:
            return None

        return value
