def RUN_GAME(Player_1_Voltage, Player_2_Voltage):
    import pygame, random, sys, math
    from collections import deque

    WIDTH, HEIGHT = 1000, 750

    # --- physics ---
    GRAVITY = 0.0
    GAME_GRAVITY = 0.2
    FLAP = -6

    # --- pipes ---
    PIPE_SPEED = 3
    PIPE_GAP = 190
    PIPE_WIDTH = 60
    PIPE_INTERVAL = 1500

    # --- RMS ---
    RMS_WINDOW = 3
    THRESHOLD_1 = 0.2
    THRESHOLD_2 = 0.2
    READY_RMS_MAX = 5

    # --- ready phase ---
    READY_TIME = 5000  # ms before auto-start fallback

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    class Bird:
        def __init__(self, x, color):
            self.x = x
            self.y = HEIGHT // 2
            self.vy = 0
            self.radius = 12
            self.color = color
            self.alive = True
            self.score = 0
            self.mean = 0

        def flap(self):
            if self.alive:
                self.vy = FLAP

        def update(self):
            if not self.alive:
                return
            if not game_started:
                return
            self.vy += GRAVITY
            self.y += self.vy
            if self.y > HEIGHT:
                self.alive = False

        def draw(self):
            c = self.color if self.alive else (120, 120, 120)
            pygame.draw.circle(screen, c, (int(self.x), int(self.y)), self.radius)

    class Pipe:
        def __init__(self):
            self.x = WIDTH
            self.top = random.randint(50, HEIGHT - PIPE_GAP - 50)
            self.passed = False

        def update(self):
            self.x -= PIPE_SPEED

        def draw(self):
            pygame.draw.rect(screen, (46, 204, 113), (self.x, 0, PIPE_WIDTH, self.top))
            pygame.draw.rect(
                screen,
                (46, 204, 113),
                (self.x, self.top + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.top - PIPE_GAP),
            )

        def collide(self, b):
            if not b.alive:
                return
            if b.x + b.radius > self.x and b.x - b.radius < self.x + PIPE_WIDTH:
                if b.y - b.radius < self.top or b.y + b.radius > self.top + PIPE_GAP:
                    b.alive = False

    bird1 = Bird(200, (255, 200, 0))
    bird2 = Bird(300, (0, 200, 255))

    pipes = []
    spawn_timer = pygame.time.get_ticks()

    buf1 = deque(maxlen=RMS_WINDOW)
    buf2 = deque(maxlen=RMS_WINDOW)
    trig1 = False
    trig2 = False

    # --- ready state ---
    game_started = False
    start_time = pygame.time.get_ticks()

    while True:
        clock.tick(60)

        # --- read voltages ---
        with Player_1_Voltage.get_lock():
            v1 = Player_1_Voltage.value
        with Player_2_Voltage.get_lock():
            v2 = Player_2_Voltage.value

        buf1.append(v1)
        buf2.append(v2)

        # --- RMS ---

        rms1 = math.sqrt(sum(x1 * x1 for x1 in buf1) / len(buf1)) if buf1 else 0
        rms2 = math.sqrt(sum(x2 * x2 for x2 in buf2) / len(buf2)) if buf2 else 0

        # --- READY DETECTION ---
        elapsed = pygame.time.get_ticks() - start_time
        buffers_ready = len(buf1) == RMS_WINDOW and len(buf2) == RMS_WINDOW and sum(buf1)>0.5
        rms_valid = (rms1 < READY_RMS_MAX and rms2 < READY_RMS_MAX)

        if not game_started:
            if (buffers_ready and rms_valid) or elapsed > READY_TIME:
                game_started = True
                GRAVITY = GAME_GRAVITY
                spawn_timer = pygame.time.get_ticks()

        # --- flap triggers ---
        if game_started:
            if (rms1 > THRESHOLD_1 and not trig1) and rms1 < 5:
                bird1.flap()

                trig1 = True
            if rms1 <= THRESHOLD_1:

                trig1 = False

            if (rms2 > THRESHOLD_2 and not trig2) and rms2 < 5:
                bird2.flap()
                trig2 = True
            if rms2 <= THRESHOLD_2:
                trig2 = False

        # --- events ---
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        now = pygame.time.get_ticks()

        # --- pipes ---
        if game_started and now - spawn_timer > PIPE_INTERVAL:
            pipes.append(Pipe())
            spawn_timer = now

        # --- update birds ---
        bird1.update()
        bird2.update()

        # --- update pipes ---
        for p in pipes:
            p.update()
            p.collide(bird1)
            p.collide(bird2)
            if not p.passed and p.x + PIPE_WIDTH < bird1.x:
                p.passed = True
                if bird1.alive:
                    bird1.score += 1
                if bird2.alive:
                    bird2.score += 1

        pipes = [p for p in pipes if p.x + PIPE_WIDTH > 0]

        # --- draw ---
        screen.fill((112, 197, 206))
        for p in pipes:
            p.draw()
        bird1.draw()
        bird2.draw()

        t1 = font.render(f"P1 RMS:{rms1:.2f}", True, (0, 0, 0))
        t2 = font.render(f"P2 RMS:{rms2:.2f}", True, (0, 0, 0))
        screen.blit(t1, (10, 10))
        screen.blit(t2, (WIDTH - 160, 10))

        if not game_started:
            msg = font.render("Waiting for signal...", True, (0, 0, 0))
            screen.blit(msg, (WIDTH // 2 - 140, HEIGHT // 2 - 20))

        pygame.display.flip()