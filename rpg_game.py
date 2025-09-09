#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jogo de RPG Simples
Um jogo de RPG básico em texto com combate, inventário e progressão.
"""

import random
import os
import time

class Character:
    """Classe base para personagens (jogador e inimigos)"""
    
    def __init__(self, name, health, attack, defense, level=1):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.level = level
        self.experience = 0
        self.experience_to_next_level = 100
        
    def is_alive(self):
        return self.health > 0
        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.health = max(0, self.health - actual_damage)
        return actual_damage
        
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
        
    def attack_enemy(self, enemy):
        damage = random.randint(self.attack - 5, self.attack + 5)
        damage = max(1, damage)
        actual_damage = enemy.take_damage(damage)
        return actual_damage

class Player(Character):
    """Classe do jogador com inventário e sistema de level"""
    
    def __init__(self, name):
        super().__init__(name, health=100, attack=20, defense=5, level=1)
        self.inventory = {
            'Poção de Vida': 3,
            'Poção de Mana': 2
        }
        self.gold = 50
        
    def gain_experience(self, exp):
        self.experience += exp
        print(f"Você ganhou {exp} pontos de experiência!")
        
        while self.experience >= self.experience_to_next_level:
            self.level_up()
            
    def level_up(self):
        self.experience -= self.experience_to_next_level
        self.level += 1
        
        # Aumenta atributos
        health_increase = random.randint(10, 20)
        attack_increase = random.randint(3, 7)
        defense_increase = random.randint(1, 3)
        
        self.max_health += health_increase
        self.health = self.max_health  # Cura completa no level up
        self.attack += attack_increase
        self.defense += defense_increase
        
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)
        
        print(f"\n🎉 LEVEL UP! Você subiu para o nível {self.level}!")
        print(f"💪 Vida: +{health_increase} (Total: {self.max_health})")
        print(f"⚔️ Ataque: +{attack_increase} (Total: {self.attack})")
        print(f"🛡️ Defesa: +{defense_increase} (Total: {self.defense})")
        print(f"Próximo nível: {self.experience_to_next_level} EXP")
        
    def use_item(self, item_name):
        if item_name in self.inventory and self.inventory[item_name] > 0:
            self.inventory[item_name] -= 1
            
            if item_name == 'Poção de Vida':
                heal_amount = random.randint(30, 50)
                self.heal(heal_amount)
                print(f"Você usou uma Poção de Vida e recuperou {heal_amount} pontos de vida!")
                return True
            elif item_name == 'Poção de Mana':
                self.attack += 5  # Boost temporário de ataque
                print(f"Você usou uma Poção de Mana! Seu ataque aumentou temporariamente!")
                return True
        else:
            print(f"Você não tem {item_name} no inventário!")
            return False
    
    def show_status(self):
        print(f"\n📊 Status de {self.name}")
        print(f"Nível: {self.level}")
        print(f"❤️ Vida: {self.health}/{self.max_health}")
        print(f"⚔️ Ataque: {self.attack}")
        print(f"🛡️ Defesa: {self.defense}")
        print(f"⭐ EXP: {self.experience}/{self.experience_to_next_level}")
        print(f"💰 Ouro: {self.gold}")
        
    def show_inventory(self):
        print(f"\n🎒 Inventário de {self.name}")
        print(f"💰 Ouro: {self.gold}")
        print("Itens:")
        for item, quantity in self.inventory.items():
            print(f"  - {item}: {quantity}")

class Enemy(Character):
    """Classe para inimigos"""
    
    def __init__(self, name, health, attack, defense, experience_reward, gold_reward):
        super().__init__(name, health, attack, defense)
        self.experience_reward = experience_reward
        self.gold_reward = gold_reward

class Game:
    """Classe principal do jogo"""
    
    def __init__(self):
        self.player = None
        self.enemies = [
            Enemy("Goblin", 40, 15, 2, 25, 15),
            Enemy("Orc", 60, 20, 4, 40, 25),
            Enemy("Esqueleto", 50, 18, 3, 35, 20),
            Enemy("Lobo", 45, 22, 1, 30, 10),
            Enemy("Bandido", 70, 25, 5, 50, 35),
            Enemy("Dragão Jovem", 120, 35, 8, 100, 75),
        ]
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def pause(self):
        input("\nPressione Enter para continuar...")
        
    def create_character(self):
        self.clear_screen()
        print("🗡️ Bem-vindo ao RPG Adventure! 🗡️")
        print("=" * 40)
        
        name = input("Digite o nome do seu personagem: ").strip()
        if not name:
            name = "Aventureiro"
            
        self.player = Player(name)
        print(f"\nPersonagem {name} criado com sucesso!")
        print(f"Você começa sua jornada como um aventureiro nível 1.")
        self.pause()
        
    def combat(self, enemy):
        print(f"\n⚔️ Um {enemy.name} selvagem apareceu!")
        print(f"❤️ {enemy.name}: {enemy.health} HP")
        
        while self.player.is_alive() and enemy.is_alive():
            print(f"\n--- Turno de Combate ---")
            print(f"❤️ Sua vida: {self.player.health}/{self.player.max_health}")
            print(f"❤️ {enemy.name}: {enemy.health} HP")
            
            print("\nO que você quer fazer?")
            print("1. Atacar")
            print("2. Usar item")
            print("3. Fugir")
            
            choice = input("Escolha uma opção (1-3): ").strip()
            
            if choice == "1":
                # Jogador ataca
                damage = self.player.attack_enemy(enemy)
                print(f"Você atacou {enemy.name} e causou {damage} de dano!")
                
                if not enemy.is_alive():
                    print(f"\n🎉 Você derrotou {enemy.name}!")
                    self.player.gain_experience(enemy.experience_reward)
                    self.player.gold += enemy.gold_reward
                    print(f"💰 Você ganhou {enemy.gold_reward} moedas de ouro!")
                    return True
                    
            elif choice == "2":
                print("\nItens disponíveis:")
                for item, qty in self.player.inventory.items():
                    if qty > 0:
                        print(f"- {item} ({qty})")
                
                item_choice = input("Digite o nome do item: ").strip()
                if not self.player.use_item(item_choice):
                    continue  # Não perde o turno se não conseguir usar o item
                    
            elif choice == "3":
                if random.random() < 0.7:  # 70% chance de fugir
                    print("Você fugiu com sucesso!")
                    return False
                else:
                    print("Você não conseguiu fugir!")
            else:
                print("Opção inválida!")
                continue
                
            # Inimigo ataca
            if enemy.is_alive():
                damage = enemy.attack_enemy(self.player)
                print(f"{enemy.name} te atacou e causou {damage} de dano!")
                
                if not self.player.is_alive():
                    print(f"\n💀 Você foi derrotado por {enemy.name}...")
                    return False
                    
        return True
        
    def random_encounter(self):
        if random.random() < 0.6:  # 60% chance de encontro
            enemy = random.choice(self.enemies).copy()
            # Cria uma nova instância do inimigo
            enemy = Enemy(enemy.name, enemy.max_health, enemy.attack, 
                         enemy.defense, enemy.experience_reward, enemy.gold_reward)
            return self.combat(enemy)
        else:
            events = [
                "Você encontrou uma pequena bolsa com moedas! (+10 ouro)",
                "Você encontrou uma poção abandonada!",
                "Uma brisa fresca restaura um pouco da sua energia. (+5 HP)",
                "Você não encontrou nada interessante por aqui."
            ]
            event = random.choice(events)
            print(f"\n🗺️ {event}")
            
            if "moedas" in event:
                self.player.gold += 10
            elif "poção" in event:
                self.player.inventory['Poção de Vida'] += 1
            elif "energia" in event:
                self.player.heal(5)
                
            return True
            
    def main_menu(self):
        while True:
            self.clear_screen()
            print(f"🗡️ RPG Adventure - {self.player.name} 🗡️")
            print("=" * 40)
            print("1. Explorar área")
            print("2. Ver status")
            print("3. Ver inventário")
            print("4. Descansar (recuperar vida)")
            print("5. Sair do jogo")
            
            choice = input("\nEscolha uma opção (1-5): ").strip()
            
            if choice == "1":
                print("\n🗺️ Você decide explorar a área...")
                time.sleep(1)
                if not self.random_encounter():
                    if not self.player.is_alive():
                        print("\n💀 GAME OVER 💀")
                        print("Obrigado por jogar!")
                        break
                self.pause()
                
            elif choice == "2":
                self.player.show_status()
                self.pause()
                
            elif choice == "3":
                self.player.show_inventory()
                self.pause()
                
            elif choice == "4":
                cost = 20
                if self.player.gold >= cost:
                    self.player.gold -= cost
                    self.player.health = self.player.max_health
                    print(f"\n🏠 Você descansou em uma taverna e recuperou toda sua vida!")
                    print(f"💰 Custo: {cost} moedas de ouro")
                else:
                    print(f"\n❌ Você precisa de {cost} moedas de ouro para descansar.")
                self.pause()
                
            elif choice == "5":
                print("\nObrigado por jogar RPG Adventure!")
                break
                
            else:
                print("Opção inválida!")
                self.pause()
                
    def run(self):
        self.create_character()
        self.main_menu()

if __name__ == "__main__":
    game = Game()
    game.run()