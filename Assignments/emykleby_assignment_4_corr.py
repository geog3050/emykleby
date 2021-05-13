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
arcpy.env.overwriteOutput = True
###################################################################### 
# Problem 1 (20 points)
# 
# Given an input point feature class (e.g., facilities or hospitals) and a polyline feature class, i.e., bike_routes:
# Calculate the distance of each facility to the closest bike route and append the value to a new field.
#        
###################################################################### 
def calculateDistanceFromPointsToPolylines(input_geodatabase, fcPoint, fcPolyline):
    if arcpy.Exists(input_geodatabase): # check for valid workspace
        arcpy.env.workspace = input_geodatabase # sets workspace
        
        # Run near analysis tool between the point feature class and polygon feature class
        arcpy.Near_analysis(fcPoint, fcPolyline,"","","",GEODESIC)
        # This tool automatically creates 2 new fields called NEAR_FID and NEAR_DIST. NEAR_DIST will store the distances of each facility to the closest bike route
        print(arcpy.GetMessages())

    else:
        print("Invalid workspace")

######################################################################
# Problem 2 (30 points)
# 
# Given an input point feature class, i.e., facilities, with a field name (FACILITY) and a value ('NURSING HOME'), and a polygon feature class, i.e., block_groups:
# Count the number of the given type of point features (NURSING HOME) within each polygon and append the counts as a new field in the polygon feature class
#
######################################################################
def countPointsByTypeWithinPolygon(input_geodatabase, fcPoint, pointFieldName, pointFieldValue, fcPolygon):
    if arcpy.Exists(input_geodatabase): # check for valid workspace
        arcpy.env.workspace = input_geodatabase # sets workspace

        # Use SummarizeWithin_analysis tool in order to create a new feature class containing information from point feature class and polygon feature class
        # This tool also creates a new table that includes summary fields for each group of summary features for each input polygon
        arcpy.SummarizeWithin_analysis(fcPolygon, fcPoint, "Point_Poly", "", "", "", "", pointFieldName,'', '', "Count_Table")

        # Add field to polygon feature class for Point Count variable         
        arcpy.AddField_management(fcPolygon, "Point_Count", "DOUBLE")

        # Create a new dictionary that will store values for use in cursors
        dict = {}
        # Set count to 0 so that it can be incremented in cursor
        count = 0
        # Run cursor to search through the summarized table to fill dictionary and Point Count values
        with arcpy.da.SearchCursor("Count_Table",["Join_ID", pointFieldName, "pfv_count"]) as search_cur:
            for search_row in search_cur:
                if search_row[1] == pointFieldValue:
                    dict[search_row[0]] = search_row[2]
                    count +=1 

        # Run cursor to update new Point Count field with values from summary table, search cursor, dictionary        
        with arcpy.da.UpdateCursor(fcPolygon,["FIPS", "pfv_count"]) as upd_cur:
            for upd_row in upd_cur:
                if upd_row[0] in dict.keys():
                        upd_row[1] = dict[upd_row[0]]
                upd_cur.updateRow(upd_row)

        del row
        del cursor

        arcpy.management.CopyFeatures(Point_Poly, fcPolygon)

        arcpy.management.Delete(Point_Poly, Count_Table)
                        
    else:
        print("Invalid workspace")

######################################################################
# Problem 3 (50 points)
# 
# Given a polygon feature class, i.e., block_groups, and a point feature class, i.e., facilities,
# with a field name within point feature class that can distinguish categories of points (i.e., FACILITY);
# count the number of points for every type of point features (NURSING HOME, LIBRARY, HEALTH CENTER, etc.) within each polygon and
# append the counts to a new field with an abbreviation of the feature type (e.g., nursinghome, healthcenter) into the polygon feature class 

# HINT: If you find an easier solution to the problem than the steps below, feel free to implement.
# Below steps are not necessarily explaining all the code parts, but rather a logical workflow for you to get started.
# Therefore, you may have to write more code in between these steps.

# 1- Extract all distinct values of the attribute (e.g., FACILITY) from the point feature class and save it into a list
# 2- Go through the list of values:
#    a) Generate a shortened name for the point type using the value in the list by removing the white spaces and taking the first 13 characters of the values.
#    b) Create a field in polygon feature class using the shortened name of the point type value.
#    c) Perform a spatial join between polygon features and point features using the specific point type value on the attribute (e.g., FACILITY)
#    d) Join the counts back to the original polygon feature class, then calculate the field for the point type with the value of using the join count field.
#    e) Delete uncessary files and the fields that you generated through the process, including the spatial join outputs.  
######################################################################
def countCategoricalPointTypesWithinPolygons(fcPoint, pointFieldName, fcPolygon, workspace):
    if arcpy.Exists(workspace): # check for valid workspace
        arcpy.env.workspace = workspace # sets workspace

        # Use SummarizeWithin_analysis tool in order to create a new feature class containing information from point feature class and polygon feature class
        # This tool also creates a new table that includes summary fields for each group of summary features for each input polygon
        arcpy.SummarizeWithin_analysis(fcPolygon, fcPoint, "Point_Poly", "", "", "", "", pointFieldName,'', '', "Count_Table")

        # Add field to polygon feature class for Point Count variable 
        arcpy.AddField_management(fcPolygon, "Point_Count", "DOUBLE") 

        # Use a set to get the unique names from the pointFieldName variable for use in later cursors
        uniqueNames = set([row[0] for row in arcpy.da.SearchCursor(fcPoint, [pointFieldName])])

        for Name in uniqueNames: # Iterates through each name

            # Create a new dictionary that will store values for use in cursors
            dict = {}
            # Set count to 0 so that it can be incremented in cursor
            count = 0
            # Run cursor to search through the summarized table to fill dictionary and Point Count values with unique names
            with arcpy.da.SearchCursor("Count_Table",["Join_ID", pointFieldName, "Point_Count"]) as search_cur:
                for search_row in search_cur:
                    if search_row[1] == Name:
                        dict[search_row[0]] = search_row[2]
                        count +=1
                        
            # Run cursor to update new Point Count field with values from summary table, search cursor, dictionary          
            with arcpy.da.UpdateCursor(fcPolygon,["FIPS", "Point_Count"]) as upd_cur:
                for upd_row in upd_cur:
                    if upd_row[0] in dict.keys():
                            upd_row[1] = dict[upd_row[0]]
                    upd_cur.updateRow(upd_row)

            del row
            del cursor

            arcpy.management.CopyFeatures(Point_Poly, fcPolygon)

            arcpy.management.Delete(Point_Poly, Count_Table)

    else:
        print("Invalid workspace")

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
