
### create <a name="create"></a>
Create Animation

Create a Animation video. The estimated frame cost is calculated based on the `fps` and `end_seconds` input.

**API Endpoint**: `POST /v1/animation`

#### Synchronous Client

```python
from magic_hour import Client
from os import getenv

client = Client(token=getenv("API_TOKEN"))
res = client.v1.animation.create(
    data={
        "assets": {
            "audio_file_path": "api-assets/id/1234.mp3",
            "audio_source": "file",
            "image_file_path": "api-assets/id/1234.png",
            "youtube_url": "http://www.example.com",
        },
        "end_seconds": 15,
        "fps": 12,
        "height": 960,
        "name": "Animation video",
        "style": {
            "art_style": "Painterly Illustration",
            "art_style_custom": "string",
            "camera_effect": "Accelerate",
            "prompt": "Cyberpunk city",
            "prompt_type": "ai_choose",
            "transition_speed": 5,
        },
        "width": 512,
    }
)
```

#### Asynchronous Client

```python
from magic_hour import AsyncClient
from os import getenv

client = AsyncClient(token=getenv("API_TOKEN"))
res = await client.v1.animation.create(
    data={
        "assets": {
            "audio_file_path": "api-assets/id/1234.mp3",
            "audio_source": "file",
            "image_file_path": "api-assets/id/1234.png",
            "youtube_url": "http://www.example.com",
        },
        "end_seconds": 15,
        "fps": 12,
        "height": 960,
        "name": "Animation video",
        "style": {
            "art_style": "Painterly Illustration",
            "art_style_custom": "string",
            "camera_effect": "Accelerate",
            "prompt": "Cyberpunk city",
            "prompt_type": "ai_choose",
            "transition_speed": 5,
        },
        "width": 512,
    }
)
```

**Upgrade to see all examples**
