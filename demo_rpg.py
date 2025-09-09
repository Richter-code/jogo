#!/usr/bin/env python3
"""
Demonstração rápida do jogo RPG para mostrar interface
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpg_game import Player, Enemy, Game

def demo_game():
    """Demonstra o funcionamento do jogo"""
    print("🗡️ DEMO - Jogo de RPG 🗡️")
    print("=" * 40)
    
    # Cria jogador
    player = Player("Herói Demo")
    print(f"Personagem criado: {player.name}")
    
    # Mostra status inicial
    player.show_status()
    
    # Mostra inventário
    player.show_inventory()
    
    # Simula combate
    print("\n" + "=" * 40)
    print("SIMULAÇÃO DE COMBATE")
    print("=" * 40)
    
    enemy = Enemy("Goblin", 40, 15, 2, 25, 15)
    print(f"Inimigo: {enemy.name}")
    print(f"Vida do inimigo: {enemy.health} HP")
    
    # Simula alguns ataques
    for round_num in range(1, 4):
        print(f"\n--- Round {round_num} ---")
        
        # Jogador ataca
        damage = player.attack_enemy(enemy)
        print(f"{player.name} atacou {enemy.name} causando {damage} de dano!")
        print(f"{enemy.name} vida restante: {enemy.health}")
        
        if not enemy.is_alive():
            print(f"\n🎉 {enemy.name} foi derrotado!")
            player.gain_experience(enemy.experience_reward)
            player.gold += enemy.gold_reward
            print(f"💰 Ouro ganho: {enemy.gold_reward}")
            break
            
        # Inimigo ataca
        damage = enemy.attack_enemy(player)
        print(f"{enemy.name} atacou {player.name} causando {damage} de dano!")
        print(f"{player.name} vida restante: {player.health}")
        
        if not player.is_alive():
            print(f"\n💀 {player.name} foi derrotado!")
            break
    
    # Status final
    print("\n" + "=" * 40)
    print("STATUS FINAL")
    print("=" * 40)
    player.show_status()
    
    print("\n✅ Demo concluída com sucesso!")
    print("Para jogar, execute: python3 rpg_game.py")

if __name__ == "__main__":
    demo_game()