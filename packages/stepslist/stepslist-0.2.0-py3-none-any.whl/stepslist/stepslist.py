import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class StepsPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        in_steps = False
        current_content = []

        for line in lines:
            if '<steps>' in line:
                in_steps = True
                continue  # Skip the <steps> line
            elif '</steps>' in line:
                in_steps = False
                # When closing tag is found, convert the collected content into an ordered list
                new_lines.append(self.generate_steps_html(current_content))
                current_content = []  # Reset content for next potential steps
                continue  # Skip the </steps> line
            
            if in_steps:
                current_content.append(line)  # Collect content while inside <steps>
            else:
                new_lines.append(line)  # Add lines that are outside <steps>

        return new_lines

    def generate_steps_html(self, content):
        # Create an ordered list with class "md-steps"
        content_html = ''.join(content)  # Join collected lines into a single string
        return f'<ol class="md-steps">{content_html}</ol>'

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(StepsPreprocessor(), 'steps_preprocessor', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)