# AskVideosClient

`AskVideosClient` is a Python client for interacting with the AskVideos API. This client allows you to create indices, search for videos, synthesize answers from multiple videos, index videos from various sources (YouTube search, URL, playlist, channel), and more.

## Installation

To install the python client.

```bash
pip install askvideos
```

## Usage

### Set-up client
```python
from ask_videos_client import AskVideosClient

api_url = os.environ.get("ASKVIDEOS_SERVER_URL")
api_key = os.environ.get("ASKVIDEOS_API_KEY")
client = AskVideosClient(api_url, api_key)

```
### Create an index
```python
index_name = "coffee"
client.create_index(index_name)
```

### Text search
```
query = "coldbrew"
results = client.search_videos(index_name, query)
print(results)
```
