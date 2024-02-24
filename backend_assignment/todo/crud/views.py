from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from .models import ToDo
from .serializers import ToDoSerializer


class AddToDoView(APIView):
    """
    add a new ToDo
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ToDoSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ToDoListView(generics.ListAPIView):
    """
    list all ToDos for the authenticated user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ToDoSerializer

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)
    

class RetrieveToDoView(APIView):
    """
    retrieve details of a ToDo object
    """

    def get(self, request, todo_id):
        try:
            todo = ToDo.objects.get(id=todo_id)
            serializer = ToDoSerializer(todo, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ToDo.DoesNotExist:
            return Response({"error": "ToDo does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        

class UpdateToDoView(APIView):
    """
    update a ToDo object
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, todo_id):
        try:
            todo = ToDo.objects.get(id=todo_id)
            serializer = ToDoSerializer(todo, data=request.data, context={"request": request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ToDo.DoesNotExist:
            return Response({"error": "ToDo does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        

class MarkToDoAsCompletedView(APIView):
    """
    mark a ToDo as completed
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, todo_id):
        try:
            todo = ToDo.objects.get(id=todo_id)
            todo.completed = True
            todo.save()
            return Response(ToDoSerializer(todo, context={"request": request}).data, status=status.HTTP_200_OK)
        except ToDo.DoesNotExist:
            return Response({"error": "ToDo does not exist!"}, status=status.HTTP_404_NOT_FOUND)


class DeleteToDoView(APIView):
    """
    delete a ToDo object
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, todo_id):
        try:
            todo = ToDo.objects.get(id=todo_id)
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ToDo.DoesNotExist:
            return Response({"error": "ToDo does not exist!"}, status=status.HTTP_404_NOT_FOUND)