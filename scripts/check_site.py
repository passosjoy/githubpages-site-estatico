"""Valida o site estático: HTML bem formado e links internos apontando para arquivos existentes."""
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {"meta", "link", "img", "br", "hr", "input", "source", "area", "base", "col", "embed", "track", "wbr"}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.links, self.errors = [], [], []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.links.append(value)
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"tag </{tag}> fechada fora de ordem (linha {self.getpos()[0]})")
        else:
            self.stack.pop()


def main(root: Path) -> int:
    errors = []
    pages = sorted(root.rglob("*.html"))
    for page in pages:
        checker = Checker()
        checker.feed(page.read_text(encoding="utf-8"))
        errors += [f"{page}: {e}" for e in checker.errors]
        errors += [f"{page}: tag <{t}> não fechada" for t in checker.stack]
        for link in checker.links:
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (page.parent / link.split("#")[0]).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{page}: link quebrado -> {link}")
    for e in errors:
        print("ERRO", e)
    print(f"{len(pages)} página(s), {len(errors)} erro(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else "site")))
