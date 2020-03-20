import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .pagination import CustomCoursePaginator

from .serializers import LogSerializer, GetLogSerializer

from .models import Log


class LogView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request):

        logs = Log.objects.all()

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            logs = logs.filter(userId=user_id)

        action_type = self.request.query_params.get('action_type', None)
        if action_type is not None:
            logs = logs.filter(actionType=action_type)

        start_date = self.request.query_params.get('start_date', None)
        if start_date is not None:
            logs = logs.filter(actionTime__date__gte=start_date)

        end_date = self.request.query_params.get('end_date', None)
        if end_date is not None:
            logs = logs.filter(actionTime__date__lte=end_date)

        paginator = CustomCoursePaginator()
        result_page = paginator.paginate_queryset(logs, request)
        serializer = GetLogSerializer(result_page, many=True)
        data = paginator.get_paginated_response(serializer.data)
        return Response({'data': data}, 200)

    def post(self, request):
        
        request_data = request.data

        data_list = []
        for x in request_data:
            

            user_id = x['userId']
            session_id = x['sessionId']

            for y in x['actions']:
                action_time = y['time']
                action_type = y['type']
                action_properties = y['properties']
                
                data_list.append({
                    'userId' : user_id,
                    'sessionId' : session_id,
                    'actionTime' : action_time,
                    'actionType' : action_type,
                    'actionProperties' : json.dumps(action_properties)
                })

                # Batch Processing
                if len(data_list) > 50:

                    serializer = LogSerializer(data=data_list, many=True)
                    if serializer.is_valid():
                        serializer.save()
                        data_list = []
                        # return Response({'data': request.data}, 200)

                    else:
                        return Response({'data': serializer.errors}, 200)

            # Batch Processing
            if len(data_list) > 50:

                serializer = LogSerializer(data=data_list, many=True)
                if serializer.is_valid():
                    serializer.save()
                    data_list = []
                    # return Response({'data': request.data}, 200)

                else:
                    return Response({'data': serializer.errors}, 200)

            else:
                continue
        
        if len(data_list) > 0:
            serializer = LogSerializer(data=data_list, many=True)
            if serializer.is_valid():
                serializer.save()
                data_list = []
                return Response({'message': 'Success'}, 200)

            else:
                return Response({'data': serializer.errors}, 200)

        else:
            return Response({'message': 'Success'}, 200)
