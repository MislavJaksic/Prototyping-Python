import os
import sys

# Adds "protopy" to sys.path
# Now you can do import with "from protopy.Sub-Package ..."
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "protopy"))
)
