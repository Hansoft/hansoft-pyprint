#!/usr/bin/env python
"""The hansoft-pyprint prints the user story field in a Hansoft XML file.

Args:
--xml=file.xml The input file that will be printed.
--style=file.css The style that should be applied.
--output=file.html The destination of the file.

Returns:
Generates a .html file to be open in a browser that can be
printed to pdf or a printer.

"""
import sys
from optparse import OptionParser
import xml.etree.ElementTree as ET
from io import FileIO

def main(argv=None):
	if argv is None:
		argv = sys.argv

	parser = OptionParser()
	parser.add_option("-x", "--xml",
			  dest="xml",
			  help="Input Hansoft XML",
			  metavar="FILE",
			  default='hansoft.xml')
	parser.add_option("-s", "--style",
			  dest="css", 
			  help="CSS Style to use in generated html",
			  metavar="FILE",
			  default='default.css')
	parser.add_option("-o", "--output",
			  dest="html",
			  help="Output HTML file destination",
			  metavar="FILE",
			  default='output.html')
	(opts, args) = parser.parse_args()

	# Parse the input file
	try:
		tree = ET.parse(opts.xml)
	except IOError:
		print "The file " + opts.xml + " could not be found."
		sys.exit(0)

	root = tree.getroot()
	stories = []
	for activity in root.findall('Activities'):
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
	html = html + "<link rel='stylesheet' href='" + opts.css +  "' type='text/css' />"
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

	output_file = FileIO(opts.html, 'w')
	output_file.write(html)
	output_file.close()

main()
