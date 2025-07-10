import time
import requests #realiza peticiones http, obtiene las paginas web y maneja headers y cookies.
from bs4 import BeautifulSoup #Parsea html y xml, encuentra elementos especificos. ademas extrae textos y atributos.
import schedule # programa tareas automaticas, ejecuta funciones en horarios especificos y maneja intervalos de tiempo.

class MonitorPrice: 
    def __init__(self, url, target_price):
        self.url = url
        self.target_price = target_price
        
    #con está función emularemos un comportamiento humano
    def get_price(self):
        headers ={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try: 
            response =requests.get(self.url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            #buscar el prcio del elemento
            item_price = soup.find('span', class_='andes-money-amount__fraction')
            
            if not item_price:
                print("The element was not found")
                return None
            
            price_texto = item_price.text.strip() 
            # Extraer el número del precio (separador de miles en esté caso)
            price = float(price_texto.replace('.',''))
            return price
        
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def show_alert(sefl, current_price):
        print("🔴 ¡PRICE ALERT!...")
        print(F"Current price: ${current_price}")
        print(f"Target price: ${sefl.target_price}")
        print("¡It's time to buy!...")
        
    def check_price(self):
        current_price = self.get_price()
        if current_price and current_price <= self.target_price:
            self.show_alert(current_price)
            return True #Precio encontrado
        if current_price:
            print(f"Current price: ${current_price} - It hasn't gone down yet.")
        
        return False #Continuar monitoreando 
    
    def monitor(self):
        print(f"Monitor: {self.url}")
        print(f"Target price: ${self.target_price}")
        print("checking every day at 09:00 am.")
    #Programar revisión diaria a la 9:00 Schedule
        schedule.every().day.at("09:00").do(self.check_price) 
        
        #Hcaer revisión inmediata 
        print("Doing firts review...")
        if self.check_price():
            return # Si encuentra el precio termina
        
        while True:
            schedule.run_pending()
            time.sleep(60) #Revisar cada minuto si hay tareas pendientes
            
#Usa el monitor
if __name__== "__main__":
    monitors =MonitorPrice(url="https://www.mercadolibre.com.co/portatil-asus-vivobook-x1502-ci5-12500h-24gb-ssd512-fhd156-color-quiet-blue/p/MCO47191661#polycard_client=search-nordic&searchVariation=MCO47191661&position=2&search_layout=stack&type=product&tracking_id=f1bafa75-37de-4658-82f4-5bb01bb1905f&wid=MCO1569451947&sid=search",
    target_price=2000000)
    monitors.monitor()