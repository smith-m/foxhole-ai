def is_inventory_screen(image) -> bool:
    """
    calculates if player is on inventory screen
    :return:
    """


def is_inventory_share_screen(image) -> bool:
    """
    calculates if player is on inventory share screen
    :return:
    """


def get_inventory_from_inventory_share_screen(image):
    """
    calculates my inventory and object inventory from image
    my_inventory
    [
        0,1,2,3,4,
        5,6,7,8
    ]
    storage_box_inventory
    [
        0,1,2,3,4,
        5,6,7,8,9,
        10,12,12,13,14
    ]
    :return: tuple(my_inventory, object_inventory)
    [
        {"name":"other"},
        {"name":"scrap"},
        {"name":"technology_part"},
        {"name":"empty"},
        {"name":"empty"},
        {"name":"empty"},
        {"name":"empty"},
    ],
    [
        {"name":"other"},
        {"name":"scrap"},
        {"name":"technology_part"},
    ],
    """
    raise NotImplementedError


def get_share_object_name_from_inventory_screen(image) -> str:
    """
    returns name of object play is sharing with ("storage_object", "other")
    :return: str
    """


def get_inventory_from_inventory_screen(image):
    """
    calculates my inventory from image
    my_inventory
    [
        0,1,2,3,4,
        5,6,7,8
    ]
    :return: tuple(my_inventory, object_inventory)
    [
        {"name":"other"},
        {"name":"scrap"},
        {"name":"technology_part"},
        {"name":"empty"},
        {"name":"empty"},
        {"name":"empty"},
        {"name":"empty"},
        {"name":"empty"},
        {"name":"empty"},
    ],
    [
        {"name":"other"},
        {"name":"scrap"},
        {"name":"technology_part"},
    ],
    """
    raise NotImplementedError


def can_share_with_storage_box(image) -> bool:
    """
    Identifies whether or not player is adjacent to storage box and can press "E" to show inventory share screen

    """
    raise NotImplementedError


# TODO: this may be lower priority / not necessary - could be helpful for validating successful salvaging
def is_gathering_salvage(image) -> bool:
    """
    Identifies whether player is "gathering salvage" based on image
    """


def get_salvage_locations(image):
    """
    Identifies salvage stack locations on screen and returns on screen coordinate system.
    Might make sense to stay consistent wth cv.rectangle api here nstead of tuples
    :return:
    [
        # scrap 0
        (x0,y0,x1,y1),
        # scrap 1
        (x0,y0,x1,y1),
        (x0,y0,x1,y1),

    ]
    """


def get_storage_object_locations(image):
    """
    Identifies storage object locations on screen and returns on screen coordinate system.
    Might make sense to stay consistent wth cv.rectangle api here instead of tuples
    :return:
    [
        # scrap 0
        (x0,y0,x1,y1),
        # scrap 1
        (x0,y0,x1,y1),
        (x0,y0,x1,y1),

    ]
    """
