import pygame
import math
from Box2D import b2Vec2

class Renderer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Lunar Lander")
        
        self.scale = 20.0  # pixels per meter
        self.screen_center = b2Vec2(width/2, height * 0.75)
        
    def clear(self):
        self.screen.fill((0, 0, 0))
        
    def to_screen(self, point):
        """This is to convert Box2D coordinates to screen coordinates"""
        return (
            int(point.x * self.scale + self.screen_center.x),
            int(self.height - (point.y * self.scale + self.screen_center.y))
        )

    def draw_flag(self, x, y, facing_right=True):
        base_pos = self.to_screen(b2Vec2(x, y))
        pole_top = self.to_screen(b2Vec2(x, y + 2))  # 2 meters tall pole
        pygame.draw.line(self.screen, (255, 255, 255), base_pos, pole_top, 2)
        flag_points = []
        if facing_right:
            flag_points = [
                pole_top,
                (pole_top[0] + 20, pole_top[1] - 10),
                (pole_top[0], pole_top[1] - 20)
            ]
        else:
            flag_points = [
                pole_top,
                (pole_top[0] + 20, pole_top[1] - 10),
                (pole_top[0], pole_top[1] - 20)
            ]
        
        pygame.draw.polygon(self.screen, (255, 0, 0), flag_points)
        
    def draw_landing_zone(self, landing_zone):
        self.draw_flag(landing_zone['left'], landing_zone['y'], False)  # Left flag faces right
        self.draw_flag(landing_zone['right'], landing_zone['y'], True)  # Right flag faces left
        left_point = self.to_screen(b2Vec2(landing_zone['left'], landing_zone['y']))
        right_point = self.to_screen(b2Vec2(landing_zone['right'], landing_zone['y']))
        pygame.draw.line(self.screen, (255, 255, 0), left_point, right_point, 2)  # Yellow line
        
    def draw_lander(self, position, angle):
        screen_pos = self.to_screen(position)
        
        points = [
            (-10, -15),  # bottom left
            (10, -15),   # bottom right
            (20, 15),    # top right
            (-20, 15),   # top left
        ]
        
        rotated_points = []
        for x, y in points:
            # rotate
            rx = x * math.cos(angle) - y * math.sin(angle)
            ry = x * math.sin(angle) + y * math.cos(angle)
            # translate
            rx += screen_pos[0]
            ry += screen_pos[1]
            rotated_points.append((int(rx), int(ry)))
            
        pygame.draw.polygon(self.screen, (255, 255, 255), rotated_points, 2)

    def draw_ground(self, segment):
        if hasattr(segment, "fixtures"):
            fixture = segment.fixtures[0]
            body = segment
        else:
            fixture = segment
            body = fixture.body
        vertices = [body.GetWorldPoint(v) for v in fixture.shape.vertices]
        screen_points = [self.to_screen(v) for v in vertices]

        pygame.draw.polygon(self.screen, (255, 255, 255), screen_points, 2)

    def draw_game_state(self, state):
        """game state info"""
        font = pygame.font.Font(None, 36)
        
        if 'time_remaining' in state:
            time_text = f"Time: {state['time_remaining']:.1f}s"
            text_surface = font.render(time_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, 10))
        
        if state.get('game_over', False):
            font_large = pygame.font.Font(None, 74)
            if state.get('landed_successfully', False):
                text = font_large.render('LANDED!', True, (0, 255, 0))
            else:
                text = font_large.render('CRASHED!', True, (255, 0, 0))
            text_rect = text.get_rect(center=(self.width/2, self.height/4))
            self.screen.blit(text, text_rect)

    def draw_thrust_effect(self, position, angle):
        thrust_local = [
            (-10, 20),  # left base of flame
            (10, 20),  # right base of flame
            (0, 25)  # tip of flame
        ]

        screen_pos = self.to_screen(position)
        rotated_points = []
        for x, y in thrust_local:
            rx = x * math.cos(angle) - y * math.sin(angle)
            ry = x * math.sin(angle) + y * math.cos(angle)
            rx += screen_pos[0]
            ry += screen_pos[1]
            rotated_points.append((int(rx), int(ry)))
        pygame.draw.polygon(self.screen, (255, 0, 0), rotated_points)

    def update(self):
        pygame.display.flip()