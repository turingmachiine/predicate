from rest_framework import serializers

from mistake.models import Sentence, Mistake


class SentenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sentence
        fields = ('message', 'author')


class MistakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mistake
        fields = ('type', 'sentence', 'changed_by_user')

