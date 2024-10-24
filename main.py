import sqlite3
import player

# 創建或連接到 SQLite 資料庫
conn = sqlite3.connect('game.db')
cursor = conn.cursor()

# cursor.execute("SQL語法")

# 創建玩家表格 ('''多行字串''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    inventory TEXT
)
''')
conn.commit()


# 主遊戲邏輯
def main():
    print("歡迎來到簡易 RPG 遊戲！")
    # 使用 fetchall() 獲取所有結果
    All_players = cursor.fetchall()

    # 打印所有玩家的名字
    for players in All_players:
        print(players[0])  # player 是一個元組，名字在第一個位置

    # 選擇或創建玩家
    player_name = input("你是？ ")
    
    # 檢查玩家是否已存在，同時獲得此player cursor.fetchone()
    player_data = player.get_player(cursor, player_name)  # 使用 player 前綴
    
    if player_data:
        print(f"歡迎回來，{player_name}！")
    else:
        check = input("即將創建新玩家，輸入yes繼續： ")
        if (check=="yes"):
            print(f"新玩家 {player_name} 創建成功！")
            player.add_player(cursor, player_name)
            conn.commit()
        else:
            print("遊戲結束~")
            exit()
    
    while True:
        action = input("你想做什麼？(1: 獲得武器, 2: 獲得藥水, 3: 查看物品清單, 4: 退出) ")

        try:
            if action == '1':
                while True:
                    weapon = input("請輸入獲得的武器名稱：")
                    if not weapon.strip():
                        print("武器名稱不能為空！")
                        continue
                    break
                player.update_inventory(cursor, player_name, weapon=weapon)  # player.py 處理append
                print(f"武器 {weapon} 已添加！")
            elif action == '2':
                
                while True:
                    try:
                        potions = int(input("請輸入獲得的藥水數量："))
                        if potions < 0:
                            print("數量不能為負數！")
                            continue
                        elif potions > 0:
                            print(f"已獲得 {potions} 瓶藥水！")
                        else:print(f"沒有獲得藥水...")
                        break
                    except ValueError:
                        print("請輸入一個有效的整數！")
                player.update_inventory(cursor, player_name, potions=potions) # player.py處理運算
            elif action == '3':
                player.show_inventory(cursor, player_name)
            elif action == '4':
                print("再見！")
                break
            else:
                print("無效的選擇，請重新輸入！")
        except Exception as e:
            print(f"發生錯誤：{e}")

if __name__ == "__main__":
    main()

# 關閉資料庫連接
conn.close()
