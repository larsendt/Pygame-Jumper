import os, pygame, math, random
from pygame import *

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
		self.smash_speed = -building_speed/4
		for i in xrange(15):
			shard = Shard([random.uniform(1, self.smash_speed+2), random.uniform(-7, 1)], self.position, building_top, building_speed, gravity)
			self.add(shard)
			
class Building(pygame.sprite.Sprite):	
	def __init__(self, building_id, height, building_speed, width):
		pygame.sprite.Sprite.__init__(self)
		self.width = random.uniform(100, 300)
		self.height = random.uniform(50, 200)
		self.color = (50, 50, 50)
		self.image = pygame.surface.Surface((self.width, self.height))
		self.image.fill(self.color)
		self.rect = self.image.get_rect()
		self.rect.topleft = (building_id * 150, height - self.height)
		self.building_speed = building_speed
		self.screenwidth = width
	
	def update(self, building_speed):
		self.building_speed = building_speed
		self.rect = self.rect.move(self.building_speed, 0)	
		if self.rect.right < 0:
			self.rect.left = self.screenwidth
			
class BuildingGroup(pygame.sprite.RenderUpdates):
	def __init__(self, building_top, building_speed, width):
		pygame.sprite.RenderUpdates.__init__(self)
		for i in xrange(8):
			building = Building(i, building_top, building_speed, width)
			self.add(building)
			
class Layer2(pygame.sprite.Sprite):
	def __init__(self, prev_pos, height, building_speed, width):
		pygame.sprite.Sprite.__init__(self)
		self.screenwidth = width
		self.width = random.uniform(20, 100)
		self.height = random.uniform(150, 250)
		self.screenheight = height
		self.color = 80, 80, 80
		self.image =  pygame.surface.Surface((self.width, self.height))
		self.image.fill(self.color)
		self.rect = self.image.get_rect()
		self.rect.topleft = (prev_pos+self.width, self.screenheight-self.height)
		
	def update(self, building_speed):
		self.rect = self.rect.move(building_speed/3, 0)
		if self.rect.right < 0:
			self.rect.left = self.screenwidth
			self.width = random.uniform(20, 100)
			self.height = random.uniform(150, 250)
			self.image = pygame.surface.Surface((self.width, self.height))
			self.image.fill(self.color)
			self.rect = self.image.get_rect()
			self.rect.topleft = (self.screenwidth, self.screenheight-self.height)
			
class L2Group(pygame.sprite.RenderUpdates):
	def __init__(self, building_top, building_speed, width):
		pygame.sprite.RenderUpdates.__init__(self)
		self.b_top = building_top
		self.screenwidth = width
		pos = 0
		for i in xrange(25):
			l2_item = Layer2(pos, self.b_top, building_speed, self.screenwidth)
			pos = l2_item.rect.left
			self.add(l2_item)
			
class Layer3(pygame.sprite.Sprite):
	def __init__(self, prev_pos, height, building_speed, width):
		pygame.sprite.Sprite.__init__(self)
		self.screenwidth = width
		self.width = random.uniform(10, 50)
		self.height = random.uniform(150, 350)
		self.screenheight = height
		self.color = 110, 110, 115
		self.image =  pygame.surface.Surface((self.width, self.height))
		self.image.fill(self.color)
		self.rect = self.image.get_rect()
		self.rect.topleft = (prev_pos+self.width, self.screenheight-self.height)
		
	def update(self, building_speed):
		self.rect = self.rect.move(building_speed/6, 0)
		if self.rect.right < 0:
			self.rect.left = self.screenwidth
			self.width = random.uniform(10, 50)
			self.height = random.uniform(150, 350)
			self.image = pygame.surface.Surface((self.width, self.height))
			self.image.fill(self.color)
			self.rect = self.image.get_rect()
			self.rect.topleft = (self.screenwidth, self.screenheight-self.height)
			
