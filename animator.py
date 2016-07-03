import glob
import os
import math

import bpy
from wand.image import Image


def blurimage(imagefilepath,blurimagefilepathdest,blurfactor=15):
    with Image (filename=imagefilepath) as img:
        with img.clone() as blurimg :
            blurimg.resize(img.width,img.height,'gaussian',blurfactor)
            blurimg.save(filename=blurimagefilepathdest)

def getallimagefilesfromdir (directory):
    listFile=[]
    listFile+=glob.glob(directory+'/*.jpg')
    listFile +=glob.glob(directory+'/*.jpeg')
    listFile +=glob.glob(directory+'/*.png')
    return listFile

def slideshowanimation(blenderImageCoupleList):
    frameAnimationStart = 0
    frameAnimationEnd = 23

    for imageCoupleObject in blenderImageCoupleList:



        imageCoupleObject[0].keyframe_insert(data_path="location", frame=frameAnimationStart)
        imageCoupleObject[1].keyframe_insert(data_path="location", frame=frameAnimationStart)
        imageCoupleObject[0].location = (0, imageCoupleObject[0].location[1], 0)
        imageCoupleObject[1].location = (0, imageCoupleObject[1].location[1]+0.01, 0)
        imageCoupleObject[1].scale = (3, 3, 1)
        imageCoupleObject[0].keyframe_insert(data_path="location", frame=frameAnimationStart+1)
        imageCoupleObject[1].keyframe_insert(data_path="location", frame=frameAnimationStart+1)


        imageCoupleObject[0].location = (0,imageCoupleObject[0].location[1]-0.5,0)
        imageCoupleObject[0].keyframe_insert(data_path="location", frame=frameAnimationEnd)


        imageCoupleObject[1].location = (0, imageCoupleObject[1].location[1]-0.25, 0)
        imageCoupleObject[1].keyframe_insert(data_path="location", frame=frameAnimationEnd)

        imageCoupleObject[0].location = (-10, imageCoupleObject[0].location[1], 0)
        imageCoupleObject[0].keyframe_insert(data_path="location", frame=frameAnimationEnd+1)

        imageCoupleObject[1].location = (-10, imageCoupleObject[1].location[1], 0)
        imageCoupleObject[1].keyframe_insert(data_path="location", frame=frameAnimationEnd+1)

        frameAnimationStart=frameAnimationEnd+1
        frameAnimationEnd+=24

def imagezlocationfitframe(imageobject):
    depth = 0.0
    imagedimension = imageobject.dimensions
    x = imagedimension[0]
    y = imagedimension[1]
    z = imagedimension[2]
    print(imagedimension)

    imageRatio = x/y
    if imageRatio>1:
        Ah =  math.atan(math.tan(math.radians(25) * (1080/1920)))
        depth = x / (math.tan(Ah) * 2)
    else:
        Ah = math.atan(math.tan(math.radians(25) * (1080 / 1920)))
        depth = y / (math.tan(Ah) * 2)

    return depth

def slideshow(imagePathList):
    coupleimagelist = []
    for imagePath in imagePathList:
        if os.path.exists(imagePath):
            imageblurfilepath = os.path.dirname(imagePath) + '/' + os.path.splitext(os.path.basename(imagePath))[0] + '_blurred' + os.path.splitext(os.path.basename(imagePath))[1]
            if not os.path.exists(imageblurfilepath):
                blurimage(imagePath,imageblurfilepath)
            coupleimagelist.append([imagePath,imageblurfilepath])
    i=0
    blenderImageCoupleList = []
    blenderImageCoupleObject = []

    for coupleimage in coupleimagelist :
        for image in coupleimage :

            imageObject = createImageAsPlane(image,(0,0,0),(1,1,1))
            depth = imagezlocationfitframe(imageObject)
            imageObject.location = (i,depth-0.2,0)
            blenderImageCoupleObject.append(imageObject)
            print (blenderImageCoupleObject)
        blenderImageCoupleList.append(blenderImageCoupleObject)
        blenderImageCoupleObject=[]
        i+=4

    print(blenderImageCoupleList)
    slideshowanimation(blenderImageCoupleList)


def createImageAsPlane(imageFilePath,location,scale):
    if os.path.exists(imageFilePath):
        bpy.ops.import_image.to_plane(alpha_mode='STRAIGHT',use_shadeless=True,files=[{'name': os.path.abspath(imageFilePath)}],directory=os.path.dirname(imageFilePath))
        imageObject=bpy.context.active_object
        imageObject.rotation_euler = [1.5708,0,0]
        imageObject.location = location
        imageObject.scale = scale
    return imageObject

imagefilepathlist = getallimagefilesfromdir('/home/belgaloo/PycharmProjects/sovibes/1465240806.958222')
slideshow(imagefilepathlist)