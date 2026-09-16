import pygame
import cv2
import numpy as np
import random
import math
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_PATH = os.path.join(SCRIPT_DIR, 'image.png')
if not os.path.exists(IMAGE_PATH):
    IMAGE_PATH = os.path.join(SCRIPT_DIR, 'image_2.png')

WIDTH, HEIGHT = 1280, 720  
FPS = 60

def create_sharp_dot(color, size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (0, 0, size, size))
    return surf

def create_glow_particle(color, size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    pygame.draw.circle(surf, (*color, 80), (center, center), center)
    pygame.draw.circle(surf, (*color, 255), (center, center), max(1, center // 2))
    return surf

def create_flower_sprite(base_color, size=12):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    petal_radius = max(2, size // 3)
    
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        px = center + int(math.cos(rad) * (size / 3.5))
        py = center + int(math.sin(rad) * (size / 3.5))
        pygame.draw.circle(surf, base_color, (int(px), int(py)), petal_radius)
        
    pygame.draw.circle(surf, (255, 215, 0), (center, center), max(2, petal_radius - 1))
    pygame.draw.circle(surf, (255, 100, 0), (center, center), max(1, petal_radius - 2))
    return surf

def create_glossy_pastel_aura(w, h):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w // 2, int(h * 0.45) 
    max_r = int(math.hypot(cx, cy)) 
    
    for r in range(max_r, 0, -5):
        factor = r / max_r
        alpha = int(180 * (1 - factor)**1.5) 
        pygame.draw.circle(surf, (255, 240, 200, alpha), (cx, cy), r)
    return surf

def analyze_image_and_targets(image_path, screen_w, screen_h):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        print(f"Error: Could not find {image_path}. Please ensure image.png is in the directory.")
        sys.exit()
        
    orig_h, orig_w = img.shape[:2]
    # Preserve aspect ratio and center on screen
    scale = min(screen_w / orig_w, screen_h / orig_h)
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    offset_x = (screen_w - new_w) // 2
    offset_y = (screen_h - new_h) // 2
    
    img_smooth = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img_smooth, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.bilateralFilter(gray, 5, 50, 50)
    edges = cv2.Canny(blurred, 50, 150) 
            
    outline_targets = []
    for y in range(new_h):
        for x in range(new_w):
            if edges[y, x] > 0:
                outline_targets.append({'x': x + offset_x, 'y': y + offset_y})

    # Realistic flame locations mapped to deepams, wicks, and lamps in the image
    flame_ratios = [
        # Left standing peacock deepam wicks
        (0.205, 0.555), (0.231, 0.535), (0.252, 0.555),
        # Right standing peacock deepam wicks
        (0.748, 0.555), (0.772, 0.540), (0.795, 0.555),
        # Floor oil lamps / diyas
        (0.145, 0.870), (0.201, 0.890), (0.258, 0.810), 
        (0.740, 0.835), (0.798, 0.890), (0.855, 0.880)
    ]
    flame_centers = []
    for rx, ry in flame_ratios:
        flame_centers.append({
            'x': int(new_w * rx) + offset_x, 
            'y': int(new_h * ry) + offset_y
        })

    rgb_img = cv2.cvtColor(img_smooth, cv2.COLOR_BGR2RGB)
    surface_temp = pygame.image.frombuffer(rgb_img.tobytes(), (new_w, new_h), 'RGB')
    reveal_color_surface = pygame.Surface((screen_w, screen_h))
    reveal_color_surface.blit(surface_temp, (offset_x, offset_y))
    
    reveal_targets = []
    TILE_SIZE = 2 
    for y in range(0, new_h, TILE_SIZE):
        for x in range(0, new_w, TILE_SIZE):
            reveal_targets.append({'x': x + offset_x, 'y': y + offset_y})
                
    # Sort targets ascending by y so highest Y (bottom) pops first
    outline_targets.sort(key=lambda t: t['y'])
    reveal_targets.sort(key=lambda t: t['y'])
    
    return outline_targets, reveal_targets, reveal_color_surface, flame_centers

def main():
    global WIDTH, HEIGHT
    pygame.init()
    
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,35"
    
    info = pygame.display.Info()
    WIDTH = info.current_w
    HEIGHT = info.current_h - 130
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("Ganesha Visualizer - Sacred Masterpiece")
    clock = pygame.time.Clock()

    targets = analyze_image_and_targets(IMAGE_PATH, WIDTH, HEIGHT)
    outline_targets, reveal_targets, reveal_color_surface, flame_centers = targets
    
    pastel_aura = create_glossy_pastel_aura(WIDTH, HEIGHT)
    
    outline_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    fill_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    spr_outline_gold = create_sharp_dot((255, 215, 0), 1)  

    bg_flower_sprites = [
        create_flower_sprite((255, 20, 147), 12),  
        create_flower_sprite((0, 220, 120), 12),   
        create_flower_sprite((65, 130, 255), 12),  
        create_flower_sprite((255, 215, 0), 12)    
    ]
    
    bg_glitter_sprites = [
        create_glow_particle((255, 215, 0), 4),    
        create_glow_particle((255, 255, 255), 3)   
    ]
    
    TILE_SIZE = 2
    active_particles = []
    bg_particles = []
    running = True
    phase = 1
    
    # Dynamic animation speed controls
    speed_multiplier = 1.0
    paused = False
    show_controls = True
    MAX_ACTIVE_PARTICLES = 6500

    try:
        font_ctrl = pygame.font.SysFont('Segoe UI', 11)
        font_ctrl_bold = pygame.font.SysFont('Segoe UI', 11, bold=True)
    except:
        font_ctrl = pygame.font.SysFont('Arial', 11)
        font_ctrl_bold = pygame.font.SysFont('Arial', 11, bold=True)

    while running:
        screen.fill((5, 2, 5))
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_UP, pygame.K_RIGHT, pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    speed_multiplier = min(10.0, round(speed_multiplier + 0.5, 1))
                elif event.key in (pygame.K_DOWN, pygame.K_LEFT, pygame.K_MINUS, pygame.K_KP_MINUS):
                    speed_multiplier = max(0.5, round(speed_multiplier - 0.5, 1))
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_h:
                    show_controls = not show_controls
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                    speed_multiplier = float(event.key - pygame.K_0)
                elif event.key == pygame.K_f:
                    # Fast forward / Skip phase
                    if phase == 1:
                        for t in outline_targets:
                            rect = spr_outline_gold.get_rect(center=(t['x'], t['y']))
                            outline_surface.blit(spr_outline_gold, rect)
                        outline_targets.clear()
                        active_particles.clear()
                        phase = 2
                    elif phase == 2:
                        fill_surface.blit(reveal_color_surface, (0, 0))
                        reveal_targets.clear()
                        active_particles.clear()
                        phase = 3
                elif event.key == pygame.K_r:
                    # Restart animation
                    targets = analyze_image_and_targets(IMAGE_PATH, WIDTH, HEIGHT)
                    outline_targets, reveal_targets, reveal_color_surface, flame_centers = targets
                    outline_surface.fill((0, 0, 0, 0))
                    fill_surface.fill((0, 0, 0, 0))
                    active_particles.clear()
                    bg_particles.clear()
                    phase = 1
                    paused = False

        if phase == 1:
            hue = (current_time // 30) % 360 
            pastel_color = pygame.Color(0)
            pastel_color.hsva = (hue, 25, 95, 100)
            colored_aura = pastel_aura.copy()
            colored_aura.fill(pastel_color, special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(colored_aura, (0, 0))

        if phase < 3:
            screen.blit(outline_surface, (0, 0))
            
        screen.blit(fill_surface, (0, 0))

        # Particle simulation update
        if not paused:
            surviving_particles = []
            for p in active_particles:
                step_speed = p['speed']
                if p['state'] == 'falling':
                    p['y'] += step_speed * 2  # Fall swiftly
                    if p['y'] >= HEIGHT:
                        p['y'] = HEIGHT
                        p['state'] = 'rising'
                    
                    if p['type'] == 'tile':
                        rect = (p['target_x'], p['target_y'], TILE_SIZE, TILE_SIZE)
                        screen.blit(reveal_color_surface, (p['x'], int(p['y'])), rect)
                    elif p['type'] == 'outline':
                        sprite = p['sprite']
                        sprite_rect = sprite.get_rect(center=(p['target_x'], int(p['y'])))
                        screen.blit(sprite, sprite_rect)
                    surviving_particles.append(p)
                    
                elif p['state'] == 'rising':
                    p['y'] -= step_speed  # Rise to designated place
                    if p['y'] <= p['target_y']:
                        # Reached target destination
                        if p['type'] == 'tile':
                            rect = (p['target_x'], p['target_y'], TILE_SIZE, TILE_SIZE)
                            fill_surface.blit(reveal_color_surface, (p['target_x'], p['target_y']), rect)
                        elif p['type'] == 'outline':
                            sprite = p['sprite']
                            target_rect = sprite.get_rect(center=(p['target_x'], p['target_y']))
                            outline_surface.blit(sprite, target_rect)
                    else:
                        # Continue rising
                        if p['type'] == 'tile':
                            rect = (p['target_x'], p['target_y'], TILE_SIZE, TILE_SIZE)
                            screen.blit(reveal_color_surface, (p['x'], int(p['y'])), rect)
                        elif p['type'] == 'outline':
                            sprite = p['sprite']
                            sprite_rect = sprite.get_rect(center=(p['target_x'], int(p['y'])))
                            screen.blit(sprite, sprite_rect)
                        surviving_particles.append(p)
                    
            active_particles = surviving_particles

        # Particle spawning (calm, graceful pacing at 1.0x)
        if not paused:
            if phase == 1:
                can_spawn = max(0, MAX_ACTIVE_PARTICLES - len(active_particles))
                spawn_count = min(can_spawn, int(420 * speed_multiplier))
                for _ in range(spawn_count):
                    if outline_targets:
                        t = outline_targets.pop()
                        active_particles.append({
                            'type': 'outline',
                            'sprite': spr_outline_gold,
                            'x': t['x'],
                            'y': random.randint(-120, -10),
                            'target_x': t['x'],
                            'target_y': t['y'],
                            'speed': random.uniform(3.5, 6.5) * speed_multiplier,
                            'state': 'falling'
                        })
                if not outline_targets and len(active_particles) == 0:
                    phase = 2
                    
            elif phase == 2:
                can_spawn = max(0, MAX_ACTIVE_PARTICLES - len(active_particles))
                spawn_count = min(can_spawn, int(320 * speed_multiplier))
                for _ in range(spawn_count):
                    if reveal_targets:
                        t = reveal_targets.pop()
                        active_particles.append({
                            'type': 'tile',
                            'x': t['x'],
                            'y': random.randint(-160, -10),
                            'target_x': t['x'],
                            'target_y': t['y'],
                            'speed': random.uniform(3.8, 7.0) * speed_multiplier,
                            'state': 'falling'
                        })
                if not reveal_targets and len(active_particles) == 0:
                    phase = 3 

        # Phase 3: Sacred Diya / Flame pulse
        if phase >= 3:
            for i, center in enumerate(flame_centers):
                pulse = math.sin(current_time * 0.006 + i) 
                radius = int(10 + pulse * 4) 
                alpha = int(140 + pulse * 60)
                
                glow_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
                c_pt = radius * 2
                
                pygame.draw.circle(glow_surf, (255, 255, 200, alpha), (c_pt, c_pt), int(radius * 0.4))
                pygame.draw.circle(glow_surf, (255, 180, 50, int(alpha * 0.6)), (c_pt, c_pt), int(radius * 0.8))
                pygame.draw.circle(glow_surf, (255, 80, 0, int(alpha * 0.2)), (c_pt, c_pt), radius)
                
                shake_x = center['x'] + random.uniform(-0.5, 0.5)
                shake_y = center['y'] + random.uniform(-0.5, 0.5)
                
                rect = glow_surf.get_rect(center=(shake_x, shake_y))
                screen.blit(glow_surf, rect, special_flags=pygame.BLEND_RGBA_ADD)

        # Flower petals and divine glitter
        if phase >= 2 and not paused:
            if random.random() < 0.08 * min(2.0, speed_multiplier): 
                is_flower = random.random() < 0.50  
                if is_flower:
                    sprite = random.choice(bg_flower_sprites)
                    speed_y = random.uniform(1.2, 2.5) * (1.0 + (speed_multiplier - 1.0) * 0.3)
                    wobble_width = random.uniform(0.8, 1.8)
                else:
                    sprite = random.choice(bg_glitter_sprites)
                    speed_y = random.uniform(1.0, 3.5) * (1.0 + (speed_multiplier - 1.0) * 0.3)
                    wobble_width = random.uniform(0.1, 0.4)

                bg_particles.append({
                    'sprite': sprite,
                    'x': random.randint(0, WIDTH),
                    'y': random.randint(-50, -10),
                    'speed_y': speed_y,
                    'wobble_speed': random.uniform(0.002, 0.005),
                    'wobble_offset': random.uniform(0, math.pi * 2),
                    'wobble_width': wobble_width
                })

        surviving_bg = []
        for p in bg_particles:
            if not paused:
                p['y'] += p['speed_y']
            draw_x = p['x'] + math.sin(current_time * p['wobble_speed'] + p['wobble_offset']) * p['wobble_width'] * 20
            
            if p['y'] < HEIGHT:
                screen.blit(p['sprite'], (int(draw_x), int(p['y'])))
                surviving_bg.append(p)
        # Vertical Sidebar View for Controls (docked along the right edge)
        if show_controls:
            bar_w, bar_h = 138, 172
            bar_surf = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)
            pygame.draw.rect(bar_surf, (14, 9, 22, 195), (0, 0, bar_w, bar_h), border_radius=10)
            pygame.draw.rect(bar_surf, (218, 165, 32, 90), (0, 0, bar_w, bar_h), width=1, border_radius=10)

            # Header divider
            pygame.draw.line(bar_surf, (218, 165, 32, 60), (10, 26), (bar_w - 10, 26), 1)

            t_head = font_ctrl_bold.render("CONTROLS", True, (212, 175, 55))
            status_color = (255, 120, 120) if paused else (255, 230, 140)
            status_lbl = "⏸ PAUSED" if paused else f"Speed: {speed_multiplier:.1f}x"
            t_speed = font_ctrl_bold.render(status_lbl, True, status_color)

            t_spd_adj = font_ctrl.render("▲/▼ : Speed", True, (210, 210, 220))
            t_pause = font_ctrl.render("Space : Pause", True, (210, 210, 220))
            t_skip = font_ctrl.render("F : Skip Phase", True, (210, 210, 220))
            t_reset = font_ctrl.render("R : Restart", True, (210, 210, 220))
            t_hide = font_ctrl.render("H : Hide Dock", True, (160, 160, 170))

            bar_surf.blit(t_head, ((bar_w - t_head.get_width()) // 2, 7))
            bar_surf.blit(t_speed, ((bar_w - t_speed.get_width()) // 2, 33))
            bar_surf.blit(t_spd_adj, (12, 58))
            bar_surf.blit(t_pause, (12, 80))
            bar_surf.blit(t_skip, (12, 102))
            bar_surf.blit(t_reset, (12, 124))
            bar_surf.blit(t_hide, (12, 146))

            screen.blit(bar_surf, (WIDTH - bar_w - 12, (HEIGHT - bar_h) // 2))

        # Clearly visible "Arun" badge on bottom-left
        badge_w, badge_h = 110, 32
        badge_surf = pygame.Surface((badge_w, badge_h), pygame.SRCALPHA)
        pygame.draw.rect(badge_surf, (14, 9, 22, 210), (0, 0, badge_w, badge_h), border_radius=16)
        pygame.draw.rect(badge_surf, (255, 215, 0, 160), (0, 0, badge_w, badge_h), width=1, border_radius=16)
        t_author = font_ctrl_bold.render("✨ Arun", True, (255, 240, 160))
        badge_surf.blit(t_author, ((badge_w - t_author.get_width()) // 2, 7))
        screen.blit(badge_surf, (16, HEIGHT - 44))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()