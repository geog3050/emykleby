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

import arcpy
import sys, os

###################################################################### 
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 
def printFeatureClassNames(workspace):
    
    if arcpy.Exists(workspace): # check for workspace
        arcpy.env.workspace = workspace
        fclist = arcpy.ListFeatureClasses() # creates list of all FCs
        for fc in fclist: # goes through each fc
            desc = arcpy.da.Describe(fc) 
            print("{} is a {} feature class".format(desc["baseName"],desc["shapeType"]))
    else:
        print("Invalid workspace")

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    
    if arcpy.Exists(workspace): # check for workspace
        arcpy.env.workspace = workspace
        try:
            fieldlist = arcpy.ListFields(inputFc) # lists fields
            for field in fieldlist: # goes through fields
                if field.type in ["Integer","Double","Float","SmallInteger","Single"]:
                    print("{} is a {} feature class".format(field.name,field.type))
        except Exception as e: # exception catcher
            print("Error: ",e)
    else:
        print("Invalid worspace")

###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):

     # Check for database at output path, then allows overwrite
    if arcpy.Exists(output_geodatabase) or \
        arcpy.Exists(os.path.dirname(output_geodatabase)) or \
        arcpy.Exists(os.path.dirname(input_geodatabase)):
        print("Database {} already exists".format(output_geodatabase))
        question = input("Overwrite {}? (y/n)".format(output_geodatabase)).lower()
        if question == "y":
            arcpy.Delete_management(output_geodatabase)
            print("Overwriting database and executing copy function")
        else: 
            sys.exit("Database not overwritten")
  
    if output_geodatabase.count(':') > 0: #Determine if inputs are valid
        workspace = os.path.dirname(output_geodatabase)
    elif input_geodatabase.count(':') > 0:
        workspace = os.path.dirname(input_geodatabase)
    else: 
        workspace = os.getcwd() # uses the current directory

    outGDB = arcpy.management.CreateFileGDB(workspace,os.path.basename(output_geodatabase))
    
    arcpy.env.workspace = input_geodatabase
    fclist = arcpy.ListFeatureClasses(feature_type = shapeType)
    for fc in fclist:
        arcpy.FeatureClassToFeatureClass_conversion(fc,outGDB,fc+".shp")
        print("Added {} to new GDB, a {} feature class".format(fc,shapeType))

###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):
    
    arcpy.env.workspace = workspace

    # This creates a join, then copies to the new fc, then removes the join from inputFc
    joined_fc_table = arcpy.management.AddJoin(inputFc, idFieldInputFc, inputTable, idFieldTable,"KEEP_COMMON")
    arcpy.CopyFeatures_management(joined_fc_table,"new_fc")
    arcpy.RemoveJoin_management(inputFc)

    # This obtains the number of records in the original and new fc, then this prints either matched or unmatched
    old_len = arcpy.GetCount_management(inputFc)
    new_len = arcpy.GetCount_management("new_fc")
    print("{} records matched".format(new_len))
    print("{} records unmatched".format(int(old_len[0])-int(new_len[0])))

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
