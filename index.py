import requests #realiza peticiones http, obtiene las paginas web y maneja headers y cookies.
from bs4 import BeautifulSoup #Parsea html y xml, encuentra elementos especificos. ademas extrae textos y atributos.
import schedule # programa tareas automaticas, ejecuta funciones en horarios especificos y maneja intervalos de tiempo.

class MonitorPrecios: 
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