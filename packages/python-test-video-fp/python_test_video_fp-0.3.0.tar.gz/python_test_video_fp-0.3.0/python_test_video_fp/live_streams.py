from .exceptions import APIError
from .api import make_request

class Livestream:
    def __init__(self, client):
        self.client = client
    
    def create(self, data):
        """Create a live stream."""
        try:
            return make_request(
                method="POST", 
                endpoint="/live/streams", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            raise APIError(f"Failed to create live stream: {str(e)}")
    
    def list(self):
        """Retrieve all live streams."""
        try:
            return make_request(
                method="GET", 
                endpoint="/live/streams", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to retrieve live streams: {str(e)}")
    
    def get(self, stream_id):
        """Retrieve a specific live stream by ID."""
        if not stream_id:
            raise ValueError("Stream ID must be provided.")
        
        try:
            return make_request(
                method="GET", 
                endpoint=f"/live/streams/{stream_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to retrieve live stream: {str(e)}")
    
    def update(self, stream_id, data):
        """Update a specific live stream."""
        if not stream_id:
            raise ValueError("Stream ID must be provided.")
        
        try:
            return make_request(
                method="PATCH", 
                endpoint=f"/live/streams/{stream_id}", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            raise APIError(f"Failed to update live stream: {str(e)}")
    
    def delete(self, stream_id):
        """Delete a specific live stream."""
        if not stream_id:
            raise ValueError("Stream ID must be provided.")
        
        try:
            return make_request(
                method="DELETE", 
                endpoint=f"/live/streams/{stream_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to delete live stream: {str(e)}")
    
    def create_simulcast(self, stream_id, data):
        """Create a simulcast for a live stream."""
        if not stream_id:
            raise ValueError("Stream ID must be provided.")
        
        try:
            return make_request(
                method="POST", 
                endpoint=f"/live/streams/{stream_id}/simulcast", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            raise APIError(f"Failed to create simulcast: {str(e)}")
    
    def get_simulcast(self, stream_id, simulcast_id):
        """Retrieve a specific simulcast."""
        if not stream_id or not simulcast_id:
            raise ValueError("Stream ID and Simulcast ID must be provided.")
        
        try:
            return make_request(
                method="GET", 
                endpoint=f"/live/streams/{stream_id}/simulcast/{simulcast_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to retrieve simulcast: {str(e)}")
    
    def update_simulcast(self, stream_id, simulcast_id, data):
        """Update a specific simulcast."""
        if not stream_id or not simulcast_id:
            raise ValueError("Stream ID and Simulcast ID must be provided.")
        
        try:
            return make_request(
                method="PUT", 
                endpoint=f"/live/streams/{stream_id}/simulcast/{simulcast_id}", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            raise APIError(f"Failed to update simulcast: {str(e)}")
    
    def delete_simulcast(self, stream_id, simulcast_id):
        """Delete a specific simulcast."""
        if not stream_id or not simulcast_id:
            raise ValueError("Stream ID and Simulcast ID must be provided.")
        
        try:
            return make_request(
                method="DELETE", 
                endpoint=f"/live/streams/{stream_id}/simulcast/{simulcast_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to delete simulcast: {str(e)}")
            