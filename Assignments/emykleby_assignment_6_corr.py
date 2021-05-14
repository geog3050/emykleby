###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Eric Mykleby", "emykleby"])

###################################################################### 
# Problem 1: 20 Points
#
# Given a csv file import it into the database passed as in the second parameter
# Each parameter is described below:

# csvFile: The absolute path of the file should be included (e.g., C:/users/ckoylu/test.csv)
# geodatabase: The workspace geodatabase
###################################################################### 
def importCSVIntoGeodatabase(csvFile, geodatabase):
    
    arcpy.env.overwriteOutput = True
    
    if arcpy.Exists(geodatabase): # check for valid workspace
        arcpy.env.workspace = geodatabase # sets workspace

    else:
        print("Invalid Workspace")
        sys.exit(1)

    
    # Set in table and out table parameters need for table conversion tool
    inTable = r"C:\Users\emykl\OneDrive\Documents\GEOG-5055\Test.csv"
    outTable = "Test_Out"

    # Run table to table conversion tool to import csv file into the database
    arcpy.TableToTable_conversion(csvfile, geodatabase)

##################################################################################################### 
# Problem 2: 80 Points Total
#
# Given a csv table with point coordinates, this function should create an interpolated
# raster surface, clip it by a polygon shapefile boundary, and generate an isarithmic map

# You can organize your code using multiple functions. For example,
# you can first do the interpolation, then clip then equal interval classification
# to generate an isarithmic map

# Each parameter is described below:

# inTable: The name of the table that contain point observations for interpolation       
# valueField: The name of the field to be used in interpolation
# xField: The field that contains the longitude values
# yField: The field that contains the latitude values
# inClipFc: The input feature class for clipping the interpolated raster
# workspace: The geodatabase workspace

# Below are suggested steps for your program. More code may be needed for exception handling
#    and checking the accuracy of the input values.

# 1- Do not hardcode any parameters or filenames in your code.
#    Name your parameters and output files based on inputs. For example,
#    interpolated raster can be named after the field value field name 
# 2- You can assume the input table should have the coordinates in latitude and longitude (WGS84)
# 3- Generate an input feature later using inTable
# 4- Convert the projection of the input feature layer
#    to match the coordinate system of the clip feature class. Do not clip the features yet.
# 5- Check and enable the spatial analyst extension for kriging
# 6- Use KrigingModelOrdinary function and interpolate the projected feature class
#    that was created from the point feature layer.
# 7- Clip the interpolated kriging raster, and delete the original kriging result
#    after successful clipping. 
#################################################################################################################### 
def krigingFromPointCSV(inTable, valueField, xField, yField, inClipFc, workspace = "assignment3.gdb"):
    
    arcpy.env.overwriteOutput = True
    
    if arcpy.Exists(workspace): # check for valid workspace
        arcpy.env.workspace = workspace # sets workspace

    else:
        print("Invalid Workspace")
        sys.exit(1)

    try:    # try section where input attributes are described and if statement that checks if inputs are in the valid format
        clip_input = arcpy.Describe(inClipFc)
        table_input = arcpy.Describe(inTable)
        if clip_input.shapeType != "Polygon":
            print("Input is not shapeType Polygon")

        inTable = r"C:\Users\emykl\Downloads\hw6_data\yearly.csv"
        outTable = "yearly"
        yearly_pts = "yearly_pts"
        
        # Set the expression, with help from the AddFieldDelimiters function, to select the appropriate field delimiters for the data type
        expression = arcpy.AddFieldDelimiters(arcpy.env.workspace, "stationID") + " <> 'IA0000'"
 
        # Run table to table conversion tool to import csv file into the database
        arcpy.TableToTable_conversion(inTable, workspace, outTable, expression)

        # Run XY Table to Point tool to convert table data to new point shapefile
        arcpy.management.XYTableToPoint(outTable, yearly_pts, xfield, yfield)

        # new attributes set for use with spatial reference parameters for each input variable for comparisons
        yly_pts_pr = "yly_pts_pr"
        spatial_ref_clip = arcpy.Describe(inClipFc).spatialReference
        spatial_ref_table = arcpy.Describe(yearly_pts).spatialReference

        # Run if statement to determine if the types of the spatial references are the same
        if spatial_ref_clip.type == spatial_ref_table.type:
            print("Coordinate systems are the same")

        # Convert coordinate system projection of new points shapefile to match the projection of the clip polygon feature class
        else:
            arcpy.Project_management(inClipFc, yly_pts_pr, sp_ref_clip)
            print("Coordinate systems have been converted to the same projection")

        # Use a try statement to check and enable the spatial analyst extension for use in kriging
        try:
            if arcpy.CheckExtension("Spatial") == "Available":
                arcpy.CheckOutExtension("Spatial")
            else:
                raise LicenseError
        except LicenseError:
            print("Spatial Analyst license is unavailable")

        # Set new kriging variables, then use Kriging tool to interpolate new raster using shapefile and given value field
        valueField_K = "valueField_K"
        outKriging = Kriging(yly_pts_pr, valueField, '#')
        outKriging.save(valueField_K)

        # Describe object is used to get the minimum and maximum X and Y coordinates to obtain the bounding coordinates for the rectangle needed for clip tool
        descClip = arcpy.Describe(inClipFc)
        rectangle = str(descClip.extent.XMin) + " " + str(descClip.extent.YMin) + " " + str(descClip.extent.XMax) + " " + str(descClip.extent.YMax)

        # Clip management tool is used to clip the kriging layer with the iowa counties layer
        valueField_KC = "valueField_KC"
        arcpy.Clip_management(valueField_K, rectangle, valueField_KC, inClipFc, "#", "ClippingGeometry", "MAINTAIN_EXTENT")

    except Exception:
        e = sys.exc_info() [1]
        print(e.args[0])
        

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
