import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

# --- Configuration and Data Definitions ---

# --- Theme Colors ---
BG_DARK = "#0A192F"      # Dark Blue
BG_LIGHT = "#112240"     # Slightly lighter blue
ACCENT_GREEN = "#64FFDA" # Bright Green
TEXT_COLOR = "#CCD6F6"   # Off-white/blue

RARITIES = {
    "Common": {"multiplier": 1.0, "color": "#A0A0A0", "luck_cost": 10},
    "Uncommon": {"multiplier": 2.5, "color": "#00FF00", "luck_cost": 25},
    "Rare": {"multiplier": 7.0, "color": "#0099FF", "luck_cost": 60},
    "Epic": {"multiplier": 20.0, "color": "#CC33FF", "luck_cost": 150},
    "Legendary": {"multiplier": 100.0, "color": "#FFCC00", "luck_cost": 400},
    "Mythic": {"multiplier": 500.0, "color": "#FF00FF", "luck_cost": 1200},
}

# Expanded Item List
ITEMS_LIST = [
    # Common
    {"name": "Bent Nail", "base_value": 5, "rarity": "Common"},
    {"name": "Rusty Bolt", "base_value": 7, "rarity": "Common"},
    {"name": "Dusty Cloth", "base_value": 10, "rarity": "Common"},
    {"name": "Broken Glass", "base_value": 12, "rarity": "Common"},
    {"name": "Old Key", "base_value": 15, "rarity": "Common"},
    {"name": "Scrap Metal", "base_value": 8, "rarity": "Common"},
    {"name": "Plastic Shard", "base_value": 6, "rarity": "Common"},
    # Uncommon
    {"name": "Copper Wire", "base_value": 20, "rarity": "Uncommon"},
    {"name": "Iron Plate", "base_value": 25, "rarity": "Uncommon"},
    {"name": "Simple Gear", "base_value": 30, "rarity": "Uncommon"},
    {"name": "Polished Stone", "base_value": 35, "rarity": "Uncommon"},
    {"name": "Small Battery", "base_value": 40, "rarity": "Uncommon"},
    {"name": "Circuit Board", "base_value": 45, "rarity": "Uncommon"},
    # Rare
    {"name": "Silver Bar", "base_value": 150, "rarity": "Rare"},
    {"name": "Ruby Fragment", "base_value": 180, "rarity": "Rare"},
    {"name": "Quartz Crystal", "base_value": 120, "rarity": "Rare"},
    # Epic
    {"name": "Gold Ingot", "base_value": 800, "rarity": "Epic"},
    {"name": "Emerald Gem", "base_value": 950, "rarity": "Epic"},
    {"name": "Plasma Cell", "base_value": 1100, "rarity": "Epic"},
    # Legendary
    {"name": "Diamond Core", "base_value": 5000, "rarity": "Legendary"},
    {"name": "Neutron Star Dust", "base_value": 7500, "rarity": "Legendary"},
    # Shards
    {"name": "Rare Fragment", "base_value": 80, "rarity": "Rare"},
    {"name": "Epic Crystal Shard", "base_value": 350, "rarity": "Epic"},
    {"name": "Legendary Shard", "base_value": 1500, "rarity": "Legendary"},
    {"name": "Mine-Shard", "base_value": 500, "rarity": "Epic"},
    {"name": "Void Shard", "base_value": 2000, "rarity": "Legendary"},
]

