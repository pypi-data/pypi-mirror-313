import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class StepPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        step_list = []
        in_step = False

        for line in lines:
            if '<step>' in line:
                in_step = True
                step_list.append(self.strip_tags(line))
            elif '</step>' in line:
                in_step = False
                new_lines.append(f'<li>{" ".join(step_list)}</li>')
                step_list = []
            else:
                if in_step:
                    step_list.append(self.strip_tags(line))
                else:
                    new_lines.append(line)

        if step_list:
            new_lines.append(f'<li>{" ".join(step_list)}</li>')

        return new_lines

    def strip_tags(self, text):
        return re.sub(r'<.*?>', '', text)

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(StepPreprocessor(), 'step_preprocessor', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)