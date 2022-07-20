# Script Location Visualizer

Extremely rough code sketch for visualizing characters' locations as they pass through a narrative.

### Concept
Inspired by Randall Munroe's [Movie Narrative Charts](https://xkcd.com/657/) I wondered if I could automatically generate similar diagrams by parsing freely available scripts.

In particular I was inspired by Seinfeld scripts since where characters are (and how/when they come together) seemed like the basis of its humor.

Script parsing based on [Adrien Luxey's Da Fonky Movie Script Parser](https://raw.githubusercontent.com/Adrien-Luxey/Da-Fonky-Movie-Script-Parser/master/movie_script_parser.py)

### How to Use
* download a script into `scripts/`
* update global variables at the top of `script.py`
* run the code
* save the graphics

### TODO
* collapse spans if neighboring place is the same (commercial break?)
* mode to save renders directly
* Batch process multiple scripts
* nicer drawing
    * less cluttered
    * more handdrawn / artsy ala Munroe
* clear up bogus scenes:
    * inserts(?)
    * remove scenes with no characters
* try to pull out / trace objects?

