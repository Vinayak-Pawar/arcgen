try:
    # pyrefly: ignore [missing-import]
    import diagrams.generic.compute as c
    print(dir(c))
except ImportError as e:
    print(e)

try:
    # pyrefly: ignore [missing-import]
    import diagrams.onprem.compute as c
    print(dir(c))
except ImportError as e:
    print(e)
