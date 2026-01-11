import importlib.resources

PACKAGE="hangman.res"

def copy_text_resource(resource: str, dest_path: str):
    with importlib.resources.open_text(PACKAGE, resource, encoding='utf-8') as src, open(dest_path, 'w', encoding='utf-8') as dst:
        for line in src:
            dst.write(line)