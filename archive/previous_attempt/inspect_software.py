try:
    import diagrams.programming.language as pl
    print("Programming Language:", dir(pl))
except ImportError as e:
    print(e)

try:
    import diagrams.programming.framework as pf
    print("Programming Framework:", dir(pf))
except ImportError as e:
    print(e)

try:
    import diagrams.onprem.network as on
    print("OnPrem Network:", dir(on))
except ImportError as e:
    print(e)
    
try:
    import diagrams.generic.software as gs
    print("Generic Software:", dir(gs))
except ImportError as e:
    print("Generic Software:", e)
