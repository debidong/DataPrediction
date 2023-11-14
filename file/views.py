from rest_framework.views import APIView, Response, status
import os
import pandas as pd
import datetime

from .storage import is_allowed_file, is_duplicate_name, UPLOAD_FOLDER
from .models import File

class TableView(APIView):
    def post(self, request):
        '''查询数据库中全部的文件
        '''
        files = File.objects.all()
        res = {
            "message": "查询成功",
            "content": {
                "columns": [
                    {
                        "name": "时空数据",
                        "value": "dataName"
                    },
                    {
                        "name": "数据集描述",
                        "value": "dataDescription",
                        "tooltip": True
                    },
                    {
                        "name": "行数",
                        "value": "rowCount"
                    },
                    {
                    "name": "字段数",
                        "value": "fieldCount"
                    },
                    {
                        "name": "创建时间",
                        "value": "creationTime"
                    },
                    {
                        "name": "操作",
                        "value": "operation",
                        "slot": True
                    }
                    ],
                "data": [],
                "componentTitle": "",
                "pageTotal": 1
            }
        }
        for file in files:
            res["content"]["data"].append({
                "id": file.hash,
                "dataName": file.name,
                "dataDescription": file.description,
                "rowCount": file.row,
                "fieldCount": file.column,
                "creationTime": file.created.strftime('%Y-%m-%d %H:%M:%S')
            })
        return Response(res, status=status.HTTP_200_OK)


class FileView(APIView):
    def post(self, request):
        """文件上传
        """

        file = request.FILES['file']
        if not (file and is_allowed_file(file.name)):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if is_duplicate_name(file.name):
            res = {
                "message": "存在重复文件",
                "content": False
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        path = UPLOAD_FOLDER+"/"+file.name
        with open(path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        dumped_file = pd.read_csv(path)      
        row, column = dumped_file.shape

        File.objects.create(
            path=path,
            description="test",
            name=file.name,
            row=row,
            column=column,
            created=datetime.datetime.now()
        ).save()

        res = {
            "message": "查询成功",
            "content": True
        }
        return Response(res, status=status.HTTP_200_OK)
    
    def put(self, request):
        pass

    def delete(self, request):
        pass