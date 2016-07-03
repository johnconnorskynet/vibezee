import bpy
import os
import datetime

# Set a material to a blender object
def setMaterial(object, material):
    objectData = object.data
    objectData.materials.append(material)

# Create text object with parameters : text,location,scale and material
# TODO: add rotation parameter
def createText(string,location,scale,material):
    bpy.ops.object.text_add(enter_editmode=True,location=location,rotation=(1.5708,0,0))
    bpy.ops.font.delete()
    bpy.ops.font.text_insert(text=string)
    bpy.ops.object.editmode_toggle()
    textObject = bpy.context.active_object
    textObject.scale =scale
    setMaterial(textObject,material)
    return textObject

# Create image as plane object
# TODO: add rotation parameter
def createImageAsPlane(imageFilePath,location,scale):
    if os.path.exists(imageFilePath):
        bpy.ops.import_image.to_plane(alpha_mode='STRAIGHT',use_shadeless=True,files=[{'name': os.path.abspath(imageFilePath)}],directory=os.path.dirname(imageFilePath))
        imageObject=bpy.context.active_object
        imageObject.rotation_euler = [1.5708,0,0]
        imageObject.location = location
        imageObject.scale = scale
        return imageObject

# Animate object
def animateTranslateObject(blenderObject,frameAnimationStart, frameAnimationEnd, finalLocation):
    blenderObject.keyframe_insert(data_path="location",frame=frameAnimationStart)
    blenderObject.location = finalLocation
    blenderObject.keyframe_insert(data_path="location",frame=frameAnimationEnd)