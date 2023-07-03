"""
This file contains the pytest tests for the markdown_helper.py file.
"""
try:
    from src import markdown_helper as markdown
except ModuleNotFoundError:
    try:
        import markdown_helper as markdown
    except ModuleNotFoundError:
        from ..src import markdown_helper as markdown # pylint: disable=import-error, relative-beyond-top-level
def test_ordered_list():
    """
    This function tests the markdown.List class.
    """
    list_1: markdown.List = markdown.List(["item 1", "item 2", "item 3"], ordered=True)
    assert (
        str(list_1) == "1. item 1\n2. item 2\n3. item 3\n"
    ), "String representation of ordered list is incorrect."
    assert list_1.items == ["item 1", "item 2", "item 3"], "List items are incorrect."


def test_modify_list():
    """
    This function tests the markdown.List class.
    """
    list_1 = markdown.List(["item 1", "item 2", "item 3"], ordered=True)
    list_1.add("item 4")
    assert (
        str(list_1) == "1. item 1\n2. item 2\n3. item 3\n4. item 4\n"
    ), "String representation of ordered list is incorrect."
    assert list_1.items == [
        "item 1",
        "item 2",
        "item 3",
        "item 4",
    ], "List items are incorrect."


def test_unordered_list():
    """
    This function tests the markdown.List class.
    """
    list_1 = markdown.List(["item 1", "item 2", "item 3"], ordered=False)
    assert (
        str(list_1) == "- item 1\n- item 2\n- item 3\n"
    ), "String representation of unordered list is incorrect."


def test_named_list():
    """
    This function tests the markdown.List class.
    """
    list_1 = markdown.List(
        ["item 1", "item 2", "item 3"], ordered=False, title="my_list"
    )
    assert (
        str(list_1) == "### my_list\n- item 1\n- item 2\n- item 3\n"
    ), "String representation of unordered list is incorrect."
    assert list_1.title == "my_list", "List name is incorrect."


def test_link():
    """
    This function tests the markdown.Link class.
    """
    link_1 = markdown.Link("http://www.google.com", "Google")
    assert (
        str(link_1) == "[Google](http://www.google.com)\n"
    ), "String representation of link is incorrect."
    assert link_1.url == "http://www.google.com", "Link URL is incorrect."
    assert link_1.text == "Google", "Link text is incorrect."


def test_link_no_trailing():
    """
    This function tests the markdown.Link class.
    """
    link_1 = markdown.Link("http://www.google.com", "Google", trailing=False)
    assert (
        str(link_1) == "[Google](http://www.google.com)"
    ), "String representation of link is incorrect."
    assert link_1.url == "http://www.google.com", "Link URL is incorrect."
    assert link_1.text == "Google", "Link text is incorrect."


def test_link_no_text():
    """
    This function tests the markdown.Link class.
    """
    link_1 = markdown.Link("http://www.google.com")
    assert (
        str(link_1) == "[http://www.google.com](http://www.google.com)\n"
    ), "String representation of link is incorrect."
    assert link_1.url == "http://www.google.com", "Link URL is incorrect."
    assert link_1.text == "http://www.google.com", "Link text is incorrect."


def test_link_new_tab():
    """
    This function tests the markdown.Link class.
    """
    link_1 = markdown.Link("http://www.google.com", "Google", new_tab=True)
    assert (
        str(link_1) == "[Google](http://www.google.com target=_blank)\n"
    ), "String representation of link is incorrect."
    assert link_1.url == "http://www.google.com", "Link URL is incorrect."
    assert link_1.text == "Google", "Link text is incorrect."


def test_image():
    """
    This function tests the markdown.Image class.
    """
    image_1 = markdown.Image("http://www.google.com", alt="Google")
    assert (
        str(image_1) == "![Google](http://www.google.com)\n"
    ), "String representation of image is incorrect."
    assert image_1.url == "http://www.google.com", "Image URL is incorrect."
    assert image_1.alt == "Google", "Image text is incorrect."


def test_image_size():
    """
    This function tests the markdown.Image class.
    """
    image_1 = markdown.Image(
        "http://www.google.com", alt="Google", width=100, height=100
    )
    assert (
        str(image_1)
        == '<img src="http://www.google.com" alt="Google" width="100" height="100">'
    ), "String representation of image is incorrect."
    assert image_1.url == "http://www.google.com", "Image URL is incorrect."
    assert image_1.alt == "Google", "Image text is incorrect."
    assert image_1.width == 100, "Image width is incorrect."
    assert image_1.height == 100, "Image height is incorrect."


def test_image_no_alt():
    """
    This function tests the markdown.Image class.
    """
    image_1 = markdown.Image("http://www.google.com")
    assert (
        str(image_1) == "![http://www.google.com](http://www.google.com)\n"
    ), "String representation of image is incorrect."
    assert image_1.url == "http://www.google.com", "Image URL is incorrect."
    assert image_1.alt == "http://www.google.com", "Image text is incorrect."


