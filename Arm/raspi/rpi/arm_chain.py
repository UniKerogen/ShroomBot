

from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from ikpy import plot_utils
import math


# create the arm using IKpy's chain constructor with URDF links
# TODO: check length of each link could be wrong
#
arm = Chain(name="arm", links= [
    URDFLink(
        name = "base servo",
        translation_vector = [0, 0, 0],
        orientation = [ 0, 0, 0],
        rotation = [0, 0, 1],
        # bounds=(math.radians(0), math.radians(180))
        ),
    URDFLink(
        name = "elbow low",
        translation_vector = [0, 0, 8],
        orientation = [0, 0, 0],
        rotation = [0, 1, 0],
        bounds=(math.radians(-25), math.radians(90))
        ),
    URDFLink(
        name = "elbow hight",
        translation_vector = [0, 0, 2.5],
        orientation = [0, 0, 0],
        rotation = [0, 1, 0],
        bounds=(math.radians(-160), math.radians(36))
        ),

    URDFLink(
        name = "middle",
        translation_vector = [9, 0, 0],
        orientation = [0, 0, 0],
        rotation = [0, 1, 0],
        bounds=(math.radians(-110), math.radians(110))
        ),

    URDFLink(
        name = "wrist",
        translation_vector = [5.25, 0, 0],
        orientation = [0, 0, 0],
        rotation = [0, 1, 0],
        bounds=(math.radians(-120), math.radians(120))
        )
     
    # ,URDFLink(
    #     name = "end effector",
    #     translation_vector = [1, 0, 0],
    #     orientation = [0, 0, 0],
    #     rotation = [0, 1, 0])
])