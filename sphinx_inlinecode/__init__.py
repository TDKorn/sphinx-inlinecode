import re
import sphinx
from pathlib import Path
from typing import Dict, Any, List, Optional
from sphinx.application import Sphinx
from bs4 import BeautifulSoup, Tag, NavigableString


__version__ = "1.3.0"
__author__ = 'Adam Korn <hello@dailykitten.net>'


def setup(app: Sphinx) -> Dict[str, Any]:
    app.connect("builder-inited", add_static_path)
    app.connect('build-finished', add_source_code)

    app.setup_extension('sphinx.ext.viewcode')
    app.add_css_file("sphinx-inlinecode.css")
    app.add_js_file('sphinx-inlinecode.js')

    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}


def add_static_path(app) -> None:
    """Add the path for the ``_static`` folder"""
    app.config.html_static_path.append(
        str(Path(__file__).parent.joinpath("_static").absolute())
    )


def add_source_code(app, exception):
    """Insert source code blocks into documentation entries."""
    viewcode_dir = Path(app.outdir).joinpath("_modules").absolute()
    if not viewcode_dir.exists():
        return

    html_files = get_html_files(viewcode_dir.parent)
    code_blocks = get_code_blocks(viewcode_dir)

    for file in html_files:
        if result := insert_source_code(file, code_blocks):
            file.write_text(str(result), encoding='utf-8')


def get_code_blocks(viewcode_dir: Path) -> Dict[str, Tag]:
    """Retrieve code blocks from HTML files generated by :mod:`sphinx.ext.viewcode`

    :param viewcode_dir: path of the ``build/html/_modules`` directory
    :return: mapping of fully qualified object names to their HTML code block
    """
    files = get_html_files(viewcode_dir)
    mapping = {}

    for file in files:
        soup = BeautifulSoup(file.read_text(encoding='utf-8'), 'html.parser')
        code_blocks = soup.findAll('div', 'viewcode-block')

        for block in code_blocks:
            backlink = block.find("a", "viewcode-back")
            qualname = backlink.get('href').split("#")[-1]
            mapping[qualname] = block

            # Remove internal link to documentation entry
            backlink.replace_with()

    return mapping


def get_html_files(root: Path) -> List[Path]:
    """Retrieves all HTML files contained in the specified directory

    :param root: path of the directory to search for HTML files in
    :return: list of all HTML files in the directory and its subdirectories
    """
    files = []

    for entry in root.iterdir():
        if entry.is_file() and entry.suffix == ".html":
            files.append(entry)
        elif entry.is_dir():
            files.extend(get_html_files(entry))

    return files


def insert_source_code(file: Path, code_blocks: Dict[str, Tag]) -> Optional[BeautifulSoup]:
    """Inserts source code blocks into the specified documentation HTML file.

    :param file: path to the HTML file.
    :param code_blocks: dictionary containing code block data.
    :return: HTML content of the file, with all code blocks inserted
    """
    soup = BeautifulSoup(file.read_text(encoding='utf-8'), 'html.parser')
    doc_entries = soup.findAll("dt", "sig sig-object py")

    if not doc_entries:
        return

    for doc_entry in doc_entries:
        viewcode_label = doc_entry.find("span", "viewcode-link")

        if not viewcode_label:
            continue

        viewcode_link = viewcode_label.parent

        if not (ref_id := doc_entry.get('id')):
            ref_id = get_ref_id(viewcode_link)

        # Insert formatted source code block after object signature.
        code_block = wrap_code_block(code_blocks[ref_id])
        doc_entry.append(code_block)

        # Remove viewcode link
        viewcode_link.replace_with()

    return soup


def get_ref_id(viewcode_link: Tag) -> str:
    """Parses the fully qualified object name from the viewcode internal reference

    :param viewcode_link: the viewcode internal reference
    :return: the fully qualified name of the referenced object
    """
    return viewcode_link.get('href').removeprefix("_modules/").replace("html#", "").replace("/", ".")


def wrap_code_block(code_block: Tag) -> BeautifulSoup:
    """Wraps the given code block inside a <details> HTML element.

    :param code_block: HTML of the code block to wrap.
    :return: the wrapped code block.
    """
    formatted_block = adjust_indentation(code_block)
    html = """
    <details class="sphinx-inlinecode">
        <summary>
            <span class="pre">View Source Code</span>
        </summary>
        <div class="highlight">
            <pre>{adjusted_code_block}</pre>
        </div>
    </details>
    """.format(adjusted_code_block=formatted_block)
    return BeautifulSoup(html, 'html.parser')


def adjust_indentation(code_block: Tag) -> Tag:
    """Adjusts indentation of the code block by removing common leading whitespace.

    :param code_block: HTML code block whose indentation needs adjustment.
    :return: code block with adjusted indentation.
    """
    contents = code_block.contents

    if not isinstance(contents[0], NavigableString):
        return code_block  # Block has no indentation

    initial_indent = len(contents[0])
    pattern = fr"[ ]{{{initial_indent}}}(.*)"

    for child in contents:
        if isinstance(child, NavigableString):
            replacement = re.sub(pattern, r"\1", child)
            child.replace_with(replacement)
        else:
            replacement = re.sub(pattern, r"\1", child.string)
            child.string = replacement

    return code_block
