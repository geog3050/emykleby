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
import sys

###################################################################### 
# Problem 1 (30 Points)
#
# Given a polygon feature class in a geodatabase, a count attribute of the feature class(e.g., population, disease count):
# this function calculates and appends a new density column to the input feature class in a geodatabase.

# Given any polygon feature class in the geodatabase and a count variable:
# - Calculate the area of each polygon in square miles and append to a new column
# - Create a field (e.g., density_sqm) and calculate the density of the selected count variable
#   using the area of each polygon and its count variable(e.g., population) 
# 
# 1- Check whether the input variables are correct(e.g., the shape type, attribute name)
# 2- Make sure overwrite is enabled if the field name already exists.
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate area calculation and conversion
# 4- Give a warning message if the projection is a geographic projection(e.g., WGS84, NAD83).
#    Remember that area calculations are not accurate in geographic coordinate systems. 
# 
###################################################################### 
def calculateDensity(fcpolygon, attribute, geodatabase = "assignment2.gdb"):

    arcpy.env.overwriteOutput = True
    
    if arcpy.Exists(geodatabase): # check for valid workspace
        arcpy.env.workspace = geodatabase # sets workspace

    else:
        print("Invalid Workspace")
        sys.exit(1)

    try:    # try section where input attributes are described and if statement that checks if inputs are in the valid format
        att_input = arcpy.Describe(attribute)
        fc_input = arcpy.Describe(fcpolygon)
        if fc_input.shapeType != "Polygon":
            print("Input is not shapeType Polygon")
        
            # check to see if attribute is name is in list of field names
        fieldname = [field.name for field in arcpy.ListFields(fcpolygon)]
        if attribute not in fieldname:
            print("Attribute not a field")
        else:
            arcpy.AddField_management(fcpolygon, "area_sqmi", "DOUBLE") 

            # new attributes set for use with spatial reference parameters for each input variable for comparisons
        spatial_ref_poly = arcpy.Describe(fcpolygon).spatialReference
        spatial_ref_att = arcpy.Describe(attribute).spatialReference

            # if statement to determine if coordinate system of polygon feature class is in geographic or projected format
        if spatial_ref_poly.type == "Geographic":
            print("{} has a Geographic coordinate system. Calculations are not accurate".format(fcpolygon))
        else:
            print("{} has a Projected coordinate system.".format(fcpolyon))
            
            # calculate the area of each polygon in square miles 
            area_calc_exp = "{0}".format("!SHAPE.area@SQUAREMILES!")
            arcpy.CalculateField_management(fcpolygon,"area_sqmi", area_calc_exp, "PYTHON3")
            
            # field is added to polygon feature class to hold the density calculation
            arcpy.AddField_management(fcpolygon, "density_sqm", "DOUBLE")

            # calculate the density of the selected count variable using the area of each polygon and its count variable
            density = "density_sqm"
            arcpy.CalculateField_management(fcpolygon, "density_sqm", "!attribute!/!area_sqmi!", "PYTHON3")
            print(density = "density_sqm")

            # if linear unit names are not the same, system will exit
        else:
            print("Units of inputs are not the same")
            sys.exit(1)

    except Exception:
        e = sys.exc_info() [1]
        print(e.args[0])

###################################################################### 
# Problem 2 (40 Points)
# 
# Given a line feature class (e.g.,river_network.shp) and a polygon feature class (e.g.,states.shp) in a geodatabase, 
# id or name field that could uniquely identify a feature in the polygon feature class
# and the value of the id field to select a polygon (e.g., Iowa) for using as a clip feature:
# this function clips the linear feature class by the selected polygon boundary,
# and then calculates and returns the total length of the line features (e.g., rivers) in miles for the selected polygon.
# 
# 1- Check whether the input variables are correct (e.g., the shape types and the name or id of the selected polygon)
# 2- Transform the projection of one to other if the line and polygon shapefiles have different projections
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate distance calculation and conversion
#        
###################################################################### 
def estimateTotalLineLengthInPolygons(fcLine, fcClipPolygon, polygonIDFieldName, clipPolygonID, geodatabase = "assignment2.gdb"):
    
    arcpy.env.overwriteOutput = True

    if arcpy.Exists(geodatabase): # check for valid workspace
        arcpy.env.workspace = geodatabase # sets workspace

    else:
        print("Invalid Workspace")
        sys.exit(1)

    try: # try section where input attributes are described and if statement that checks if inputs are in the valid format
        Line_input = arcpy.Describe(fcLine)
        Poly_input = arcpy.Describe(fcClipPolygon)
        if Line_input.shapeType != "Polyline": 
            print("Input shape types are invalid")
            sys.exit(1)
        elif Poly_input.shapeType != "Polygon":
            print("Input shape types are invalid")
            sys.exit(1)

        # new attributes set for use with spatial reference parameters for each input variable for comparisons, also a new projection variable    
        spatial_ref_line = arcpy.Describe(fcLine).spatialReference
        spatial_ref_poly = arcpy.Describe(fcClipPolygon).spatialReference
        fcPoly_proj = "fcPoly_proj"

        # run select by attributes to obtain the correct portion of the polygon feature class for later use
        sla_poly = arcpy.SelectLayerByAttribute_management(fcClipPolygon, "NEW_SELECTION", "{polygonIDFieldName} = '{clipPolygonID}'")

        # run initial if statement to determine if the linear unit name of the spatial references are the same
        if spatial_ref_line.linearUnitName == spatial_ref_poly.linearUnitName:
            print("Units of input feature classes are the same")

            # if the units are the same, run another if statement to determine if the types of the spatial references are the same
            if spatial_ref_line.type == spatial_ref_poly.type:
                print("Coordinate systems are the same")

                # if the spatial reference types are the same, then run clip analysis for the line feature class and polygon feature class to create a new clipped feature
                arcpy.Clip_analysis(fcLine, sla_poly, "fcClip")

                # calculate the line length variable and summarize it by using dissolve management tool
                arcpy.Dissolve_management("fcClip", "line_length", ["ARCID", "Shape_Length"], "SUM")

                # if the spatial reference types are the same, then we first must project the polygon feature class to the same spatial reference type as the line feature class
            else:
                arcpy.Project_management(fcLine, fcPoly_proj, spatial_ref_line)
                print("Coordinate systems have been converted to the same projection")

                # Run clip analysis for the line feature and now polygon feature class to create a new clipped feature
                arcpy.Clip_analysis(fcLine, fcPoly_proj, "fcClip_proj")

                # calculate the line length variable and summarize it by using dissolve management tool
                arcpy.Dissolve_management("fcClip_proj", "line_length", ["ARCID", "Shape_Length"], "SUM")

        else:
            print("Units of input feature classes are not the same")
            sys.exit(1)

    except Exception:
        e = sys.exc_info() [1]
        print(e.args[0])


