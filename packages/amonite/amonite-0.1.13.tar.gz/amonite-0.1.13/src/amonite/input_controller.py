from enum import Enum
from functools import reduce
from typing import Any
import pyglet
import pyglet.math as pm

class ControllerButton(str, Enum):
    ########################
    # Left hand buttons.
    ########################
    UP = "dpup"
    LEFT = "dpleft"
    DOWN = "dpdown"
    RIGHT = "dpright"
    ########################
    ########################

    ########################
    # Right hand buttons.
    ########################
    NORTH = "y"
    WEST = "x"
    SOUTH = "a"
    EAST = "b"
    ########################
    ########################

    ########################
    # Function buttons.
    ########################
    START = "start"
    SELECT = "select"
    LOGO = "guide"
    ########################
    ########################

    ########################
    # Stick buttons.
    ########################
    LSTICK = "leftstick"
    RSTICK = "rightstick"
    ########################
    ########################

    ########################
    # Shoulder buttons.
    ########################
    LSHOULDER = "leftshoulder"
    RSHOULDER = "rightshoulder"
    ########################
    ########################

class ControllerStick(str, Enum):
    LSTICK = "leftstick"
    RSTICK = "rightstick"

class ControllerTrigger(str, Enum):
    LTRIGGER = "lefttrigger"
    RTRIGGER = "righttrigger"

