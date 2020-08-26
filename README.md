https://kennytv.eu/secretgraph/
---

*Please don't judge me, web dev sucks*

## Usage
* `py main.py` to start a scheduler that will execute the task every day at 18:00 (6pm)
  * `-n` to execute the task instantly and only once
* `py collect-data-to-file.py` to iterate the entire `data` directory and save them for the web format into `servers.json`
  * `--date [date]` to only append data of the single `<date>.json` file from the `data` directory


This project uses [Chart.js](https://www.chartjs.org/).