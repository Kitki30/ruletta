import time
import random

import apps.thirdparty.com_kitki30_ruletta.drawer as drawer
import apps.thirdparty.com_kitki30_ruletta.texts as texts

import modules.io_manager as io_man
import modules.menus as menus

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

    # Random outcome
    sectors = 6
    target_sector = random.randint(0, sectors - 1)
    win = (bet == 1 and target_sector % 2 == 0) or (bet == 2 and target_sector % 2 == 1)

    # Spin
    total_steps = random.randint(80, 150)
    current_sector = 0
    prev_sector = None
    delay_base = 0.01

    for step in range(total_steps):
        # Turn off last light
        if prev_sector is not None:
            drawer.light_lamp(tft, lamps, prev_sector, 0x7BEF)  # gray

        # Light up curr light
        drawer.light_lamp(tft, lamps, current_sector % sectors)

        prev_sector = current_sector % sectors

        # Smooth slowdown
        fraction = step / total_steps
        delay = delay_base + (fraction ** 3) * 0.12 + random.uniform(0, 0.005)
        time.sleep(delay)

        current_sector += 1

    # Stop for result
    for i in range(sectors):
        drawer.light_lamp(tft, lamps, i, 0x7BEF)
    drawer.light_lamp(tft, lamps, target_sector)

    # Message
    msg = random.choice(texts.WIN) if win else random.choice(texts.LOST)
    tft.text(f8x8, msg, 0, 127, 65535)
    time.sleep(3)