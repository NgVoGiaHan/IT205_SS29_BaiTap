from abc import ABC, abstractmethod

class BaseCharacter(ABC):
    def __init__(self, hp):
        self.__base_hp = int(hp)

    @property
    def base_hp(self):
        return self.__base_hp

    @abstractmethod
    def attack_enemy(self):
        pass

    def __add__(self, other):
        if isinstance(other, BaseCharacter) or hasattr(other, 'base_hp'):
            return self.base_hp + other.base_hp
        return self.base_hp + int(other)

class MagicalStance:
    def attack_enemy(self):
        return 150.0

class Warrior(BaseCharacter):
    def __init__(self, hp, strength):
        super().__init__(hp)
        self.strength = float(strength)

    def attack_enemy(self):
        return self.strength * 2.5

class Spellblade(Warrior, MagicalStance):
    def __init__(self, hp, strength):
        super().__init__(hp, strength)

    def attack_enemy(self):
        warrior_dmg = Warrior.attack_enemy(self)
        magic_dmg = MagicalStance.attack_enemy(self)
        return warrior_dmg + magic_dmg

class VolcanoZone:
    def activate_buff(self, character):
        print("Sức nóng dung nham kích hoạt! Gia tăng +20% sát thương cho Warrior!")

def apply_battleground_effect(environment, character):
    environment.activate_buff(character)

def main():
    current_hero = None

    while True:
        print("\n===== RPG GAME CORE MENU =====")
        print("1. Khởi tạo Ma kiếm sĩ Spellblade & Xem cấu trúc MRO")
        print("2. Ra lệnh tấn công & Kích hoạt chiến trường (Duck Typing)")
        print("3. Thoát")

        choice = input("Chọn chức năng (1-2): ").strip()

        match choice:
            case '1':
                print("--- KHỞI TẠO MA KIẾM SĨ SPELLBLADE ---")
                hp_input = input("Nhập lượng máu cơ bản (HP): ")
                str_input = input("Nhập chỉ số sức mạnh (Strength): ")

                current_hero = Spellblade(hp_input, str_input)
                print("\nKhởi tạo nhân vật Spellblade thành công!")

                mro_list = " -> ".join([cls.__name__ for cls in Spellblade.__mro__])
                print(f"[MRO Architecture]: {mro_list}")

                total_hp = current_hero + current_hero
                print(f"[Overloading __add__]: Tổng HP tích lũy khi gộp đội hình: {total_hp}")

            case '2':
                if current_hero is None:
                    print("Vui lòng khởi tạo nhân vật trước!")
                else:
                    print("--- THI THIẾT KẾ GIAO TRANH & DUCK TYPING ---")
                    total_dmg = current_hero.attack_enemy()
                    print(f"[Đa hình]: Spellblade vung kiếm ma thuật gây tổng sát thương: {total_dmg} DMG")

                    volcano = VolcanoZone()
                    apply_battleground_effect(volcano, current_hero)
                    print("[Duck Typing]: Xác thực môi trường trận đấu thành công!")

            case _:
                print("Thoát chương trình")
                break

if __name__ == "__main__":
    main()