class InputController:
    def __init__(
        self,
        window: pyglet.window.BaseWindow,
        threshold: float = 0.1
    ):
        self.__window = window
        self.__threshold = threshold

        # Keyboard.
        self.keys: dict[int, bool] = {}
        self.key_presses: dict[int, bool] = {}
        self.key_releases: dict[int, bool] = {}

        # Controller.
        self.buttons: list[dict[str, bool]] = []
        self.button_presses: list[dict[str, bool]] = []
        self.button_releases: list[dict[str, bool]] = []
        self.sticks: list[dict[str, tuple[float, float]]] = []
        self.triggers: list[dict[str, float]] = []

        self.__window.push_handlers(self)

        # Get controllers.
        controller_manager = pyglet.input.ControllerManager()
        self.controllers: list[pyglet.input.Controller] = []
        all_controllers: list[pyglet.input.Controller] = controller_manager.get_controllers()
        for controller in all_controllers:
            self.add_controller(controller = controller)

        controller_manager.push_handlers(self)

    def add_controller(self, controller: pyglet.input.Controller) -> None:
        controller.open()
        controller.push_handlers(self)
        self.controllers.append(controller)
        self.buttons.append({})
        self.button_presses.append({})
        self.button_releases.append({})
        self.sticks.append({})
        self.triggers.append({})

    def remove_controller(self, controller: pyglet.input.Controller) -> None:
        # Fetch controller index and return if not found.
        controller_index: int
        try:
            controller_index = self.controllers.index(controller)
        except:
            return

        self.buttons.pop(controller_index)
        self.button_presses.pop(controller_index)
        self.button_releases.pop(controller_index)
        self.sticks.pop(controller_index)
        self.triggers.pop(controller_index)
        self.controllers.remove(controller)

    # ----------------------------------------------------------------------
    # Keyboard events.
    # ----------------------------------------------------------------------
    def on_key_press(
        self,
        symbol: int,
        modifiers
    ):
        self.keys[symbol] = True

        # Only save key press if the key has been released first.
        self.key_presses[symbol] = self.key_releases.get(symbol, True)
        self.key_releases[symbol] = False

    def on_key_release(
        self,
        symbol: int,
        modifiers
    ):
        self.keys[symbol] = False
        self.key_presses[symbol] = False
        self.key_releases[symbol] = True
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # Controller events.
    # ----------------------------------------------------------------------
    def on_connect(
        self,
        controller: pyglet.input.Controller
    ) -> None:
        self.add_controller(controller = controller)
        print("controller_connected:", controller)

    def on_disconnect(
        self,
        controller: pyglet.input.Controller
    ) -> None:
        self.remove_controller(controller = controller)
        print("controller_disconnected:", controller)

    def on_button_press(
        self,
        controller: pyglet.input.Controller,
        button_name: str
    ) -> None:
        # Fetch controller index and return if not found.
        controller_index: int
        try:
            controller_index = self.controllers.index(controller)
        except:
            return

        self.buttons[controller_index][button_name] = True

        # Only save key press if the key has been released first.
        self.button_presses[controller_index][button_name] = self.button_releases[controller_index].get(button_name, True)
        self.button_releases[controller_index][button_name] = False

    def on_button_release(
        self,
        controller: pyglet.input.Controller,
        button_name: str
    ) -> None:
        # Fetch controller index and return if not found.
        controller_index: int
        try:
            controller_index = self.controllers.index(controller)
        except:
            return

        self.buttons[controller_index][button_name] = False
        self.button_presses[controller_index][button_name] = False
        self.button_releases[controller_index][button_name] = True

    def on_dpad_motion(
        self,
        controller: pyglet.input.Controller,
        dpleft,
        dpright,
        dpup,
        dpdown
    ) -> None:
        pass

    def on_stick_motion(
        self,
        controller: pyglet.input.Controller,
        stick: str,
        xvalue: float,
        yvalue: float
    ) -> None:
        # Fetch controller index and return if not found.
        controller_index: int
        try:
            controller_index = self.controllers.index(controller)
        except:
            return

        self.sticks[controller_index][stick] = (
            xvalue if xvalue < -self.__threshold or xvalue > self.__threshold else 0.0,
            yvalue if yvalue < -self.__threshold or yvalue > self.__threshold else 0.0
        )

    def on_trigger_motion(
        self,
        controller: pyglet.input.Controller,
        trigger: str,
        value: float
    ) -> None:
        # Fetch controller index and return if not found.
        controller_index: int
        try:
            controller_index = self.controllers.index(controller)
        except:
            return

        self.triggers[controller_index][trigger] = value if value > self.__threshold else 0.0
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------

    def __getitem__(self, key: int):
        return self.keys.get(key, False)

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        self.key_presses.clear()

    # ----------------------------------------------------------------------
    # Getters.
    # ----------------------------------------------------------------------
    def get_button(
        self,
        button: ControllerButton,
        controller_index: int = 0,
        default_value: bool = False,
    ) -> bool:
        buttons: dict[str, bool] | None = self.buttons[controller_index] if controller_index < len(self.buttons) else None
        return buttons.get(button, False) if buttons is not None else default_value

    def get_button_presses(
        self,
        button: ControllerButton,
        controller_index: int = 0,
        default_value: bool = False,
    ) -> bool:
        button_presses: dict[str, bool] | None = self.button_presses[controller_index] if controller_index < len(self.button_presses) else None
        return button_presses.get(button, False) if button_presses is not None else default_value

    def get_button_release(
        self,
        button: ControllerButton,
        controller_index: int = 0,
        default_value: bool = False,
    ) -> bool:
        button_releases: dict[str, bool] | None = self.button_releases[controller_index] if controller_index < len(self.button_releases) else None
        return button_releases.get(button, False) if button_releases is not None else default_value

    def get_stick_activation(
        self,
        stick: ControllerStick,
        threshold: float | None = None,
        controller_index: int = 0,
    ) -> bool:
        stick_vec: pm.Vec2 = self.get_stick_vector(
            stick = stick,
            controller_index = controller_index
        )

        return stick_vec.mag > (threshold if threshold is not None else self.__threshold)

    def get_stick_vector(
        self,
        stick: ControllerStick,
        controller_index: int = 0
    ) -> pm.Vec2:
        sticks: dict[str, tuple[float, float]] | None = self.sticks[controller_index] if controller_index < len(self.sticks) else None
        result: tuple[float, float] = sticks.get(stick, (0.0, 0.0)) if sticks is not None else (0.0, 0.0)
        return pm.Vec2(result[0], result[1])

    def get_trigger(
        self,
        trigger: ControllerTrigger,
        controller_index: int = 0
    ) -> float:
        triggers: dict[str, float] | None = self.triggers[controller_index] if controller_index < len(self.triggers) else None
        return triggers.get(trigger, 0.0) > 0.0 if triggers is not None else False

    def get_key_vector(
        self,
        up: int = pyglet.window.key.W,
        left: int = pyglet.window.key.A,
        down: int = pyglet.window.key.S,
        right: int = pyglet.window.key.D
    ) -> pm.Vec2:
        """
        Returns a vector
        """

        keyboard_vec: pyglet.math.Vec2 = pyglet.math.Vec2(
            self[right] - self[left],
            self[up] - self[down]
        ).from_magnitude(1.0)

        return keyboard_vec.normalize()

    def get_modifier(
        self,
        controller_index: int = 0
    ) -> bool:
        """
        Returns whether or not the modifier key is being pressed, either on controller or keyboard.
        """

        buttons: dict[str, bool] | None = self.buttons[controller_index] if controller_index < len(self.buttons) else None

        return self[pyglet.window.key.LSHIFT] or (buttons.get("leftshoulder", False) if buttons is not None else False)

    def get_sprint(
        self,
        controller_index: int = 0
    ) -> bool:
        """
        Returns whether the sprint button was pressed or not, either on controller or keyboard.
        """

        button_presses: dict[str, bool] | None = self.button_presses[controller_index] if controller_index < len(self.button_presses) else None

        return self.key_presses.get(pyglet.window.key.SPACE, False) or (button_presses.get("b", False) if button_presses is not None else False)

    def get_interaction(
        self,
        controller_index: int = 0
    ) -> bool:
        """
        Returns whether the interact button was pressed or not, either on controller or keyboard.
        """

        button_presses: dict[str, bool] | None = self.button_presses[controller_index] if controller_index < len(self.button_presses) else None

        return self.key_presses.get(pyglet.window.key.F, False) or self.key_presses.get(pyglet.window.key.H, False) or (button_presses.get("a", False) if button_presses is not None else False)

    def get_main_atk(
        self,
        controller_index: int = 0
    ) -> bool:
        """
        Returns whether the main attack button was pressed or not, either on controller or keyboard.
        """

        button_presses: dict[str, bool] | None = self.button_presses[controller_index] if controller_index < len(self.button_presses) else None

        return self.key_presses.get(pyglet.window.key.M, False) or (button_presses.get("x", False) if button_presses is not None else False)

    def get_secondary_atk(
        self,
        controller_index: int = 0
    ) -> bool:
        """
        Returns whether the secondary attack button was pressed or not, either on controller or keyboard.
        """

        button_presses: dict[str, bool] | None = self.button_presses[controller_index] if controller_index < len(self.button_presses) else None

        return self.key_presses.get(pyglet.window.key.K, False) or (button_presses.get("y", False) if button_presses is not None else False)

    def get_fire_aim(
        self,
        controller_index: int = 0
    ) -> bool:
        """
        Returns whether the range attack aim button was pressed or not.
        """

        triggers: dict[str, float] | None = self.triggers[controller_index] if controller_index < len(self.triggers) else None

        return triggers.get("lefttrigger", 0.0) > 0.0 if triggers is not None else False

    def get_fire_load(
        self,
        controller_index: int = 0
    ) -> bool:
        """
        Returns whether the range attack load button was pressed or not.
        """

        triggers: dict[str, float] | None = self.triggers[controller_index] if controller_index < len(self.triggers) else None

        return triggers.get("righttrigger", 0.0) > 0.0 if triggers is not None else False

    def get_movement(
        self,
        controller_index: int = 0
    ) -> bool:
        """
        Returns whether there's any move input or not, regardless its resulting magnitude.
        """

        sticks: dict[str, tuple[float, float]] | None = self.sticks[controller_index] if controller_index < len(self.sticks) else None

        stick: tuple[float, float] = (sticks.get("leftstick", (0.0, 0.0)) if sticks is not None else (0.0, 0.0))
        stick_vec: pyglet.math.Vec2 = pyglet.math.Vec2(stick[0], stick[1])
        return self[pyglet.window.key.D] or self[pyglet.window.key.A] or self[pyglet.window.key.W] or self[pyglet.window.key.S] or stick_vec.mag > 0.0

    def get_aim(
        self,
        controller_index: int = 0
    ) -> bool:
        """
        Returns whether there's any aim input or not, regardless its resulting magnitude.
        """

        sticks: dict[str, tuple[float, float]] | None = self.sticks[controller_index] if controller_index < len(self.sticks) else None

        stick: tuple[float, float] = (sticks.get("rightstick", (0.0, 0.0)) if sticks is not None else (0.0, 0.0))
        stick_vec: pyglet.math.Vec2 = pyglet.math.Vec2(stick[0], stick[1])
        return self[pyglet.window.key.L] or self[pyglet.window.key.J] or self[pyglet.window.key.I] or self[pyglet.window.key.K] or stick_vec.mag > 0.0

    def get_movement_vec(
        self,
        controller_index: int = 0
    ) -> pyglet.math.Vec2:
        """
        Returns the movement vector from keyboard and controller.
        """

        sticks: dict[str, tuple[float, float]] | None = self.sticks[controller_index] if controller_index < len(self.sticks) else None

        stick: tuple[float, float] = (sticks.get("leftstick", (0.0, 0.0)) if sticks is not None else (0.0, 0.0))
        stick_vec: pyglet.math.Vec2 = pyglet.math.Vec2(stick[0], stick[1])
        keyboard_vec: pyglet.math.Vec2 = pyglet.math.Vec2(
            self[pyglet.window.key.D] - self[pyglet.window.key.A],
            self[pyglet.window.key.W] - self[pyglet.window.key.S]
        ).from_magnitude(1.0)

        return (stick_vec + keyboard_vec).normalize()

    def get_aim_vec(
        self,
        controller_index: int = 0
    ) -> pyglet.math.Vec2:
        """
        Returns the camera movement vector from keyboard and controller.
        """

        sticks: dict[str, tuple[float, float]] | None = self.sticks[controller_index] if controller_index < len(self.sticks) else None

        stick: tuple[float, float] = (sticks.get("rightstick", (0.0, 0.0)) if sticks is not None else (0.0, 0.0))
        stick_vec: pyglet.math.Vec2 = pyglet.math.Vec2(stick[0], stick[1])
        keyboard_vec: pyglet.math.Vec2 = pyglet.math.Vec2(
            self[pyglet.window.key.L] - self[pyglet.window.key.J],
            self[pyglet.window.key.I] - self[pyglet.window.key.K]
        ).from_magnitude(1.0)

        return (stick_vec + keyboard_vec).normalize()

    def get_cursor_movement_press(
        self,
        up_keys: list[int],
        left_keys: list[int],
        down_keys: list[int],
        right_keys: list[int]
    ) -> bool:
        """
        Returns whether the cursor movement is being started or not given the provided keys.
        """

        up: bool = reduce(lambda a, b: a or b, map(lambda element: self.key_presses.get(element, False), up_keys))
        left: bool = reduce(lambda a, b: a or b, map(lambda element: self.key_presses.get(element, False), left_keys))
        down: bool = reduce(lambda a, b: a or b, map(lambda element: self.key_presses.get(element, False), down_keys))
        right: bool = reduce(lambda a, b: a or b, map(lambda element: self.key_presses.get(element, False), right_keys))

        return up or left or down or right

    def get_cursor_movement_release(
        self,
        up_keys: list[int],
        left_keys: list[int],
        down_keys: list[int],
        right_keys: list[int]
    ) -> bool:
        """
        Returns whether the cursor movement is being ended or not.
        """

        up: bool = reduce(lambda a, b: a and b, map(lambda element: not self[element], up_keys))
        left: bool = reduce(lambda a, b: a and b, map(lambda element: not self[element], left_keys))
        down: bool = reduce(lambda a, b: a and b, map(lambda element: not self[element], down_keys))
        right: bool = reduce(lambda a, b: a and b, map(lambda element: not self[element], right_keys))

        return up and left and down and right

    def get_cursor_movement_vec(
        self,
        up_keys: list[int],
        left_keys: list[int],
        down_keys: list[int],
        right_keys: list[int]
    ) -> pyglet.math.Vec2:
        """
        Returns the movement vector from keyboard and controller.
        """

        up: bool = reduce(lambda a, b: a or b, map(lambda element: self[element], up_keys))
        left: bool = reduce(lambda a, b: a or b, map(lambda element: self[element], left_keys))
        down: bool = reduce(lambda a, b: a or b, map(lambda element: self[element], down_keys))
        right: bool = reduce(lambda a, b: a or b, map(lambda element: self[element], right_keys))

        return pyglet.math.Vec2(
            1 if right else 0 - 1 if left else 0,
            1 if up else 0 - 1 if down else 0
        )

    def get_ctrl(self) -> bool:
        return self[pyglet.window.key.LCTRL] or self[pyglet.window.key.LCOMMAND] or self[pyglet.window.key.RCTRL] or self[pyglet.window.key.RCOMMAND]

    def get_shift(self) -> bool:
        return self[pyglet.window.key.LSHIFT] or self[pyglet.window.key.RSHIFT]

    def get_tool_run(self) -> bool:
        return self.key_presses.get(pyglet.window.key.SPACE, False)

    def get_tool_clear(self) -> bool:
        return self.get_shift() and self.get_tool_run()

    def get_tool_alt(self) -> bool:
        """
        Returns whether the tool alternate mode key is being pressed or not.
        """

        return self[pyglet.window.key.RSHIFT]

    def get_start(self) -> bool:
        return self.key_presses.get(pyglet.window.key.ENTER, False)

    def get_undo(self) -> bool:
        return self.key_presses.get(pyglet.window.key.BACKSPACE, False)

    def get_redo(self) -> bool:
        return self.get_shift() and self.get_undo()

    def get_switch(self) -> bool:
        return self.key_presses.get(pyglet.window.key.TAB, False)

    def get_menu_page_left(self) -> bool:
        return self.key_presses.get(pyglet.window.key.Q, False)

    def get_menu_page_right(self) -> bool:
        return self.key_presses.get(pyglet.window.key.E, False)

    def get_draw(
        self,
        controller_index: int = 0
    ) -> bool:
        """
        Returns whether the draw button was pressed or not, either on controller or keyboard.
        """

        triggers: dict[str, float] | None = self.triggers[controller_index] if controller_index < len(self.triggers) else None

        return self[pyglet.window.key.SPACE] or (triggers.get("righttrigger", 0.0) > 0.0 if triggers is not None else False)

    def get_inventory_toggle(
        self,
        controller_index: int = 0
    ) -> bool:
        """
        Returns whether the inventory toggle button was pressed or not.
        """

        button_presses: dict[str, bool] | None = self.button_presses[controller_index] if controller_index < len(self.button_presses) else None

        return self.key_presses.get(pyglet.window.key.ENTER, False) or (button_presses.get("start", False) if button_presses is not None else False)