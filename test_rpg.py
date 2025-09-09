#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste básico para o jogo RPG
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpg_game import Player, Enemy, Game

def test_character_creation():
    """Testa criação de personagem"""
    print("Testando criação de personagem...")
    player = Player("Teste")
    assert player.name == "Teste"
    assert player.health == 100
    assert player.max_health == 100
    assert player.level == 1
    assert player.is_alive() == True
    print("✅ Criação de personagem OK")

def test_combat_mechanics():
    """Testa mecânicas de combate"""
    print("Testando combate...")
    player = Player("Herói")
    enemy = Enemy("Goblin", 40, 15, 2, 25, 15)
    
    # Testa ataque
    initial_enemy_health = enemy.health
    damage = player.attack_enemy(enemy)
    assert enemy.health < initial_enemy_health
    assert damage > 0
    print("✅ Sistema de ataque OK")
    
    # Testa receber dano
    initial_player_health = player.health
    damage = enemy.attack_enemy(player)
    assert player.health < initial_player_health
    assert damage > 0
    print("✅ Sistema de dano OK")

def test_inventory_system():
    """Testa sistema de inventário"""
    print("Testando inventário...")
    player = Player("Herói")
    
    # Testa uso de poção
    initial_health = player.health
    player.health = 50  # Simula dano
    
    initial_potions = player.inventory['Poção de Vida']
    success = player.use_item('Poção de Vida')
    
    assert success == True
    assert player.inventory['Poção de Vida'] == initial_potions - 1
    assert player.health > 50
    print("✅ Sistema de inventário OK")

def test_level_system():
    """Testa sistema de level"""
    print("Testando sistema de level...")
    player = Player("Herói")
    
    initial_level = player.level
    initial_attack = player.attack
    initial_defense = player.defense
    initial_max_health = player.max_health
    
    # Simula ganho de experiência suficiente para subir de nível
    player.gain_experience(100)
    
    assert player.level > initial_level
    assert player.attack > initial_attack
    assert player.defense > initial_defense
    assert player.max_health > initial_max_health
    print("✅ Sistema de level OK")

def test_enemy_creation():
    """Testa criação de inimigos"""
    print("Testando criação de inimigos...")
    enemy = Enemy("Orc", 60, 20, 4, 40, 25)
    
    assert enemy.name == "Orc"
    assert enemy.health == 60
    assert enemy.attack == 20
    assert enemy.defense == 4
    assert enemy.experience_reward == 40
    assert enemy.gold_reward == 25
    print("✅ Criação de inimigos OK")

def run_all_tests():
    """Executa todos os testes"""
    print("🧪 Iniciando testes do jogo RPG...\n")
    
    try:
        test_character_creation()
        test_combat_mechanics()
        test_inventory_system()
        test_level_system()
        test_enemy_creation()
        
        print("\n🎉 Todos os testes passaram com sucesso!")
        print("O jogo está funcionando corretamente!")
        
    except Exception as e:
        print(f"\n❌ Erro nos testes: {e}")
        return False
        
    return True

if __name__ == "__main__":
    run_all_tests()