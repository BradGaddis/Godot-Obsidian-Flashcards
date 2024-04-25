import os
import pyautogui
import subprocess
from html import unescape
import shutil
import re

def remove_tag(line, tag:str, ignore: str = ""):
    output = line
    open_tag = f"<{tag}"
    while open_tag + " " in output or open_tag + ">" in output:
        open_tag_index = output.find(open_tag)
        open_tag_close_index = output.find(">", open_tag_index) + 1 
        replace_string = output[open_tag_index: open_tag_close_index]
        output = output.replace(replace_string, "")

    output = output.replace(f"</{tag}>", "", -1)
    return output

def replace_code_tag(line):
    output = line
    while "<pre" in output:
        open_tag_index = output.find("<pre")
        open_tag_close_index = output.find(">", open_tag_index) + 1 
        replace_string = output[open_tag_index: open_tag_close_index]
        output = output.replace(replace_string, "```GDScript\n")
    output = output.replace("</pre>", "```")

    while "<code" in output:
        open_tag_index = output.find("<code")
        open_tag_close_index = output.find(">", open_tag_index) + 1 
        replace_string = output[open_tag_index: open_tag_close_index]
        output = output.replace(replace_string, "`")
    output = output.replace("</code>", "`")
    return output

def replace_lists(line):
    output = line
    open_unordered_index = output.find("<ul")
    open_ordered_index = output.find("<ol")
    if "<ul" in output:
        return ""
        output = output.replace("<ul", "-")
    if "<ol" in output:
        return ""
    if "</ul" in output:
        output = output.replace("</ul>", "")
    if "</ol" in output:
        output = output.replace("</ol>", "")
    if "<li" in output:
        output = output.replace("<li>", "  - ")
    if "</li" in output:
        output = output.replace("</li>", "")
    return output

def replace_hr_tag(line):
    if "<hr" in line:
        return "---\n\n"
    return line

def correct_h_tags(line):
    for i in range(7):
        line = line.replace(f"<h{i}>", f"#" * i + " ")
        line = line.replace(f"</h{i}>", "")
    return line

def clean_tables(line):
    # if "<table" in line:
    #     return ""
    # if "</table" in line:
    #     return ""
    # if "<tr" in line:
    #     start = line.find("<tr")
    #     end = line.find(">", start)
    #     line = line.replace(line[start:end+1], "---\n")
    # line = line.replace("</tr>", "---\n")
    # if "<td" in line:
    #     start = line.find("<td")
    #     end = line.find(">", start)
    #     line = line.replace(line[start:end+1], "| ")
    # line = line.replace("</td>", " |")
    # if "<tbody" in line or "</tbody" in line:
    #     return ""
    return line


def correct_bolds(line, no_bold: list = [], replace_by = "**"):
    """
    Seeing as bolds are important, key words, replace them with whatever you want cloze deletions to be
    """

    # </strong> should not be followed by a '('
    close_strong_index = line.find("</strong>")

    if '</strong>' in line and line[close_strong_index + 9] == "(":
        line = line.replace("<strong>", "")
        line = line.replace("</strong>", "")
        return line


    for word in no_bold:
        if '<strong>' in line and word:
            line = line.replace("<strong>", "")
            line = line.replace("</strong>", "")
            return line

    line = line.replace("<strong>", replace_by)
    line = line.replace("</strong>", replace_by)
    return line

def make_descriptions_flashcard(lines):
    for i, line in enumerate(lines):
        if line.startswith("## Description"):
                    j = i + 1
                    while j < len(lines) and not "## Description" in lines[j]:
                        if j >= len(lines) or lines[j].startswith("## ") and lines[j] != lines[i]:
                            break
                        
                        if "## Description" in lines[j - 1]:
                            lines[j - 1] = lines[j - 1].replace("\n\n", "\n?\n")
                        
                        if lines[j][-2:] == "\n\n":
                            if lines[j] == "\n\n" and lines[j - 1] == "\n<br>\n":
                                break
                            
                            lines[j] = lines[j].replace("\n\n", "\n<br>\n")
                        
                        j += 1

