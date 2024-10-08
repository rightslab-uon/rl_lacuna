def format_string(string):
    string = string.replace('_', ' ')
    string = string.title()
    return string


def get_units(pollutant: str):
    if pollutant == 'pm_25' or pollutant == 'pm_10' or pollutant == 'no2':
        return 'μm/m³'
    elif pollutant == 'co':
        return 'mg/m³'
    elif pollutant == 'temp':
        return '°C'
    elif pollutant == 'rh':
        return '%'
    else:
        return ''


def get_who_air_quality_guideline(pollutant: str):
    if pollutant == 'pm_25':
        return 15
    elif pollutant == 'pm_10':
        return 45
    elif pollutant == 'no2':
        return 25
    elif pollutant == 'co':
        return 4
    else:
        return 0


def get_pollutant_name(pollutant: str):
    if pollutant == 'pm_25':
        return 'pm 2.5'
    elif pollutant == 'pm_10':
        return 'pm 10'
    elif pollutant == 'no2':
        return 'NO\u2082'
    elif pollutant == 'temp':
        return 'Temp'
    elif pollutant == 'rh' or pollutant == 'co':
        return pollutant.upper()
    elif pollutant == 'Pollutant':
        return 'Site'
    else:
        return capitalise_first_letter(pollutant)


def capitalise_first_letter(string_to_capitalise_start: str):
    if string_to_capitalise_start and not string_to_capitalise_start[0].isupper():
        return string_to_capitalise_start[0].upper() + string_to_capitalise_start[1:]
    return string_to_capitalise_start
