class Player:
    def __init__(self, id, name, level, HP, weapon, armor):
        self.id = id
        self.name = name
        self.level = level
        self.HP = HP
        self.weapon = weapon
        self.armor = armor
        self.guild = None

    def attack(self):
        pass

    def player_info(self):
        print(f"=== Player{self.id} ===")
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print(f"HP: {self.HP}")
        print(f"Weapon: {self.weapon.name} (Damage: {self.weapon.damage})")
        print(f"Armor: {self.armor.name} (Defense: {self.armor.defense})")
        print(f"Guild: {self.guild}")     


class Weapon:
    def __init__(self, id, name, damage):
        self.id = id
        self.name = name
        self.damage = damage

    def special_attack(self):
        pass
        
class Armor:
    def __init__(self, id, name, defense):
        self.id = id
        self.name = name
        self.defense = defense

    def special_defense(self):
        pass

class Guild:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.leader = None
        self.member_list = []

    def join(self, player):
        if self.leader == None:
            self.leader = player.name
        else:
            self.member_list.append(player)
        player.guild = self.name

    def guild_info(self):
        print(f"### Guild {self.name} ###")
        print(f"Name: {self.name}")
        print(f"Leader: {self.leader}")
        print(f"Member:")
        for player in self.member_list:
            print(f" - {player.name}")

woodenSword1 = Weapon(1, "Wooden Sword", 10)
woodenSword2 = Weapon(2, "Wooden Sword", 10)
ironSword1 = Weapon(3, "Iron Sword", 15)
ironSword2 = Weapon(4, "Iron Sword", 15)

woodenArmor1 = Armor(1, "Wooden Armor", 4)
woodenArmor2 = Armor(2, "Wooden Armor", 4)
ironArmor1 = Armor(3, "Iron Armor", 8)
ironArmor2 = Armor(4, "Iron Armor", 8)

player1 = Player(1, "Welt Yang", 1, 100, woodenSword1, woodenArmor1)
player2 = Player(2, "Otto Apocalypse", 5, 150, ironSword2 ,ironArmor2)

guild1 = Guild(1, "StarRail")
guild1.join(player1)
guild1.join(player2)

player1.player_info()
print()
player2.player_info()
print("\n-----------------------------------\n")
guild1.guild_info()