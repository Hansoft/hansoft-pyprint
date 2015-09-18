#!/usr/bin/env python
"""The hansoft-pyprint prints the user story field in a Hansoft XML file.

Args:
--xml=file.xml The input file that will be printed.
--style=file.css The style that should be applied.
--output=file.html The destination of the file.
-u Flag to only print items flagged as user stories.
-c Use a custom category column for style.

Returns:
Generates a .html file to be open in a browser that can be
printed to pdf or a printer.

"""
import sys
import argparse
import xml.etree.ElementTree as ET
from io import FileIO

def main(argv=None):
	if argv is None:
		argv = sys.argv

	parser = argparse.ArgumentParser()
	parser.add_argument("-x", "--xml",
			  dest="xml",
			  type=file,
			  help="Input Hansoft XML",
			  metavar="FILE",
			  default='hansoft.xml')
	parser.add_argument("-s", "--style",
			  dest="css",
			  type=file,
			  help="CSS Style to use in generated html",
			  metavar="FILE",
			  default='default.css')
	parser.add_argument("-o", "--output",
			  dest="html",
			  type=argparse.FileType('w'),
			  help="Output HTML file destination",
			  metavar="FILE",
			  default='output.html')
	parser.add_argument("-u",
			  dest='userstory',
			  help='Only print items Flagged as User Story',
			  action='store_true')
	parser.add_argument("-c",
			    dest='category',
			    help='Name of custom category column for style options.')
	try:
		opts = parser.parse_args()
	except IOError as e:
		print "I/O error ({0}): {1}".format(e.errno, e.strerror)
		sys.exit(e.errno)

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
			if not task.findtext('FlaggedAsUserStory') == '1' and opts.userstory:
				continue
			story['name'] = task.find('TaskName').text
			if story['name'] is None:
				story['name'] = '(No name)'
			try:
				story['story'] = task.find('LongText').text
			except AttributeError:
				story['story'] = ""
			story['database_id'] = task.find('DatabaseID').text
			# Product Backlog Priority
			story['priority'] = task.findtext('PreCreatedColumn_MainBacklogPriority')
			if opts.category:
				custom_data = task.find('CustomColumnDatas')
				if not custom_data is None:
					category = custom_data.findtext(opts.category)
					if category:
						category = category.replace(' ', '-')
						category = category.lower()
					# Clean data
						story['category'] = category
			stories.append(story)

	# Print pretty
	html = "<html><head>"
	html = html + "<link rel='stylesheet' href='" + opts.css.name +  "' type='text/css' />"
	html = html + "</head><body>"

	for raw_story in stories:
		# Clean up the story
		story = raw_story['story']
		story = story.replace("<BOLD>", "<strong>")
		story = story.replace("</BOLD>","</strong>")
		story = story.replace("\n", "<br />")
		
		# Prefix
		html = html + "<div class='card'>"
		if 'category' in raw_story:
			html = html + "<div class='" + raw_story['category'] + "'>"
		if 'priority' in raw_story:
			html = html + "<div class='prio-" + raw_story['priority'] + "'>"

		html = html + "<div class='name'>" + raw_story['name'] + " ("
		if 'priority' in raw_story:
			html = html + raw_story['priority'] + " / " 
		html = html + "#" + raw_story['database_id'] + ")"
	
		html = html + "</div>"
		html = html + story

		# Closing tags
		html = html + "</div>"
		if 'category' in raw_story:
			html = html + "</div>"
		if 'priority' in raw_story:
			html = html + "</div>"

	html = html + "</body></html>"

	opts.html.write(html)
	opts.html.close()

main()
