import sapien.core as sapien
import numpy as np
from sapien.core import Pose
from transforms3d.quaternions import axangle2quat as aa
from transforms3d.quaternions import qmult, mat2quat, rotate_vector

import sapien.core.pysapien.renderer as R
from sapien.asset import download_partnet_mobility, create_dome_envmap

from sapien.utils import Viewer


def create_table(
    scene: sapien.Scene,
    pose: sapien.Pose,
    size,
    height,
    thickness=0.1,
    color=(0.8, 0.6, 0.4),
    name="table",
) -> sapien.Actor:
    """Create a table (a collection of collision and visual shapes)."""
    builder = scene.create_actor_builder()

    # Tabletop
    tabletop_pose = sapien.Pose(
        [0.0, 0.0, -thickness / 2]
    )  # Make the top surface's z equal to 0
    tabletop_half_size = [size / 2, size / 2, thickness / 2]
    builder.add_box_shape(pose=tabletop_pose, half_size=tabletop_half_size)
    builder.add_box_visual(
        pose=tabletop_pose, half_size=tabletop_half_size, color=color
    )

    # Table legs (x4)
    for i in [-1, 1]:
        for j in [-1, 1]:
            x = i * (size - thickness) / 2
            y = j * (size - thickness) / 2
            table_leg_pose = sapien.Pose([x, y, -height / 2])
            table_leg_half_size = [thickness / 2, thickness / 2, height / 2]
            builder.add_box_shape(pose=table_leg_pose, half_size=table_leg_half_size)
            builder.add_box_visual(
                pose=table_leg_pose, half_size=table_leg_half_size, color=color
            )

    table = builder.build(name=name)
    table.set_pose(pose)
    return table


def main():

    sapien.SapienRenderer.set_log_level("info")

    sim = sapien.Engine()
    renderer = sapien.SapienRenderer(default_mipmap_levels=4)
    renderer_context: R.Context = renderer._internal_context
    sim.set_renderer(renderer)

    copper = renderer.create_material()
    copper.set_base_color([0.875, 0.553, 0.221, 1])
    copper.set_metallic(1)
    copper.set_roughness(0.2)

    viewer = Viewer(renderer)

    def create_ant_builder(scene):
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
        f3.add_capsule_collision(Pose(), 0.08, 0.282)
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
        f4.add_capsule_collision(Pose(), 0.08, 0.282)
        f4.add_capsule_visual(Pose(), 0.08, 0.282, copper)

        return builder

    config = sapien.SceneConfig()
    scene = sim.create_scene(config)
    scene.add_ground(0)
    scene.set_timestep(1 / 240)

    scene.set_environment_map(create_dome_envmap())

    mount = scene.create_actor_builder().build_kinematic()
    mount.set_pose(Pose([-3, 0, 2], qmult(aa([0, 0, 1], 0.3), aa([0, 1, 0], 0.5))))
    cam1 = scene.add_mounted_camera("cam", mount, Pose(), 1920, 1080, 0, 1, 0.1, 100)

    print(cam1.get_projection_matrix())


    mount = scene.create_actor_builder().build_kinematic()
    mount.set_pose(Pose([-3, 0, 2], qmult(aa([0, 0, 1], 0.3), aa([0, 1, 0], 0.5))))
    cam2 = scene.add_mounted_camera("cam", mount, Pose(), 1920, 1080, 0, 1, 0.1, 100)

    ant_builder = create_ant_builder(scene)
    ant = ant_builder.build()
    ant.set_root_pose(Pose([0, 0, 5]))
    for v in ant.get_links()[0].get_visual_bodies():
        v.shade_flat = True

    loader = scene.create_urdf_loader()
    loader.fix_root_link = True
    robot = loader.load("../assets/robot/movo/movo.urdf")
    robot.set_pose(sapien.Pose([-1, 0, 0]))
    robot.get_qpos()

    viewer.set_scene(scene)
    viewer.set_camera_xyz(-4, 0, 0.3)
    viewer.window.set_camera_parameters(0.1, 1000, 1)

    scene.step()
    ant.set_qpos([0, 0, 0, 0, 0.7, 0.7, 0.7, 0.7])
    ant.set_qvel([0] * 8)
    f = [0.1] * 8
    acc = ant.compute_forward_dynamics([0.1] * 8)
    ant.set_qf(f)
    scene.step()

    dirlight = scene.add_directional_light([0, 0, -1], [0.3, 0.3, 0.3], True)

    light = scene.add_active_light(
        Pose([0, 0, 1]),
        [10, 10, 10],
        np.pi / 2,
        "../3rd_party/sapien-vulkan-2/test/assets/image/flashlight.jpg",
    )

    plight = scene.add_point_light([0, -1, 1], [2, 1, 2], True)

    count = 0
    while not viewer.closed:
        for i in range(4):
            scene.step()
        scene.update_render()
        viewer.render()
        count += 1
        robot.get_qpos()

    viewer.close()


main()

# TODO: get targets on camera
