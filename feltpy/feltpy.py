# FeltPy: a wrapper for the public API from Felt.com

# Importing other useful packages
import requests 
import re 
import os
import geopandas 

### INTERNAL ###
# These functions and variables are not meant for external use
# They simply help other functions perform their job

# Saving the URL of a felt request, with flexibility for the endpoint
_felt_api = "https://felt.com/api/v1/{endpoint}"

# Purpose: format the header for any request that should be sent out
# pat: the user's personal access token
# Returns a formatted dictionary with Content-Type and Authorization headers
def _requestHeaders(pat):
    # Creating the dictionary
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {pat}"
    }
    # Returning what was created
    return headers

# Purpose: format and send a GET request to the specified endpoint
# pat: the user's personal access token
# endpoint: the desired action's endpoint
# Will return either a JSON (if the action was successful) or print out the relevant Felt error message
def _getRequest(pat, endpoint):
    # Getting headers
    headers = _requestHeaders(pat)
    # Querying the endpoint
    response = requests.get(_felt_api.format(endpoint=endpoint), headers=headers)
    # Checking the response
    # If it is a 200, then the information was successfully retrieved
    if response.status_code == 200:
        return response.json()
    elif response.status_code in range(400,500):
        _process_error(response.json())
    else:
        print("Unexpected error occured:", response.status_code)
        print(response.text)

# Purpose: format and send a POST request to the specified endpoint
# pat: the user's personal access token
# endpoint: the desired action's endpoint
# data: dict of parameters to pass too
# Will return either a JSON (if the action was successful) or print out the relevant Felt error message
def _postRequest(pat, endpoint, data):
    # Getting headers
    headers = _requestHeaders(pat)
    # Querying the endpoint
    response = requests.post(_felt_api.format(endpoint=endpoint), headers=headers, json=data)
    # Checking the response
    # If it is a 200, then the information was successfully retrieved
    if response.status_code == 200:
        return response.json()
    # If it is a 204, then the upload was successfl
    elif response.status_code == 204:
        print("File upload successful")
    elif response.status_code in range(400,500):
        _process_error(response.json())
    else:
        print("Unexpected error occured:", response.status_code)
        print(response.text)

# Purpose: format and send a PATCH request to the specified endpoint
# pat: the user's personal access token
# endpoint: the desired action's endpoint
# data: dict of parameters to pass too
# Will return either a JSON (if the action was successful) or print out the relevant Felt error message
def _patchRequest(pat, endpoint, data):
    # Getting headers
    headers = _requestHeaders(pat)
    # Querying the endpoint
    response = requests.patch(_felt_api.format(endpoint=endpoint), headers=headers, json=data)
    # Checking the response
    # If it is a 200, then the information was successfully retrieved
    if response.status_code == 200:
        return response.json()
    elif response.status_code in range(400,500):
        _process_error(response.json())
    else:
        print("Unexpected error occured:", response.status_code)
        print(response.text)

# Purpose: format and send a DELETE request to the specified endpoint
# pat: the user's personal access token
# endpoint: the desired action's endpoint
# Will return either a JSON (if the action was successful) or print out the relevant Felt error message
def _deleteRequest(pat, endpoint):
    # Getting headers
    headers = _requestHeaders(pat)
    # Querying the endpoint
    response = requests.delete(_felt_api.format(endpoint=endpoint), headers=headers)

# Purpose: take in an JSON response error that was returned by a request, format, and print it
# error: the json response
# Will not return anything, but will print out messages detailing the error
def _process_error(error):
    # A JSON response is expected to be a list of errors
    dict_error_response = {
        "title":"Felt Error:",
        "code":"Error Code:",
        "source":"Error Source:",
        "detail":"Details:"
    }
    for e in error["errors"]:
        for k,v in dict_error_response.items():
            try:
                print(v, e[k])
            except:
                pass

### GET REQUESTS ###
# All functions that require a GET request to perform

