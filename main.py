#Estados
#IDLE: Contador OFF, LED parpadeo lento
#READY: pilot OK, esperando uusuario (LED FIJO)
#CHARGING: contactor ON(si no hay fallo) - LED Parpadeo rápido
#FAULT #Contador OFF , LED doble destello/s

#Reglas:
1. Arranque -> IDLE
2. IDLE -> READY cuando PILOT_OK = 1
3. READY -> CHARGING al pulsar boton
4. EN CUALQUIER ESTADO FAULT = 1 -> FAULT DESDE FAULT SE DESPEJA Y CON EL BTN A IDLE
5. CHARGING, SI PILOT_OK = 0 IDLE
