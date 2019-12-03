

from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from ikpy import plot_utils
import numpy as np
import math

my_chain = Chain(name='left_arm', links=[
    # OriginLink(),
    URDFLink(
      name="base",
      translation_vector=[0, 0, 0],
      orientation=[0, 0, 0.],
      rotation=[0, 0, 1],
      bounds = (90, 45)
    ),
    URDFLink(
      name="elbo",
      translation_vector=[0, 0, 0.5],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
      bounds = (0, 1)

    ),
    URDFLink(
      name="wrist",
      translation_vector=[0.5, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
      bounds = (0, 30)
    ),
    URDFLink(
      name="EOF",
      translation_vector=[0.5, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
      # bounds = (0, 0)

      )
    
])

# blue
#
target_vector = [0.4, 0.8, .2]
target_frame = np.eye(4)
target_frame[:3, 3] = target_vector


angles = my_chain.inverse_kinematics(target_frame)
for (i, angle) in enumerate(angles):
    angles[i] = math.degrees(angle)
    print("angle({}) = {} deg, {} pos".format(i, angles[i], int(angles[i]/0.24)))
    
real_frame = my_chain.forward_kinematics(my_chain.inverse_kinematics(target_frame))
print("Computed position vector : %s, original position vector : %s" % (real_frame[:3, 3], target_frame[:3, 3]))

import matplotlib.pyplot as plt
ax = plot_utils.init_3d_figure()

my_chain.plot(my_chain.inverse_kinematics(target_frame), ax, target=target_vector)

print("-------yellow--------")

# yellow
#
target_vector = [0.4, 0.8, 0]
target_frame = np.eye(4)
target_frame[:3, 3] = target_vector

angles = my_chain.inverse_kinematics(target_frame)
for (i, angle) in enumerate(angles):
    angles[i] = math.degrees(angle)
    print("angle({}) = {} deg, {} pos".format(i, angles[i], int(angles[i]/0.24)))
my_chain.plot(my_chain.inverse_kinematics(target_frame), ax, target=target_vector)


plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.show()