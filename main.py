###################################################################
###################################################################
####███╗░░██╗░█████╗░░██████╗░██████╗████████╗░█████╗░████████╗####
####████╗░██║██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝####
####██╔██╗██║███████║╚█████╗░╚█████╗░░░░██║░░░███████║░░░██║░░░####
####██║╚████║██╔══██║░╚═══██╗░╚═══██╗░░░██║░░░██╔══██║░░░██║░░░####
####██║░╚███║██║░░██║██████╔╝██████╔╝░░░██║░░░██║░░██║░░░██║░░░####
####╚═╝░░╚══╝╚═╝░░╚═╝╚═════╝░╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░####
#### A WRAPPER OF FAA AIRSPACE DATA BY DARIEL CRUZ RODRIGUEZ ######
###################################################################
###################################################################

import requests
import json
import xml.etree.ElementTree as ET
import re

class Airport():
    """
    Class that represents an airport, and provides methods to retrieve data from it.
    """
    def __init__(self, airportid):
        """
        Constructor for the Airport class, takes only one input, the FAA airport ID.

        Inputs:
            - FAA Airport ID (string): The FAA airport ID.

        Outputs:
            - None

        Example:
            airport = Airport("MCO")
            Retrieves information from Orlando International Airport in Orlando, Florida, which uses
            the FAA airport ID "MCO". Only valid for U.S. domestic airports.
        """
        self.airportid = airportid
        self.airportdelays = None

    def getDelays(self):
            """
            Fetches live airport delay data from the FAA NAS Status API and updates self.airportdelays.

            Outputs:
                - None (updates self.airportdelays)
            """
            
            try:
                response = requests.get("https://nasstatus.faa.gov/api/airport-status-information")
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Error fetching data: {e}")
                return

            # Helper function: Convert text like "1 hour and 24 minutes" to minute format
            def parse_minutes(time_str):
                numbers = re.findall(r"(\d+)", time_str.lower())
                if "hour" in time_str.lower():
                    hours = int(numbers[0]) if len(numbers) >= 1 else 0
                    minutes = int(numbers[1]) if len(numbers) >= 2 else 0
                    return hours * 60 + minutes
                elif "minute" in time_str.lower():
                    return int(numbers[0]) if numbers else 0
                return 0

            # Helper function: search FAA's XML for airport delays
            def parse_faa_xml(xml_string):
                root = ET.fromstring(xml_string)
                delays = {}

                for delay_type in root.findall("Delay_type"):

                    # Ground Delays
                    for ground_delay in delay_type.findall(".//Ground_Delay"):
                        arpt = ground_delay.find("ARPT").text if ground_delay.find("ARPT") is not None else None
                        if arpt and arpt.upper() == self.airportid:
                            reason = ground_delay.find("Reason").text if ground_delay.find("Reason") is not None else "Unknown"
                            max_delay = ground_delay.find("Max").text if ground_delay.find("Max") is not None else "0 minutes"
                            avg_delay = ground_delay.find("Avg").text if ground_delay.find("Avg") is not None else "0 minutes"
                            min_delay = avg_delay  # Approximate min delay as avg for missing data
                            
                            delays["Ground"] = {
                                "minDelay": parse_minutes(min_delay),
                                "maxDelay": parse_minutes(max_delay),
                                "avgDelay": parse_minutes(avg_delay),
                                "reason": reason
                            }

                    # Arrival/Departure Delays
                    for delay in delay_type.findall(".//Delay"):
                        arpt = delay.find("ARPT").text if delay.find("ARPT") is not None else None
                        if arpt and arpt.upper() == self.airportid:
                            reason = delay.find("Reason").text if delay.find("Reason") is not None else "Unknown"

                            for arr_dep in delay.findall("Arrival_Departure"):
                                delay_category = arr_dep.get("Type", "Unknown")
                                min_delay = arr_dep.find("Min").text if arr_dep.find("Min") is not None else "0 minutes"
                                max_delay = arr_dep.find("Max").text if arr_dep.find("Max") is not None else "0 minutes"
                                avg_delay = (parse_minutes(min_delay) + parse_minutes(max_delay)) // 2  # Approximate avg
                                
                                delays[delay_category] = {
                                    "minDelay": parse_minutes(min_delay),
                                    "maxDelay": parse_minutes(max_delay),
                                    "avgDelay": avg_delay,
                                    "reason": reason
                                }

                return delays if delays else None

            self.airportdelays = parse_faa_xml(response.text)
    
    def isDelay(self):
        """
        Returns True if the airport is experiencing delays, False otherwise.

        Inputs:
            - None
        Outputs:
            - Boolean: True if the airport is experiencing delays, False otherwise.
        """
        if self.airportevents is None:
            try:
                print("Airport events is None, trying to refresh...")
                self.getDelays()
            except Exception as e:
                print(f"Error while fetching airport events: {e}")
                return False 

        return self.airportdelays is not None
