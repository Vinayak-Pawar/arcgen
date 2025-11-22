try:
    import diagrams.onprem.client as client
    print("OnPrem Client:", dir(client))
except ImportError as e:
    print("OnPrem Client:", e)
