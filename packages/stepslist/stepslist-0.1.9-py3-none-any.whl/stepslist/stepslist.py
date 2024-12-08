import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class StepsPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        step_list = []
        in_steps = False

        for line in lines:
            if '<steps>' in line:
                in_steps = True
                continue  # Skip the <steps> line
            elif '</steps>' in line:
                in_steps = False
                if step_list:
                    new_lines.append(self.generate_steps_html(step_list))
                continue  # Skip the </steps> line
            
            if in_steps:
                # Extract list items from the line
                step_list.extend(self.extract_steps(line))
            else:
                new_lines.append(line)

        return new_lines

    def extract_steps(self, line):
        # Extract lines that start with a number followed by a period (e.g., 1. Step 1)
        return [step.strip() for step in line.splitlines() if re.match(r'^\d+\.\s', step.strip())]

    def generate_steps_html(self, step_list):
        # Create an ordered list with class "md-steps"
        list_items = ''.join(f'<li>{step}</li>' for step in step_list)
        return f'<ol class="md-steps">{list_items}</ol>'

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(StepsPreprocessor(), 'steps_preprocessor', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)