######################################################################
# Problem 3 (30 points)
# 
# Given an input point feature class, (i.e., eu_cities.shp) and a distance threshold and unit:
# Calculate the number of points within the distance threshold from each point (e.g., city),
# and append the count to a new field (attribute).
#
# 1- Identify the input coordinate systems unit of measurement (e.g., meters, feet, degrees) for an accurate distance calculation and conversion
# 2- If the coordinate system is geographic (latitude and longitude degrees) then calculate bearing (great circle) distance
#
######################################################################
def countObservationsWithinDistance(fcPoint, distance, distanceUnit, geodatabase = "assignment2.gdb"):

    arcpy.env.overwriteOutput = True

    if arcpy.Exists(geodatabase): # check for valid workspace
        arcpy.env.workspace = geodatabase # sets workspace

    else:
        print("Invalid Workspace")
        sys.exit(1)

    try: # try section where input attribute is described and if statement that checks if inputs are in the valid format
        point_input = arcpy.Describe(fcPoint)
        if point_input.shapeType != "Point":
            print("Input shape type is invalid")
            sys.exit(1)
            
        # new attributes set for use with spatial reference parameters for each input variable for comparisons, also a new projection variable    
        spatial_ref_point = arcpy.Describe(fcPoint).spatialReference

        # run if statement to determine if the linear unit name of the spatial reference matches the given distance unit
        if spatial_ref_point.linearUnitName == distanceUnit:
            print("Units of input feature class and input unit are the same")
            
        # Add field to polygon feature class for Point Count variable         
        arcpy.AddField_management(fcPoint, "Point_Count", "DOUBLE")
        
        # Run generate near table to obtain the distances between points of the point feature class using the given distance
        arcpy.analysis.GenerateNearTable(fcPoint, fcPoint, "Dist_table", distance, "LOCATION", "", "ALL")
        
        # Create a new dictionary that will store values for use in cursors
        dict = {}
        # Set count to 0 so that it can be incremented in cursor
        count = 0
        # Run cursor to search through the distance table to fill dictionary and Point Count values
        with arcpy.da.SearchCursor("Dist_Table",["OBJECTID", "Point_Count"]) as search_cur:
            for search_row in search_cur:
                    dict[search_row[0]] = search_row[1]
                    count +=1 

        # Run cursor to update new Point Count field with values from distance table, search cursor, dictionary        
        with arcpy.da.UpdateCursor(fcPoint,["OBJECTID", "Point_Count"]) as upd_cur:
            for upd_row in upd_cur:
                if upd_row[0] in dict.keys():
                        upd_row[1] = dict[upd_row[0]]
                else:
                    upd_row[1] = [0]
                upd_cur.updateRow(upd_row)

        # If statement to determine if spatial reference type of point feature class is Geographic
        # If this is true, then the bearing distance to line tool will be run to calculate the bearing distance 
        Bearing_Distance = "Bearing_Dist"
        if spatial_ref_point.type == "Geographic":
            arcpy.management.BearingDistanceToLine("Dist_Table", "Bearing_Dist", "FROM_X", "FROM_Y", "NEAR_DIST", distanceUnit, "NEAR_ANGLE", "", "GREAT_CIRCLE")
            print("{} Bearing Distance is:.".format(Bearing_Distance))
        else:
            print("Coodinate System is not Geographic")

    except Exception:
        e = sys.exc_info() [1]
        print(e.args[0])
            

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
    print('### Otherwise, the Autograder will assign 0 points.')
