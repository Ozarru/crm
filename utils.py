from hashids import Hashids
from django.conf import settings
from django.core.paginator import Paginator


# custom ID hasher ------------------------------
hashids = Hashids(settings.HASHIDS_SALT, min_length=8)


def h_encode(id):
    return hashids.encode(id)


def h_decode(h):
    z = hashids.decode(h)
    if z:
        return z[0]


class HashIdConverter:
    regex = '[a-zA-Z0-9]{8,}'

    def to_python(self, value):
        return h_decode(value)

    def to_url(self, value):
        return h_encode(value)


# custom paginator ------------------------------
def paginate_objects(req, obj_table, obj_count=12):
    p = Paginator(obj_table, obj_count)
    page = req.GET.get('page')
    objects = p.get_page(page)
    return objects


