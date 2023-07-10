""" 
This module contains classes and functions to generate markdown files.


Author: Arttu Mahlakaarto (github.com/amahlaka)
License: MIT License
Copyrigth (c) 2023 Arttu Mahlakaarto
"""

import os


class Header:
    """Class to generate markdown headers."""

    def __init__(self, text: str, level: int = 1):
        """Create a header object.

        Args:
            text (str): Text for the header

        Keyword Args:
            level (int): Level of the header
        """
        self.text = text
        self.level = level

    def __str__(self):
        """Return the header as a string."""
        return "#" * self.level + " " + self.text

    def __repr__(self):
        """Return the header as a string."""
        return "#" * self.level + " " + self.text

class Table:
    """Class to generate markdown tables."""

    def __init__(self, headers: list[str], **kwargs):  # type: ignore
        """Create a table object

        Args:
            headers (list[str]): List of headers for the table

        Keyword Args:
            title (str): Title for the table
            flexible_headers (bool): If True, allow headers to be added dynamically
            sort_reverse (bool): If True, sort the table in reverse order
            sort_key (str): Key to sort the table by
            custom_map (dict): Custom map to remap values in the table
        """
        self.headers = headers
        self.rows: list[dict[str, str | int | float | bool]] = []
        self.flexible_headers = kwargs.get("flexible_headers", False)
        self.sort_reverse = kwargs.get("sort_reverse", False)
        self.sort_key = kwargs.get("sort_key", "")
        self.custom_map: dict = kwargs.get("custom_map", False)
        self.title = kwargs.get("title", False)

    def remap(self):
        """Remap values in the table based on the custom_map"""
        for header, value_map in self.custom_map.items():
            for row in self.rows:
                row[header] = value_map.get(row[header], row[header])

    def add_rows(self, rows: list[dict[str, str | int | float | bool]]):
        """Add multiple rows to the table.
        
        Args:
            rows (list[dict[str, str | int | float | bool]]): List of rows to add
        """
        for row in rows:
            self.add_row(row)

    def add_row(self, row: dict[str, str | int | float | bool] | list[str]):
        """Add a row to the table.
        
        Args:
            row (dict[str, str | int | float | bool], list[str]): Row to add
        """

        # If row is a list, convert it to a dict, using the headers as keys
        if isinstance(row, list):
            if len(row) != len(self.headers):
                raise ValueError(
                    f"Row length ({len(row)}) does not match header length ({len(self.headers)})"
                )
            row = dict(zip(self.headers, row))
        # If row is a dict, check that all the keys are in the headers, if not, raise error
        elif isinstance(row, dict):
            for key in row.keys():
                if key not in self.headers:
                    if self.flexible_headers:
                        self.headers.append(key)
                    else:
                        raise ValueError(
                            f"Key {key} not in headers and flexible_headers is False"
                        )
        # Check that all the headers are in the row
        for header in self.headers:
            if header not in row.keys():
                row[header] = ""

        self.rows.append(row)

    def sort_table(self, disable_convert: bool = False):
        """Sort the table by the sort_key."""
        if self.sort_key:
            # If multiple sort keys are provided, prioritize the first one, then the second, etc.
            sort_keys = self.sort_key.split(",")
            for sort_key in sort_keys:
                if sort_key not in self.headers:
                    raise ValueError(f"sort_key {sort_key} not in headers")
                if disable_convert:
                    self.rows = sorted(
                        self.rows,
                        key=lambda row: row.get(sort_key, ""), # pylint: disable=cell-var-from-loop
                        reverse=self.sort_reverse,
                    )
                    break
                if all( # pylint: disable=use-a-generator
                    [
                        row.get(sort_key, "")
                        in [1, 0, False, True, "False", "True", "false", "true"]
                        for row in self.rows
                    ]
                ):
                    for row in self.rows:
                        row[sort_key] = bool(row.get(sort_key, False))
                    self.rows = sorted(
                        self.rows,
                        key=lambda row: bool(row.get(sort_key, False)), # pylint: disable=cell-var-from-loop
                        reverse=self.sort_reverse,
                    )
                    break

                try:
                    self.rows = sorted(
                        self.rows,
                        key=lambda row: row.get(sort_key, 0), # pylint: disable=cell-var-from-loop
                        reverse=self.sort_reverse,
                    )
                    break
                except TypeError:
                    try:
                        self.rows = sorted(
                            self.rows,
                            key=lambda row: int(row.get(sort_key, 0)), # pylint: disable=cell-var-from-loop
                            reverse=self.sort_reverse,
                        )
                        break
                    # if type or value error:
                    except (TypeError, ValueError):
                        self.rows = sorted(
                            self.rows,
                            key=lambda row: str(row.get(sort_key, "")), # pylint: disable=cell-var-from-loop
                            reverse=self.sort_reverse,
                        )
                        break

        else:
            raise ValueError("sort_key not set")

    def get_table(self) -> str:
        """Generate the table."""
        if self.sort_key:
            self.sort_table()
        if self.custom_map:
            self.remap()
        table = ""
        if self.title:
            table += f"### {self.title}\n"

        table += f"| {' | '.join(self.headers)} |\n"
        table += f"| {' | '.join(['---' for _ in self.headers])} |\n"
        for row in self.rows:
            table += f"| {' | '.join([str(row.get(header, '')) for header in self.headers])} |\n"
        # if self.total_row:
        #     total_row = {}
        #     for header in self.headers:
        #         if header == self.total_row_label:
        #             total_row[header] = "Total"
        #         else:
        #             try:
        #                 total_row[header] = sum(
        #                     [int(row.get(header, 0)) for row in self.rows]
        #                 )
        #             except ValueError:
        #                 total_row[header] = ""
        #     table += f"| {' | '.join([str(total_row.get(header, '')) for header in self.headers])} |\n" # pylint: disable=line-too-long
        return table

    def __str__(self):
        return self.get_table()


