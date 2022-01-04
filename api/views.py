from django.shortcuts import render
from rest_framework.reverse import reverse
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import TaskSerializer, UserSerializer, UserCreateSerializer
from .models import Task

from django.http import Http404
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.db.models import Q

from .pagination import SetPagination

# Create your views here.
@api_view(['GET'])
def apiOverview(request , format=None):

    return Response({
        'users': reverse('api-userlist', request=request, format=format),
        'tasks': reverse('api-tasklist', request=request, format=format)
    })


"""
serializing using generic based view
"""



class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = "you must be the owner of this task"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user

class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'id', 'completed']
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    pagination_class = SetPagination
    
    def get_queryset(self, *args, **kwargs):
        queryset = Task.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(

                Q(id__icontains=query)|
                 Q(title__icontains=query)|
                  Q(completed__icontains=query)
            ).distinct()
        return queryset
    
 
     



class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    



class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    



"""
serializing using class based view
"""

#class TaskList(APIView):
 #   """
  #  List all task and creates new task.
   # """
#    def get(self, request, format=None):
#        tasks = Task.objects.all()
#        serializer = TaskSerializer(tasks, many=True)
#        return Response(serializer.data)

#    def post(self, request, format=None):
#        serializer = TaskSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class TaskDetail(APIView):
#"""
 #   Retrieve, update or delete a task.
 #   """
#    def get_object(self, pk):
#        try:
#            return Task.objects.get(pk=pk)
#        except Task.DoesNotExist:
#            raise Http404

#    def get(self, request, pk, format=None):
#        tasks = self.get_object(pk)
#        serializer = TaskSerializer(tasks)
#        return Response(serializer.data)

#    def put(self, request, pk, format=None):
#        tasks = self.get_object(pk)
#       if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    def delete(self, request, pk, format=None):
#        tasks = self.get_object(pk)
#        tasks.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)





""" 
serializing using fucntions
"""
#@permission_classes([IsAuthennticated])
#@api_view(['GET'])
#def tasklist(request):
#    tasks = Task.objects.all()
#    serializer = TaskSerializer(tasks, many=True)
#    
#    return Response(serializer.data)

#@api_view(['GET'])
#def taskdetail(request, pk):
#    tasks = Task.objects.get(id=pk)
#   serializer = TaskSerializer(tasks, many=False)
    
#    return Response(serializer.data)




#@api_view(['POST'])
#def taskcreate(request):
  
#    serializer = TaskSerializer(data=request.data)
#    if serializer.is_valid():
#            serializer.save()
    
#            return Response(serializer.data, status=status.HTTP_201_CREATED)

#   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@api_view(['POST'])
#def taskupdate(request, pk):
#    tasks = Task.objects.get(id=pk)
#    serializer = TaskSerializer(data=request.data)
#    if serializer.is_valid():
#            serializer.save()
    
#            return Response(serializer.data, status=status.HTTP_201_CREATED)

#    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#@api_view(['DELETE'])
#def taskdelete(request, pk):
#    tasks = Task.objects.get(id=pk)
#    tasks.delete()
    