# Purpose: return information about the current user
# pat: the user's personal access token
# Returns a User class
def getUserInfo(pat):
    # Setting the endpoint
    endpoint = "user/"
    # Retrieving the response
    user_info = _getRequest(pat, endpoint)
    # Only proceeding if something was actually returned
    if user_info:
        # Creating the class to store the information
        user = User(type = user_info["data"]["type"],
                    id = user_info["data"]["id"],
                    name = user_info["data"]["attributes"]["name"],
                    email = user_info["data"]["attributes"]["email"])
        # Returning the User
        return user

# Purpose: return information about a map
# pat: the user's personal access token
# map_id: the ID of the map
# Returns a Map class
def getMapInfo(pat, map_id):
    # Setting the endpoint
    endpoint = f"maps/{map_id}"
    # Retrieving the response
    map_info = _getRequest(pat, endpoint)
    # Only proceeding if something was actually returned
    if map_info:
        # Creating the class to store the information
        map = Map(type = map_info["data"]["type"],
                  id = map_info["data"]["id"],
                  title = map_info["data"]["attributes"]["title"],
                  url = map_info["data"]["attributes"]["url"])
        # Returning the Map
        return map

# Purpose: retrieves the feature collection of all the elements in a map
# NOTE: this does NOT mean the data that powers layers - this refers to drawings, text, notes, etc.
# pat: the user's personal access token
# map_id: the ID of the map
# Returns a Geopandas GeoDataFrame of all the elements
def getMapElements(pat, map_id):
    # Setting the endpoint
    endpoint = f"maps/{map_id}/elements"
    # Retrieving the response
    map_elements = _getRequest(pat, endpoint)
    # Only proceeding if something was actually returned
    if map_elements:
        gdf_elements = geopandas.GeoDataFrame.from_features(map_elements["data"])
        return gdf_elements

# Purpose: retrieves all of the comments in a map
# pat: the user's personal access token
# map_id: the ID of the map
# Returns a JSON of all the elements
# TODO: Would be nice to return this as a structured format, maybe a dataframe?
# TODO: Is possible to specify this as a JSON or a CSV
def getMapComments(pat, map_id):
    # Setting the endpoint
    endpoint = f"maps/{map_id}/comments/export"
    # Retrieving the response
    map_comments = _getRequest(pat, endpoint)
    # Only proceeding if something was actually returned
    if map_comments:
        return map_comments

# Purpose: retrieves all of the layers of a map
# NOTE: Only retrieves metadata, not actual data
# pat: the user's personal access token
# map_id: the ID of the map
# Returns a LayerCollection of all the elements
def getLayers(pat, map_id):
    # Setting the endpoint
    endpoint = f"maps/{map_id}/layers"
    # Retrieving the response
    map_layers = _getRequest(pat, endpoint)
    # Only proceeding if something was actually returned
    if map_layers:
        # Creating the class to store the information
        lc = LayerCollection(map_id = map_id,
                             layers = map_layers)
        return lc

# Purpose: retrieves the information for a single layer
# NOTE: Only retrieves metadata, not actual data
# pat: the user's personal access token
# map_id: the ID of the map
# layer_id: the ID of the layer
# Returns a Layer
def getLayer(pat, map_id, layer_id):
    # Setting the endpoint
    endpoint = f"maps/{map_id}/layers/{layer_id}"
    # Retrieving the response
    map_layer = _getRequest(pat, endpoint)
    # Only proceeding if something was actually returned
    if map_layer:
        # Creating the class to store the information
        layer = Layer(type = map_layer["data"]["type"],
                      id = map_layer["data"]["id"],
                      name = map_layer["data"]["attributes"]["name"],
                      status = map_layer["data"]["attributes"]["status"],
                      map_id = map_id,
                      datasets = map_layer["data"]["relationships"]["datasets"])
        return layer

### POST REQUESTS ###
# All functions that require a POST request to perform

