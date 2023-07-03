# python-markdown-helper
[![Coverage Status](https://coveralls.io/repos/github/amahlaka/python-markdown-helper/badge.svg)](https://coveralls.io/github/amahlaka/python-markdown-helper)  
A bunch of helper classes that make generating markdown files easier.

Originally written to make my own life easier. I got tired of writing repetitive code to generate markdown files for my projects.  


# Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Upcoming Features](#upcoming-features)
- [Contributing](#contributing)
- [License](#license)

---

## Installation
```bash
pip install markdown-helper
```

## Usage
Sample code that generated the [EXAMPLE.md](EXAMPLE.md) file

```python
import markdown_helper as mdh

# Create a new markdown Document that includes a table of contents
doc = mdh.Document("Title", "EXAMPLE.md", overwrite=True, table_of_contents=True)

# Add a new section to the document
first_section = doc.add_section("Section 1")
# Add some text to the section
first_section.add("Regular text in the first section")
# Add a list to the section
list_of_fruits = mdh.List(["Apple", "Banana", "Orange"], ordered=True, title="Fruit List")

first_section.add(list_of_fruits)

# Make a new Table with custom value mapping
table = mdh.Table(["Fruit", "Color"], sort_key="Fruit", title="Fruit Table", custom_map={"Fruit": {"Apple": "🍎", "Banana": "🍌"}})
# Add some rows to the table
table.add_row({"Fruit": "Apple", "Color": "Red"})
table.add_row({"Fruit": "Banana", "Color": "Yellow"})

# Add the table to the document
first_section.add(table)

# Add a new section to the document with Smaller title
second_section = mdh.Section(mdh.Header("Section 2", 2))
doc.add_section(second_section)
second_section.add("Regular text in the second section")

# Add a link and an image to the section
link = mdh.Link("https://google.com", "Google")
second_section.add(link)
image = mdh.Image("https://picsum.photos/200", alt="A random image")
second_section.add(image)

# Output the document to as a string
print(doc)

# Save the document to a file
doc.save()
```

# Upcoming Features

-  Add support for code blocks
- ???

# Contributing

Feel free to open a pull request or an issue if you have any suggestions or find any bugs

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details