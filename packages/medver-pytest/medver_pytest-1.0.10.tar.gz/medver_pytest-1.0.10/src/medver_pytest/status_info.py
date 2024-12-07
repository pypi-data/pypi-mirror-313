import json
import os

from . import services


# --------------------
## holds all information that be used from run invocation to others
# Note:
#  * should hold only values that the user can/should change between runs
#  * no constants
class StatusInfo:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds last manual tester initials if any
        self._last_tester_initials = ''

        ## holds last position of dlg box, x coord
        self._last_position_x = None
        ## holds last position of dlg box, y coord
        self._last_position_y = None
        ## holds path to the status json file
        self._path = os.path.join(services.cfg.statusdir, 'status.json')

        self._load()

    # -------------------
    ## getter for the last dlg x position
    #
    # @return last dlg position for x coordinate
    @property
    def last_position_x(self):
        return self._last_position_x

    # -------------------
    ## getter for the last dlg y position
    #
    # @return last dlg position for y coordinate
    @property
    def last_position_y(self):
        return self._last_position_y

    # -------------------
    ## check if there is a last position saved
    #
    # @return None
    def last_position_saved(self):
        return self._last_position_x is not None and self._last_position_y is not None

    # -------------------
    ## save last dlg screen coordinates
    #
    # @param x   the x coordinate of the screen position
    # @param y   the y coordinate of the screen position
    # @return None
    def save_last_position(self, x, y):
        self._last_position_x = x
        self._last_position_y = y
        self._save()

    # -------------------
    ## getter for the last tester initials
    #
    # @return last tester initials
    @property
    def last_tester_initials(self):
        return self._last_tester_initials

    # -------------------
    ## setter for the last tester initials
    #
    # @param val  the new last tester initials
    # @return None
    @last_tester_initials.setter
    def last_tester_initials(self, val):
        self._last_tester_initials = val
        self._save()

    # -------------------
    ## save all data to file
    #
    # @return None
    def _save(self):
        with open(self._path, 'w', encoding='utf-8') as fp:
            j = {
                'last_tester_initials': self._last_tester_initials,
                'last_position_x': self._last_position_x,
                'last_position_y': self._last_position_y,
            }
            json.dump(j, fp, indent=4)

    # -------------------
    ## save data from file, if it exists.
    # Otherewise leave data in its current state.
    #
    # @return None
    def _load(self):
        if not os.path.isfile(self._path):
            # file doesn't exist yet
            return

        with open(self._path, 'r', encoding='utf-8') as fp:
            j = json.load(fp)
            self._last_tester_initials = j['last_tester_initials']
            self._last_position_x = j['last_position_x']
            self._last_position_y = j['last_position_y']
