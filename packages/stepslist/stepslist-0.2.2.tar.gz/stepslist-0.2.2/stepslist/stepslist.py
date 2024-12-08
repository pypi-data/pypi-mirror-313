import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

class StepsPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        in_steps = False
        current_content = []

        for line in lines:
            if '<steps>' in line:
                if in_steps:
                    continue  # If already in a steps block, ignore nested <steps>
                in_steps = True
                continue  # Skip the <steps> line
            elif '</steps>' in line:
                if not in_steps:
                    new_lines.append(line)  # Outside of steps, just add the line
                    continue
                in_steps = False
                # Wrap the collected content in an ordered list without converting to HTML
                new_lines.append(self.generate_steps_markdown(current_content))
                current_content = []  # Reset content for next potential steps
                continue  # Skip the </steps> line

            if in_steps:
                current_content.append(line)  # Collect content while inside <steps>
            else:
                new_lines.append(line)  # Add lines that are outside <steps>

        return new_lines

    def generate_steps_markdown(self, content):
        # Create an ordered list in Markdown format
        markdown_content = ''.join(content)
        return f'<ol class="md-steps">\n{markdown_content}\n</ol>'

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(StepsPreprocessor(), 'steps_preprocessor', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)