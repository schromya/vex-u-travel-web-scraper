import requests
from bs4 import BeautifulSoup
from google_flight_analysis.scrape import Scrape

class Competition():
    def __init__(self, url):
        self.url = url
        self.name = ""
        self.date_start = ""
        self.date_end = ""
        self.registration_deadline = ""
        self.address = ""
        self.city_state = ""
        self.zip = ""
        self.spots_open = ""
        self.capacity =""
        self.registration_cost = ""
        self.flight_cost = -1
        self.flight_link = ""
        self.IS_CAR_RENTAL_NEEDED = True
        self.notes = ""

    def get_attributes(self):
        # Directly returns the attributes in the order initialized
        return self.__dict__

def scrape_robot_events_competition_page(comp:Competition) -> None:
    URL = comp.url
    response = requests.get(URL)
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')

        comp.name = soup.find('h3').get_text().strip()

        # Parse event data
        event_soup = soup.find('dl')

        event_data = event_soup.get_text().split()

        event_date_idx = event_data.index("Date") + 1
        comp.date_start = event_data[event_date_idx]
        if event_data[event_date_idx + 1] == "-":
            comp.date_end = event_data[event_date_idx + 2]
        else:
            comp.date_end = comp.date_start


        comp.registration_deadline = event_data[event_data.index("Deadline") + 1]
        comp.capacity = event_data[event_data.index("Capacity") + 1]
        comp.spots_open = event_data[event_data.index("Open") + 1]
        if "Price" in event_data:
            comp.registration_cost = event_data[event_data.index("Price") + 1]
            

        # Location
        full_address = soup.find('div', {'class': 'well well-sm'}).get_text().strip().split("\n")
        comp.address = full_address[0].strip() + " " + full_address[1].strip()
        comp.city_state = full_address[2][:-1].strip() + " " + full_address[3].strip()
        comp.zip = full_address[4].strip()

def scrape_google_flights(comp:Competition):
    SOURCE = "ANC"

    # Scrapes Google Flights for round-trip JFK to IST, leave July 15, 2023, return July 25, 2023.
    print(comp.date_start, comp.date_end)
    result = Scrape(SOURCE, "SEA", comp.date_start, comp.date_end)

    # Obtain data + info
    flights = result.data # outputs as a Pandas dataframe
    print(flights)

def scrape_robot_events_page() -> [Competition]:
    URL = "https://www.robotevents.com/robot-competitions/college-competition?from_date=2023-11-13&country_id=244&page=2"

    competitions = []
    response = requests.get(URL)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            link = link.get('href')
            if link and "RE-VEXU" in link:
                link += "#general-info"
                comp = Competition(link)
                competitions.append(comp)
                scrape_robot_events_competition_page(comp)
                #scrape_google_flights(comp)
    else:
        print("Bad Response")
                

    return competitions

def to_csv(competitions:[Competition]) -> None:
    file_name = "Competitions.csv"
    if len(competitions) >= 1:
        print(competitions)
        # Write heading
        heading = ""
        for attribute in competitions[0].get_attributes():
            heading += str(attribute) + ","
        heading += "\n"
        with open(file_name, 'w') as file:
            file.write(heading)

        
        # Write information
        
        for comp in competitions:
            line = ""
            for _, value in comp.get_attributes().items():
                line += str(value) + ","
            line += "\n"
            with open(file_name, 'a') as file:
                file.write(line)
    else:
        print("No Competitions Could be found")

if __name__ == "__main__":
    comps = scrape_robot_events_page()
    to_csv(comps)