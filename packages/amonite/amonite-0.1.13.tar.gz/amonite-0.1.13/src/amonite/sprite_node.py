from typing import Callable
import pyglet
import pyglet.gl as gl

from amonite.shaded_sprite import ShadedSprite
from amonite.node import PositionNode
from amonite.settings import GLOBALS, Keys
from amonite.utils import utils

class SpriteNode(PositionNode):
    """
    Base sprite node. Holds a single sprite and handles its position and shader.

    Attributes
    ----------
    resource: pyglet.image.Texture | pyglet.image.animation.Animation
        The image resource to provide the sprite with.
    batch: pyglet.graphics.Batch | None
        The batch to use when rendering the sprite.
    on_animation_end: Callable | None
        A callback function which gets called when any sprite animation ends.
    y_sort: bool
        Whether to sort the sprite using its y position or not.
    x: float
        The sprite x position.
    y: float
        The sprite y position.
    z: float | None
        The sprite z position.
    shader: pyglet.graphics.shader.ShaderProgram | None
        The shader program to use to render the sprite.
    samplers_2d: dict[str, pyglet.image.ImageData] | None
        The list of samplers2d as required by the provided shader program.
    """

    def __init__(
        self,
        resource: pyglet.image.Texture | pyglet.image.animation.Animation,
        batch: pyglet.graphics.Batch | None = None,
        on_animation_end: Callable | None = None,
        y_sort: bool = True,
        x: float = 0,
        y: float = 0,
        z: float = 0,
        shader: pyglet.graphics.shader.ShaderProgram | None = None,
        samplers_2d: dict[str, pyglet.image.ImageData] | None = None,
    ) -> None:
        super().__init__(
            x = x,
            y = y,
            z = z
        )

        self.__y_sort: bool = y_sort

        # Make sure the given resource is filtered using a nearest neighbor filter.
        utils.set_filter(resource = resource, filter = gl.GL_NEAREST)

        self.sprite = ShadedSprite(
            img = resource,
            x = x * GLOBALS[Keys.SCALING],
            y = y * GLOBALS[Keys.SCALING],
            z = -y if y_sort else z,
            program = shader,
            samplers_2d = samplers_2d,
            batch = batch
        )
        self.sprite.scale = GLOBALS[Keys.SCALING]
        self.sprite.push_handlers(self)

        self.__on_animation_end = on_animation_end

    def delete(self) -> None:
        self.sprite.delete()

    def get_image(self):
        return self.sprite.image

    def set_position(
        self,
        position: tuple[float, float],
        z: float | None = None
    ) -> None:
        super().set_position(
            position = position,
            z = -position[1] if self.__y_sort else z if z is not None else self.z
        )

        self.sprite.position = (
            self.x * GLOBALS[Keys.SCALING],
            self.y * GLOBALS[Keys.SCALING],
            self.z
        )

    def set_scale(
        self,
        x_scale: int | None = None,
        y_scale: int | None = None
    ) -> None:
        if x_scale is not None:
            self.sprite.scale_x = x_scale

        if y_scale is not None:
            self.sprite.scale_y = y_scale

    def set_image(
        self,
        image: pyglet.image.Texture | pyglet.image.animation.Animation
    ) -> None:
        self.sprite.image = image

    def get_frames_num(self) -> int:
        """
        Returns the amount of frames in the current animation.
        Always returns 0 if the sprite image is not an animation.
        """

        return self.sprite.get_frames_num()

    def get_frame_index(self) -> int:
        """
        Returns the current animation frame.
        Always returns 0 if the sprite image is not an animation.
        """
        return self.sprite.get_frame_index()

    def on_animation_end(self):
        if self.__on_animation_end is not None:
            self.__on_animation_end()

    def draw(self) -> None:
        self.sprite.draw()

    def get_bounding_box(self):
        if isinstance(self.sprite.image, pyglet.image.TextureRegion):
            return (
                self.sprite.x - self.sprite.image.anchor_x * GLOBALS[Keys.SCALING],
                self.sprite.y - self.sprite.image.anchor_y * GLOBALS[Keys.SCALING],
                self.sprite.width,
                self.sprite.height
            )
        elif isinstance(self.sprite.image, pyglet.image.animation.Animation):
            return (
                self.sprite.x - self.sprite.image.frames[0].image.anchor_x * GLOBALS[Keys.SCALING],
                self.sprite.y - self.sprite.image.frames[0].image.anchor_y * GLOBALS[Keys.SCALING],
                self.sprite.width,
                self.sprite.height
            )

        return super().get_bounding_box()