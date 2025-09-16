import random
import time
import sys

# --- Data dan Konstanta ---

# Senjata: nama, damage
WEAPONS = {
    "baseball": 5,
    "pisau": 15,
    "kapak": 25,
    "pistol": [15, 30, 50]  # pistol damage bisa bervariasi
}

# Item heal dan efek
ITEMS = {
    "bandage": {"heal": 15, "price": 10},
    "api_unggul": {"heal_sanity": True, "price": 15},
    "peluru": {"amount": 10, "price": 20},
    "jimat": {"price": 10000}
}

# Enemy data: name, damage options, hp, drop chance %
ENEMIES = [
    {"name": "the error", "damage": [5, 10, 20], "hp": 50, "chance": 30, "drop": ["bandage", "peluru"]},
    {"name": "the corrupted", "damage": [10, 18, 15, 30], "hp": 100, "chance": 28, "drop": ["bandage", "api_unggul"]},
    {"name": "the boiled one", "damage": [15, 25, 30, 45], "hp": 250, "chance": 5, "drop": ["jimat"]}
]

# Merchant stock (senjata dan item)
MERCHANT_STOCK = {
    "bandage": 10,
    "api_unggul": 15,
    "peluru": 20,
    "jimat": 10000,
    "baseball": 0,
    "pisau": 0,
    "kapak": 0,
    "pistol": 0
}

# --- Fungsi Utility ---

def slow_print(text, delay=0.03):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

def clear_screen():
    print("\n" * 50)

def press_enter():
    input("Tekan Enter untuk melanjutkan...")

# --- Kelas Player ---

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.sanity = 100.0  # persen
        self.money = 50
        self.inventory = {
            "baseball": 1,
            "bandage": 1,
            "api_unggul": 0,
            "jimat": 0,
            "peluru": 0
        }
        self.weapons = ["baseball"]  # senjata yang dimiliki
        self.current_weapon = "baseball"

    def show_status(self):
        slow_print(f"Nama: {self.name}")
        slow_print(f"HP: {self.hp}/{self.max_hp}")
        slow_print(f"Sanity: {self.sanity:.2f}%")
        slow_print(f"Uang: Rp{self.money}")
        slow_print(f"Senjata saat ini: {self.current_weapon} (Damage: {self.get_weapon_damage()})")

    def get_weapon_damage(self):
        if self.current_weapon == "pistol":
            # pistol damage random dari list
            return random.choice(WEAPONS["pistol"])
        else:
            return WEAPONS.get(self.current_weapon, 0)

    def show_inventory(self):
        slow_print("Inventory:")
        for item, qty in self.inventory.items():
            if qty > 0:
                if item in WEAPONS:
                    slow_print(f"- {item} (Senjata) x{qty}")
                else:
                    slow_print(f"- {item} x{qty}")

    def has_item(self, item):
        return self.inventory.get(item, 0) > 0

    def add_item(self, item, qty=1):
        if item in self.inventory:
            self.inventory[item] += qty
        else:
            self.inventory[item] = qty

    def remove_item(self, item, qty=1):
        if self.has_item(item):
            self.inventory[item] -= qty
            if self.inventory[item] < 0:
                self.inventory[item] = 0

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def reduce_sanity(self, amount):
        self.sanity -= amount
        if self.sanity < 0:
            self.sanity = 0

    def increase_sanity(self, amount):
        self.sanity += amount
        if self.sanity > 100:
            self.sanity = 100

# --- Kelas Enemy ---

class Enemy:
    def __init__(self, data):
        self.name = data["name"]
        self.hp = data["hp"]
        self.max_hp = data["hp"]
        self.damage_options = data["damage"]
        self.drop = data["drop"]

    def attack(self):
        return random.choice(self.damage_options)

# --- Fungsi Game ---

def intro():
    clear_screen()
    slow_print("Dunia ini gelap dan penuh misteri...")
    slow_print("Kamu terjebak di dunia creepy pasta yang menyeramkan.")
    slow_print("Sanity-mu akan diuji, dan bertahan hidup adalah satu-satunya tujuan.")
    slow_print("Berhati-hatilah, karena kegelapan menyimpan banyak rahasia dan bahaya.")
    press_enter()

def choose_name():
    clear_screen()
    name = input("Masukkan nama player: ").strip()
    if not name:
        name = "Player"
    return name