# Purpose: make a new blank map
# pat: the user's personal access token
# title: Name of the map - if blank, will be "Untitled Map"
# basemap: Basemap of map - can be "default", "satellite", tile URL, or hex color string (#FF0000)
# layer_urls: list of URLs to load in map - only raster layer tile URLs supported as of 2023-07-28
# lat: latitude to center the map on
# lon: longitude to center the map on
# zoom: zoom level for the map to start at
# Returns a Map object if the map was successfully created
def postMap(pat, title: str=None, basemap: str="default", layer_urls: list=[], lat: float=0.0, lon: float=0.0, zoom: float=10.0):
    # Setting the endpoint
    endpoint = f"maps/"
    # Setting up the parameter dictionary 
    data = {
        "title": title,
        "basemap": basemap,
        "layer_urls": layer_urls,
        "lat": lat,
        "lon": lon,
        "zoom": zoom
    }
    # Retrieving the response
    map_info = _postRequest(pat, endpoint, data)
    # Only proceeding if something was actually returned
    if map_info:
        # Creating the class to store the information
        map = Map(type = map_info["data"]["type"],
                  id = map_info["data"]["id"],
                  title = map_info["data"]["attributes"]["title"],
                  url = map_info["data"]["attributes"]["url"])
        # Returning the Map
        return map

# Purpose: to upload a layer to S3
# NOTE: Will automatically call _processLayer to add it the map unless process is set to False
# pat: the user's personal access token
# map_id: the ID of the map
# file: either a string path or a Geopandas GeoDataFrame to upload
# NOTE: All GeoDataFrames will be re-projected to CRS 4326!
# name: what to name the layer
# process: whether or not to call _processLayer, which finishes uploading the data to the Map (instead of just the cloud)
# verbose: whether or not you want messages printed about the upload being successful or not
# Doesn't return anything
# TODO: Have this work with a list of files as well, that all get uploaded to the same layer
# TODO: Implement verbose
def postLayer(pat, map_id, file: str|geopandas.GeoDataFrame, name: str, process: bool=True, verbose: bool=True):
    # If file is a string, check that it corresponds to a file
    if type(file) == str:
        if os.path.exists(file):
            # Grabbing the name of the file, which is necessary for uploading
            file_name = os.path.basename(file)
        else:
            print("File does not exist - check path and retry")
            return None 
    # If a file is a GeoDataFrame, create a dummy name for it
    elif type(file) == geopandas.GeoDataFrame:
        file_name = re.sub("[^\w]", "_", "gdf_"+name)
    
    # Setting the endpoint
    endpoint = f"maps/{map_id}/layers"
    # Structuring the data for the response
    data = {
        "file_names": [file_name],
        "name": name
    }
    # First, doing a POST request to receive information on which bucket to upload the data to
    upload_request = _postRequest(pat, endpoint, data)
    # Then, doing a separate POST request to upload the data
    # This one isn't done with _postRequest since it doesn't go through the Felt API
    presigned_attributes = upload_request["data"]["attributes"]["presigned_attributes"]
    upload_url = upload_request["data"]["attributes"]["url"]
    layer_id = upload_request["data"]["attributes"]["layer_id"]
    # If the file is a string path, need to process as a file object
    if type(file) == str:
        with open(file, "rb") as file_obj:
            upload_action = requests.post(upload_url, files={**presigned_attributes, "file": file_obj})
    # If the file is a GeoDataFrame, need to get the JSON representation of it, and upload that
    elif type(file) == geopandas.GeoDataFrame:
        upload_action = requests.post(upload_url, files={**presigned_attributes, "file": file.to_crs(4326).to_json()})
    
    # Checking that the upload was successful
    if upload_action.status_code != 204:
        print("Layer upload not successful! Check the following message and try again")
        print(upload_action.text)
    else:
        if process == True:
            endpoint_upload = f"maps/{map_id}/layers/{layer_id}/finish_upload"
            data_upload = {"filename": file_name}
            upload_response = _postRequest(pat, endpoint_upload, data_upload)
            # upload_response is a dictionary - if successfull, the "data" key is set to None
            if not upload_response["data"]:
                print("Processing started, check back later to see if it is complete")
            else:
                print("Processing failed")
                print(upload_response)

