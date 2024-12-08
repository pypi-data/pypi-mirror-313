from markdown import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re

class StepsBlockProcessor(BlockProcessor):
    """Custom block processor to handle <steps> tags."""
    
    def test(self, parent, block):
        """Test if the block starts with <steps>."""
        return block.startswith('<steps>')

    def run(self, parent, blocks):
        """Convert <steps> block to <ol class="md-steps">."""
        try:
            block = blocks.pop(0)
            content = self.extract_content(block)

            # Create an ordered list with class "md-steps"
            ol = etree.Element('ol', {'class': 'md-steps'})

            # Split the content into items
            items = self.parse_steps_content(content)
            for item in items:
                li = etree.Element('li')
                li.text = item
                # Append the <li> to the <ol>
                ol.append(li)

            # Append the ordered list to the parent
            parent.append(ol)
        except IndexError as e:
            print(f"Error processing steps: {e}")
            # Optionally, append a placeholder message to the parent
            parent.append(etree.Element('p', text='Error processing steps block.'))

    def extract_content(self, block):
        """Extract the content between <steps> and </steps>."""
        return re.sub(r'<steps>|</steps>', '', block).strip()

    def parse_steps_content(self, content):
        """Parse the content into individual steps."""
        # Split by the newline and filter empty lines
        return [line.strip() for line in content.splitlines() if line.strip()]

class StepsExtension(Extension):
    """Custom Markdown extension to process <steps> tags."""

    def extendMarkdown(self, md):
        """Register the block processor."""
        md.parser.blockprocessors.register(StepsBlockProcessor(md.parser), 'steps', 175)

def makeExtension(**kwargs):
    """Return an instance of the extension."""
    return StepsExtension(**kwargs)