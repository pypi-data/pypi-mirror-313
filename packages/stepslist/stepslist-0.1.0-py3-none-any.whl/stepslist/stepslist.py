from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import markdown

class StepsPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        in_steps = False
        steps_list = []

        for line in lines:
            # Check for opening <steps> tag
            if '<steps>' in line:
                in_steps = True
                steps_list.append(line.replace('<steps>', ''))
            elif '</steps>' in line and in_steps:
                in_steps = False
                steps_list.append(line.replace('</steps>', ''))
                # Wrap the steps list in an ordered list
                steps_html = '<ol class="md-steps">\n' + ''.join(f'<li>{step.strip()}</li>\n' for step in steps_list) + '</ol>'
                new_lines.append(steps_html)
                steps_list = []
            elif in_steps:
                steps_list.append(line)
            else:
                new_lines.append(line)

        return new_lines

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(StepsPreprocessor(), 'stepslist', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)