def main_menu():
    slow_print("\n=== MENU UTAMA ===")
    slow_print("1. Jelajahi dunia creepy")
    slow_print("2. Status")
    slow_print("3. Storage (Inventory)")
    slow_print("4. Merchant")
    slow_print("5. Exit Game")
    choice = input("Pilih opsi (1-5): ")
    return choice

def explore(player):
    clear_screen()
    slow_print("Kamu mulai menjelajahi dunia creepy...")
    # Tentukan musuh muncul berdasarkan chance
    enemy = spawn_enemy()
    if enemy:
        slow_print(f"Musuh muncul! {enemy.name} menyerang!")
        battle(player, enemy)
    else:
        slow_print("Tidak ada musuh yang muncul kali ini.")
        # Sanity berkurang sedikit karena suasana mencekam
        sanity_loss = random.uniform(1, 3)
        player.reduce_sanity(sanity_loss)
        slow_print(f"Sanity-mu berkurang {sanity_loss:.2f}% karena suasana mencekam.")
        if player.sanity < 10:
            sanity_effect(player)
    press_enter()

def spawn_enemy():
    roll = random.uniform(0, 100)
    cumulative = 0
    for data in ENEMIES:
        cumulative += data["chance"]
        if roll <= cumulative:
            return Enemy(data)
    return None

