from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from typing import List, Tuple


class YamlHighlighter(QSyntaxHighlighter):
    """
    A syntax highlighter for YAML files.

    Highlights YAML keys, values, and comments with different text formats to
    improve readability in a text editor.
    """

    def __init__(self, parent) -> None:
        """
        Initialize the YamlHighlighter.

        Defines highlighting rules for YAML syntax, including keys, values, and comments.

        :param parent: The text document to which the highlighter will be applied.
        """
        super().__init__(parent)
        self.highlighting_rules: List[Tuple[QRegularExpression, QTextCharFormat]] = (
            []
        )  # List of highlighting rules.

        # Define format for YAML keys
        key_format = QTextCharFormat()
        key_format.setForeground(QColor("blue"))  # Set text color to blue.
        key_format.setFontWeight(QFont.Weight.Bold)  # Set text to bold.
        self.highlighting_rules.append(  # Match YAML keys (e.g., "key:").
            (QRegularExpression(r"^\s*[\w\-]+(?=\s*:)"), key_format)
        )

        # Define format for YAML values
        value_format = QTextCharFormat()
        value_format.setForeground(QColor("darkgreen"))  # Set text color to dark green.
        self.highlighting_rules.append(  # Match YAML values (e.g., ": value").
            (QRegularExpression(r":\s*.*"), value_format)
        )

        # Define format for YAML comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("gray"))  # Set text color to gray.
        comment_format.setFontItalic(True)  # Set text to italic.
        self.highlighting_rules.append(  # Match YAML comments (e.g., "# comment").
            (QRegularExpression(r"#.*"), comment_format)
        )

    def highlightBlock(self, text: str) -> None:
        """
        Apply highlighting to a block of text.

        This method is called automatically by the QTextDocument to apply
        syntax highlighting to the given text block.

        :param text: The text block to highlight.
        """
        for (
            pattern,
            fmt,
        ) in self.highlighting_rules:  # Iterate over defined highlighting rules.
            match_iterator = pattern.globalMatch(
                text
            )  # Find all matches of the pattern in the text.
            while match_iterator.hasNext():  # Iterate through all matches.
                match = match_iterator.next()
                self.setFormat(
                    match.capturedStart(), match.capturedLength(), fmt
                )  # Apply the format to the match.
