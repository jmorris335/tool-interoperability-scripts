'''
client
======

Convenience functions for working with the Onshape API
'''

from onshape_api.onshape import Onshape

import mimetypes
import random
import string
import os
import json


class DocumentIDs():
    '''
    Structured acccess to document ids.

    Attributes:
        - name (str, default=None): Document name
        - did (str, default=None): Document id
        - wvm (str, default=None): Workspace, version, or microversion tag
        - wvmid (str, default=None): id corresponding to `wvm`
        - eid (str, default=None): Element id
        - file_path (str, default=None): file path of JSON file to read
        - raw (str, default=None): JSON file data to parse
    '''
    def __init__(self, name: str=None, did: str=None, wvm: str=None, 
                 wvmid: str=None, eid: str=None, **kwargs):
        self.name = name
        self.did = did
        self.wvm = wvm
        self.wvmid = wvmid
        self.eid = eid
        if "file_path" in kwargs:
            self.fromJson(kwargs["file_path"])
        if "raw" in kwargs:
            self.fromJson(kwargs["raw"])

    def fromJson(self, file_path: str=None, raw: str=None):
        '''
        Sets class parameters from JSON file.
        '''
        if file_path is not None:
            with open('API.json', 'r') as file:
                ids = json.load(file)
        elif raw is not None:
            ids = json.load(raw)
        else:
            raise Exception("JSON data not passed to function.")
        for key, val in ids.items():
            setattr(self, key, val)
        

class Client():
    '''
    Defines methods for testing the Onshape API. Comes with several methods:

    - Create a document
    - Delete a document
    - Get a list of documents

    Attributes:
        - stack (str, default='https://cad.onshape.com'): Base URL
        - logging (bool, default=True): Turn logging on or off
    '''

    def __init__(self, stack='https://cad.onshape.com', creds: str='./cred.json', logging=False):
        '''
        Instantiates a new Onshape client.

        Args:
            - stack (str, default='https://cad.onshape.com'): Base URL
            - logging (bool, default=True): Turn logging on or off
        '''

        self._stack = stack
        self._api = Onshape(stack=stack, creds=creds, logging=logging)

    def new_document(self, name='Test Document', owner_type=0, public=False):
        '''
        Create a new document.

        Args:
            - name (str, default='Test Document'): The doc name
            - owner_type (int, default=0): 0 for user, 1 for company, 2 for team
            - public (bool, default=False): Whether or not to make doc public

        Returns:
            - requests.Response: Onshape response data
        '''

        payload = {
            'name': name,
            'ownerType': owner_type,
            'isPublic': public
        }

        return self._api.request('post', '/api/documents', body=payload)

    def rename_document(self, did, name):
        '''
        Renames the specified document.

        Args:
            - did (str): Document ID
            - name (str): New document name

        Returns:
            - requests.Response: Onshape response data
        '''

        payload = {
            'name': name
        }

        return self._api.request('post', '/api/documents/' + did, body=payload)

    def del_document(self, did):
        '''
        Delete the specified document.

        Args:
            - did (str): Document ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('delete', '/api/documents/' + did)

    def get_document(self, did):
        '''
        Get details for a specified document.

        Args:
            - did (str): Document ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('get', '/api/documents/' + did)

    def list_documents(self):
        '''
        Get list of documents for current user.

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('get', '/api/documents')

    def create_assembly(self, did, wid, name='My Assembly'):
        '''
        Creates a new assembly element in the specified document / workspace.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - name (str, default='My Assembly')

        Returns:
            - requests.Response: Onshape response data
        '''

        payload = {
            'name': name
        }

        return self._api.request('post', '/api/assemblies/d/' + did + '/w/' + wid, body=payload)

    def get_features(self, did, wid, eid):
        '''
        Gets the feature list for specified document / workspace / part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('get', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/features')

    def get_partstudio_tessellatededges(self, did, wid, eid):
        '''
        Gets the tessellation of the edges of all parts in a part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('get', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/tessellatededges')

    def upload_blob(self, did, wid, filepath='./blob.json'):
        '''
        Uploads a file to a new blob element in the specified doc.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - filepath (str, default='./blob.json'): Blob element location

        Returns:
            - requests.Response: Onshape response data
        '''

        chars = string.ascii_letters + string.digits
        boundary_key = ''.join(random.choice(chars) for i in range(8))

        mimetype = mimetypes.guess_type(filepath)[0]
        encoded_filename = os.path.basename(filepath)
        file_content_length = str(os.path.getsize(filepath))
        blob = open(filepath)

        req_headers = {
            'Content-Type': 'multipart/form-data; boundary="%s"' % boundary_key
        }

        # build request body
        payload = '--' + boundary_key + '\r\nContent-Disposition: form-data; name="encodedFilename"\r\n\r\n' + encoded_filename + '\r\n'
        payload += '--' + boundary_key + '\r\nContent-Disposition: form-data; name="fileContentLength"\r\n\r\n' + file_content_length + '\r\n'
        payload += '--' + boundary_key + '\r\nContent-Disposition: form-data; name="file"; filename="' + encoded_filename + '"\r\n'
        payload += 'Content-Type: ' + mimetype + '\r\n\r\n'
        payload += blob.read()
        payload += '\r\n--' + boundary_key + '--'

        return self._api.request('post', '/api/blobelements/d/' + did + '/w/' + wid, headers=req_headers, body=payload)

    def part_studio_stl(self, did, wid, eid):
        '''
        Exports STL export from a part studio

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        '''

        req_headers = {
            'Accept': 'application/vnd.onshape.v1+octet-stream'
        }
        return self._api.request('get', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/stl', headers=req_headers)

    def execute_feature_script(self, did, wid, eid, feature_script: str=None, file_path: str=None):
        '''
        Executes the feature script.
        
        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID
            - feature_script (str, default=None): text of feature script
            - file_path (str, default=None): file path for feature script text

        Returns:
            - requests.Response: Onshape response data
        '''
        if file_path is not None:
            with open(file_path, 'r', encoding='utf-8') as file:
                feature_script = file.read()

        payload = {
            'script': feature_script
        }

        api_url = f"/api/partstudios/d/{did}/w/{wid}/e/{eid}/featurescript"
        return self._api.request('post', api_url, body=payload)
    
    def add_feature(self, did, wid, eid, body: str=None, file_path: str=None):
        '''
        Executes the feature script.
        
        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID
            - body (str, default=None): text of body (JSON format)
            - file_path (str, default=None): file path for body text

        Returns:
            - requests.Response: Onshape response data
        '''
        if file_path is not None:
            with open(file_path, 'r', encoding='utf-8') as file:
                body = file.read()

        api_url = f"/api/v9/partstudios/d/{did}/w/{wid}/e/{eid}/features"
        return self._api.request('post', api_url, body=body)
    
    def delete_feature(self, did, wid, eid, feature_id):
        '''
        Deletes the feature with the given feature Id.
        
        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID
            - feature_id (str): ID of feature

        Returns:
            - requests.Response: Onshape response data
        '''
        api_url = f"/api/v9/partstudios/d/{did}/w/{wid}/e/{eid}/features/featureid/{feature_id}"
        return self._api.request('delete', api_url)
    
    def get_mass_properties(self, did, wid, eid, part_id):
        '''
        Gets the mass properties for a part with the given part_id.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID
            - feature_id (str): ID of feature

        Returns:
            - requests.Response: Onshape response data
        '''
        api_url = f"/parts/d/{did}/w/{wid}/e/{eid}/partid/{part_id}/massproperties"
        return self._api.request('get', api_url)