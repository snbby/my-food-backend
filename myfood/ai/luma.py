import io

import requests

from myfood.models import ModelLumaGenerate

class NotAuthenticatedException(BaseException):
    pass

class LumaClient:
    API_BASE = 'https://internal-api.virginia.labs.lumalabs.ai'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "origin": "https://lumalabs.ai",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36'
    
    def __init__(self):
        self.session = requests.session()
        self.session.headers = self.headers
        self.session.headers.update({'user_agent': self.user_agent})
        self.generations_url = f'{self.API_BASE}/api/photon/v1/user/generations/'
        self.generate_url = f'{self.API_BASE}/api/photon/v1/generations/'
        self.file_upload_url = f'{self.generate_url}file_upload'
        self.usage_url = f'{self.API_BASE}/api/photon/v1/subscription/usage'
        
    def generate(self, luma_obj: ModelLumaGenerate) -> dict:
        self.session.cookies.update({
            'luma_session': luma_obj.access_token
        })
        
        # Get presigned urls
        response = self.session.post(url=self.file_upload_url, params={'file_type': 'image', 'filename': 'file.jpg'})
        response.raise_for_status()
        response_json = response.json()
        if response.status_code == 401:
            luma_obj.authenticated = False
            luma_obj.save()
            raise NotAuthenticatedException('Not authenticated')
        luma_obj.status = ModelLumaGenerate.LumaStatus.generated_presign_url
        luma_obj.luma_id = response_json['id']
        luma_obj.luma_presigned_url = response_json['presigned_url']
        luma_obj.luma_image_public_url = response_json['public_url']
        luma_obj.save()
        
        # Upload file
        response = self.session.put(url=luma_obj.luma_presigned_url, data=luma_obj.s3_file.file)
        response.raise_for_status()
        luma_obj.status = ModelLumaGenerate.LumaStatus.uploaded_image
        luma_obj.save()
        
        # Send to generation
        data = {
            'user_prompt': luma_obj.text,
            'image_url': luma_obj.luma_image_public_url,
            "expand_prompt": True,
            "aspect_ratio": "16:9"
        }
        response = self.session.post(url=self.generate_url, json=data)
        response.raise_for_status()
        luma_obj.status = ModelLumaGenerate.LumaStatus.is_generating
        luma_obj.save()
        
    def get_generations(self, luma_obj: ModelLumaGenerate) -> dict:
        self.session.cookies.update({
            'luma_session': luma_obj.access_token
        })
        response = self.session.get(url=self.generations_url, params={'offset': 0, 'limit': 10})
        if response.status_code == 401:
            luma_obj.authenticated = False
            luma_obj.save()
            raise NotAuthenticatedException('Not authenticated')
        luma_obj.authenticated = True

        response_json = response.json()
        return response_json
    
    def get_video(self, url: str) -> bytes:
        r = self.session.get(url)
        r.raise_for_status()
        return io.BytesIO(r.content)

luma_client = LumaClient()