import subprocess
from va.utils.misc import *
from distutils.spawn import find_executable
from va.metrics.contour_level_predicator import *
import mrcfile

def create_relion_folders(root, mapname, result_type):
    """
    Create <mapname>_relion folder in the va directory and subfolders containing mask, fsc and local_resolution
    """
    relion_dir = f'{root}{mapname}_relion'
    mask_dir = f'{relion_dir}/mask'
    fsc_dir = f'{relion_dir}/fsc'
    local_resolution_dir = f'{relion_dir}/local_resolution'

    if create_directory(relion_dir) and create_directory(mask_dir):
        print('Relion folder and mask folder created.')
        if result_type == 'fsc':
            if create_directory(fsc_dir):
                print('FSC folder created.')
                return fsc_dir, mask_dir
            else:
                print('FSC folder was not created. Please check.')
                return None, None

        if result_type == 'locres':
            if create_directory(local_resolution_dir):
                print('FSC folder created.')
                return local_resolution_dir, mask_dir
            else:
                print('FSC folder was not created. Please check.')
                return None, None
        print('Check the input folder type either fsc or locres.')
        return None, None
    else:
        print('Relion folder and mask folder was not created. Please check')
        return None, None


def check_mrc(input_map):
    """
    Check if the input map is in MRC format. If not, create a symbolic link in the same folder ends with mrc
    """

    suffix = '.mrc'
    if not input_map.endswith('.mrc'):
        last_dot_index = input_map.rfind('.')
        mrc_input_map = input_map[:last_dot_index] + suffix
        if create_symbolic_link(input_map, mrc_input_map):
            return mrc_input_map
    else:
        print('MRC file format.')
        return None

def relion_mask(mapone, maptwo, out_dir, relion_mask_executable, mapname=None):

    original_input_mrc = check_mrc(mapone)
    angpix = get_voxel_size(mapone)
    input_mrc = mrcfile.open(original_input_mrc)
    d = input_mrc.data
    max_val_thirty = f'{calc_level_dev(d)[0] * 0.7}'

    dilatepx, softpx = calculate_pixels(angpix)
    mask_loose = os.path.join(out_dir, f'{mapname}_mask.mrc')

    if angpix and max_val_thirty and dilatepx and softpx and input_mrc:

        subprocess.run(f'{relion_mask_executable} --i {original_input_mrc} --o {mask_loose} --ini_threshold {max_val_thirty} '
                       f'--extend_inimask {dilatepx} --width_soft_edge {softpx} --lowpass 12 ', shell=True)

        return mask_loose
    else:
        print(f'!!! Check the cmd: {relion_mask_executable} --i {original_input_mrc} --o {mask_loose} --ini_threshold {max_val_thirty} '
                       f'--extend_inimask {dilatepx} --width_soft_edge {softpx} --lowpass 12')
        return None


def relion_fsc(mapone, maptwo, out_dir, relion_executable, mapname=None):
    """
    Relion FSC calculation running
    """

    mapone_mrc = check_mrc(mapone)
    maptwo_mrc = check_mrc(maptwo)
    mask_file = f'{os.path.dirname(out_dir)}/mask/{mapname}_mask.mrc'

    if mapone_mrc and maptwo_mrc and mask_file:

        subprocess.run(f"{relion_executable} --i {mapone_mrc} --i2 {maptwo_mrc} --o {out_dir}/fsc"
                           f" --mask {mask_file} --auto_bfac", shell=True)

        return True
    else:
        print(f'!!! Check the cmd: f"{relion_executable} --i {mapone_mrc} --i2 {maptwo_mrc} --o {out_dir}/fsc"'
              f' --mask {mask_file} --auto_bfac", shell=True)"')
        return None

