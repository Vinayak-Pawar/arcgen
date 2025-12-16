try:
    # pyrefly: ignore [missing-import]
    import diagrams.programming.language as pl
    print("Programming Language:", dir(pl))
except ImportError as e:
    print(e)

try:
    # pyrefly: ignore [missing-import]
    import diagrams.programming.framework as pf
    print("Programming Framework:", dir(pf))
except ImportError as e:
    print(e)

try:
    # pyrefly: ignore [missing-import]
    import diagrams.onprem.network as on
    print("OnPrem Network:", dir(on))
except ImportError as e:
    print(e)
    
try:
    # pyrefly: ignore [missing-import]
    import diagrams.generic.software as gs
    print("Generic Software:", dir(gs))
except ImportError as e:
    print("Generic Software:", e)
