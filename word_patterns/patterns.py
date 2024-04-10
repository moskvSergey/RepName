from datetime import datetime
import locale
from docxtpl import DocxTemplate

locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')
def create_waybill(data):
    template = DocxTemplate("word_patterns/PL-1.docx")
    context = data
    template.render(context)
    save_path = f'путевые листы/{data["ds"]} {data["fio"]}.docx'
    template.save(save_path)

def convert_bd(shift, driver, car):
    date_started = shift.date_started
    date_ended = shift.date_started
    formatted_date_1 = date_started.strftime('%d %B %Y')
    formatted_date_2 = date_ended.strftime('%d %B %Y')
    driver_full = driver.last_name + " " + driver.first_name + " " + driver.surname
    license_date = driver.license_date
    formatted_date_3 = license_date.strftime('%d.%m.%Y')
    formattet_d = date_started.strftime('%d')
    formattet_m = date_started.strftime('%b')
    formattet_ds = date_started.strftime('%d.%m')
    formattet_hs = date_started.strftime('%H:%M')
    fio = driver.last_name + " " + str(driver.first_name)[0]+'.'+str(driver.surname)[0]
    shift = {
        'id': shift.id,
        'date_started': formatted_date_1,
        'date_ended': formatted_date_2,
        'car_model': car.model,
        'car_plate': car.plate,
        'driver': driver_full,
        'tabel': driver.tabel,
        'snils': driver.snils,
        'license_n': driver.license_number,
        'license_d': formatted_date_3,
        'd':formattet_d,
        'm':formattet_m,
        'ds':formattet_ds,
        'hs': formattet_hs,
        'odometer': shift.odometer,
        'diesel': shift.diesel,
        'fio': fio
    }
    return shift

def download_pl(shift, driver, car):
    shift = convert_bd(shift, driver, car)
    create_waybill(shift)