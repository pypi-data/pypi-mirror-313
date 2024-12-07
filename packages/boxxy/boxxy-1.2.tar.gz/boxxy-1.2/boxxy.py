__version__ = '1.2'


import enum
from typing import Iterable
import unicodedata
from dataclasses import dataclass


__all__ = [
    'BoxChar',
    'Padding',
    'HAlign',
    'VAlign',
    'BoxCanvas',
    'TableCell',
    'Table',
]


if hasattr(enum, 'KEEP'):
    _enum_kwargs = dict(boundary=enum.KEEP)
else:
    _enum_kwargs = {}


class BoxChar(enum.Flag, **_enum_kwargs):
    SPACE = 0
    #
    LEFT = 1
    UP = 2
    RIGHT = 4
    DOWN = 8
    #
    LEFT_DOUBLE = 1 + 16
    UP_DOUBLE = 2 + 32
    RIGHT_DOUBLE = 4 + 64
    DOWN_DOUBLE = 8 + 128
    #
    HORIZONTAL = LEFT | RIGHT
    VERTICAL = UP | DOWN
    #
    DOWN_AND_RIGHT = DOWN | RIGHT
    DOWN_AND_LEFT = DOWN | LEFT
    UP_AND_RIGHT = UP | RIGHT
    UP_AND_LEFT = UP | LEFT
    #
    VERTICAL_AND_RIGHT = VERTICAL | RIGHT
    VERTICAL_AND_LEFT = VERTICAL | LEFT
    DOWN_AND_HORIZONTAL = DOWN | HORIZONTAL
    UP_AND_HORIZONTAL = UP | HORIZONTAL
    #
    VERTICAL_AND_HORIZONTAL = VERTICAL | HORIZONTAL
    #
    DOUBLE_HORIZONTAL = LEFT_DOUBLE | RIGHT_DOUBLE
    DOUBLE_VERTICAL = UP_DOUBLE | DOWN_DOUBLE
    #
    DOWN_SINGLE_AND_RIGHT_DOUBLE = DOWN | RIGHT_DOUBLE
    DOWN_DOUBLE_AND_RIGHT_SINGLE = DOWN_DOUBLE | RIGHT
    DOUBLE_DOWN_AND_RIGHT = DOWN_DOUBLE | RIGHT_DOUBLE
    #
    DOWN_SINGLE_AND_LEFT_DOUBLE = DOWN | LEFT_DOUBLE
    DOWN_DOUBLE_AND_LEFT_SINGLE = DOWN_DOUBLE | LEFT
    DOUBLE_DOWN_AND_LEFT = DOWN_DOUBLE | LEFT_DOUBLE
    #
    UP_SINGLE_AND_RIGHT_DOUBLE = UP | RIGHT_DOUBLE
    UP_DOUBLE_AND_RIGHT_SINGLE = UP_DOUBLE | RIGHT
    DOUBLE_UP_AND_RIGHT = UP_DOUBLE | RIGHT_DOUBLE
    #
    UP_SINGLE_AND_LEFT_DOUBLE = UP | LEFT_DOUBLE
    UP_DOUBLE_AND_LEFT_SINGLE = UP_DOUBLE | LEFT
    DOUBLE_UP_AND_LEFT = UP_DOUBLE | LEFT_DOUBLE
    #
    VERTICAL_SINGLE_AND_RIGHT_DOUBLE = VERTICAL | RIGHT_DOUBLE
    VERTICAL_DOUBLE_AND_RIGHT_SINGLE = DOUBLE_VERTICAL | RIGHT
    DOUBLE_VERTICAL_AND_RIGHT = DOUBLE_VERTICAL | RIGHT_DOUBLE
    #
    VERTICAL_SINGLE_AND_LEFT_DOUBLE = VERTICAL | LEFT_DOUBLE
    VERTICAL_DOUBLE_AND_LEFT_SINGLE = DOUBLE_VERTICAL | LEFT
    DOUBLE_VERTICAL_AND_LEFT = DOUBLE_VERTICAL | LEFT_DOUBLE
    #
    DOWN_SINGLE_AND_HORIZONTAL_DOUBLE = DOWN | DOUBLE_HORIZONTAL
    DOWN_DOUBLE_AND_HORIZONTAL_SINGLE = DOWN_DOUBLE | HORIZONTAL
    DOUBLE_DOWN_AND_HORIZONTAL = DOWN_DOUBLE | DOUBLE_HORIZONTAL
    #
    UP_SINGLE_AND_HORIZONTAL_DOUBLE = UP | DOUBLE_HORIZONTAL
    UP_DOUBLE_AND_HORIZONTAL_SINGLE = UP_DOUBLE | HORIZONTAL
    DOUBLE_UP_AND_HORIZONTAL = UP_DOUBLE | DOUBLE_HORIZONTAL
    #
    VERTICAL_SINGLE_AND_HORIZONTAL_DOUBLE = VERTICAL | DOUBLE_HORIZONTAL
    VERTICAL_DOUBLE_AND_HORIZONTAL_SINGLE = DOUBLE_VERTICAL | HORIZONTAL
    DOUBLE_VERTICAL_AND_HORIZONTAL = DOUBLE_VERTICAL | DOUBLE_HORIZONTAL

    @property
    def unicode_name(self):
        """
        Get the unicode character name corresponding to this value.

        Note that some values will return a name that does not correspond to a valid unicode character.
        In particular: DOUBLE_RIGHT, DOUBLE_UP, etc., since these were not included in the box drawings block.
        """
        if self == BoxChar.SPACE:
            return 'SPACE'
        #
        name = 'BOX DRAWINGS '
        if (self & BoxChar.VERTICAL_AND_HORIZONTAL) == self:
            name += 'LIGHT '
        name += self.name.replace('_', ' ')
        return name

    def __str__(self):
        """
        Look up and return the unicode character corresponding to this value.
        If not found (unicodedata.lookup throws a KeyError), then the unicode replacement character will be returned.
        """
        try:
            return unicodedata.lookup(self.unicode_name)
        except KeyError:
            return '�'


