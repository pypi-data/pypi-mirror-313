```
pip install umkt-service-utility-django
```

# konfigurasi di settings.py
```
    INSTALLED_APPS = [
        'umkt_service_utils',
        'rest_framework'
    ]

    REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
            # 'umkt_service_utils.permissions.IsAuthenticatedOrReadOnlyUMKT'
        ),
        'DEFAULT_PAGINATION_CLASS': 'umkt_service_utils.pagination.UMKTPagination',
    }

    # tambahkan ini pada file urls.py
    path('utils/', include('umkt_service_utils.urls')),
```


# konfigurasi .env
```
    # ini untuk akses api groups
    UTI = ['hs048','shs500','shw929','hendras']
```

# cek token di setiap function
```
    # setiap function tambah property @auth_check

    from umkt_service_utils.auth_middleware import auth_check

    @auth_check
    def index(request):
        pass
```

# list API
```
# groups
    - list  : http://localhost:8000/utils/group (GET, POST)
    - detil : http://localhost:8000/utils/group/Pegawai (GET, PUT, DELETE)
# users
    - list  : http://localhost:8000/utils/user (GET)
    - detil : http://localhost:8000/utils/user/hendras (GET, PUT)

```
