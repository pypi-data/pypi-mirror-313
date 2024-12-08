import markdown
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree

class StepsProcessor(BlockProcessor):
    """
    A custom BlockProcessor that transforms <steps>...</steps> into
    <ol class="md-steps">...</ol> and prevents nested <ol> elements.
    """

    def test(self, parent, block):
        # Check if the block starts with <steps>
        return block.startswith('<steps>')

    def run(self, parent, blocks):
        # Get the block and convert it
        block = blocks.pop(0)
        content = block[len('<steps>'):-len('</steps>')].strip()

        # Create the <ol> element
        ol = etree.Element('ol')
        ol.set('class', 'md-steps')

        # Split the content into lines and process them
        for line in content.splitlines():
            # Create a list item for each line
            li = etree.SubElement(ol, 'li')
            li.text = line.strip()
        
        # Append the <ol> to the parent
        parent.append(ol)

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(StepsProcessor(md.parser), 'steps', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)