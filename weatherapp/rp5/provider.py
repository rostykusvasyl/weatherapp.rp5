""" Weather provider.
"""

from bs4 import BeautifulSoup

from weatherapp.rp5 import config
from weatherapp.core.abstract import WeatherProvider


class Rp5Provider(WeatherProvider):
    """ Weather provider for rp5.ua site.
    """

    name = config.RP5_PROVIDER_NAME
    title = config.RP5_PROVIDER_TITLE

    def get_default_location(self):
        """ Default location name.
        """
        return config.DEFAULT_RP5_LOCATION_NAME

    def get_default_url(self):
        """ Default location url.
        """
        return config.DEFAULT_RP5_LOCATION_URL

    def get_name(self):
        """ Get name provider
        """
        return self.name

    def get_locations_region(self, locations_url):
        """ Choosing a place for which you need to get weather information.
        """

        soup = BeautifulSoup(
            self.get_page_source(locations_url), 'html.parser')
        locations = []
        for location in soup.find_all("h3"):
            url = 'http://rp5.ua/' +\
                location.find("a", class_="href20").get('href')
            location = location.find("a", class_="href20").get_text()
            locations.append((location, url))
        return locations

    def configurate(self):
        """ The user chooses the city for which he wants to get the weather.
        """

        # Find country
        soup = BeautifulSoup(
            self.get_page_source(config.RP5_BROWSE_LOCATIONS), 'html.parser')
        country_link = soup.find_all(class_="country_map_links")
        list_country = []
        for link in country_link:
            url = link.find(["a", "span"]).get('href')
            link = link.find(["a", "span"]).get_text()
            list_country.append((link, url))
        for index_country, location in enumerate(list_country):
            print("{}. {}".format((index_country + 1), (location[0])))
        while True:
            try:
                index_country = \
                    int(input('Please select country location: '))
                if index_country > 0:
                    link_country = list_country[index_country - 1]
                    break
            except ValueError:
                print("That was no valid number. Try again...")
            except IndexError:
                print("This number out of range. Try again...")

        country_url = 'http://rp5.ua' + link_country[1]

        # Find region
        locations = self.get_locations_region(country_url)
        for index_region, location in enumerate(locations):
            print("{}. {}".format((index_region + 1), (location[0])))
        while True:
            try:
                index_region = int(input('Please select location region: '))
                if index_region > 0:
                    region = locations[index_region - 1]
                    break
            except ValueError:
                print("That was no valid number. Try again...")
            except IndexError:
                print("This number out of range. Try again...")

        region_url = region[1]

        # Find city
        city_location = \
            BeautifulSoup(self.get_page_source(region_url), 'html.parser')
        list_city = []
        ob_popular_links = city_location.find_all("h3")
        city_link = city_location.find_all(class_="city_link")
        if ob_popular_links:
            for location in ob_popular_links:
                url = 'http://rp5.ua/' + \
                    location.find(class_="href20").get('href')
                location = location.find(class_="href20").get_text()
                list_city.append((location, url))
            for index_city, location in enumerate(list_city):
                print("{}. {}".format((index_city + 1), (location[0])))
            while True:
                try:
                    index_city = int(input('Please select city: '))
                    if index_city > 0:
                        city = list_city[index_city - 1]
                        break
                except ValueError:
                    print("That was no valid number. Try again...")
                except IndexError:
                    print("This number out of range. Try again...")

            self.save_configuration(*city)
        elif city_link:
            for location in city_link:
                url = 'http://rp5.ua/' + location.find("a").get('href')
                location = location.find("a").get_text()
                list_city.append((location, url))
            for index_city, location in enumerate(list_city):
                print("{}. {}".format((index_city + 1), (location[0])))
            while True:
                try:
                    index_city = int(input('Please select city: '))
                    if index_city > 0:
                        city = list_city[index_city - 1]
                        break
                except ValueError:
                    print("That was no valid number. Try again...")
                except IndexError:
                    print("This number out of range. Try again...")

            self.save_configuration(*city)
        else:
            self.save_configuration(*region)

    @staticmethod
    def get_weather_info(page):
        """ The function returns a list with the value the state of the weather.
        """

        # create a blank dictionary to enter the weather data
        weather_info = {}
        soup = BeautifulSoup(page, 'html.parser')
        tag_container = soup.find(id="archiveString")
        if tag_container:
            forecast_temp = tag_container.find(id="ArchTemp")
            if forecast_temp:
                temp_info = forecast_temp.find(class_="t_0").get_text()
                weather_info['temp'] = temp_info

            forecast_realfeel = tag_container.find(class_="TempStr")
            if forecast_realfeel:
                realfeel = forecast_realfeel.find(class_="t_0").get_text()
                weather_info['feels_like'] = realfeel

        forecast_string = soup.find(id="forecastShort-content").get_text()
        if forecast_string:
            lst_forecast = forecast_string.split(',')
            cond = lst_forecast[2].strip()
            weather_info['cond'] = cond
        forecast_wind = soup.find(class_="ArchiveInfo").get_text()
        if forecast_wind:
            lst_forecast = forecast_wind.split(',')
            wind = lst_forecast[-2].strip()[:lst_forecast[-2].find(')') + 1] +\
                lst_forecast[-1].strip()
            weather_info['wind'] = wind
        return weather_info

