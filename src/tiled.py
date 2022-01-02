from .game_object   import *
from .wall          import *
from .shared        import *
from .decoration    import *
from math          import floor
import xml.etree.ElementTree as et

# TODO - optimize, this is really slow
class TiledManager():
    def load_map(self, filename):
        tree = et.parse(filename)
        root = tree.getroot()

        if root.attrib['version'] != '1.2':
            print('WARNING: xml version != 1.2 may not work properly')

        if root.attrib['tiledversion'] != '1.2.4':
            print('WARNING: tiled version != 1.2.4 may not work properly')

        tilewidth   =   int(root.attrib['tilewidth'])
        tileheight  =   int(root.attrib['tileheight'])
        currentlayer = 0

        for obj in root:
            if obj.tag == 'tileset':
                temptree    =   et.parse(basedir + 'data/maps/'+obj.attrib['source'])
                temproot    =   temptree.getroot()
                for item in temproot:
                    if item.tag == 'image':
                        #TODO handle this path properly
                        tileset         =   pygame.image.load(basedir + 'data/maps/dungeon_ v1.0/' +  item.attrib['source'] ).convert_alpha()
                        tilesetwidth    =   int(item.attrib['width'])
                        tilesetheight   =   int(item.attrib['height'])

            elif obj.tag == 'layer':
                try:
                    if obj.attrib['visible'] == '0':
                        continue
                except:
                    print(f"WARNING: layer {obj.attrib['id']} visible by default ")
                currentlayer += 1
                if currentlayer != collision_layer:
                    for subobj in obj:
                        if subobj.tag == 'data' and subobj.attrib['encoding'] == 'csv':
                            for sso in subobj:
                                if sso.tag == 'chunk':
                                    x = 0
                                    y = -1
                                    chunkwidth = int(sso.attrib['width'])
                                    chunkheight = int(sso.attrib['height'])
                                    chunk = Decoration()
                                    chunk.name = obj.attrib['name'] + ' X' + sso.attrib['x'] + ' Y' + sso.attrib['y']
                                    chunk.layer = currentlayer
                                    chunk.position.x = int(sso.attrib['x'])*tilewidth
                                    chunk.position.y = int(sso.attrib['y'])*tileheight
                                    chunk.animation_spritesheet = Surface((tilewidth*chunkwidth, tileheight*chunkheight), pygame.SRCALPHA, 32)
                                    chunk.set_size(Vector2(chunk.animation_spritesheet.get_size()))
                                    chunk.surface = Surface((chunk.size.x, chunk.size.y), pygame.SRCALPHA, 32)

                                    for line in sso.text.split('\n'):
                                        for block in line.split(','):
                                            if block == '':
                                                continue
                                            else:
                                                blockcode = int(block)
                                                if blockcode != 0:
                                                    blockcode -= 1
                                                    temprect = Rect( (blockcode%(tilesetwidth/tilewidth))*tilewidth , floor(blockcode/(tilesetwidth/tilewidth))*tileheight,tilewidth,tileheight)
                                                    chunk.animation_spritesheet.blit(tileset, (x*tilewidth, y*tileheight), temprect)
                                                x += 1
                                                x %= chunkwidth
                                        y += 1
                                        y %= chunkheight
                else:
                    for subobj in obj:
                        if subobj.tag == 'data' and subobj.attrib['encoding'] == 'csv':
                            for sso in subobj:
                                if sso.tag == 'chunk':
                                    x = 0
                                    y = -1
                                    chunkwidth = int(sso.attrib['width'])
                                    chunkheight = int(sso.attrib['height'])
                                    for line in sso.text.split('\n'):
                                        for block in line.split(','):
                                            if block == '':
                                                continue
                                            else:
                                                blockcode = int(block)
                                                if blockcode != 0:
                                                    blockcode -= 1
                                                    block = Decoration()
                                                    block.layer = currentlayer
                                                    block.position.x = int(sso.attrib['x'])*tilewidth + x*tilewidth
                                                    block.position.y = int(sso.attrib['y'])*tilewidth + y*tileheight
                                                    block.animation_spritesheet = Surface((tilewidth, tileheight), pygame.SRCALPHA, 32)
                                                    block.set_size(Vector2(block.animation_spritesheet.get_size()))
                                                    block.surface = Surface((block.size.x, block.size.y), pygame.SRCALPHA, 32)
                                                    temprect = Rect( (blockcode%(tilesetwidth/tilewidth))*tilewidth , floor(blockcode/(tilesetwidth/tilewidth))*tileheight,tilewidth,tileheight)
                                                    block.animation_spritesheet.blit(tileset, (0,0), temprect)
                                                x += 1
                                                x %= chunkwidth
                                        y += 1
                                        y %= chunkheight
            elif obj.tag == 'objectgroup':
                for subobj in obj:
                    if not list(subobj):    #rectangle
                        wall = Wall()
                        wall.position.x = int(subobj.attrib['x'])
                        wall.position.y = int(subobj.attrib['y'])
                        try:
                            width = int(subobj.attrib['width'])
                            height = int(subobj.attrib['height'])
                        except KeyError:
                            width = tilewidth
                            height = tileheight
                        wall.animation_spritesheet = Surface( (width, height), pygame.SRCALPHA, 32)
                        wall.set_size(Vector2(wall.animation_spritesheet.get_size()))
                        wall.surface = Surface((wall.size.x, wall.size.y), pygame.SRCALPHA, 32)
                    elif subobj[0].tag == 'point':
                        wall = Wall()
                        wall.position.x = int(subobj.attrib['x'])
                        wall.position.y = int(subobj.attrib['y'])
                        wall.animation_spritesheet = Surface( (1,1), pygame.SRCALPHA, 32)
                        wall.set_size(Vector2(wall.animation_spritesheet.get_size()))
                        wall.surface = Surface((wall.size.x, wall.size.y), pygame.SRCALPHA, 32)
                    elif subobj[0].tag == 'ellipse':
                        print('ERROR: ellipse objects not implemented')
                    elif subobj[0].tag == 'polygon':
                        print('ERROR: polygon objects not implemented')
    def save_map(self):
        print('ERROR: saving map not implemented yet')
