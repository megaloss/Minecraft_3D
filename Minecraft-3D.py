from numpy import asarray, rot90
import numpy as np
import trimesh
#from PIL import Image

dry_run=False ## Change this to False to execute creating for real


startx=60 ## Positions to start building in Minecraft world
starty=78
startz=60
block_type=1 # Tyfe of block used (41 is gold)



if dry_run==False:
    from mcpi import minecraft
    ## connecting using ip and port for your Spigot server + RaspberryJuice mod installed
    mc = minecraft.Minecraft.create(address="192.168.0.15", port=4712)


mesh = trimesh.load_mesh('/home/yurick/Eiffel.stl') ## This is a 3d - model file from Thingiverse
assert(mesh.is_watertight) # you cannot build a solid if your volume is not tight
volume = mesh.voxelized(pitch=2) ## we make it twice smaller here
mat = volume.matrix # matrix of boolean
m=rot90(asarray(mat),3,axes=(2, 1)) ##rotate to correct(vertical) position



#from IPython.display import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

### Let's show the model we are creating !
# prepare some coordinates
x, y, z = np.indices((8, 8, 8))
# draw cuboids in the top left and bottom right corners, and a link between them
cube1 = (x < 3) & (y < 3) & (z < 3)
# combine the objects into a single boolean array
voxels = cube1
# and plot everything
fig = plt.figure(figsize=((20,20)))
ax = fig.gca(projection='3d', ymargin=0.2)
ax.voxels (mat,  edgecolor='k')
plt.show()
### Let's build in Minecraft world !
if dry_run==False:
    mc.setBlocks(startx,starty,startz,startx+m.shape[0],starty+m.shape[1],startz+m.shape[2],0)
    for ix,x in enumerate (m):

        for iy,y in enumerate (x):

            for iz,z in enumerate(y):
                if z:
                    mc.setBlock(startx+ix,m.shape[1]+starty-iy,startz+iz,block_type)


    mc.player.setPos(startx-5, starty+1, startz-5)# let's send a player to see what we have built

#print (mat.shape)
