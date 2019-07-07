import game_sensor
import cv2
from matplotlib import pyplot as plt


def test_load_inventory_trade_template():
    img = game_sensor.load_inventory_trade_template()
    plt.imshow(img)
    plt.show()


def test_load_player_inventory_template():
    img = game_sensor.load_player_inventory_template()
    plt.imshow(img)
    plt.show()


def test_get_inventory_from_inventory_share_screen():
    sensor = game_sensor.GameSensor()
    # patch not implemented functions
    sensor.is_inventory_share_screen = lambda x: True


    screenshot = cv2.imread("images/screens/1024-768/inventory-trade-technology-part-1.png", game_sensor.GRAYSCALE_LOAD)
    # plt.imshow(screenshot)
    # plt.show()

    inventory_image = game_sensor.crop_inventory_from_screen(screenshot)
    plt.imshow(inventory_image)
    plt.show()
    inventory = sensor.get_inventory_from_inventory_share_screen(inventory_image)

    print(inventory)


test_get_inventory_from_inventory_share_screen()
# test_load_inventory_trade_template()
# test_load_player_inventory_template()
