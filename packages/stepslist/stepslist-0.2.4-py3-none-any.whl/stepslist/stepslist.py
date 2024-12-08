import markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree

class StepsBlockProcessor(BlockProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test(self, parent, block):
        # Check if the block starts with <steps>
        return block.startswith('<steps>')

    def run(self, parent, blocks):
        # Pop the current block
        block = blocks.pop(0)
        content = []

        # Collect content until we find the closing </steps>
        while blocks and not blocks[0].startswith('</steps>'):
            content.append(blocks.pop(0))

        # If we found the closing tag, pop it
        if blocks and blocks[0].startswith('</steps>'):
            blocks.pop(0)

        # Join the content and convert it to HTML
        markdown_content = ''.join(content)
        html_content = markdown.markdown(markdown_content)

        # Create an ordered list element with class "md-steps"
        ol = etree.Element('ol', {'class': 'md-steps'})
        ol.text = html_content  # Set the inner HTML content

        # Append the ordered list to the parent element
        parent.append(ol)

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(StepsBlockProcessor(md.parser), 'steps', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)