import os
import numpy as np
import pickle
import cv2
import pandas as pd
import warnings
from skimage import io as skio
from skimage.morphology import skeletonize
warnings.filterwarnings("ignore")

def branchpoint_lut_PN(skel_image):

    # print(skel_image.shape)


    thresh, im = cv2.threshold(skel_image, 0, 1, cv2.THRESH_BINARY)

    branch_lut = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                  0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1,
                  1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                  0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1,
                  1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                  0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1]

    k = np.zeros((3, 3, 1), dtype="uint16")
    k[0][0][0] = 256
    k[1][0][0] = 128
    k[2][0][0] = 64
    k[0][1][0] = 32
    k[1][1][0] = 16
    k[2][1][0] = 8
    k[0][2][0] = 4
    k[1][2][0] = 2
    k[2][2][0] = 1

    dst = cv2.filter2D(im, 2, k)
    w, h = dst.shape

    for i in range(w):
        for j in range(h):
            dst[i][j] = branch_lut[dst[i][j]]

    dst = dst * 255

    return dst


class feature_extraction(object):

    def __init__(self,
                 wsi_tiles_dir,
                 patch_mask_dir,
                 file_type,
                 shape_type
                 ):
        self.wsi_tiles_dir = wsi_tiles_dir
        self.patch_mask_dir = patch_mask_dir
        self.file_type = file_type
        self.shape_type = shape_type

    def extract_patch_level_features(self):

        # Check if the value is the string "Tree"
        if isinstance(self.shape_type, str) and self.shape_type == "Tree":
            print("Extraction of Tree descriptors and Proceeding with feature extraction.")
            print(self.wsi_tiles_dir)

            file_names_list = [fname for fname in os.listdir(self.wsi_tiles_dir) if fname.endswith(self.file_type) and (
                    fname.startswith('BCPP') or fname.startswith('RADIO') or fname.startswith('PLUMMB')) is True]

            for slide in file_names_list:

                param = pickle.load(open(os.path.join(self.wsi_tiles_dir, slide, 'param.p'), 'rb'))

                results_dir = os.path.join(self.patch_mask_dir, 'cws', slide, 'tree')
                results_overlay_dir = os.path.join(self.patch_mask_dir, 'cws', slide, 'tree_overlay_img')

                if os.path.exists(results_dir) is False:
                    os.makedirs(results_dir)
                if os.path.exists(results_overlay_dir) is False:
                    os.makedirs(results_overlay_dir)
                roi_df = pd.DataFrame(columns=['file_name', 'mask', 'tree_count', 'tree_ratio'])
                for r_ind, roi_n in enumerate(os.listdir(os.path.join(self.patch_mask_dir, 'cws', slide, 'ROI_80_H1'))):

                    if os.path.exists(os.path.join(results_dir, roi_n)) is False:
                        os.makedirs(os.path.join(results_dir, roi_n))

                    if os.path.exists(os.path.join(results_overlay_dir, roi_n)) is False:
                        os.makedirs(os.path.join(results_overlay_dir, roi_n))

                    print(roi_n)
                    tree_a = 0
                    sk_sum = 0
                    mask_sum = 0
                    stat_da_df = pd.DataFrame(columns=['file_name', 'mask', 'tree_count', 'tree_ratio'])

                    for ind, da_n in enumerate(os.listdir(os.path.join(self.patch_mask_dir, 'cws', slide, 'ROI_80_H1', roi_n))):
                        img = cv2.imread(os.path.join(self.patch_mask_dir, 'cws', slide, 'ROI_80_H1', roi_n, da_n))
                        if not hasattr(img, 'shape') or img.shape is None:
                            continue
                        else:

                            g_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                            thresh, im = cv2.threshold(g_img, 100, 255, cv2.THRESH_BINARY)
                            imn = cv2.bitwise_not(im)
                            # cv2.imwrite(os.path.join(results_dir, slide, roi_n, da_n.split('.jpg')[0] + "_skel" + ".png"), imn)
                            thresh, im_s = cv2.threshold(imn, 0, 1, cv2.THRESH_BINARY)

                            skeleton = skeletonize(im_s)
                            skeleton8 = skeleton * 255

                            sk8 = skeleton8.astype('uint8')

                            conts = np.zeros((sk8.shape), dtype='uint8')
                            img_overlay = img.copy()

                            _, contours, hierarchy = cv2.findContours(sk8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                            cv2.drawContours(img_overlay, contours, -1, (0, 255, 0), 1)
                            print(os.path.join(results_overlay_dir, roi_n, da_n.split('.jpg')[0] + "_skel.png"))
                            # Filter contours with an area less than 50
                            sk8_filtered_mask = np.zeros_like(sk8)  # Create a blank mask to draw filtered contours
                            for contour in contours:
                                area = cv2.contourArea(contour)
                                if area >= 100:
                                    # Draw the contour on the filtered mask
                                    cv2.drawContours(sk8_filtered_mask, [contour], -1, 255, thickness=1, lineType=cv2.LINE_8)


                            cv2.imwrite(os.path.join(results_overlay_dir, roi_n, da_n.split('.jpg')[0] + "_skel.png"), sk8_filtered_mask)
                            # cv2.imwrite(os.path.join(results_overlay_dir, slide, roi_n, da_n.split('.jpg')[0] + "_skel" + ".png"), img_overlay)
                            sk_mask = cv2.countNonZero(sk8_filtered_mask)


                            im_mask = cv2.imread(os.path.join(self.patch_mask_dir, 'cws', slide, 'img_mask', roi_n, da_n))
                            g_img_mask = cv2.cvtColor(im_mask, cv2.COLOR_RGB2GRAY)
                            thresh, im_mk = cv2.threshold(g_img_mask, 100, 255, cv2.THRESH_BINARY)
                            m_cnt = cv2.countNonZero(im_mk)
                            sk_core_mask_ratio = (sk_mask * 1e6) / (m_cnt * 0.4428 * 0.4428)  ###core_mask###
                            sk_r_f_value = round(sk_core_mask_ratio, 2)
                            # sk_r_f_value = "{:.2f}".format(sk_core_mask_ratio)
                            print(sk_r_f_value, sk_mask)
                            tree_a += sk_mask
                            sk_sum += sk_r_f_value
                            mask_sum += m_cnt

                            stat_da_df.loc[ind, ['file_name', 'mask', 'tree_count', 'tree_ratio']] = [
                                os.path.join(slide, 'ROI_80_H1', roi_n, da_n), m_cnt, sk_mask, sk_r_f_value]

                            stat_da_df.to_csv(os.path.join(results_overlay_dir, roi_n, 'all_tree_da.csv'), index=False)

                            # get_tree_score_on_tiles(wsi_files, patch_mask_dir, slide, da_n, )
                    # print(os.path.join(slide, 'ROI_80_H1', roi_n), tree_a, sk_sum, mask_sum)
                    print(stat_da_df)
                    roi_df.loc[r_ind, ['file_name', 'mask', 'tree_count', 'tree_ratio']] = [
                        os.path.join(slide, 'ROI_80_H1', roi_n), mask_sum, tree_a, sk_sum]
                roi_df.to_csv(os.path.join(results_overlay_dir, 'all_roi_tree.csv'), index=False)
            pass
        # Check if the value is the string "Branch"
        elif isinstance(self.shape_type, str) and self.shape_type == "Branch":
            print("Extraction of Branch descriptors and Proceeding with feature extraction.")

            file_names_list = [fname for fname in os.listdir(self.wsi_tiles_dir) if fname.endswith(self.file_type) and (
                    fname.startswith('BCPP') or fname.startswith('RADIO') or fname.startswith('PLUMMB')) is True]

            for slide in file_names_list:

                param = pickle.load(open(os.path.join(self.wsi_tiles_dir, slide, 'param.p'), 'rb'))


                results_dir = os.path.join(self.patch_mask_dir, 'cws', slide, 'tree')
                results_overlay_dir = os.path.join(self.patch_mask_dir, 'cws', slide, 'tree_overlay_img')

                if os.path.exists(results_dir) is False:
                    os.makedirs(results_dir)
                if os.path.exists(results_overlay_dir) is False:
                    os.makedirs(results_overlay_dir)

                roi_df = pd.DataFrame(columns=['file_name', 'mask', 'branch_area', 'branch_ratio'])
                if os.path.isdir(os.path.join(self.patch_mask_dir, 'cws', slide, 'tree_overlay_img')):

                    for r_ind, roi_n in enumerate(os.listdir(os.path.join(self.patch_mask_dir, 'cws', slide, 'tree_overlay_img'))):

                        if roi_n.endswith('.csv'):
                            continue
                        # os.path.isdir(path)

                        if os.path.exists(os.path.join(results_dir, roi_n)) is False:
                            os.makedirs(os.path.join(results_dir, roi_n))

                        if os.path.exists(os.path.join(results_overlay_dir, roi_n)) is False:
                            os.makedirs(os.path.join(results_overlay_dir, roi_n))

                        branch_a = 0
                        bk_sum = 0
                        mask_sum = 0
                        stat_da_df = pd.DataFrame(columns=['file_name', 'mask', 'branch_area', 'branch_ratio'])

                        for ind, da_n in enumerate(os.listdir(os.path.join(self.patch_mask_dir, 'cws', slide, 'tree_overlay_img', roi_n))):
                            if da_n.endswith('.png'):
                                print(da_n)

                                sk8_img = cv2.imread(os.path.join(self.patch_mask_dir, 'cws', slide, 'tree_overlay_img', roi_n, da_n))
                                if not hasattr(sk8_img, 'shape') or sk8_img.shape is None:
                                    continue
                                else:

                                    g_img = cv2.cvtColor(sk8_img, cv2.COLOR_RGB2GRAY)
                                    thresh, im = cv2.threshold(g_img, 100, 255, cv2.THRESH_BINARY)
                                    ######
                                    dst = branchpoint_lut_PN(im)
                                    print(dst.dtype, dst.shape)
                                    dst8 = dst * 255

                                    dst8 = dst8.astype('uint8')
                                    _, contours, hierarchy = cv2.findContours(dst8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                                    dst8_branch = np.zeros_like(g_img)
                                    cv2.drawContours(dst8_branch, contours, -1, (255), 5)
                                    ## branch mask before filtering ##
                                    b_mask_bf = cv2.countNonZero(dst8)
                                    #
                                    # b_mask_filtered = np.zeros_like(
                                    #     b_mask)  # Create a blank mask to draw filtered contours
                                    # for contour in contours:
                                    #     area = cv2.contourArea(contour)
                                    #     if area >= 50:
                                    #         # Draw the contour on the filtered mask
                                    #         cv2.drawContours(b_mask_filtered, [contour], -1, 255,
                                    #                          thickness=1)

                                    cv2.imwrite(
                                        os.path.join(results_overlay_dir, roi_n, da_n.split('_')[0] + "_brch.png"),
                                        dst8_branch)
                                    # cv2.imwrite(os.path.join(results_overlay_dir, slide, roi_n, da_n.split('.jpg')[0] + "_skel" + ".png"), img_overlay)
                                    b_mask = cv2.countNonZero(dst8)

                                    im_mask = cv2.imread(os.path.join(self.patch_mask_dir, 'cws', slide, 'img_mask', roi_n, da_n.split('_')[0]+'.jpg'))
                                    g_img_mask = cv2.cvtColor(im_mask, cv2.COLOR_RGB2GRAY)
                                    thresh, im_mk = cv2.threshold(g_img_mask, 100, 255, cv2.THRESH_BINARY)
                                    im_mk = im_mk.astype('uint8')
                                    m_cnt = cv2.countNonZero(im_mk)
                                    b_core_mask_ratio = (b_mask * 1e6) / (m_cnt * 0.4428 * 0.4428)  ###core_mask###
                                    b_r_f_value = round(b_core_mask_ratio, 2)
                                    # sk_r_f_value = "{:.2f}".format(sk_core_mask_ratio)
                                    print(b_r_f_value, b_mask)
                                    branch_a += b_mask
                                    bk_sum += b_r_f_value
                                    mask_sum += m_cnt

                                    stat_da_df.loc[ind, ['file_name', 'mask', 'branch_area', 'branch_ratio']] = [
                                        os.path.join(slide, 'ROI_80_H1', roi_n, da_n), m_cnt, b_mask, b_r_f_value]

                                    stat_da_df.to_csv(os.path.join(results_overlay_dir, roi_n, 'all_brch_da.csv'), index=False)

                                roi_df.loc[r_ind, ['file_name', 'mask', 'branch_area', 'branch_ratio']] = [
                                os.path.join(slide, 'ROI_80_H1', roi_n), mask_sum, branch_a, bk_sum]
                                roi_df.to_csv(os.path.join(results_overlay_dir, 'all_roi_brch.csv'), index=False)

                            else:# for other file types
                                continue
        else:
            pass



def get_patch_level_features(wsi_tiles_dir, patch_mask_dir, file_type, shape_type):
    params_keys = {'wsi_tiles_dir': wsi_tiles_dir,
                   'patch_mask_dir': patch_mask_dir,
                   'file_type': file_type,
                   'shape_type': shape_type
                   }

    obj = feature_extraction(**params_keys)
    obj.extract_patch_level_features()





