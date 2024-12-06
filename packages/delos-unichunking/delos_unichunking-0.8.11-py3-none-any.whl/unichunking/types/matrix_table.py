"""Class used to represent and handle table/chart objects."""


class MatrixTable:
    """Class for handling tables and charts in a functional structure, allowing algorithmic correction and reading.

    Fields:
        title: Title of the table, empty by default.
        content: Matrix representation of the table content.
        is_chart: Boolean marker indicating whether the data table must be read as a chart.
    """

    def __init__(
        self: "MatrixTable",
        title: str,
        content: list[list[str]],
        is_chart: bool = False,
    ) -> None:
        """Create a MatrixTable object."""
        self.title: str = title
        self.content: list[list[str]] = content
        self.is_chart: bool = is_chart

    def abort(self: "MatrixTable") -> bool:
        """Returns a boolean value indicating whether the table is smaller than 2x2, in which case must be read as a string."""
        return len(self.content) <= 1 or len(self.content[0]) <= 1

    def read(self: "MatrixTable") -> str:
        """Returns a string representing the table/chart with its title and content."""
        if self.is_chart:
            return (
                "** Chart : "
                + str(self.title)
                + " "
                + str(self.content)
                + " ; End Of Chart ** "
            )
        return (
            "** Table : "
            + str(self.title)
            + " "
            + str(self.content)
            + " ; End Of Table ** "
        )

    def read_as_str(self: "MatrixTable") -> str:
        """Returns a string containing all the text in the table, without any structure."""
        text = self.title + " "
        for i in range(len(self.content)):
            for j in range(len(self.content[0])):
                text += self.content[i][j] + " "
        return text
