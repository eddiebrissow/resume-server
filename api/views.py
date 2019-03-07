import os
import datetime

from .models import Resume
from .serializers import ResumeSerializer, UserSerializer
from .filters import Resumefilter
from .permissions import CustomObjectPermissions

from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import APIException, NotFound
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication

from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_condition import Or
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from PyPDF2 import PdfFileReader
from django.http import HttpResponse, Http404


def read_pdf(pdf_file):
    try:
        doc = PdfFileReader(pdf_file)
    except Exception as e:
        raise APIException(str(e))
    return doc

class UserList(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ResumeList(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    parser_classes = (MultiPartParser,)
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = (CustomObjectPermissions, )
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filter_class = Resumefilter
    ordering_fields = '__all__'
    filter_fields = '__all__'

    def perform_create(self, serializer):
        f = self.request.data.get('file')
        doc = read_pdf(f)
        serializer.save(file=f,
                        page_count=doc.getNumPages(),
                        user=self.request.user.username)


class ResumeDetail(generics.RetrieveUpdateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    parser_classes = (MultiPartParser,)
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = (CustomObjectPermissions, )
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = '__all__'

    def perform_update(self, serializer):
        f = self.request.data.get('file')
        doc = read_pdf(f)
        old_filename = str(self.get_object().file)

        serializer.save(file=f,
                        page_count=doc.getNumPages(),
                        user=self.request.user.username,
                        updated=str(datetime.datetime.now()))
        os.unlink(old_filename)


class ResumeDownload(generics.RetrieveAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = (CustomObjectPermissions, )

    def retrieve(self, request, *args, **kwargs):
        file_path = '{0}/{1}'.format(kwargs.get('user'), kwargs.get('name'))

        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise NotFound
