import tkinter as tk

import numpy as np
import streamlit as st
from matplotlib import pyplot as plt

from liver_frame import read_patient_information, draw_x_ray, pct_images
import os
# START - TK
root = tk.Tk()
root.withdraw()
root.wm_attributes('-topmost', 1)
# END - TK

# START - STREAM LIT PAGE CONFIG
# st.set_page_config(layout="wide")
# END - STREAM LIT PAGE CONFIG

# START - SESSION STATE
SST_SELECTED_FOLDER = 'selected folder'
SST_CENTER = 'center'
SST_WD_SIZE = 'wd_size'
SST_AXIAL_SLIDER = 'axial_slider'
SST_SAGITTAL_SLIDER = 'sagittal_slider'
SST_CORONAL_SLIDER = 'coronal_slider'


def add_to_session_state_if_absent(key, value):
    if key not in st.session_state:
        add_to_session_state(key, value)


def add_to_session_state(key, value):
    st.session_state[key] = value


def get_from_session_state(key):
    return st.session_state[key]


add_to_session_state_if_absent(SST_SELECTED_FOLDER, '')
add_to_session_state_if_absent(SST_CENTER, 50)
add_to_session_state_if_absent(SST_WD_SIZE, 90)
add_to_session_state_if_absent(SST_AXIAL_SLIDER, 0)
add_to_session_state_if_absent(SST_SAGITTAL_SLIDER, 0)
add_to_session_state_if_absent(SST_CORONAL_SLIDER, 0)
add_to_session_state_if_absent('niter', 5)
add_to_session_state_if_absent('kappa', 40)
add_to_session_state_if_absent('wdwmi', 0)
add_to_session_state_if_absent('wdwma', 1200)
add_to_session_state_if_absent('suvmi', 0)
add_to_session_state_if_absent('suvma', 20)

add_to_session_state_if_absent('SEG_' + SST_CENTER, 40)
add_to_session_state_if_absent('SEG_' + SST_WD_SIZE, 70)
add_to_session_state_if_absent('SEG_' + SST_AXIAL_SLIDER, 0)
add_to_session_state_if_absent('SEG_' + SST_SAGITTAL_SLIDER, 0)
add_to_session_state_if_absent('SEG_' + SST_CORONAL_SLIDER, 0)
add_to_session_state_if_absent('SEG_' + 'niter', 1)
add_to_session_state_if_absent('SEG_' + 'kappa', 50)
add_to_session_state_if_absent('SEG_' + 'kappa', 50)
add_to_session_state_if_absent('SEG_' + 'liver_vol_from', 40)
add_to_session_state_if_absent('SEG_' + 'liver_vol_to', 70)
add_to_session_state_if_absent('SEG_' + 'iterations', 2)



# END - SESSION STATE

# START - CACHE
# END - CACHE

# START - UTIL

## fix folder to os(fix error when macos, window://, //)
def extract_root_path_and_patient_num(selected_folder):
    opts = selected_folder.rsplit(os.sep, 1)
    return opts[0] + os.sep, opts[1]


# END - UTIL


def write_select_folder():
    import os
    d = 'data'
    dirs = [os.path.join(d, o) for o in os.listdir(d)
            if os.path.isdir(os.path.join(d, o))]
    dirs = ['None'] + dirs
    dataset_selector = st.sidebar.selectbox(
        'Choose one of the following dataset',
        dirs
    )
    if dataset_selector == 'None':
        return ''
    return dataset_selector


def main():
    selected_box = st.sidebar.selectbox(
        'Choose one of the following',
        ('Welcome', 'liver show', 'PET/CT images')
    )

    if selected_box == 'Welcome':
        welcome()
    elif selected_box == 'liver show':
        liver_show()
    elif selected_box == 'PET/CT images':
        pet_ct_image()
  