# Purpose: to upload a layer hosted elsewhere on the internet
# pat: the user's personal access token
# map_id: the ID of the map
# url: the URL that points to the content to upload
# name: what to name the layer
# Returns a Layer
def postWebLayer(pat, map_id, url: str, name: str="Untitled Layer"):
    # Setting the endpoint
    endpoint = f"maps/{map_id}/layers/url_import"
    # Setting up the parameter dictionary 
    data = {"layer_url": url, "name": name}
    # Retrieving the response
    layer_upload = _postRequest(pat, endpoint, data)
    if layer_upload:
        uploaded_layer = Layer(type = layer_upload["data"]["type"], 
                            id = layer_upload["data"]["id"], 
                            name = name, 
                            status = None, 
                            map_id = map_id, 
                            datasets = None)
        return uploaded_layer

### PATCH REQUESTS ###
# All functions that require a PATCH request to perform

# Purpose: Updates the details of a layer
# pat: the user's personal access token
# map_id: the ID of the map
# layer_id: the ID of the layer
# name: the name you want to update the layer
# description: the description you want to update for the layer (shows in the layer's "Info" tab)
# visible: Whether or not the layer is visible (True/False)
# Returns a Layer
def patchLayer(pat, map_id, layer_id, name: str=None, description: str=None, visible: bool=None):
    # Setting the endpoint
    endpoint = f"maps/{map_id}/layers/{layer_id}"
    # Setting up the parameter dictionary 
    data = {}
    for k,v in zip(["name","description","visible"], [name, description, visible]):
        if v:
            data[k] = v
    # Retrieving the response (note: no actual response)
    patch_layer = _patchRequest(pat, endpoint, data)
    # Only proceeding if something was actually returned
    if patch_layer:
        # Creating the class to store the information
        layer = Layer(type = patch_layer["data"]["type"],
                      id = patch_layer["data"]["id"],
                      name = patch_layer["data"]["attributes"]["name"],
                      status = patch_layer["data"]["attributes"]["status"],
                      map_id = map_id,
                      datasets = patch_layer["data"]["relationships"]["datasets"])
        return layer

### DELETE REQUESTS ###
# All functions that require a DELETE request to perform

# Purpose: Deletes a map
# pat: the user's personal access token
# map_id: the ID of the map
# Does not return anyting
# TODO: Write code to confirm the map is deleted by re-querying for the map using the ID
def deleteMap(pat, map_id):
    # Setting the endpoint
    endpoint = f"maps/{map_id}"
    # Retrieving the response (note: no actual response)
    delete_request = _deleteRequest(pat, endpoint)

# Purpose: Deletes a layer within a map
# pat: the user's personal access token
# map_id: the ID of the map
# layer_id: the ID of the layer
# Does not return anyting
# TODO: Write code to confirm the layer is deleted by re-querying for the layer using the ID
def deleteLayer(pat, map_id, layer_id):
    # Setting the endpoint
    endpoint = f"maps/{map_id}/layers/{layer_id}"
    # Retrieving the response (note: no actual response)
    delete_request = _deleteRequest(pat, endpoint)

### CLASSES ###
# Objects that contain attributes    

# Class type for Users, which are people who edit or read maps
# Has attributes for type, id, name, and email
class User:
    # Info is created on initialization
    def __init__(self, type, id, name, email):
        self.type = type
        self.id = id 
        self.name = name 
        self.email = email

# Class type for Maps
# Has attributes for type, id, title, and url
# Has methods to call all map-based functions
class Map:
    # Info is created on initialization
    def __init__(self, type, id, title, url):
        self.type = type
        self.id = id 
        self.title = title
        self.url = url
    # Methods to perform map-based actions (get info, delete)
    def getMapElements(self, pat):
        getMapElements(pat, self.id)
    def getMapComments(self, pat):
        getMapComments(pat, self.id)
    def getMapLayers(self, pat):
        getLayers(pat, self.id)
    def deleteMap(self, pat):
        deleteMap(pat, self.id)

