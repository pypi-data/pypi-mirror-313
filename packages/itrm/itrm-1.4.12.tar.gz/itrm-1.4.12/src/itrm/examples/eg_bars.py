"""
This example shows how a horizontal bar chart can be generated, first with ASCII
characters only, and then again with Unicode characters. See
figures/eg_bars.png.
"""

import itrm

x = [2.3, 11.0, 13.3, 5.2, 7.5]
labels = ['apples', 'oranges', 'bananas', 'pears', 'grapes']
itrm.bars(x, labels, uni=False)
print()
itrm.bars(x, labels, uni=True)
