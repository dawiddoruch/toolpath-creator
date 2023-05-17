# toolpath-creator

This script is part of my daily workflow. It automates daily task that used to take hours and was extremely prone to errors.

My workflow used to look something like this:

1. Make DWG/DXF drawings for panels (each panel individually and usually upwards of 40+ panels a day)
2. Use some software to do nesting (place as many as possible one one sheet of raw material) and export nested sheets.
3. Import each nested sheet into CAM software and prepare GCode for CNC router. Each line, tool, settings had to be selected manually and this resulted in many errors.

I have automated task #1 with ACM Drafter script - got that out of the way.
Still using software for nesting and exporting nested sheets as DXF files.

This script automates task #3 - takes bunch of DXF files and converts them into GCode. It eliminated all of CAM errors like: skipped holes, skipped cut lines, wrong tool settings or wrong tool in general.
