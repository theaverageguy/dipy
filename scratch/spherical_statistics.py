import numpy as np
import dipy.core.meshes as meshes
from dipy.core.triangle_subdivide import create_unit_sphere
from dipy.viz import fos
from dipy.io import dicomreaders as dcm

sphere_dic = {'fy362': {'filepath' : '/home/ian/Devel/dipy/dipy/core/matrices/evenly_distributed_sphere_362.npz', 'object': 'npz', 'vertices': 'vertices', 'omit': 0, 'hemi': False},
              'fy642': {'filepath' : '/home/ian/Devel/dipy/dipy/core/matrices/evenly_distributed_sphere_642.npz', 'object': 'npz', 'vertices': 'odf_vertices', 'omit': 0, 'hemi': False},
              'siem64': {'filepath':'/home/ian/Devel/dipy/dipy/core/tests/data/small_64D.gradients.npy', 'object': 'npy', 'omit': 1, 'hemi': True},
#              'create2': {},
#              'create3': {},
#              'create4': {},
              'create5': {},
              'create6': {},
#              'create7': {},
#              'create8': {},
#              'create9': {},
              'marta200': {'filepath': '/home/ian/Data/Spheres/200.npy', 'object': 'npy', 'omit': 0, 'hemi': True},
              'dsi101': {'filepath': '/home/ian/Data/Frank_Eleftherios/frank/20100511_m030y_cbu100624/08_ep2d_advdiff_101dir_DSI', 'object': 'dicom', 'omit': 0, 'hemi': False}}

def get_vertices(key):
    if key[:6] == 'create':
        number = eval(key[6:])
        vertices, edges, faces = create_unit_sphere(number) 
        omit = 0
    else:
        entry = sphere_dic[key]
        #print entry
        if entry.has_key('omit'):
            omit = entry['omit']
        else:
            omit = 0
        filepath = entry['filepath']
        if entry['object'] == 'npz':
            filearray  = np.load(filepath)
            vertices = filearray[entry['vertices']]
        elif sphere_dic[key]['object'] == 'npy':
            vertices = np.load(filepath)
        elif entry['object'] == 'dicom':
            data,affine,bvals,gradients=dcm.read_mosaic_dir(filepath)
            #print (bvals.shape, gradients.shape)
            grad3 = np.vstack((bvals,bvals,bvals)).transpose()
            #print grad3.shape
            #vertices = grad3*gradients
            vertices = gradients
        if entry['hemi']:
            vertices = np.vstack([vertices, -vertices])
    print key, ': number of vertices = ', vertices.shape[0], '(drop ',omit,')'
    return vertices[omit:,:]

for key in sphere_dic:
    v = get_vertices(key)
    #print v.shape[0]
    r = fos.ren()
    fos.add(r,fos.point(v,fos.green, point_radius= 0.01))
    fos.show(r, title=key, size=(1000,1000))
    meshes.equatorial_statistics(v)
    