from api.utils.common_utils import get_page_count


def get_row_object(target_class, **kwargs):
    queryset = getattr(target_class, 'objects').filter(**kwargs)
    # 打印出sql: str(queryset.query)
    if queryset:
        return queryset[0]
    return None


def get_row_dict(target_class, **kwargs):
    queryset = getattr(target_class, 'objects').filter(**kwargs)
    # print the sql: str(queryset.query)
    if queryset:
        rows = list(queryset.values())
        return rows[0]
    return {}


def get_row_list(**kwargs):
    page_index = kwargs['page_index']
    row_count_per_page = kwargs['page_size']
    offset = page_index * row_count_per_page
    end_index = offset + row_count_per_page
    qs = getattr(kwargs['target_class'], 'objects').filter(**kwargs['where'])
    rows = qs.order_by('-mtime')[offset:end_index].values()
    rows = list(rows)
    row_count = qs.count()
    page_count = get_page_count(row_count, row_count_per_page)
    return {
        'page_index': page_index,
        'page_count': page_count,
        'row_count': row_count,
        'row_count_per_page': row_count_per_page,
        'offset': offset,
        'end_index': end_index,
        'rows': rows,
    }
