import steammarket as sm

item_name = "★ Butterfly Knife | Fade (Factory New)"
item = sm.get_csgo_item(item_name, currency='EUR')
price = item
print(f"The price of {item_name} is {price}")
