from dafo_common import rest_tools
from nurseregister import models

import sys

# Add custom serializers here.

# Automatically generate serializers for models that are has enable_rest = True
# in their Meta data and does not have a customized serializer.
rest_tools.autogenerate_serializers(sys.modules[__name__], models)
