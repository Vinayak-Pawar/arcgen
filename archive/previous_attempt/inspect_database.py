try:
    # pyrefly: ignore [missing-import]
    import diagrams.generic.database as gd
    print("Generic Database:", dir(gd))
except ImportError as e:
    print("Generic Database:", e)
