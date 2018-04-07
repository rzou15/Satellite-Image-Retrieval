import math


EarthRadius = 6378137
MinLat = -85.05112878
MaxLat = 85.05112878
MinLong = -180
MaxLong = 180


def clip(n, minval, maxval):
	"""
		Clip a number to the specified min and max values.
	Input:
		n 			the number to clip
		minval		minimum allowable value
		maxval		maximum allowable value
	Return:
		The clipped value
	"""		
	return min(max(n, minval), maxval)



def mapSize(level):
	"""
		Determine the map width and height (in pixels) at a specified level of detail.
	Input:
		level		level of detail from 1 (lowest detail) to 23 (highest detail)
	Return:
		The map width and height in pixels
	"""
	return 256 << level



def groundResolution(latitude, level):
	"""
		Determine the ground resolution (in meters per pixel) at a specified latitude and level of detail.
	Input:
		latitude 		latitude (in degrees) at which to measure the map scale
		level 		 	level of detail from 1 (lowest detail) to 23 (highest detail)
	Return:
		The ground resolution, in meters per pixel
	"""
	latitude = clip(latitude, MinLat, MaxLat)
	return math.cos(latitude*math.pi / 180) * 2 * math.pi * EarthRadius / mapSize(level)



def mapScale(latitude, level, dpi):
	"""
		Determine the map scale at a specified latitude, level of detail, and screen resolution.
	Input:
		latitude 		latitude (in degrees) at which to measure the map scale
		level			level of detail from 1 (lowest detail) to 23 (highest detail)
		dpi 		 	Resolution of the screen, in dots per inch
	Return:
		The map scale, expressed as the denominator N of the ratio 1 : N
	"""
	return groundResolution(latitude, level) * dpi/0.0254 



def latLongToPixelXY(latitude, longitude, level):
	"""
		Convert a point from latitude/longitutde WGS-84 coordinates (in degrees) into pixel XY coordinates at a specified level of detail.
	Input:
		latitude 		latitude of the point, in degrees.
		longitude		longitutde of the point, in degrees.
		level 			level of detail from 1 (lowest detail) to 23 (highest detail)
	Return:
		pixelX 			X coordinate in pixels
		pixelY  	 	Y coordinate in pixels
	"""
	latitude = clip(latitude, MinLat, MaxLat)
	longitude = clip(longitude, MinLong, MaxLong)

	x = (longitude + 180) / 360
	sinLatitude = math.sin(latitude * math.pi / 180)
	y = 0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi)

	mapsize = mapSize(level)
	pixelX = int(clip(x * mapsize + 0.5, 0, mapsize - 1))
	pixelY = int(clip(y * mapsize + 0.5, 0, mapsize - 1))

	return pixelX, pixelY



def pixelXYToTileXY(pixelX, pixelY):
	"""
		Convert pixel XY coordinates into tile XY coordinates of the tile containing the specified pixel.
	Input:
		pixelX 		X coordinate of the point, in pixels
		pixelY 		Y coordinate of the point, in pixels
	Return: 
		tileX 		X coordinate of the point, in tiles
		tileY 		Y coordinate of the point, in tiles
	"""
	tileX = int(pixelX / 256)
	tileY = int(pixelY / 256)
	return tileX, tileY



def tileXYToQuadKey(tileX, tileY, level):
	"""
		Convert tile XY coordinates into a QuadKey at a specified level of detail.
	Input:
		tileX 		Tile X coordinate
		tileY 		Tile Y coordinate
		level 		Level of detail, from 1 (lowest detail) to 23 (highest detail)
	Return:
		quadkey 	A string containing the QuadKey
	"""
	quadkey = ""
	for i in range(level, 0, -1):
		digit = '0'
		mask = 1 << (i-1)
		if ((tileX & mask) != 0):
			digit = chr(ord(digit) + 1)
		if ((tileY & mask) != 0):
			digit = chr(ord(digit) + 1)
			digit = chr(ord(digit) + 1)
		quadkey += digit

	return quadkey



def latLongToTileXY(latitude, longitude, level):
	"""
		Convert a point from latitude/longitutde (in degrees) into tile XY coordinates at a specified level of detail.
	Input:
		latitude 		latitude of the point, in degrees.
		longitude		longitutde of the point, in degrees.
		level 			level of detail from 1 (lowest detail) to 23 (highest detail)
	Return:
		tileX 			X coordinate in tiles
		tileY  	 		Y coordinate in tiles
	"""
	pixelX, pixelY = latLongToPixelXY(latitude, longitude, level)
	tileX, tileY = pixelXYToTileXY(pixelX, pixelY)
	
	return tileX, tileY



