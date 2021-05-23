from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mistake.analyze.analyze import error_finder
from mistake.api.permissions import SentencePermission, MistakePermission
from mistake.api.serializers import SentenceSerializer, MistakeSerializer
from mistake.models import Sentence, Mistake


def _getType(mistake):
    return {'id': mistake.id, 'type': mistake.type}


class SentenceViewSet(viewsets.ModelViewSet):
    permission_classes = [SentencePermission]
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer

    def create(self, request, *args, **kwargs):
        serializer = SentenceSerializer(data=request.data)
        if serializer.is_valid():
            sentence = serializer.save()
        data = {'id': sentence.id, 'sentence': sentence.message, 'mistakes': map(_getType, error_finder(sentence))}
        return Response(data)


class MistakeViewSet(viewsets.ModelViewSet):
    permission_classes = [MistakePermission]
    queryset = Mistake.objects.all()
    serializer_class = MistakeSerializer

    @action(methods=['post'], detail=True, url_path='decline', url_name='decline')
    def set_change(self, request, pk=None):
        instance = self.get_object()
        instance.changed_by_user = True
        instance.save()
        return Response(MistakeSerializer(instance).data)
