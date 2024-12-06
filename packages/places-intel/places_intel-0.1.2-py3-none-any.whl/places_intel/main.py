from outscraper import ApiClient
import overpy
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

def multiple_place_intel(api_key, place_groups, region, result_amount=20, radius=10):
    """Get intel on multiple top attractions based on a google maps search query. Provides polygon options for each attraction.
        
        Args:
            api_key (string): You Outscraper API key.
            place_groups (string): A type of location (hotels, hospitals, museums, etc).
            region (string): A city, zip code, county or any other gerneral geographical indicator (not addresses).
            result_amount (int) (optional): The number of attraction results the user would like to recieve. Defaults to 10.
            radius (string or int) (optional): The initial radius of the polygon search. Can be "s" (10 meters), "m" (30 meters), "l" (100 meters), or a custom radius amount.
                                               Defaults to 10 meters. Expands by 10 meters until a ccomplete polygon is found.
            
        Returns:
            A tuple comtaining the following:
                final: A list of dictionaries containing the following:
                    [{'place_id': Google Place ID, 'place_name': Place Name, 'place_groups': Place Group, 'query': Search Query Used, 'polygon_id', Individual ID for a polygon, 'possible_polygon': Polygon Coordinates}]
                polygon_list: A list of tuples with the individual attraction name and all of its polygon options to be used to create a KML file.
        """
    sizes = {"xs": 5, "s": 10, "m": 30, "l": 100}
    try:
        if isinstance(radius, str):
            radius = radius.lower()
            if radius in sizes:
                size = sizes[radius]
        elif isinstance(radius, int):
            size = radius
    except:
        return {"Error": "Invalid radius input."}
    query = f"{place_groups} in {region}"
    try:
        client = ApiClient(api_key)
    except Exception as e:
        return {"Error occurred while creating the API client": f"{e}"}
    results = client.google_maps_search(query, limit=result_amount,  language="en",)
    final = []
    polygon_list = []
    for r in results:
        for result in r:
            result_dict = {}
            polygons = _polygons(result['latitude'], result['longitude'], size)
            for polygon in polygons:
                result_dict['place_id'] = result['place_id']
                result_dict['place_name'] = result['name']
                result_dict['place_group'] = place_groups
                result_dict['category'] = result['type']
                result_dict['query'] = query
                result_dict['polygon_id'] = list(polygon.keys())[0]
                result_dict['possible_polygon'] = list(polygon.values())[0]
                final.append(result_dict)
            polygon_list.append((result['name'], polygons))
    return final, polygon_list

def single_place_intel(api_key, place_name, radius=10):
    """Get intel on a single attraction based on a google maps search query. Provides polygon options for the attraction.
        
        Args:
            api_key (string): You Outscraper API key.
            place_name (string): The name, address, or Google Place ID of the location the user would like intel on.
            radius (string or int) (optional): The initial radius of the polygon search. Can be "s" (10 meters), "m" (30 meters), "l" (100 meters), or a custom radius amount.
                                               Defaults to 10 meters. Expands by 10 meters until a ccomplete polygon is found.
            
        Returns:
            final: A list with a nested dictionary containing the following:
                [{'place_id': Google Place ID, 'place_name': Place Name, 'place_groups': Place Group, 'query': Search Query Used, 'polygon_id', Individual ID for a polygon, 'possible_polygon': Polygon Coordinates}]
                polygon_list: A list of tuples with the individual attraction name and all of its polygon options to be used to create a KML file.
        """
    sizes = {"xs": 5, "s": 10, "m": 30, "l": 100}
    try:
        if isinstance(radius, str):
            radius = radius.lower()
            if radius in sizes:
                size = sizes[radius]
        elif isinstance(radius, int):
            size = radius
    except:
        return {"Error": "Invalid radius input."}
    query = f"{place_name}"
    try:
        client = ApiClient(api_key)
    except Exception as e:
        return {"Error occurred while creating the API client": f"{e}"}
    results = client.google_maps_search(query, limit=1,  language="en",)
    final = []
    result_dict = {}
    polygon_list = []
    for r in results:
        for result in r:
            polygons = _polygons(result['latitude'], result['longitude'], size)
            for polygon in polygons:
                result_dict['place_id'] = result['place_id']
                result_dict['place_name'] = result['name']
                result_dict['place_group'] = 'Individual Search'
                result_dict['category'] = result['type']
                result_dict['query'] = query
                result_dict['polygon_id'] = list(polygon.keys())[0]
                result_dict['possible_polygon'] = list(polygon.values())[0]
                final.append(result_dict)
            polygon_list.append((result['name'], polygons))
    return final, polygon_list


