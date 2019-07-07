import cv2
import numpy as np
from matplotlib import pyplot as plt


class InvalidScreenError(Exception):
    """Raised when image evaluated is from incorrect screen"""
    pass


class GameSensor:
    def __init__(self):
        self.inventory_trade = load_inventory_trade_template()
        self.player_inventory = load_player_inventory_template()
        self.storage_interact_instruction = load_storage_interact_instruction_template()

        self.identifiable_inventory = {
            "salvage_item": load_scrap_item_template(),
            "technology_part": load_technology_part_template(),
            "empty_slot": load_empty_slot_template()
        }

    def is_player_inventory_screen(self, image) -> bool:
        """
        calculates if player is on inventory screen
        :return:
        """
        raise NotImplementedError

    def is_inventory_share_screen(self, image) -> bool:
        """
        calculates if player is on inventory share screen
        :return:
        """
        raise NotImplementedError

    def identify_inventory_slot(self, image):
        """
        identifies inventory slot image based on list on known images
        :param image:
        :return:
        """
        best_match = "other"
        best_score = .5
        for name, template in self.identifiable_inventory.items():
            match = image_match(image, template)
            if match > .8:
                return name

            elif match > best_score:
                best_match = name
                best_score = match

        return best_match

    def get_inventory_from_inventory_share_screen(self, image):
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
        if not self.is_inventory_share_screen(image):
            raise InvalidScreenError

        object_img, player_img = crop_inventory_halves(image)

        object_images = crop_items_from_half_inventory(object_img, 15)
        player_images = crop_items_from_half_inventory(player_img, 9)

        # for img in object_images:
        #     plt.imshow(img)
        #     plt.show()
        #
        # for img in player_images:
        #     plt.imshow(img)
        #     plt.show()

        object_inventory = []
        for img in object_images:
            object_inventory.append(self.identify_inventory_slot(img))

        player_inventory = []
        for img in player_images:
            player_inventory.append(self.identify_inventory_slot(img))

        return player_inventory, object_inventory

    def get_share_object_name_from_inventory_screen(self, image) -> str:
        """
        returns name of object play is sharing with ("storage_object", "other")
        :return: str
        """
        raise NotImplementedError

    def get_inventory_from_player_inventory_screen(self, image):
        """
        calculates my inventory from image
        my_inventory
        [
            0,1,2,3,4,
            5,6,7,8
        ]
        :return: my_inventory
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
        ]
        """
        if not self.is_player_inventory_screen(image):
            raise InvalidScreenError

        object_img, player_img = crop_inventory_halves(image)

        player_images = crop_items_from_half_inventory(player_img, 9)

        player_inventory = []
        for image in player_images:
            player_inventory.append(self.identify_inventory_slot(image))

        return player_inventory

    def can_share_with_storage_box(self, image) -> bool:
        """
        Identifies whether or not player is adjacent to storage box and can press "E" to show inventory share screen

        """
        raise NotImplementedError

    # TODO: this may be lower priority / not necessary - could be helpful for validating successful salvaging
    def is_gathering_salvage(self, image) -> bool:
        """
        Identifies whether player is "gathering salvage" based on image
        """

        raise NotImplementedError

    def get_salvage_locations(self, image):
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

    def get_storage_object_locations(self, image):
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


# 1920 x 1080 (full screen windowed replicates monitor setting, not game resolution setting)
# INVENTORY_ANCHOR = (780, 930)
# INVENTORY_DIMENSIONS = (360, 495)
# INVENTORY_TOP_SLOT_ANCHOR = (782, 185)
# INVENTORY_SLOT_DIMENSIONS = (68, 68)
# INVENTORY_BOTTOM_SLOT_ANCHOR = (782, 437)
# INVENTORY_Y_SLOT_BORDER = 3
# INVENTORY_X_SLOT_BORDER = 4

