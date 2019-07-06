# basic actions


def move_direction_for_time(direction, time_ms):
    """
    hold for wasd for x, async
    """
    raise NotImplementedError


def toggle_player_inventory():
    """
    tab
    """
    raise NotImplementedError


def interact_object():
    """
    e
    """
    raise NotImplementedError


def exit_menu():
    """
    esc
    """
    raise NotImplementedError


# TODO: might be lower priority, we might need it for salvage / storage box identification
def rotate_perspective(angle_change):
    """
    right click and drag angle change
    """
    raise NotImplementedError


# complex actions

def move_to_location(screen_coordinates):
    raise NotImplementedError


