import Abinde as ab
import random
import pkg_resources
import sys

if pkg_resources.get_distribution("Abinde").version < "2.4.2":
    print("Minimum Abinde version 2.4.2 is required to run this game.")
    sys.exit()
    

blobs = []
game = ab.Game(title="Blob Game", size=[1000, 900])
player = ab.sprite.Ellipse(game, [0, 0], [50, 50], color=ab.color.RASPBERRY)
points = 0
game_over = False
score = ab.sprite.Text(game, [10, 10], f"Score: {points}", color=ab.color.RASPBERRY)
center = [game.size[0] / 2 - player.width, game.size[1] / 2 - player.height]
player.go_to(center)
def move(keys):
    if (player.x > 0 and keys[ab.key.LEFT]) or (player.x > 0 and keys[ab.key.A]):
        player.move([-(player.width / 20), 0])
    if (player.x < 1000 - player.width and keys[ab.key.RIGHT]) or (player.x < 1000 - player.width and keys[ab.key.D]):
        player.move([(player.width / 20), 0])
    if (player.y > 0 and keys[ab.key.UP]) or (player.y > 0 and keys[ab.key.W]):
        player.move([0, 0-(player.height / 20)])
    if (player.y < 900 - player.height and keys[ab.key.DOWN]) or (player.y < 900 - player.height and keys[ab.key.S]):
        player.move([0, (player.height / 20)])

    score.text = f"Score: {int(points)}"

def if_touching(e):
    global points, player, game_over
    touching = player.touching_any(blobs)
    if len(touching) > 0:
        for blob in touching:
            if game_over:
                game.wait(2000)
                game.reset()
                score = ab.sprite.Text(game, [10, 10], f"Score: {int(points)}", color=ab.color.MAROON)
                ab.sprite.Text(game, pos=[1000 / 2 - 190, 900 / 2 - 70], text="Game Over", fontsize=100, color=ab.color.MAROON)
            if blob.width < player.width:
                player.height += blob.height / 10
                player.width += blob.width / 10
                points += blob.width / 10
                blobs.remove(blob)
                blob.kill()
            elif blob.width > player.width and not game_over:
                player.kill()
                game_over = True
    if player.width >= 300:
        zoom_out()

def spawn(e):
    if random.randint(1, 100) == 50:
        size = random.randint(1, int(player.width * 2) - random.randint(int(player.width / 2 - 1), int(player.width - 1)))
        blobs.append(ab.sprite.Ellipse(game, [random.randint(1, 1000), random.randint(1, 900)], [size, size], color=ab.color.RASPBERRY))

def zoom_out():
    player.width -= 30
    player.height -= 30
    player.x -= 30
    player.y -= 30
    for blob in blobs:
        blob.width -= 30
        blob.height -= 30
        blob.x -= 30
        blob.y -= 30
def zoom_in():
    player.height += 2
    player.width += 2
    for blob in blobs:
        blob.width += 2
        blob.height += 2

ab.OnUpdate(game, if_touching)
ab.OnUpdate(game, spawn)
ab.OnKeyPress(game, move)
game.mainloop()