class Padding:
    left: int
    up: int
    right: int
    down: int

    @property
    def width(self):
        return self.left + self.right

    @property
    def height(self):
        return self.up + self.down

    def __init__(self, *args: int):
        if len(args) == 0:
            self.left = self.up = self.right = self.down = 0
        elif len(args) == 1:
            self.left = self.up = self.right = self.down = args[0]
        elif len(args) == 2:
            self.left = self.right = args[0]
            self.up = self.down = args[1]
        elif len(args) == 4:
            self.left, self.up, self.right, self.down = args
        else:
            raise Exception(f'Padding() expects 0, 1, 2, or 4 arguments. Got {len(args)}.')


class HAlign(enum.Enum):
    Left = 'left'
    Center = 'center'
    Right = 'right'


class VAlign(enum.Enum):
    Top = 'top'
    Middle = 'middle'
    Bottom = 'bottom'


class BoxCanvas:
    background_char: str = ' '
    default_fill_char: str = ' '
    default_h_align: HAlign = HAlign.Left
    default_v_align: VAlign = VAlign.Top
    default_align_char: str = ' '
    default_padding: Padding = Padding(1, 0)

    def __init__(self):
        self._width = 0
        self._height = 0
        self._canvas: list[BoxChar | str | None] = []

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def __getitem__(self, index: tuple[int, int]) -> BoxChar | str | None:
        x, y = index
        if 0 <= x < self.width and 0 <= y < self.height:
            return self._canvas[y][x]

    def __setitem__(self, index: tuple[int, int], value: BoxChar | str | None):
        x, y = index
        if x < 0 or y < 0:
            return
        self.expand(x + 1, y + 1)
        self._canvas[y][x] = value

    def __str__(self):
        return '\n'.join(self.get_lines())

    def get_lines(self):
        for row in self._canvas:
            line = ''
            for cell in row:
                if cell is None:
                    line += self.background_char
                else:
                    line += str(cell)
            yield line

    def expand(self, w: int, h: int):
        if w > self.width:
            for row in self._canvas:
                row += [None] * (w - self.width)
            self._width = w
        if h > self.height:
            for _ in range(h - self.height):
                self._canvas.append([None] * self.width)
            self._height = h

    def or_boxchar(self, x: int, y: int, item: BoxChar):
        current = self[x, y]
        if isinstance(current, BoxChar):
            self[x, y] = current | item
        else:
            self[x, y] = item

    def and_boxchar(self, x: int, y: int, item: BoxChar):
        current = self[x, y]
        if isinstance(current, BoxChar):
            self[x, y] = current & item

    def remove_boxchar(self, x: int, y: int, item: BoxChar):
        self.and_boxchar(x, y, ~item)

    def draw_horizontal(self, x: int, y: int, w: int, double: bool = False):
        right = BoxChar.RIGHT_DOUBLE if double else BoxChar.RIGHT
        left = BoxChar.LEFT_DOUBLE if double else BoxChar.LEFT
        for x_ in range(x, x + w - 1):
            self.or_boxchar(x_, y, right)
            self.or_boxchar(x_ + 1, y, left)

    def draw_vertical(self, x: int, y: int, h: int, double: bool = False):
        down = BoxChar.DOWN_DOUBLE if double else BoxChar.DOWN
        up = BoxChar.UP_DOUBLE if double else BoxChar.UP
        for y_ in range(y, y + h - 1):
            self.or_boxchar(x, y_, down)
            self.or_boxchar(x, y_ + 1, up)

    def clear_rect(self, x: int, y: int, w: int, h: int, fill: str | None = None):
        assert fill is None or isinstance(fill, str) and len(fill) == 1
        left = max(0, x)
        right = min(self.width, x + w)
        top = max(0, y)
        bottom = min(self.height, y + h)
        for x_ in range(left, right):
            for y_ in range(top, bottom):
                self[x_, y_] = fill

    def clear_box(self, x: int, y: int, w: int, h: int, fill: str | None = None):
        self.clear_rect(x + 1, y + 1, w - 2, h - 2, fill)
        for x_ in range(x, x + w):
            self.remove_boxchar(x_, y, BoxChar.DOWN_DOUBLE)
            self.remove_boxchar(x_, y + h - 1, BoxChar.UP_DOUBLE)
        for y_ in range(y, y + h):
            self.remove_boxchar(x, y_, BoxChar.RIGHT_DOUBLE)
            self.remove_boxchar(x + w - 1, y_, BoxChar.LEFT_DOUBLE)

    def draw_box(self,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 *,
                 double_top: bool = False,
                 double_bottom: bool = False,
                 double_left: bool = False,
                 double_right: bool = False,
                 double_all: bool = False,
                 fill: str | bool = False,
                 ):
        """
        Draw a box.

        By default, this will be a single-line rectangle, but some or all edges may be drawn with doubled lines if
        specified via keyword arguments.

        If :param:`fill` is False (the default), the inside of the box will be unmodified, meaning existing text will
        be left alone, and existing borders will be combined with the new ones. If :param:`fill` is a one-character
        string then the inside will instead be filled with this character, and existing borders will be adjusted to
        not continue into the box. If :param:`fill` is True, this is equivalent to calling with `default_fill_char`
        as the `fill` parameter.

        :param x: X coordinate of upper left corner.
        :param y: Y coordinate of upper left corner.
        :param w: Width of box, including border.
        :param h: Height of box, including border.
        :param double_top: Draw the top edge with double lines.
        :param double_bottom: Draw the bottom edge with double lines.
        :param double_left: Draw the left edge with double lines.
        :param double_right: Draw the right edge with double lines.
        :param double_all: Draw all edges with double lines.
        :param fill: Fill the inside of the box with empty space.
        """
        self.expand(x + w - 1, y + h - 1)
        if fill is not False:
            self.clear_box(x, y, w, h, self.default_fill_char if fill is True else fill)
        self.draw_horizontal(x, y, w, double_top or double_all)
        self.draw_horizontal(x, y + h - 1, w, double_bottom or double_all)
        self.draw_vertical(x, y, h, double_left or double_all)
        self.draw_vertical(x + w - 1, y, h, double_right or double_all)

    def fit_text(self, text, *, padding: Padding | None = None):
        """
        Figure out the size of the box required to fit around the given text.
        :param text: Text to be drawn.
        :param padding: Optional padding. Will use BoxCanvas.default_padding if None (the default).
        :return: A tuple (width, height) of the box that fits around the given text.
        """
        if padding is None:
            padding = self.default_padding
        lines = text.splitlines()
        w = max(map(len, lines), default=0) + 2 + padding.width
        h = len(lines) + 2 + padding.height
        return w, h

    def text_box(self,
                 x: int,
                 y: int,
                 text: str,
                 *,
                 width: int | None = None,
                 height: int | None = None,
                 h_align: HAlign | None = None,
                 v_align: VAlign | None = None,
                 align_char: str | None = None,
                 padding: Padding | None = None,
                 fill_char: str | None = None,
                 **kwargs
                 ) -> tuple[int, int]:
        """
        Draw a box and write text inside it.

        If `width` and/or `height` is `None` (which is the default), then the missing value(s) will be calculated
        by `fit_text()`.

        If `width` and/or `height` is given, and the text extends outside the available space, then the text will
        be clipped. The available space is the width and/or height, minus one character on each side for the border,
        minus padding.

        :param x: X coordinate of upper left corner of the box.
        :param y: Y coordinate of upper left corner of the box.
        :param text: Text to be written inside the box.
        :param width: Width of the drawn box, including border and padding, or `None` to auto-fit.
        :param height: Height of the drawn box, including border and padding, or `None` to auto-fit.
        :param fill_char: Character used to fill the box. Will use `default_fill_char` if `None`.
        :param h_align: Horizontal text alignment inside the box. Will use `default_h_align` if `None`.
        :param v_align: Vertical text alignment inside the box. Will use `default_v_align` if `None`.
        :param align_char: Padding character to use when adjusting text. Will use `default_align_char` if `None`.
        :param padding: Optional padding. Will use `default_padding` if `None`.
        :param kwargs: Additional keyword arguments are passed to `draw_box()`, such as `double_all`.
        :returns: A tuple (width, height) of the final box size, including padding and borders.
        """

        # Apply defaults.
        h_align = h_align or self.default_h_align
        v_align = v_align or self.default_v_align
        align_char = align_char or self.default_align_char
        padding = padding or self.default_padding

        # Auto-fit width and/or height if not given.
        fit_w, fit_h = self.fit_text(text, padding=padding)
        width = width or fit_w
        height = height or fit_h

        # Draw the box.
        self.draw_box(x, y, width, height, fill=fill_char, **kwargs)

        # Figure out what out text lines are going to be.
        lines = text.splitlines()
        max_lines = height - 2 - padding.height
        height_diff = max_lines - len(lines)
        if height_diff < 0:
            # Truncate lines past what we can fit.
            lines = lines[:max_lines]
        elif height_diff > 0:
            # Apply vertical alignment.
            if v_align == VAlign.Top:
                pad_top = 0
            elif v_align == VAlign.Middle:
                pad_top = height_diff // 2
            else:
                pad_top = height_diff
            lines = [''] * pad_top + lines + [''] * (height_diff - pad_top)

        # Adjust individual lines for width.
        max_width = width - 2 - padding.width
        for idx, line in enumerate(lines):
            width_diff = max_width - len(line)
            if width_diff < 0:
                # Truncate lines that are too long.
                lines[idx] = line[:width_diff]
            elif width_diff > 0:
                # Apply horizontal alignment.
                if h_align == HAlign.Left:
                    lines[idx] = line.ljust(max_width, align_char)
                elif h_align == HAlign.Center:
                    lines[idx] = line.center(max_width, align_char)
                elif h_align == HAlign.Right:
                    lines[idx] = line.rjust(max_width, align_char)

        # Add the final text to the canvas.
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                self[x + padding.left + c + 1, y + padding.up + r + 1] = char

        return width, height


