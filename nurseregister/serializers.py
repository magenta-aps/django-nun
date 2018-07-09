from nurseregister import models
from rest_framework import serializers

import sys

def create_model_serializer_class(namespace, reverse_name, model):
    # Class name is name of model postfixed with "Serializer"
    class_name = model.__name__ + "Serializer"

    # If it already exists just return that
    if hasattr(sys.modules[__name__], class_name):
        return getattr(sys.modules[__name__], class_name)

    # reverse name for the detail view is
    #   <namespace>:<reverse_name>-detail
    detail_reverse_name = "".join([namespace, ":", reverse_name, "-detail"])
    cls = type(
        # Class name
        class_name,
        # Base classes
        (serializers.ModelSerializer,),
        # Members
        {
            "url": serializers.HyperlinkedIdentityField(
                view_name=detail_reverse_name
            ),
            "Meta": create_model_serializer_meta_class(model)
        }
    )

    # Store it as a class in the module
    setattr(sys.modules[__name__], class_name, cls)

    return cls

def create_model_serializer_meta_class(model):
    return type(
        "Meta", # class name
        tuple(), # Base classes
        {"model": model, "fields": "__all__"} # members
    )
