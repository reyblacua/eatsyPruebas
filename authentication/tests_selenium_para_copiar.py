from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from authentication.models import User, Perfil

class SeleniumTests(StaticLiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        self.driver.set_window_size(1920, 1080)
        super().setUp()
        call_command('flush', interactive=False)
        call_command("loaddata", "datosEjemplo.json", verbosity=0)

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        call_command('flush', interactive=False)

    def test_registro_e_inicio_correcto(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(960, 810)
        self.driver.find_element(By.LINK_TEXT, "Registrarse").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("user1")
        self.driver.find_element(By.ID, "id_nombre").send_keys("user1")
        self.driver.find_element(By.ID, "id_apellidos").click()
        self.driver.find_element(By.ID, "id_apellidos").send_keys("user1")
        self.driver.find_element(By.ID, "id_email").click()
        self.driver.find_element(By.ID, "id_email").send_keys("user1@example.com")
        dropdown = self.driver.find_element(By.ID, "id_dieta")
        dropdown.find_element(By.XPATH, "//option[. = 'Vegano']").click()
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.ID, "id_v_password").click()
        self.driver.find_element(By.ID, "id_v_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "id_username")))
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("user1")
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "id_nombre")))
        self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(2) > .col").click()
        value = self.driver.find_element(By.ID, "id_nombre").get_attribute("value")
        assert value == "user1"
    
    def test_registro_sin_privacidad(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(960, 810)
        self.driver.find_element(By.LINK_TEXT, "Registrarse").click()
        self.driver.find_element(By.ID, "id_username").send_keys("user2")
        self.driver.find_element(By.ID, "id_nombre").send_keys("user2")
        self.driver.find_element(By.ID, "id_apellidos").send_keys("user2")
        self.driver.find_element(By.ID, "id_email").send_keys("user2@example.com")
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        dropdown = self.driver.find_element(By.ID, "id_dieta")
        dropdown.find_element(By.XPATH, "//option[. = 'Vegano']").click()
        self.driver.find_element(By.ID, "id_v_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".nombreProducto").text == "Registro de usuario"

    def test_inicio_con_mala_contra(self):
        self.driver.get(f'{self.live_server_url}/authentication/login')
        self.driver.set_window_size(960, 810)
        self.driver.find_element(By.ID, "id_username").send_keys("user1")
        self.driver.find_element(By.ID, "id_password").send_keys("nocontra")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(4) div:nth-child(2)").text == "* Inicio de sesión incorrecto"


    def test_entrar_perfil(self):
        self.driver.get(f'{self.live_server_url}/authentication/login')
        self.driver.set_window_size(960, 810)
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/authentication/profile')
        assert self.driver.find_element(By.XPATH, "//h2[contains(.,\'Mi Perfil\')]").text == "Mi Perfil"

    def test_modificar_perfil(self):
        self.driver.get(f'{self.live_server_url}/authentication/login')
        self.driver.set_window_size(960, 810)
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/authentication/profile')
        self.driver.find_element(By.ID, "id_nombre").send_keys("CambioNombre")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()

        value = self.driver.find_element(By.ID, "id_nombre").get_attribute("value")
        assert value == "KeefeCambioNombre"

    def test_modificar_perfil_con_fallo(self):
        self.driver.get(f'{self.live_server_url}/authentication/login')
        self.driver.set_window_size(960, 810)
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/authentication/profile')
        self.driver.find_element(By.ID, "id_nombre").send_keys(Keys.DELETE)
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/authentication/profile')
        value = self.driver.find_element(By.ID, "id_nombre").get_attribute("value")
        assert value == "Keefe"

    def test_cancelar_suscripcion(self):
        self.driver.get(f'{self.live_server_url}/authentication/login')
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        p = Perfil.objects.filter(user=User.objects.filter(username="Usuario1").first()).first()
        if(p.activeAccount == False):
            p.activeAccount = True
            p.save()
        self.driver.implicitly_wait(10)
        self.driver.get(f'{self.live_server_url}/authentication/profile')
        self.driver.find_element(By.ID, "cancelButton").click()
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.LINK_TEXT, "Activa tu cuenta")))
        assert self.driver.find_element(By.LINK_TEXT, "Activa tu cuenta").text == "Activa tu cuenta"