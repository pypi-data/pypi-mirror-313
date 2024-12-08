from __future__ import annotations
import asyncio
import json
import logging
import pathlib
import typing
import warnings
from typing import List, Union, Optional, Tuple
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Set

import zendriver_flare_bypasser.core.browser
from . import element
from . import util
from .util import merge_dict, key_definitions
from .config import PathLike
from .connection import Connection, ProtocolException
from .. import cdp

class Keyboard:
    def __init__(self, tab: 'Tab') -> None:
        self.tab = tab
        self._modifiers = 0
        self._pressed_keys: Set[str] = set()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def down(self, key: str, options: dict = None, **kwargs: Any) -> None:
        """Dispatch a ``keydown`` event with ``key``."""
        options = merge_dict(options, kwargs)

        description = self._key_description_for_string(key)
        autoRepeat = description['code'] in self._pressed_keys
        self._pressed_keys.add(description['code'])
        self._modifiers |= self._modifier_bit(description['key'])

        text = options.get('text')
        if text is None:
            text = description['text']

        await self.tab.send(cdp.input_.dispatch_key_event(
            type_ = "keyDown" if text else "rawKeyDown",
            modifiers = self._modifiers,
            windows_virtual_key_code = description['keyCode'],
            code = description['code'],
            key = description['key'],
            text = text,
            unmodified_text = text,
            auto_repeat = autoRepeat,
            location = description['location'],
            is_keypad = description['location'] == 3,
        ))

    def _modifier_bit(self, key: str) -> int:
        if key == 'Alt':
            return 1
        if key == 'Control':
            return 2
        if key == 'Meta':
            return 4
        if key == 'Shift':
            return 8
        return 0

    def _key_description_for_string(self, keyString: str) -> Dict:  # noqa: C901
        shift = self._modifiers & 8
        description = {
            'key': '',
            'keyCode': 0,
            'code': '',
            'text': '',
            'location': 0,
        }

        definition: Dict = key_definitions.get(keyString)  # type: ignore
        if not definition:
            raise Exception(f'Unknown key: {keyString}')

        if 'key' in definition:
            description['key'] = definition['key']
        if shift and definition.get('shiftKey'):
            description['key'] = definition['shiftKey']

        if 'keyCode' in definition:
            description['keyCode'] = definition['keyCode']
        if shift and definition.get('shiftKeyCode'):
            description['keyCode'] = definition['shiftKeyCode']

        if 'code' in definition:
            description['code'] = definition['code']

        if 'location' in definition:
            description['location'] = definition['location']

        if len(description['key']) == 1:  # type: ignore
            description['text'] = description['key']

        if 'text' in definition:
            description['text'] = definition['text']
        if shift and definition.get('shiftText'):
            description['text'] = definition['shiftText']

        if self._modifiers & ~8:
            description['text'] = ''

        return description

    async def up(self, key: str) -> None:
        """Dispatch a ``keyup`` event of the ``key``."""
        description = self._key_description_for_string(key)

        self._modifiers &= ~self._modifier_bit(description['key'])
        if description['code'] in self._pressed_keys:
            self._pressed_keys.remove(description['code'])
        await self.tab.send(cdp.input_.dispatch_key_event(
            type_ = "keyUp",
            modifiers = self._modifiers,
            key = description['key'],
            windows_virtual_key_code = description['keyCode'],
            code = description['code'],
            location = description['location'],
        ))

    async def send_character(self, char: str) -> None:
        """Send character into the page."""
        await self.tab.send(cdp.input_.insert_text(char))

    async def type(self, text: str, options: Dict = None, **kwargs: Any) -> None:
        """Type characters into a focused element."""
        options = merge_dict(options, kwargs)
        delay = options.get('delay', 0)
        for char in text:
            if char in key_definitions:
                await self.press(char, {'delay': delay})
            else:
                await self.send_character(char)
            if delay:
                await asyncio.sleep(delay / 1000)

    async def press(self, key: str, options: Dict = None, **kwargs: Any) -> None:
        """Press ``key``."""
        options = merge_dict(options, kwargs)

        await self.down(key, options)
        if 'delay' in options:
            await asyncio.sleep(options['delay'] / 1000)
        await self.up(key)

