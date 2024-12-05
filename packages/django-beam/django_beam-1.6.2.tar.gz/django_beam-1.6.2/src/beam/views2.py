from typing import Any
from .viewsets import ViewSet
from django.shortcuts import render


class ResponseReady(Exception):
    pass


class Person:
    pass


class DeleteAction:
    pass


def process_list(request, config):
    qs = config.process_queryset()

    if request.POST:
        for action in config.action_classes:
            result = action.handle(request, qs)
            if result:
                raise ResponseReady(result)

    return {
        "config": config,
        "queryset": qs,
    }


def process_detail(request, config, pk):
    pass


def process_create(request, config):
    form = config.form
    formsets = config.formsets

    obj = None

    if form.is_valid() and all(f.is_valid() for f in formsets):
        obj = form.save()
        for f in formsets:
            f.save()

    return {"obj": obj, "form": form, "formsets": formsets}


class person_config:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, view) -> Any:
        self.view = view

    model = Person
    sort_fields = ["first_name", "last_name", "date_joined"]
    search_fields = ["first_name", "last_name"]
    fields = ["first_name", "last_name", "date_joined", "is_active"]
    paginate_by = 20
    action_classes = [DeleteAction]
    filterset_fields = ["date_joined"]


@person_config("list")
def person_list_view(request):
    context = process_list(request, request.config)
    return render(request, "beam/list.html", context)


@person_config("detail")
def person_detail_view(request, pk):
    context = process_detail(request, request.config, pk)
    return render(request, "beam/detail.html", context)


@person_config("create")
def person_create_view(request):
    context = process_create(request, request.config)
    return render(request, "beam/create.html", context)


# Why do we want to have the viewsets in a registry?
# - we want to know what kind of links to add?
# - we want to know permissions?


class PersonViewSet(ViewSet):
    model = Person

    list_sort_fields = ["first_name", "last_name", "date_joined"]
    list_search_fields = ["first_name", "last_name"]
    list_fields = ["first_name", "last_name", "date_joined", "is_active"]
    list_paginate_by = 20
    list_action_classes = [DeleteAction]
    list_filterset_fields = ["date_joined"]


# These are what we want
#    list_component = ListComponent
#    list_view_class = ListView
#    list_url = ""
#    list_url_name: str
#    list_url_kwargs: UrlKwargDict = {}
#    list_verbose_name = _("list")
#
#    list_sort_fields: List[str]
#    list_sort_fields_columns: Mapping[str, str]
#    list_search_fields: List[str] = []
#    list_paginate_by = 25
#    list_item_link_layout = ["update", "detail"]
#
#    list_model: Model
#    list_fields: List[str]
#    list_layout: LayoutType
#    list_queryset: QuerySet
#    list_inline_classes: List[Type[RelatedInline]]
#    list_form_class: ModelForm
#    list_permission = "{app_label}.view_{model_name}"
#    list_filterset_fields: List[str] = []
#    list_filterset_class: Optional[Type[django_filters.FilterSet]] = None
#    list_action_classes: List[Type[Action]] = []
#    list_link_layout = ["create"]
