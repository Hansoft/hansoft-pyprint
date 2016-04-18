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
from string import Template

PRIO = {
	'-1': '(No prio set)',
	'1': 'Very Low',
	'2': 'Low',
	'3': 'Medium',
	'4': 'High',
	'5': 'Very High'
	}

STATUS = {
	'1': 'Not Done',
	'2': 'In Progress',
	'3': 'Completed',
	'4': 'Blocked',
	'5': 'To be deleted'
}

TEMPLATEHEADER = "template-header.html"
TEMPLATEFOOTER = "template-footer.html"

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
	parser.add_argument("-t",
			    dest='template_story',
			    help='Template HTML for each story.',
			    default="template-story.html")
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
	except ET.ParseError as e:
		print "Error parsing XML input:", e
		sys.exit()
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
				story['story'] = task.findtext('LongText')
			except AttributeError:
				story['story'] = ""
			story['databaseid'] = task.findtext('DatabaseID')
			story['priority'] = task.findtext('PreCreatedColumn_MainBacklogPriority')
			if story['priority'] is None:
				story['priority'] = "-1"
			story['status'] = task.findtext('PreCreatedColumn_ItemStatus')
			subprojectpath = task.findtext('SubProjectPath')
			if subprojectpath:
				story['subprojectpath'] = subprojectpath
			else:
				story['subprojectpath'] = '(No parent)'
			if opts.category:
				custom_data = task.find('CustomColumnDatas')
				if not custom_data is None:
					category = custom_data.findtext(opts.category)
					if category:
						category = category.replace(' ', '-')
						category = category.lower()
						story['category'] = category
			if not 'category' in story:
				story['category'] = 'no-category'

			stories.append(story)

	# Print pretty
	try:
		template_header_file = open(TEMPLATEHEADER, 'r')
	except IOError as e:
		print "Missing file:", TEMPLATEHEADER
		sys.exit(e.errno)

	template_header = Template(template_header_file.read())
	template_header_file.close()
	html = template_header.substitute(stylesheet=opts.css.name)

	try:
		template_story_file = open(opts.template_story, 'r')
	except IOError as e:
		print "Missing file:", opts.template_story
		sys.exit(e.errno)
	template_story = Template(template_story_file.read())
	template_story_file.close()

	for raw_story in stories:
		if not raw_story['story']:
			continue
		# Clean up the story
		story = raw_story['story']
		story = story.replace("<BOLD>", "<strong>")
		story = story.replace("</BOLD>","</strong>")
		story = story.replace("\n", "<br />")

		html = html +  template_story.substitute(
			category=raw_story['category'],
			databaseid=raw_story['databaseid'],
			prio=raw_story['priority'],
			prioname=PRIO[raw_story['priority']],
			status=raw_story['status'],
			statusname=STATUS[raw_story['status']],
			subprojectpath=raw_story['subprojectpath'],
			name=raw_story['name'],
			story=raw_story['story']
			)

	try:
		template_story_footer = open(TEMPLATEFOOTER, 'r')
	except IOError:
		print "Missing file:", TEMPLATEFOOTER
	html = html + template_story_footer.read()
	template_story_footer.close()

	opts.html.write(html.encode('utf-8'))
	opts.html.close()

main()
