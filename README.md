# Satellite-Image-Retrieval
## Problem: 
Use Bing maps tile system to automatically download aerial imagery (maximum resolution available) given a lat/lon bounding box. Reference the link at the bottom for quad key calculation and code. An example tile: http://h0.ortho.tiles.virtualearth.net/tiles/h023131022213211200.jpeg?g=131

-**Input:** lat1, lon1, lat2, lon2

-**Output:** an aerial imagery within the bounding box defined above


## Run Instructions


Simply open a Terminal at the project directory, run, for example:

    # Example for IIT Campus
    python3 main.py 41.839341 -87.629504 41.831092 -87.623239
	
or

    # Example for Chicago Loop
    $ python3 main.py 41.888438 -87.644858 41.848298 -87.614988

The output desired image is then saved as 'result.jpg', one at a time.

Note:
    The four parameters represents lat1, lon1, lat2, lon2, respectively.


## Required Environment

Python 3.6

Pillow (PIL Fork) 5.1.x

Note:

1. Installation of PIL:  

		$ pip install Pillow
	
2. Make sure the 'null.jpeg' file is in the current running directory.



## Project files
	main.py

	TileSystem.py

	null.jpeg


## Algorithm Introduction

1. Determine the lowest acceptable level by all bounding box area within one tile.

2. Determine the final best level by filtering out from fine to coarse iteratively.

3. Query each tile image and paste.

      1) Convert lat/lon to pixel coordinates.
	
      2) Convert pixel coordinates to tile coordinates.
	
      3) Query tile image from Bing Server.
	
4. Refine and crop the generated image by pixel granularity.



## Reference

https://msdn.microsoft.com/en-us/library/bb259689.aspx



