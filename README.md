# Chess-Torunament-Analyzer
## What is Chess Tournament Analyzer?
Chess Tournament Analyzer is a small web-scraping based tool to analyze chess-results websites (e.g. https://chess-results.com/tnr792656.aspx) and determine underrated players based on their recent performances.
The tool uses simple HTTP requests to fetch the list of participants. Afterwards, for each FideID found a HTTP GET request is performed to evaluate recent rating changes. 
This tool might help some chess players to decide whether it is feasible to gain rating in a given tournament from mathematical perspective.

## How to use Chess Tournament Analyzer?

First, clone the project using git with 
```git
git clone https://github.com/ManuAndy/chess-analyzer.git
```
Afterwards install all the needed dependencies:
```bash
pip3 install selenium
pip3 install bs4
pip3 install flask
pip3 install flask_cors
```
When this is done, you should start the backend server (it will run on port 5000) with 

```bash
python3 server.py
```

The frontend server of the application shall also be started. For example, you can use live-server extension with VS Code on any other port (e.g. 5500).

Have fun using Chess Tournament Analyzer!
