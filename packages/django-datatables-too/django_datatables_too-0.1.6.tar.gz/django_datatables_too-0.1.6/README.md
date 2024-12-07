# Django DataTables Too

Author:Tim Santor <tsantor@xstudios.agency>

## Overview

Handle server side processing for datatables 1.10.x.

## Getting It

To install Django DataTables Too, just use pip:

    $ pip install django-datatables-too

## Usage

### views.py

    from django.http import JsonResponse
    from django.views.generic import View
    from django_datatables_too.mixins import DataTableMixin

    class DataTablesAjaxPagination(DataTableMixin, View):
        model = Report
        queryset = Report.objects.all()

        def _get_actions(self, obj):
            """Get action buttons w/links."""
            return f'<a href="{obj.get_update_url()}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-pencil"></i></a> <a data-title="{obj}" title="Delete" href="{obj.get_delete_url()}" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash"></i></a>'

        def filter_queryset(self, qs):
            """Return the list of items for this view."""
            # If a search term, filter the query
            if self.search:
                return qs.filter(
                    Q(number__icontains=self.search) |
                    Q(title__icontains=self.search) |
                    Q(state__icontains=self.search) |
                    Q(year__icontains=self.search)
                )
            return qs

        def prepare_results(self, qs):
            # Create row data for datatables
            data = []
            for o in qs:
                data.append({
                    'number': o.number,
                    'title': Truncator(o.title).words(10),
                    'state': o.state,
                    'year': o.year,
                    'published': o.published,
                    'modified': o.modified,
                    'actions': self._get_actions(o)
                })
            return data

        def get(self, request, *args, **kwargs):
            context_data = self.get_context_data(request)
            return JsonResponse(context_data)

### urls.py

    from django.urls import path

    from . import views

    app_name = 'reports'

    urlpatterns = [

        ...

        path('ajax',
            views.DataTablesAjaxPagination.as_view(), name='report-list-ajax'),

    ]

### report_list.html

    $('#report-table').DataTable({
        columnDefs: [{
            orderable: true,
            targets: -1
        }, ],

        // Ajax for pagination
        processing: true,
        serverSide: true,
        ajax: {
            url: '{% url "reports:report-list-ajax" %}',
            type: 'get',
        },
        columns: [
            // data: json key from prepare_results, name: model field name
            { data: 'number', name: 'number'},
            { data: 'title', name: 'title' },
            { data: 'state', name: 'state' },
            { data: 'year', name: 'year' },
            { data: 'published', name: 'published' },
            { data: 'modified', name: 'modified' },
            { data: 'actions', name: 'actions' }
        ]

    });

## Local Development

```bash
make env
make pip_install
make migrations
make migrate
make superuser
make serve
```

or simply `make from_scratch`

- Visit `http://127.0.0.1:8000/admin/` for the Django Admin

### Testing

```bash
make pytest
make coverage
make open_coverage
```
