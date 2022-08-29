"""Exceptions raised within this package."""


class LutraError(Exception):
    """Pretty-printed exceptions from this package."""

    def __init__(self, *, reference: str, message: str, hint_stmt: str) -> None:
        """Initialize."""
        super().__init__(message)
        self.reference = reference
        self.message = message
        self.hint_stmt = hint_stmt

    def __str__(self) -> str:
        """Make string representations pretty.

        This is formatted in this manner to have a nicer presentation style, when
        presented by Sphinx 4.
        """
        lines = [f"lutra-{self.reference})", "", self.message]
        if self.hint_stmt is not None:
            lines.append(f"[hint] {self.hint_stmt}")
            lines.append("")
        lines.append("(this will cause a build failure")
        return "\n".join(lines)