def test_table():
    """
    This function tests the markdown.Table class.
    """
    table_1 = markdown.Table(["col 1", "col 2", "col 3"])
    assert (
        str(table_1) == "| col 1 | col 2 | col 3 |\n| --- | --- | --- |\n"
    ), "String representation of table is incorrect."
    assert table_1.headers == [
        "col 1",
        "col 2",
        "col 3",
    ], "Table columns are incorrect."


def test_table_add_row():
    """
    This function tests the markdown.Table class.
    """
    table_1 = markdown.Table(["col 1", "col 2", "col 3"])
    table_1.add_row({"col 1": "item 1", "col 2": "item 2", "col 3": "item 3"})
    assert (
        str(table_1)
        == "| col 1 | col 2 | col 3 |\n| --- | --- | --- |\n| item 1 | item 2 | item 3 |\n"
    ), "String representation of table is incorrect."
    assert table_1.headers == [
        "col 1",
        "col 2",
        "col 3",
    ], "Table columns are incorrect."
    assert table_1.rows == [
        {"col 1": "item 1", "col 2": "item 2", "col 3": "item 3"}
    ], "Table rows are incorrect."


def test_table_sort():
    """
    This function tests the markdown.Table class.
    """
    table_1 = markdown.Table(["Name", "Value"], sort_key="Value")
    table_1.add_row({"Name": "First", "Value": 1})
    table_1.add_row({"Name": "Second", "Value": 2})
    table_1.add_row({"Name": "Fourth", "Value": 4})
    table_1.add_row({"Name": "Third", "Value": 3})
    assert (
        str(table_1)
        == "| Name | Value |\n| --- | --- |\n| First | 1 |\n| Second | 2 |\n| Third | 3 |\n| Fourth | 4 |\n" # pylint: disable=line-too-long
    ), "Sorted Table is incorrect."
    assert table_1.headers == ["Name", "Value"], "Table columns are incorrect."
    table_1.sort_reverse = True
    assert (
        str(table_1)
        == "| Name | Value |\n| --- | --- |\n| Fourth | 4 |\n| Third | 3 |\n| Second | 2 |\n| First | 1 |\n" # pylint: disable=line-too-long
    ), "Reverse sorted Table is incorrect."
    table_1.sort_reverse = False
    table_1.sort_key = "Name"
    assert (
        str(table_1)
        == "| Name | Value |\n| --- | --- |\n| First | 1 |\n| Fourth | 4 |\n| Second | 2 |\n| Third | 3 |\n" # pylint: disable=line-too-long
    ), "Second sorted Table is incorrect."


def test_table_flexible():
    """
    This function tests the markdown.Table class.
    """
    table_1 = markdown.Table(["Name", "Value"], flexible_headers=True)
    table_1.add_row({"Name": "First", "Value": 1})
    table_1.add_row({"Name": "Second", "Value": 2})
    table_1.add_row({"Name": "Third", "Value": 3, "Extra": "Extra Value"})
    table_1.add_row({"Name": "Fourth", "Value": 4})
    assert (
        str(table_1)
        == "| Name | Value | Extra |\n| --- | --- | --- |\n| First | 1 |  |\n| Second | 2 |  |\n| Third | 3 | Extra Value |\n| Fourth | 4 |  |\n" # pylint: disable=line-too-long
    ), "Flexible Table is incorrect."
    assert table_1.headers == ["Name", "Value", "Extra"], "Table columns are incorrect."


def test_section():
    """
    This function tests the markdown.Section class.
    """
    section_1 = markdown.Section("Section 1")
    assert (
        str(section_1) == "# Section 1\n\n"
    ), "String representation of section is incorrect."
    assert section_1.title.text == "Section 1", "Section title is incorrect."


def test_section_add():
    """
    This function tests the markdown.Section class.
    """
    section_1 = markdown.Section("Section 1")
    section_1.add("This is a paragraph.")
    assert (
        str(section_1) == "# Section 1\nThis is a paragraph.  \n"
    ), "String representation of section is incorrect."


def test_document():
    """
    This function tests the markdown.Document class.
    """
    document_1 = markdown.Document("Document 1", filename="document_1.md")
    document_1.add_section(markdown.Section(markdown.Header("Section 1", 2)))
    assert (
        document_1.sections["Section 1"].title.text == "Section 1"
    ), "Section title is incorrect."
    section = document_1.sections["Section 1"]
    section.add("This is a paragraph.")
    assert (
        str(document_1) == "# Document 1\n## Section 1\nThis is a paragraph.  \n"
    ), "String representation of document is incorrect."


def test_document_save(tmp_path):
    """
    This function tests the markdown.Document class.
    """
    filename = tmp_path / "document_1.md"
    document_1 = markdown.Document("Document 1", filename=str(filename))
    print(filename)
    document_1.add_section(markdown.Section(markdown.Header("Section 1", 2)))
    assert (
        document_1.sections["Section 1"].title.text == "Section 1"
    ), "Section title is incorrect."
    section = document_1.sections["Section 1"]
    section.add("This is a paragraph.")
    document_1.save()
    assert filename.exists(), "File was not saved."
    assert (
        filename.read_text() == "# Document 1\n## Section 1\nThis is a paragraph.  \n"
    ), "File contents are incorrect."
