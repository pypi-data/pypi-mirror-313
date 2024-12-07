from .exceptions import APIError
from .api import make_request

class MediaPlaybackIDs:
    def __init__(self, client):
        self.client = client
    
    def create(self, media_id, data):
        """Create a playback ID for a media resource."""
        if not media_id:
            raise ValueError("Media ID must be provided.")
        
        try:
            return make_request(
                method="POST", 
                endpoint=f"/on-demand/{media_id}/playback-ids", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            raise APIError(f"Failed to create media playback ID: {str(e)}")
    
    def delete(self, media_id, playback_ids):
        """Delete playback IDs for a media resource."""
        if not media_id:
            raise ValueError("Media ID must be provided.")
        
        try:
            return make_request(
                method="DELETE", 
                endpoint=f"/on-demand/{media_id}/playback-ids", 
                headers=self.client.headers,
                params={'playbackId': playback_ids}
            )
        except APIError as e:
            raise APIError(f"Failed to delete media playback IDs: {str(e)}")

class LivestreamPlaybackIDs:
    def __init__(self, client):
        self.client = client
    
    def create(self, stream_id, data=None):
        """Create a playback ID for a live stream."""
        if not stream_id:
            raise ValueError("Stream ID must be provided.")
        
        try:
            return make_request(
                method="POST", 
                endpoint=f"/live/streams/{stream_id}/playback-ids", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            raise APIError(f"Failed to create live stream playback ID: {str(e)}")
    
    def delete(self, stream_id, playback_ids):
        """Delete a specific playback ID for a live stream."""
        if not stream_id:
            raise ValueError("Stream ID must be provided.")
        
        try:
            return make_request(
                method="DELETE", 
                endpoint=f"/live/streams/{stream_id}/playback-ids", 
                headers=self.client.headers,
                params={'playbackId': playback_ids}
            )
        except APIError as e:
            raise APIError(f"Failed to delete live stream playback ID: {str(e)}")
    
    def get(self, stream_id, playback_id):
        """Retrieve a specific playback ID for a live stream."""
        if not stream_id or not playback_id:
            raise ValueError("Stream ID and Playback ID must be provided.")
        
        try:
            return make_request(
                method="GET", 
                endpoint=f"/live/streams/{stream_id}/playback-ids/{playback_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to retrieve live stream playback ID: {str(e)}")
            