def relion_fsc_calculation(mapone, maptwo, root, mapname=None):
    """
    Calculates FSc using Relion

    return: data dictionary of fsc
    """

    result_type = 'fsc'
    if not mapname:
        mapname = f'{os.path.basename(mapone)}_{os.path.basename(maptwo)}'
    fsc_dir, mask_dir = create_relion_folders(root, mapname, result_type)
    relion_executable_name = 'relion_postprocess'
    relion_mask_executable_name = 'relion_mask_create'

    try:
        assert find_executable(relion_executable_name) and find_executable(relion_mask_executable_name) is not None
        relion_executable = find_executable(relion_executable_name)
        relion_mask_executable = find_executable(relion_mask_executable_name)
        if fsc_dir and mask_dir and relion_mask_executable:
            relion_mask(mapone, maptwo, mask_dir, relion_mask_executable, mapname)
            if relion_fsc(mapone, maptwo, fsc_dir, relion_executable, mapname):
                return f'{fsc_dir}/fsc.star'
            else:
                return None

    except Exception as e:
        print('No relion or fsc calculation was wrong.')
        return None

def get_voxel_size(input_map):

    try:
        with mrcfile.open(input_map, permissive=True) as mrc:
            voxel_size = mrc.voxel_size

            return float(voxel_size['x'])
    except Exception as e:
        print('No voxel size of the map.')
        return None


# def get_max_value(input_map):
#     """
#     Get max value from the input map
#     """
#
#     try:
#         with mrcfile.open(input_map, permissive=True) as mrc:
#             dmax = mrc.header.dmax
#
#             return float(dmax)
#     except Exception as e:
#         print('No max value of the input map.')
#         return None


def calculate_pixels(angpix):
    """
    Calculate hard and soft pixel for mask map
    """

    if angpix != 0:
        dilatepx = 10 / angpix
        softpx = 5 / angpix
        return dilatepx, softpx
    else:
        print('No hard and soft radius for mask as voxel value is 0.')
        return None, None


# def read_fscs(star):
#     # Read the block, note data_fsc becomes fsc
#     fsc_block = cif.read_file(str(star)).find_block("fsc")
#
#     # Read the loop, note loop_ excluded and only search by suffix
#     resolution = list(fsc_block.find_loop("_rlnResolution"))
#     resolutionAng = list(fsc_block.find_loop("_rlnAngstromResolution"))
#     fsc = list(fsc_block.find_loop("_rlnFourierShellCorrelationCorrected"))
#     fsc_unmasked = list(fsc_block.find_loop("_rlnFourierShellCorrelationUnmaskedMaps"))
#     fsc_randomised = list(fsc_block.find_loop("_rlnCorrectedFourierShellCorrelationPhaseRandomizedMaskedMaps"))
#
#     # Create a DataFrame for the fsc values
#     data = {
#         'resolution': pd.Series(resolution, dtype=float),
#         'resolutionAng': pd.Series(resolutionAng, dtype=float),
#         'fsc_corrected': pd.Series(fsc, dtype=float),
#         'fsc_unmasked': pd.Series(fsc_unmasked, dtype=float),
#         'fsc_randomised': pd.Series(fsc_randomised, dtype=float)
#     }
#     df = pd.DataFrame(data)
#
#     return df