@dataclass
class TableCell:
    row: int
    col: int

    content: any
    format_string: str | None = None

    row_span: int = 1
    col_span: int = 1

    double: bool = False

    h_align: HAlign | None = None
    v_align: VAlign | None = None
    padding: Padding | None = None
    align_char: str | None = None

    @property
    def left(self):
        return self.col

    @property
    def right(self):
        return self.col + self.col_span

    @property
    def top(self):
        return self.row

    @property
    def bottom(self):
        return self.row + self.row_span

    @property
    def col_range(self) -> range:
        return range(self.left, self.right)

    @property
    def row_range(self) -> range:
        return range(self.top, self.bottom)

    @property
    def pos(self):
        return self.row, self.col

    def contains_point(self, x: int, y: int) -> bool:
        return self.left <= x < self.right and self.top <= y < self.bottom

    def overlaps(self, other: 'TableCell') -> bool:
        return (
            self.right > other.left and
            self.left < other.right and
            self.top > other.bottom and
            self.bottom < other.top
        )

    def get_text(self, default_format_string: str | None = None) -> str:
        if self.content is None:
            return ''
        #
        format_string = self.format_string or default_format_string or '{}'
        try:
            return format_string.format(self.content)
        except ValueError as err:
            raise ValueError(f'Error formatting {self} with format {repr(format_string)}: {err}') from err

    def __str__(self):
        col = str(self.col) if self.col_span == 1 else f'{self.left}:{self.right}'
        row = str(self.row) if self.row_span == 1 else f'{self.top}:{self.bottom}'
        return f'<R{row}, C{col}, {repr(self.content)}>'