def welcome():
    #st.header('Project: GANs applications in PET-C11&F18')
    #st.subheader('Welcome subheader')
    st.title('Project: GANs applications in PET-CT')
    st.header('Process to preparing data')
    st.subheader('reparing data. '+ 'The process followed by below diagram')
    
    #st.subheader('A simple app that shows different image processing algorithms. You can choose the options'
            #+ ' from the left. I have implemented only a few to show how it works on Streamlit. ' + 
            # 'You are free to add stuff to this app.')    
    
    st.image('fig.png',use_column_width=True)

    # TODO: change image
    #st.image('png.png')


def liver_show():
    selected_folder = write_select_folder()
    if selected_folder != '':
        root_path, patient_num = extract_root_path_and_patient_num(selected_folder)
        st.title('liver show')
        with st.expander("Patient's information"):
            st.dataframe(read_patient_information(root_path, patient_num))
        col1, col2 = st.columns(2)
        if '@@@xray --- ' + root_path + patient_num in st.session_state:
            print('IN')
            z = st.session_state['@@@xray --- ' + root_path + patient_num]
        else:
            print('NOT IN')
            z = draw_x_ray(root_path, patient_num)
            st.session_state['@@@xray --- ' + root_path + patient_num] = z


        #values2 = col1.slider(
            #'Contrast',
            #0, 70, (st.session_state['suvmi'], st.session_state['suvma']), key="4")

        
        #plt.imshow(z, cmap="gray",vmin= values2[0], vmax= values2[1])
        plt.imshow(z, cmap="gray")
        plt.colorbar()
        col1.pyplot(plt)

      