# def assess_fscs(star, df):
#     print('Assessing post processing star file')
#     ## Postprocessing information
#     # Read the block, note data_
#     block = cif.read_file(star).find_block("general")
#
#     # Read star file pairs, excluded and only search by suffix
#     randomise = block.find_pair("_rlnRandomiseFrom")[1]
#
#     bfac = block.find_pair("_rlnBfactorUsedForSharpening")[1]
#
#     # Look up the 'resolution' value corresponding to the 'randomise' value in df
#     resolution_randomise = df[df['resolutionAng'] == float(randomise)]['resolution'].values
#
#     # Check if the resolution corresponding to randomise value is found in df
#     if resolution_randomise:
#         resolution_randomise = resolution_randomise[0]
#     else:
#         resolution_randomise = 0
#
#     ## Do some sanity checks on the FSC curves
#     # Report
#     print()
#     print('### Phase randomisation assessment:')
#     print()
#     print(f"The resolution (Ang) value where phases were randomised is: {randomise}")
#     print(f"The corresponding resolution value is: {resolution_randomise}")
#     print()
#
#     # Filter the DataFrame for FSC_randomised values below 0.143
#     filtered_df = df[df['fsc_randomised'] < 0.143]
#     # Check if there are rows in the filtered DataFrame
#     if not filtered_df.empty:
#         randomisation_drop = 'normal behaviour'
#         # Retrieve the resolution value when FSC drops below 0.143
#         resolutionAng_rdm_below_0_143 = filtered_df.iloc[0]['resolutionAng']
#         resolution_rdm_below_0_143 = filtered_df.iloc[0]['resolution']
#         print(f"The resolution (Ang) value where FSC_randomised drops below 0.143 is: {resolutionAng_rdm_below_0_143}")
#         print(f"The corresponding resolution value is: {resolution_rdm_below_0_143}")
#         print()
#
#         # Is the rate of drop from phase randomisation rapid?
#         differenceAng = float(randomise) - float(resolutionAng_rdm_below_0_143)
#         difference = float(resolution_rdm_below_0_143) - float(resolution_randomise)
#         print(f"The FSC_randomisation drops from 1-0.143 in x (Ang): {differenceAng}")
#         print(f"The FSC_randomisation drops from 1-0.143 in x (1/Ang): {difference}")
#         print('Low values are better, indicating a rapid drop in the phase randomised curve after phase randomisation')
#         print()
#         # This is an example check and needs validating to establish what the correct normal and abnormal behaviour is
#         if difference > 0.05:
#             randomisation_rate = 'abnormal behaviour'
#         else:
#             randomisation_rate = 'normal behaviour'
#
#     else:
#         randomisation_rate = 'N.D.'
#         randomisation_drop = 'abnormal behaviour'
#
#     # Phase randomisation reporting
#     print('1: FSC_randomised drops below 0.143: '+randomisation_drop)
#     print('2: FSC_randomised drop rate from 1-0.143: '+randomisation_rate)
#
#     print()
#     print('### Resolution assessment:')
#     print()
#
#     measure_resolution(df, 0.143, 'fsc_randomised', 'FSC_randomised')
#     measure_resolution(df, 0.143, 'fsc_unmasked', 'FSC_unmasked')
#     measure_resolution(df, 0.143, 'fsc_corrected', 'FSC_masked_corrected')
#
#     print()
#
#     # Declare naughty global variables
#     assess_fscs.bfac = bfac

# def measure_resolution(df, threshold, column, label):
#     # Filter the DataFrame for FSC values below 0.143
#     filtered_df = df[df[column] < threshold]
#     # Retrieve the resolution value when FSC drops below 0.143
#     resolution_below_0_143 = filtered_df.iloc[0]['resolutionAng']
#
#     print(f"The resolution (Ang) value where FSC drops below "+str(threshold)+" for "+str(label)+": "+str(resolution_below_0_143))


# def generate_mask(mapname, mapone, maptwo, out_dir):
#
#     angpix = get_voxel_size(mapone)
#     dilatepx, softpx = calculate_pixels(angpix)
#
#     output_directory = os.path.join(out_dir, f'{mapname}_relion_phrand')
#     mask_loose = os.path.join(output_directory, f'{mapname}_mask_loose.mrc')
#     os.makedirs(output_directory, exist_ok=True)
#
#     if not os.path.isfile(mask_loose):
#         output = subprocess.run(f"relion_image_handler --i {mapone} --stats", shell=True, capture_output=True,
#                                 text=True)
#         mapvalmax = output.stdout.split('=')[5].split(';')[0]
#
#         mapval25 = float(mapvalmax) * 0.30
#         mapval25_formatted = f"{mapval25:.3f}"
#
#         print(f"The 30% of mapvalmax is: {mapval25_formatted}")
#
#         subprocess.run(
#             f"relion_mask_create --i {mapone} --o {mask_loose} --ini_threshold {mapval25_formatted} --extend_inimask {dilatepx} --width_soft_edge {softpx}",
#             shell=True)
#
#         return mask_loose
#     else:
#         print("mask_loose.mrc already exists. Skipping mask creation.")
#         return None


# def generate_star(mapname, mapone, maptwo, out_dir):
#
#     mask_loose = generate_mask(mapname, mapone, out_dir)
#     postprocess_star_file = os.path.join(out_dir, f'{mapname}_postprocess.star')
#     if not os.path.isfile(postprocess_star_file) and os.path.isfile(mask_loose):
#         subprocess.run(f"relion_postprocess --i {mapone} --i2 {maptwo} --o {out_dir}/{mapname}_relion_phrand --mask {mask_loose} --auto_bfac",
#             shell=True)
#     else:
#         print("postprocess.star already exists. Skipping post-processing.")
#
#
#     if os.path.isfile(postprocess_star_file):
#         return postprocess_star_file
#     else:
#         return None

