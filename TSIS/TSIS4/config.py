"""
config.py — Shared constants for the Snake TSIS4 project.
"""

# Window / grid
WIDTH       = 800
HEIGHT      = 600
PANEL_H     = 50          # top HUD panel height
BLOCK       = 20          # grid cell size in pixels
COLS        = WIDTH  // BLOCK
ROWS        = (HEIGHT - PANEL_H) // BLOCK

# Speed
FPS_BASE    = 10          # level-1 ticks per second
FPS_MAX     = 30

# Gameplay tuning
FOOD_PER_LEVEL   = 5      # foods eaten to advance a level
OBSTACLE_COUNT   = 6      # wall blocks added per level (cumulative)
POWERUP_FIELD_TTL  = 8_000   # ms a power-up stays on the field
POWERUP_EFFECT_TTL = 5_000   # ms an effect lasts after collection
POISON_SHORTEN    = 2     # segments removed on poison eat

# Colours  (r, g, b)
C_BLACK       = (  0,   0,   0)
C_WHITE       = (255, 255, 255)
C_DARK        = ( 20,  20,  30)
C_PANEL       = ( 30,  30,  45)
C_GRID        = ( 35,  35,  50)
C_SNAKE_DEF   = ( 80, 220,  80)   # default snake colour (overridden by settings)
C_SNAKE_EYE   = (255, 255, 255)
C_FOOD_LIGHT  = (255, 220,  80)   # weight-1 food
C_FOOD_MEDIUM = (255, 140,   0)   # weight-2 food
C_FOOD_HEAVY  = (255,  60,  60)   # weight-3 food
C_POISON      = (100,   0,   0)   # poison food
C_OBSTACLE    = (120, 120, 140)
C_PU_SPEED    = (  0, 220, 255)   # speed-boost
C_PU_SLOW     = (160,   0, 255)   # slow-motion
C_PU_SHIELD   = (255, 215,   0)   # shield
C_TEXT_HI     = (255, 215,   0)
C_TEXT_LO     = (180, 180, 200)
C_BTN         = ( 50,  50,  75)
C_BTN_HI      = ( 80,  80, 120)
C_RED         = (220,  50,  50)
C_GREEN       = ( 50, 200,  50)

# Power-up type constants
PU_SPEED  = "speed"
PU_SLOW   = "slow"
PU_SHIELD = "shield"

# DB connection — edit to match your PostgreSQL setup
DB_CONFIG = dict(
    host     = "localhost",
    port     = 5432,
    dbname   = "snake_db",
    user     = "postgres",
    password = "postgres",
)
