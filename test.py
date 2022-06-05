from selenium import webdriver
#permite esperar a que cargue la página antes de empezar
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

DRIVER = "C://Users//rastr//Documents//RPA//Apartment-fotocasa//driver"

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-web-security')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--allow-cookies')

driver = webdriver.Chrome(executable_path=DRIVER)

driver.get('https://www.fotocasa.es/es/crear-anuncio/')