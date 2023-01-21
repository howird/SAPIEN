import sapien.core as sapien
import numpy as np
import transforms3d.euler
from sapien.core import Pose
from sapien.sensor import ActiveLightSensorCUDA
import PIL.Image as im
import matplotlib.pyplot as plt
import time

from tqdm import trange

def main():
    sim = sapien.Engine()

    sapien.render_config.camera_shader_dir = "../vulkan_shader/rt"
    sapien.render_config.viewer_shader_dir = "../vulkan_shader/rt"
    sapien.render_config.rt_samples_per_pixel = 32
    sapien.render_config.rt_max_path_depth = 8
    sapien.render_config.rt_use_denoiser = True
    renderer = sapien.VulkanRenderer()

    # config = sapien.KuafuConfig()
    # config.spp = 32
    # config.max_bounces = 8
    # config.use_denoiser = True
    # renderer = sapien.KuafuRenderer(config)

    sim.set_renderer(renderer)

    scene_config = sapien.SceneConfig()
    scene = sim.create_scene(scene_config)

    ground_material = renderer.create_material()
    ground_material.base_color = np.array([202, 164, 114, 256]) / 256
    ground_material.specular = 0.5
    scene.add_ground(0, render_material=ground_material)
    scene.set_timestep(1 / 240)

    builder = scene.create_actor_builder()
    material = renderer.create_material()
    material.base_color = [0.2, 0.2, 0.8, 1.0]
    material.roughness = 0.5
    material.metallic = 0.0
    builder.add_sphere_visual(radius=0.06, material=material)
    builder.add_sphere_collision(radius=0.06)
    sphere1 = builder.build()
    sphere1.set_pose(Pose(p=[-0.05, 0.05, 0.06]))

    builder = scene.create_actor_builder()
    material = renderer.create_material()
    material.ior = 1.2
    material.transmission = 1.0
    material.base_color = [1.0, 1.0, 1.0, 1.0]
    material.roughness = 0.3
    material.metallic = 0.0
    # material.metallic = 0.1
    builder.add_sphere_visual(radius=0.07, material=material)
    builder.add_sphere_collision(radius=0.07)
    sphere2 = builder.build()
    sphere2.set_pose(Pose(p=[0.05, -0.05, 0.07]))

    builder = scene.create_actor_builder()
    material = renderer.create_material()
    material.base_color = [0.8, 0.7, 0.1, 1.0]
    material.roughness = 0.01
    material.metallic = 0.95
    builder.add_capsule_visual(radius=0.02, half_length=0.1, material=material)
    builder.add_capsule_collision(radius=0.02, half_length=0.1)
    cap = builder.build()
    cap.set_pose(Pose(p=[0.15, -0.01, 0.01], q=transforms3d.euler.euler2quat(0, 0, -0.7)))

    builder = scene.create_actor_builder()
    material = renderer.create_material()
    material.base_color = [0.8, 0.2, 0.2, 1.0]
    material.roughness = 0.01
    material.metallic = 1.0
    builder.add_box_visual(half_size=[0.09, 0.09, 0.09], material=material)
    builder.add_box_collision(half_size=[0.09, 0.09, 0.09])
    box = builder.build()
    box.set_pose(Pose(p=[0.05, 0.17, 0.09]))

    builder = scene.create_actor_builder()
    material = renderer.create_material()
    material.base_color = [0.9, 0.6, 0.5, 1.0]
    material.roughness = 0.0
    material.metallic = 1.0
    builder.add_visual_from_file(
        '../3rd_party/kuafu/resources/models/suzanne.dae', scale=[0.1, 0.1, 0.1], material=material)
    builder.add_box_collision(half_size=[0.1, 0.1, 0.1])
    box = builder.build()
    box.set_pose(Pose(p=[0.15, -0.25, 0.1], q=transforms3d.euler.euler2quat(0, 0, -1)))

    scene.set_ambient_light([0.3, 0.3, 0.3])
    scene.add_directional_light([0, 0.5, -1], color=[3.0, 3.0, 3.0])

    sensor_cuda = ActiveLightSensorCUDA(
        'sensor', renderer, scene, sensor_type='d415')
    sensor_cuda.depth_sensor.set_penalties(p1_penalty=7, p2_penalty=86)
    sensor_cuda.depth_sensor.set_uniqueness_ratio(15)

    sensor_cuda.set_pose(
        Pose([-0.28, -0.28, 0.46], [0.8876263, -0.135299, 0.3266407, 0.2951603]))

    # scene.step()
    # scene.update_render()
    # sensor_cuda.take_picture()
    # depth_cuda = sensor_cuda.get_depth()

    # rgb = sensor_cuda.get_rgb()
    # im.fromarray((rgb * 255).astype(np.uint8)).show()
    # start = time.process_time()
    # depth_cuda = sensor_cuda.get_depth()
    # print("Runtime of get_depth() for gpu sensor: ", time.process_time() - start)
    # plt.figure()
    # plt.imshow(depth_cuda)
    # plt.figure()
    # ir = sensor_cuda.get_ir()
    # print(np.sum(np.isnan(ir[0])))
    # plt.imshow(ir[0])
    # plt.show()


    from sapien.utils import Viewer
    viewer = Viewer(renderer)
    viewer.set_scene(scene)
    viewer.set_camera_xyz(x=-1, y=0, z=0.5)
    viewer.set_camera_rpy(r=0, p=-np.arctan2(2, 4), y=0)

    while not viewer.closed:
        scene.step()
        scene.update_render()
        viewer.render()
        tex = viewer.window.get_float_texture("Color")
        print(np.sum(np.isnan(tex)))


main()
