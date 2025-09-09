// Jogo RPG Pixel Art
// Core game engine and logic

class PixelArtRPG {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Disable image smoothing for pixel art
        this.ctx.imageSmoothingEnabled = false;
        this.ctx.webkitImageSmoothingEnabled = false;
        this.ctx.mozImageSmoothingEnabled = false;
        this.ctx.msImageSmoothingEnabled = false;
        
        // Game settings
        this.tileSize = 32;
        this.worldWidth = 25;
        this.worldHeight = 19;
        
        // Game state
        this.gameRunning = false;
        this.keys = {};
        
        // Player properties
        this.player = {
            x: 12,
            y: 9,
            health: 100,
            maxHealth: 100,
            level: 1,
            exp: 0,
            expToNext: 100,
            facing: 'down',
            moving: false,
            moveSpeed: 4,
            animFrame: 0,
            animTimer: 0
        };
        
        // World map (0 = grass, 1 = tree, 2 = rock, 3 = water)
        this.world = this.generateWorld();
        
        // Inventory
        this.inventory = new Array(16).fill(null);
        
        // Initialize game
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupUI();
        this.gameRunning = true;
        this.gameLoop();
    }
    
    setupEventListeners() {
        // Keyboard input
        document.addEventListener('keydown', (e) => {
            this.keys[e.key.toLowerCase()] = true;
            e.preventDefault();
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.key.toLowerCase()] = false;
            e.preventDefault();
        });
        
        // Canvas click for interactions
        this.canvas.addEventListener('click', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const x = Math.floor((e.clientX - rect.left) / this.tileSize);
            const y = Math.floor((e.clientY - rect.top) / this.tileSize);
            this.handleTileClick(x, y);
        });
    }
    
    setupUI() {
        // Generate inventory slots
        const inventoryGrid = document.getElementById('inventoryGrid');
        for (let i = 0; i < 16; i++) {
            const slot = document.createElement('div');
            slot.className = 'inventory-slot';
            slot.dataset.index = i;
            inventoryGrid.appendChild(slot);
        }
        
        this.updateUI();
    }
    
    generateWorld() {
        const world = [];
        for (let y = 0; y < this.worldHeight; y++) {
            world[y] = [];
            for (let x = 0; x < this.worldWidth; x++) {
                // Create a simple world with some variety
                let tile = 0; // Default grass
                
                // Add border trees
                if (x === 0 || x === this.worldWidth - 1 || y === 0 || y === this.worldHeight - 1) {
                    tile = 1; // Tree
                }
                // Random elements
                else if (Math.random() < 0.1) {
                    tile = Math.random() < 0.7 ? 1 : 2; // Tree or rock
                }
                // Water patches
                else if (Math.random() < 0.05) {
                    tile = 3; // Water
                }
                
                world[y][x] = tile;
            }
        }
        
        // Clear player spawn area
        for (let y = 8; y <= 10; y++) {
            for (let x = 11; x <= 13; x++) {
                world[y][x] = 0;
            }
        }
        
        return world;
    }
    
    update() {
        this.handleInput();
        this.updatePlayer();
        this.updateUI();
    }
    
    handleInput() {
        let dx = 0, dy = 0;
        
        // Movement controls
        if (this.keys['w'] || this.keys['arrowup']) {
            dy = -1;
            this.player.facing = 'up';
        }
        if (this.keys['s'] || this.keys['arrowdown']) {
            dy = 1;
            this.player.facing = 'down';
        }
        if (this.keys['a'] || this.keys['arrowleft']) {
            dx = -1;
            this.player.facing = 'left';
        }
        if (this.keys['d'] || this.keys['arrowright']) {
            dx = 1;
            this.player.facing = 'right';
        }
        
        // Try to move player
        if (dx !== 0 || dy !== 0) {
            this.movePlayer(dx, dy);
        } else {
            this.player.moving = false;
        }
        
        // Interaction
        if (this.keys[' ']) {
            this.interact();
            this.keys[' '] = false; // Prevent spam
        }
    }
    
    movePlayer(dx, dy) {
        const newX = this.player.x + dx;
        const newY = this.player.y + dy;
        
        // Check bounds and collision
        if (this.canMoveTo(newX, newY)) {
            this.player.x = newX;
            this.player.y = newY;
            this.player.moving = true;
            
            // Random encounter chance
            if (Math.random() < 0.02) {
                this.triggerRandomEvent();
            }
        }
    }
    
    canMoveTo(x, y) {
        // Check bounds
        if (x < 0 || x >= this.worldWidth || y < 0 || y >= this.worldHeight) {
            return false;
        }
        
        // Check tile collision (trees, rocks, water block movement)
        const tile = this.world[y][x];
        return tile === 0; // Only grass is walkable
    }
    
    updatePlayer() {
        // Update animation
        if (this.player.moving) {
            this.player.animTimer++;
            if (this.player.animTimer > 10) {
                this.player.animFrame = (this.player.animFrame + 1) % 2;
                this.player.animTimer = 0;
            }
        } else {
            this.player.animFrame = 0;
        }
    }
    
    interact() {
        // Check adjacent tiles for interaction
        const directions = [
            { x: 0, y: -1 }, // up
            { x: 0, y: 1 },  // down
            { x: -1, y: 0 }, // left
            { x: 1, y: 0 }   // right
        ];
        
        for (const dir of directions) {
            const checkX = this.player.x + dir.x;
            const checkY = this.player.y + dir.y;
            
            if (checkX >= 0 && checkX < this.worldWidth && 
                checkY >= 0 && checkY < this.worldHeight) {
                
                const tile = this.world[checkY][checkX];
                if (tile === 1) { // Tree
                    this.gatherResource('Madeira');
                    return;
                } else if (tile === 2) { // Rock
                    this.gatherResource('Pedra');
                    return;
                }
            }
        }
    }
    
    gatherResource(resourceName) {
        // Add to inventory
        for (let i = 0; i < this.inventory.length; i++) {
            if (this.inventory[i] === null) {
                this.inventory[i] = { name: resourceName, count: 1 };
                this.gainExp(5);
                this.showMessage(`Coletou: ${resourceName}!`);
                return;
            } else if (this.inventory[i].name === resourceName) {
                this.inventory[i].count++;
                this.gainExp(5);
                this.showMessage(`Coletou: ${resourceName} (${this.inventory[i].count})!`);
                return;
            }
        }
        this.showMessage('Inventário cheio!');
    }
    
    gainExp(amount) {
        this.player.exp += amount;
        if (this.player.exp >= this.player.expToNext) {
            this.levelUp();
        }
    }
    
    levelUp() {
        this.player.level++;
        this.player.exp = 0;
        this.player.expToNext = this.player.level * 100;
        this.player.maxHealth += 20;
        this.player.health = this.player.maxHealth;
        this.showMessage(`Subiu de nível! Nível ${this.player.level}!`);
    }
    
    triggerRandomEvent() {
        const events = [
            () => {
                this.showMessage('Você encontrou moedas!');
                this.gatherResource('Moedas');
            },
            () => {
                this.showMessage('Uma poção apareceu!');
                this.gatherResource('Poção');
            },
            () => {
                this.showMessage('Você se sente revigorado!');
                this.player.health = Math.min(this.player.maxHealth, this.player.health + 10);
            }
        ];
        
        const randomEvent = events[Math.floor(Math.random() * events.length)];
        randomEvent();
    }
    
    showMessage(text) {
        // Simple message system
        console.log(text);
        // You could add a proper message display system here
    }
    
    handleTileClick(x, y) {
        // Handle clicking on tiles
        if (Math.abs(x - this.player.x) <= 1 && Math.abs(y - this.player.y) <= 1) {
            const tile = this.world[y][x];
            if (tile === 1) {
                this.gatherResource('Madeira');
            } else if (tile === 2) {
                this.gatherResource('Pedra');
            }
        }
    }
    
    updateUI() {
        // Update health bar
        const healthPercent = (this.player.health / this.player.maxHealth) * 100;
        document.getElementById('healthBar').style.width = healthPercent + '%';
        document.getElementById('healthText').textContent = 
            `${this.player.health}/${this.player.maxHealth}`;
        
        // Update stats
        document.getElementById('playerLevel').textContent = this.player.level;
        document.getElementById('playerExp').textContent = 
            `${this.player.exp}/${this.player.expToNext}`;
        
        // Update inventory display
        const slots = document.querySelectorAll('.inventory-slot');
        slots.forEach((slot, index) => {
            const item = this.inventory[index];
            slot.className = 'inventory-slot';
            slot.textContent = '';
            
            if (item) {
                slot.classList.add('has-item');
                slot.textContent = item.name.charAt(0);
                slot.title = `${item.name} (${item.count})`;
            }
        });
    }
    
    render() {
        // Clear canvas
        this.ctx.fillStyle = '#2d5016';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw world
        this.drawWorld();
        
        // Draw player
        this.drawPlayer();
    }
    
    drawWorld() {
        for (let y = 0; y < this.worldHeight; y++) {
            for (let x = 0; x < this.worldWidth; x++) {
                const tile = this.world[y][x];
                this.drawTile(x, y, tile);
            }
        }
    }
    
    drawTile(x, y, tileType) {
        const pixelX = x * this.tileSize;
        const pixelY = y * this.tileSize;
        
        // Draw base grass
        this.ctx.fillStyle = '#4a7c59';
        this.ctx.fillRect(pixelX, pixelY, this.tileSize, this.tileSize);
        
        // Draw tile type
        switch (tileType) {
            case 0: // Grass
                this.drawGrass(pixelX, pixelY);
                break;
            case 1: // Tree
                this.drawTree(pixelX, pixelY);
                break;
            case 2: // Rock
                this.drawRock(pixelX, pixelY);
                break;
            case 3: // Water
                this.drawWater(pixelX, pixelY);
                break;
        }
    }
    
    drawGrass(x, y) {
        // Draw simple grass texture
        this.ctx.fillStyle = '#5d8a6b';
        for (let i = 0; i < 5; i++) {
            this.ctx.fillRect(
                x + Math.random() * this.tileSize,
                y + Math.random() * this.tileSize,
                2, 2
            );
        }
    }
    
    drawTree(x, y) {
        // Tree trunk
        this.ctx.fillStyle = '#8b4513';
        this.ctx.fillRect(x + 12, y + 20, 8, 12);
        
        // Tree leaves
        this.ctx.fillStyle = '#228b22';
        this.ctx.fillRect(x + 4, y + 4, 24, 20);
        
        // Tree outline
        this.ctx.strokeStyle = '#006400';
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(x + 4, y + 4, 24, 20);
    }
    
    drawRock(x, y) {
        // Rock shape
        this.ctx.fillStyle = '#696969';
        this.ctx.fillRect(x + 6, y + 8, 20, 16);
        this.ctx.fillRect(x + 8, y + 6, 16, 20);
        
        // Rock highlights
        this.ctx.fillStyle = '#a9a9a9';
        this.ctx.fillRect(x + 8, y + 8, 4, 4);
        this.ctx.fillRect(x + 16, y + 12, 4, 4);
    }
    
    drawWater(x, y) {
        // Water base
        this.ctx.fillStyle = '#4169e1';
        this.ctx.fillRect(x, y, this.tileSize, this.tileSize);
        
        // Water ripples
        this.ctx.fillStyle = '#87ceeb';
        for (let i = 0; i < 3; i++) {
            this.ctx.fillRect(
                x + i * 8,
                y + 8 + Math.sin(Date.now() * 0.003 + i) * 4,
                6, 2
            );
        }
    }
    
    drawPlayer() {
        const x = this.player.x * this.tileSize;
        const y = this.player.y * this.tileSize;
        
        // Player body
        this.ctx.fillStyle = '#ff6b6b';
        this.ctx.fillRect(x + 8, y + 16, 16, 16);
        
        // Player head
        this.ctx.fillStyle = '#fdbcb4';
        this.ctx.fillRect(x + 10, y + 8, 12, 12);
        
        // Player hair
        this.ctx.fillStyle = '#8b4513';
        this.ctx.fillRect(x + 10, y + 6, 12, 6);
        
        // Player eyes
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(x + 12, y + 12, 2, 2);
        this.ctx.fillRect(x + 18, y + 12, 2, 2);
        
        // Player legs
        this.ctx.fillStyle = '#4ecdc4';
        const legOffset = this.player.moving ? (this.player.animFrame * 2 - 1) : 0;
        this.ctx.fillRect(x + 10 + legOffset, y + 26, 4, 6);
        this.ctx.fillRect(x + 18 - legOffset, y + 26, 4, 6);
        
        // Direction indicator
        this.ctx.fillStyle = '#fff';
        switch (this.player.facing) {
            case 'up':
                this.ctx.fillRect(x + 15, y + 4, 2, 4);
                break;
            case 'down':
                this.ctx.fillRect(x + 15, y + 28, 2, 4);
                break;
            case 'left':
                this.ctx.fillRect(x + 4, y + 15, 4, 2);
                break;
            case 'right':
                this.ctx.fillRect(x + 24, y + 15, 4, 2);
                break;
        }
    }
    
    gameLoop() {
        if (!this.gameRunning) return;
        
        this.update();
        this.render();
        
        requestAnimationFrame(() => this.gameLoop());
    }
}

// Start the game when page loads
document.addEventListener('DOMContentLoaded', () => {
    const game = new PixelArtRPG();
    
    // Make game globally accessible for debugging
    window.game = game;
});