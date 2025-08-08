# GCode Merger

A simple Python GUI tool that helps you merge two G-code files—one as the starting segment ("Start GCode") and the other as a continuation ("End GCode")—with an adjustable Z-axis lift. Built with Tkinter.

---

##  Features

- Intuitive graphical interface using `Tkinter`
- File selectors for:
  - **Start GCode**: the initial segment
  - **End GCode**: the continuation file
- Input field to apply a Z-axis offset (in millimeters) to the End GCode
- Automatic merging based on markers:
  - Detects `; filament end gcode` as the merge point in the Start file
  - Detects `;Layer: 0` or `;LAYER:0` as the start of the End file
- Save dialog to export the merged G-code

---

##  Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gcode-merger.git
   cd gcode-merger
