import subprocess
import os
from editables import *
import time

print('Starting Reconstruction...')
tic = time.clock()
#starting OpenMVG
command = "openMVG_main_SfMInit_ImageListing -i '{}' -d '{}' -o '{}' ".format(image_dir,camera_dir,matches_dir)
process = subprocess.call(command, shell=True)

command = "openMVG_main_ComputeFeatures -i '{}' -o '{}'".format(matches_dir + '/sfm_data.json',matches_dir)
process = subprocess.call(command, shell=True)

command = "openMVG_main_ComputeMatches -i '{}' -o '{}'".format(matches_dir + '/sfm_data.json',matches_dir)
process = subprocess.call(command, shell=True)

command = "openMVG_main_IncrementalSfM -i '{}' -m '{}' -o '{}'".format(matches_dir + '/sfm_data.json',matches_dir,output_dir)
process = subprocess.call(command, shell=True)

command = "openMVG_main_openMVG2openMVS -i '{}' -o 'scene.mvs'".format(output_dir + '/sfm_data.bin')
process = subprocess.call(command, shell=True)

print('Starting OpenMVS...')
#starting OpenMVS

os.chdir(output_dir)
command = "DensifyPointCloud scene.mvs"
process = subprocess.call(command, shell=True)

command = "ReconstructMesh scene_dense.mvs"
process = subprocess.call(command, shell=True)

command = "TextureMesh scene_dense_mesh.mvs"
process = subprocess.call(command, shell=True)

toc = time.clock()
print('Completed in {} minutes').format( (toc - tic)/60 )
