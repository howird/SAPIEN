"""Hello world for Sapien.

Concepts:
    1. Engine and scene
    2. Renderer, viewer, lighting
    3. Run a simulation loop

Notes:
    1. For one process, you can only create one engine and one renderer.
"""

import sapien.core as sapien
from sapien.utils import Viewer
import numpy as np


def main():
    engine = sapien.Engine()  # Create a physical simulation engine
    renderer = sapien.VulkanRenderer()  # Create a Vulkan renderer
    engine.set_renderer(renderer)  # Bind the renderer and the engine

    scene = engine.create_scene()  # Create an instance of simulation world (aka scene)
    scene.set_timestep(1 / 100.0)  # Set the simulation frequency

    # NOTE: How to build actors (rigid bodies) is elaborated in create_actors.py
    scene.add_ground(altitude=0)  # Add a ground
    actor_builder = scene.create_actor_builder()
    actor_builder.add_box_shape(pose=sapien.Pose(p=[0, 0, 0.5]),
                                half_size=[0.5, 0.5, 0.5])
    actor_builder.add_box_visual(pose=sapien.Pose(p=[0, 0, 0.5]),
                                 half_size=[0.5, 0.5, 0.5],
                                 color=[1., 0., 0.])
    box = actor_builder.build(name='box')  # Add a box

    viewer = Viewer(renderer)  # Create a viewer (window)
    viewer.set_scene(scene)  # Bind the viewer and the scene

    # The coordinate frame in Sapien is: x(forward), y(left), z(upward)
    # The principle axis of the camera is the x-axis
    viewer.set_camera_xyz(x=-4, y=0, z=2)
    # The rotation of the free camera is represented as [yaw(z), pitch(y), roll(x)]
    # The camera now looks at the origin
    viewer.set_camera_rpy(y=0, p=-np.arctan2(2, 4), r=0)
    viewer.window.set_camera_parameters(near=0.001, far=100, fovy=1)

    # Add some lights so that you can observe the scene
    scene.set_ambient_light([0.5, 0.5, 0.5])
    rscene = scene.get_render_scene()
    rscene.add_shadow_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

    while not viewer.closed:  # Press key q to quit
        scene.step()  # Simulate the world
        scene.update_render()  # Update the world to the renderer
        viewer.render()
    
    del scene


if __name__ == '__main__':
    main()
