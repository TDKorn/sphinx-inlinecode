import re
import sys
import sphinx
import inspect

from pathlib import Path
from typing import Dict, Any
from bs4 import BeautifulSoup, Tag
from functools import cached_property

from sphinx import addnodes
from sphinx.application import Sphinx
from pygments.lexers.python import PythonLexer


__version__ = "2.0.1"
__author__ = 'Adam Korn <hello@dailykitten.net>'


#: Object types that can't have code blocks inserted
BAD_OBJTYPES = ("attribute", "data", "decorator")


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


def add_source_code(app: Sphinx, exception) -> None:
    """Inserts source code blocks into documentation entries."""
    if app.builder.name != 'html':
        return

    highlighter = app.builder.highlighter
    outdir = Path(app.builder.outdir)
    objects = parse_py_domain(app)

    for doc in app.env.found_docs:  # Check if the file has any documentation entries
        if app.env.get_doctree(doc).traverse(addnodes.desc_signature):
            file = outdir.joinpath(f"{doc}.html")
            add_code_blocks(file, objects, highlighter)


def parse_py_domain(app) -> Dict[str, Any]:
    """Parses all Python objects in the package from the :external:class:`~.BuildEnvironment`

    :returns: a dictionary mapping fully qualified object names to the actual objects
    """
    py_objects = app.env.domaindata.get('py', {}).get("objects", {})
    object_map = {}

    for qualname, entry in py_objects.items():
        if entry.objtype in ("attribute", "data", "decorator"):
            continue  # Cannot get source code lines

        parts = entry.node_id.removeprefix('module-').split('.')

        if entry.objtype in ("class", "function", "module", "exception"):
            module = '.'.join(parts[:-1]).removeprefix('module-')
            fullname = parts[-1]

        elif entry.objtype in ("method", "property"):
            module = '.'.join(parts[:-2])
            fullname = '.'.join(parts[-2:])

        else:
            continue

        submod = sys.modules.get(module)
        if submod is None:
            continue

        obj = submod
        for part in fullname.split('.'):
            try:
                obj = getattr(obj, part)
            except AttributeError:
                continue

        if isinstance(obj, property):
            obj = obj.fget
        elif isinstance(obj, cached_property):
            obj = obj.func

        object_map[qualname] = obj

    return object_map


def add_code_blocks(file: Path, objects: Dict[str, Any], highlighter: "PythonLexer") -> None:
    """Inserts source code blocks into the provided HTML file and writes the output.

    :param file: path to the HTML file.
    :param objects: dictionary containing the objects in the package
    :param highlighter: the Pygments lexer to highlight source code blocks with
    """
    soup = BeautifulSoup(file.read_text(encoding='utf-8'), 'html.parser')
    doc_entries = soup.findAll("dt", "sig sig-object py")

    for doc_entry in doc_entries:
        if doc_entry.parent['class'][-1] in BAD_OBJTYPES:
            continue

        target = doc_entry.get('id')
        viewcode_label = doc_entry.find("span", "viewcode-link")

        if not target:
            if not viewcode_label:
                continue
            else:
                target = get_target(viewcode_label.parent)

        if not (obj := objects.get(target)):
            continue

        # Highlight and insert the source code block after the object signature
        code_block = get_code_block(target, obj, highlighter)
        doc_entry.append(code_block)

        if viewcode_label:  # Remove the viewcode link, if it exists
            viewcode_label.parent.replace_with()

    file.write_text(str(soup), encoding='utf-8')


def get_target(viewcode_link: Tag) -> str:
    """Parses the fully qualified object name from the viewcode internal reference

    :param viewcode_link: the viewcode internal reference
    :return: the fully qualified name of the referenced object
    """
    return viewcode_link.get('href').removeprefix("_modules/").replace("html#", "").replace("/", ".")


def get_code_block(qualname: str, obj: Any, highlighter: PythonLexer) -> BeautifulSoup:
    """Parses and highlights the source code lines of the provided object

    :param qualname: the fully qualified name of the object
    :param obj: the actual object to retrieve the source code lines from
    :param highlighter: the Pygments lexer to highlight the code block with
    :return: the highlighted and fully formatted HTML codeblock to insert
    """
    sourcelines, _ = inspect.getsourcelines(obj)
    initial_indent = len(sourcelines[0]) - len(sourcelines[0].lstrip())

    if initial_indent:  # Remove common leading whitespace
        pattern = fr"[ ]{{{initial_indent}}}(.*)"
        sourcelines = (
            re.sub(pattern, r"\1", line)
            for line in sourcelines
        )
    # Convert to HTML code block with syntax highlighting
    highlighted = highlighter.highlight_block(
        source=''.join(sourcelines),
        lang='python',
        linenos=False
    )
    lines = highlighted.splitlines()
    before, after = re.split(r"<pre>(?:<span></span>)?", lines[0])
    lines[0] = f'{before}<pre><div class="viewcode-block" id="{qualname}">{after}'

    code_block = '\n'.join(lines)
    return wrap_code_block(code_block)


def wrap_code_block(code_block: str) -> BeautifulSoup:
    """Wraps the given code block inside a ``<details>`` HTML element

    :param code_block: HTML of the code block to wrap
    :return: the wrapped code block
    """
    html = f"""
    <details class="sphinx-inlinecode">
        <summary>
            <span class="pre">View Source Code</span>
        </summary>
        {code_block}
    </details>
    """
    return BeautifulSoup(html, 'html.parser')
