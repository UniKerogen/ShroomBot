import ikpy
import numpy as np
from ikpy import plot_utils
import matplotlib.pyplot as plt



PATH =  "/Users/Abdul./Desktop/Arm Base Assembly.SLDASM/urdf/Arm Base Assembly.SLDASM.urdf"
my_chain = ikpy.chain.Chain.from_urdf_file(PATH)

target_vector = [ 0.01, 0.1, 0.1]
target_frame = np.eye(4)
target_frame[:3, 3] = target_vector

print(my_chain)

print("The angles of each joints are : ", my_chain.inverse_kinematics(target_frame))

real_frame = my_chain.forward_kinematics(my_chain.inverse_kinematics(target_frame))
print("Computed position vector : %s, original position vector : %s" % (real_frame[:3, 3], target_frame[:3, 3]))

ax = plot_utils.init_3d_figure()
my_chain.plot(my_chain.inverse_kinematics(target_frame), ax, target=target_vector)
plt.xlim(-0.1, 0.1)
plt.ylim(-0.1, 0.1)
plt.show()