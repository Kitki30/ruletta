import time
import random
import machine

import apps.thirdparty.com_kitki30_ruletta.drawer as drawer
import apps.thirdparty.com_kitki30_ruletta.texts as texts

import modules.io_manager as io_man
import modules.menus as menus
import modules.os_constants as osc

import fonts.def_8x8 as f8x8

tft = io_man.get("tft")

# Entrypoint
def run():
    while True:

        ruletta_menu = menus.menu("Ruletta", [
            ("Play", 1),
            ("Warning!", 2),
            ("Exit", None)
        ])

        if ruletta_menu == None:
            break

        if ruletta_menu == 1:
            play()
        elif ruletta_menu == 2:
            import modules.popup as popup
            popup.show("This game is made for entertainment puproses only, please don't use it to gamble real money. Authors and contributors don't take any responsibility for loses.")

def play():
    bet = menus.menu("Ruletta", [
        ("Bet on red", 2),
        ("Bet on black", 1),
        ("Exit", None)
    ])
    
    if bet == None:
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
    
    random.seed(time.ticks_ms())

    time.sleep(2)

    # Random outcome
    sectors = 6
    target_sector = random.randint(0, sectors - 1)
    win = (bet == 1 and target_sector % 2 == 0) or (bet == 2 and target_sector % 2 == 1)

    full_turns = random.randint(15, 25)   # Full turns
    total_steps = full_turns * sectors + target_sector  # Target steps
    current_sector = 0
    prev_sector = None

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

    # Random message
    time.sleep(1)
    msg = random.choice(texts.WIN) if win else random.choice(texts.LOST)
    tft.text(f8x8, msg, 0, 127, 63788)
    time.sleep(5)