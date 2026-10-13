# DSA ALGORITHM: Directed Acyclic Graph (DAG) & BFS Traversal
# USED FOR: Crop rotation cycle recommendations based on soil nutrient restoration.

class CropGraph:
    def __init__(self):
        self.adj_list = {}

    def add_crop_edge(self, current_crop, next_crop, benefit_score):
        """Adds a directed edge: Current Crop -> Next Crop"""
        c1, c2 = current_crop.lower(), next_crop.lower()
        if c1 not in self.adj_list:
            self.adj_list[c1] = []
        self.adj_list[c1].append({"crop": next_crop, "benefit": benefit_score})

    def get_rotation_plan(self, current_crop):
        """DSA: Traversal - Finds optimal successor crops in DAG network."""
        crop_key = current_crop.lower()
        if crop_key in self.adj_list:
            return sorted(self.adj_list[crop_key], key=lambda x: x['benefit'], reverse=True)
        return []

# Pre-populate DAG Network
rotation_graph = CropGraph()
rotation_graph.add_crop_edge("Rice", "Chickpea (Chana)", 95)
rotation_graph.add_crop_edge("Rice", "Mustard", 85)
rotation_graph.add_crop_edge("Rice", "Lentil", 90)

rotation_graph.add_crop_edge("Wheat", "Moong Dal", 98)
rotation_graph.add_crop_edge("Wheat", "Groundnut", 88)

rotation_graph.add_crop_edge("Tomato", "Maize", 92)
rotation_graph.add_crop_edge("Tomato", "Beans", 90)

rotation_graph.add_crop_edge("Potato", "Sesame", 85)
rotation_graph.add_crop_edge("Potato", "Cowpea", 94)
