StepsList
=========================================

A Markdown extension for MkDocs that converts `<steps>` tags into an ordered list with a class of `md-steps` to use in CSS to style your lists.

# Installation

You can install this package using pip:

```bash
pip install stepslist
```

# Usage

To use this extension, add it to your MkDocs configuration file (`mkdocs.yml`):

```
markdown_extensions:
  - stepslist
```
Now, you can use the `<steps>` tag in your Markdown files:

```
<steps>
1. Step one
2. Step two
3. Step three
</steps>
```
This will be rendered as an ordered list:

```
<ol class="md-steps">
<li>Step one</li>
<li>Step two</li>
<li>Step three</li>
</ol> 
```

_This project is licensed under the MIT License._