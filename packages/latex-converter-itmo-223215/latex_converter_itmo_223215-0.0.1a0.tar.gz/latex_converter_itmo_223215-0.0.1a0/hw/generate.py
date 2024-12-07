from generator import image_generate, generate

data = [
    ["Date", "Event", "Place"],
    [1818, "Was born", "Orel"],
    [1827, "Studying in a boarding school", "Moscow"],
    [1833, "Entered in University", "Moscow"],
    [1834, "Transfer to St. Petersburg University", "St. Petersburg"],
    [1852, "\"Notes of a hunter\" in the \"Sovremennik\"", "St. Petersburg"],
    [1856, "\"Rudin\" novel", "St. Petersburg"],
]

latex_table = generate(data)
latex_picture = image_generate(path="picture.png", width="\\linewidth")

latex_document = (
    "\\documentclass{article}\n" +
    "\\usepackage[utf8]{inputenc}\n" +
    "\\usepackage{graphicx}\n" +
    "\t\\begin{document}\n" +
    latex_table +
    "\n" +
    latex_picture +
    "\n\t\\end{document}"
)

with open("../artifacts/task2.tex", "w", encoding="utf-8") as f:
    f.write(latex_document)