def pet_ct_image():
    selected_folder = write_select_folder()
    if selected_folder != '':
        root_path, patient_num = extract_root_path_and_patient_num(selected_folder)
        st.title('PET/CT images')

        selecter_top = st.sidebar.selectbox(
            'Choose one of the following',
            ('ACT', 'FDG')
        )

        n_center = st.sidebar.number_input('Center: ', value=st.session_state[SST_CENTER])
        n_wd_size = st.sidebar.number_input('Window size: ', value=st.session_state[SST_WD_SIZE])
        n_niter = st.sidebar.slider("Niter", 1, 10, key="12", value=st.session_state['niter'])
        n_kappa = st.sidebar.slider("Kappa", 10, 100, key="13", value=st.session_state['kappa'])

        st.session_state[SST_CENTER] = n_center
        st.session_state[SST_WD_SIZE] = n_wd_size
        st.session_state['niter'] = n_niter
        st.session_state['kappa'] = n_kappa

        ma = 1200
        mi = 0
        values = st.sidebar.slider(
            'CT: Hounsfield windowing',
            mi, ma, (st.session_state['wdwmi'], st.session_state['wdwma']))

        st.session_state['wdwmi'] = values[0]
        st.session_state['wdwma'] = values[1]

        liver_vol = None
        b = None
        crop_vol = None
        fdg_3d = None
        liver_bg = None
        img_sg = None
        if str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(n_niter) + '@@@' + str(
                n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                n_wd_size) + '@@@' + root_path + patient_num + 'liver_bg' in st.session_state:
            liver_bg = st.session_state[
                str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(
                    n_niter) + '@@@' + str(n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                    n_wd_size) + '@@@' + root_path + patient_num + 'liver_bg']           
        if str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(n_niter) + '@@@' + str(
                n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                n_wd_size) + '@@@' + root_path + patient_num + 'img_sg' in st.session_state:
            img_sg = st.session_state[
                str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(
                    n_niter) + '@@@' + str(n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                    n_wd_size) + '@@@' + root_path + patient_num + 'img_sg']
        if str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(n_niter) + '@@@' + str(
                n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                n_wd_size) + '@@@' + root_path + patient_num + 'fdg_3d' in st.session_state:
            fdg_3d = st.session_state[
                str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(
                    n_niter) + '@@@' + str(n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                    n_wd_size) + '@@@' + root_path + patient_num + 'fdg_3d']
        if str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(n_niter) + '@@@' + str(
                n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                n_wd_size) + '@@@' + root_path + patient_num + 'liver_vol' in st.session_state:
            liver_vol = st.session_state[
                str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(
                    n_niter) + '@@@' + str(n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                    n_wd_size) + '@@@' + root_path + patient_num + 'liver_vol']
        if str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(n_niter) + '@@@' + str(
                n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                n_wd_size) + '@@@' + root_path + patient_num + 'crop_vol' in st.session_state:
            crop_vol = st.session_state[
                str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(
                    n_niter) + '@@@' + str(n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                    n_wd_size) + '@@@' + root_path + patient_num + 'crop_vol']
        if str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(n_niter) + '@@@' + str(
                n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                n_wd_size) + '@@@' + root_path + patient_num + 'b' in st.session_state:
            b = st.session_state[str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(
                n_niter) + '@@@' + str(n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                n_wd_size) + '@@@' + root_path + patient_num + 'b']
        if fdg_3d is None or crop_vol is None or liver_vol is None or b is None:
            crop_vol, liver_vol, b, fdg_3d, liver_bg,  img_sg, _ = pct_images(selecter_top, root_path, patient_num,
                                                                             n_center, n_wd_size, n_niter, n_kappa,
                                                                             values[0], values[1])
            st.session_state[
                str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(
                    n_niter) + '@@@' + str(n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                    n_wd_size) + '@@@' + root_path + patient_num + 'liver_bg'] = liver_bg                  
            st.session_state[
                str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(
                    n_niter) + '@@@' + str(n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                    n_wd_size) + '@@@' + root_path + patient_num + 'img_sg'] = img_sg
            st.session_state[
                str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(
                    n_niter) + '@@@' + str(n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                    n_wd_size) + '@@@' + root_path + patient_num + 'fdg_3d'] = fdg_3d
            st.session_state[
                str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(
                    n_niter) + '@@@' + str(n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                    n_wd_size) + '@@@' + root_path + patient_num + 'liver_vol'] = liver_vol
            st.session_state[
                str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(
                    n_niter) + '@@@' + str(n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                    n_wd_size) + '@@@' + root_path + patient_num + 'crop_vol'] = crop_vol
            st.session_state[str(selecter_top) + '@@@' + str(values[0]) + '@@@' + str(values[1]) + '@@@' + str(
                n_niter) + '@@@' + str(n_kappa) + '@@@' + str(n_center) + '@@@' + str(
                n_wd_size) + '@@@' + root_path + patient_num + 'b'] = b

        col1, col2 = st.columns(2)
        col1.subheader('Axial')
        axial_slider = col1.slider("Actual scale", 1, 200, key="1", value=st.session_state['axial_slider'])
        a = crop_vol[axial_slider, :, :]  # actual scale
        a = np.where((a >= 40) & (a<=70), 1, 0)
        plt.clf()
        plt.imshow(a, cmap='gray')
        col1.pyplot(plt)
        # a = bone_vol[axial_slider, :, :]
        # a = np.where((a >= 150), 1, 0)
        # plt.imshow(a, cmap='gray')
        #plt.imshow(crop_vol[axial_slider, :, :], cmap="gray")
        #plt.colorbar()
        col2.subheader('Sagittal')
        sagittal_slider = col2.slider("Actual scale", 1, 200, key="2", value=st.session_state['sagittal_slider'])
        d = crop_vol[:, :, sagittal_slider]  # actual scale
        d = np.where((d >= 40) & (d<=70), 1, 0)
        plt.clf()
        plt.imshow(d, cmap='gray')
        col2.pyplot(plt)

        col1, col2 = st.columns(2)
        col1.subheader('Coronal')
        coronal_slider = col1.slider("Actual scale", 1, 200, key="3", value=st.session_state['coronal_slider'])
        c = crop_vol[:, coronal_slider, :]  # actual scale
        c = np.where((c >= 40) & (c<=70), 1, 0)
        plt.clf()
        plt.imshow(c, cmap='gray')
        col1.pyplot(plt)

        st.subheader('PET/CT image')
        col1, col2 = st.columns(2)
        # plt.imshow(b, cmap='gray')
        # col1.pyplot(plt)
        # plt.imshow(fdg_3d, cmap='binary', vmax=8)
        # plt.colorbar()
        # col1.pyplot(plt)

        values2 = col2.slider(
            'Standard uptake value (SUV)',
            0, 20, (st.session_state['suvmi'], st.session_state['suvma']), key="4")

        st.session_state['suvmi'] = values2[0]
        st.session_state['suvma'] = values2[1]

        selecter = col2.selectbox(
            'Choose one of the following',
            ('PET_CT', 'PET', 'ACT/FDG_CT')
        )

        # niter -> n iter

        print(values2)
        # plt.imshow(b, cmap='hot', vmin=values2[0], vmax=values2[1])
        # plt.colorbar()
        # col2.pyplot(plt)

        col1, col2 = st.columns(2)
        plt.clf()
        plt.imshow(fdg_3d, cmap='binary', vmax=8)
        plt.colorbar()
        col1.pyplot(plt)

        plt.clf()

        if selecter == 'PET_CT':
            plt.imshow(img_sg, cmap='hot', alpha=0.5, vmin=values2[0], vmax=values2[1])
        elif selecter == 'PET':
            plt.imshow(img_sg, cmap='hot', alpha=0.5, vmin=values2[0], vmax=values2[1])
            plt.colorbar()
        else:
            plt.imshow(liver_bg, cmap='gray')
            plt.imshow(img_sg, cmap='hot', alpha=0.5, vmin=values2[0], vmax=values2[1])
            plt.colorbar()

        col2.pyplot(plt)

        #plt.savefig('pet.png')
        #with open("pet.png", "rb") as file:
            #col2.download_button(
                #label="Download",
                #data=file,
                #file_name='pet.png',
                #mime='image/png',
            #)

        st.session_state['center'] = n_center
        st.session_state['wd_size'] = n_wd_size
        st.session_state['axial_slider'] = axial_slider
        st.session_state['sagittal_slider'] = sagittal_slider
        st.session_state['coronal_slider'] = coronal_slider
        print('DEBUG: ', st.session_state['axial_slider'])



        #selected_folder = write_select_folder()
        #if selected_folder != '':
            #root_path, patient_num = extract_root_path_and_patient_num(selected_folder)
        #st.title('liver show')
        #with st.expander("Patient's information"):
            #st.dataframe(read_patient_information(root_path, patient_num))
        #col1, col2 = st.columns(2)
        #if '@@@xray --- ' + root_path + patient_num in st.session_state:
            #print('IN')
            #k = st.session_state['@@@xray --- ' + root_path + patient_num + os.sep  + patient_num +'.png']
        #else:
            #print('NOT IN')
            #patient_no = patient_num
            #file = '.png'
            #k = read_img(root_path, patient_num, patient_no, file)
            #st.session_state['@@@xray --- ' + root_path + patient_num + os.sep+ patient_num +'.png'] = k
        if  selecter_top == 'ACT':
            col2.image(selected_folder+os.sep+'ACT' +os.sep+ patient_num + '.png')
            with open(selected_folder+os.sep+'ACT'+os.sep + patient_num + '.png', "rb") as file:
                col2.download_button(
                    label="Download",
                    data=file,
                    file_name=selected_folder+os.sep+'ACT'+os.sep + patient_num + '.png',
                    mime='image/png',
                )
        else:    
            col2.image(selected_folder+os.sep+'FDG'+os.sep + patient_num + '.png')
            with open(selected_folder+os.sep+'FDG' +os.sep + patient_num + '.png', "rb") as file:
                col2.download_button(
                    label="Download",
                    data=file,
                    file_name=selected_folder+os.sep+'FDG'+os.sep + patient_num + '.png',
                    mime='image/png',
                )
        st.session_state['SEG_' + 'center'] = n_center
        st.session_state['SEG_' + 'wd_size'] = n_wd_size
        st.session_state['SEG_' + 'axial_slider'] = axial_slider
        st.session_state['SEG_' + 'sagittal_slider'] = sagittal_slider
        st.session_state['SEG_' + 'coronal_slider'] = coronal_slider


if __name__ == "__main__":
    main()



