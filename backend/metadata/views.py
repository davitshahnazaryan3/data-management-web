import operator
import logging
from functools import reduce
import mimetypes

from django.db.models import Q, F, Count, Min
from django.http import Http404, HttpResponse
from django.conf import settings
from django.core import mail
from django.core.cache import cache
from django.core.mail.message import EmailMessage

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from metadata import models
from metadata import serializers

from django.http import StreamingHttpResponse, FileResponse
from wsgiref.util import FileWrapper


logger = logging.getLogger('django')


def get_datasets(logger_msg):
    if cache.get("metadata"):
        projects = cache.get("metadata").order_by('-year_of_experiment')
        logger.info(f"Reading {logger_msg} from CACHE")
        
    else:
        projects = models.Dataset.objects.all().order_by('-year_of_experiment')
        cache.set("metadata", projects)
        logger.info(f"Reading {logger_msg} from SERVER")

    return projects


class MostDownloadedDatasets(APIView):
    @extend_schema(responses=serializers.DatasetSerializer, description='Get Most Downloaded Datasets')
    def get(self, request, format=None):

        projects = get_datasets('most downloaded datasets')

        # show 4 datasets max
        count = 4
        if len(projects) < count:
            count = len(projects)
        
        latest_projects = projects.order_by('-downloads')[:count]
        serializer = serializers.DatasetSerializer(latest_projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LatestProjects(APIView):
    @extend_schema(responses=serializers.DatasetSerializer, description='Get Latest Datasets')
    def get(self, request, format=None):

        projects = get_datasets("latest datasets")

        # show 4 projects max
        count = 4
        if len(projects) < count:
            count = len(projects)

        latest_projects = projects[:count]
        serializer = serializers.DatasetSerializer(latest_projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectDetail(APIView):
    def get_object(self, project_id):
        try:
            if cache.get("metadata"):
                project = cache.get("metadata").get(id=project_id)
            else:
                project = models.Dataset.objects.get(id=project_id)
            return project
        except models.Dataset.DoesNotExist:
            logger.error(f"Dataset with ID {project_id} does not exist!")
            raise Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(responses=serializers.DatasetSerializer)
    def get(self, request, project_id, format=None):
        project = self.get_object(project_id)
        serializer = serializers.DatasetSerializer(project)
        logger.info(f"Dataset with ID {project_id} found!")
        return Response(serializer.data, status=status.HTTP_200_OK)


class PersonDetail(APIView):
    def get_object(self, person_slug):
        try:
            return models.Person.objects.get(slug=person_slug)
        except models.Person.DoesNotExist:
            logger.error(f"Person {person_slug} does not exist!")
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, person_slug, format=None):
        person = self.get_object(person_slug)
        serializer = serializers.PersonSerializerRef(person)
        logger.info(f"PI {person_slug} found!")
        return Response(serializer.data, status=status.HTTP_200_OK)


class FacilityDetail(APIView):
    def get_object(self, facility_slug):
        try:
            return models.ExperimentalFacility.objects.get(slug=facility_slug)
        except models.ExperimentalFacility.DoesNotExist:
            logger.error(f"Facility {facility_slug} does not exist!")
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, facility_slug, format=None):
        facility = self.get_object(facility_slug)
        serializer = serializers.ExperimentalFacilitySerializerRef(facility)
        logger.info(f"Facility {facility_slug} found!")
        return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        all_projects = get_datasets("all datasets for query")

        projects = all_projects.filter(
            Q(experiment_title__icontains=query) |
            Q(keywords__icontains=query) |
            Q(experiment_description__icontains=query) |
            Q(experiment_pi__first_name__icontains=query) |
            Q(experiment_pi__last_name__icontains=query) |
            Q(experiment_facility__name__icontains=query)
        ).distinct()

        serializer = serializers.DatasetSerializer(projects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        return Response({'datasets': []}, status=status.HTTP_200_OK)
        

@api_view(['POST'])
def filterProjectsByMetadata(request):
    if cache.get('current-projects'):
        all_projects = cache.get('current-projects')
    else:
        return Response({'datasets': []})
    
    engineeringDiscipline = request.data.get('engineeringDiscipline', '')
    license = request.data.get('license', '')
    experimentType = request.data.get('experimentType', '')
    experimentScale = request.data.get('experimentScale', '')
    
    if engineeringDiscipline == "Any":
        engineeringDiscipline = ""
    if license == "Any":
        license = ""
    if experimentType == "Any":
        experimentType = ""
    if experimentScale == "Any":
        experimentScale = ""

    projects = all_projects.filter(
        Q(engineering_discipline__discipline__icontains=engineeringDiscipline) &
        Q(license__name__icontains=license) &
        Q(experiment_type__name__icontains=experimentType) &
        Q(experiment_scale__name__icontains=experimentScale)
    ).distinct()

    serializer = serializers.DatasetSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def queryProjectsByTaxonomy(request):
    query = request.data.get('tax', '')

    if not query:
        projects = get_datasets('all datasets')
        serializer = serializers.DatasetSerializer(projects, many=True)
        
        # to be used by a metadata filter
        cache.set('current-projects', projects)

        return Response(serializer.data)
    
    if not isinstance(query, list):
        query = query.split("/")

    if query:
        all_projects = get_datasets('all datasets')

        projects = all_projects.filter(
            reduce(operator.and_, (Q(taxonomy__icontains=f"/{tax}/") for tax in query if tax != ""))
        ).order_by('-year_of_experiment')

        serializer = serializers.DatasetSerializer(projects, many=True)
    
        # to be used by a metadata filter
        cache.set('current-projects', projects)

        logger.info(f"Query based on taxonomy: {query}, Number of datasets {len(projects)}")

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        # to be used by a metadata filter
        cache.set('current-projects', [])

        return Response({'datasets': []}, status=status.HTTP_200_OK)


class UpdateCacheMetadata(APIView):
    def get(self, request):
        try:
            projects = models.Dataset.objects.all()
            cache.set("metadata", projects)
            logger.info("Dataset metadata cache was updated")
            return Response(status=status.HTTP_200_OK)

        except models.Dataset.DoesNotExist:
            logger.error("No datasets were found for caching...")
            return Response(status=status.HTTP_404_NOT_FOUND)


class AllProjects(APIView):
    def get(self, request, format=None):
        projects = get_datasets("All datasets")
        serializer = serializers.DatasetSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view(['GET'])
def download_data(request, project_id):
    try:

        if cache.get("metadata"):
            project = cache.get("metadata").get(id=project_id)
        else:
            project = models.Dataset.objects.get(id=project_id)

        if project.url:
            file_path = settings.BASE_DIR.parents[2] / "data/storage" / project.url
            filename = file_path.name
            chunk_size = 8192

            response = FileResponse(
                FileWrapper(open(file_path, 'rb'), chunk_size),
                content_type=mimetypes.guess_type(file_path)[0],
                # content_type = 'application/zip'
            )

            response['Content-Length'] = file_path.stat().st_size
            response['Content-Disposition'] = "attachment; filename=%s" % filename

            # increment download count
            project.downloads += 1
            project.save(update_fields=['downloads'])

            logger.info(f"Download of dataset {project_id} successful!")
            return response
        else:
            logger.error(f"Download of dataset {project_id} failed!")
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    except models.Dataset.DoesNotExist:
        logger.error(f"Download of dataset {project_id} failed. Dataset does not exist!")
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def contact(request):
    try:
        # Get data from frontend
        fname = request.data["first_name"]
        lname = request.data["last_name"]
        email = request.data["email"]
        phone = request.data["phone"]
        company = request.data["company"]
        position = request.data["position"]
        how_hear = request.data["how_hear"]
        message = request.data["message"]
        
        # send email
        connection = mail.get_connection()
        connection.open()
        email_message = EmailMessage(
            f'Contact request from {fname} {lname}',
            f'SenderEmail: {email}\n\
                PhoneNumber: {phone}\n\
                Company: {company}\n\
                Position: {position}\n\
                How did you hear about us? {how_hear}\n\n\
                {message}',
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            connection=connection,
        )

        connection.send_messages([email_message])
        connection.close()
        
        logger.info(f"Contact request from {email} successful!")
        return Response(status=status.HTTP_200_OK)

    except Exception:
        logger.error("Contact request failed!")
        return Response(status=status.HTTP_400_BAD_REQUEST)