# 1024 x 768 settings
SCREEN_DIMENSIONS = (1024, 768)
INVENTORY_ANCHOR = (380, 106)
INVENTORY_DIMENSIONS = (261, 362)
INVENTORY_TOP_SLOT_ANCHOR = (386, 132)
INVENTORY_SLOT_DIMENSIONS = (48, 48)
INVENTORY_BOTTOM_SLOT_ANCHOR = (386, 313)
INVENTORY_Y_SLOT_BORDER = 4
INVENTORY_X_SLOT_BORDER = 3

STORAGE_TOGGLE_ANCHOR = (15, 732)
STORAGE_TOGGLE_DIMENSIONS = (161, 21)

GATHERING_RESOURCES_ANCHOR = (448, 543)
GATHERING_RESOURCES_DIMENSIONS = (128, 23)

GRAYSCALE_LOAD = cv2.IMREAD_GRAYSCALE


def image_match(image, template) -> float:
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    match = np.max(res)
    return match


def crop_image(img, anchor, dimensions):
    return img[
           anchor[1]:anchor[1] + dimensions[1],
           anchor[0]:anchor[0] + dimensions[0],
           ]


def crop_inventory_from_screen(img):
    return crop_image(img, INVENTORY_ANCHOR, INVENTORY_DIMENSIONS)


def crop_inventory_halves(img):
    top_anchor = (
        INVENTORY_TOP_SLOT_ANCHOR[0] - INVENTORY_ANCHOR[0], INVENTORY_TOP_SLOT_ANCHOR[1] - INVENTORY_ANCHOR[1])
    bottom_anchor = (
        INVENTORY_BOTTOM_SLOT_ANCHOR[0] - INVENTORY_ANCHOR[0], INVENTORY_BOTTOM_SLOT_ANCHOR[1] - INVENTORY_ANCHOR[1])

    top_dimensions = (
        INVENTORY_DIMENSIONS[0] - top_anchor[0], INVENTORY_BOTTOM_SLOT_ANCHOR[1] - INVENTORY_TOP_SLOT_ANCHOR[1])
    bottom_dimensions = (
        INVENTORY_DIMENSIONS[0] - bottom_anchor[0], INVENTORY_DIMENSIONS[1] - top_dimensions[1])

    top_img = crop_image(img, top_anchor, top_dimensions)
    bottom_img = crop_image(img, bottom_anchor, bottom_dimensions)
    return top_img, bottom_img


def crop_items_from_half_inventory(img, num_item_slots):
    images = []
    for i in range(num_item_slots):
        anchor = (
            (INVENTORY_X_SLOT_BORDER + INVENTORY_SLOT_DIMENSIONS[0]) * (i % 5),
            (i // 5) * (INVENTORY_Y_SLOT_BORDER + INVENTORY_SLOT_DIMENSIONS[1])
        )
        item_img = crop_image(img, anchor, INVENTORY_SLOT_DIMENSIONS)

        images.append(item_img)

    return images


def load_inventory_trade_template():
    img = cv2.imread("images/screens/1024-768/inventory-trade-1.png", GRAYSCALE_LOAD)
    return crop_inventory_from_screen(img)


def load_player_inventory_template():
    img = cv2.imread("images/screens/1024-768/player-inventory-1.png", GRAYSCALE_LOAD)
    return crop_inventory_from_screen(img)


def load_scrap_item_template():
    img = cv2.imread("images/snippets/1024-768/inventory-scrap-1.png", GRAYSCALE_LOAD)
    return img


def load_technology_part_template():
    img = cv2.imread("images/snippets/1024-768/inventory-technology-part-1.png", GRAYSCALE_LOAD)
    return img


def load_empty_slot_template():
    img = cv2.imread("images/snippets/1024-768/inventory-empty-slot-1.png", GRAYSCALE_LOAD)
    return img


def load_storage_box_inventory_label_template():
    raise NotImplementedError


def load_storage_interact_instruction_template():
    img = cv2.imread("images/snippets/1024-768/storage-box-toggle-1.png", GRAYSCALE_LOAD)
    return img


def load_storage_box_3d_template():
    raise NotImplementedError
