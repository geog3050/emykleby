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
# Problem 1 (20 Points)
#
# This function reads all the feature classes in a workspace, and
# prints the number of feature classes by each shape type. For example,
# polygon: 3, polyline: 2, point: 4

###################################################################### 
def printNumberOfFeatureClassesByShapeType(workspace):
    if arcpy.Exists(workspace): # checks if this is a valid workspace
        arcpy.env.workspace = workspace # sets workspace
        fclist = arcpy.ListFeatureClasses() # gets list of all FCs in the workspace
        shapeList = [] # creates an empty list to fill during for loop
        for fc in fclist: # iterates through each fc
            desc = arcpy.Describe(fc).shapeType # creates a description variable of the fc
            shapeList.append(desc) # adds shape types to list
        for shape in set(shapeList): # iterates through each shape type
            shapeCount = shapeList.count(shape) # counts each shape by type
            print("{}: {}".format(shape,shapeCount)) # prints the shape type and amount
    else:
        print("Invalid workspace")

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the feature classes in a workspace, and
# prints the coordinate systems for each file

###################################################################### 
def printCoordinateSystems(workspace):
    if arcpy.Exists(workspace): # check for valid workspace
        arcpy.env.workspace = workspace # sets workspace
        fclist = arcpy.ListFeatureClasses() # gets list of all FCs in the workspace
        for fc in fclist: # iterates through each fc
            spatial_ref = arcpy.Describe(fc).spatialReference # creates a description variable for each fc along with the spatial reference
            if spatial_ref.name == "Unknown": # loops through each fc and prints feature class and spatial reference
                print("{} has an unknown spatial reference".format(fc))
            else:
                print("The coordinate system of {} is {}".format(fc, spatial_ref.name))

###################################################################### 
# Problem 3 (60 Points)
#
# Given two feature classes in a workspace:
# check whether their coordinate systems are
# the same, and if not convert the projection of one of them to the other.
# If one of them has a geographic coordinate system (GCS) and the other has
# a projected coordinate system (PCS), then convert the GCS to PCS. 

###################################################################### 
def autoConvertProjections(fc1, fc2, workspace):
    if arcpy.Exists(workspace): # check for valid workspace
        arcpy.env.workspace = workspace # sets workspace
        spatial_ref1 = arcpy.Describe(fc1).spatialReference # creates a description variable for each fc along with the spatial reference
        spatial_ref2 = arcpy.Describe(fc2).spatialReference
        if spatial_ref1.name == spatial_ref2.name: # if statement to determine if spatial reference names are the same
            print("Coordinate systems are the same")
        elif (spatial_ref1.type == "Geographic") and (spatial_ref2.type == "Geographic"): # statements to determine if the spatial reference of each fc are the same type
            print("Coordinate systems are the same type")
        elif (spatial_ref1.type == "Projected") and (spatial_ref2.type == "Projected"): 
            print("Coordinate systems are the same type")
        elif (spatial_ref1.type == "Projected") and (spatial_ref2.type == "Geographic"):
            arcpy.Project_management(fc1, "fc2_proj", spatial_ref2)
            print("New coordinate type for fc2 is Projected")
        elif (spatial_ref1.type == "Geographic") and (spatial_ref2.type == "Projected"): # if they are not the same type, then whichever fc is not projected is changed to projected
            arcpy.Project_management(fc2, "fc1_proj", spatial_ref1)
            print("New coordinate type for fc1 is Projected")
            
######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
