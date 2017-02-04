import mcpi.minecraft as minecraft
import mcpi.block as block
import random
import time

mc = minecraft.Minecraft.create()
pos = mc.player.getTilePos()

#detonation height
HEIGHT = 20

#flickering out of firework height
FLICKER = int(HEIGHT * 0.5)

#block ids
TNT = 46
STONE = block.STONE.id
AIR = block.AIR.id
WOOL = 35
WOOD_PLANKS = 5

#Wool colors
WOOL_COLORS = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] #unused
WHITE = 0
ORANGE = 1
MAGENTA = 2
LT_BLUE = 3
YELLOW = 4
LIME = 5
PINK = 6
GREY = 7
LT_GREY = 8
CYAN = 9
PURPLE = 10
BLUE = 11
BROWN = 12
GREEN = 13
RED = 14
BLACK = 15

mc.postToChat("Fireworks, 1v")
time.sleep(1)
mc.postToChat("Strike the concrete trigger to launch!")

#saved location
orgX, orgY, orgZ = pos.x, pos.y, pos.z

#the trigger
triggerX, triggerY, triggerZ = orgX+5, orgY, orgZ
mc.setBlock(triggerX,triggerY,triggerZ,STONE)

#the gantry
mc.setBlocks(orgX+6, orgY, orgZ-1, orgX+6, orgY+1, orgZ+1, WOOD_PLANKS)
mc.setBlocks(orgX+7, orgY, orgZ+1, orgX+7, orgY+1, orgZ+1, WOOD_PLANKS)
mc.setBlocks(orgX+7, orgY, orgZ-1, orgX+7, orgY+1, orgZ-1, WOOD_PLANKS)
mc.setBlocks(orgX+8, orgY, orgZ-1, orgX+8, orgY+1, orgZ+1, WOOD_PLANKS)

#the rocket
rocketSpeed = 1 #in blocks
rocketBottom, rocketTop, rocketX, rocketZ = orgY, orgY+1, orgX+7, orgZ
mc.setBlocks(rocketX, rocketBottom, rocketZ, rocketX, rocketTop, rocketZ, TNT)
shards = []

class Rocket():
    """Class to maintain rockets"""
    pass

class Shard():
    """Class to hold shards from firework"""

    def __init__(self, rocketX, rocketTop, rocketZ):
        """Initialize and draw shard to game"""
        super(Shard, self).__init__()
        self.X = rocketX
        self.Y = rocketTop
        self.Z = rocketZ
        self.D6 = 0
        self.D15 = random.randint(1,15)
        mc.setBlock(self.X, self.Y, self.Z, WOOL, ORANGE)

    def updateShard(self):
        """Cause Shards to flicker and fall"""
        mc.setBlock(self.X,self.Y, self.Z, AIR)
        time.sleep(0.02)
        self.Y -= 1
        self.D6 = random.randint(1,6)
        if self.D6 == 1 or self.D6 == 2:
            self.X += 1
        elif self.D6 == 3 or self.D6 == 4:
            self.X -= 1
        elif self.D6 == 5:
            self.Z += 1
        elif self.D6 == 6:
            self.Z -= 1
        mc.setBlock(self.X,self.Y, self.Z, WOOL, self.D15)
        time.sleep(0.05)

    def endShard(self):
        """Cause shards to disappear"""
        mc.setBlock(self.X,self.Y, self.Z, AIR)

while True:
    for hitBlock in mc.events.pollBlockHits():
        #verify that hitBlock is the trigger
        if (hitBlock.pos.x == triggerX) and (hitBlock.pos.y == triggerY) and (hitBlock.pos.z == triggerZ):
            print("Launch")
            while rocketTop < HEIGHT:
                mc.setBlocks(rocketX, rocketBottom, rocketZ, rocketX, rocketTop, rocketZ, TNT)
                rocketBottom += rocketSpeed
                rocketTop += rocketSpeed
                mc.setBlocks(rocketX, rocketBottom, rocketZ, rocketX, rocketTop, rocketZ, TNT)
                mc.setBlock(rocketX, rocketBottom-1, rocketZ, AIR)
                time.sleep(0.2)
            if rocketTop == HEIGHT:
                print("Explosion!")
                mc.setBlocks(rocketX,rocketBottom, rocketZ, rocketX, rocketTop, rocketTop, AIR)
                time.sleep(0.2)
                #Initialize/draw shards
                shard0 = Shard(rocketX, rocketTop, rocketZ)
                shard1 = Shard(rocketX+2, rocketTop, rocketZ)
                shard2 = Shard(rocketX-2, rocketTop, rocketZ)
                shard3 = Shard(rocketX, rocketTop + 2, rocketZ)
                shard4 = Shard(rocketX, rocketTop - 2, rocketZ)
                shard5 = Shard(rocketX, rocketTop, rocketZ + 2)
                shard6 = Shard(rocketX, rocketTop, rocketZ - 2)
                shards.append(shard0)
                shards.append(shard1)
                shards.append(shard2)
                shards.append(shard3)
                shards.append(shard4)
                shards.append(shard5)
                shards.append(shard6)
                while shard0.Y > FLICKER: #shards above dissipation height
                    for shard in shards:
                        shard.updateShard()
            if shard0.Y == FLICKER:
                #Return to original parameters
                print("New Rocket")
                rocketBottom = orgY
                rocketTop = orgY+1
                for shard in shards:
                    shard.endShard()
                shards = []
                mc.setBlocks(rocketX, rocketBottom, rocketZ, rocketX, rocketTop, rocketZ, TNT)
