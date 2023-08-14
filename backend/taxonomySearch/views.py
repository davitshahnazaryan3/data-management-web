from django.http import Http404
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status
from taxonomySearch import models
from taxonomySearch import serializers


class SpecimenTypes(APIView):
    def get(self, request, format=None):
        if cache.get("specimen-type"):
            options = cache.get("specimen-type")
        else:
            options = models.SpecimenType.objects.all()
            cache.set("specimen-type", options)

        serializer = serializers.SpecimenTypeSerializer(options, many=True)
        return Response(serializer.data)


class SelectedSpecimenType(APIView):
    def get_object(self, specimen_id):
        try:
            return models.SpecimenType.objects.get(id=specimen_id)
        except models.SpecimenType.DoesNotExist:
            raise Http404

    def get(self, request, specimen_id, format=None):

        if cache.get('specimen-type'):
            options = cache.get('specimen-type')
            specimenType = options.get(id=specimen_id)

        else:
            specimenType = self.get_object(specimen_id)

        serializer = serializers.SpecimenTypeSerializer(specimenType)

        return Response(serializer.data)

    
class MaterialTypes(APIView):
    def get(self, request, format=None):
        if cache.get("material-type"):
            options = cache.get("material-type")
        else:
            options = models.TypeMaterial.objects.all()
            cache.set("material-type", options)
            
        serializer = serializers.TypeMaterialSerializer(options, many=True)
        return Response(serializer.data)


class SelectedMaterialType(APIView):
    def get_object(self, material_id):
        try:
            return models.TypeMaterial.objects.get(id=material_id)
        except models.TypeMaterial.DoesNotExist:
            raise Http404

    def get(self, request, material_id, format=None):

        if cache.get('material-type'):
            options = cache.get('material-type')
            materialType = options.get(id=material_id)

        else:
            materialType = self.get_object(material_id)

        serializer = serializers.TypeMaterialSerializer(materialType)

        return Response(serializer.data)


class MaterialTechnologies(APIView):
    def get(self, request, format=None):
        if cache.get("material-technology"):
            options = cache.get("material-technology")
        else:
            options = models.MaterialTechnology.objects.all()
        serializer = serializers.MaterialTechnologySerializer(options, many=True)
        return Response(serializer.data)


class MaterialProperties(APIView):
    def get(self, request, format=None):
        if cache.get("material-properties"):
            options = cache.get("material-properties")
        else:
            options = models.MaterialProperties.objects.all()
        serializer = serializers.MaterialPropertiesSerializer(options, many=True)
        return Response(serializer.data)


class LLRSystems(APIView):
    def get(self, request, format=None):
        if cache.get("llrs"):
            options = cache.get("llrs")
        else:
            options = models.LateralLoadResistingSystemType.objects.all()
        serializer = serializers.LateralLoadResistingSystemTypeSerializer(options, many=True)
        return Response(serializer.data)


class SystemDuctilities(APIView):
    def get(self, request, format=None):
        if cache.get("system-ductility"):
            options = cache.get("system-ductility")
        else:
            options = models.SystemDuctility.objects.all()
        serializer = serializers.SystemDuctilitySerialzier(options, many=True)
        return Response(serializer.data)


class UpdateCacheTaxonomy(APIView):
    def _set_cache(self, obj, key):
        options = obj.objects.all()
        cache.set(key, options)

    def get(self, request):
        try:
            # Material type
            self._set_cache(models.TypeMaterial, "material-type")
            
            # Material technology
            self._set_cache(models.MaterialTechnology, "material-technology")
            
            # Material technology
            self._set_cache(models.SpecimenType, "specimen-type")
            
            # Material technology
            self._set_cache(models.SpecimenSubType, "specimen-sub-type")
            
            return Response(status=status.HTTP_200_OK)

        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
