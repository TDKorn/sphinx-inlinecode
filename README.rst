

.. meta::
   :author: Adam Korn
   :title: sphinx-inlinecode - embed source code blocks directly into Sphinx documentation
   :description: A Sphinx extension to embed source code blocks directly into Sphinx documentation


sphinx-inlinecode
--------------------

``sphinx-inlinecode`` is a Sphinx extension that embeds source code blocks directly into your documentation as a dropdown.


**Example**

.. image:: https://raw.githubusercontent.com/TDKorn/sphinx-inlinecode/main/docs/source/_static/example.png
   :alt: embedded code block added by sphinx-inlinecode

|

Installation
~~~~~~~~~~~~

To install ``sphinx-inlinecode`` via pip::

   pip install sphinx-inlinecode


Configuration
~~~~~~~~~~~~~~

Add the extension to your ``conf.py``

.. code-block:: python

   extensions = [
       "sphinx_inlinecode",
   ]