def battle(player, enemy):
    while enemy.hp > 0 and player.hp > 0:
        slow_print(f"\n{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
        slow_print(f"Player HP: {player.hp}/{player.max_hp} | Sanity: {player.sanity:.2f}%")
        slow_print("Opsi bertarung:")
        slow_print("1. Serang")
        slow_print("2. Heal (bandage & api unggun)")
        slow_print("3. Ganti senjata")
        slow_print("4. Kabur")
        choice = input("Pilih opsi (1-4): ")

        if choice == "1":
            # Serang musuh
            damage = player.get_weapon_damage()
            slow_print(f"Kamu menyerang dengan {player.current_weapon} dan memberikan damage {damage}.")
            enemy.hp -= damage
            if enemy.hp <= 0:
                slow_print(f"Musuh {enemy.name} telah dikalahkan!")
                drop_loot(player, enemy)
                break
        elif choice == "2":
            heal_battle(player)
        elif choice == "3":
            change_weapon(player)
            continue
        elif choice == "4":
            if try_escape():
                slow_print("Kamu berhasil kabur dari pertarungan!")
                break
            else:
                slow_print("Gagal kabur!")
        else:
            slow_print("Opsi tidak valid.")
            continue

        # Musuh menyerang jika masih hidup
        if enemy.hp > 0:
            enemy_attack(player, enemy)
            if player.hp <= 0:
                death_effect(player, enemy)
                break

        # Sanity berkurang sedikit setiap giliran
        sanity_loss = random.uniform(0.5, 2)
        player.reduce_sanity(sanity_loss)
        if player.sanity < 10:
            sanity_effect(player)

def heal_battle(player):
    slow_print("Item heal yang tersedia:")
    options = []
    if player.has_item("bandage"):
        options.append("bandage")
        slow_print(f"- Bandage (heal 15%) x{player.inventory['bandage']}")
    if player.has_item("api_unggul"):
        options.append("api_unggul")
        slow_print(f"- Api Unggun (heal sanity perlahan) x{player.inventory['api_unggul']}")
    if not options:
        slow_print("Tidak ada item heal yang tersedia.")
        return
    choice = input(f"Pilih item heal ({'/'.join(options)}): ").lower()
    if choice == "bandage" and player.has_item("bandage"):
        heal_amount = int(player.max_hp * 0.15)
        player.heal(heal_amount)
        player.remove_item("bandage")
        slow_print(f"Kamu menggunakan bandage dan sembuh {heal_amount} HP.")
    elif choice == "api_unggul" and player.has_item("api_unggul"):
        # api unggun meningkatkan sanity perlahan
        sanity_gain = 10
        player.increase_sanity(sanity_gain)
        player.remove_item("api_unggul")
        slow_print(f"Kamu menggunakan api unggun dan sanity bertambah {sanity_gain}%.")
    else:
        slow_print("Item tidak valid atau tidak tersedia.")

def change_weapon(player):
    slow_print("Senjata yang kamu miliki:")
    for idx, wpn in enumerate(player.weapons, 1):
        slow_print(f"{idx}. {wpn} (Damage: {WEAPONS[wpn] if wpn != 'pistol' else '15/30/50'})")
    choice = input("Pilih senjata (nomor): ")
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(player.weapons):
            player.current_weapon = player.weapons[idx]
            slow_print(f"Senjata diganti ke {player.current_weapon}.")
        else:
            slow_print("Pilihan tidak valid.")
    else:
        slow_print("Input tidak valid.")

def try_escape():
    chance = 30
    roll = random.randint(1, 100)
    return roll <= chance

def enemy_attack(player, enemy):
    # Chance miss 25%
    if random.randint(1, 100) <= 25:
        slow_print(f"{enemy.name} menyerang tapi meleset!")
        return
    damage = enemy.attack()
    player.hp -= damage
    slow_print(f"{enemy.name} menyerang dan memberikan damage {damage} HP!")

def drop_loot(player, enemy):
    slow_print("Musuh menjatuhkan barang:")
    for item in enemy.drop:
        # Drop chance 50% per item
        if random.randint(1, 100) <= 50:
            player.add_item(item)
            slow_print(f"- {item} ditambahkan ke inventory.")
            # Jika senjata baru, tambahkan ke weapons list
            if item in WEAPONS and item not in player.weapons:
                player.weapons.append(item)
    # Drop jimat rare 10% chance
    if random.randint(1, 100) <= 10:
        player.add_item("jimat")
        slow_print("- Jimat rare didapatkan!")

def sanity_effect(player):
    slow_print("\n!!! Sanity-mu sangat rendah, dunia mulai terlihat aneh dan menyeramkan !!!")
    slow_print("Suara-suara aneh terdengar, bayangan bergerak di sudut matamu...")
    # Bisa ditambah efek lain jika ingin

def death_effect(player, enemy):
    slow_print(f"\nKamu telah dibunuh oleh {enemy.name}!")
    if enemy.name == "the error":
        slow_print("Tubuhmu mulai error dan perlahan menghilang...")
    elif enemy.name == "the corrupted":
        slow_print("Kamu mulai terinfeksi dan berubah menjadi corrupted...")
    elif enemy.name == "the boiled one":
        slow_print("Kamu mulai dikendalikan dan kepalamu direbus dalam air mendidih...")
    slow_print("Game Over.")
    sys.exit()

def merchant(player):
    clear_screen()
    slow_print("=== Merchant Creepy ===")
    slow_print("Barang yang tersedia:")
    # Tampilkan item yang harganya > 0
    for item, price in MERCHANT_STOCK.items():
        if price > 0:
            if item in WEAPONS:
                slow_print(f"- {item} (Senjata) Rp{price}")
            else:
                slow_print(f"- {item} Rp{price}")
    slow_print(f"Uang kamu: Rp{player.money}")
    slow_print("Ketik 'exit' untuk keluar merchant.")
    while True:
        choice = input("Mau beli apa? ").lower()
        if choice == "exit":
            break
        if choice in MERCHANT_STOCK and MERCHANT_STOCK[choice] > 0:
            price = MERCHANT_STOCK[choice]
            if player.money >= price:
                player.money -= price
                player.add_item(choice)
                slow_print(f"Berhasil membeli {choice} seharga Rp{price}.")
                # Jika senjata baru, tambahkan ke weapons list
                if choice in WEAPONS and choice not in player.weapons:
                    player.weapons.append(choice)
            else:
                slow_print("Uang tidak cukup.")
        else:
            slow_print("Barang tidak tersedia.")

def show_storage(player):
    clear_screen()
    player.show_inventory()
    press_enter()

def show_status(player):
    clear_screen()
    player.show_status()
    press_enter()

# --- Main Game Loop ---

def main():
    intro()
    name = choose_name()
    player = Player(name)

    while True:
        clear_screen()
        choice = main_menu()
        if choice == "1":
            explore(player)
        elif choice == "2":
            show_status(player)
        elif choice == "3":
            show_storage(player)
        elif choice == "4":
            merchant(player)
        elif choice == "5":
            slow_print("Terima kasih sudah bermain!")
            break
        else:
            slow_print("Pilihan tidak valid.")
            press_enter()

if __name__ == "__main__":
    main()

