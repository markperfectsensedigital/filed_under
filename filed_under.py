#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
#
# This script extracts all the tags in the docs project. It presumes that
# all tags start with the phrase 'Filed under:
#
import os
import re

pattern = re.compile('Filed under.*')
syntax_pattern = re.compile('Filed under: \*\*.{2,}\*\*')
tag_pattern = re.compile('\*\*(.*)\*\*')
tag_dictionary = {}

def syntax_not_ok(candidate):
# Checks that the syntax for filed under is valid.
   syntax_search = re.search(syntax_pattern,candidate)
   return bool(syntax_search is None)

# walk each file under the document root.
for root,dirs,files in os.walk("/Users/mlautman/Documents/docs"):
   for name in files:
      filename = os.path.join(root,name)
# A source file is one that ends in .txt and is not in the _build subdirectory.#
      if filename.endswith('.txt') and (filename.find('_build') == -1) :
         #print('Processing ', filename)
         sourcefile = open(filename,'r')
         for line in sourcefile:
# Check if the line has the phrase 'Filed under:'
            searchtags = re.search(pattern,line)
            if searchtags is not None:
               #print(line)
               #print(searchtags.group(0))
# Check the syntax for the tag listing.
               if syntax_not_ok(searchtags.group(0)):
                  print("Faulty syntax: " , searchtags.group(0), " in ", filename)
                  continue
               tag_string = re.search(tag_pattern,searchtags.group(0))
               #print(tag_string.group(1))
# Split the list of tags into individual tags
               tag_list = tag_string.group(1).split(',')
               #print(tag_list)
# For each tag, increment the number of occurrences.
               for tag in tag_list:
                  tag_net = tag.strip()
                  tag_dictionary[tag_net] = tag_dictionary.get(tag_net, 0) + 1

         sourcefile.close()  
tagfile = open('/tmp/tagfile.csv','w')
tagfile.write('Tag\tQuantity\n')
for tag in sorted(tag_dictionary.keys(),key=str.casefold):
   tagfile.write(tag  + "\t" + str(tag_dictionary[tag]) + "\n")
tagfile.close()
print("Number of tags found: " + str(len(tag_dictionary.keys())))
print("Results in the file /tmp/tagfile.csv")
