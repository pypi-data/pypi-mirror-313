import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class StepsPreprocessor(Preprocessor):
    def run(self, lines):
        # Join lines into a single string to process
        text = "\n".join(lines)

        # Use regex to find and replace <steps>...</steps> with <ol class="md-steps">...</ol>
        text = re.sub(r'<steps>(.*?)<\/steps>', r'<ol class="md-steps">\1</ol>', text, flags=re.DOTALL)

        # Split back into lines
        return text.splitlines(keepends=True)

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(StepsPreprocessor(), 'steps', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)