from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from api.utils.common_utils import api_success, api_failure, get_page_count
from store.models import Store


@csrf_exempt
@require_http_methods(["GET"])
def get_list(request):
    """
    Get a list of records
    curl --request GET 'http://127.0.0.1:8080/api/store/get_list'
    """
    page_index = int(request.GET.get('pageIndex', 0))
    row_count_per_page = int(request.GET.get('rowCountPerPage', 5))
    offset = page_index * row_count_per_page
    end_index = offset + row_count_per_page
    # Get rows
    qs = Store.objects.filter(is_active=1, is_del=0)
    rows = qs.order_by('-mtime', '-pk')[offset:end_index].values('id', 'name', 'address', 'ctime', 'mtime')
    rows = list(rows)
    # Get row count
    row_count = qs.count()
    # Get page count
    page_count = get_page_count(row_count, row_count_per_page)
    output = {
        'page_index': page_index,
        'page_count': page_count,
        'row_count': row_count,
        'row_count_per_page': row_count_per_page,
        'offset': offset,
        'end_index': end_index,
        'rows': rows,
        # 'sql': str(qs.query)
    }
    return api_success(d=output)


@csrf_exempt
@require_http_methods(["GET"])
def get_detail(request):
    """
    Get one record
    curl --request GET 'http://127.0.0.1:8080/api/store/get_detail?id=1'
    """
    try:
        pk = request.GET.get('id', None)
        if not pk:
            raise Exception('Invalid id')

        qs = Store.objects.filter(pk=pk, is_active=1, is_del=0).values('name', 'address', 'ctime', 'mtime')
        if not qs:
            raise Exception('Failed to find data')
        return api_success(d=qs[0])
    except Exception as e:
        return api_failure(m=e.args[0])


@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    """
    Create a record
    curl -X POST 'http://127.0.0.1:8080/api/store/create' -F 'name=大岗镇' -F 'address=广州市南沙区'
    curl -X POST 'http://127.0.0.1:8080/api/store/create' -d 'name=大岗镇&address=广州市南沙区'
    """
    try:
        name = request.POST.get('name', '').strip()
        address = request.POST.get('address', '').strip()
        if not name or not address:
            raise Exception('Invalid parameters')
        created_obj = Store.objects.create(name=name, address=address)
        if created_obj and created_obj.pk:
            return api_success(m='Created successfully', d={"id": created_obj.pk})
        raise Exception('Failed to create')
    except Exception as e:
        return api_failure(m=e.args[0])


@csrf_exempt
@require_http_methods(["POST"])
def update(request):
    """
    Update fields of a record
    curl -X POST 'http://127.0.0.1:8080/api/store/update' -d 'id=38&name=万顷沙&address=广州市南沙区'
    """
    try:
        pk = request.POST.get('id', None)
        name = request.POST.get('name', '').strip()
        address = request.POST.get('address', '').strip()
        if not pk:
            raise Exception('Invalid id')
        if not name or not address:
            raise Exception('Invalid parameters')

        qs = Store.objects.filter(pk=pk, is_active=1, is_del=0)
        if not qs:
            raise Exception('Failed to find data')
        # store_obj = qs[0]
        store_obj = qs.get()
        store_obj.name = name
        store_obj.address = address
        store_obj.save()
        # qs.update()
        return api_success(m='Updated successfully')
    except Exception as e:
        return api_failure(m=e.args[0])


@csrf_exempt
@require_http_methods(["POST"])
def delete(request):
    """
    soft delete a record
    curl -X POST 'http://127.0.0.1:8080/api/store/delete' -d 'id=38'
    """
    try:
        pk = request.POST.get('id', None)
        if not pk:
            raise Exception('Invalid id')

        qs = Store.objects.filter(pk=pk, is_active=1, is_del=0)
        if not qs:
            raise Exception('Failed to find data')
        # store_obj = qs[0]
        store_obj = qs.get()
        store_obj.is_del = 1
        store_obj.save()
        # qs.update()
        return api_success(m='Deleted successfully')
    except Exception as e:
        return api_failure(m=e.args[0])

