import logging

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.http import JsonResponse
from querystring_parser import parser

logger = logging.getLogger(__name__)


class DataTableMixin:
    """
    Create JSON response suitable for datatables ajax pagination.
    https://datatables.net/manual/server-side
    """

    model = None
    queryset = None

    @property
    def _querydict(self):
        """Return the request method query dict."""
        # Can't parse multidimensional array query params without a 3rd party?
        return parser.parse(self.request.META["QUERY_STRING"])

    @property
    def draw(self):
        """Draw counter. This is used by DataTables to ensure that the Ajax
        returns from server-side processing requests are drawn in sequence by
        DataTables (Ajax requests are asynchronous and thus can return out of
        sequence)."""
        return int(self._querydict.get("draw", 0))

    @property
    def start(self):
        """Paging first record indicator. This is the start point in the
        current data set (0 index based - i.e. 0 is the first record)."""
        return int(self._querydict.get("start", 0))

    @property
    def length(self):
        """Number of records that the table can display in the current draw."""
        return int(self._querydict.get("length", 25))

    @property
    def search(self):
        """Global search value. To be applied to all columns which have
        searchable as true."""
        if "search" in self._querydict:
            # self._querydict["search"].get("regex")
            return self._querydict["search"].get("value")
        return None

    @property
    def columns(self):
        """Get column information"""
        return self._querydict.get("columns")

    @property
    def order(self):
        """Columns to which ordering should be applied."""
        return self._querydict.get("order", [])

    def col_data(self, column_num):
        """Get column data"""
        return self.columns[column_num]["data"]

    def col_name(self, column_num):
        """Get column name"""
        return self.columns[column_num]["name"]

    def col_searchable(self, column_num):
        """Get column searchable boolean"""
        return self.columns[column_num]["searchable"]

    def col_orderable(self, column_num):
        """Get column orderable boolean"""
        return self.columns[column_num]["orderable"]

    def col_search(self, column_num):
        """Get column search"""
        return self.columns[column_num]["search"]["value"]

    def col_search_regex(self, column_num):
        """Get column search regex boolean"""
        return self.columns[column_num]["search"]["regex"]

    def build_order_by(self, key):
        """Build order_by string"""
        direction = "" if self.order[key]["dir"] == "asc" else "-"
        col_num = int(self.order[key]["column"])
        col_name = self.col_name(col_num)
        return f"{direction}{col_name}"

    @property
    def page(self):
        """Current page."""
        return int(self.start / self.length + 1) if self.start > 1 else 1

    def get_ordering(self, qs):
        """Return the queryset with ordering."""
        ordering = []
        for key in self.order:
            order_by = self.build_order_by(key)
            ordering.append(order_by)
            qs = qs.order_by(order_by)
        # logger.info(f"Ordering: {ordering}")
        return qs

    def filter_queryset(self, qs):
        """
        Override with custom search logic.

        Example:
        ```
        if self.search:
            return qs.filter(
                Q(field1__icontains=self.search) |
                Q(field2__icontains=self.search) |
                Q(field3__icontains=self.search) |
                Q(field4__icontains=self.search)
            )
        return qs
        ```
        """
        raise NotImplementedError  # pragma: no cover

    def get_queryset(self):
        """Get queryset."""
        qs = self.queryset or self.model.objects.all()
        if not qs.ordered:
            qs = qs.order_by("pk")
        return qs

    def get_paging(self, qs):
        """Get paging."""
        paginator = Paginator(qs, self.length)
        try:
            object_list = paginator.page(self.page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        return object_list

    def prepare_results(self, qs) -> list:
        """Override this method."""
        raise NotImplementedError  # pragma: no cover

    def handle_exception(self, e):
        """Handle exceptions."""
        logger.exception(str(e))
        raise e

    def get_context_data(self, request):
        """Get object list."""
        try:
            self.request = request

            # Get queryset
            qs = self.get_queryset()

            # Number of records (before filtering)
            records_total = qs.count()

            # Apply filters
            qs = self.filter_queryset(qs)

            # Number of records (after filtering)
            records_filtered = qs.count()

            # Apply ordering
            qs = self.get_ordering(qs)

            # Apply pagintion
            qs = self.get_paging(qs)

            # Prepare output data
            data = self.prepare_results(qs)

            return {
                "draw": self.draw,
                "recordsTotal": records_total,
                "recordsFiltered": records_filtered,
                "data": data,
            }
        except Exception as e:  # noqa: BLE001
            return self.handle_exception(e)

    def get(self, request, *args, **kwargs):
        """Handle GET request."""
        context_data = self.get_context_data(request)
        resp = JsonResponse(context_data)
        # Inject headers
        resp["Cache-Control"] = "no-store"
        return resp
