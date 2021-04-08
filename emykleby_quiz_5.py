# Eric Mykleby
# Quiz 5
# GEOG:5505
# Dr. Koylu

import arcpy


def calculatePercentAreaOfPolygonAInPolygonB(input_geodatabase, fcPolygon1, fcPolygon2):
    if arcpy.Exists(input_geodatabase): # check for valid workspace
        arcpy.env.workspace = input_geodatabase # sets workspace
        
	# establishes input features for use in Intersect tool
        inFeatures = [fcPolygon1, fcPolygon2]
        
	# Run intersect tool to obtain intersection feature class between two input classes
        arcpy.Intersect_analysis(inFeatures, "int_ouput")
        
	# Run spatial join tool to obtain join feature class so that areas can be compared
        arcpy.SpatialJoin_analysis("int_ouput", fcPolygon2, "join_feat")
        
	# Add the field needed to store result of calculation for percentage of area
        arcpy.AddField_management(fcPolygon2, "area_pct", "DOUBLE")
        
	# Calculate the percentage area for the first polygon feature class in the second polygon feature class
        arcpy.CalculateField_management("join_feat", "area_pct", "!Shape_Area!/!Shape_Area_1!", "PYTHON3")
        
	# Run cursor to search through the joined feature class table and update the table for the second polygon
	# feature class with that same area percentage value
        with arcpy.da.SearchCursor("join_feat",["FIPS", "area_pct"]) as search_cur:
            for search_row in search_cur:
                with arcpy.da.UpdateCursor(fcPolygon2,["FIPS", "area_pct"]) as upd_cur:
                    for upd_row in upd_cur:
                        if upd_row[0] == search_cur[0]:
                            upd_row[1] = search_row[1]
                            upd_cur.updateRow(upd_row)
