from web_app.model import Robot

carrie = Robot("Carrie")

print(carrie.battery)
carrie.battery = "50.0"
print(carrie.battery)