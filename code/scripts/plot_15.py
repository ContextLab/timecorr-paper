
import supereeg as se
import os
import numpy as np
from visbrain.objects import BrainObj, SceneObj, SourceObj, ColorbarObj

cmap = 'autumn_r'

replication_dir ='../figs/replication/'
neurosynth_dir = os.path.join(replication_dir, 'neurosynth_data')
fig_dir = replication_dir

#
# neurosynth_dir ='../figs/neurosynth_data'
#
# fig_dir = '../figs'

bo_dir = os.path.join(neurosynth_dir, 'bos')

n_f_dir = os.path.join(neurosynth_dir, 'figs')
if not os.path.exists(n_f_dir):
    os.mkdir(n_f_dir)

conditions = ['intact', 'paragraph', 'rest', 'word']

for c in conditions:

    data1 = np.load(os.path.join(bo_dir,f'{c}_1_data_largest_abs.npy'))
    xyz1 = np.load(os.path.join(bo_dir, f'{c}_1_locs_largest_abs.npy'))

    data2 = np.load(os.path.join(bo_dir, f'{c}_2_data_largest_abs.npy'))
    xyz2 = np.load(os.path.join(bo_dir, f'{c}_2_locs_largest_abs.npy'))

    data3= np.load(os.path.join(bo_dir, f'{c}_3_data_largest_abs.npy'))
    xyz3 = np.load(os.path.join(bo_dir, f'{c}_3_locs_largest_abs.npy'))

    data4 = np.load(os.path.join(bo_dir, f'{c}_4_data_largest_abs.npy'))
    xyz4 = np.load(os.path.join(bo_dir, f'{c}_4_locs_largest_abs.npy'))

    data5 = np.load(os.path.join(bo_dir,f'{c}_5_data_largest_abs.npy'))
    xyz5 = np.load(os.path.join(bo_dir, f'{c}_5_locs_largest_abs.npy'))

    data6 = np.load(os.path.join(bo_dir, f'{c}_6_data_largest_abs.npy'))
    xyz6 = np.load(os.path.join(bo_dir, f'{c}_6_locs_largest_abs.npy'))

    data7= np.load(os.path.join(bo_dir, f'{c}_7_data_largest_abs.npy'))
    xyz7 = np.load(os.path.join(bo_dir, f'{c}_7_locs_largest_abs.npy'))

    data8 = np.load(os.path.join(bo_dir, f'{c}_8_data_largest_abs.npy'))
    xyz8 = np.load(os.path.join(bo_dir, f'{c}_8_locs_largest_abs.npy'))

    data9 = np.load(os.path.join(bo_dir, f'{c}_9_data_largest_abs.npy'))
    xyz9 = np.load(os.path.join(bo_dir, f'{c}_9_locs_largest_abs.npy'))

    data10 = np.load(os.path.join(bo_dir,f'{c}_10_data_largest_abs.npy'))
    xyz10 = np.load(os.path.join(bo_dir, f'{c}_10_locs_largest_abs.npy'))

    data11 = np.load(os.path.join(bo_dir,f'{c}_11_data_largest_abs.npy'))
    xyz11 = np.load(os.path.join(bo_dir, f'{c}_11_locs_largest_abs.npy'))

    data12 = np.load(os.path.join(bo_dir, f'{c}_12_data_largest_abs.npy'))
    xyz12 = np.load(os.path.join(bo_dir, f'{c}_12_locs_largest_abs.npy'))

    data13= np.load(os.path.join(bo_dir, f'{c}_13_data_largest_abs.npy'))
    xyz13 = np.load(os.path.join(bo_dir, f'{c}_13_locs_largest_abs.npy'))

    data14 = np.load(os.path.join(bo_dir, f'{c}_14_data_largest_abs.npy'))
    xyz14 = np.load(os.path.join(bo_dir, f'{c}_14_locs_largest_abs.npy'))

    data15 = np.load(os.path.join(bo_dir,f'{c}_15_data_largest_abs.npy'))
    xyz15 = np.load(os.path.join(bo_dir, f'{c}_15_locs_largest_abs.npy'))

    # b1 = se.load(os.path.join(bo_dir,f'{c}_1_largest_abs.bo'))
    # b2 = se.load(os.path.join(bo_dir,f'{c}_2_largest_abs.bo'))
    # b3 = se.load(os.path.join(bo_dir,f'{c}_3_largest_abs.bo'))
    # b4 = se.load(os.path.join(bo_dir,f'{c}_4_largest_abs.bo'))
    # b5 = se.load(os.path.join(bo_dir, f'{c}_5_largest_abs.bo'))
    # b6 = se.load(os.path.join(bo_dir, f'{c}_6_largest_abs.bo'))
    # b7 = se.load(os.path.join(bo_dir, f'{c}_7_largest_abs.bo'))
    # b8 = se.load(os.path.join(bo_dir, f'{c}_8_largest_abs.bo'))
    # b9 = se.load(os.path.join(bo_dir, f'{c}_9_largest_abs.bo'))
    # b10 = se.load(os.path.join(bo_dir, f'{c}_10_largest_abs.bo'))
    # b11 = se.load(os.path.join(bo_dir, f'{c}_11_largest_abs.bo'))
    # b12 = se.load(os.path.join(bo_dir, f'{c}_12_largest_abs.bo'))
    # b13 = se.load(os.path.join(bo_dir, f'{c}_13_largest_abs.bo'))
    # b14 = se.load(os.path.join(bo_dir, f'{c}_14_largest_abs.bo'))
    # b15 = se.load(os.path.join(bo_dir, f'{c}_15_largest_abs.bo'))
    #
    #
    # data1 = b1.get_data().values.ravel()
    # xyz1 = b1.locs.values
    #
    # data2 = b2.get_data().values.ravel()
    # xyz2 = b2.locs.values
    #
    # data3 = b3.get_data().values.ravel()
    # xyz3 = b3.locs.values
    #
    # data4 = b4.get_data().values.ravel()
    # xyz4 = b4.locs.values
    #
    # data5 = b5.get_data().values.ravel()
    # xyz5 = b5.locs.values
    #
    # data6 = b6.get_data().values.ravel()
    # xyz6 = b6.locs.values
    #
    # data7 = b7.get_data().values.ravel()
    # xyz7 = b7.locs.values
    #
    # data8 = b8.get_data().values.ravel()
    # xyz8 = b8.locs.values
    #
    # data9 = b9.get_data().values.ravel()
    # xyz9 = b9.locs.values
    #
    # data10 = b10.get_data().values.ravel()
    # xyz10 = b10.locs.values
    #
    # data11 = b11.get_data().values.ravel()
    # xyz11 = b11.locs.values
    #
    # data12 = b12.get_data().values.ravel()
    # xyz12 = b12.locs.values
    #
    # data13 = b13.get_data().values.ravel()
    # xyz13 = b13.locs.values
    #
    # data14 = b14.get_data().values.ravel()
    # xyz14 = b14.locs.values
    #
    # data15 = b15.get_data().values.ravel()
    # xyz15 = b15.locs.values

    template_brain = 'B3'

    sc = SceneObj(bgcolor='white', size=(1000, 1000))

    CBAR_STATE = dict(cbtxtsz=12, clim=[0, 15], txtsz=10., width=.1, cbtxtsh=3.,
                      rect=(-.3, -2., 1., 4.))
    KW = dict(title_size=14., zoom=1)

    s_obj_1 = SourceObj('iEEG', xyz1, data=data1, cmap=cmap)
    s_obj_1.color_sources(data=data1)
    s_obj_2 = SourceObj('iEEG', xyz2, data=data2, cmap=cmap)
    s_obj_2.color_sources(data=data2)
    s_obj_3 = SourceObj('iEEG', xyz3, data=data3, cmap=cmap)
    s_obj_3.color_sources(data=data3)
    s_obj_4 = SourceObj('iEEG', xyz4, data=data4, cmap=cmap)
    s_obj_4.color_sources(data=data4)
    s_obj_5 = SourceObj('iEEG', xyz5, data=data5, cmap=cmap)
    s_obj_5.color_sources(data=data5)
    s_obj_6 = SourceObj('iEEG', xyz6, data=data6, cmap=cmap)
    s_obj_6.color_sources(data=data6)
    s_obj_7 = SourceObj('iEEG', xyz7, data=data7, cmap=cmap)
    s_obj_7.color_sources(data=data7)
    s_obj_8 = SourceObj('iEEG', xyz8, data=data8, cmap=cmap)
    s_obj_8.color_sources(data=data8)
    s_obj_9 = SourceObj('iEEG', xyz9, data=data9, cmap=cmap)
    s_obj_9.color_sources(data=data9)
    s_obj_10 = SourceObj('iEEG', xyz10, data=data10, cmap=cmap)
    s_obj_10.color_sources(data=data10)
    s_obj_11 = SourceObj('iEEG', xyz11, data=data11, cmap=cmap)
    s_obj_11.color_sources(data=data11)
    s_obj_12 = SourceObj('iEEG', xyz12, data=data12, cmap=cmap)
    s_obj_12.color_sources(data=data12)
    s_obj_13 = SourceObj('iEEG', xyz13, data=data13, cmap=cmap)
    s_obj_13.color_sources(data=data13)
    s_obj_14 = SourceObj('iEEG', xyz14, data=data14, cmap=cmap)
    s_obj_14.color_sources(data=data14)
    s_obj_15 = SourceObj('iEEG', xyz15, data=data15, cmap=cmap)
    s_obj_15.color_sources(data=data15)

    s_obj_all = s_obj_1 + s_obj_2 + s_obj_3 + s_obj_4 + s_obj_5 + s_obj_6 + s_obj_7 + s_obj_8 + s_obj_9 + s_obj_10 + \
                s_obj_11 + s_obj_12 + s_obj_13 + s_obj_14 + s_obj_15

    b_obj_proj_left = BrainObj(template_brain, hemisphere='left', translucent=False)
    b_obj_proj_left.project_sources(s_obj_all, clim=(0, 16), cmap=cmap)
    sc.add_to_subplot(b_obj_proj_left, row=0, col=0, rotate='left', use_this_cam=True)


    b_obj_proj_left = BrainObj(template_brain, hemisphere='left', translucent=False)
    b_obj_proj_left.project_sources(s_obj_all, clim=(0, 16), cmap=cmap)
    sc.add_to_subplot(b_obj_proj_left, row=0, col=1, rotate='right', use_this_cam=True)

    b_obj_proj_right = BrainObj(template_brain, hemisphere='right', translucent=False)
    b_obj_proj_right.project_sources(s_obj_all, clim=(0, 16), cmap=cmap)
    sc.add_to_subplot(b_obj_proj_right, row=0, col=2, rotate='left', use_this_cam=True)

    b_obj_proj_right = BrainObj(template_brain, hemisphere='right', translucent=False)
    b_obj_proj_right.project_sources(s_obj_all, clim=(0, 16), cmap=cmap)
    sc.add_to_subplot(b_obj_proj_right, row=0, col=3, rotate='right', use_this_cam=True)

    # cb_proj = ColorbarObj(b_obj_proj_right, cblabel='Order', **CBAR_STATE)
    # sc.add_to_subplot(cb_proj, row=0, col=4, width_max=200)

    sc.screenshot(os.path.join(fig_dir, f'{c}_15.png'), transparent=True)
