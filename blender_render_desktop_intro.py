import argparse
import json
import os
import bpy
import sys
import blender_utils

def formatString(string,lenLineMax):
    splitString =  string.split()
    lenSplitString = splitString.__len__()
    len =0
    for n in range(0,lenSplitString-1):
        splitString[n]+=' '
        len+=splitString[n].__len__()
        if(len>lenLineMax):
            splitString[n-1]+="\n"
            len=splitString[n].__len__()

    return splitString

# Initialize scene
def initSceneDesktopPattern(args):

    jsonFilePath = os.path.abspath(args.input)

    with open(jsonFilePath) as blender_data_file:
        blender_data = json.load(blender_data_file)
        for blender_object in blender_data['blender_objects']:
            # Create Text
            if(blender_object['type']=='text'):

                string = blender_object['string']
                # TODO check max length
                if blender_object.get('max_char_length_x'):
                    string = ''.join(formatString(string,blender_object['max_char_length_x']))

                location = (blender_object['origin_location']['x'],blender_object['origin_location']['y'],blender_object['origin_location']['z'])
                scale = (blender_object['scale']['x'],blender_object['scale']['y'],blender_object['scale']['z'])
                material = blender_object['material']

                if bpy.data.materials.get(material) is not None:
                    blenderMmaterial = bpy.data.materials[material]
                    textObject = blender_utils.createText(string, location, scale, blenderMmaterial)
                    # TODO:FACTOR CODE
                    if blender_object.get('final_location'):
                        frameAnimationStart = blender_object['frame_animation_start']
                        frameAnimationEnd = blender_object['frame_animation_end']
                        finalLocation =  (blender_object['final_location']['x'],blender_object['final_location']['y'],blender_object['final_location']['z'])
                        blender_utils.animateTranslateObject(textObject,frameAnimationStart,frameAnimationEnd,finalLocation)

            # Create image as plane
            elif(blender_object['type']=='images_as_plane'):
                imageFilePath = blender_object['image_file_path']
                location = (blender_object['origin_location']['x'],blender_object['origin_location']['y'],blender_object['origin_location']['z'])
                scale = (blender_object['scale']['x'],blender_object['scale']['y'],blender_object['scale']['z'])
                imageObject = blender_utils.createImageAsPlane(imageFilePath,location,scale)
                # TODO:FACTOR CODE
                if blender_object.get('final_location'):
                    frameAnimationStart = blender_object['frame_animation_start']
                    frameAnimationEnd = blender_object['frame_animation_end']
                    finalLocation =  (blender_object['final_location']['x'],blender_object['final_location']['y'],blender_object['final_location']['z'])
                    blender_utils.animateTranslateObject(imageObject,frameAnimationStart,frameAnimationEnd,finalLocation)


def renderScene(args):

    # Initialize scene/camera
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = args.fps * args.time
    scene.render.image_settings.file_format = args.file_format
    scene.render.ffmpeg.codec = args.codec
    scene.render.ffmpeg.format = args.format
    scene.render.filepath = args.output
    print(args.output)
    bpy.ops.render.render(animation=True, write_still=True)
    pass



# Parse command line
class ArgumentParserError(Exception):
    pass

class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(message)
        raise ArgumentParserError(message)

parser = ThrowingArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    'input',
    help="Path to blender object scene description")
parser.add_argument(
    '-o', '--output', default='/tmp/',
    help="Output file")
parser.add_argument(
    '-r', '--resolution', default='640x360',
    help="Output resolution width x height")
parser.add_argument(
    '--fps', type=int, default=24,
    help="Frame per second")
parser.add_argument(
    '-t', '--time', type=int, default='5',
    help="Duration of the video in second")
parser.add_argument(
    '-ff', '--file-format', default='FFMPEG',
    help="Blender file format")
parser.add_argument(
    '-f', '--format', default='MPEG4',
    help="Blender format")
parser.add_argument(
    '-c', '--codec', default='MPEG4',
    help="Blender codec")

if '--' in sys.argv:
    argv = sys.argv
    sys.argv = [' '.join(argv[:argv.index('--')])] + argv[argv.index('--')+1:]
else:
    sys.argv = [' '.join(sys.argv)]

try:
    initSceneDesktopPattern(parser.parse_args())
    renderScene(parser.parse_args())
except ArgumentParserError:
    pass
except SystemExit:
    pass
