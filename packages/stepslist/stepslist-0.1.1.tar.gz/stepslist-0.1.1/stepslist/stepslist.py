import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class StepsPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        steps_pattern = re.compile(r'<steps>(.*?)</steps>', re.DOTALL)

        for line in lines:
            # Replace <steps></steps> with <ol class="md-steps"></ol> without <li> tags
            line = steps_pattern.sub(lambda m: f'<ol class="md-steps">{m.group(1).strip()}</ol>', line)
            new_lines.append(line)

        return new_lines

class StepsListExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(StepsPreprocessor(), 'stepslist', 175)

def makeExtension(**kwargs):
    return StepsListExtension(**kwargs)