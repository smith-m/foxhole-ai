import game_sensor
import cv2
from matplotlib import pyplot as plt


def test_load_inventory_trade_template():
    img = game_sensor.load_inventory_trade_template()
    # plt.imshow(img)
    # plt.show()


def test_load_player_inventory_template():
    img = game_sensor.load_player_inventory_template()
    # plt.imshow(img)
    # plt.show()


def test_get_inventory_from_inventory_share_screen():
    sensor = game_sensor.GameSensor()
    screenshot = cv2.imread("images/screens/1024-768/inventory-trade-technology-part-1.png", game_sensor.GRAYSCALE_LOAD)
    # plt.imshow(screenshot)
    # plt.show()

    inventory_image = game_sensor.crop_inventory_from_screen(screenshot)
    plt.imshow(inventory_image)
    plt.show()
    player_inventory, object_inventory = sensor.get_inventory_from_inventory_share_screen(inventory_image)

    print(player_inventory)
    print(object_inventory)

    assert len(player_inventory) == 9
    assert len(object_inventory) == 15

    expected_player_inventory = [
        "other",
        "scrap",
        "scrap",
        "empty",
        "empty",
        "empty",
        "empty",
        "empty",
        "empty",
    ]

    expected_object_inventory = [
        "technology_part",
        "technology_part",
        "technology_part",
        "scrap",
        "empty",
        "empty",
        "empty",
        "empty",
        "empty",
        "empty",
        "empty",
        "empty",
        "empty",
        "empty",
        "empty",
    ]

    assert player_inventory == expected_player_inventory
    assert object_inventory == expected_object_inventory


def test_is_inventory_trade_screen_false_player_inventory():
    sensor = game_sensor.GameSensor()
    screenshot = cv2.imread("images/screens/1024-768/player-inventory-1.png", game_sensor.GRAYSCALE_LOAD)

    assert not sensor.is_inventory_share_screen(screenshot)


def test_is_inventory_trade_screen_false_landscape():
    sensor = game_sensor.GameSensor()
    screenshot = cv2.imread("images/screens/1024-768/storage-boxes-scrap-day-1.png", game_sensor.GRAYSCALE_LOAD)

    assert not sensor.is_inventory_share_screen(screenshot)


def test_is_player_inventory_screen_true():
    sensor = game_sensor.GameSensor()
    screenshot = cv2.imread("images/screens/1024-768/player-inventory-1.png", game_sensor.GRAYSCALE_LOAD)

    assert sensor.is_player_inventory_screen(screenshot)


# test_load_inventory_trade_template()
# test_load_player_inventory_template()

