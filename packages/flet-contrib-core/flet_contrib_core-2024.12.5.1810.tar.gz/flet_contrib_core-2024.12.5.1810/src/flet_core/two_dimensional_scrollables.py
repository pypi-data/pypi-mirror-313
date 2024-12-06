from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ImageFit,
)


class TwoDimensionalScrollablesControl(ConstrainedControl):
    """
    Custom control for Flet to handle two-dimensional scrollable areas.


    -----

    Online docs: https://flet.dev/docs/controls/two_dimensional_scrollables_control
    """

    def __init__(
        self,
        current_action: Optional[str]= "",
        current_cell: Optional[str] = "",
        cell_content: Optional[str] = "",
        column_widths: Optional[str] = "",
        on_change=None,

        
        
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
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
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
            rtl=rtl,
        )

        
        self.current_action = current_action
        self.current_cell = current_cell 
        self.cell_content = cell_content
        self.column_widths = column_widths
        self.on_change = on_change
        
        
    def _get_control_name(self):
        return "two_dimensional_scrollables"

    # Implement properties and setters    

    
    @property
    def current_action(self):
        return self._get_attr("currentAction")

    @current_action.setter
    def current_action(self, value):
        self._set_attr("currentAction", value)
    
    @property
    def current_cell(self):
        return self._get_attr("currentCell")

    @current_cell.setter
    def current_cell(self, value):
        self._set_attr("currentCell", value)

    @property
    def cell_content(self):
        return self._get_attr("cellContent")

    @cell_content.setter
    def cell_content(self, value):
        self._set_attr("cellContent", value)
    

    @property
    def column_widths(self):
        return self._get_attr("columnWidths")

    @column_widths.setter
    def column_widths(self, value):
        self._set_attr("columnWidths", value)
    
    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

   
  