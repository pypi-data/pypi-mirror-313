
from pathlib import Path

def _load_md_files():
    current_dir = Path(__file__).parent
    md_files = current_dir.glob("*.md")

    # Dictionary to store module contents
    module_contents = {}

    for md_file in md_files:
        var_name = md_file.stem
        with open(md_file, 'r') as f:
            module_contents[var_name] = f.read().strip()

    return module_contents

# Load all MD files and add them to global namespace
globals().update(_load_md_files())

# Export all MD file variables
__all__ = [f.stem for f in Path(__file__).parent.glob("*.md")]