class Image:
    """Image object for markdown."""
    def __init__(self, url: str, **kwargs):
        """Create an image object.
        Args:
            url (str): URL of the image
            title (str, optional): Title of the image.
            alt (str, optional): Alt text for the image. Defaults to "alt text".
            width (int, optional): Width of the image.
            height (int, optional): Height of the image.
            align (str, optional): Alignment of the image.
            caption (str, optional): Caption for the image.
            """
        self.url = url
        self.title = kwargs.get("title", False)
        self.alt = kwargs.get("alt", url)
        self.width = kwargs.get("width", False)
        self.height = kwargs.get("height", False)
        self.align = kwargs.get("align", False)
        self.caption = kwargs.get("caption", False)


    def html(self):
        """Generate the html for the image."""
        image = f'<img src="{self.url}" alt="{self.alt}"'
        if self.width:
            image += f' width="{self.width}"'
        if self.height:
            image += f' height="{self.height}"'
        if self.align:
            image += f' align="{self.align}"'
        image += ">"
        if self.caption:
            image += f'<br><i>{self.caption}</i>'
        return image

    def markdown(self):
        """Generate the markdown for the image."""
        image = ""
        if self.title:
            image += f"### {self.title}\n"
        image += f"![{self.alt}]({self.url}"
        image += ")\n"
        if self.caption:
            image += f"_{self.caption}_\n"
        return image
    def __str__(self):
        if any([self.width, self.height, self.align]):
            return self.html()
        return self.markdown()
    def __repr__(self):
        return_string = f"Image(url={self.url}, title={self.title}, alt={self.alt}"
        return_string += f", width={self.width}, height={self.height}, align={self.align},"
        return_string +=f"caption={self.caption})"
        return return_string


class Link:
    """Link object for markdown."""
    def __init__(self, url: str, text: str = "", **kwargs):
        """Create a link object.

        Args:
            url (str): URL of the link
            text (str): Text of the link
            title (str, optional): Title of the link. Defaults to False.
            new_tab (bool, optional): Open link in new tab. Defaults to False.
        """
        self.url = url
        if not text:
            text = url
        self.text = text
        self.title = kwargs.get("title", False)
        self.new_tab = kwargs.get("new_tab", False)
        self.trailing = kwargs.get("trailing", True)

    def __str__(self):
        link = ""
        if self.title:
            link += f"### {self.title}\n"
        link += f"[{self.text}]({self.url}"
        if self.new_tab:
            link += " target=_blank"
        link += ")"
        if self.trailing:
            link += "\n"
        return link

    def __repr__(self):
        return f"Link(url={self.url}, text={self.text}, title={self.title}, new_tab={self.new_tab})"


