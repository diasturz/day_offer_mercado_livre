import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains

from time import sleep

#### Você deve estar com o navegador do driver com whatsapp conectado



def day_offer_in_mercadolivre(contact_name:str, is_group=False):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # retirar interface gráfica
    driver1 = webdriver.Chrome(options=options)
    driver1.get("https://www.mercadolivre.com.br/")
    driver1.maximize_window()
    sleep(5)
    text = driver1.find_element(By.CLASS_NAME, 'ui-recommendations-carousel-dual__first-card')
    sleep(1)
    action = ActionChains(driver1)
    action.move_to_element(text).click().perform()
    sleep(5)
    item_with_discount = driver1.find_element(By.CLASS_NAME, 'ui-pdp-title')
    price_with_discount = driver1.find_element(By.CLASS_NAME, 'ui-pdp-price__second-line').text
    target_url_image = driver1.find_element(By.XPATH, "//img[contains(@class, 'ui-pdp-gallery__figure')]")
    url = target_url_image.get_attribute("src")

    response = requests.get(url)
    
    with open("image_offer.png", "wb") as file:
        file.write(response.content)
    
    print(len(price_with_discount.split('\n')))

    print(50*'-')

    print(price_with_discount.split('\n'))
    if len(price_with_discount.split('\n')) > 3:
        price_with_discount = price_with_discount.split('\n')[1].replace('.','')+'.'+price_with_discount.split('\n')[3]
    else:
        price_with_discount = price_with_discount.split('\n')[1].replace('.','')
    price_with_discount_formatted = float(price_with_discount)
    print(f"The item with discount is {item_with_discount.text} and the price is R${price_with_discount_formatted}")
    print(50*'-')
    url_purchase = driver1.current_url
    price_without_discount = driver1.find_element(By.XPATH, "//span[@data-testid='price-part']").text
    print(price_without_discount.split('\n'))
    if len(price_without_discount.split('\n')) > 2:
        price_without_discount = price_without_discount.split('\n')[1].replace('.','')+'.'+price_without_discount.split('\n')[3]
    else:
        price_without_discount = price_without_discount.split('\n')[1].replace('.','')

    price_without_discount_formatted = float(price_without_discount)

    print(f"The price with discount is R${price_with_discount_formatted} and the price without discount is R${price_without_discount_formatted}")
    print(50*'-')
    price_now = price_with_discount_formatted # price_now é o preco com desconto
    price_before = price_without_discount_formatted
    economy = float(price_before - price_now)
    print(f"The economy is R${economy}")
    print("Webscrapping succed")

    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir=C:\\Users\\artur\\AppData\\Local\\Google\\Chrome\\User Data\\Profile_6_Clone")  # Aqui você trocará pelo seu perfil logado
    # options.add_argument("--headless")

    # Inicializar o ChromeDriver
    service = Service("C:\\Users\\artur\\Desktop\\rpa\\chromedriver.exe")
    driver = webdriver.Chrome(service=service,options=options)
    # Abrir o WhatsApp Web
    driver.get("https://web.whatsapp.com")
    driver.maximize_window()
    sleep(30)
    action = ActionChains(driver)
    # Encontrar o contato
    autocomplete = driver.find_element(By.XPATH, "//div/div[contains(@aria-autocomplete,'list')]")
    autocomplete.send_keys(contact_name)
    sleep(1)
    if is_group:
        contato = driver.find_element(By.XPATH, "//div[@aria-selected='false']")
    else:
        contato = driver.find_element(By.XPATH, f"//span[@title='{contact_name}']")
    action.move_to_element(contato).click().perform()
    sleep(1)
    mensagem = f"Olá :)\n\nEu sou o turzin-bot e vou estar aqui te falando sobre a oferta do dia no mercado livre!\n\nO preço do produto {item_with_discount.text} com desconto é *R${price_now}* e a *economia é de R${economy.__round__(2)}!*\n\nIsso significa que custava *R${float(price_before)}*.\n\nO link de compra é {url_purchase}"
    driver.find_element(By.XPATH, "//div/div[contains(@aria-placeholder,'Digite uma mensagem')]").send_keys(mensagem)
    driver.find_element(By.XPATH, "//div/div[contains(@aria-placeholder,'Digite uma mensagem')]").send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, '//span[@data-icon="plus"]').click()
    # Localizar o <input> para anexar imagem
    input_imagem = driver.find_element(By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
    caminho_imagem = 'C:\\Users\\artur\\Desktop\\rpa\\image_offer.png'  # Substitua pelo caminho completo da sua imagem
    input_imagem.send_keys(caminho_imagem)  # Enviar a imagem
    sleep(3)
    send_button = driver.find_element(By.XPATH, "//div/span[contains(@data-icon,'send')]")
    send_button.click()
    sleep(3)  # Aguarde o upload da imagem
    driver1.quit()
    driver.quit()

day_offer_in_mercadolivre("Entusiasta 2.0",True)

