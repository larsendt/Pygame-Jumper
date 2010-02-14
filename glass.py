import os, pygame, math, random
from pygame import *

building_speed = -6

def load_image(name, colorkey=None):
	fullname = os.path.join('', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', fullname
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

class Shard(pygame.sprite.Sprite):
	def __init__(self, spd, pos, building_top, building_speed, gravity):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image("im.bmp", -1)
		self.position = self.rect.topleft = pos
		self.speed = spd
		self.spin = 0
		self.original = self.image
		self.building_top = building_top
		self.building_speed = building_speed
		self.gravity = gravity
		
	def update(self, building_speed):
		self.speed[1] += self.gravity
		self.building_speed = building_speed
		self.rect = self.rect.move(self.speed)
		self.position = self.rect.topleft
		self.spin += 15
		rotate = pygame.transform.rotate
		self.image = rotate(self.original, self.spin)
		self.rect = self.image.get_rect()
		self.rect.topleft = self.position
		
		if self.rect.bottom > self.building_top:
			self.speed[1] = -self.speed[1] + (self.gravity*15)
			self.speed[0] = self.speed[0] + self.building_speed
			if self.speed[0] < self.building_speed:
				self.speed[0] = self.building_speed
			self.rect.bottom = self.building_top
		if self.rect.right < 0:
			self.kill()
		
class Shards(pygame.sprite.RenderUpdates):
	def __init__(self, pos, building_top, building_speed, gravity):
		pygame.sprite.RenderUpdates.__init__(self)
		self.position = pos
		for i in xrange(10):
			shard = Shard([random.uniform(7, 10), random.uniform(3, 10)], self.position, building_top, building_speed, gravity)
			self.add(shard)
			
class Building(pygame.sprite.Sprite):	
	def __init__(self, building_id, building_top, building_speed, width):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('building.png')
		self.rect.topleft = (building_id*108, building_top)
		self.building_speed = building_speed
		self.screenwidth = width
	
	def update(self, building_speed):
		self.building_speed = building_speed
		self.rect = self.rect.move(self.building_speed, 0)	
		if self.rect.right < 0:
			self.rect.left = self.screenwidth
			
class BuildingGroup(pygame.sprite.RenderPlain):
	def __init__(self, building_top, building_speed, width):
		pygame.sprite.RenderPlain.__init__(self)
		for i in xrange(8):
			building = Building(i, building_top, building_speed, width)
			self.add(building)
			
class Hero(pygame.sprite.Sprite):
	def __init__(self, building_top, gravity):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('ball.png', -1)
		self.rect.bottomleft = (100, building_top)
		self.jumping = 0
		self.jump_speed = 0
		self.building_top = building_top
		self.gravity = gravity
		
	def update(self, jumping):
		self.jumping = jumping
		self.rect = self.rect.move(0, self.jump_speed)
		if self.rect.bottom > self.building_top:
			self.rect.bottom = self.building_top
		self.jump_speed += self.gravity
		if self.jumping:
			if self.rect.bottom == self.building_top:
				self.jump_speed = -7
			if self.rect.bottom > self.building_top:
				self.jumping = 0
				self.rect.bottom = self.building_top
			
		
class GlassPane(pygame.sprite.Sprite):
	def __init__(self, pos, building_speed, building_top, width):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('glasspane.png')
		self.rect.bottomleft = pos
		self.building_speed = building_speed
		self.building_top = building_top
		self.screenwidth = width
	
	def update(self, collision, building_speed):
		self.building_speed = building_speed
		self.rect = self.rect.move(self.building_speed, 0)
		if self.rect.bottomleft < 0:
			self.rect.bottomleft = self.screenwidth, self.building_top
		if collision:
			temp_pos = self.rect.bottomleft
			self.rect.bottomleft = self.screenwidth, self.building_top
			return temp_pos
			
class GlassPanes(pygame.sprite.RenderUpdates):
	def __init__(self, building_top, building_speed, width):
		pygame.sprite.RenderUpdates.__init__(self)
		self.building_speed = building_speed
		self.building_top = building_top
		self.screenwidth = width
		glass_pane = GlassPane((self.screenwidth, self.building_top), self.building_speed, self.building_top, self.screenwidth)
		self.add(glass_pane)
	
	def add_pane(self):
		glass_pane = GlassPane((self.screenwidth, self.building_top), self.building_speed, self.building_top, self.screenwidth)
		self.add(glass_pane)

def main():	
	sky = 150, 150, 150
	jumping = 0
	building_speed = -6
	size = width, height = 756, 400
	screen = pygame.display.set_mode(size)
	screen.fill((255, 255, 255))

	gravity = .2
	acceleration = -.001
	building_top = height - 100

	shard_groups = pygame.sprite.Group()
	buildings = BuildingGroup(building_top, building_speed, width)
	hero_sprite = Hero(building_top, gravity)
	hero = pygame.sprite.RenderUpdates((hero_sprite))
	clock = pygame.time.Clock()
	glass_panes = GlassPanes(building_top, building_speed, width)
	
	while 1:
		clock.tick(60)
		mouse_pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
				if event.type == QUIT:
					return
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					return
				if event.type == MOUSEBUTTONDOWN:
					glass_panes.add_pane()
					jumping = 1
				if event.type == MOUSEBUTTONUP:
					jumping = 0
					
		for glass_pane in sprite.spritecollide(hero_sprite, glass_panes, 0):
			position = glass_pane.update(1, building_speed)
			shards = Shards((position), building_top, building_speed, gravity)
			shard_groups.add(shards)
			building_speed -= building_speed/10
			
		screen.fill(sky)
		
		building_speed += acceleration
		
		shard_groups.update(building_speed)
		glass_panes.update(0, building_speed)
		buildings.update(building_speed)
		hero.update(jumping)
		
		shard_groups.draw(screen)
		buildings.draw(screen)
		hero.draw(screen)
		glass_panes.draw(screen)
		
		pygame.display.flip()


if __name__ == '__main__': main()
