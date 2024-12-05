from neapolitan.views import Role
from django.urls import NoReverseMatch, path, reverse
from django.utils.decorators import classonlymethod
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from django.template.response import TemplateResponse

from django.conf import settings
from django.db.models.fields.reverse_related import ManyToOneRel

import logging
log = logging.getLogger("nominopolitan")


class NominopolitanMixin:
    namespace = None
    create_form_class = None
    templates_path = "nominopolitan" # path to overridden set of templates
    base_template_path = "nominopolitan/base.html" # location of template

    use_crispy = None # True = use crispy-forms if installed; False otherwise.

    properties = []
    detail_fields = []
    detail_properties = []

    use_htmx = None
    use_modal = None

    def _get_all_fields(self):
        fields = [field.name for field in self.model._meta.get_fields()]
            
        # Exclude reverse relations
        fields = [
            field.name for field in self.model._meta.get_fields()
            if not isinstance(field, ManyToOneRel)
        ]
        return fields
    
    def _get_all_properties(self):
        return [name for name in dir(self.model)
                    if isinstance(getattr(self.model, name), property) and name != 'pk'
                ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.fields or self.fields == 'all':
            # set to all fields in model
            self.fields = self._get_all_fields()
        elif type(self.fields) == list:
            # check all are valid fields
            all_fields = self._get_all_fields()
            log.debug(f"All fields: {all_fields}")
            for field in self.fields:
                log.debug(f"Checking field {field}")
                if field not in all_fields:
                    raise ValueError(f"Field {field} not defined in {self.model.__name__}")
        elif type(self.fields) != list:
            raise TypeError("fields must be a list")        
        else:
            raise ValueError("fields must be 'all', a list of valid fields or not defined")
        
        if self.properties:
            if self.properties == 'all':
                # Set self.properties to a list of every property in self.model
                self.properties = self._get_all_properties()
            elif type(self.properties) == list:
                # check all are valid properties
                all_properties = self._get_all_properties()
                for prop in self.properties:
                    if prop not in all_properties:
                        raise ValueError(f"Property {prop} not defined in {self.model.__name__}")
            elif type(self.properties) != list:
                raise TypeError("properties must be a list")
            
        if self.detail_properties:
            if self.detail_properties == 'all':
                # Set self.detail_properties to a list of every property in self.model
                self.detail_properties = self._get_all_properties()
            elif self.detail_properties == 'properties':
                # Set self.detail_properties to a list of every property in self.model
                self.detail_properties = self.properties
            elif type(self.detail_properties) == list:
                # check all are valid properties
                all_properties = self._get_all_properties()
                for prop in self.detail_properties:
                    if prop not in all_properties:
                        raise ValueError(f"Property {prop} not defined in {self.model.__name__}")
            elif type(self.detail_properties) != list:
                raise TypeError("detail_properties must be a list or 'all' or 'properties'")


        if self.detail_fields == 'all':
            # Set self.detail_fields to a list of every field in self.model
            self.detail_fields = self._get_all_fields()        
        elif not self.detail_fields or self.detail_fields == 'fields':
            # Set self.detail_fields to self.fields
            self.detail_fields = self.fields
        elif type(self.detail_fields) == list:
            # check all are valid fields
            all_fields = self._get_all_fields()
            for field in self.detail_fields:
                if field not in all_fields:
                    raise ValueError(f"detail_field {field} not defined in {self.model.__name__}")
        elif type(self.detail_fields) != list:
            raise TypeError("detail_fields must be a list or 'all' or 'fields' or a list of fields")
        
    def get_session_key(self):
        return f"nominopolitan_list_target_{self.url_base}"

    def get_original_target(self):
        return self.request.session.get(self.get_session_key(), None)

    def get_use_htmx(self):
        # return True if it was set to be True, and False otherwise
        return self.use_htmx is True

    def get_use_modal(self):
        # must be using htmx for this to work
        return self.use_modal is True and self.get_use_htmx()

    def get_htmx_target(self):

        # only if using htmx
        if not self.get_use_htmx():
            htmx_target = None
        elif self.use_modal:
            htmx_target = "#nominopolitanModalContent"
        elif hasattr(self.request, 'htmx') and self.request.htmx.target:
            # return the target of the original list request
            htmx_target = f"#{self.request.htmx.target}"
        else:
            htmx_target = None  # Default target for non-HTMX requests

        return htmx_target

    def get_use_crispy(self):
        # check if attribute was set
        use_crispy_set = self.use_crispy is not None
        # check if crispy_forms is installed
        crispy_installed = "crispy_forms" in settings.INSTALLED_APPS

        if use_crispy_set:
            if self.use_crispy is True and not crispy_installed:
                log.warning("use_crispy is set to True, but crispy_forms is not installed. Forcing to False.")
                return False
            return self.use_crispy
        # user did not set attribute. Return True if crispy_forms is installed else False
        return crispy_installed

    @staticmethod
    def get_url(role, view_cls):
        return path(
            role.url_pattern(view_cls),
            view_cls.as_view(role=role),
            name=f"{view_cls.url_base}-{role.url_name_component}",
        )

    @classonlymethod
    def get_urls(cls, roles=None):
        if roles is None:
            roles = iter(Role)
        return [NominopolitanMixin.get_url(role, cls) for role in roles]

    def reverse(self, role, view, object=None):
        url_name = (
            f"{view.namespace}:{view.url_base}-{role.url_name_component}"
            if view.namespace
            else f"{view.url_base}-{role.url_name_component}"
        )
        url_kwarg = view.lookup_url_kwarg or view.lookup_field

        match role:
            case Role.LIST | Role.CREATE:
                return reverse(url_name)
            case _:
                if object is None:
                    raise ValueError("Object required for detail, update, and delete URLs")
                return reverse(
                    url_name,
                    kwargs={url_kwarg: getattr(object, view.lookup_field)},
                )

    def maybe_reverse(self, view, object=None):
        try:
            return self.reverse(view, object)
        except NoReverseMatch:
            return None

    def get_form_class(self):
        if self.create_form_class and self.role is Role.CREATE:
            return self.create_form_class
        return super().get_form_class()

    def get_prefix(self):
        return f"{self.namespace}:{self.url_base}" if self.namespace else self.url_base

    def safe_reverse(self, viewname, kwargs=None):
        """Attempt to reverse a URL, returning None if it fails."""
        try:
            return reverse(viewname, kwargs=kwargs)
        except NoReverseMatch:
            return None

    def get_template_names(self):
        if self.template_name is not None:
            return [self.template_name]

        if self.model is not None and self.template_name_suffix is not None:
            names = [
                f"{self.model._meta.app_label}/"
                f"{self.model._meta.object_name.lower()}"
                f"{self.template_name_suffix}.html",
                f"{self.templates_path}/object{self.template_name_suffix}.html",
            ]
            return names
        msg = (
            "'%s' must either define 'template_name' or 'model' and "
            "'template_name_suffix', or override 'get_template_names()'"
        )
        raise ImproperlyConfigured(msg % self.__class__.__name__)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Override the create_view_url to use our namespaced reverse
        view_name = f"{self.get_prefix()}-create"
        context["create_view_url"] = self.safe_reverse(view_name)

        if self.object:
            update_view_name = f"{self.get_prefix()}-update"
            context["update_view_url"] = self.safe_reverse(update_view_name, kwargs={"pk": self.object.pk})

        # to be used in partials to update the header title
        context["header_title"] = f"{self.url_base.title()}-{self.role.value.title()}"

        # set base_template_path
        context["base_template_path"] = self.base_template_path

        # set use_crispy for templates
        context["use_crispy"] = self.get_use_crispy()

        # set use_htmx for templates
        context["use_htmx"] = self.get_use_htmx()

        # set use_modal for templates
        context['use_modal'] = self.get_use_modal()

        context["original_target"] = self.get_original_target()

        if self.request.htmx:
            context["htmx_target"] = self.get_htmx_target()

        # Add related fields for list view
        if self.role == Role.LIST and hasattr(self, "object_list"):
            context["related_fields"] = {
                field.name: field.related_model._meta.verbose_name
                for field in self.model._meta.fields
                if field.is_relation
            }

        # Add related objects for detail view
        if self.role == Role.DETAIL and hasattr(self, "object"):
            context["related_objects"] = {
                field.name: str(getattr(self.object, field.name))
                for field in self.model._meta.fields
                if field.is_relation and getattr(self.object, field.name)
            }

        return context

    def get_success_url(self):
        # Verify that a model is defined for this view
        # This is required to construct the URL patterns
        assert self.model is not None, (
            "'%s' must define 'model' or override 'get_success_url()'"
            % self.__class__.__name__
        )

        # Construct the list URL name, using namespace if provided
        # Example: "sample:author-list" or just "author-list"
        url_name = (
            f"{self.namespace}:{self.url_base}-list"
            if self.namespace
            else f"{self.url_base}-list"
        )

        # Different behavior based on the role
        if self.role in (Role.DELETE, Role.UPDATE, Role.CREATE):
            # After deletion, go to the list view
            success_url = reverse(url_name)
        else:
            # For create/update, construct detail URL
            # Example: "sample:author-detail" or "author-detail"
            detail_url = (
                f"{self.namespace}:{self.url_base}-detail"
                if self.namespace
                else f"{self.url_base}-detail"
            )
            # Reverse the detail URL with the object's primary key
            success_url = reverse(detail_url, kwargs={"pk": self.object.pk})

        return success_url

    def render_to_response(self, context={}):
        """Handle both HTMX and regular requests"""
        template_names = self.get_template_names()
        template_name = template_names[0] if self.template_name else template_names[1]

        if self.request.htmx:
            # Store original target when first receiving list view
            if self.role == Role.LIST:
                self.request.session[self.get_session_key()] = f"#{self.request.htmx.target}"
                # context["original_target"] = f"#{self.request.htmx.target}"
                context["original_target"] = self.get_original_target()
            return render(
                request=self.request,
                template_name=f"{template_name}#content",
                context=context,
            )
        else:
            return TemplateResponse(
                request=self.request, template=template_name, context=context
            )