# Expanded Crafting Recipes
CRAFTING_RECIPES = [
    {"result": "Aether Key", "rarity": "Epic", "base_val": 700, "req": {"Rare Fragment": 5}},
    {"result": "Singularity Engine", "rarity": "Legendary", "base_val": 3000, "req": {"Epic Crystal Shard": 10}},
    {"result": "Apex Core", "rarity": "Mythic", "base_val": 15000, "req": {"Legendary Shard": 50}},
    {"result": "Reinforced Plate", "rarity": "Rare", "base_val": 200, "req": {"Iron Plate": 5, "Scrap Metal": 10}},
    {"result": "High-Cap Battery", "rarity": "Rare", "base_val": 250, "req": {"Small Battery": 3, "Copper Wire": 5}},
    {"result": "Advanced Processor", "rarity": "Epic", "base_val": 1200, "req": {"Circuit Board": 5, "Copper Wire": 10, "Plastic Shard": 20}},
    {"result": "Precision Clockwork", "rarity": "Rare", "base_val": 300, "req": {"Simple Gear": 8, "Polished Stone": 2}},
    {"result": "Master Key", "rarity": "Epic", "base_val": 1500, "req": {"Old Key": 10, "Aether Key": 1}},
    {"result": "Cybernetic Eye", "rarity": "Legendary", "base_val": 5000, "req": {"Broken Glass": 50, "Advanced Processor": 2, "Rare Fragment": 10}},
    {"result": "Void Fabric", "rarity": "Epic", "base_val": 1100, "req": {"Dusty Cloth": 30, "Epic Crystal Shard": 1}},
    {"result": "Quantum Capacitor", "rarity": "Legendary", "base_val": 8000, "req": {"Plasma Cell": 5, "Void Shard": 2}},
    {"result": "Mythic Relic", "rarity": "Mythic", "base_val": 50000, "req": {"Diamond Core": 5, "Apex Core": 1, "Void Shard": 10}},
]

# Add crafted items to ITEMS_LIST
for r in CRAFTING_RECIPES:
    ITEMS_LIST.append({"name": r["result"], "base_value": r["base_val"], "rarity": r["rarity"]})

CRATES = {
    1: {"name": "Junk Crate", "cost": 100, "luck_range": (50, 150), "weights": {"Common": 80, "Uncommon": 20}},
    2: {"name": "Standard Crate", "cost": 500, "luck_range": (150, 350), "weights": {"Common": 50, "Uncommon": 40, "Rare": 10}},
    3: {"name": "Reinforced Crate", "cost": 2500, "luck_range": (400, 800), "weights": {"Uncommon": 50, "Rare": 40, "Epic": 10}},
    4: {"name": "Advanced Crate", "cost": 10000, "luck_range": (1000, 2500), "weights": {"Rare": 60, "Epic": 35, "Legendary": 5}},
    5: {"name": "Ultimate Crate", "cost": 50000, "luck_range": (3000, 7000), "weights": {"Epic": 60, "Legendary": 35, "Mythic": 5}},
    6: {"name": "Void Crate", "cost": 250000, "luck_range": (8000, 15000), "weights": {"Epic": 30, "Legendary": 50, "Mythic": 20}},
    7: {"name": "Godly Crate", "cost": 1000000, "luck_range": (20000, 50000), "weights": {"Legendary": 60, "Mythic": 40}},
}

class CrateGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Crate Opening Simulator - Ultra")
        self.root.geometry("1100x850")
        self.root.configure(bg=BG_DARK)
        
        # Game State
        self.coins = 500
        self.inventory = {}
        self.item_data = {item['name']: item for item in ITEMS_LIST}
        self.selected_items = set()
        self.is_opening = False
        
        # Mining Upgrades
        self.mine_level = 1
        self.mine_shard_bonus = 0
        
        self.setup_styles()
        self.setup_ui()
        self.update_status()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=BG_DARK)
        style.configure("TLabel", background=BG_DARK, foreground=TEXT_COLOR, font=("Segoe UI", 10))
        style.configure("TLabelframe", background=BG_DARK, foreground=ACCENT_GREEN)
        style.configure("TLabelframe.Label", background=BG_DARK, foreground=ACCENT_GREEN, font=("Segoe UI", 11, "bold"))
        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_LIGHT, foreground=TEXT_COLOR, padding=[10, 5], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", BG_DARK)], foreground=[("selected", ACCENT_GREEN)])
        style.configure("TButton", background=BG_LIGHT, foreground=ACCENT_GREEN, borderwidth=1, font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", ACCENT_GREEN)], foreground=[("active", BG_DARK)])
        style.configure("Treeview", background=BG_LIGHT, foreground=TEXT_COLOR, fieldbackground=BG_LIGHT, rowheight=30)
        style.configure("Treeview.Heading", background=BG_DARK, foreground=ACCENT_GREEN, font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", ACCENT_GREEN)], foreground=[("selected", BG_DARK)])

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top Section: Status & Mining
        self.status_frame = ttk.LabelFrame(self.main_frame, text="Player Status & Mining", padding="10")
        self.status_frame.pack(fill=tk.X, pady=5)
        
        self.coin_label = ttk.Label(self.status_frame, text="Coins: 500", font=("Segoe UI", 16, "bold"), foreground=ACCENT_GREEN)
        self.coin_label.pack(side=tk.LEFT)
        
        self.mine_info_label = ttk.Label(self.status_frame, text="Mine Lvl: 1", font=("Segoe UI", 10))
        self.mine_info_label.pack(side=tk.LEFT, padx=20)
        
        self.mine_btn = ttk.Button(self.status_frame, text="⛏️ Mine Coins", command=self.mine)
        self.mine_btn.pack(side=tk.RIGHT)
        
        self.upgrade_mine_btn = ttk.Button(self.status_frame, text="Upgrade Mine (1,000)", command=self.upgrade_mine)
        self.upgrade_mine_btn.pack(side=tk.RIGHT, padx=10)
        
        # Middle Section: Tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Shop Tab
        self.shop_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.shop_tab, text="🛒 Shop")
        self.setup_shop_tab()
        
        # Inventory Tab
        self.inv_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.inv_tab, text="🎒 Inventory")
        self.setup_inv_tab()
        
        # Crafting Tab
        self.craft_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.craft_tab, text="⚒️ Crafting")
        self.setup_craft_tab()
        
        # Bottom Section: Log & Animation
        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_frame = ttk.LabelFrame(self.bottom_frame, text="Game Log", padding="10")
        self.log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_text = tk.Text(self.log_frame, height=6, bg=BG_LIGHT, fg=TEXT_COLOR, state=tk.DISABLED, wrap=tk.WORD, font=("Consolas", 10), borderwidth=0)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=self.scrollbar.set)
        
        self.anim_frame = ttk.LabelFrame(self.bottom_frame, text="Crate Opening", padding="10", width=300)
        self.anim_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        self.anim_label = ttk.Label(self.anim_frame, text="Ready...", font=("Segoe UI", 14, "bold"), foreground=ACCENT_GREEN)
        self.anim_label.pack(expand=True)

    def setup_shop_tab(self):
        canvas = tk.Canvas(self.shop_tab, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.shop_tab, orient="vertical", command=canvas.yview)
        shop_container = ttk.Frame(canvas)
        shop_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=shop_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for level, crate in CRATES.items():
            frame = ttk.Frame(shop_container, padding="5")
            frame.pack(fill=tk.X, pady=2)
            info = f"{crate['name']} - Cost: {crate['cost']:,} Coins\n(Luck Pool: {crate['luck_range'][0]}-{crate['luck_range'][1]})"
            ttk.Label(frame, text=info).pack(side=tk.LEFT)
            
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(side=tk.RIGHT)
            
            ttk.Button(btn_frame, text=f"Buy 1", command=lambda l=level: self.buy_crate(l, 1)).pack(side=tk.LEFT, padx=2)
            ttk.Button(btn_frame, text=f"Buy 5", command=lambda l=level: self.buy_crate(l, 5)).pack(side=tk.LEFT, padx=2)
            ttk.Button(btn_frame, text=f"Buy 10", command=lambda l=level: self.buy_crate(l, 10)).pack(side=tk.LEFT, padx=2)

    def setup_inv_tab(self):
        columns = ("Select", "Name", "Rarity", "Quantity", "Value (Each)")
        self.inv_tree = ttk.Treeview(self.inv_tab, columns=columns, show="headings", selectmode="none")
        self.inv_tree.heading("Select", text="[ ]")
        self.inv_tree.column("Select", width=50, anchor=tk.CENTER)
        for col in columns[1:]:
            self.inv_tree.heading(col, text=col)
            self.inv_tree.column(col, width=150, anchor=tk.CENTER)
        self.inv_tree.pack(fill=tk.BOTH, expand=True)
        self.inv_tree.bind("<ButtonRelease-1>", self.on_tree_click)
        
        ctrl_frame = ttk.Frame(self.inv_tab, padding="5")
        ctrl_frame.pack(fill=tk.X)
        self.sell_selected_btn = ttk.Button(ctrl_frame, text="Sell Selected (0 items)", command=self.sell_selected)
        self.sell_selected_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(ctrl_frame, text="Select All", command=self.select_all_inv).pack(side=tk.LEFT, padx=5)
        ttk.Button(ctrl_frame, text="Deselect All", command=self.deselect_all_inv).pack(side=tk.LEFT, padx=5)
        self.bonus_label = ttk.Label(ctrl_frame, text="Batch Bonus: +0%", foreground=ACCENT_GREEN)
        self.bonus_label.pack(side=tk.RIGHT, padx=10)

    def on_tree_click(self, event):
        item_id = self.inv_tree.identify_row(event.y)
        if not item_id: return
        name = self.inv_tree.item(item_id)['values'][1]
        if name in self.selected_items: self.selected_items.remove(name)
        else: self.selected_items.add(name)
        self.refresh_inventory_display()
        self.update_sell_button_text()

    def select_all_inv(self):
        for name, qty in self.inventory.items():
            if qty > 0: self.selected_items.add(name)
        self.refresh_inventory_display()
        self.update_sell_button_text()

    def deselect_all_inv(self):
        self.selected_items.clear()
        self.refresh_inventory_display()
        self.update_sell_button_text()

    def update_sell_button_text(self):
        count = sum(self.inventory.get(name, 0) for name in self.selected_items)
        bonus_pct = min(100, count // 5)
        self.sell_selected_btn.config(text=f"Sell Selected ({count} items)")
        self.bonus_label.config(text=f"Batch Bonus: +{bonus_pct}%")

    def setup_craft_tab(self):
        canvas = tk.Canvas(self.craft_tab, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.craft_tab, orient="vertical", command=canvas.yview)
        self.craft_scroll_frame = ttk.Frame(canvas)
        self.craft_scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.craft_scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.refresh_crafting()

    def get_recipe_completion(self, recipe):
        total_req = sum(recipe['req'].values())
        total_have = sum(min(self.inventory.get(k, 0), v) for k, v in recipe['req'].items())
        return (total_have / total_req) * 100

    def refresh_crafting(self):
        for widget in self.craft_scroll_frame.winfo_children():
            widget.destroy()
        sorted_recipes = sorted(CRAFTING_RECIPES, key=lambda r: self.get_recipe_completion(r), reverse=True)
        for recipe in sorted_recipes:
            completion = self.get_recipe_completion(recipe)
            frame = ttk.LabelFrame(self.craft_scroll_frame, text=f"Craft: {recipe['result']} ({completion:.0f}%)", padding="10")
            frame.pack(fill=tk.X, pady=5, padx=5)
            req_text = "Requires: " + ", ".join([f"{v}x {k}" for k, v in recipe['req'].items()])
            have_text = "You have: " + ", ".join([f"{self.inventory.get(k, 0)}x {k}" for k in recipe['req'].keys()])
            ttk.Label(frame, text=f"{req_text}\n{have_text}").pack(side=tk.LEFT)
            can_craft = all(self.inventory.get(k, 0) >= v for k, v in recipe['req'].items())
            btn_state = tk.NORMAL if can_craft else tk.DISABLED
            ttk.Button(frame, text="Craft", state=btn_state, command=lambda r=recipe: self.craft_item(r)).pack(side=tk.RIGHT)

    def log(self, message):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def update_status(self):
        self.coin_label.config(text=f"Coins: {self.coins:,.0f}")
        self.mine_info_label.config(text=f"Mine Lvl: {self.mine_level} (+{self.mine_shard_bonus} Shard Bonus)")
        upgrade_cost = self.mine_level * 1000
        self.upgrade_mine_btn.config(text=f"Upgrade Mine ({upgrade_cost:,})")
        self.refresh_inventory_display()
        self.refresh_crafting()
        self.update_sell_button_text()

    def refresh_inventory_display(self):
        for item in self.inv_tree.get_children():
            self.inv_tree.delete(item)
        active_inventory = {k: v for k, v in self.inventory.items() if v > 0}
        sorted_items = sorted(active_inventory.items(), key=lambda x: self._get_item_sell_value(x[0]), reverse=True)
        for name, qty in sorted_items:
            data = self.item_data[name]
            val = self._get_item_sell_value(name)
            mark = "[X]" if name in self.selected_items else "[ ]"
            self.inv_tree.insert("", tk.END, values=(mark, name, data['rarity'], qty, f"{val:,}"))

    def _get_item_sell_value(self, item_name):
        data = self.item_data.get(item_name)
        if not data: return 0
        return round(data['base_value'] * RARITIES[data['rarity']]['multiplier'])

    def mine(self):
        if self.is_opening: return
        total_gain = self.mine_level + (self.inventory.get("Mine-Shard", 0) * 10 * self.mine_level)
        self.coins += total_gain
        self.log(f"⛏️ Mined {total_gain} coins.")
        self.update_status()

    def upgrade_mine(self):
        if self.is_opening: return
        cost = self.mine_level * 1000
        if self.coins >= cost:
            self.coins -= cost
            self.mine_level += 1
            self.log(f"⚒️ Mine upgraded to Level {self.mine_level}!")
            self.update_status()
        else:
            messagebox.showwarning("Upgrade", f"You need {cost:,} coins!")

    def buy_crate(self, level, count):
        if self.is_opening: return
        crate = CRATES[level]
        total_cost = crate['cost'] * count
        if self.coins < total_cost:
            messagebox.showwarning("Insufficient Funds", f"You need {total_cost:,} coins!")
            return
        self.coins -= total_cost
        self.is_opening = True
        self.animate_crate(crate, count)

    def animate_crate(self, crate, count):
        self.anim_label.config(text=f"Opening {count}x {crate['name']}...")
        self.root.update()
        
        colors = ["#FFFFFF", ACCENT_GREEN, "#FF00FF", "#00FFFF"]
        for i in range(10):
            self.anim_label.config(foreground=random.choice(colors))
            self.root.after(100)
            self.root.update()
            
        total_items_gained = {}
        for _ in range(count):
            luck_pool = random.randint(crate['luck_range'][0], crate['luck_range'][1])
            while luck_pool >= 10: # Minimum cost for Common
                rarities = list(crate['weights'].keys())
                weights = list(crate['weights'].values())
                dropped_rarity = random.choices(rarities, weights=weights, k=1)[0]
                
                # If luck pool can't afford it, try to downgrade or stop
                if luck_pool < RARITIES[dropped_rarity]['luck_cost']:
                    # Try to find a rarity we can afford
                    affordable = [r for r, d in RARITIES.items() if d['luck_cost'] <= luck_pool]
                    if not affordable: break
                    dropped_rarity = random.choice(affordable)
                
                possible_drops = [item for item in ITEMS_LIST if item['rarity'] == dropped_rarity and item['name'] not in [r['result'] for r in CRAFTING_RECIPES]]
                if possible_drops:
                    dropped_item = random.choice(possible_drops)
                    name = dropped_item['name']
                    self.inventory[name] = self.inventory.get(name, 0) + 1
                    total_items_gained[name] = total_items_gained.get(name, 0) + 1
                    luck_pool -= RARITIES[dropped_rarity]['luck_cost']
                else:
                    break
        
        if total_items_gained:
            best_item = max(total_items_gained.keys(), key=lambda x: self._get_item_sell_value(x))
            self.anim_label.config(text=f"BEST: {best_item}!", foreground=RARITIES[self.item_data[best_item]['rarity']]['color'])
            self.log(f"📦 Opened {count}x {crate['name']}! Found {sum(total_items_gained.values())} items.")
        else:
            self.anim_label.config(text="Nothing found...", foreground="red")
            
        self.is_opening = False
        self.update_status()

    def sell_selected(self):
        if self.is_opening: return
        if not self.selected_items:
            messagebox.showinfo("Selection", "No items selected to sell.")
            return
        total_base_val = 0
        total_items = 0
        for name in list(self.selected_items):
            qty = self.inventory.get(name, 0)
            if qty > 0:
                total_base_val += self._get_item_sell_value(name) * qty
                total_items += qty
                self.inventory[name] = 0
        if total_items > 0:
            bonus_pct = min(100, total_items // 5)
            final_val = total_base_val * (1 + bonus_pct / 100)
            self.coins += final_val
            self.log(f"💰 Sold {total_items} items for {final_val:,.0f} coins! (+{bonus_pct}% bonus)")
            self.selected_items.clear()
            self.update_status()

    def craft_item(self, recipe):
        if self.is_opening: return
        for k, v in recipe['req'].items():
            self.inventory[k] -= v
        self.inventory[recipe['result']] = self.inventory.get(recipe['result'], 0) + 1
        self.log(f"✨ Crafted {recipe['result']}!")
        self.update_status()

if __name__ == "__main__":
    root = tk.Tk()
    app = CrateGameGUI(root)
    root.mainloop()
