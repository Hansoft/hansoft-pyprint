Hansoft-Pyprint
===============

Overview
--------
Hansoft-pyprint parses a Hansoft XML file and generates a simple HTML file associated with a CSS Stylesheet. This let's you quickly generate printouts of user stories with the style you would like.

Example use cases:
* Print user stories from a sprint backlog. You mark the items in the sprint backlog, export them to Hansoft XML and run the command `python hansoft-pyprint.py --xml=hansoft.xml -u`
* Print items in the product backlog for a backlog priotization meeting on one page per sheet of paper. Export the items from the product backlog and run the command `python hansoft-pyprint.py --xml=hansoft.xml --style=onestoryperpage.css`

Terms and conditions
--------------------
hansoft-pyprint is licensed under what is known as a MIT License as states in the [LICENSE.md](LICENSE.md).

This content of this repository is not part of the official Hansoft product or subject to its license agreement.
The content of this repository is provided as is and there is no obligation on Hansoft AB to provide support, update or enhance this program.

Styles
------
The python script hansoft-pyprint.py generates a very simple HTML file. In this file it uses css classes that you can customize:
* .card - control style of each card/user story. Typically where you would add borders, set a background color etc.
* .name - control style of the item name as displayed in Hansoft.