def make_flashcards(lines, startstr: str = "## enum", endstr: str = "## ", delimeter: str = " = ", misc = False):
    break_flag = False
    wait_flag = False

    for i, line in enumerate(lines):
        if line.startswith(startstr):
            j = i + 1
            while j < len(lines) and not startstr in lines[j]:
                if j >= len(lines) or lines[j].startswith("## ") and lines[j] != lines[i]:
                    lines[j - 1] = lines[j - 1].replace("<br>\n", "\n\n")
                    break
                
                if "```" in lines[j]:
                    wait_flag = True
                    
                if lines[j] == "```\n\n":
                    wait_flag = False

                if wait_flag:
                    j += 1
                    continue

                if lines[j][-2:] == "\n\n":
                    if lines[j].startswith("\n\n"): 
                        lines[j] = lines[j].replace("\n\n", "<br>\n")

                    if lines[j] == "---\n\n":
                        break_flag = False
                        lines[j - 1] = lines[j - 1].replace("<br>\n", "\n\n") 
                        lines[j + 1] = lines[j + 1].replace("\n<br>\n", "\n\n") 
                        j +=  1
                        continue

                    if misc:
                        if delimeter in lines[j]:
                            lines[j] = lines[j].replace("\n\n", "\n?\n")
                            lines[j - 1] = lines[j - 1].replace("\n<br>\n", "\n\n") 
                        else:
                            lines[j] = lines[j].replace("\n\n", "\n<br>\n")
                        j += 1
                        continue

                    if not break_flag and lines[j][0].isalpha():
                        lines[j] = lines[j].replace("\n\n", "\n?\n") 
                        break_flag = True
                    elif break_flag:
                        lines[j] = lines[j].replace("\n\n", "\n<br>\n") 


                j += 1

def four_header(line, name):
    if line.startswith(f"{name} "):
            line = "#### " + line
    return line

def clean_files(folder_path, output_path): 

    files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

    for i, file in enumerate(files):

        if file.split(".")[-1] != "html":
            if file.split(".")[-1] != "md":
                continue
            
        name = file.split(".")[0]

        if file.split("_")[0] != "class":
            continue
        
        with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
                lines = f.readlines()

                target_phrase_to_remove_top = 'Checking the stable version of the documentation...'
                target_phrase_to_remove_bottom = "<footer>"

                # Find the line with the target phrase and cut off from there
                for j, line in enumerate(lines):
                    if target_phrase_to_remove_top in line:
                        lines = lines[j + 11:]  # Keep lines after the target phrase
                        break
                
                for j in range(0, len(lines) -1):
                    if target_phrase_to_remove_bottom in lines[j]:
                        lines = lines[:j - 8]
                        break

                # Write the modified lines back to the file 
                with open(os.path.join(output_path, file.split(".")[0] + ".md"), 'w' , encoding='utf-8') as f:
                    f.writelines(lines)


        with open(os.path.join(output_path, file.split(".")[0] + ".md"), "r") as f:
            lines = f.readlines()
            content = []
        
            for j, line in enumerate(lines):
                line = unescape(line)
                line = remove_tag(line, "div")
                line = remove_tag(line, "section")
                line = remove_tag(line, "span")
                line = remove_tag(line, "p") + "\n"
                line = remove_tag(line, "a")
                line = remove_tag(line, "abbr")
                line = remove_tag(line, "button")
                line = line.replace("GDScriptC#", "")
                # line = line.replace("GDScript", "")
                line = remove_tag(line, "em")
                line = replace_hr_tag(line)
                line = replace_code_tag(line)
                line = replace_lists(line)
                line = correct_h_tags(line)
                line = correct_bolds(line, ["Note", "Warning", 
                                            "Depricated"])
                line = four_header(line, "enum")
                line = four_header(line, "flags")
                if line.startswith("Inherits:"):
                    line = line.replace("Inherits:", "Inherits :: ")
                    
                if line.startswith("Inherited By:"):
                    line = line.replace("Inherited By:", "Inherited By :: ")
                make_descriptions_flashcard(content)
                lines[j] = line

                content.append(lines[j])


            make_flashcards(content, "#### enum", "## ", " = ", True)
            make_flashcards(content, "#### flags", "##", " = ", True)
            make_flashcards(content, "## Property Descriptions", "## ")
            make_flashcards(content, "## Signal", "## ", "(")
            make_flashcards(content, "## Method Descriptions", "## ")

            name = content[0].split("# ")[1][:-3]
            

            with open(os.path.join(output_path, file.split(".")[0] + ".md"), "w") as f:
                f.writelines("".join(content))
                os.rename(os.path.join(output_path, file.split(".")[0] + ".md"), os.path.join(output_path, name + ".md"))
                os.mkdir(os.path.join(output_path, name))
                shutil.move(os.path.join(output_path, name + ".md"), os.path.join(output_path, name, name + ".md"))
                f.write("\n#godotdocs")


# change me
clean_files("source dir", "output dir")