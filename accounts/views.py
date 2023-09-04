from logging.config import valid_ident
from typing import List
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from accounts.models import ValorantAccount

from accounts.serializers import AccountSerializer, ValorantSerializer
from collections import OrderedDict


# all endpoints


# view to create a new account
class CreateAccountView(CreateAPIView):
    serializer_class = AccountSerializer


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, **kwargs):
        request.user.delete()
        return Response({'detail': "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# view to update an account
class UpdateAccountView(UpdateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class AccountView(APIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = {'username': request.user.username, 'first_name': request.user.first_name,
                    'last_name': request.user.last_name, 'email': request.user.email}

        if request.user.avatar:
            response['avatar'] = str(request.path).replace('accounts/profile/', 'media/') + str(request.user.avatar)

        return JsonResponse({"user": response})


class ValorantAccountList(ListAPIView):
    query_set = ValorantAccount.objects.all()
    serializer_class = ValorantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ValorantAccount.objects.all().filter(owner=self.request.user)

class ValorantAdminAccountList(ListAPIView):
    query_set = ValorantAccount.objects.all()
    serializer_class = ValorantSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ValorantAccount.objects.all()



class ValorantAccountSearch(ListAPIView):
    serializer_class = ValorantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = []
        search_string = ''
        try:
            if self.kwargs['rank']:
                search_string = self.kwargs['rank']
            else:
                search_string = None
        except:
            pass
       
        if search_string is not None:
            search_string = search_string.replace('%20', ' ').lower()
            queryset = ValorantAccount.objects.all().filter(rank__icontains=search_string)
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ValorantAccountCreate(CreateAPIView):
    serializer_class = ValorantSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        val_acc = self.create(request, *args, **kwargs)
        acc = ValorantAccount.objects.get(pk=val_acc.data['id'])
        self.request.user.valorant_accounts.add(acc)
        self.request.user.save()

        return val_acc


class ValorantAccountDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, **kwargs):
        print(kwargs['id'])
        acc = get_object_or_404(ValorantAccount, id=kwargs['id'])
        if acc.owner == request.user:
            name = acc.username
            acc.owner.valorant_accounts.remove(acc)
            acc.delete()
            return Response({'detail': f"{name} Account Deleted"}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied()


class ValorantAccountUpdate(UpdateAPIView):
    serializer_class = ValorantSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        acc = get_object_or_404(ValorantAccount, id=self.kwargs['id'])
        if acc.owner == self.request.user:
            return acc
        else:
            raise PermissionDenied()