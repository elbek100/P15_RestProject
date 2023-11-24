import datetime

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from accounts.permission import AdminPermission
from main.models import Todo, Category
from .serializers import TodoSerializer, CategorySerializer, QuerySerializer, TodoSerializerForFilter


class TodoApiView(GenericAPIView):
    serializer_class = TodoSerializer

    def get(self, request):
        todos = Todo.objects.all()
        todos_data = TodoSerializer(todos, many=True)
        return Response(todos_data.data)


class CreateTodoAPIView(GenericAPIView):
    permission_classes = (AdminPermission,)
    serializer_class = TodoSerializer

    def post(self, request, ):
        todo_serializer = TodoSerializer(data=request.data)
        todo_serializer.is_valid(raise_exception=True)
        todo_serializer.save()
        return Response(todo_serializer.data)


class TodoUpdateAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TodoSerializer

    def put(self, request, pk):
        title = request.POST.get('title')
        description = request.POST.get('description')
        todo = Todo.objects.get(pk=pk)
        todo.title = title
        todo.description = description
        todo.save()
        todo_serializer = TodoSerializer(todo)
        return Response(todo_serializer.data)

    def patch(self, request, pk):
        title = request.POST.get('title', None)
        description = request.POST.get('description', None)
        todo = Todo.objects.get(pk=pk)
        if title:
            todo.title = title
        if description:
            todo.description = description
        todo.save()
        todo_serializer = TodoSerializer(todo)
        return Response(todo_serializer.data)

    def delete(self, request, pk):
        Todo.objects.get(pk=pk).delete()
        return Response(status=204)


class TodoSlugAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = TodoSerializer

    def post(self, request, slug):
        try:
            todo = Todo.objects.get(slug=slug)
        except Todo.DoesNotExist:
            return Response({'success': False, 'error': 'Slug is invalid !'}, status=404)
        todos_serializer = TodoSerializer(todo)
        return Response(todos_serializer.data)


class SearchAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = CategorySerializer

    @swagger_auto_schema(query_serializer=QuerySerializer)
    def get(self, request):
        query = request.GET.get('query')
        base_categories = Category.objects.filter(name__icontains=query).values('tree_id')
        categories = Category.objects.filter(tree_id__in=base_categories)
        #category_data = []
        #for category in categories:
        #    cate = Category.objects.filter(tree_id=category.tree_id)
        #    category_serializer = CategorySerializer(cate, many=True)
        #    return Response(category_serializer.data)
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)


class TodoFilterAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = TodoSerializer

    @swagger_auto_schema(query_serializer=TodoSerializerForFilter)
    def get(self, request):
        name = request.GET.get('name', None)
        category_name = request.GET.get('category_name', None)
        start = request.GET.get('start', None)
        end = request.GET.get('end', None)
        date = request.GET.get('date', None)
        color = request.GET.get('color', None)

        todos = None

        if start and end:
            todos = Todo.objects.filter(price__gte=start, price__lte=end)
        if name:
            todos = Todo.objects.filter(title__icontains=name)
        if date:
            todos = Todo.objects.filter(expires_at=date)
        if color:
            todos = Todo.objects.filter(color=color)

        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data)







