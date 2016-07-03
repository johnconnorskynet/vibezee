from wand.display import display
from wand.image import Image

# with Image(filename='media download/wonderwoman.jpg') as img:
#     display(img)
#     with img.clone() as imgclone:
#         imgclone.resize(img.width,img.height,'gaussian',10)
#         imgclone.save(filename='media download/wonderwoman{0}.jpg'.format('resizeblur'))
#         display(imgclone)



def blurimage(imagefilepath,blurimagefilepathdest,blurfactor=15):
    with Image (filename=imagefilepath) as img:
        with img.clone() as blurimg :
            blurimg.resize(img.width,img.height,'gaussian',blurfactor)
            blurimg.save(filename=blurimagefilepathdest)
            # display(blurimg)

