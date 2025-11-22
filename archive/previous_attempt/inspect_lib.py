try:
    import diagrams.generic.compute as c
    print(dir(c))
except ImportError as e:
    print(e)

try:
    import diagrams.onprem.compute as c
    print(dir(c))
except ImportError as e:
    print(e)
