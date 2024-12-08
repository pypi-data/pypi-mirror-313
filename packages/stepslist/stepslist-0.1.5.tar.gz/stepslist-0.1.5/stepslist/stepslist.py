import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import xml.etree.ElementTree as etree
import re

class StepPreprocessor(Preprocessor):
    def run(self, lines):
        # Join the lines together to form a single text block
        text = "\n".join(lines)

        # Use regex to find <step>...</step> tags
        step_pattern = r'<step>(.*?)</step>'
        steps = re.findall(step_pattern, text, re.DOTALL)

        # Create the ordered list with class "md-steps"
        if steps:
            ol = etree.Element('ol', {'class': 'md-steps'})
            for step in steps:
                li = etree.SubElement(ol, 'li')
                # Convert the step content to Markdown
                li.text = markdown.markdown(step.strip())
            # Replace original <step> tags with the generated <ol>
            text = re.sub(step_pattern, '', text)
            text += etree.tostring(ol, encoding='unicode')

        # Return the modified lines
        return text.splitlines()

class StepExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(StepPreprocessor(), 'step_preprocessor', 15)

def makeExtension(**kwargs):
    return StepExtension(**kwargs)