#libreria propio python
import time
import os
from pynput.keyboard import Key, Controller

#permite esperar a que cargue la página antes de empezar
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Locales
from tasks.ReadCSV import ReadCSV
from classes.Errors import errors, process

URL = "https://www.fotocasa.es/es/crear-anuncio/"
DRIVER = R"C:\Users\rastr\Documents\RPA\Apartment-fotocasa\driver\chromedriver.exe"

#maps
EFICIENCIA = { "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7 }
TIPO_VIVIENDA = { "piso": 1, "apartamento": 2, "chalet": 3, "atico": 4, "estudio": 5, "casa": 6}
ORIENTACION = { "Norte": 1, "Noroeste": 2, "Noreste": 3, "Sur": 4, "Sureste": 5, "Suroeste": 6, "Este": 7, "Oeste": 8}
ESTADO_INMUEBLE = { "Casi nuevo": 1, "Muy bien": 2, "Bien": 3, "A reformar": 4, "Reformado": 5}
ANTIGUEDAD = { "Menos 1 anyo": 1, "1 a 5 anyos": 2, "5 a 10 anyos": 3, "10 a 20 anyos": 4, "20 a 30 anyos": 5, "30 a 50 anyos": 6, "50 a 70 anyos": 7, "70 a 100 anyos": 8, "+100 anyos": 9}

class CompleteForm:

    def __init__(self): 
        self.csv = ReadCSV()
        self.errors = []
        self.proc = 0

    def load_data(self):
        return self.csv.ReadData()

    def load_login(self):
        return self.csv.ReadLogin()

    def run(self):
        try:
            data = self.load_data()
            user = self.load_login()
            for i in range (0, len(data)):
                driver = self.load_web()
                self.login(user, driver)
                self.completeForm(data[i], driver)
                self.proc = self.proc + 1
        except Exception as e: 
            errors.append(f"Error al intentar ejecutar la sesion. Se han insertado {self.proc} anuncios")
            print(f"Error al ejecutar la sesion: {e}")
        finally: 
            process.append(self.proc)
            time.sleep(3)
            driver.close()
                
    def login(self, user, driver):
        #login
        try:

            #Resolvemos cookies
            self.click('/html/body/div[2]/div/div/div/div/div/footer/div/button[2]', driver)

            #input email
            self.sendInput('/html/body/div[2]/div/section/article/form/div[2]/div/div/div/div[2]/div/form/div[1]/div[1]/input', user.email, driver)

            #input password
            self.sendInput('/html/body/div[2]/div/section/article/form/div[2]/div/div/div/div[2]/div/form/div[1]/div[2]/input', user.password, driver)

            #button login
            self.click('/html/body/div[2]/div/section/article/form/div[2]/div/div/div/div[2]/div/form/div[1]/div[4]/input', driver)

            time.sleep(1)
            return True
        except Exception as e: 
            errors.append(f"Error al leer el archivo CSV. Compruebe no dejar ninguna columna vacia.")
            print(f"Error: {e}")
            return False

    def load_web(self):
        try: 
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--allow-cookies')

            driver = webdriver.Chrome(DRIVER, chrome_options=options)

            driver.get(URL)
        except Exception as e:
            errors.append(f"Error ejecutando chrome")
            print(f"Error: {e}")
            return False
        return driver

    def dropDowns(self, xpath, max, driver):
        time.sleep(0.5)
        self.click(xpath, driver)
        
        keyboard = Controller()
        for i in range(0, max): 
            time.sleep(0.25)
            keyboard.press(Key.down)
        
        time.sleep(0.5)
        keyboard.press(Key.enter)

    def uploadImages(self, driver, images_path):
        images = []
        if(images_path != ''): 
            #Se lista todo lo que contiene la carpeta images:path
            contenido = os.listdir(images_path)
            
            #Se comprueba que en la carpeta haya imagenes que sean de tipo jpeg o png
            for fichero in contenido:
                if os.path.isfile(os.path.join(images_path, fichero)) and fichero.endswith('.jpeg') or fichero.endswith('.png'):
                    images.append(fichero)

            #Se suben las imágenes buscando por input de tipo file 
            for i in range(0, len(images)):
                print(images_path + "\\" + images[i])
                img_upload = driver.find_elements_by_xpath("//input[@type='file']")
                img_upload[0].send_keys(images_path + "\\" + images[i])
                img_upload.clear()
                time.sleep(10)

    def click(self, xpath, driver):
        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.XPATH, xpath)))\
            .click()

        time.sleep(0.5)

    def sendInput(self, xpath, data, driver):
        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.XPATH, xpath)))\
            .send_keys(data)

        time.sleep(0.5)
    
    def buttonRange(self, xpath, max, driver):
        if(int(max) != 1):
            for i in range(1, int(max)):
                WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.XPATH, xpath)))\
                .click()

    def viviendas(self, data, driver):
        try:
            #superficie
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[2]/div/div[2]/div/input', data.superficie, driver)

            #habitaciones
            self.buttonRange('/html/body/div[2]/div/section/article/form/div[1]/div[1]/div/div/div[2]/div/button[2]', data.habitaciones, driver)
        
            #banyos
            self.buttonRange('/html/body/div[2]/div/section/article/form/div[1]/div[2]/div/div/div[2]/div/button[2]', data.banyos, driver)

            #orientacion
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[3]/div/div[2]/div/div/input',\
                           ORIENTACION.get(data.orientacion), driver)

            #estado_inmueble
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[4]/div/div[2]/div/div/input',\
                           ESTADO_INMUEBLE.get(data.estado_inmueble), driver)
            
            #antiguedad
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[5]/div/div[2]/div/div/input',\
                           ANTIGUEDAD.get(data.antiguedad), driver)

            #direccion
            direccion = data.calle + ', ' + data.localidad
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/input', direccion, driver)
            self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[2]/button', driver)

            #descripcion
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[5]/div/div/div/div/textarea', data.descripcion, driver)

            driver.execute_script("window.scrollTo(0, 1450)")

            #extras
            if(data.ascensor == 'TRUE'): 
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[9]/div/div/div/div/div/span[5]/span', driver)

            if(data.jardin == 'TRUE'): 
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[8]/div/div/div/div/div/span[2]/span', driver)

            if(data.amueblado == 'TRUE'): 
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[7]/div/div/div/div/div/span[2]/span', driver)
            
            if(data.terraza == 'TRUE'): 
                self.click('//html/body/div[1]/div/section/article/form/div[1]/fieldset[8]/div/div/div/div/div/span[5]/span', driver)

            #habitaclia
            if(data.habitaclia == "FALSE"):
                self.click('/html/body/div[2]/div/section/article/form/div[1]/div[6]/div/div/button/div[1]', driver)
            
            #eficiencia
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[2]/div/div/div/div/input', 1, driver)
            time.sleep(2)
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[3]/div/div[2]/div/div/input',\
                EFICIENCIA.get(data.eficiencia), driver)
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[5]/div/div[2]/div/div/input',\
                EFICIENCIA.get(data.eficiencia), driver)
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[4]/div/div[2]/div/input', 0, driver)
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[6]/div/div[2]/div/input', 0, driver)

            #subir fotos
            self.uploadImages(driver, data.photos_path)

            #publicar
            self.click('/html/body/div[2]/div/section/article/form/div[3]/div/button', driver)
            time.sleep(1)
            
            return True
        except Exception as e: 
            errors.append(f"Error al intentar insertar la {self.proc + 1} vivienda")
            print(f"*Error: {e}")
            return False

    def viviendasAlquiler(self, data, driver):
        try:
            #superficie
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[4]/div/div[2]/div/input', data.superficie, driver)

            #habitaciones
            self.buttonRange('/html/body/div[2]/div/section/article/form/div[1]/div[1]/div/div/div[2]/div/button[2]', data.habitaciones, driver)
        
            #banyos
            self.buttonRange('/html/body/div[2]/div/section/article/form/div[1]/div[2]/div/div/div[2]/div/button[2]', data.banyos, driver)
            driver.execute_script("window.scrollTo(0,200)")
            #orientacion
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[3]/div/div[2]/div/div/input',\
                           ORIENTACION.get(data.orientacion), driver)

            #estado_inmueble
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[4]/div/div[2]/div/div/input',\
                           ESTADO_INMUEBLE.get(data.estado_inmueble), driver)
            
            #antiguedad
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[5]/div/div[2]/div/div/input',\
                           ANTIGUEDAD.get(data.antiguedad), driver)

            #direccion
            direccion = data.calle + ', ' + data.localidad
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/input', direccion, driver)
            self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[2]/button', driver)

            #descripcion
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[5]/div/div/div/div/textarea', data.descripcion, driver)

            driver.execute_script("window.scrollTo(0, 1850)")

            #extras
            if(data.ascensor == 'TRUE'): 
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[9]/div/div/div/div/div/span[5]/span', driver)

            if(data.jardin == 'TRUE'): 
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[8]/div/div/div/div/div/span[2]/span', driver)

            if(data.amueblado == 'TRUE'): 
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[7]/div/div/div/div/div/span[2]/span', driver)
            
            if(data.terraza == 'TRUE'): 
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[8]/div/div/div/div/div/span[5]/span', driver)

            #habitaclia
            if(data.habitaclia == "FALSE"):
                self.click('/html/body/div[2]/div/section/article/form/div[1]/div[6]/div/div/button', driver)
            
            #eficiencia
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[2]/div/div/div/div/input', 1, driver)
            time.sleep(2)
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[3]/div/div[2]/div/div/input',\
                EFICIENCIA.get(data.eficiencia), driver)
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[5]/div/div[2]/div/div/input',\
                EFICIENCIA.get(data.eficiencia), driver)
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[4]/div/div[2]/div/input', 0, driver)
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[6]/div/div[2]/div/input', 0, driver)

            #subir fotos
            self.uploadImages(driver, data.photos_path)

            #publicar
            self.click('/html/body/div[2]/div/section/article/form/div[3]/div/button', driver)
            time.sleep(1)
            
            return True
        except Exception as e: 
            errors.append(f"Error al intentar insertar la {self.proc + 1} vivienda-alquiler")
            print(f"*Error: {e}")
            return False

    def garajeAlquiler(self, data, driver):
        try:
            #superficie
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[4]/div/div[2]/div/input', data.superficie, driver)

            #direccion
            direccion = data.calle + ', ' + data.localidad
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/input', direccion, driver)
            self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[2]/button', driver)

            driver.execute_script("window.scrollTo(0, 1750)")
            #descripcion
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[5]/div/div/div/div/textarea', data.descripcion, driver)

            #habitaclia
            if(data.habitaclia == "FALSE"):
                self.click('/html/body/div[2]/div/section/article/form/div[1]/div/div/div/button/div[3]', driver)
            
            #subir fotos
            self.uploadImages(driver, data.photos_path)

            #publicar
            self.click('/html/body/div[2]/div/section/article/form/div[3]/div/button', driver)
            time.sleep(1)
            
            return True
        except Exception as e: 
            errors.append(f"Error al intentar completar al insertar el {self.proc + 1} garaje-alquiler")
            print(f"*Error: {e}")
            return False

    def garaje(self, data, driver):
        try:
            #superficie
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[2]/div/div[2]/div/input', data.superficie, driver)

            #direccion
            direccion = data.calle + ', ' + data.localidad
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/input', direccion, driver)
            self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[2]/button', driver)

            driver.execute_script("window.scrollTo(0, 1750)")
            #descripcion
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[5]/div/div/div/div/textarea', data.descripcion, driver)

            #habitaclia
            if(data.habitaclia == "FALSE"): self.click('/html/body/div[2]/div/section/article/form/div[1]/div/div/div/button', driver)
            
            #subir fotos
            self.uploadImages(driver, data.photos_path)

            #publicar
            self.click('/html/body/div[2]/div/section/article/form/div[3]/div/button', driver)
            time.sleep(1)
            
            return True
        except Exception as e: 
            errors.append(f"Error al intentar completar al insertar el {self.proc + 1} garaje")
            print(f"*Error: {e}")
            return False

    def terreno(self, data, driver):
        try:
            #precio
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[1]/div/div[2]/div/input', data.precio, driver)

            #superficie
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[2]/div/div[2]/div/input', data.superficie, driver)

            #orientacion
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[1]/div/div[2]/div/div/input',\
                           ORIENTACION.get(data.orientacion), driver)

            #direccion
            direccion = data.calle + ', ' + data.localidad
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/input', direccion, driver)
            self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[2]/button', driver)

            driver.execute_script("window.scrollTo(0, 1750)")
            #descripcion
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[5]/div/div/div/div/textarea', data.descripcion, driver)

            #habitaclia
            if(data.habitaclia == "FALSE"): self.click('/html/body/div[2]/div/section/article/form/div[1]/div[2]/div/div/button', driver)
            
            #subir fotos
            self.uploadImages(driver, data.photos_path)

            #publicar
            self.click('/html/body/div[2]/div/section/article/form/div[3]/div/button', driver)
            time.sleep(1)
            
            return True
        except Exception as e: 
            errors.append(f"Error al intentar insertar el {self.proc + 1} terreno")
            print(f"*Error: {e}")
            return False

    def local(self, data, driver):
        try:
            #superficie
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[2]/div/div[2]/div/input', data.superficie, driver)

            #orientacion
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[2]/div/div[2]/div/div/input',\
                           ORIENTACION.get(data.orientacion), driver)

            #estado_inmueble
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[3]/div/div[2]/div/div/input',\
                           ESTADO_INMUEBLE.get(data.estado_inmueble), driver)
            
            #antiguedad
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[4]/div/div[2]/div/div/input',\
                           ANTIGUEDAD.get(data.antiguedad), driver)

            #direccion
            direccion = data.calle + ', ' + data.localidad
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/input', direccion, driver)
            self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[2]/button', driver)

            #descripcion
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[5]/div/div/div/div/textarea', data.descripcion, driver)

            driver.execute_script("window.scrollTo(0, 1450)")

            #extras
            if(data.amueblado == 'TRUE'): 
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[7]/div/div/div/div/div/span[2]/span', driver)
            
            #habitaclia
            if(data.habitaclia == "FALSE"):
                self.click('/html/body/div[2]/div/section/article/form/div[1]/div[6]/div/div/button/div[1]', driver)
            
            #eficiencia
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[2]/div/div/div/div/input', 1, driver)
            time.sleep(2)
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[3]/div/div[2]/div/div/input',\
                EFICIENCIA.get(data.eficiencia), driver)
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[5]/div/div[2]/div/div/input',\
                EFICIENCIA.get(data.eficiencia), driver)
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[4]/div/div[2]/div/input', 0, driver)
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[6]/div/div[2]/div/input', 0, driver)

            #subir fotos
            self.uploadImages(driver, data.photos_path)

            #publicar
            self.click('/html/body/div[2]/div/section/article/form/div[3]/div/button', driver)
            time.sleep(1)
            
            return True
        except Exception as e: 
            errors.append(f"Error al intentar insertar el {self.proc + 1} local")
            print(f"*Error: {e}")
            return False

    def localAlquiler(self, data, driver):
        try:
            #superficie
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[4]/div/div[2]/div/input', data.superficie, driver)

            #orientacion
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[2]/div/div[2]/div/div/input',\
                           ORIENTACION.get(data.orientacion), driver)

            #estado_inmueble
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[3]/div/div[2]/div/div/input',\
                           ESTADO_INMUEBLE.get(data.estado_inmueble), driver)
            
            #antiguedad
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[4]/div/div[2]/div/div/input',\
                           ANTIGUEDAD.get(data.antiguedad), driver)

            #direccion
            direccion = data.calle + ', ' + data.localidad
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/input', direccion, driver)
            self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[2]/button', driver)

            #descripcion
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[5]/div/div/div/div/textarea', data.descripcion, driver)

            driver.execute_script("window.scrollTo(0, 1450)")

            #extras
            if(data.amueblado == 'TRUE'): 
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[7]/div/div/div/div/div/span[2]/span', driver)
            
            #habitaclia
            if(data.habitaclia == "FALSE"):
                self.click('/html/body/div[2]/div/section/article/form/div[1]/div[5]/div/div/button', driver)
            
            #eficiencia
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[2]/div/div/div/div/input', 1, driver)
            time.sleep(2)
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[3]/div/div[2]/div/div/input',\
                EFICIENCIA.get(data.eficiencia), driver)
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[5]/div/div[2]/div/div/input',\
                EFICIENCIA.get(data.eficiencia), driver)
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[4]/div/div[2]/div/input', 0, driver)
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[6]/div/div[2]/div/input', 0, driver)

            #subir fotos
            self.uploadImages(driver, data.photos_path)

            #publicar
            self.click('/html/body/div[2]/div/section/article/form/div[3]/div/button', driver)
            time.sleep(1)
            
            return True
        except Exception as e: 
            errors.append(f"Error al intentar insertar el {self.proc + 1} local")
            print(f"*Error: {e}")
            return False

    def oficina(self, data, driver):
        try:
            #superficie
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[2]/div/div[2]/div/input', data.superficie, driver)

            #orientacion
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[1]/div/div[2]/div/div/input',\
                           ORIENTACION.get(data.orientacion), driver)

            #estado_inmueble
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[2]/div/div[2]/div/div/input',\
                           ESTADO_INMUEBLE.get(data.estado_inmueble), driver)
            
            #antiguedad
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[3]/div/div[2]/div/div/input',\
                           ANTIGUEDAD.get(data.antiguedad), driver)

            #direccion
            direccion = data.calle + ', ' + data.localidad
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/input', direccion, driver)
            self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[2]/button', driver)

            #descripcion
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[5]/div/div/div/div/textarea', data.descripcion, driver)

            driver.execute_script("window.scrollTo(0, 1450)")

            #habitaclia
            if(data.habitaclia == "FALSE"): self.click('/html/body/div[2]/div/section/article/form/div[1]/div[4]/div/div/button', driver)
            
            #eficiencia
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[2]/div/div/div/div/input', 1, driver)
            time.sleep(2)
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[3]/div/div[2]/div/div/input',\
                EFICIENCIA.get(data.eficiencia), driver)
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[5]/div/div[2]/div/div/input',\
                EFICIENCIA.get(data.eficiencia), driver)
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[4]/div/div[2]/div/input', 0, driver)
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[6]/div/div[2]/div/input', 0, driver)

            #subir fotos
            self.uploadImages(driver, data.photos_path)

            #publicar
            self.click('/html/body/div[2]/div/section/article/form/div[3]/div/button', driver)
            time.sleep(1)
            
            return True
        except Exception as e: 
            errors.append(f"Error al intentar insertar la {self.proc + 1} oficina")
            print(f"*Error: {e}")
            return False

    def oficinaAlquiler(self, data, driver):
        try:
            #superficie
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[4]/div/div[2]/div/input', data.superficie, driver)

            #orientacion
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[1]/div/div[2]/div/div/input',\
                           ORIENTACION.get(data.orientacion), driver)

            #estado_inmueble
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[2]/div/div[2]/div/div/input',\
                           ESTADO_INMUEBLE.get(data.estado_inmueble), driver)
            
            #antiguedad
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/div[3]/div/div[2]/div/div/input',\
                           ANTIGUEDAD.get(data.antiguedad), driver)

            #direccion
            direccion = data.calle + ', ' + data.localidad
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/input', direccion, driver)
            self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[2]/button', driver)

            #descripcion
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[5]/div/div/div/div/textarea', data.descripcion, driver)

            driver.execute_script("window.scrollTo(0, 1450)")

            #habitaclia
            if(data.habitaclia == "FALSE"): self.click('/html/body/div[2]/div/section/article/form/div[1]/div[4]/div/div/button', driver)
            
            #eficiencia
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[2]/div/div/div/div/input', 1, driver)
            time.sleep(2)
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[3]/div/div[2]/div/div/input',\
                EFICIENCIA.get(data.eficiencia), driver)
            self.dropDowns('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[5]/div/div[2]/div/div/input',\
                EFICIENCIA.get(data.eficiencia), driver)
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[4]/div/div[2]/div/input', 0, driver)
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[6]/div/div[6]/div/div[2]/div/input', 0, driver)

            #subir fotos
            self.uploadImages(driver, data.photos_path)

            #publicar
            self.click('/html/body/div[2]/div/section/article/form/div[3]/div/button', driver)
            time.sleep(1)
            
            return True
        except Exception as e: 
            errors.append(f"Error al intentar insertar la {self.proc + 1} oficina")
            print(f"*Error: {e}")
            return False

    def trastero(self, data, driver):
        try:
            #superficie
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[2]/div/div[2]/div/input', data.superficie, driver)

            #direccion
            direccion = data.calle + ', ' + data.localidad
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/input', direccion, driver)
            self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[2]/button', driver)

            driver.execute_script("window.scrollTo(0, 1750)")
            #descripcion
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[5]/div/div/div/div/textarea', data.descripcion, driver)

            #habitaclia
            if(data.habitaclia == "FALSE"): self.click('/html/body/div[2]/div/section/article/form/div[1]/div/div/div/button', driver)
            
            #subir fotos
            self.uploadImages(driver, data.photos_path)

            #publicar
            self.click('/html/body/div[2]/div/section/article/form/div[3]/div/button', driver)
            time.sleep(1)
            
            return True
        except Exception as e: 
            errors.append(f"Error al intentar completar al insertar el {self.proc + 1} garaje")
            print(f"*Error: {e}")
            return False

    def trasteroAlquiler(self, data, driver):
        try:
            #superficie
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[4]/div/div[2]/div/input', data.superficie, driver)

            #direccion
            direccion = data.calle + ', ' + data.localidad
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[1]/div/div/input', direccion, driver)
            self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[3]/div/div[1]/div/div[1]/div/div/div[2]/button', driver)

            driver.execute_script("window.scrollTo(0, 1750)")
            #descripcion
            self.sendInput('/html/body/div[2]/div/section/article/form/div[1]/fieldset[5]/div/div/div/div/textarea', data.descripcion, driver)

            #habitaclia
            if(data.habitaclia == "FALSE"): self.click('/html/body/div[2]/div/section/article/form/div[1]/div/div/div/button', driver)
            
            #subir fotos
            self.uploadImages(driver, data.photos_path)

            #publicar
            self.click('/html/body/div[2]/div/section/article/form/div[3]/div/button', driver)
            time.sleep(1)
            
            return True
        except Exception as e: 
            errors.append(f"Error al intentar completar al insertar el {self.proc + 1} garaje")
            print(f"*Error: {e}")
            return False

    def completeForm(self, data, driver):
        try:
            if( data.tipo_vivienda == 'vivienda' ): 
                #condicion de alquiler o venta
                type = self.condicionAlquiler(data, '',driver)
                if(type): self.viviendas(data, driver)
                else: self.viviendasAlquiler(data, driver)

            if( data.tipo_vivienda == 'garaje' ): 
                #condicion de alquiler o venta
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[1]/div/div[1]/div/div[2]/label/span', driver)
                type = self.condicionAlquiler(data,'/html/body/div[2]/div/section/article/form/div[1]/fieldset[1]/div/div[2]/div/div/span/button[2]',driver)
                if(type): self.garaje(data,driver)
                else: self.garajeAlquiler(data, driver)

            if( data.tipo_vivienda == 'terreno' ): 
                #condicion de alquiler o venta
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[1]/div/div[1]/div/div[3]/label/span', driver)
                self.terreno(data, driver)

            if( data.tipo_vivienda == 'local' ): 
                #condicion de alquiler o venta
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[1]/div/div[1]/div/div[4]/label/span', driver)
                type = self.condicionAlquiler(data,'/html/body/div[2]/div/section/article/form/div[1]/fieldset[1]/div/div[2]/div/div/span/button[2]',driver)
                if(type): self.local(data,driver)
                else: self.localAlquiler(data, driver)
            
            if( data.tipo_vivienda == 'oficina' ): 
                #condicion de alquiler o venta
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[1]/div/div[1]/div/div[5]/label/span', driver)
                type = self.condicionAlquiler(data,'/html/body/div[2]/div/section/article/form/div[1]/fieldset[1]/div/div[2]/div/div/span/button[2]',driver)
                if(type): self.oficina(data,driver)
                else: self.oficinaAlquiler(data, driver)
            
            if( data.tipo_vivienda == 'trastero' ): 
                #condicion de alquiler o venta
                self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[1]/div/div[1]/div/div[6]/label/span', driver)
                type = self.condicionAlquiler(data,'/html/body/div[2]/div/section/article/form/div[1]/fieldset[1]/div/div[2]/div/div/span/button[2]',driver)
                if(type): self.trastero(data,driver)
                else: self.trasteroAlquiler(data, driver)

            return True
        except Exception as e: 
            errors.append(f"Error al intentar completar el fomulario de Fotocasa en el proceso {self.proc + 1}")
            print(f"*Error formulario fotocasa: {e}")
            return False
    
    def condicionAlquiler(self, data, xpath, driver):
        inpute = '/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[1]/div/div[2]/div/input'
        driver.execute_script("window.scrollTo(0,0)")
        if(data.accion == 'venta'):
            self.sendInput(inpute, data.precio, driver)
            return True
        else:
            self.click(xpath, driver)
            self.sendInput(inpute, data.precio, driver)
            if(data.comunidad == 'TRUE'): self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[2]/div/div/button/div[3]', driver)
            if(data.fianza == 'TRUE'): self.click('/html/body/div[2]/div/section/article/form/div[1]/fieldset[2]/div/div[3]/div/div/button/div[1]', driver)
            return False

    

