.. meta::
   :author: Adam Korn
   :title: sphinx-inlinecode - embed source code blocks directly into Sphinx documentation
   :description: A Sphinx extension to embed source code blocks directly into Sphinx documentation


sphinx-inlinecode
--------------------

.. image:: https://img.shields.io/pypi/v/sphinx-inlinecode?color=eb5202
   :target: https://pypi.org/project/sphinx-inlinecode/
   :alt: sphinx-inlinecode PyPI Version

.. image:: https://img.shields.io/badge/GitHub-sphinx--inlinecode-4f1abc
   :target: https://github.com/tdkorn/sphinx-inlinecode/
   :alt: sphinx-inlinecode GitHub Repository

.. image:: https://static.pepy.tech/personalized-badge/sphinx-inlinecode?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads
    :target: https://pepy.tech/project/sphinx-inlinecode/

.. image:: https://readthedocs.org/projects/sphinx-inlinecode/badge/?version=latest
    :target: https://sphinx-inlinecode.readthedocs.io/en/latest/?badge=latest
    :alt: sphinx-inlinecode Documentation Status

.. only:: readme

   |

``sphinx-inlinecode`` is a Sphinx extension that embeds source code blocks directly into your documentation as a dropdown.


.. rubric:: Example


.. only:: not html

   .. image:: /_static/example.png
      :alt: embedded code block added by sphinx-inlinecode


.. only:: html

   .. autofunction:: sphinx_inlinecode.adjust_indentation
      :noindex:


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



.. only:: readme

   Documentation
   ~~~~~~~~~~~~~~~

   Full documentation can be found on |RTD|_


   .. |RTD| replace:: ReadTheDocs
   .. _RTD: https://sphinx-inlinecode.readthedocs.io/en/latest/
