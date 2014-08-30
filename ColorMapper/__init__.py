from itertools import product
from math import sqrt
from PIL import Image
import numpy

def rgb2xy(r, g, b, step=4):
    '''
    >>> rgb2xy(0, 0, 0, step=4)
    (0, 0)
    >>> rgb2xy(0, 0, 255, step=4)
    (63, 0)
    >>> rgb2xy(0, 255, 0, step=4)
    (0, 63)
    >>> rgb2xy(0, 255, 255, step=4)
    (63, 63)
    >>> rgb2xy(128, 128, 128, step=4)
    (32, 288)
    >>> rgb2xy(255, 0, 0, step=4)
    (448, 448)
    >>> rgb2xy(255, 0, 255, step=4)
    (511, 448)
    >>> rgb2xy(255, 255, 0, step=4)
    (448, 511)
    >>> rgb2xy(255, 255, 255, step=4)
    (511, 511)
    '''
    x = b / step
    y = (g % 256) / step

    # xr = r / step
    # yr = 0

    if step in (1, 4):
        if step == 4:
            xr = (r / step) & 0b000111
            yr = ((r / step) & 0b111000) >> 3
        elif step == 1:
            xr = r & 0b00001111
            yr = (r & 0b11110000) >> 4

    elif step in (3, 5, 17, 51):
        xr = 0xff / step
        yr = 0
        xr = r & 0b00001111
        yr = (r & 0b11110000) >> 4
    else:
        raise NotImplementedError('step: {0}'.format(step))

    x += xr * 256 / step
    y += yr * 256 / step
    
    return x, y

def xy2rgb(x, y, step=4):
    '''
    >>> xy2rgb(*rgb2xy(0, 0, 0, step=4), step=4)
    (0, 0, 0)
    >>> xy2rgb(*rgb2xy(0, 0, 255, step=4), step=4)
    (0, 0, 252)
    >>> xy2rgb(*rgb2xy(0, 255, 0, step=4), step=4)
    (0, 252, 0)
    >>> xy2rgb(*rgb2xy(0, 255, 255, step=4), step=4)
    (0, 252, 252)
    >>> xy2rgb(*rgb2xy(128, 128, 128, step=4), step=4)
    (128, 128, 128)
    >>> xy2rgb(*rgb2xy(255, 0, 0, step=4), step=4)
    (252, 0, 0)
    >>> xy2rgb(*rgb2xy(255, 0, 255, step=4), step=4)
    (252, 0, 252)
    >>> xy2rgb(*rgb2xy(255, 255, 0, step=4), step=4)
    (252, 252, 0)
    >>> xy2rgb(*rgb2xy(255, 255, 255, step=4), step=4)
    (252, 252, 252)
    '''
    b = step * (x % (256 / step))
    g = step * (y % (256 / step))
    
    if step == 4:
        rx = x / (256 / step)
        ry = (y / (256 / step)) << 3
        r = (rx | ry) * step
    else:
        raise NotImplementedError('step: {0}'.format(step))
    
    return r, g, b

def get_pixels(step=4):
    rgbs = product(*(range(0, 256, step) for chan in 'rgb'))
    xyrgbs = (rgb2xy(*rgb, step=step) + rgb for rgb in rgbs)

    return xyrgbs

def make_image(step=4):
    '''
    >>> make_image(step=4).size
    (512, 512)
    '''
    if step in (16, 4, 1):
        dim = int(16 / sqrt(step)) * (256 / step)
        xdim, ydim = dim, dim
    elif step in (3, 5, 17, 51):
        ydim = 0xff / step
        xdim = (0xff * 0xff) / (step * step)
    else:
        raise NotImplementedError('step: {0}'.format(step))

    img = Image.new('RGB', (xdim, ydim))

    for (x, y, r, g, b) in get_pixels(step):
        try:
            img.putpixel((x, y), (r, g, b))
        except:
            print (x, y, r, g, b)
            raise
    
    return img

def arr2img(ar):
    """ Convert Numeric array to PIL Image.
    """
    return Image.fromstring('L', (ar.shape[1], ar.shape[0]), ar.astype(numpy.ubyte).tostring())

def img2arr(im):
    """ Convert PIL Image to Numeric array.
    """
    assert im.mode == 'L'
    return numpy.reshape(numpy.fromstring(im.tostring(), numpy.ubyte), (im.size[1], im.size[0]))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
    #    img = make_image()
    #    from numpy import zeros
    #    cube = zeros((64, 64, 64, 3), int)
    #    
    #    for red in range(0, 256, 4):
    #        x, y = rgb2xy(red, 0, 0, 4)
    #        
    #        slice = img.crop((x, y, x+64, y+64))
    #        r, g, b = slice.split()
    #        
    #        cube[red/4,:,:,0] = r
    #        cube[red/4,:,:,1] = g
    #        cube[red/4,:,:,2] = b
    #    
    #    print cube[0,0,0], cube[-1,-1,-1]
    #    
    #    photo = Image.open('/Users/migurski/Pictures/stupid bicycle.jpg')
    #    r, g, b = map(img2arr, photo.split())
    #    
    #    out = cube[r/4, g/4, b/4]
    #    rgb_out = out[:,:,0], out[:,:,1], out[:,:,2]
    #    
    #    Image.merge('RGB', map(arr2img, rgb_out)).save('out.png')
    #    
    #    exit(1)

    make_image(4).save('map.png')
