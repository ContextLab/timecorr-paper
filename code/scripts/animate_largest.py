import supereeg as se
import numpy as np
import os
from visbrain.objects import BrainObj, SceneObj, SourceObj

cmap = 'autumn_r'

neurosynth_dir ='../figs/neurosynth_data'

fig_dir = '../figs'

bo_dir = os.path.join(neurosynth_dir, 'bos')

n_f_dir = os.path.join(neurosynth_dir, 'figs')
if not os.path.exists(n_f_dir):
    os.mkdir(n_f_dir)

b1 = se.load(os.path.join(bo_dir, 'intact_1_largest.bo'))
b2 = se.load(os.path.join(bo_dir, 'intact_2_largest.bo'))
b3 = se.load(os.path.join(bo_dir, 'intact_3_largest.bo'))
b4 = se.load(os.path.join(bo_dir, 'intact_4_largest.bo'))

data1 = b1.get_data().values.ravel()
xyz1 = b1.locs.values
xyz1 = xyz1[data1>.9999]
data1 = data1[data1>.9999]
data1 = np.ones(data1.shape)


data2 = b2.get_data().values.ravel()
xyz2 = b2.locs.values
xyz2 = xyz2[data2>.9999]
data2 = data2[data2>.9999]
data2 = np.ones(data2.shape)+1

data3 = b3.get_data().values.ravel()
xyz3 = b3.locs.values
xyz3 = xyz3[data3>.9999]
data3 = data3[data3>.9999]
data3 = np.ones(data3.shape)+2

data4 = b4.get_data().values.ravel()
xyz4 = b4.locs.values
xyz4 = xyz4[data4>.9999]
data4 = data4[data4>.9999]
data4 = np.ones(data4.shape)+3

template_brain = 'B3'

sc = SceneObj(bgcolor='white', size=(500, 500))

CBAR_STATE = dict(cbtxtsz=12, clim=[0, 6], txtsz=10., width=.1, cbtxtsh=3.,
                  rect=(-.3, -2., 1., 4.))
KW = dict(title_size=14., zoom=1)

sc_blank = SceneObj(bgcolor='white', size=(500, 500))
b_obj_proj_blank = BrainObj(template_brain, hemisphere='left', translucent=False)
sc_blank.add_to_subplot(b_obj_proj_blank, row=0, col=0, rotate='left', use_this_cam=True)
sc_blank.screenshot(os.path.join(fig_dir, 'blank.png'), transparent=True)


s_obj_1 = SourceObj('iEEG', xyz1, data=data1, cmap=cmap)
s_obj_1.color_sources(data=data1)
s_obj_2 = SourceObj('iEEG', xyz2, data=data2, cmap=cmap)
s_obj_2.color_sources(data=data2)
s_obj_3 = SourceObj('iEEG', xyz3, data=data3, cmap=cmap)
s_obj_3.color_sources(data=data3)
s_obj_4 = SourceObj('iEEG', xyz4, data=data4, cmap=cmap)
s_obj_4.color_sources(data=data4)


s_obj_all = s_obj_1 + s_obj_2 + s_obj_3 + s_obj_4

b_obj_proj_left = BrainObj(template_brain, hemisphere='both', translucent=False)
b_obj_proj_left.project_sources(s_obj_all, clim=(0, 4), cmap=cmap)
sc.add_to_subplot(b_obj_proj_left, row=0, col=0, rotate='right', use_this_cam=True)

# b_obj_proj_left = BrainObj(template_brain, hemisphere='left', translucent=False)
# b_obj_proj_left.project_sources(s_obj_all, clim=(0, 4), cmap=cmap)
# sc.add_to_subplot(b_obj_proj_left, row=0, col=1, rotate='right', use_this_cam=True)
#
# b_obj_proj_right = BrainObj(template_brain, hemisphere='right', translucent=False)
# b_obj_proj_right.project_sources(s_obj_all, clim=(0, 4), cmap=cmap)
# sc.add_to_subplot(b_obj_proj_right, row=0, col=2, rotate='right', use_this_cam=True)


sc.record_animation(os.path.join(n_f_dir,'intact_largest.gif'), n_pic=40)
sc.preview()