from .exceptions import APIError
from .api import make_request

class MediaResource:
    def __init__(self, client):
        self.client = client
    
    def get_all(self):
        """Fetch all medias."""
        try:
            return make_request(
                method="GET", 
                endpoint="/on-demand", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to fetch medias: {str(e)}")

    def get_by_id(self, media_id):
        """Fetch media by its ID."""
        if not media_id:
            raise ValueError("Media ID must be provided.")
        
        try:
            return make_request(
                method="GET", 
                endpoint=f"/on-demand/{media_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to fetch media: {str(e)}")

    def update(self, media_id, data):
        """Update media by its ID."""
        if not media_id:
            raise ValueError("Media ID must be provided.")
        
        try:
            return make_request(
                method="PATCH", 
                endpoint=f"/on-demand/{media_id}", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            raise APIError(f"Failed to update media: {str(e)}")

    def delete(self, media_id):
        """Delete media by its ID."""
        if not media_id:
            raise ValueError("Media ID must be provided.")
        
        try:
            return make_request(
                method="DELETE", 
                endpoint=f"/on-demand/{media_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to delete media: {str(e)}")

    def create_pull_video(self, data):
        """Create an on-demand request by calling the /on-demand endpoint."""
        endpoint = "/on-demand"
        
        if "accessPolicy" not in data:
            data["accessPolicy"] = "public"
        
        try:
            response = make_request(
                method="POST", 
                endpoint=endpoint, 
                headers=self.client.headers, 
                data=data
            )
            return response
        except APIError as e:
            raise APIError(f"Failed to create on-demand request: {str(e)}")

    def get_presigned_url(self, data):
        """Create an on-demand presigned URL request by calling the /on-demand/uploads endpoint."""
        endpoint = "/on-demand/uploads"
        
        if "corsOrigin" not in data:
            data["corsOrigin"] = "*"
        
        try:
            response = make_request(
                method="POST", 
                endpoint=endpoint, 
                headers=self.client.headers, 
                data=data
            )
            return response
        except APIError as e:
            raise APIError(f"Failed to create presigned URL request: {str(e)}")
            