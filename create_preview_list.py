#!/usr/bin/python

import os

preview_list_file = "PREVIEW.md"

model_file_extensions = ('dae','blend','wrl','stp','stl')

def walk_dir_rec(level, curr_dir):
	fileContent = ""

	if level > 1:
		#process files in current dir:

		fileContent += '#' * level + " " + os.path.basename(curr_dir) + "\r\n\r\n"

		previewFile = ""
		modelFiles = ""
		for filename in sorted(os.walk(curr_dir).next()[2]):
			if filename.lower() == "preview.png":
				previewFile = "![{0}]({1})\r\n".format(os.path.basename(curr_dir), curr_dir[2:] + "/" + filename)
			elif filename.lower().endswith(model_file_extensions):
				modelFiles += "* [{0}]({1}?raw=true)\r\n".format(filename, curr_dir[2:] + "/" + filename)

		if len(modelFiles) > 0:
			fileContent += previewFile + "\r\n" + modelFiles + "\r\n"

	for dirname in sorted(os.walk(curr_dir).next()[1]):
		if any(dirname in s for s in ['.git', 'textures']):
			continue

		fileContent += walk_dir_rec(level+1,os.path.join(curr_dir,dirname))

		if level == 1:
			fileContent += "_____________\r\n"

	return fileContent;

def walk_dirs(base):
	return "# Model list & preview\r\n\r\n" + walk_dir_rec(1,base)


if __name__ == "__main__":
	print("Creating %s" % preview_list_file)
	f = open(preview_list_file, 'w+')
	f.write(walk_dirs('.'))    
	f.close()
	print("File created and saved.")
