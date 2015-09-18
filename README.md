Hansoft-Pyprint
===============

Overview
--------
Hansoft-pyprint parses a Hansoft XML file and generates a simple HTML file associated with a CSS Stylesheet. This let's you quickly generate printouts of user stories.

Example use cases:
* Print user stories from a sprint backlog. Export the sprint backlog items to Hansoft XML and run the command `python hansoft-pyprint.py --xml=hansoft.xml -u`
* Print items in the product backlog for a backlog priotization meeting on one page per sheet of paper. Export the items from the product backlog and run the command `python hansoft-pyprint.py --xml=hansoft.xml --style=onestoryperpage.css`

Terms and conditions
--------------------
hansoft-pyprint is licensed under what is known as a MIT License as states in the [LICENSE.md](LICENSE.md).

The content of this repository is not part of the official Hansoft product or subject to its license agreement.
The content of this repository is provided as is and there is no obligation on Hansoft AB to provide support, update or enhance this program.

Options
-------
* -h, --help : show help message and exit
* -x FILE, --xml FILE : Input Hansoft XML.
* -s FILE, --style FILE : CSS Style to use in generated HTML.
* -o FILE, --output FILE : Output HTML file destination.
* -u : Only print items Flagged as User Story.
* -c CATEGORY : CATEGORY is Name of custom category column for advanced styling options.

Styles
------
The python script hansoft-pyprint.py generates a very simple HTML file that can be associated with a stylesheet (.css file). There are two examples in this repository:
* default.css - Simple and basic printing the user stories one by one.
* onestoryperpage.css - Prints one user story per page.
* classofservice.css - Example when using a category column with the choices (Expedite, Standard, Fixed Date, Intangible)

Css classes that you can customize:
* .card - control style of each card/user story. Typically where you would add borders, set a background color etc.
* .name - control style of the item name as displayed in Hansoft.
* If using the -c flag with a custom column you can use the values in the custom columns.
* .prio-X - X is a number 1 (Very low prio) - 5 (Very high prio) to style depending on priority.