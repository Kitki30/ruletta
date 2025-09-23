import time
import random
import machine

import apps.thirdparty.com_kitki30_ruletta.drawer as drawer
import apps.thirdparty.com_kitki30_ruletta.texts as texts

import modules.io_manager as io_man
import modules.menus as menus
import modules.os_constants as osc
import modules.cache as cache
import modules.seed_random as s_random
import modules.nvs as nvs
import modules.popup as popup
import modules.numpad as numpad

import fonts.def_8x8 as f8x8

tft = io_man.get("tft")
n_shared = cache.get_nvs("kitki30_shared")

# Entrypoint
def run():
    init_nvs()
    
    if cache.get('random_seeded') != True:
        s_random.seed()
    
    while True:
        ruletta_menu = menus.menu("Ruletta", [
            ("Play", 1),
            ("Bank", 2),
            ("Warning!", 3),
            ("Exit", None)
        ])

        if ruletta_menu == None:
            break
        if ruletta_menu == 1:
            play()
        elif ruletta_menu == 2:
            bank()
        elif ruletta_menu == 3:
            popup.show("This game is made for entertainment puproses only, please don't use it to gamble real money. Authors and contributors don't take any responsibility for loses.")
            
# Init NVS
def init_nvs(bypass=False):
    if nvs.get_int(n_shared, "ru_init") != 1 or bypass:
        nvs.set_int(n_shared, "ru_init", 1)
        nvs.set_int(n_shared, "ru_money", 1000)
        nvs.set_int(n_shared, "ru_games_played", 0)
        nvs.set_int(n_shared, "ru_games_won", 0)
        nvs.set_int(n_shared, "ru_money_lost", 0)
        nvs.set_int(n_shared, "ru_money_won", 0)
            
# Bank
def bank():
    while True:
        bank_menu = menus.menu("Balance: " + str(nvs.get_int(n_shared, "ru_money")), [
            ("Work", 1),
            ("See stats", 2),
            ("Reset everything", 3),
            ("Warning!", 4),
            ("Back", None)
        ])
        
        if bank_menu == None:
            break
        
        if bank_menu == 1:
            time.sleep(0.1)
            earn = random.randint(10, 50)
            nvs.set_int(n_shared, "ru_money", nvs.get_int(n_shared, "ru_money") + earn)
        elif bank_menu == 2:
            popup_text = f"""
            Money: {nvs.get_int(n_shared, "ru_money")}
            Games played: {nvs.get_int(n_shared, "ru_games_played")}
            Games won: {nvs.get_int(n_shared, "ru_games_won")}
            Games lost: {nvs.get_int(n_shared, "ru_games_played") - nvs.get_int(n_shared, "ru_games_won")}
            Money won: {nvs.get_int(n_shared, "ru_money_won")}
            Money lost: {nvs.get_int(n_shared, "ru_money_lost")}
            """
            
            popup.show(popup_text, "Stats")
        elif bank_menu == 3:
            confirm = menus.menu("Are you sure?", [
                ("Yes", True),
                ("No", False)
            ])
            if confirm:
                init_nvs(bypass=True)
        elif bank_menu == 4:
            popup.show("This game is made for entertainment puproses only, please don't use it to gamble real money. Authors and contributors don't take any responsibility for loses. Money in bank is not real money, and cannot be withdrawn or exchanged for real money.")

def play():
    bet = menus.menu("Ruletta", [
        ("Bet on red", 2),
        ("Bet on black", 1),
        ("Exit", None)
    ])
    
    if bet == None:
        return
    
    bet_amount = numpad.numpad("Bet amount (max " + str(nvs.get_int(n_shared, "ru_money")) + ")")
    
    if bet_amount != None:
        bet_amount = int(bet_amount)
    
    if bet_amount == None or bet_amount < 1 or bet_amount > nvs.get_int(n_shared, "ru_money"):
        popup.show("Invalid bet amount!\nYour money: " + str(nvs.get_int(n_shared, "ru_money")) + "\nSelected amount: " + str(bet_amount))
        return
    
    tft.fill(0)

    machine.freq(osc.ULTRA_FREQ)

    # Draw green circle
    drawer.fill_circle(tft, 160, 67, 70, 0x0324)
    # Roulette
    drawer.draw_roulette(tft, 160, 67, 50)
    # Lamps
    lamps = drawer.draw_lamps(tft, 160, 67, 50)

    # Bet tags
    bet_text = "Bet on: "
    if bet == 2:
        bet_text += "Red"
    else:
        bet_text += "Black"
    tft.text(f8x8, bet_text, 0, 0, 65535)

    time.sleep(2)

    # Random outcome
    sectors = 6
    target_sector = random.randint(0, sectors - 1)
    win = (bet == 1 and target_sector % 2 == 0) or (bet == 2 and target_sector % 2 == 1)

    full_turns = random.randint(15, 25)   # Full turns
    total_steps = full_turns * sectors + target_sector  # Target steps
    current_sector = 0
    prev_sector = None

    # Save money, get random text
    if win == True:
        msg = random.choice(texts.WIN)
        nvs.set_int(n_shared, "ru_money", nvs.get_int(n_shared, "ru_money") + bet_amount)
        nvs.set_int(n_shared, "ru_games_played", nvs.get_int(n_shared, "ru_games_played") + 1)
        nvs.set_int(n_shared, "ru_games_won", nvs.get_int(n_shared, "ru_games_won") + 1)
        nvs.set_int(n_shared, "ru_money_won", nvs.get_int(n_shared, "ru_money_won") + bet_amount)
    else: 
        nvs.set_int(n_shared, "ru_money", nvs.get_int(n_shared, "ru_money") - bet_amount)
        nvs.set_int(n_shared, "ru_games_played", nvs.get_int(n_shared, "ru_games_played") + 1)
        nvs.set_int(n_shared, "ru_money_lost", nvs.get_int(n_shared, "ru_money_lost") + bet_amount)
        msg = random.choice(texts.LOST)

    for step in range(total_steps):
        if prev_sector is not None:
            drawer.light_lamp(tft, lamps, prev_sector, 0x7BEF)
        
        # Light up lamp
        drawer.light_lamp(tft, lamps, current_sector % sectors)
        prev_sector = current_sector % sectors

        # Speed curve
        fraction = step / total_steps
        if fraction < 0.15:
            delay = 0.02 - fraction * 0.12
        elif fraction > 0.7:
            f = (fraction - 0.7) / 0.3
            delay = 0.005 + (f**2) * 0.12 + random.uniform(0, 0.003)
        else:
            delay = 0.005

        time.sleep(delay)
        current_sector += 1

    # Light down all other, show result
    for i in range(sectors):
        drawer.light_lamp(tft, lamps, i, 0x7BEF)
    drawer.light_lamp(tft, lamps, target_sector)

    machine.freq(osc.BASE_FREQ)
    
    # Random message
    time.sleep(1)
    tft.text(f8x8, msg, 0, 127, 63788)
    time.sleep(3)