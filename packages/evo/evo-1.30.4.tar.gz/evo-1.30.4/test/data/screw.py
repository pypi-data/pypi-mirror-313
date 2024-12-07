import numpy as np

from evo.core import lie_algebra as lie
from evo.core.trajectory import PosePath3D

o = lie.se3()

r = lie.so3_exp([0, 0, 0.4])
t = lie.se3(r=r, t=np.array([0.25, 0., 0.05]))

o = o.dot(t)

poses = []
for i in range(40):
    if i == 0:
        poses.append(o)
        continue
    poses.append(poses[i - 1].dot(t))

traj = PosePath3D(poses_se3=poses)

from evo.tools import file_interface
file_interface.write_kitti_poses_file("reference.txt", traj)
