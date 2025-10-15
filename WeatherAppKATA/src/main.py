import requests
from tabulate import tabulate

def user_inputs_coordinates(num):
    inputs = []

    for i in range(num):
        print("\nLocation #" + str(i + 1) + " coordinates:")
        while True:
            lat = input("Enter latitude: ")
            lon = input("Enter longitude: ")
            try:
                lat = float(lat)
                lon = float(lon)
                if -90.0 <= lat <= 90.0 and -180 <= lon <= 180:
                    inputs.append([lat, lon])
                    break
                else:
                    print("Please enter valid coordinates.")
            except(ValueError, TypeError):
                print("Please enter valid coordinates.")
    return inputs

def user_inputs_location(num):
    inputs = []

    for i in range(num):
        print("\nLocation #" + str(i + 1) + ": ")
        while True:
            state_code = None
            country_code = "," + str(input("Enter country code (please use ISO 3166 country codes): "))

            if country_code == ",581":
                state_code = "," + str(input("Enter US state code: ")).lower()

            city = str(input("Enter city name: ")).lower()
            response = requests.get("https://api.openweathermap.org/geo/1.0/direct?q=" + city + state_code + country_code + "&limit=1&appid=0ccbf19d4c06506bc78bdc8cfb0165db")

            if response.ok:
                lat = response.json()[0]['lat']
                lon = response.json()[0]['lon']
                inputs.append([lat, lon, city])
                break

            else:
                print("Your entered location was not found. Please enter valid location information.")
    print("inputs:", inputs)
    return inputs

def api_call(inputs, table):
    raw_data = []
    for i in range(len(inputs)):
        lat = inputs[i][0]
        lon = inputs[i][1]
        response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(
            lon) + "&appid=0ccbf19d4c06506bc78bdc8cfb0165db")

        weather_data = {
            0: f"{((response.json()['main']['temp'] - 273.25) * 1.8) + 32:.2f}",

            1: f"{((response.json()['main']['feels_like'] - 273.25) * 1.8) + 32:.2f}",

            2: response.json()['weather'][0]['description'],

            3: f"{response.json()['wind']['speed'] * 2.23694:.2f}",

            4: f"{response.json()['main']['humidity']:.2f}",

            5: f"{response.json()['main']['pressure'] * 0.02953:.2f}",
        }
        raw_data.append(weather_data)

    for k in range(len(inputs)):
        if len(inputs[0]) == 2:
            table.append(["Location #" + str(k + 1)])
        elif len(inputs[0]) == 3:
            table.append([inputs[k][2].title()])
        for j in range(6):
            table[k + 1].append(raw_data[k][j])

    table_data = tabulate(table, headers="firstrow", tablefmt="fancy_grid")

    return table_data

def main():
    # Takes the number of locations the user would like to compare,
    # and prevents them from giving invalid inputs
    while True:
        num = input("How many locations would you like to compare? ")
        try:
            num = int(num)
            if int(num) < 0:
                print("Please enter a valid response.")
            elif int(num) > 10:
                print("Please enter a valid integer less than 10.")
            else:
                break
        except(ValueError, TypeError):
            print("Please enter a valid response.")

    # Takes the
    while True:
        choice = str(input('Enter "coordinates" to search weather data using coordinates, or "location" to search using location: '))
        if choice.lower() == "coordinates":
            inputs = user_inputs_coordinates(num)
            break
        elif choice.lower() == "location":
            inputs = user_inputs_location(num)
            break
        else:
            print("Please enter a valid input.")

    table = [["Temperature", "Feels Like", "Clouds", "Wind Speed", "Humidity", "Pressure"]]
    print(api_call(inputs, table))

if __name__ == "__main__":
    main()