class Mouse:
    """Mouse class.

    The :class:`Mouse` operates in main-frame CSS pixels relative to the
    top-left corner of the viewport.
    """

    def __init__(self, tab: 'Tab') -> None:
        self.tab = tab
        self._x = 0.0
        self._y = 0.0
        self._button = 'none'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def move(self, x: float, y: float, options: dict = None,
                **kwargs: Any) -> None:
        """Move mouse cursor (dispatches a ``mousemove`` event).

        Options can accepts ``steps`` (int) field. If this ``steps`` option
        specified, Sends intermediate ``mousemove`` events. Defaults to 1.
        """
        options = merge_dict(options, kwargs)
        from_x = self._x
        from_y = self._y
        self._x = float(x)
        self._y = float(y)
        steps = options.get('steps', 1)
        for i in range(1, steps + 1):
            x = round(from_x + (self._x - from_x) * (i / steps))
            y = round(from_y + (self._y - from_y) * (i / steps))
            await self.tab.send(cdp.input_.dispatch_mouse_event(
                type_ = 'mouseMoved',
                x = x,
                y = y,
                modifiers = self.tab.keyboard._modifiers,
                button = cdp.input_.MouseButton(self._button),
            ))

    async def click(self, x: float, y: float, options: dict = None,
                    **kwargs: Any) -> None:
        """Click button at (``x``, ``y``).

        Shortcut to :meth:`move`, :meth:`down`, and :meth:`up`.

        This method accepts the following options:

        * ``button`` (str): ``left``, ``right``, or ``middle``, defaults to
        ``left``.
        * ``clickCount`` (int): defaults to 1.
        * ``delay`` (int|float): Time to wait between ``mousedown`` and
        ``mouseup`` in milliseconds. Defaults to 0.
        """
        options = merge_dict(options, kwargs)
        await self.move(x, y)
        await self.down(options)
        if options and options.get('delay'):
            await asyncio.sleep(options.get('delay', 0) / 1000)
        await self.up(options)

    async def down(self, options: dict = None, **kwargs: Any) -> None:
        """Press down button (dispatches ``mousedown`` event).

        This method accepts the following options:

        * ``button`` (str): ``left``, ``right``, or ``middle``, defaults to
        ``left``.
        * ``clickCount`` (int): defaults to 1.
        """
        options = merge_dict(options, kwargs)
        self._button = options.get('button', 'left')
        await self.tab.send(cdp.input_.dispatch_mouse_event(
            type_ = 'mousePressed',
            button = cdp.input_.MouseButton(self._button),
            x = self._x,
            y = self._y,
            modifiers = self.tab.keyboard._modifiers,
            click_count = options.get('clickCount') or 1,
        ))

    async def up(self, options: dict = None, **kwargs: Any) -> None:
        """Release pressed button (dispatches ``mouseup`` event).

        This method accepts the following options:

        * ``button`` (str): ``left``, ``right``, or ``middle``, defaults to
        ``left``.
        * ``clickCount`` (int): defaults to 1.
        """
        options = merge_dict(options, kwargs)
        self._button = 'none'
        await self.tab.send(cdp.input_.dispatch_mouse_event(
            type_ = 'mouseReleased',
            button = cdp.input_.MouseButton(options.get('button', 'left')),
            x = self._x,
            y = self._y,
            modifiers = self.tab.keyboard._modifiers,
            click_count = options.get('clickCount') or 1,
        ))

class Touchscreen:
    """Touchscreen class."""

    def __init__(self, tab: 'Tab') -> None:
        """Make new touchscreen object."""
        self.tab = tab

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def tap(self, x: float, y: float) -> None:
        """Tap (``x``, ``y``).

        Dispatches a ``touchstart`` and ``touchend`` event.
        """
        touch_points = [{'x': round(x), 'y': round(y)}]
        await self.tab.send(cdp.input_.dispatch_touch_event(
            type_ = 'touchStart',
            touch_points = touch_points,
            modifiers = self.tab.keyboard._modifiers,
        ))
        await self.tab.send(cdp.input_.dispatch_touch_event(
            type_ = 'touchEnd',
            touch_points = [],
            modifiers = self.tab.keyboard._modifiers,
        ))
