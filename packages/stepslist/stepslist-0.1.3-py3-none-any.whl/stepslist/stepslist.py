import re
from markdown import Extension
from markdown.preprocessors import Preprocessor

class StepsPreprocessor(Preprocessor):
    def run(self, lines):
        # Join lines to process multi-line content
        text = '\n'.join(lines)
        
        # Define a regex pattern to find <steps> blocks
        steps_pattern = re.compile(r'<steps>(.*?)</steps>', re.DOTALL)
        
        # Function to replace found <steps> blocks
        def replace_steps(match):
            steps_content = match.group(1)
            # Split the content by lines
            steps_lines = steps_content.splitlines()
            output_lines = ['<ol class="md-steps">']
            
            for line in steps_lines:
                # Remove leading/trailing whitespace
                stripped_line = line.strip()
                
                if stripped_line:  # Non-empty line
                    # Check if the line starts with a number followed by a dot
                    if re.match(r'^\d+\.', stripped_line):
                        # This is a step, create a list item
                        step_text = stripped_line[2:].strip()  # Remove number and dot
                        output_lines.append(f'<li>{step_text}</li>')
                    else:
                        # This is normal markdown text, wrap it in <p>
                        output_lines.append(f'<p>{stripped_line}</p>')
                else:
                    # Preserve empty lines
                    output_lines.append('')

            output_lines.append('</ol>')
            return '\n'.join(output_lines)
        
        # Replace the content inside <steps> tags with processed content
        text = steps_pattern.sub(replace_steps, text)
        
        # Return the modified lines
        return text.splitlines()

class StepsExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(StepsPreprocessor(), 'steps', 175)

def makeExtension(**kwargs):
    return StepsExtension(**kwargs)