# Class type for LayerCollection (all layers within a single map)
# Has attributes for map_id, names, layer_ids, types
# Also has a method for printing out all the layer information in a digestible manner
class LayerCollection:
    # Info is created on initialization
    def __init__(self, map_id, layers):
        self.map_id = map_id
        self.layer_names = []
        self.layer_ids = []
        self.layer_types = []
        self._layers = [self._make_layer(l) for l in layers["data"]]
    # Function to parse a JSON object per-Layer information, and create the Layer class
    def _make_layer(self, layer_json):
        # Making the layer
        layer =  Layer(type = layer_json["type"],
                       id = layer_json["id"],
                       name = layer_json["attributes"]["name"],
                       status = layer_json["attributes"]["status"],
                       map_id = self.map_id,
                       datasets = layer_json["relationships"]["datasets"])
        # Appending the info to each attribute
        self.layer_names.append(layer.name)
        self.layer_ids.append(layer.id)
        self.layer_types.append(layer.type)
        # Finally, returning the actual layer, to be added to the list
        return layer
    # Method for pretty-printing the layers
    def listLayers(self):
        for i, n in zip(self.layer_ids, self.layer_names):
            print(i, n)
    # Methods for returning a specific layer
    # Using square brackets, like LayerCollection[0]:
    def __getitem__(self, index):
        return self._layers[index]
    # Using the ID of the layer
    def getLayer(self, id):
        for i, l in zip(self.layer_ids, self._layers):
            if i == id:
                return l 
            else:
                pass

# Class type for Layers (created when data is uploaded to a map)
# Has attributes for type, id, name, status, and datasets
# Also has a method for printing out all the layer information in a digestible manner
# And has methods to call all layer-based functions
# TODO: Should map_id be stored here?
class Layer:
    # Info is created on initialization
    def __init__(self, type, id, name, status, map_id, datasets):
        self.type = type 
        self.id = id 
        self.name = name 
        self.status = status
        self.map_id = map_id
        self.dataset_names = []
        self.dataset_ids = []
        self.dataset_types = []
        if datasets:
            self._datasets = [self._make_dataset(d) for d in datasets["data"]]
        else:
            self._datasets = []
    # Function to parse a JSON object per-Dataset information, and create the Dataset class
    def _make_dataset(self, dataset_json):
        # Making the dataset
        dataset =  Dataset(type = dataset_json["type"],
                           id = dataset_json["id"],
                           name = dataset_json["attributes"]["name"])
        # Appending the info to each attribute
        self.dataset_names.append(dataset.name)
        self.dataset_ids.append(dataset.id)
        self.dataset_types.append(dataset.type)
        # Finally, returning the actual dataset, to be added to the list
        return dataset
    # Method for pretty-printing the datasets
    def listDatasets(self):
        for i, n in zip(self.dataset_ids, self.dataset_names):
            print(i, n)
    # Methods for returning a specific layer
    # Using square brackets, like LayerCollection[0]:
    def __getitem__(self, index):
        return self._datasets[index]
    # Using the ID of the layer
    def getDataset(self, id):
        for i, l in zip(self.dataset_ids, self._datasets):
            if i == id:
                return l 
            else:
                pass
    
    # Methods to perform Layer actions (patch, delete)
    def patchLayer(self, pat, name: str=None, description: str=None, visible: str=None):
        patchLayer(pat, self.map_id, self.id, name, description, visible)
    def deleteLayer(self, pat):
        deleteLayer(pat, self.map_id, self.id)

# Class type for Datasets (created when data is uploaded to a map)
# Has attributes for type, id, and name
# TODO: Add layer_id?
class Dataset:
    # Info is created on initialization
    def __init__(self, type, id, name):
        self.type = type
        self.id = id
        self.name = name