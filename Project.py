from PIL import Image
import numpy as np

def main():
    filesquares = 'images/squares.png'
    filebird = 'images/bird.png'
    filebirdout1_similarity = 'images/birdout1_similarity.png'
    filebirdout1_affine = 'images/birdout1_affine.png'
    filesquaresout1_similarity = 'images/squaresout1_similarity.png'
    filesquaresout1_affine = 'images/squaresout1_affine.png'
    filebirdout2_similarity = 'images/birdout2_similarity.png'
    filebirdout2_affine = 'images/birdout2_affine.png'
    filesquaresout2_similarity = 'images/squaresout2_similarity.png'
    filesquaresout2_affine = 'images/squaresout2_affine.png'

    imsquares = Image.open(filesquares)
    imbird = Image.open(filebird)

    imsquaresout1_similarity = transform(
        'similarity',
        imsquares,
        translate=(10,20),
        scale=(2, 2),
        shear=(0, 0),
        rotation=30
    )

    imsquaresout1_affine = transform(
        'affine',
        imsquares,
        translate=(0,0),
        scale=(1, 1),
        shear=(20, 10),
        rotation=0
    )

    imbirdout1_similarity = transform(
        'similarity',
        imbird,
        translate=(10,20),
        scale=(2, 2),
        shear=(0, 0),
        rotation=30
    )

    imbirdout1_affine = transform(
        'affine',
        imbird,
        translate=(0,0),
        scale=(1, 1),
        shear=(20, 10),
        rotation=0
    )

    imsquaresout2_similarity = transform(
        'similarity',
        imsquares,
        translate=(10,5),
        scale=(3, 3),
        shear=(0, 0),
        rotation=45
    )

    imsquaresout2_affine = transform(
        'affine',
        imsquares,
        translate=(0,0),
        scale=(1, 1),
        shear=(10, 20),
        rotation=0
    )

    imbirdout2_similarity = transform(
        'similarity',
        imbird,
        translate=(10,5),
        scale=(3, 3),
        shear=(0, 0),
        rotation=45
    )

    imbirdout2_affine = transform(
        'affine',
        imbird,
        translate=(0,0),
        scale=(1, 1),
        shear=(10, 20),
        rotation=0
    )

    imsquaresout1_similarity.save(filesquaresout1_similarity)
    imsquaresout1_affine.save(filesquaresout1_affine)
    imbirdout1_similarity.save(filebirdout1_similarity)
    imbirdout1_affine.save(filebirdout1_affine)

    imsquaresout2_similarity.save(filesquaresout2_similarity)
    imsquaresout2_affine.save(filesquaresout2_affine)
    imbirdout2_similarity.save(filebirdout2_similarity)
    imbirdout2_affine.save(filebirdout2_affine)


def transform(transformationType,
                     image,
                     translate,
                     scale,
                     shear,
                     rotation
                     ):
    if transformationType == 'similarity':
        tx, ty = translate
        theta = rotation
        sx, sy = scale
        m_rot = np.matrix([[np.cos(theta), -np.sin(theta), 0],
                           [np.sin(theta), np.cos(theta), 0],
                           [0, 0, 1]])
        m_scale = np.matrix([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        image = image.rotate(0, translate=(tx, ty))
        trans_matrix = m_rot *  m_scale
    elif transformationType == 'affine':
        shx, shy = shear
        shx = shx / 100
        shy = shy / 100
        m_shear_x = np.matrix([[1, shx, 0], [0, 1, 0], [0, 0, 1]])
        m_shear_y = np.matrix([[1, 0, 0], [shy, 1, 0], [0, 0, 1]])
        trans_matrix = m_shear_y * m_shear_x

    w, h = image.size
    ww, hh, mnx, mny = get_size(w, h, trans_matrix)
    trans_matrix = np.matrix([[1, 0, -mnx],
                                 [0, 1, -mny],
                                 [0, 0, 1]]) * trans_matrix
    t_inv = np.linalg.inv(trans_matrix)
    t_inv_tuple = (t_inv[0, 0], t_inv[0, 1], t_inv[0, 2],
                   t_inv[1, 0], t_inv[1, 1], t_inv[1, 2])

    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    wrap_image = image.transform((ww, hh),
                                 Image.AFFINE, t_inv_tuple,
                                 resample=Image.BILINEAR)
    wrap_image = wrap_image.transpose(Image.FLIP_TOP_BOTTOM)
    return wrap_image

def get_size(w, h, trans_matrix):
    p = {}
    q = {}
    p['ll'] = np.array([[0, 0, 1]]).transpose()
    p['lr'] = np.array([[w-1, 0, 1]]).transpose()
    p['ul'] = np.array([[0, h-1, 1]]).transpose()
    p['ur'] = np.array([[w-1, h-1, 1]]).transpose()
    for key in p:
        q[key] = trans_matrix * p[key]

    x, y = [], []
    for key in p:
        x.append(q[key][0, 0])
        y.append(q[key][1, 0])
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    hh = int(round(y_max - y_min)) + 1
    ww = int(round(x_max - x_min)) + 1
    return ww, hh, x_min, y_min

main()
