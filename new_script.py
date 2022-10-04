import requests
import pandas as pd

xhr = 'https://api.decentraland.org/v2/tiles'
response = requests.get(xhr)

# load data into JSON object
tiles = response.json().get("data")
# print(tiles)

tile_table = []

# print(tiles.get("data"))

for tile_key in tiles:
    # tile_table.append(tiles.get(tile_key))
    # this_tile = []
    # for tile_attribute in tiles.get(tile_key):
    #     this_tile.append(tiles.get(tile_key).get(tile_attribute))
    # tile_table.append(this_tile)
    tile_table.append(tiles.get(tile_key))

# print(tile_table)

df = pd.DataFrame(tile_table)
# print(df)

# df = pd.DataFrame(tile_table, columns=["id", "x", "y", "updatedAt", "type", "top", "left", "topLeft", "estateId", "owner", "tokenId"])
df.to_csv("all_parcels.csv", index=True, header=True)
