import requests
import pandas as pd

# Function to get Spotify access token
def get_spotify_token(client_id, client_secret):
	auth_url = 'https://accounts.spotify.com/api/token'
	auth_response = requests.post(auth_url, {
	'grant_type': 'client_credentials',
	'client_id': client_id,
	'client_secret': client_secret,
	})
	auth_data = auth_response.json()
	return auth_data['access_token']

# Function to search for a track and get its ID
def search_track(track_name, artist_name, token):
	query = f"{track_name} artist:{artist_name}"
	url = f"https://api.spotify.com/v1/search?q={query}&type=track"
	response = requests.get(url, headers={
	'Authorization': f'Bearer {token}'
	})
	json_data = response.json()
	try:
		first_result = json_data['tracks']['items'][0]
		track_id = first_result['id']
		return track_id
	except (KeyError, IndexError):
		return None

# Function to get track details
def get_track_details(track_id, token):
	url = f"https://api.spotify.com/v1/tracks/{track_id}"
	response = requests.get(url, headers={
	'Authorization': f'Bearer {token}'
	})
	json_data = response.json()
	print("API Response:", json_data)
	image_url = json_data['album']['images'][0]['url']
	return image_url

# Your Spotify API Credentials
client_id = '4119b1c63acb4029a90aae046934494b'
client_secret = '7ebb56dcf5c74fe295b50b30b4a20a4e'

# Get Access Token
access_token = get_spotify_token(client_id, client_secret)

# Read your DataFrame (replace 'spotify-2023.csv' "D:\Projects\Spotify Power BI\spotify-2023.xlsx")
df_spotify = pd.read_csv(r'D:\Projects\Spotify\spotify-2023.csv', encoding='ISO-8859-1')

# Loop through each row to get track details and add to DataFrame
for i, row in df_spotify.iterrows():
	track_id = search_track(row['track_name'], row['artist_name'], access_token)
	if track_id:
		image_url = get_track_details(track_id, access_token)
		df_spotify.at[i, 'image_url'] = image_url

# Save the updated DataFrame (replace 'updated_file.csv' with your desired output file name)
df_spotify.to_csv('updated_file.csv', index=False)