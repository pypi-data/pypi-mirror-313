import markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re

class StepsProcessor(BlockProcessor):
    def test(self, parent, block):
        return block.startswith("<steps>")

    def run(self, parent, blocks):
        # Get the entire block
        block = blocks.pop(0)

        # Remove <steps> and </steps>
        content = re.sub(r"<steps>(.*?)</steps>", r"\1", block, flags=re.DOTALL).strip()

        # Create an ordered list with class "md-steps"
        ol = etree.Element('ol')
        ol.set('class', 'md-steps')

        # Split content into lines and create list items
        for line in content.splitlines():
            line = line.strip()
            if line:
                li = etree.SubElement(ol, 'li')
                li.text = line

        # Append the ordered list to the parent
        parent.append(ol)

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(StepsProcessor(md.parser), 'steps', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)

# Sample usage
if __name__ == "__main__":
    text = """
<steps>
1. Add a default (fallback) email address to `config/_default/params.toml`:
2. Add the following CSS to `assets/scss/common/_custom.scss`:
3. Create shortcode file `layouts/shortcodes/email.html` with the following content:
</steps>
"""

    md = markdown.Markdown(extensions=[makeExtension()])
    html = md.convert(text)
    print(html)