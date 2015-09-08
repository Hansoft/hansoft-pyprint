#!/usr/bin/env python
"""The hansoft-pyprint prints the user story field in a Hansoft XML file.

Args:
--file=file.xml The input file that will be printed.
--style=file.css The style that should be applied.
--output=file.html The destination of the file.

Returns:
Generates a .html file to be open in a browser that can be
printed to pdf or a printer.

"""

import sys
import getopt
import xml.etree.ElementTree as ET
from io import FileIO

def main(argv=None):
	if argv is None:
		argv = sys.argv
	style = "default.css"
	file = "hansoft.xml"
	output = "cards.html"

	try:
		opts, args = getopt.getopt(argv[1:], "hs:f:o:", ["help", "style=","file=", "output="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-s", "--style"):
			style=arg
		elif opt in ("-f", "--file"):
			file=arg
		elif opt in ("-o", "--output"):
			output=arg

	# Parse the input file
	try:
		tree = ET.parse(file)
	except IOError:
		print "The file " + file + " could not be found."
		sys.exit(0)

	root = tree.getroot()
	stories = []
	for activity in root.findall('Activities'):
		# TODO - add a title
		for task in activity.findall('Task'):
			story = {}
			story['name'] = task.find('TaskName').text
			try:
				story['story'] = task.find('LongText').text
			except AttributeError:
				story['story'] = ""
			story['database_id'] = task.find('DatabaseID').text
			stories.append(story)

	# Print pretty
	html = "<html><head>"
	html = html + "<link rel='stylesheet' href='" + style +  "' type='text/css' />"
	html = html + "</head><body>"

	for raw_story in stories:
		# Clean up the story
		story = raw_story['story']
		story = story.replace("<BOLD>", "<strong>")
		story = story.replace("</BOLD>","</strong>")
		story = story.replace("\n", "<br />")
		
		# Prefix
		html = html + "<div class='card'>"
		
		html = html + "<div class='name'>" + raw_story['name'] + " (#" + raw_story['database_id'] + ")</div>"
		html = html + story

		# Closing tags
		html = html + "</div>"

	html = html + "</body></html>"

	output_file = FileIO(output, 'w')
	output_file.write(html)
	output_file.close()

main()
