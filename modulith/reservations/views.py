from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from reservations.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("text", "user")


class NotesViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    # queryset = Note.objects.all()

    def get_queryset(self):
        qs = Note.objects.all()
        return qs
