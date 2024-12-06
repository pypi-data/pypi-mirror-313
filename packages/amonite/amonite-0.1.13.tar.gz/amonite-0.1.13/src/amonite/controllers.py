import pyglet

from amonite.collision.collision_controller import CollisionController
from amonite.interaction_controller import InteractionController
from amonite.input_controller import InputController
from amonite.inventory_controller import InventoryController, MenuController
from amonite.sound_controller import SoundController

COLLISION_CONTROLLER: CollisionController
INPUT_CONTROLLER: InputController
INTERACTION_CONTROLLER: InteractionController
SOUND_CONTROLLER: SoundController
INVENTORY_CONTROLLER: InventoryController
MENU_CONTROLLER: MenuController

def create_controllers(window: pyglet.window.BaseWindow) -> None:
    global COLLISION_CONTROLLER
    global INPUT_CONTROLLER
    global INTERACTION_CONTROLLER
    global SOUND_CONTROLLER
    global INVENTORY_CONTROLLER
    global MENU_CONTROLLER

    COLLISION_CONTROLLER = CollisionController()
    INPUT_CONTROLLER = InputController(window = window)
    INTERACTION_CONTROLLER = InteractionController()
    SOUND_CONTROLLER = SoundController()
    INVENTORY_CONTROLLER = InventoryController()
    MENU_CONTROLLER = MenuController()