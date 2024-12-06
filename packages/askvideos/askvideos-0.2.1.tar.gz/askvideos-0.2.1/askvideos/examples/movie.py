import askvideos

# Create client
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlOYW1lIjoidGVzdCIsImlhdCI6MTcxOTkxMDI2OCwiZXhwIjoxNzE5OTEzODY4fQ.BTDKyTCwwlDRDqpPCjMA5LPelCdrvsmIRwN1lWrfmTY'
client = askvideos.Client(api_key=api_key)

# Create an index
indices = client.list_indices()
print(indices)
exit()
index_name = 'movie_example'
client.create_index(index_name)

# List all available indexes
indices = client.list_indices()
print(indices)

# Index a video
movie_file = 'no_country_for_old_men.mp4'
transcript_path = 'no_country_for_old_men.vtt'
metadata = {
  'title': "No Country For Old Men",
  'description': "A classic thriller set in the deserts of Texas",
  'info': {}
}

results = client.index(
            index_name,
            movie_file,
            transcript_path=transcript_path)

print(results)

# Search

# Search by text
# Find scenes with cowboy hats
search_term = 'cowboy hats'

results = client.search_videos(
            index_name,
            search_term,
            top_k=10)
print(results)

# Search by image
# Find scenes with an image
image_path = 'img.jpg'

results = client.search_by_image(
            index_name,
            image_path=image_path,
            top_k=10)
print(results)


# Search by video
# Find scenes with an video
query_video_path = 'video.mp4'

results = client.search_by_video(
            index_name,
            video_path=query_video_path,
            start_seconds=10,
            end_seconds=14,
            top_k=10)
print(results)

# Answer Engine

# Answer a question
query = 'Which city is this movie set in?'
results = client.answer(
            index_name,
            query)

