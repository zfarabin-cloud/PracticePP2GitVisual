"""
config.py — Shared constants for Racer TSIS3.
All graphics are drawn procedurally; no image assets required.
"""

# Window
WIDTH, HEIGHT = 400, 600
FPS           = 60

# Road geometry
ROAD_L = 55          # left edge of road
ROAD_R = 345         # right edge of road
ROAD_W = ROAD_R - ROAD_L          # 290 px
LANES  = [103, 200, 297]          # x-centre of each lane
LANE_W = ROAD_W // 3              # ~97 px per lane

# Car sizes (px)
PLAYER_W, PLAYER_H  = 46, 76
TRAFFIC_W, TRAFFIC_H = 46, 76

# Speeds (px / frame)
PLAYER_SPEED   = 6
SCROLL_BASE    = 4    # road scroll px/frame at level 1
TRAFFIC_BASE   = 5

# Gameplay tuning
COIN_SPAWN_INTERVAL    = 120   # frames between coin spawns
OBSTACLE_SPAWN_INTERVAL= 200   # frames between hazard rows
PU_SPAWN_INTERVAL      = 300   # frames between power-up spawns
PU_FIELD_FRAMES        = 300   # frames a power-up stays on screen before vanishing

# Difficulty presets
DIFFICULTY = {
    "Easy":   {"speed_mult": 0.70, "spawn_mult": 0.60, "traffic_n": 2},
    "Normal": {"speed_mult": 1.00, "spawn_mult": 1.00, "traffic_n": 3},
    "Hard":   {"speed_mult": 1.40, "spawn_mult": 1.50, "traffic_n": 4},
}

# Scoring
DIST_PX_PER_POINT = 60    # road pixels scrolled → 1 distance point
PU_REPAIR_BONUS   = 50

# Power-up types
PU_NITRO  = "nitro"
PU_SHIELD = "shield"
PU_REPAIR = "repair"
PU_NITRO_FRAMES  = 240   # ~4 s at 60 FPS
PU_SHIELD_FRAMES = None  # until hit

# Colours
C_SKY       = ( 20,  25,  40)
C_GRASS     = ( 35,  90,  40)
C_ROAD      = ( 65,  68,  78)
C_LANE_MRK  = (230, 230, 170)
C_KERB_A    = (210,  40,  40)
C_KERB_B    = (240, 240, 240)
C_WHITE     = (255, 255, 255)
C_BLACK     = (  0,   0,   0)
C_PANEL     = ( 18,  18,  28)

C_OIL       = ( 20,  10,  50)
C_BARRIER   = (230,  80,  20)
C_NITRO_STR = (  0, 180, 255)

C_PU = {
    PU_NITRO:  (  0, 220, 255),
    PU_SHIELD: (255, 215,   0),
    PU_REPAIR: ( 50, 220, 110),
}

C_HUD_HI    = (255, 215,   0)
C_HUD_LO    = (180, 180, 200)
C_BTN       = ( 50,  55,  80)
C_BTN_HI    = ( 80,  90, 130)
C_RED_BTN   = (110,  30,  30)
C_RED_BTN_H = (160,  50,  50)

# Default car colour options
CAR_COLORS = {
    "Blue":   (  0, 120, 255),
    "Red":    (220,  40,  40),
    "Green":  ( 30, 200,  80),
    "Yellow": (255, 210,   0),
    "Purple": (160,  60, 220),
    "White":  (220, 220, 230),
}
