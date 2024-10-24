import sqlite3
import json

# 創建或連接到 SQLite 資料庫
conn = sqlite3.connect('game.db')
cursor = conn.cursor()

# 創建玩家表格
cursor.execute('''
CREATE TABLE IF NOT EXISTS player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    inventory TEXT
)
''')
conn.commit()

def add_player(name):
    # 初始化玩家的物品清單為空 JSON
    inventory = json.dumps({"weapons": [], "potions": 0})
    cursor.execute("INSERT INTO player (name, inventory) VALUES (?, ?)", (name, inventory))
    conn.commit()

def get_player(name):
    cursor.execute("SELECT * FROM player WHERE name = ?", (name,))
    return cursor.fetchone()

def update_inventory(name, weapon=None, potions=0):
    player = get_player(name)
    if player:
        inventory = json.loads(player[2])  # 解析 JSON
        if weapon:
            inventory["weapons"].append(weapon)
        inventory["potions"] += potions
        
        # 更新玩家的物品清單
        cursor.execute("UPDATE player SET inventory = ? WHERE name = ?", (json.dumps(inventory), name))
        conn.commit()
        print(f"{name} 的物品清單已更新：{inventory}")
    else:
        print("玩家不存在！")

def show_inventory(name):
    player = get_player(name)
    if player:
        inventory = json.loads(player[2])
        print(f"{name} 的物品清單：{inventory}")
    else:
        print("玩家不存在！")

# 主遊戲邏輯
def main():
    print("歡迎來到簡易 RPG 遊戲！")
    player_name = input("請輸入你的名字：")
    add_player(player_name)
    
    while True:
        action = input("你想做什麼？(1: 獲得武器, 2: 獲得藥水, 3: 查看物品清單, 4: 退出) ")
        
        if action == '1':
            weapon = input("請輸入獲得的武器名稱：")
            update_inventory(player_name, weapon=weapon)
        elif action == '2':
            potions = int(input("請輸入獲得的藥水數量："))
            update_inventory(player_name, potions=potions)
        elif action == '3':
            show_inventory(player_name)
        elif action == '4':
            print("再見！")
            break
        else:
            print("無效的選擇，請重新輸入！")

if __name__ == "__main__":
    main()

# 關閉資料庫連接
conn.close()
