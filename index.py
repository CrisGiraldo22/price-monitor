import time
import requests #realiza peticiones http, obtiene las paginas web y maneja headers y cookies.
from bs4 import BeautifulSoup #Parsea html y xml, encuentra elementos especificos. ademas extrae textos y atributos.
import schedule # programa tareas automaticas, ejecuta funciones en horarios especificos y maneja intervalos de tiempo.

class MonitorPrice: 
     #Clase que monitorea el precio de un producto en una página web (Mercado Libre) y envía una alerta si el precio baja por debajo del objetivo.
    
    def __init__(self, url, target_price: float): 
    #Inicializa el monitor de precios.

    #param url: URL del producto a monitorear.
    #param target_price: Precio objetivo para la alerta.
        
        self.url = url
        self.target_price = target_price
        
    #Obtiene el precio actual del producto desde la página.
    #return: Precio del producto como float, o None si no se puede obtener.
    #Deteta errores HTTP
        
    def get_price(self) -> float | None:
        headers ={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try: 
            response =requests.get(self.url, headers=headers)
            response.raise_for_status() 
            soup = BeautifulSoup(response.content, 'html.parser')
            
            item_container = soup.find('div', class_='ui-pdp-price__second-line')
            item_price_span = item_container.find('span', class_='andes-money-amount__fraction') if item_container else None
            
            if not item_price_span:
                print("⚠️ The element was not found")
                return None
            
            price_texto = item_price_span.text.strip() 
        #Replace elimina el separador de miles
            price = float(price_texto.replace('.',''))
            return price
        
        except Exception as e:
            print(f" ❌ Error: {e}")
            return None
    
    #Muestra una alerta si el precio es menor o igual al objetivo.
    #param current_price: Precio actual del producto.  
    def show_alert(sefl, current_price: float):
        print("🔴 ¡PRICE ALERT!...")
        print(F"Current price: ${current_price}")
        print(f"Target price: ${sefl.target_price}")
        print("¡✅ It's time to buy!...")
        
        
    #Revisa si el precio actual cumple con la condición del objetivo.
    #return: True si el precio es igual o menor al objetivo, False en otro caso.
    def check_price(self) -> bool:
        current_price = self.get_price()
        
        if current_price is None:
            return False
        
        if current_price <= self.target_price:
            self.show_alert(current_price)
            return True
        
        print(f"Current price: ${current_price} - It hasn't gone down yet.")
        
        return False #Continuar monitoreando 
    
    #Inicia el monitoreo diario del precio, revisando a las 9:00 AM.
    
    def monitor(self):
        print(f"Monitor: {self.url}")
        print(f"Target price: ${self.target_price}")
        print("checking every day at 09:00 am.")
    #Programar revisión diaria a la 9:00 Schedule
        schedule.every().day.at("09:00").do(self.check_price) 
        
    #Hace revisión inmediata 
        print("Doing firts review...")
        if self.check_price():
            return # Si encuentra el precio termina
    
    # Ciclo para revisar cada minuto si hay tareas programadas pendiente   
        while True:
            schedule.run_pending()
            time.sleep(60) #Revisar cada minuto si hay tareas pendientes
            
# --- Punto de entrada del programa ---
if __name__== "__main__":
    product_url = ("https://www.mercadolibre.com.co/portatil-asus-vivobook-x1502-ci5-12500h-24gb-ssd512-fhd156-color-quiet-blue/p/MCO47191661#polycard_client=search-nordic&searchVariation=MCO47191661&position=2&search_layout=stack&type=product&tracking_id=f1bafa75-37de-4658-82f4-5bb01bb1905f&wid=MCO1569451947&sid=search")
    
    price_monitor = MonitorPrice(url=product_url, target_price= 2000000)
    target_price=2000000
    price_monitor.monitor()