# Godot-Obsidian-Flashcards
A simple Python script to convert GODOT .html to useable .md files for the Spaced Repition plugin for Obsidian

---

This is a quick script that translates the documentation for Godot into flash cards for Spaced Repition.

Yes, it could be better, but the idea is just to have a way to study the documenation. I intend to expand this script for other types of documenation, as well.

## How to use:

- Dowload [the docs](https://nightly.link/godotengine/godot-docs/workflows/build_offline_docs/master/godot-docs-html-master.zip) for Godot
- Unzip them, and grab the file from the classes directory.
- Add the source (classes dir) and destination (where you want to save the files in your Obsidian Vault) paths to the method at the bottom of the script.

## What it does:

This script follows the rules in spaced repition so that you can challenge yourself to memorize what inherits what, and each property of a class, as well what inherits what.

![image](https://github.com/BradGaddis/Godot-Obsidian-Flashcards/assets/66101412/0c1e2134-bea1-4896-bfd1-bffb376ebdc8)

If you want to use cloze deletion, just be sure to toggle that on for bold markup in your settings. This script assumes that if it is bolded, it must be important.

