#  +---------------------------------------------------------------------------------|
#  | NAME : PHO KHAING                                                               |
#  | EMAIL: khaing.pho@ftb.com.kh                                                    |
#  | DUTY : FTB BANK (HEAD OFFICE)                                                   |
#  | ROLE : Full-Stack Software Developer                                            |
#  +---------------------------------------------------------------------------------|
#  | Released 20.08.2023.                                                            |
#  | Description: This class provides methods for data pagination by search, filter. |
#  +---------------------------------------------------------------------------------+

from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class PaginatorResponse:
    def __init__(
        self,
        queryset,
        request,
        serializer_class,
        search_fields,
        filter_fields,
        page_size=10,
    ):
        self.queryset = queryset
        self.request = request
        self.serializer_class = serializer_class
        self.page_size = page_size
        self.search_fields = search_fields
        self.filter_fields = filter_fields

    def get_paginated_response(self):
        paginator = PageNumberPagination()
        paginator.page_size = self.page_size

        queryset = self.apply_filters_and_ordering(self.queryset)
        paginated_queryset = paginator.paginate_queryset(queryset, self.request)

        serializer = self.serializer_class(paginated_queryset, many=True)

        # Get the default paginated response
        paginated_response = paginator.get_paginated_response(serializer.data)

        # Include additional fields in the response
        paginated_response.data["page"] = paginator.page.number
        paginated_response.data["pages"] = paginator.page.paginator.num_pages

        return paginated_response

    # ----------------------------------------------------------------
    # This method return only results data dics of paginations
    # ----------------------------------------------------------------
    # output: []
    # ----------------------------------------------------------------
    def paginator_results(self):
        paginated_response = self.get_paginated_response()
        return paginated_response.data.get("results")

    def paginator_count(self):
        paginated_response = self.get_paginated_response()
        return paginated_response.data.get("count")

    def paginator_next(self):
        paginated_response = self.get_paginated_response()
        page_number = paginated_response.data.get("page")
        return self.get_page_url(page_number + 1) if page_number > 1 else None

    def paginator_previous(self):
        paginated_response = self.get_paginated_response()
        page_number = paginated_response.data.get("page")
        return self.get_page_url(page_number - 1) if page_number > 1 else None

    # ----------------------------------------------------------------
    # This method return only paginators data dics of paginations
    # ----------------------------------------------------------------
    # output: {
    # "count": int,
    # "page": int,
    # "pages": int,
    # "page_size": int,
    # "next_page": int,
    # "next_page_url": link,
    # "previous_page": int,
    # "previous_page_url": int
    # }
    # ----------------------------------------------------------------
    def api_response_paginators(self):
        paginated_response = self.get_paginated_response()
        page_number = paginated_response.data.get("page")
        total_pages = paginated_response.data.get("pages")

        paginators_context = {
            "count": paginated_response.data.get("count"),
            "page": page_number,
            "pages": total_pages,
            "page_size": self.page_size,
        }

        if page_number < total_pages:
            paginators_context["next_page"] = page_number + 1
            paginators_context["next_page_url"] = self.get_page_url(page_number + 1)
        else:
            paginators_context["next_page"] = None
            paginators_context["next_page_url"] = None

        if page_number > 1:
            paginators_context["previous_page"] = page_number - 1
            paginators_context["previous_page_url"] = self.get_page_url(page_number - 1)
        else:
            paginators_context["previous_page"] = None
            paginators_context["previous_page_url"] = None

        return paginators_context

    # --------------------------------------------------------------------
    # This method return all properties of paginators, results, paginators
    # --------------------------------------------------------------------
    # output: {
    # "results": [],
    # "paginators": {
    # "count": int,
    # "page": int,
    # "pages": int,
    # "page_size": int,
    # "next_page": int,
    # "next_page_url": link,
    # "previous_page": int,
    # "previous_page_url": int
    # }
    # }
    # --------------------------------------------------------------------
    def paginator_full_api_response(self):
        paginated_response = self.get_paginated_response()
        page_number = paginated_response.data.get("page")
        total_pages = paginated_response.data.get("pages")

        api_context = {
            "results": paginated_response.data.get("results"),
            "paginators": {
                "count": paginated_response.data.get("count"),
                "page": page_number,
                "pages": total_pages,
                "page_size": self.page_size,
            },
        }

        if page_number < total_pages:
            api_context["paginators"]["next_page"] = page_number + 1
            api_context["paginators"]["next_page_url"] = self.get_page_url(
                page_number + 1
            )
        else:
            api_context["paginators"]["next_page"] = None
            api_context["paginators"]["next_page_url"] = None

        if page_number > 1:
            api_context["paginators"]["previous_page"] = page_number - 1
            api_context["paginators"]["previous_page_url"] = self.get_page_url(
                page_number - 1
            )
        else:
            api_context["paginators"]["previous_page"] = None
            api_context["paginators"]["previous_page_url"] = None

        return api_context

    def get_page_url(self, page_number):
        base_url = self.request.build_absolute_uri()
        return base_url.replace(
            f'page={self.request.GET.get("page")}', f"page={page_number}"
        )

    def apply_filters_and_ordering(self, queryset):
        search_query = self.request.GET.get("search", "")
        if search_query:
            filter_expression = Q()
            for field_name in self.search_fields:
                if hasattr(field_name, "name"):
                    field_name = field_name.name
                lookup = f"{field_name}__icontains"
                filter_expression |= Q(**{lookup: search_query})
            queryset = queryset.filter(filter_expression)

        for field in self.request.GET:
            if field in self.filter_fields:
                value = self.request.GET.get(field)
                queryset = queryset.filter(**{field: value})

        ordering = self.request.GET.get("ordering")
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
