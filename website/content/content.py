from markdown import Markdown
import os

from website import config

CONTENT_PATH = config.CONTENT_PATH  # Read content path from config module.

class MarkdownPage:
    id: str  # Unique identifier for a markdown page; filename without ".md"
    content: str  # Markdown file content converted to HTML
    meta: dict  # Markdown metadata

    def __init__(self, id: str):
        """Convenience class for converting Markdown files into HTML.

        id: Markdown page ID; the filename without ".md".
        """
        self.id = id

        # Open the Markdown file and convert to HTML.
        self.content = None
        with open(f"{CONTENT_PATH}/{id}.md", encoding="utf-8") as f:
            self.content = f.read()
        md = Markdown(extensions=["fenced_code", "meta"], output_format="html5") # Extensions for code snippets and meta header
        self.content = md.convert(self.content)

        # Read Markdown meta header.
        self.meta = {}
        for key, value in md.Meta.items():
            self.meta[key] = value[0]


    def __repr__(self):
        """Allow MarkdownPage to be printed.
        
        returns: Markdown HTML content.
        """
        return self.content


class MarkdownCatalog:
    page_ids: list[str] = []  # Keep a list of MarkdownPage IDs.

    def __init__(self):
        self.load_pages()


    def load_pages(self):
        """Load Markdown page IDs.

        Identifies Markdown files in website/content/
        and builds their respective ID strings so that MarkdownPage(id)
        can be called dynamically without having to load the whole 
        MarkdownPage into memory.
        """
        self.page_ids = [f.replace(".md", "") for f in os.listdir(CONTENT_PATH) if f.endswith(".md")]
            
