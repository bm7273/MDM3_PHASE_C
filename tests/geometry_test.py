import osmnx as ox
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
from pyrosm import OSM

# ============================================================
# Step 1: Download road network with ALL useful tags
# ============================================================

# By default osmnx only retains a subset of tags
# Use the custom_filter or ox.settings to get more

useful_tags = [
    'highway', 'maxspeed', 'lanes', 'surface', 'width',
    'lit', 'bridge', 'tunnel', 'oneway', 'junction',
    'shoulder', 'cycleway', 'sidewalk', 'access',
    'turn:lanes', 'placement', 'divider', 'barrier',
    'hazard', 'overtaking', 'traffic_calming',
    'name', 'ref',
]

# Tell osmnx to retain these tags on edges
ox.settings.useful_tags_way = useful_tags

# Download motorway network for a region
osm = OSM("united-kingdom-260322.osm.pbf")
print('Getting nodes and edges')
nodes, edges = osm.get_network(network_type="driving", nodes=True)
nodes.to_file("england_nodes.gpkg", driver="GPKG")
edges.to_file("england_edges.gpkg", driver="GPKG")
# print('Converting to networkx')
# G = osm.to_graph(nodes, edges, graph_type="networkx")
# Convert to GeoDataFrames


# See what columns/tags you actually got
print("Available edge attributes:")
print(edges.columns.tolist())
print(f"\nCompleteness of key fields:")
for col in ['maxspeed', 'lanes', 'surface', 'width', 'lit', 
            'bridge', 'tunnel']:
    if col in edges.columns:
        pct = edges[col].notna().mean() * 100
        print(f"  {col}: {pct:.1f}% populated")