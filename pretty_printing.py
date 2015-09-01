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
		opts, args = getopt.getopt(argv[1:], "hs:f:o:d", ["help", "style=","file=", "output="])
	except getopt.GetOptError:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt == 'd':
			global debug
			_debug = 1
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
			story['story'] = task.find('LongText').text
			stories.append(story)

	# Print pretty
	output = "<html><head>"

	output = output + "<link rel='stylesheet' href='default.css' type='text/css' />"

	output = output + "</head><body>"


	for raw_story in stories:
		# Prefix
		output = output + "<div class='card'>"

		# Clean up the story
		story = raw_story['story']
		story = story.replace("<BOLD>", "<strong>")
		story = story.replace("</BOLD>","</strong>")
		story = story.replace("\n", "<br />")

		output = output + "<div class='name'>" + raw_story['name'] + "</div>"
		output = output + story
		# TODO - Fix colors

		# Closing tags
		output = output + "</div>"

	output = output + "</body></html>"

	file = FileIO('test.html', 'w')
	file.write(output)
	file.close()

main()
