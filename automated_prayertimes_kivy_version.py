from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from bs4 import BeautifulSoup
import requests
from datetime import timedelta


class PrayerTimeApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Fetching prayer times from website
        url = 'https://www.islamicfinder.org/world/egypt/360630/cairo-prayer-times/'
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')
        mydivs = soup.find_all("span", {"class": "prayertime"})
        prayerNames = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
        prayerTimes = [i.text for i in mydivs]
        matched = list(zip(prayerNames, prayerTimes))

        # Displaying prayer times
        for prayer in matched:
            layout.add_widget(Label(text=f'{prayer[0]}: {prayer[1]}'))

        # Time calculations
        li2 = [prayer.split(' ')[0] for _, prayer in matched]
        fajr = li2[0]
        maghrib = li2[4]

        maghrib_split = maghrib.split(':')
        fajr_split = fajr.split(':')

        maghrib_hour = int(maghrib_split[0])
        maghrib_min = int(maghrib_split[1])

        fajr_hour = int(fajr_split[0]) + 24
        fajr_min = int(fajr_split[1])

        t1 = timedelta(hours=(maghrib_hour + 12), minutes=maghrib_min)
        t2 = timedelta(hours=fajr_hour, minutes=fajr_min)
        t3 = timedelta(hours=24)

        difference = t2 - t1
        half = difference / 2
        third = difference / 3

        first_third = t1 + (third * 1)
        second_third = (t1 + (third * 2)) - t3
        last_third = t1 + (third * 3) - t3

        midnight = (t1 + half) - t3

        layout.add_widget(Label(text='**************************************************'))
        layout.add_widget(Label(text='Midnight'))
        layout.add_widget(Label(text= str(midnight)))
        layout.add_widget(Label(text='First Third'))
        layout.add_widget(Label(text=f'{t1} to {first_third}'))
        layout.add_widget(Label(text='Second Third'))
        layout.add_widget(Label(text=f'{first_third} to {second_third}'))
        layout.add_widget(Label(text='Last Third'))
        layout.add_widget(Label(text=f'{second_third} to {last_third}'))

        return layout


if __name__ == '__main__':
    PrayerTimeApp().run()