def _polygons(latitude, longitude, size=10):
    """Get polygons on a location based on it's lat/long using overpy to access OpenStreetMap.
        
        Args:
            latitude (int): The latitude of the location.
            longitude (int): The longitude of the location.
            
        Returns:
            results: A list of dictionaries containing the polygons found from the provided lat/long.
        """
        #overpy query
        # Initialize Overpass API
    api = overpy.Overpass()

    # Initial radius and maximum radius
    initial_radius = size  # Starting search radius in meters
    increment = 10        # Increment for each step
    max_radius = 200      # Maximum search radius to prevent infinite loops

    # Function to fetch data with increasing radius
    def fetch_polygons(lat, lon, radius):
        query = f"""
        [out:json];
        (
        way(around:{radius},{lat},{lon});
        relation(around:{radius},{lat},{lon});
        );
        out body;
        >;
        out skel qt;
        """
        return api.query(query)

    radius = initial_radius
    result = None

    # Keep increasing radius until we get results or hit the max radius
    while radius <= max_radius:
        print(f"Trying radius: {radius} meters...")
        try:
            result = fetch_polygons(latitude, longitude, radius)
            if result.ways or result.relations:  # Check if data is retrieved
                print(f"Data found with radius: {radius} meters")
                break
        except overpy.exception.OverpassTooManyRequests:
            print("Too many requests; please try again later.")
            break
        radius += increment

    # If no results found after max radius
    if not result or (not result.ways and not result.relations):
        return "No data found within the maximum radius."
    else:
        final = []
        # Display polygon data
        for way in result.ways:
            lat_long_dict = {}
            lat_long_list = []
            print(f"Polygon for {way.tags.get('name', 'unknown')} (ID: {way.id}):")
            for node in way.nodes:
                print(f"{node.lat}, {node.lon}")
                lat_long_list.append([str(node.lat), str(node.lon)])
            lat_long_dict[str(way.id)] = lat_long_list
            print("\n")
            final.append(lat_long_dict)
        return final


def create_kml(polygon_data, output_file):
    """Creates a KML file from polygon data with subcategories based on names.
    
    Args:
        polygon_data (list[dicts]): A list of tuples, where each tuple contains a name and a list of polygons.
                                    Each polygon is a dictionary with ID as key and coordinates as values.
        output_file (string): The name of the KML file to use for Google My Maps. Can include ".kml" or not.
            
    Returns:
        KML file: a ccustom KML file of all the polygons found in the provided data.
    """
    # Initialize the root KML structure
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, "Document")
    
    # Add default styles
    style_normal = ET.SubElement(document, "Style", id="poly-default-normal")
    line_style = ET.SubElement(style_normal, "LineStyle")
    ET.SubElement(line_style, "color").text = "ff000000"
    ET.SubElement(line_style, "width").text = "1.2"
    poly_style = ET.SubElement(style_normal, "PolyStyle")
    ET.SubElement(poly_style, "color").text = "4c000000"
    ET.SubElement(poly_style, "fill").text = "1"
    ET.SubElement(poly_style, "outline").text = "1"

    style_highlight = ET.SubElement(document, "Style", id="poly-default-highlight")
    line_style_hl = ET.SubElement(style_highlight, "LineStyle")
    ET.SubElement(line_style_hl, "color").text = "ff000000"
    ET.SubElement(line_style_hl, "width").text = "1.8"
    poly_style_hl = ET.SubElement(style_highlight, "PolyStyle")
    ET.SubElement(poly_style_hl, "color").text = "4c000000"
    ET.SubElement(poly_style_hl, "fill").text = "1"
    ET.SubElement(poly_style_hl, "outline").text = "1"

    # Group polygons into folders based on the name
    for name, polygons in polygon_data:
        folder = ET.SubElement(document, "Folder")
        folder_name = ET.SubElement(folder, "name")
        folder_name.text = name

        for polygon in polygons:
            for id, coordinates in polygon.items():
                placemark = ET.SubElement(folder, "Placemark")
                name_elem = ET.SubElement(placemark, "name")
                name_elem.text = id
                
                style_url = ET.SubElement(placemark, "styleUrl")
                style_url.text = "#poly-default-normal"
                
                polygon_elem = ET.SubElement(placemark, "Polygon")
                outer_boundary = ET.SubElement(polygon_elem, "outerBoundaryIs")
                linear_ring = ET.SubElement(outer_boundary, "LinearRing")
                coords_elem = ET.SubElement(linear_ring, "coordinates")
                
                # Format coordinates into a string
                coords_text = " ".join([f"{lon},{lat}" for lat, lon in coordinates])
                coords_elem.text = coords_text

    # Pretty-print the KML
    raw_kml = ET.tostring(kml, encoding="unicode")
    dom = parseString(raw_kml)
    pretty_kml = dom.toprettyxml(indent="  ")

    # Write to file
    if not output_file.lower().endswith(".kml"):
        output_file += ".kml"
    with open(output_file, "w") as kml_file:
        kml_file.write(pretty_kml)

if __name__ == "__main__":
    # result = _polygons(39.1763123, -94.4862721)
    # output_kml_file = "omahazoo.kml"
    # create_kml(result, output_kml_file)
    api_key = 'NTQyYmMyNzc4MGM3NDU4OGE0ZGRjZTc0YTI0MTlmODJ8YjJlMjMzMTEyZg'
    # info, polygons = single_place_intel(api_key, "st. anthony hotel", "s")
    # create_kml(polygons, "st_anthony_hotel.kml")
    info, polygons = multiple_place_intel(api_key, "Restaurants", "San Antonio", 10, "s")
    create_kml(polygons, "San_Antonio_Restaurants")