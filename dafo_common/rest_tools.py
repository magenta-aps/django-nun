from django.db import models
from rest_framework import routers
from rest_framework import serializers
from rest_framework import viewsets

import inspect
import os
import sys


def get_namespace_from_model(model):
    if not hasattr(model._meta, "rest_namespace"):
        namespace = get_namespace_from_module(sys.modules[model.__module__])
        setattr(model._meta, "rest_namespace", namespace)

    return getattr(model._meta, "rest_namespace")

def get_namespace_from_module(module):
    if not hasattr(module, "REST_NAMESPACE"):
        abspath = os.path.abspath(module.__file__)
        dirname = os.path.dirname(abspath)
        namespace = os.path.basename(dirname)
        setattr(module, "REST_NAMESPACE", namespace)

    return getattr(module, "REST_NAMESPACE")

def get_rest_reverse_name_from_model(model):
    # Get rest reverse name and fall back to using the model name if none
    # is specified
    if not hasattr(model._meta, "rest_reverse_name"):
        setattr(model._meta, "rest_reverse_name", model._meta.model_name)
    return getattr(model._meta, "rest_reverse_name")

def create_model_serializer_class(target_module, model):
    # Class name is name of model postfixed with "Serializer"
    class_name = model.__name__ + "Serializer"

    # If it already exists just return that
    if hasattr(target_module, class_name):
        return getattr(target_module, class_name)

    # reverse name for the detail view is
    #   <namespace>:<reverse_name>-detail
    namespace = get_namespace_from_model(model)
    reverse_name = get_rest_reverse_name_from_model(model)
    detail_reverse_name = "".join([namespace, ":", reverse_name, "-detail"])

    # Create a dynamic Serializer class
    cls = type(
        # Class name
        class_name,
        # Base classes
        (serializers.ModelSerializer,),
        # Members
        {
            "__module__": target_module.__name__,
            "url": serializers.HyperlinkedIdentityField(
                view_name=detail_reverse_name
            ),
            "Meta": create_model_serializer_meta_class(model, target_module)
        }
    )

    # Store it as a class in the module
    setattr(target_module, class_name, cls)

    return cls


def create_model_serializer_meta_class(model, in_module):
    return type(
        "Meta",  # class name
        tuple(),  # Base classes
        # members
        {
            "__module__": in_module.__name__,
            "model": model,
            "fields": "__all__"
        }
    )


def autogenerate_serializers(serializer_module, models_module):
    # Call this to make sure we do not modify the models_module while looping
    # over it
    get_namespace_from_module(models_module)

    for k, v in models_module.__dict__.items():
        if inspect.isclass(v) and issubclass(v, models.Model):
            create_model_serializer_class(serializer_module, v)


def get_model_from_serializer(serializer):
    return serializer.Meta.model


def create_readonly_model_viewset(viewsets_module, serializer):
    model = get_model_from_serializer(serializer)

    class_name = model.__name__ + "ViewSet"

    # If it already exists just return that
    if hasattr(viewsets_module, class_name):
        return getattr(viewsets_module, class_name)

    if hasattr(model, 'filter_fields'):
        filter_fields = getattr(model, 'filter_fields')
    else:
        filter_fields = None
    if hasattr(model, 'search_fields'):
        search_fields = getattr(model, 'search_fields')
    else:
        search_fields = None
    

    cls = type(
        # Class name
        class_name,
        # Base classes
        (viewsets.ReadOnlyModelViewSet,),
        # Members
        {
            "__module__": viewsets_module.__name__,
            "queryset": model.objects.all(),
            "serializer_class": serializer,
            "filter_fields": filter_fields,
            "search_fields": search_fields,
        }
    )

    # Store it as a class in the module
    setattr(viewsets_module, class_name, cls)

    return cls


def autogenerate_viewsets(viewsets_module, serializer_module):
    for k, v in serializer_module.__dict__.items():
        if inspect.isclass(v) and issubclass(v, serializers.ModelSerializer):
            create_readonly_model_viewset(viewsets_module, v)

def autogenerate_router(viewsets_module):
    router = routers.DefaultRouter()
    for k, v in viewsets_module.__dict__.items():
        if inspect.isclass(v) and issubclass(v, viewsets.GenericViewSet):
            model = get_model_from_serializer(v.serializer_class())
            reverse_name = get_rest_reverse_name_from_model(model)
            router.register(reverse_name, v)

    return router
