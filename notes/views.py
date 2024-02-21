from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Note, NoteVersionHistory
from .serializers import NoteSerializer, NoteVersionHistorySerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        # Generate or retrieve the token for the user
        token, _ = Token.objects.get_or_create(user=user)

        # Return the token in the response
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def signup_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if username or email already exists
    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = User.objects.create_user(
        username=username, email=email, password=password)
    user.save()

    return Response({'message': 'User created successfully', 'id': user.id}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_notes(request):
    # Get all notes that are either owned by the user or shared with the user
    notes = Note.objects.filter(owner=request.user) | Note.objects.filter(
        shared_with=request.user)

    # Serialize the notes
    serializer = NoteSerializer(notes, many=True)

    # Return the serialized notes
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_note(request):
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_note(request, id):
    note = Note.objects.get(pk=id)
    if request.user == note.owner or request.user in note.shared_with.all():
        serializer = NoteSerializer(note)
        return Response(serializer.data)
    return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

# Create your views here.


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_note(request, id):
    try:
        note = Note.objects.get(pk=id)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user == note.owner:
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def share_note(request, id):
    try:
        note = Note.objects.get(pk=id)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the authenticated user is the owner of the note
    if request.user != note.owner:
        return Response({'error': 'You are not the owner of this note'}, status=status.HTTP_403_FORBIDDEN)

    # Get the list of users to share the note with from the request data
    users_to_share_with = request.data.get('users', [])

    # Validate that all users exist
    users_not_found = []
    for user_id in users_to_share_with:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            users_not_found.append(user_id)

    if users_not_found:
        return Response({'error': f'Users with IDs {users_not_found} not found'}, status=status.HTTP_404_NOT_FOUND)

    # Add the users to the shared_with field of the note
    note.shared_with.add(*users_to_share_with)

    return Response({'message': 'Note shared successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_note_version_history(request, id):
    try:
        note_history = NoteVersionHistory.objects.filter(note_id=id)
        serializer = NoteVersionHistorySerializer(note_history, many=True)
        return Response(serializer.data)
    except NoteVersionHistory.DoesNotExist:
        return Response({'error': 'Note version history not found'}, status=status.HTTP_404_NOT_FOUND)
