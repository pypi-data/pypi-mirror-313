import importlib.metadata

dist = importlib.metadata.distribution("pyovo")
print(f"Description: {dist.metadata['summary']}")
