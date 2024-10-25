import json

'''class Player:

    # 建構子 => 建構Class用
    def __init__(self, cursor, name):
        # self == this(?
        self.cursor = cursor
        self.name = name
        self.inventory = {"weapons": [], "potions": 0}
        self.load_player()

    def load_player(self):
        player_data = self.get_player()
        if player_data:
            self.inventory = json.loads(player_data[2])  # 假設 inventory 在第三列
        else:
            self.add_player()

    def add_player(self):
        inventory_json = json.dumps(self.inventory)
        self.cursor.execute("INSERT INTO player (name, inventory) VALUES (?, ?)", (self.name, inventory_json))
        self.cursor.connection.commit()

    def get_player(self):
        self.cursor.execute("SELECT * FROM player WHERE name = ?", (self.name,))
        return self.cursor.fetchone()

    def update_inventory(self, weapon=None, potions=0):
        if weapon:
            self.inventory["weapons"].append(weapon)
        self.inventory["potions"] += potions
        
        self.cursor.execute("UPDATE player SET inventory = ? WHERE name = ?", (json.dumps(self.inventory), self.name))
        self.cursor.connection.commit()

        print(f"{self.name} 的物品清單已更新：{self.inventory}")

    def show_inventory(self):
        print(f"{self.name} 的物品清單：{self.inventory}")
'''
def add_player(cursor, name):
    inventory = json.dumps({"weapons": [], "potions": 0})
    cursor.execute("INSERT INTO player (name, inventory) VALUES (?, ?)", (name, inventory))
    cursor.connection.commit()

def get_player(cursor, name):
    cursor.execute("SELECT * FROM player WHERE name = ?", (name,))
    return cursor.fetchone()

def update_inventory(cursor, name, weapon=None, potions=0):
    # 檢查玩家是否已存在，同時獲得此player cursor.fetchone()
    player_data = get_player(cursor, name)  # 使用 player 前綴
    # 獲取列名
    column_names = [description[0] for description in cursor.description]
    # 將 player_data 轉換為字典
    player_dict = dict(zip(column_names, player_data))

    if player_data:
    # 獲取 inventory 資料
        inventory = json.loads(player_dict['inventory']) # 使用列名稱而不是索引
        # inventory = json.loads(player_data[2])# inventory create時在第三個位置
        if weapon:
            inventory["weapons"].append(weapon)
        inventory["potions"] += potions
        
        cursor.execute("UPDATE player SET inventory = ? WHERE name = ?", (json.dumps(inventory), name))
        cursor.connection.commit()

        print(f"{name} 的物品清單已更新：{inventory}")
    # else:
    #     print("玩家不存在！")

def del_player(cursor, name):
    cursor.execute("DELETE FROM player WHERE name = ?", (name,))
    cursor.connection.commit()  
    print(f"玩家 {name} 已被删除。")

def show_inventory(cursor, name):
    player = get_player(cursor, name)
    if player:
        inventory = json.loads(player[2])
        print(f"{name} 的物品清單：{inventory}")
    # else:
    #     print("玩家不存在！")

def show_all_players(cursor):
    print("---------------")
    cursor.execute("SELECT name FROM player")  # 執行查詢
    all_players = cursor.fetchall()
    # 印所有玩家的名字
    for i, player in enumerate(all_players, start=1):  # enmerate
        print(f'{i}: {player[0]}')  # player 是一個元組，名字在第一個位置