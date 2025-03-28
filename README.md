# NASSTAT - National AirSpace STATistics
```
#####################################################################
#####################################################################
#####███╗░░██╗░█████╗░░██████╗░██████╗████████╗░█████╗░████████╗#####
#####████╗░██║██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝#####
#####██╔██╗██║███████║╚█████╗░╚█████╗░░░░██║░░░███████║░░░██║░░░#####
#####██║╚████║██╔══██║░╚═══██╗░╚═══██╗░░░██║░░░██╔══██║░░░██║░░░#####
#####██║░╚███║██║░░██║██████╔╝██████╔╝░░░██║░░░██║░░██║░░░██║░░░#####
#####╚═╝░░╚══╝╚═╝░░╚═╝╚═════╝░╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░#####
#####################################################################
#####################################################################
```
*Last updated: `Fri March 25 2025`*

A python wrapper of the United States Federal Aviation Authority's [National Airspace System](https://nasstatus.faa.gov/) API developed by [Dariel Cruz Rodriguez](dariel.us).

## Table of Contents
- [Dependencies](##Dependencies)
- [Installation](##Installation)
- [Attribution & Licensing](##Attributon)
- Models
  - [Airport()](###Airport)
- Methods
  - Airport
    - [.getDelays()](###getDelays)
      - [.getDepartureDelays()](###getDelays)
      - [.getArrivalDelays()](###getDelays)
    - [.averageDelay()](###averageDelay)
    - [.delayReasons()](###delayReasons)
    - [.isDelay()](###isDelay)
    - [.getPossibleDelays()](###getPossibleDelays)
    - [.getClosures()](###getClosures)
    - [.getPossibleDelays()](###getPossibleDelays)
    - [.getClosures()](###getClosures)
## Dependencies
Run this command to install the required packages:
```bash
pip install requests xml.etree.ElementTree json re
```

NASSTAT uses the following packages, many of which are included in the standard library of vanilla Python installations:
- `requests` - for making HTTP requests to the FAA's API
- `xml.etree.ElementTree` - for parsing the XML response from the FAA's API
- `json` - for parsing the JSON response from the FAA's API
- `re` - for regular expression matching

NASSTAT requires Python 3.11.0 or later. I'm not sure if it will work on older Python versions, so if you're confident it will you can override the Python version check by using `pip install nasstat --ignore-requires-python`.

## Installation
NASSTAT is published as a package on the [Python Package Index](https://pypi.org/project/nasstat/). To install this into your project run the command:

```bash
pip install nasstat
```
and to import it into your project, use the command:

```python
from nasstat import Airport
```

## Attribution & Licensing
### Attribution
Although it is not required, please attribute use of this package to the author, Dariel Cruz Rodriguez, by including a link to [dariel.us](https://dariel.us) in your project. As a college student, your attribution can be really helpful in building my portfolio and building a reputation in the data science community. If you are unable to attribute, or it doesn't make sense for your project, please feel free to [email me](mailto:hello@dariel.us) about your project so I can keep an internal note of it, I would love to hear about how you are using NASSTAT!

Additionally, the data provided by the FAA is licensed under the [Open Government License](https://www.data.gov/open-government-licensing/), which allows for free use and redistribution of the data. Thank you Uncle Sam!

### MIT License

Copyright (c) 2024 Dariel Cruz Rodriguez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Models
### Airport()
#### Importing
```python
MCO = Airport("MCO") # loads in an instance of MCO and all associated data with it
```
#### Attributes
- `airportid` (str): The airport IATA/ICAO code (e.g., "MCO", "KATL")
- `lastupdate` (datetime): The timestamp of when the airport data was last updated
- `airportclosures` (dict): Information about current airport closures, if any
- `airportdelays` (dict): Details about current delays including minimum, maximum, average delay times, and reasons
- `possibledelays` (dict): Information about potential upcoming delays

## Methods
### Airport.getDelays()
If you want to filter for just departure or arrival delays, use either `Airport.getDepartureDelays()` or `Airport.getArrivalDelays()`.

```python
airportcode = "MCO"
airport = Airport(airportcode)
delays = airport.getDelays()
print(delays)

# > {'Departure': {'minDelay': 31, 'maxDelay': 45, 'avgDelay': 38, 'reason': 'TM INITIATIVES:MIT:STOP&VOL'}}
```

```python
# In plain language, you can access items in the dictionary to form a string.
airportcode = "MCO"
airport = Airport(airportcode)
airport.getDelays()

if airport.airportdelays is None:
    print("There are no delays.")
else:
    for key, value in airport.airportdelays.items():
        print(f"There is a delay on {airportcode} {key}s averaging {value['avgDelay']} minutes (btwn. {value['minDelay']}-{value['maxDelay']} min) due to {value['reason']}.")

# > There is a delay on MCO Departures averaging 38 minutes (btwn. 31-45 min) due to TM INITIATIVES:MIT:STOP&VOL.
```

### Airport.averageDelay()
```python
airportcode = "MCO"
airport = Airport(airportcode)
print(airport.averageDelay())

# > 38.0
```

### Airport.delayReasons()
```python
airportcode = "PBI"
airport = Airport(airportcode)
print(airport.delayReasons())
# > "runway construction"
```

```python
# This method also returns multiple reasons as a plain language string (adding 'and' at the end of the list for the last reason)

airportcode = "LGA"
airport = Airport(airportcode)
print(airport.delayReasons())
# > "runway construction, wind, and TM INITIATIVES:MIT:STOP&VOL"
```
### Airport.isDelay()
```python
airportcode = "MCO"
airport = Airport(airportcode)
print(airport.isDelay())

# > True
```
```python
airportcode = "DEN"
airport = Airport(airportcode)
print(airport.isDelay())

# > "NAASTATUS Airport Delays is empty, attempting to refresh..."
# > False
```

### Airport.getPossibleDelays()
```python
airportcode = "DCA"
airport = Airport(airportcode)
print(airport.getPossibleDelays())

# > {'GROUND STOP/DELAY PROGRAM POSSIBLE': 'AFTER 1930'}
```
### Airport.getClosures()
```python
airportcode = "LAS"
airport = Airport(airportcode)
print(airport.getClosures())

# > [{'reason': '!LAS 03/121 LAS AD AP CLSD TO NON SKED TRANSIENT GA ACFT EXC 24HR PPR 702-261-7775 2503171851-2506252300', 'start': 'Mar 17 at 18:51 UTC.', 'reopen': 'Jun 25 at 23:00 UTC.'}]
```