def _total_size(sizes: dict[int, int], where: range) -> int:
    return sum(sizes[i] for i in where) - len(where) + 1


def _adjust_sizes(target: int, current: dict[int, int], where: range):
    expand_by = target - _total_size(current, where)
    if expand_by <= 0:
        return
    divided = (expand_by + len(where) - 1) // len(where)
    for i in where:
        current[i] += divided


def _accumulate_coordinates(initial: int, sizes: dict[int, int]) -> dict[int, int]:
    pos = initial
    result = {}
    for idx, size in sizes.items():
        result[idx] = pos
        pos += size - 1
    return result


class Table:
    default_background: str | None = None
    default_format: str | None = None
    default_h_align: HAlign = HAlign.Center
    default_v_align: VAlign = VAlign.Middle
    default_align_char: str | None = None
    default_padding: Padding | None = None

    def __init__(self, title: str = ''):
        self.title = title
        self.cells: list[TableCell] = []
        self.width_overrides: dict[int, int] = {}
        self.height_overrides: dict[int, int] = {}
        self.col_format: dict[int, str] = {}
        self.row_format: dict[int, str] = {}
        self.col_h_align: dict[int, HAlign] = {}
        self.row_v_align: dict[int, VAlign] = {}
        self.background: str | None = None

    @property
    def left(self):
        return min((cell.left for cell in self.cells), default=0)

    @property
    def right(self):
        return max((cell.right for cell in self.cells), default=0)

    @property
    def top(self):
        return min((cell.top for cell in self.cells), default=0)

    @property
    def bottom(self):
        return max((cell.bottom for cell in self.cells), default=0)

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    def __getitem__(self, item: tuple[int, int]) -> TableCell | None:
        x, y = item
        for cell in self.cells:
            if cell.contains_point(x, y):
                return cell

    def __str__(self):
        canvas = BoxCanvas()
        self.draw(canvas)
        return str(canvas)

    def add_cell(self, new_cell: TableCell):
        for cell in self.cells:
            if cell.overlaps(new_cell):
                raise ValueError(f'Cell {new_cell} overlaps existing cell {cell}')
        self.cells.append(new_cell)

    def add(self, row: int, column: int, content: any, **kwargs):
        self.add_cell(TableCell(row, column, content, **kwargs))

    def add_sequence(self,
                     items: Iterable[any],
                     start: tuple[int, int],
                     stride: tuple[int, int],
                     replace_none: any = None,
                     **kwargs):
        """
        Add a sequence of cells, with a given starting location and stride.
        :param items: Items that should be added to the table.
        :param start: Tuple (row, col) specifying where the first item should be added.
        :param stride: Tuple (row, col) added to the location after every item.
        :param replace_none: Optional value used to replace None items.
        :param kwargs: Additional keyword arguments which will be passed to the TableCell constructor.
        """
        row, col = start
        for value in items:
            if value is None:
                value = replace_none
            if value is not None:
                self.add(row, col, value, **kwargs)
            row += stride[0]
            col += stride[1]

    def add_row(self, *items: any, row: int | None = None, col: int | None = None, **kwargs):
        """
        Add any number of items as a row.
        :param items: Items to add. None values will not be added, but do advance the column index.
        :param row: Row index where the items should be added. This is None by default, which will make the function
                    use `Table.bottom` instead, i.e. the row will be placed at the current bottom of the table.
        :param col: Optional starting column index. If not specified then the first item will be in column 0.
        :param kwargs: Additional keyword arguments which will be passed to add_sequence.
        :returns The row index where the items were added.
        """
        if row is None:
            row = self.bottom
        self.add_sequence(items, (row, col or 0), (0, 1), **kwargs)
        return row

    def add_col(self, *items: any, col: int | None = None, row: int | None = None, **kwargs):
        """
        Add any number of items as a column.
        :param items: Items to add. None values will not be added, but do advance the row index.
        :param col: Column index where the items should be added. This is None by default, which will make the function
                    use `Table.right` instead, i.e. the column will be placed at the current right of the table.
        :param row: Optional starting row index. If not specified then the first item will be in row 0.
        :param kwargs: Additional keyword arguments which will be passed to add_sequence.
        :returns The column index where the items were added.
        """
        if col is None:
            col = self.right
        self.add_sequence(items, (row or 0, col), (1, 0), **kwargs)
        return col

    def draw(self, canvas: BoxCanvas, offset_x: int = 0, offset_y: int = 0):
        # Initialize an empty layout.
        # The default column and row size is 3, to fit a minimum box with a single empty character in it.
        col_widths = {c: 3 for c in range(self.left, self.right)}
        row_heights = {r: 3 for r in range(self.top, self.bottom)}

        # Collect formatted text values for all the cells.
        cell_text: dict[(int, int), str] = {}
        for cell in self.cells:
            format_string = self.default_format
            if cell.row >= 0 and cell.col in self.col_format:
                format_string = self.col_format[cell.col]
            if cell.col >= 0 and cell.row in self.row_format:
                format_string = self.row_format[cell.row]
            cell_text[cell.pos] = cell.get_text(format_string)

        # Figure out the minimum column widths and row heights to fit the table's content.
        for cell in self.cells:
            w, h = canvas.fit_text(cell_text[cell.pos])
            _adjust_sizes(w, col_widths, cell.col_range)
            _adjust_sizes(h, row_heights, cell.row_range)

        # Apply width and/or height overrides, if any have been set.
        for c, width in self.width_overrides.items():
            col_widths[c] = width
        for r, height in self.height_overrides.items():
            row_heights[r] = height

        # Compute the size of the title box.
        if len(self.title) > 0:
            title_width, title_height = canvas.fit_text(self.title)
        else:
            title_width, title_height = 1, 1  # Default to 1 since we subtract by one later.

        # Calculate the column x and row y coordinates based on the final widths and heights.
        col_x = _accumulate_coordinates(offset_x, col_widths)
        row_y = _accumulate_coordinates(offset_y + title_height - 1, row_heights)

        # Now it's finally time to draw everything.

        # Draw a box around the entire "main" portion of the table, and fill it with our background character (if any).
        main_width = _total_size(col_widths, range(0, self.right))
        main_height = _total_size(row_heights, range(0, self.bottom))
        canvas.draw_box(col_x[0], row_y[0], main_width, main_height, fill=self.background or self.default_background)

        # Draw title box if we have one.
        if title_height > 2:
            canvas.text_box(col_x[0], offset_y, self.title, width=title_width, height=title_height)

        # Draw all the cells.
        for cell in self.cells:
            x = col_x[cell.left]
            y = row_y[cell.top]
            w = _total_size(col_widths, cell.col_range)
            h = _total_size(row_heights, cell.row_range)
            canvas.text_box(
                x, y,
                cell_text[cell.pos],
                width=w,
                height=h,
                h_align=cell.h_align or self.col_h_align.get(cell.col, self.default_h_align),
                v_align=cell.v_align or self.row_v_align.get(cell.row, self.default_v_align),
                align_char=cell.align_char or self.default_align_char,
            )
