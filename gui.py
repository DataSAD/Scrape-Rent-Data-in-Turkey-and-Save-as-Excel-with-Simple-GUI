from tkinter import *
from tkinter import filedialog
import requests
import lxml
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import openpyxl
from tkinter import messagebox

root = Tk()
root.title('Scrape Rentals')
root.geometry('420x180')


file_location = ''


def locate_file():
    global file_location
    file_location = filedialog.askdirectory()
    print(file_location)


def last_act():
    if enter_city.get() != '' and enter_district.get() != '' and file_location != '':

        global city
        global district
        city = ''
        district = ''
        for letter in enter_city.get().lower().strip().replace(' ', ''):
            if letter == 'ı':
                city += 'i'
            elif letter == 'ğ':
                city += 'g'
            elif letter == 'ü':
                city += 'u'
            elif letter == 'ş':
                city += 's'
            elif letter == 'ö':
                city += 'o'
            elif letter == 'ç':
                city += 'c'
            else:
                city += letter
        print(f'city = {city}')

        for letter in enter_district.get().lower().strip().replace(' ', ''):
            if letter == 'ı':
                district += 'i'
            elif letter == 'ğ':
                district += 'g'
            elif letter == 'ü':
                district += 'u'
            elif letter == 'ş':
                district += 's'
            elif letter == 'ö':
                district += 'o'
            elif letter == 'ç':
                district += 'c'
            else:
                district += letter

        print(f'district = {district}')



        last_page = False
        page_no = 1

        my_dict = {'city': [], 'district': [], 'rent': [], 'rooms': [], 'm2': [], 'neighbourhood': []}

        while True:

            if last_page:
                break

            if city == 'all' and district == 'turkiye':
                url = 'https://www.emlakjet.com/kiralik-konut/'
            else:
                url = 'https://www.emlakjet.com/kiralik-konut/{}-{}/{}/'.format(city, district, page_no)

            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'lxml')

            if not soup.find('li', class_='_3au2n_ OTUgAO') or page_no == 50:
                last_page = True

            houses = soup.find_all('div', class_='_3qUI9q')

            for house in houses:

                if house.find('div', class_='_2UELHn').find_all('span')[1].text[7:] is not None:
                    rooms = house.find('div', class_='_2UELHn').find_all('span')[1].text[7:]
                else:
                    rooms = 'No Info'

                if house.find('div', class_='_2UELHn').find_all('span')[3].text[7:] is not None:
                    m2 = house.find('div', class_='_2UELHn').find_all('span')[3].text[7:]
                else:
                    m2 = 'No Info'

                if house.find('p', class_='_2C5UCT').span.text is not None:
                    rent = house.find('p', class_='_2C5UCT').span.text
                else:
                    rent = 'No Info'

                if city == 'all' and district == 'turkiye':
                    if house.find('div', class_='_2wVG12').text.split('-')[0].strip() is not None:
                        city_y = house.find('div', class_='_2wVG12').text.split('-')[0].strip()
                        district_y = house.find('div', class_='_2wVG12').text.split('-')[1].strip()

                    else:
                        city_y = 'No Info'
                        district_y = 'No Info'
                    my_dict['city'].append(city_y)
                    my_dict['district'].append(district_y)

                else:
                    my_dict['city'].append(city)
                    my_dict['district'].append(district)

                if house.find('div', class_='_2wVG12').text.split('-')[-1].strip() is not None:
                    neighbourhood = house.find('div', class_='_2wVG12').text.split('-')[-1].strip()
                else:
                    neighbourhood = 'No Info'

                my_dict['rooms'].append(rooms)
                my_dict['m2'].append(m2)
                my_dict['rent'].append(rent)
                my_dict['neighbourhood'].append(neighbourhood)

            page_no += 1

        df = pd.DataFrame(my_dict)
        formatted_file_location = file_location.replace('/', "\\")
        print(f'file loc = {formatted_file_location}')
        df.to_excel(f'{formatted_file_location}\\{city},{district}_rents.xlsx')
    else:
        messagebox.showwarning('Error', 'Please give all the info!')


label_city = Label(root, text='Enter city')
label_city.grid(row=1, column=1, sticky='w')

enter_city = Entry(root, width=30)
enter_city.grid(row=1, column=2, pady=20)

label_district = Label(root, text='Enter district')
label_district.grid(row=2, column=1, sticky='w')

enter_district = Entry(root, width=30)
enter_district.grid(row=2, column=2)

label_location = Label(root, text='File location')
label_location.grid(row=3, column=1, sticky='w')

button_location = Button(root, text='Select location to save Excel file', width=25, command=locate_file)
button_location.grid(row=3, column=2, pady=20)

button_final = Button(root, text='BRING RENTS', width=15, height=8, command=last_act)
button_final.grid(row=1, column=3, rowspan=3, padx=20, pady=20)




root.mainloop()
