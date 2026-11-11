"""Simulation physique : chute dans l'arène ronde + fusions. Produit les états par image et les événements."""
import math, random, json, sys
import pymunk
from theme import T
from sprites import LEVELS, BOMB_R

W, H, FPS = 1080, 1920, 30
CX, CY, AR = 540, 1000, 440          # arène
GAP = 92                               # demi-largeur de l'entonnoir
DUR = 62.0
SUB = 8                                # sous-pas physiques par image


TARGETS = {1: 0.4, 2: 3.0, 3: 7.5, 4: 13.0, 5: 20.0, 6: 31.0}


def run(seed=7, drop_every=0.36, early=8.0, verbose=True, bomb_t=40.0, lead=2.5):
    rnd = random.Random(seed)
    space = pymunk.Space()
    space.gravity = (0, 1500)
    space.damping = 0.97
    static = space.static_body
    # cercle (sauf l'ouverture en haut)
    yj = CY - math.sqrt(AR ** 2 - GAP ** 2)
    a_open = math.asin(GAP / AR)
    n = 120
    pts = []
    for i in range(n + 1):
        a = -math.pi / 2 + a_open + (2 * math.pi - 2 * a_open) * i / n
        pts.append((CX + AR * math.cos(a), CY + AR * math.sin(a)))
    segs = [pymunk.Segment(static, pts[i], pts[i + 1], 6) for i in range(n)]
    segs.append(pymunk.Segment(static, (CX - GAP, -400), (CX - GAP, yj), 6))
    segs.append(pymunk.Segment(static, (CX + GAP, -400), (CX + GAP, yj), 6))
    for s in segs:
        s.elasticity = 0.92; s.friction = 0.35; s.collision_type = 2; s.uid = -1
    space.add(*segs)

    bodies = {}   # id -> (body, shape, level, born_time)
    next_id = [0]
    events = []   # (t, type, level, x, y)

    def spawn(level, x, y, vx=0, vy=0, t=0.0):
        r = LEVELS[level][2]
        mass = (r / 20) ** 2
        b = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, r))
        b.position = (x, y); b.velocity = (vx, vy)
        b.angular_velocity = rnd.uniform(-2, 2)
        sh = pymunk.Circle(b, r)
        sh.elasticity = 0.9; sh.friction = 0.3
        sh.collision_type = 1
        i = next_id[0]; next_id[0] += 1
        sh.uid = i
        space.add(b, sh)
        bodies[i] = [b, sh, level, t]
        return i

    pending = []
    def on_collide(arbiter, space_, data):
        a, b = arbiter.shapes
        if a.uid in bodies and b.uid in bodies and bodies[a.uid][2] == bodies[b.uid][2]:
            pending.append((a.uid, b.uid))

    last_bounce = {}
    now = [0.0]
    def on_bounce(arbiter, space_, data):
        if not arbiter.is_first_contact:
            return
        imp = arbiter.total_impulse.length
        for sh in arbiter.shapes:
            if sh.uid in bodies:
                b = bodies[sh.uid]
                strength = imp / b[0].mass
                if strength > 260 and now[0] - last_bounce.get(sh.uid, -1) > 0.12:
                    last_bounce[sh.uid] = now[0]
                    p = b[0].position
                    events.append((now[0], "bounce", b[2], round(p.x, 1), round(p.y, 1), sh.uid, round(min(strength, 2000), 0)))
    space.on_collision(1, 1, begin=on_collide, pre_solve=on_collide, post_solve=on_bounce)
    space.on_collision(1, 2, post_solve=on_bounce)

    # pré-remplissage : de l'action dès la première image
    pre = [(470, 1330), (520, 1335), (640, 1300), (690, 1310), (575, 1250), (430, 1250), (360, 1180), (410, 1190),
           (700, 1180), (750, 1190), (560, 1150), (610, 1150)]
    for (x, y) in pre:
        spawn(0, x, y, rnd.uniform(-60, 60), rnd.uniform(-80, 0), 0.0)
    for (x, y) in ((300, 1060), (790, 1060), (480, 1080), (640, 1070)):
        spawn(1, x, y, rnd.uniform(-60, 60), 0, 0.0)
    events.append((0.0, "reveal", 1, 540, 1100))
    bomb = None   # [body, shape, t_drop, t_touch, t_boom]
    frames = []
    max_level = 1
    t = 0.0
    next_drop = 0.4
    universe_t = None
    nframes = int(DUR * FPS)
    for f in range(nframes):
        t = f / FPS
        now[0] = t
        # chute des miettes
        if bomb is None and t >= bomb_t:
            b = pymunk.Body(6, pymunk.moment_for_circle(6, 0, BOMB_R))
            b.position = (CX + rnd.uniform(-20, 20), -60); b.velocity = (0, 400)
            sh = pymunk.Circle(b, BOMB_R); sh.elasticity = 0.5; sh.friction = 0.6; sh.collision_type = 3; sh.uid = -2
            space.add(b, sh)
            bomb = [b, sh, t, None, None]
            events.append((t, "bomb_drop", -1, CX, 0))
        if bomb is not None and bomb[4] is None:
            if bomb[3] is None and bomb[0].position.y > CY - AR + 160:
                bomb[3] = t
            if bomb[3] is not None and t - bomb[3] > 1.4:
                bp = bomb[0].position
                for u, bb in bodies.items():
                    dv = bb[0].position - bp
                    dist = max(40, dv.length)
                    if dist < 520:
                        imp = dv / dist * (1 - dist / 520) * 2600 * bb[0].mass
                        bb[0].apply_impulse_at_world_point(imp, bb[0].position)
                space.remove(bomb[0], bomb[1])
                bomb[4] = t
                events.append((t, "boom", -1, round(bp.x, 1), round(bp.y, 1)))
        if universe_t is None and t >= next_drop:
            nxt = max_level + 1
            behind = nxt in TARGETS and t > TARGETS[nxt] - lead
            if behind and max_level >= 1:
                lvl = min(max_level, 3) if rnd.random() < 0.6 else min(max_level - 1, 3)
            else:
                lvl = 0 if (t < early or rnd.random() < 0.82) else 1
            spawn(lvl, CX + rnd.uniform(-30, 30), -60, rnd.uniform(-40, 40), 300, t)
            events.append((t, "drop", lvl, CX, 60))
            next_drop = t + drop_every * rnd.uniform(0.85, 1.15)
        for _ in range(SUB):
            # attraction douce entre objets identiques (aide les fusions)
            items = list(bodies.values())
            for i in range(len(items)):
                bi = items[i]
                for j in range(i + 1, len(items)):
                    bj = items[j]
                    if bi[2] != bj[2]:
                        continue
                    d = bj[0].position - bi[0].position
                    dist = d.length
                    lim = (LEVELS[bi[2]][2]) * 4.5
                    if 1 < dist < lim:
                        k = 900 * bi[0].mass * (1 - dist / lim)
                        fv = d / dist * k
                        bi[0].apply_force_at_world_point(fv, bi[0].position)
                        bj[0].apply_force_at_world_point(-fv, bj[0].position)
            space.step(1 / (FPS * SUB))
            done = set()
            for ua, ub in pending:
                if ua in done or ub in done or ua not in bodies or ub not in bodies:
                    continue
                A, B = bodies[ua], bodies[ub]
                lvl = A[2]
                if lvl >= len(LEVELS) - 1:
                    continue
                p = (A[0].position + B[0].position) / 2
                v = (A[0].velocity + B[0].velocity) / 2
                for u in (ua, ub):
                    space.remove(bodies[u][0], bodies[u][1]); del bodies[u]
                    done.add(u)
                nid = spawn(lvl + 1, p.x, p.y, v.x * 0.6 + rnd.uniform(-60, 60), min(v.y, 0) - 520, t)
                events.append((t, "merge", lvl + 1, p.x, p.y))
                if lvl + 1 > max_level:
                    max_level = lvl + 1
                    events.append((t, "reveal", lvl + 1, p.x, p.y))
                    if verbose:
                        print(f"  t={t:5.1f}s  niveau {lvl + 2} : {LEVELS[lvl + 1][0]}")
                    if lvl + 1 == len(LEVELS) - 1:
                        universe_t = t
            pending.clear()
        # objets sortis par le haut (sécurité)
        for u in list(bodies):
            if bodies[u][0].position.y > H + 300:
                space.remove(bodies[u][0], bodies[u][1]); del bodies[u]
        fr = [(u, round(b[0].position.x, 1), round(b[0].position.y, 1), round(b[0].angle, 3), b[2], b[3])
              for u, b in bodies.items()]
        if bomb is not None and bomb[4] is None:
            fr.append((-2, round(bomb[0].position.x, 1), round(bomb[0].position.y, 1), round(bomb[0].angle, 3), -1, bomb[2]))
        frames.append(fr)
    return frames, events, universe_t


if __name__ == "__main__":
    for seed in map(int, sys.argv[1:] or [7]):
        for de in (0.30, 0.34, 0.38):
            print(f"seed {seed} drop {de}")
            frames, events, ut = run(seed, de)
            print("  -> univers à", ut, " objets à la fin:", len(frames[-1]))
