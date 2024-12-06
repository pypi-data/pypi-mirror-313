from rich.markdown import Markdown


class TruncatedMarkdown(Markdown):
    def __rich_console__(self, console, options):
        results = list(super().__rich_console__(console, options))
        height = console.height
        count = 0
        buffer = []
        for segment in reversed(results):
            count += segment.text.count("\n")  # type: ignore
            if count > height:
                break
            buffer.append(segment)

        yield from reversed(buffer)
