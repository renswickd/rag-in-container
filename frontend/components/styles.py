from pathlib import Path

def load_css() -> str:
    """Load CSS from file and return as string"""
    css_path = Path(__file__).parent.parent / "static" / "css" / "styles.css"
    with open(css_path, "r") as f:
        return f"<style>{f.read()}</style>"