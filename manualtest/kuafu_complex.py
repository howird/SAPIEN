import sapien.core as sapien
import numpy as np
from sapien.core import Pose
from transforms3d.quaternions import axangle2quat as aa
from transforms3d.quaternions import qmult, mat2quat, rotate_vector
import time


def main():
    sim = sapien.Engine()
    renderer = sapien.KuafuRenderer()
    renderer.set_assets_path('/zdata/anaconda3/envs/sapien/lib/python3.7/site-packages/sapien/kuafu_assets')
    sim.set_renderer(renderer)

    renderer.init()

    def create_ant_builder(scene):
        copper = renderer.create_material()
        copper.set_base_color([0.875, 0.553, 0.221, 1])
        copper.set_metallic(1)
        copper.set_roughness(0.2)

        builder = scene.create_articulation_builder()
        body = builder.create_link_builder()
        body.add_sphere_collision(Pose(), 0.25)
        body.add_sphere_visual(Pose(), 0.25, copper)
        body.add_capsule_collision(Pose([0.141, 0, 0]), 0.08, 0.141)
        body.add_capsule_visual(Pose([0.141, 0, 0]), 0.08, 0.141, copper)
        body.add_capsule_collision(Pose([-0.141, 0, 0]), 0.08, 0.141)
        body.add_capsule_visual(Pose([-0.141, 0, 0]), 0.08, 0.141, copper)
        body.add_capsule_collision(
            Pose([0, 0.141, 0], aa([0, 0, 1], np.pi / 2)), 0.08, 0.141
        )
        body.add_capsule_visual(
            Pose([0, 0.141, 0], aa([0, 0, 1], np.pi / 2)), 0.08, 0.141, copper
        )
        body.add_capsule_collision(
            Pose([0, -0.141, 0], aa([0, 0, 1], np.pi / 2)), 0.08, 0.141
        )
        body.add_capsule_visual(
            Pose([0, -0.141, 0], aa([0, 0, 1], np.pi / 2)), 0.08, 0.141, copper
        )
        body.set_name("body")

        l1 = builder.create_link_builder(body)
        l1.set_name("l1")
        l1.set_joint_name("j1")
        l1.set_joint_properties(
            "revolute",
            [[-0.5236, 0.5236]],
            Pose([0.282, 0, 0], [0.7071068, 0, 0.7071068, 0]),
            Pose([0.141, 0, 0], [-0.7071068, 0, 0.7071068, 0]),
            0.1,
        )
        l1.add_capsule_collision(Pose(), 0.08, 0.141)
        l1.add_capsule_visual(Pose(), 0.08, 0.141, copper)

        l2 = builder.create_link_builder(body)
        l2.set_name("l2")
        l2.set_joint_name("j2")
        l2.set_joint_properties(
            "revolute",
            [[-0.5236, 0.5236]],
            Pose([-0.282, 0, 0], [0, -0.7071068, 0, 0.7071068]),
            Pose([0.141, 0, 0], [-0.7071068, 0, 0.7071068, 0]),
            0.1,
        )
        l2.add_capsule_collision(Pose(), 0.08, 0.141)
        l2.add_capsule_visual(Pose(), 0.08, 0.141, copper)

        l3 = builder.create_link_builder(body)
        l3.set_name("l3")
        l3.set_joint_name("j3")
        l3.set_joint_properties(
            "revolute",
            [[-0.5236, 0.5236]],
            Pose([0, 0.282, 0], [0.5, -0.5, 0.5, 0.5]),
            Pose([0.141, 0, 0], [0.7071068, 0, -0.7071068, 0]),
            0.1,
        )
        l3.add_capsule_collision(Pose(), 0.08, 0.141)
        l3.add_capsule_visual(Pose(), 0.08, 0.141, copper)

        l4 = builder.create_link_builder(body)
        l4.set_name("l4")
        l4.set_joint_name("j4")
        l4.set_joint_properties(
            "revolute",
            [[-0.5236, 0.5236]],
            Pose([0, -0.282, 0], [0.5, 0.5, 0.5, -0.5]),
            Pose([0.141, 0, 0], [0.7071068, 0, -0.7071068, 0]),
            0.1,
        )
        l4.add_capsule_collision(Pose(), 0.08, 0.141)
        l4.add_capsule_visual(Pose(), 0.08, 0.141, copper)

        f1 = builder.create_link_builder(l1)
        f1.set_name("f1")
        f1.set_joint_name("j11")
        f1.set_joint_properties(
            "revolute",
            [[0.5236, 1.222]],
            Pose([-0.141, 0, 0], [0, 0.7071068, 0.7071068, 0]),
            Pose([0.282, 0, 0], [0, 0.7071068, 0.7071068, 0]),
            0.1,
        )
        f1.add_capsule_collision(Pose(), 0.08, 0.282)
        f1.add_capsule_visual(Pose(), 0.08, 0.282, copper)

        f2 = builder.create_link_builder(l2)
        f2.set_name("f2")
        f2.set_joint_name("j21")
        f2.set_joint_properties(
            "revolute",
            [[0.5236, 1.222]],
            Pose([-0.141, 0, 0], [0, 0.7071068, 0.7071068, 0]),
            Pose([0.282, 0, 0], [0, 0.7071068, 0.7071068, 0]),
            0.1,
        )
        f2.add_capsule_collision(Pose(), 0.08, 0.282)
        f2.add_capsule_visual(Pose(), 0.08, 0.282, copper)

        f3 = builder.create_link_builder(l3)
        f3.set_name("f3")
        f3.set_joint_name("j31")
        f3.set_joint_properties(
            "revolute",
            [[0.5236, 1.222]],
            Pose([-0.141, 0, 0], [0, 0.7071068, 0.7071068, 0]),
            Pose([0.282, 0, 0], [0, 0.7071068, 0.7071068, 0]),
            0.1,
        )
        f2.add_capsule_collision(Pose(), 0.08, 0.282)
        f3.add_capsule_visual(Pose(), 0.08, 0.282, copper)

        f4 = builder.create_link_builder(l4)
        f4.set_name("f4")
        f4.set_joint_name("j41")
        f4.set_joint_properties(
            "revolute",
            [[0.5236, 1.222]],
            Pose([-0.141, 0, 0], [0, 0.7071068, 0.7071068, 0]),
            Pose([0.282, 0, 0], [0, 0.7071068, 0.7071068, 0]),
            0.1,
        )
        f2.add_capsule_collision(Pose(), 0.08, 0.282)
        f4.add_capsule_visual(Pose(), 0.08, 0.282, copper)

        return builder

    config = sapien.SceneConfig()
    scene = sim.create_scene(config)
    scene.add_ground(0)
    scene.set_timestep(1 / 240)

    mount = scene.create_actor_builder().build_kinematic()
    mount.set_pose(Pose([0, 0, 3], qmult(aa([0, 0, 1], 0.0), aa([0, 1, 0], 0.0))))
    cam1 = scene.add_mounted_camera("cam", mount, Pose([0, 0, 3]), 1920, 1080, 0, 1, 0.1, 100)

    # print(cam1.render_target_names)

    ant_builder = create_ant_builder(scene)
    ant = ant_builder.build()
    ant.set_root_pose(Pose([0, 0, 5]))

    # viewer.set_scene(scene)
    # viewer.set_camera_xyz(-4, 0, 0.3)
    # viewer.window.set_camera_parameters(0.1, 1000, 1)

    scene.step()
    ant.set_qpos([0, 0, 0, 0, 0.7, 0.7, 0.7, 0.7])
    ant.set_qvel([0] * 8)
    f = [0.1] * 8
    acc = ant.compute_forward_dynamics([0.1] * 8)
    ant.set_qf(f)
    scene.step()

    # scene.renderer_scene.set_ambient_light([0, 0, 0])

    dirlight = scene.add_directional_light([0, 0, -1], [0.3, 0.3, 0.3], True)

    # scene.renderer_scene.add_point_light([0, 1, 1], [1, 2, 2], True)

    # light = scene.renderer_scene.add_spot_light(
    #     [0, 0, 2], [0, 0, -1], np.pi / 2, [1, 1, 1], True
    # )

    # light.set_position([0, 0, 0.1])
    # light.set_direction([0, -100, -1])
    # light.set_color([100, 100, 100])
    # light.set_shadow_parameters(1, 100)

    # light.set_position([0, 0, 5])
    # light.set_direction([0, -1, -1])

    plight = scene.add_point_light([0, -1, 1], [2, 1, 2], True)
    # scene.renderer_scene.add_point_light([0, 1, -1], [2, 2, 1])

    print(scene.get_all_lights())

    while True:
        cam1.take_picture()

    # count = 0
    # while not viewer.closed:
    #     for i in range(4):
    #         scene.step()
    #     scene.update_render()
    #     viewer.render()
    #     count += 1

    # if count == 120:
    #     for light in scene.get_all_lights():
    #         scene.remove_light(light)

    # if count == 120:
    #     start = time.time()
    #     cam1.take_picture()
    #     img = cam1.get_dl_tensor("Color")
    #     img = torch.utils.dlpack.from_dlpack(img)
    #     dur = time.time() - start
    #     print("Render to tensor FPS: ", 1 / dur)

    #     import matplotlib.pyplot as plt
    #     plt.imshow(img.cpu().numpy())
    #     plt.show()

    #     start = time.time()
    #     cam2.take_picture()
    #     img = cam2.get_dl_tensor("Color")
    #     img = torch.utils.dlpack.from_dlpack(img)
    #     dur = time.time() - start
    #     print("Render to tensor FPS: ", 1 / dur)

    #     import matplotlib.pyplot as plt
    #     plt.imshow(img.cpu().numpy())
    #     plt.show()

    # import time
    # start = time.time()
    # cam.take_picture()
    # img = cam.get_float_texture("Color")
    # torch.tensor(img, device="cuda")
    # dur = time.time() - start
    # print("Torch CPU round trip FPS: ", 1 / dur)

    # viewer.close()


main()

# TODO: get targets on camera
