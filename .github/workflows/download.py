import requests
import os

# Get the GitHub Secrets (for security)
key = os.getenv("ITCH_API_KEY")

headers = {"Authorization": key}

# Fetch game data and uploads
game_data = requests.get(f"https://finalforeach.itch.io/cosmic-reach/data.json").json()
uploads = requests.get(f"https://api.itch.io/games/{game_data['id']}/uploads", headers=headers).json()["uploads"]

jar = None
server = None
for upload in uploads:
    if upload["channel_name"] == "jar":
        jar = upload
    if upload["channel_name"] == "server":
        server = upload

# Download files based on conditions
if jar is not None and server is None:
    with open(jar["filename"], "wb") as e:
        e.write(requests.get(f"https://api.itch.io/uploads/{jar['build']['upload_id']}/download", headers=headers).content)

elif server is not None and jar is None:
    with open(server["filename"], "wb") as e:
        e.write(requests.get(f"https://api.itch.io/uploads/{server['build']['upload_id']}/download", headers=headers).content)

elif jar is not None and server is not None and jar["build"]["user_version"] == server["build"]["user_version"]:
    with open(jar["filename"], "wb") as e:
        e.write(requests.get(f"https://api.itch.io/uploads/{jar['build']['upload_id']}/download", headers=headers).content)
    with open(server["filename"], "wb") as e:
        e.write(requests.get(f"https://api.itch.io/uploads/{server['build']['upload_id']}/download", headers=headers).content)
