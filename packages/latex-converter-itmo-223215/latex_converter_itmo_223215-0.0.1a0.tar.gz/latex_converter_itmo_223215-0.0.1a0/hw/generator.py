generate = lambda data: (
    "\t\t\\begin{tabular}{| " +
    " | ".join(["c"] * len(data[0])) + " |" +
    "}\n\t\t\\hline\n\t\t" +
    "\\\\\n\t\t\\hline\n\t\t".join(map(lambda row: " & ".join(map(lambda cell: str(cell), row)), data)) +
    "\\\\\n\t\t\\hline\n\t\t\\end{tabular}"
)

def image_generate(path, width):
    return (
        "\n\t\t\\begin{figure}[h!]\n" +
        "\t\t\\centering\n" +
        f"\t\t\\includegraphics[width={width}]{{{path}}}\n" +
        "\t\t\\end{figure}"
    )