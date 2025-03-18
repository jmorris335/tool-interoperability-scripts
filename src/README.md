This directory contains the simulating the constraint hypergraph of the crankshaft model.

Files included:
- crankshaft_chg.py : The primary script for creating the nodes and edges of the constraint hypergraph
- crankshaft_objects.py : A python script describing the objects in the hypergraph (called in `crankshaft_chg.py`). These objects are only collections of nodes, and do not encapsulate the system state.
- crankshaftchg_rels.py : A python script describing some of the functions used in `crankshaft_chg.py`.
- onshape_api : a repository of code mostly taken from an old Onshape repository for connecting with their API.

Note that to use the code you also need to provide your authorization tokens for connecting with Onshape's API. The script is set up to look for this in a file called SECRETS.json, located here. More information for what to include in SECRETS is given [here](https://onshape-public.github.io/docs/auth/apikeys/)