# def create_mrclink(mapone, maptwo):
#
#     cmapone = mapone[:-2] + 'rc'
#     cmaptwo = maptwo[:-2] + 'rc'
#     if not os.path.isfile(cmapone):
#         create_symbolic_link(mapone, cmapone)
#     if not os.path.isfile(cmaptwo):
#         create_symbolic_link(maptwo, cmaptwo)
#
#     return cmapone, cmaptwo
#

# def plot_fsc(df, plt_name):
#     # Set the style to whitegrid
#     plt.style.use('seaborn-whitegrid')
#
#     # Create a figure and axis objects
#     fig, ax = plt.subplots(figsize=(10, 6))
#
#     # Plot scatter plots
#     ax.scatter(df["resolution"], df["fsc_corrected"], label="FSC_masked_corrected", color='blue')
#     ax.scatter(df["resolution"], df["fsc_unmasked"], label="FSC_unmasked", color='grey')
#     ax.scatter(df["resolution"], df["fsc_randomised"], label="FSC Randomised", color='orange')
#
#     # Plot line plots
#     ax.plot(df["resolution"], df["fsc_corrected"], color='blue')
#     ax.plot(df["resolution"], df["fsc_unmasked"], color='grey')
#     ax.plot(df["resolution"], df["fsc_randomised"], color='orange')
#
#     # Add a horizontal line at FSC value 0.143
#     ax.axhline(y=0.143, color='red', linestyle='--', label='FSC = 0.143')
#
#     # Set title and labels
#     ax.set_title('FSC Corrected')
#     ax.set_xlabel('Resolution (1/Ang)')
#     ax.set_ylabel('FSC Values')
#
#     # Add legend
#     ax.legend()
#
#     # Save the plot
#     plt.savefig(plt_name)



# def plot_fsc(df, plt_name):
#     ## Plotting the scatter plot with lines
#     sns.set(style="whitegrid")
#
#     plt.figure(figsize=(10, 6))
#
#     sns.scatterplot(data=df, x="resolution", y="fsc_corrected", label="FSC_masked_corrected", color='blue')
#     sns.scatterplot(data=df, x="resolution", y="fsc_unmasked", label="FSC_unmasked", color='grey')
#     sns.scatterplot(data=df, x="resolution", y="fsc_randomised", label="FSC Randomised", color='orange')
#
#     sns.lineplot(data=df, x="resolution", y="fsc_corrected", color='blue')
#     sns.lineplot(data=df, x="resolution", y="fsc_unmasked", color='grey')
#     sns.lineplot(data=df, x="resolution", y="fsc_randomised", color='orange')
#
#     # Add a horizontal line at FSC value 0.143
#     plt.axhline(y=0.143, color='red', linestyle='--', label='FSC = 0.143')
#
#     plt.title('FSC Corrected')
#     plt.xlabel('Resolution (1/Ang)')
#     plt.ylabel('FSC Values')
#
#     plt.legend()
#     plt.savefig(plt_name)
# def post_phrand(mapname, mapone, maptwo, out_dir):
#
#     onemrc, twomrc = create_mrclink(mapone, maptwo)
#     ## Define the relion postprocess.star file for assessment
#     star = generate_star(mapname, onemrc, twomrc, out_dir)
#
#     ## Read FSC values into dataframe
#     if star:
#         df = read_fscs(star)
#
#         ## Do FSC curve assessments
#         assess_fscs(star, df)
#
#     # Check if the postprocess.star file already exists
#     if not star:
#         subprocess.run(f"relion_postprocess --i {input_file1} --i2 {input_file2} --o {output_directory}/postprocess --mask {mask_loose} --adhoc_bfac {assess_fscs.bfac} --locres", shell=True)
#     else:
#         print("postprocess.star already exists. Skipping post-processing.")
#
#     ## plot FSC curves
#     plot_name = f'{out_dir}/{mapname}_relion_fsc.png'
#     plot_fsc(df, plot_name)