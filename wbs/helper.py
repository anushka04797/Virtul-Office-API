import sys

from wbs.serializers import WbsFileSerializer


def wbs_wise_file_insert(request,files):
    try:
        wbs_id = request.data.get('wbs_id')
        upload_by = request.data.get('upload_by')
        files = int(request.data.get('files')) + 1

        for i in range(1, files):
            indexval = str(i)
            attribute_name = str('file' + indexval)
            file = request.data.get(attribute_name)
            requested_data = {"wbs_id": wbs_id, "file": file, "upload_by": upload_by}
            serializer = WbsFileSerializer(data=requested_data)
            if serializer.is_valid():
                serializer.save()
            else:
                serializer.errors()

        return serializer.data

    except Exception as e:
        return 'on line {}'.format(sys.exc_info()[-1].tb_lineno)
