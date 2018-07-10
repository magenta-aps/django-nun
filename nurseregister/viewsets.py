from dafo_common import rest_tools
from nurseregister import serializers

import sys

# Define custom viewsets here

# Autogenerate a viewset for each configured ModelSerializer
rest_tools.autogenerate_viewsets(sys.modules[__name__], serializers)
