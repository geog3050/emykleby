# Eric Mykleby
# Quiz 6
# GEOG:5505
# Dr. Koylu

import arcpy

# set workspace for correct environment
arcpy.env.workspace = r"C:\Users\emykl\OneDrive\Documents\GEOG-5055\airports"

# Add buffer field to airport shapefile table for later input
arcpy.management.AddField('airports.shp',"BUFFER_DIS","integer")

#Set variables for cursor use
in_fc = 'airports.shp'
fields = ["FEATURE","BUFFER_DIS"]

# Create update cursor for feature class 
with arcpy.da.UpdateCursor(in_fc, fields) as cursor:
    # For each row, evaluate the FEATURE value (index position 
    # of 0), and update BUFFER_DIS (index position of 1)
    for row in cursor:
        if row[0] == "Airport":
            row[1] = 15000
        elif row[0] == "Seaplane Base":
            row[1] = 7500
    # Update the cursor with the updated list
        cursor.updateRow(row)

# Run buffer analysis for final buffer zone implementation
arcpy.Buffer_analysis(in_fc, r"C:\Users\emykl\OneDrive\Documents\GEOG-5055\airports\buffer_airports2.shp", "BUFFER_DIS")
