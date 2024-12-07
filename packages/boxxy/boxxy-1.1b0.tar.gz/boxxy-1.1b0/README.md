# boxxy
Provides utilities for drawing fancy text boxes and tables using the Unicode Box Drawings block.

---

Some example code can be found in `example.py`:
```python
from boxxy import *

# Create a canvas we can draw boxes and text to.
canvas = BoxCanvas()

# Draw a simple box at (0, 0) with size (10, 10).
canvas.draw_box(0, 0, 10, 10)

# Draw another, overlapping, box with double-line borders.
canvas.draw_box(5, 5, 10, 10, double_all=True)

# Draw another one but only double the left and right borders.
canvas.draw_box(3, 3, 20, 8, double_left=True, double_right=True)

# Draw a box with filled inside.
canvas.draw_box(8, 1, 5, 4, fill=True)

# Draw a simple text box.
canvas.text_box(12, 9, 'Hello world!')

# Draw a text box with multiple lines and extra padding.
canvas.text_box(17, 1, 'Big multi-\nline box.', padding=Padding(3, 1))

# Create a table and give it a title.
table = Table(title="Example")

# Set a background character that will show inside the table where we don't have any cells.
table.background = '·'

# Add row headers.
# Negative rows and columns are treated as headers during layout, but are generally the same as any other cell.
table.add(0, -1, 'Row 1')
table.add(2, -1, 'Row 3')

# Add column headers using one of the utility functions.
table.add_row('Col 1', 'Col 2', 'Col 3', None, 'Col 5', row=-1)

# Add a cell with some text.
table.add(0, 0, 'Hello world!')

# Add cells spanning rows and columns.
table.add(1, 0, 'Span\nrows', row_span=2)
table.add(1, 1, 'Span columns', col_span=4)

# Add cells with different horizontal alignment.
table.add(2, 1, 'Align Right', col_span=4, h_align=HAlign.Right)
table.add(3, 0, 'Align Left', col_span=2, h_align=HAlign.Left)
table.add(3, 2, 'Center', col_span=3, h_align=HAlign.Center)

# Draw the table to the canvas, with optional offset.
table.draw(canvas, 8, 12)
# It is also possible to just print the table with a default canvas:
# print(table)

# Finally, print the canvas.
print(canvas)
```

Output (sadly not displaying correctly on PyPI):
```text
┌────────┐                                                
│       ┌┴──┐    ┌────────────────┐                       
│       │   │    │                │                       
│  ╓────┤   ├────┤   Big multi-   │                       
│  ║    └┬──┘    │   line box.    │                       
│  ║ ╔═══╪════╗  │                │                       
│  ║ ║   │    ║  └────╥───────────┘                       
│  ║ ║   │    ║       ║                                   
│  ║ ║   │    ║       ║                                   
└──╫─╫───┘  ┌─╨───────╨────┐                              
   ╙─╫──────┤ Hello world! │                              
     ║      └─╥────────────┘                              
     ║        ║ ┌─────────┐                               
     ║        ║ │ Example │                               
     ╚════════╝ ├─────────┴────┬───────┬───────┐ ┌───────┐
                │    Col 1     │ Col 2 │ Col 3 │ │ Col 5 │
        ┌───────┼──────────────┼───────┴───────┴─┴───────┤
        │ Row 1 │ Hello world! │·························│
        └───────┼──────────────┼─────────────────────────┤
                │     Span     │       Span columns      │
        ┌───────┤     rows     ├─────────────────────────┤
        │ Row 3 │              │             Align Right │
        └───────┼──────────────┴───────┬─────────────────┤
                │ Align Left           │      Center     │
                └──────────────────────┴─────────────────┘
```
