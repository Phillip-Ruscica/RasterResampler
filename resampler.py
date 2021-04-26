"""
This tool takes a folder of tifs and creates hillshades for each of them in the
specified output folder.
"""
import os
import arcpy


################################################################################
def resampler(ras, output_folder, cell_size):
    """ creates hillshades for all Tifs in the list"""
    # Create a hillshade of the current raster
    outpath = os.path.join(output_folder, ras[:-4] + ".tif")
    version_count = 0

    basename = outpath[:-4]
    rename = basename + "_v" + str(version_count) + ".tif"
    while os.path.exists(outpath) == True:
        outpath = rename
        version_count = version_count +1
    else:
        arcpy.Resample_management(ras, outpath, cell_size)
        arcpy.AddMessage(outpath + "    created ...")


################################################################################
def main(rast_folder, output_folder,z_factor):

    # Set the workspace to the raster folder
    arcpy.env.workspace = rast_folder

    # Produce a list of all tifs in the parent folder
    rast_list = arcpy.ListRasters()
    list_len = len(rast_list)

    # Set the counter and progressor
    count = 1
    pro_label = "Making hillshade for tif " + str(count) +" of " + str(list_len)
    arcpy.SetProgressor("step", "Warming up ...", 0, list_len, 1)
    arcpy.SetProgressorLabel(pro_label)
    # Run the hillshader for each tif
    for ras in rast_list:
        resampler(ras, output_folder,z_factor)
        arcpy.AddMessage("Finished Raster " + str(count) + " of " + str(list_len))
        arcpy.SetProgressorLabel(pro_label)
        count = count +1

    # End message that it worked
    arcpy.SetProgressorLabel("All of the hillshades have been created!")
    arcpy.SetProgressor(list_len)


################################################################################
if __name__ == '__main__':
    # Get the input parameters
    rast_folder = arcpy.GetParameterAsText(0)
    output_folder = arcpy.GetParameterAsText(1)
    # azimuth = arcpy.GetParameterAsText(2)
    # altitude = arcpy.GetParameterAsTest(3)
    # modelshadows = arcpy.GetParameterAsText(4) # this should be a boolean option between SHADOWS or NOSHADOWS
    cell_size = arcpy.GetParameterAsText(2)


    main(rast_folder, output_folder, cell_size)