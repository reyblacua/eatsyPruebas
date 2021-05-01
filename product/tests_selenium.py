from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium import webdriver
from selenium.webdriver.common.by import By

class SeleniumTests(StaticLiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1920, 1080)
        super().setUp()
        call_command("flush", interactive=False)
        call_command("loaddata", "datosEjemplo.json")

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        call_command("flush", interactive=False)

    def iniciar_sesion(self,username,password):
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(username)
        self.driver.find_element(By.ID, "id_password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()

    # def test_noactivo(self):
    #     self.driver.get(f'{self.live_server_url}/')
    #     elements = self.driver.find_elements(By.LINK_TEXT, "Iniciar sesión")
    #     assert len(elements) > 0
    #     elements = self.driver.find_elements(By.LINK_TEXT, "Registrarse")
    #     assert len(elements) > 0
    #     self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_username").send_keys("Usuario3")
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario3PasswordJQSA!")
    #     self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario3PasswordJQSA!=")
    #     self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #     elements = self.driver.find_elements(By.LINK_TEXT, "Activa tu cuenta")
    #     elements = self.driver.find_elements(By.CSS_SELECTOR, ".save")
    #     assert len(elements) > 0
    #     elements = self.driver.find_elements(By.CSS_SELECTOR, ".col-auto > .btn:nth-child(2)")
    #     assert len(elements) > 0
    #     self.driver.get(f'{self.live_server_url}/product/list')
    #     elements = self.driver.find_elements(By.CSS_SELECTOR, ".mt-3")
        
    # def test_activ(self):
    #     self.driver.get(f'{self.live_server_url}/')
    #     self.driver.set_window_size(1080, 1036)
    #     self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_username").send_keys("Usuario2")
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario2PasswordJQSA!=")
    #     self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #     self.driver.get(f'{self.live_server_url}/product/list')
    #     assert self.driver.find_element(By.CSS_SELECTOR, ".col-sm-8").text == "Búsqueda de productos"

    def test_restriccionesadmin(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario2")
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario2PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/product/list')
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".padding-list:nth-child(4) .w-100")
        assert len(elements) == 0
        self.driver.get(f'{self.live_server_url}/product/report/list')
        text = self.driver.find_element(By.CSS_SELECTOR, ".col").text
        assert text != "Notificaciones de productos reportados"
        self.driver.get(f'{self.live_server_url}/product/show/55')
        elements = self.driver.find_elements(By.LINK_TEXT, "Editar")
        assert len(elements) == 0

    def test_admineditarproducto(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyAdminPasswordJQSA!=1")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/product/review/55')
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".save")
        assert len(elements) > 0

    # def test_addubi(self):
    #     self.driver.get(f'{self.live_server_url}/')
    #     self.driver.set_window_size(1080, 1036)
    #     self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_username").send_keys("Usuario2")
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario2PasswordJQSA!=")
    #     self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #     self.driver.get(f'{self.live_server_url}/product/show/55')
    #     self.driver.find_element(By.XPATH, "//div[@id=\'collapseproducts\']/div[3]/span").click()
    #     self.driver.find_element(By.ID, "addUbicacion").click()
    #     self.driver.find_element(By.ID, "id_ubicaciones").click()
    #     dropdown = self.driver.find_element(By.ID, "id_ubicaciones")
    #     dropdown.find_element(By.XPATH, "//option[. = 'Lidl']").click()
    #     self.driver.find_element(By.ID, "id_ubicaciones").click()
    #     self.driver.find_element(By.ID, "id_precio").click()
    #     self.driver.find_element(By.ID, "id_precio").send_keys("2")
    #     self.driver.find_element(By.NAME, "addingUbication").click()
    #     self.driver.find_element(By.CSS_SELECTOR, ".col-sm-4:nth-child(3) > .m-auto").click()
    #     self.driver.find_element(By.ID, "select").click()
    #     dropdown = self.driver.find_element(By.ID, "select")
    #     dropdown.find_element(By.XPATH, "//option[. = 'Lidl']").click()

    #   TODO test que falla para arreglar
    # def test_reportar(self):
    #     self.driver.get(f'{self.live_server_url}/')
    #     self.driver.set_window_size(1080, 1036)
    #     self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_username").send_keys("Usuario2")
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario2PasswordJQSA!=")
    #     self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #     self.driver.get(f'{self.live_server_url}/product/show/55')
    #     elements = self.driver.find_elements(By.CSS_SELECTOR, ".mb-5 > .col-auto > .btn")
    #     assert len(elements) > 0
    #     self.driver.find_element(By.CSS_SELECTOR, ".mb-5 > .col-auto > .btn").click()
    #     elements = self.driver.find_elements(By.NAME, "reportButton")

    #def test_selenium_paginacion(self):
    #    self.driver.get(f'{self.live_server_url}/')
    #    self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #    self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #    self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
    #    self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #    self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
    #    self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #    self.driver.find_element(By.CSS_SELECTOR, ".col-xl-3:nth-child(12) .descripcion").click()
    #    self.driver.find_element(By.ID, "pglink2").click()
    #    self.driver.find_element(By.CSS_SELECTOR, ".col-xl-3:nth-child(12) > .product-card-inner").click()

    #def test_selenium_create_product(self):
    #    self.driver.get(f'{self.live_server_url}/')
    #    self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #    self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
    #    self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
    #    self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #    self.driver.find_element(By.CSS_SELECTOR, ".botonAdd > img").click()
    #    #self.driver.find_element(By.ID, "id_foto").send_keys("\leche.jpg")
    #    self.driver.find_element(By.ID, "id_nombre").send_keys("ProductoEjemplo")
    #    self.driver.find_element(By.ID, "id_descripcion").send_keys("Un producto de ejemplo")
    #    self.driver.find_element(By.ID, "id_precio").send_keys("1.99")
    #    dropdown = self.driver.find_element(By.ID, "id_dieta")
    #    dropdown.find_element(By.XPATH, "//option[. = 'Vegetariano']").click()
    #    self.driver.find_element(By.ID, "id_ubicaciones").click()
    #    dropdown = self.driver.find_element(By.ID, "id_ubicaciones")
    #    dropdown.find_element(By.XPATH, "//option[. = 'Carrefour']").click()
    #    elements = self.driver.find_elements(By.CSS_SELECTOR, ".save")
    #    assert len(elements) > 0
    #    self.driver.find_element(By.CSS_SELECTOR, ".save").click()

    #def test_selenium_not_create_product(self):
    #    self.driver.get(f'{self.live_server_url}/')
    #    self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #    self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
    #    self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
    #    self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #    self.driver.find_element(By.CSS_SELECTOR, ".botonAdd > img").click()
    #    #self.driver.find_element(By.ID, "id_foto").send_keys("\leche.jpg")
    #    self.driver.find_element(By.ID, "id_nombre").send_keys("ProductoMalEjemplo")
    #    self.driver.find_element(By.ID, "id_descripcion").click()
    #    self.driver.find_element(By.ID, "id_descripcion").send_keys("Un producto de mal ejemplo")
    #    self.driver.find_element(By.ID, "id_precio").send_keys("100.01")
    #    dropdown = self.driver.find_element(By.ID, "id_dieta")
    #    dropdown.find_element(By.XPATH, "//option[. = 'Vegetariano']").click()
    #    dropdown.find_element(By.XPATH, "//option[. = 'Vegano']").click()
    #    elements = self.driver.find_elements(By.CSS_SELECTOR, ".col-sm-8")
    #    assert len(elements) > 0

    def test_aboutUs(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.CSS_SELECTOR, ".col-sm-2:nth-child(1) u").click()
        self.driver.find_element(By.CSS_SELECTOR, ".titleblock").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".titleblock").text == "¡Nuestro proyecto!"

    def test_contactUs(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.CSS_SELECTOR, ".col-sm-2:nth-child(2) u").click()
        self.driver.find_element(By.CSS_SELECTOR, ".titleblock").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".titleblock").text == "¡Contáctanos!"

    def test_privacy(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.CSS_SELECTOR, ".col-sm-3 u").click()
        self.driver.find_element(By.CSS_SELECTOR, ".titleblock").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".titleblock").text == "Políticas de privacidad"

    def test_valorar_producto(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/product/show/46')
        self.driver.find_element(By.ID, "second").click()
        assert self.driver.find_element(By.ID, "msjrating").text == "Su voto ha sido procesado"
        self.driver.find_element(By.LINK_TEXT, "Lista de productos").click()
        self.driver.find_element(By.CSS_SELECTOR, ".col-xl-3:nth-child(8) .row-fluid .m-auto").click()
        self.driver.find_element(By.ID, "third").click()
        assert self.driver.find_element(By.ID, "msjrating").text == "Ya ha realizado una valoración"

    def test_ubicacion(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/product/show/46')
        self.driver.find_element(By.ID, "addUbicacion").click()
        self.driver.find_element(By.ID, "id_ubicaciones").click()
        self.driver.find_element(By.ID, "id_ubicaciones").click()
        self.driver.find_element(By.CSS_SELECTOR, "#link > img").click()
        self.driver.find_element(By.ID, "id_precio").click()
        self.driver.find_element(By.ID, "id_precio").send_keys("10")
        self.driver.find_element(By.NAME, "addingUbication").click()
        assert self.driver.switch_to.alert.text == "Elija o cree una ubicación"
        self.driver.find_element(By.ID, "id_nombreComercio").click()
        self.driver.find_element(By.ID, "id_nombreComercio").send_keys("Prueba")
        self.driver.find_element(By.CSS_SELECTOR, "#p-3 > .container-fluid").click()
        self.driver.find_element(By.ID, "Si").click()
        self.driver.find_element(By.NAME, "addingUbication").click()
        self.driver.find_element(By.CSS_SELECTOR, ".col-md-3:nth-child(3) > .m-auto").click()
        self.driver.find_element(By.ID, "select").click()
        dropdown = self.driver.find_element(By.ID, "select")
        dropdown.find_element(By.XPATH, "//option[. = 'Prueba']").click()
        value = self.driver.find_element(By.ID, "select").get_attribute("value")
        assert value == "-3,702433;40,417148;False"
        self.driver.find_element(By.ID, "select").click()

    def test_comentario(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/product/show/46')
        self.driver.find_element(By.XPATH, "//span[contains(.,\'Comentarios\')]").click()
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Comentar\')]").click()
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("Prueba")
        self.driver.find_element(By.ID, "id_mensaje").click()
        self.driver.find_element(By.ID, "id_mensaje").send_keys("Prueba")
        self.driver.find_element(By.NAME, "commentButton").click()
        self.driver.find_element(By.XPATH, "//span[contains(.,\'Comentarios\')]").click()
        self.driver.find_element(By.XPATH, "//div[@id=\'collapseproducts\']/div[2]/span").click()
        self.driver.find_element(By.XPATH, "//div[@id=\'p-2\']/div/div/div/div[2]").click()
        assert self.driver.find_element(By.XPATH, "//div[@id=\'p-2\']/div/div/div/div[2]/div[2]").text == "Prueba"
        self.driver.find_element(By.CSS_SELECTOR, ".fas").click()
        self.driver.find_element(By.CSS_SELECTOR, ".col-md-3:nth-child(2) > .m-auto").click()
        text = self.driver.find_element(By.CSS_SELECTOR, "#p-2 > .container-fluid").text
        assert text != "Prueba"

    def test_reporte(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyAdminPasswordJQSA!=1")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/product/show/42')
        self.driver.find_element_by_xpath( "//button[contains(.,'Reportar Producto')]").click()
        self.driver.find_element(By.ID, "id_causa_0").click()
        self.driver.find_element(By.ID, "id_comentarios").click()
        self.driver.find_element(By.ID, "id_comentarios").send_keys("Prueba reporte")
        self.driver.find_element(By.NAME, "reportButton").click()
        self.driver.find_element(By.LINK_TEXT, "Revisar reportes").click()
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(6) .fa").click()
        self.driver.find_element(By.CSS_SELECTOR, "#modalRep5 .modal-body").click()
        self.driver.find_element(By.CSS_SELECTOR, "#modalRep5 .modal-body").click()
        element = self.driver.find_element(By.CSS_SELECTOR, "#modalRep5 .modal-body")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "#modalRep5 .modal-body").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "#modalRep5 .modal-body").text == "Producto:\\\\nFideos Yakisoba curry\\\\n\\\\nCausa:\\\\nProducto repetido\\\\n\\\\nComentarios:\\\\nPrueba reporte"

    def test_listacompra(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/shoppingList')
        text = self.driver.find_element(By.CSS_SELECTOR, ".row-12:nth-child(1) > .col:nth-child(2)").text
        assert text != "Natillas danet"
        self.driver.find_element(By.LINK_TEXT, "Lista de productos").click()
        self.driver.find_element(By.LINK_TEXT, "Ver detalles").click()
        self.driver.find_element(By.ID, "buttonAddList").click()
        self.driver.find_element(By.LINK_TEXT, "Mi cuenta").click()
        self.driver.find_element(By.LINK_TEXT, "Mi Lista").click()
        self.driver.find_element(By.CSS_SELECTOR, ".row-12:nth-child(2)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".row-12:nth-child(1) .enlaceRecetas").text == "Natillas danet"
        self.driver.find_element(By.CSS_SELECTOR, ".row-12:nth-child(2) .fas").click()
        text = self.driver.find_element(By.CSS_SELECTOR, ".shopping-list-cards").text
        assert text != "Natillas danet"
        self.driver.find_element(By.LINK_TEXT, "Eliminar lista completa").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".align-self-center").text == "Añada algún producto a la lista de la compra"