class L3Group(pygame.sprite.RenderUpdates):
	def __init__(self, building_top, building_speed, width):
		pygame.sprite.RenderUpdates.__init__(self)
		self.b_top = building_top
		self.screenwidth = width
		pos = 0
		for i in xrange(25):
			l3_item = Layer3(pos, self.b_top, building_speed, self.screenwidth)
			pos = l3_item.rect.left
			self.add(l3_item)
			
class Hero(pygame.sprite.Sprite):
	def __init__(self, building_top, gravity):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('man.png', -1)
		self.rect.bottomleft = (100, building_top)
		self.jump_speed = 0
		self.jumping = 0
		self.building_top = building_top
		self.gravity = gravity
		self.position = self.rect.center
		self.original = self.image
		self.angular = 0
		
	def update(self, building_speed):
		self.angular += building_speed
		self.rect = self.rect.move(0, self.jump_speed)
		current_pos = self.rect.center
		rotate = pygame.transform.rotate
		self.image = rotate(self.original, self.angular)
		self.rect = self.image.get_rect()
		self.rect.center = current_pos
		if self.rect.centery > self.position[1]:
			self.rect.centery = self.position[1]
		self.jump_speed += self.gravity
		if self.jumping:
			self.jumping = 0
			if self.rect.centery == self.position[1]:
				self.jump_speed = -7
			if self.rect.centery > self.position[1]:
				self.jumping = 0
				self.rect.centery = self.position[1]
				
	def jump(self):
		self.jumping = 1
			
		
class GlassPane(pygame.sprite.Sprite):
	def __init__(self, pos, building_speed, building_top, width):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.surface.Surface((2, 50))
		self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.bottomleft = pos[0], pos[1]-100
		self.building_speed = building_speed
		self.building_top = building_top - 100
		self.screenwidth = width
	
	def update(self, collision, building_speed):
		self.building_speed = building_speed
		self.rect = self.rect.move(self.building_speed, 0)
		if self.rect.left < 0:
			self.rect.left = self.screenwidth
		if collision:
			temp_pos = self.rect.bottomleft
			self.kill()
			return temp_pos
			
class GlassPanes(pygame.sprite.RenderUpdates):
	def __init__(self, building_top, building_speed, width):
		pygame.sprite.RenderUpdates.__init__(self)
		self.building_speed = building_speed
		self.building_top = building_top
		self.screenwidth = width
	
	def add_pane(self):
		glass_pane = GlassPane((self.screenwidth, self.building_top), self.building_speed, self.building_top, self.screenwidth)
		self.add(glass_pane)

def main():	
	sky = 150, 150, 150
	jumping = 0
	building_speed = -8
	size = width, height = 750, 400
	screen = pygame.display.set_mode(size)
	screen.fill((255, 255, 255))

	gravity = .2
	acceleration = -.01
	building_top = height - 100

	layer3 = L3Group(height, building_speed, width)
	layer2 = L2Group(height, building_speed, width)
	buildings = BuildingGroup(height, building_speed, width)
	shard_groups = pygame.sprite.Group()
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
				if event.type == KEYDOWN and event.key == K_SPACE:
					hero_sprite.jump()
					
		for glass_pane in sprite.spritecollide(hero_sprite, glass_panes, 0):
			position = glass_pane.update(1, building_speed)
			shards = Shards((position), building_top, building_speed, gravity)
			shard_groups.add(shards)
			building_speed -= building_speed/10
			
		screen.fill(sky)
		
		building_speed += acceleration
		if building_speed < -20:
			building_speed = -20
		
		if building_speed > -4:
			building_speed = -4
		
		layer3.update(building_speed)
		layer2.update(building_speed)
		shard_groups.update(building_speed)		
		glass_panes.update(0, building_speed)
		buildings.update(building_speed)
		hero.update(building_speed)
		
		layer3.draw(screen)
		layer2.draw(screen)
		buildings.draw(screen)
		glass_panes.draw(screen)
		hero.draw(screen)
		shard_groups.draw(screen)
		
		pygame.display.update()


if __name__ == '__main__': main()
