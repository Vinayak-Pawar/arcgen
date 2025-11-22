import importlib
import pkgutil
import diagrams.aws

def find_node(node_name, package):
    """Recursively search for a node in a package."""
    results = []
    if hasattr(package, "__path__"):
        for _, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            try:
                module = importlib.import_module(name)
                if hasattr(module, node_name):
                    results.append(name)
            except ImportError:
                continue
    return results

print(f"Searching for DynamoDB in diagrams.aws...")
locations = find_node("DynamoDB", diagrams.aws)
print(f"Found DynamoDB in: {locations}")

# Also check for case variations just in case
print(f"Searching for Dynamodb in diagrams.aws...")
locations_lower = find_node("Dynamodb", diagrams.aws)
print(f"Found Dynamodb in: {locations_lower}")
