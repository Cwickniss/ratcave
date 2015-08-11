__author__ = 'ratcave'

from psychopy import event
import ratcave
from ratcave.graphics import *
import pdb
import appdirs
import pickle
import copy
from os import path

def display(optitrack_ip="127.0.0.1"):

    # Connect to Optitrack
    tracker = ratcave.devices.Optitrack(client_ip=optitrack_ip)

    # Create Arena and cube
    reader = WavefrontReader(ratcave.graphics.resources.obj_arena)
    arena = reader.get_mesh('Arena', lighting=True)
    arena.load_texture(ratcave.graphics.resources.img_colorgrid)

    reader = WavefrontReader(ratcave.graphics.resources.obj_primitives)
    cube = reader.get_mesh('Sphere', lighting=True, scale=.02, centered=True)

    # Create Scene and Window
    scene = Scene(arena, cube)
    scene.camera = projector
    #scene.camera.rot_y = -89.5

    window = Window(scene, screen=1, fullscr=True)

    while True:

        # Update Everything's Position
        arena.position = tracker.rigid_bodies['Arena'].position
        arena.rotation = tracker.rigid_bodies['Arena'].rotation
        cube.position = tracker.rigid_bodies['CalibWand'].position
        scene.light.position = scene.camera.position

        # Re-Draw Everything
        window.draw()
        window.flip()

        # Check if keyboard pressed, and update camera parameters according to key pressed.
        keylist = event.getKeys()
        if len(keylist) > 0:
            if 'up' in keylist:
                scene.camera.z += .003
            elif 'down' in keylist:
                scene.camera.z -= .003
            elif 'left' in keylist:
                scene.camera.x += .003
            elif 'right' in keylist:
                scene.camera.x -= .003
            elif 'pageup' in keylist:
                scene.camera.y += .003
            elif 'pagedown' in keylist:
                scene.camera.y -= .01
            elif 'x' in keylist:
                scene.camera.fov_y += .01
            elif 'z' in keylist:
                scene.camera.fov_y -= .01
            elif 'w' in keylist:
                scene.camera.rot_x += .1
            elif 's' in keylist:
                scene.camera.rot_x -= .1
            elif 'd' in keylist:
                scene.camera.rot_z += .1
            elif 'a' in keylist:
                scene.camera.rot_z -= .1
            elif 'f' in keylist:
                scene.camera.rot_y += .1
            elif 'r' in keylist:
                scene.camera.rot_y -= .1
            elif 'escape' in keylist:
                window.close()
                break


            # Print the Following every time a key is detected:
            print "Camera settings:\n -shift: {0}, {1}\n -position: {2}\n -fov_y: {3}\n -rotation: {4}\n\n".format(
                scene.camera.x_shift, scene.camera.y_shift, scene.camera.position, scene.camera.fov_y, scene.camera.rotation)
            print("(Press Spacebar to update to new projector parameters")

            # If spacebar was pressed, save all.
            if 'space' in keylist:
                confirm = raw_input("Are you sure you want to save? (y/n)")
                if 'y' in confirm.lower():
                    proj_file = path.join(appdirs.user_data_dir("ratCAVE"), "projector_data.pickle")  # TODO: Use relative import to get data_dir from ratCAVE.__init__.py
                    data = {'position': scene.camera.position, 'rotation': scene.camera.rotation, 'fov_y': scene.camera.fov_y}
                    pickle.dump(data, open(proj_file, 'wb'))
                    print("New Data Saved.  Projector Values Overwritten.")
                    window.close()
                    break


if __name__ == '__main__':
    display()