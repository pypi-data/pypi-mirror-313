"""
Exploration script to analyze road categories and measurement points
"""
from typing import Dict, List, Set
from collections import defaultdict
from .client import query_traffic_registration_points

def explore_road_categories(base_url: str) -> None:
    """
    Query and analyze traffic measurement points by road category.
    
    Categories:
    - E: European highways (Europavei)
    - R: National roads (Riksvei)
    - F: County roads (Fylkesvei) 
    - K: Municipal roads (Kommunal vei)
    - P: Private roads/paths (Privat vei)
    """
    # Test all valid road categories
    categories = ['E', 'R', 'F', 'K', 'P']
    
    results: Dict[str, List] = {}
    for cat in categories:
        try:
            points = query_traffic_registration_points(base_url, cat)
            if points:
                results[cat] = points
                print(f"\nRoad category '{cat}' has {len(points)} measurement points")
                # Sample some point names to understand the category
                for point in points[:3]:
                    print(f"  Example: {point.name}")
        except Exception as e:
            print(f"Category '{cat}' failed: {str(e)}")
    
    # Analyze the results
    total_points = sum(len(points) for points in results.values())
    print(f"\nTotal measurement points across all categories: {total_points}")
    
    # Look for patterns in naming
    road_prefixes: Dict[str, Set[str]] = defaultdict(set)
    for cat, points in results.items():
        for point in points:
            # Extract the road number/prefix from the name
            parts = point.name.split()
            if parts:
                road_prefixes[cat].add(parts[0])
    
    print("\nRoad number patterns by category:")
    for cat, prefixes in road_prefixes.items():
        print(f"Category {cat}: {', '.join(sorted(prefixes))}")

if __name__ == "__main__":
    BASE_URL = "https://trafikkdata-api.atlas.vegvesen.no/"
    explore_road_categories(BASE_URL)