class List:
    """List object for markdown."""
    def __init__(self, items: list[str] | None = None, ordered: bool = False, **kwargs):
        """Create a list.
        
        Args:
            items (list[str], optional): List of items. Defaults to None.
            ordered (bool, optional): Ordered list. Defaults to False.
            title (str, optional): Title of the list. Defaults to False.
            """
        self.title = kwargs.get("title", False)
        if items is None:
            items = []
        self.items = items
        self.ordered = ordered

    def add(self, item: str | Link | Image):
        """Add an item to the list.

        Args:
            item (str | Link | Image): Item to add to the list.
        """

        self.items.append(str(item))

    def __str__(self):
        list_output = ""
        if self.title:
            list_output += f"### {self.title}\n"
        if self.ordered:
            for i, item in enumerate(self.items):
                list_output += f"{i+1}. {item}\n"
        else:
            for item in self.items:
                list_output += f"- {item}\n"
        return list_output

    def __repr__(self):
        return f"List(title={self.title}, items={self.items}, ordered={self.ordered})"


class Section:
    """Section object for markdown."""
    def __init__(self, title: Header | str, **kwargs):
        """Create a section.

        Args:
            title (str): Title of the section
            content (str, optional): Content of the section.
        """
        if isinstance(title, str):
            title = Header(title, **kwargs)
        self.title = title
        self.content = kwargs.get("content", "")

    def add(self, content: str | Table | List | Image | Link | Header):
        """Add content to the section.

        Args:
            content (str | Table | List | Image | Link): Content to add to the section.
        """
        if self.content:
            self.content += "\n"
        self.content += str(content)
        if isinstance(content, str):
            self.content += "  "

    def __str__(self):
        return f"{self.title}\n{self.content}\n"

    def __repr__(self):
        return f"Section(title={self.title}, content={self.content})"


class Document:
    """Class for creating markdown documents."""

    def __init__(
        self,
        title: str,
        filename: str,
        overwrite: bool = False,
        table_of_contents: bool = False,
        **kwargs,
    ):
        """Create a new document.
        Args:
            title: Title of the document
            filename: Name of the file to save the document to
            overwrite: Whether to overwrite the file if it already exists
            table_of_contents: Whether to add a table of contents to the document
            
        Keyword Args:
            sections: Dictionary of sections to add to the document

        """
        self.title = title
        self.sections: dict[str, Section] = kwargs.get("sections", {})
        self.generate_table_of_contents = table_of_contents
        # Validate filename
        if not filename.endswith(".md"):
            filename += ".md"

        # Check if file already exists
        if os.path.exists(filename):
            if overwrite:
                # Warn the user that the file will be overwritten
                print(
                    f"Warning: File {filename} already exists and will be overwritten"
                )
            else:
                raise ValueError(f"File {filename} already exists")
        self.filename = filename

    def add_section(self, section: Section | str):
        """Add a section to the document.

        Args:
            section (Section): Section to add to the document.
        """
        if isinstance(section, str):
            new_section = Section(section)
        elif isinstance(section, Section):
            new_section = section
        else:
            raise TypeError(
                f"Section must be of type Section or str, not {type(section)}"
            )

        self.sections[new_section.title.text] = new_section
        return new_section

    def get_document(self) -> str:
        """Get the document as a string."""
        document = f"# {self.title}\n"
        if self.generate_table_of_contents:
            document += "## Table of Contents\n"
            for section in self.sections.values():
                document += (
                    f"* [{section.title.text}](#{section.title.text.lower().replace(' ', '-')})\n"
                )
        for section in self.sections.values():
            document += str(section)
        return document

    def save(self, **kwargs):
        """Save the document to a file."""
        if kwargs.get("filename"):
            self.filename = kwargs.get("filename", "")
        with open(self.filename, "w", encoding="utf-8") as file_output:
            file_output.write(self.get_document())

    def __str__(self):
        return self.get_document()

    def __repr__(self):
        return f"""Document(title={self.title}, filename={self.filename},
         sections={self.sections}, table_of_contents={self.generate_table_of_contents})"""
