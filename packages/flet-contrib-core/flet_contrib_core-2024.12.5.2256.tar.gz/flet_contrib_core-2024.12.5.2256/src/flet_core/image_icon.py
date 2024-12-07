from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    BlendMode,
    BorderRadiusValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalEventCallable,
)
from flet_core.video import FilterQuality

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class ImageIcon(ConstrainedControl):
    """
    A control that displays an image icon.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "ImageIcon Example"

        icon = ft.ImageIcon(
            src=f"/icons/icon-512.png",
            size=100,
            color="blue",
        )

        page.add(icon)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/imageicon
    """

    def __init__(
        self,
        src: Optional[str] = None,
        src_base64: Optional[str] = None,
        semantics_label: Optional[str] = None,
        color: Optional[str] = None,
        size: OptionalNumber = None,
        on_click: OptionalEventCallable = None,

        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end: OptionalEventCallable = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.src = src
        self.src_base64 = src_base64
        self.color = color
        self.size = size
        self.semantics_label = semantics_label
        self.on_click = on_click


    def _get_control_name(self):
        return "image_icon"

    # src
    @property
    def src(self):
        return self._get_attr("src")

    @src.setter
    def src(self, value: Optional[str]):
        self._set_attr("src", value)

    # src_base64
    @property
    def src_base64(self):
        return self._get_attr("srcBase64")

    @src_base64.setter
    def src_base64(self, value: Optional[str]):
        self._set_attr("srcBase64", value)

    # color
    @property
    def color(self) -> Optional[str]:
        return self._get_attr("color")

    @color.setter
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

    # size
    @property
    def size(self) -> OptionalNumber:
        return self._get_attr("size", data_type="float")

    @size.setter
    def size(self, value: OptionalNumber):
        self._set_attr("size", value)

    # semantics_label
    @property
    def semantics_label(self) -> Optional[str]:
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value: Optional[str]):
        self._set_attr("semanticsLabel", value)
    
    # on_click
    @property
    def on_click(self) -> OptionalEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalEventCallable):
        self._add_event_handler("click", handler)
