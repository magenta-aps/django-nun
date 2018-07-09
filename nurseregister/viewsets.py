from rest_framework import routers
from rest_framework import viewsets
from nurseregister.models import NurseRegistration
from nurseregister.serializers import create_model_serializer_class

import sys

def create_readonly_model_viewset(namespace, reverse_name, model):
    class_name = model.__name__ + "ViewSet"

    # If it already exists just return that
    if hasattr(sys.modules[__name__], class_name):
        return getattr(sys.modules[__name__], class_name)

    serializer = create_model_serializer_class(namespace, reverse_name, model)

    cls = type(
        # Class name
        class_name,
        # Base classes
        (viewsets.ReadOnlyModelViewSet,),
        # Members
        {
            "queryset": model.objects.all(),
            "serializer_class": serializer
        }
    )

    # Store it as a class in the module
    setattr(sys.modules[__name__], class_name, cls)

    return cls

def model_to_url_name(model):
    return model.__name__.lower()


def create_router(namespace, model_list):
    router = routers.DefaultRouter()
    for model in model_list:
        reverse_name = model_to_url_name(model)
        viewset = create_readonly_model_viewset(namespace, reverse_name, model)
        router.register(reverse_name, viewset)
    
    return router
