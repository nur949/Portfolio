from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Experience,
    HomeFeatureCard,
    HomePage,
    HomeTechStackItem,
    ManagedPage,
    Project,
    Service,
    SiteSettings,
    Skill,
    SkillGroup,
    SocialLink,
    Testimonial,
)

admin.site.site_header = "Django administration"
admin.site.site_title = "Django site admin"
admin.site.index_title = "Site administration"
admin.site.site_url = "/"


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20
    save_on_top = True

    def edit_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
            args=[obj.pk],
        )
        return format_html('<a class="button" href="{}">Open</a>', url)

    edit_link.short_description = "Open"


class SingletonAdmin(BaseAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def changelist_view(self, request, extra_context=None):
        existing = self.model.objects.order_by("id").first()
        if existing:
            url = reverse(
                f"admin:{existing._meta.app_label}_{existing._meta.model_name}_change",
                args=[existing.pk],
            )
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context)


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ("name", "summary", "level", "sort_order")
    ordering = ("sort_order", "name")


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    list_display = (
        "site_name",
        "owner_name",
        "primary_email",
        "location",
        "updated_at",
        "edit_link",
    )
    search_fields = ("site_name", "owner_name", "primary_email", "location")
    fieldsets = (
        (
            "Brand",
            {
                "fields": (
                    "site_name",
                    "site_tagline",
                    "owner_name",
                    "role_title",
                    "seo_description",
                )
            },
        ),
        (
            "Contact",
            {
                "fields": (
                    "location",
                    "primary_email",
                    "phone",
                    "availability_text",
                )
            },
        ),
        (
            "Profiles and external links",
            {
                "fields": (
                    "resume_url",
                    "github_url",
                    "linkedin_url",
                    "twitter_url",
                    "figma_url",
                    "source_code_url",
                    "design_concept_url",
                    "last_update_url",
                )
            },
        ),
        (
            "Footer",
            {
                "fields": (
                    "footer_about_title",
                    "footer_text",
                    "copyright_name",
                )
            },
        ),
    )


@admin.register(HomePage)
class HomePageAdmin(SingletonAdmin):
    list_display = ("hero_title", "full_name", "role", "updated_at", "edit_link")
    search_fields = ("hero_title", "full_name", "role", "eyebrow")
    fieldsets = (
        (
            "Identity",
            {
                "fields": (
                    "eyebrow",
                    "greeting",
                    "name",
                    "full_name",
                    "role",
                    "role_description",
                )
            },
        ),
        (
            "Hero",
            {
                "fields": (
                    "hero_title",
                    "hero_intro",
                    "hero_description",
                    "primary_cta_label",
                    "primary_cta_url",
                    "secondary_cta_label",
                    "secondary_cta_url",
                )
            },
        ),
        (
            "Highlights",
            {
                "fields": (
                    "highlight_title",
                    "highlight_body",
                    "quote_line_one",
                    "quote_line_two_prefix",
                    "quote_line_two_suffix",
                    "quote_line_three_prefix",
                    "quote_line_three_highlight",
                    "detail_title",
                    "detail_description",
                    "optimized_title",
                    "optimized_description",
                )
            },
        ),
    )


@admin.register(HomeFeatureCard)
class HomeFeatureCardAdmin(BaseAdmin):
    list_display = (
        "title",
        "icon",
        "color",
        "sort_order",
        "updated_at",
        "edit_link",
    )
    list_editable = ("sort_order",)
    search_fields = ("title", "description")
    list_filter = ("color", "icon")


@admin.register(HomeTechStackItem)
class HomeTechStackItemAdmin(BaseAdmin):
    list_display = ("label", "icon", "sort_order", "updated_at", "edit_link")
    list_editable = ("sort_order",)
    search_fields = ("label", "icon")


@admin.register(SocialLink)
class SocialLinkAdmin(BaseAdmin):
    list_display = ("label", "icon", "url", "sort_order", "updated_at", "edit_link")
    list_editable = ("sort_order",)
    search_fields = ("label", "url")
    list_filter = ("icon",)


@admin.register(Service)
class ServiceAdmin(BaseAdmin):
    list_display = ("title", "highlight", "sort_order", "updated_at", "edit_link")
    list_editable = ("sort_order",)
    search_fields = ("title", "summary", "highlight")


@admin.register(SkillGroup)
class SkillGroupAdmin(BaseAdmin):
    list_display = ("title", "description", "sort_order", "updated_at", "edit_link")
    list_editable = ("sort_order",)
    search_fields = ("title", "description")
    inlines = [SkillInline]


@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    list_display = (
        "title",
        "template_demo_status",
        "featured",
        "sort_order",
        "updated_at",
        "edit_link",
    )
    list_filter = ("featured",)
    list_editable = ("featured", "sort_order")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "description", "stack")
    readonly_fields = ("cover_preview_link", "demo_preview_link")
    fieldsets = (
        (
            "Project details",
            {
                "fields": (
                    "title",
                    "slug",
                    "summary",
                    "description",
                    "stack",
                    "featured",
                    "sort_order",
                )
            },
        ),
        (
            "Links",
            {
                "fields": (
                    "repo_url",
                    "live_url",
                    "cover_image",
                    "cover_preview_link",
                    "cover_image_url",
                )
            },
        ),
        (
            "Template demo",
            {
                "description": (
                    "Upload a static HTML/CSS/JS zip with an index.html file. "
                    "The system will extract it and create an in-site demo URL automatically."
                ),
                "fields": (
                    "template_zip",
                    "demo_preview_link",
                ),
            },
        ),
    )

    def template_demo_status(self, obj):
        if obj.demo_url:
            return format_html(
                '<span style="color:#2563eb;font-weight:700;">{}</span>',
                "Ready",
            )
        return format_html(
            '<span style="color:#64748b;">{}</span>',
            "No demo",
        )

    template_demo_status.short_description = "Template demo"

    def cover_preview_link(self, obj):
        if not obj.pk or not obj.cover_image:
            return "Upload a project cover image to show it here."
        return format_html(
            '<a class="button" href="{}" target="_blank" rel="noreferrer">Open Cover</a>',
            obj.cover_image.url,
        )

    cover_preview_link.short_description = "Uploaded cover"

    def demo_preview_link(self, obj):
        if not obj.pk or not obj.demo_url:
            return "Upload and save a template zip to generate a demo URL."
        return format_html(
            '<a class="button" href="{}" target="_blank" rel="noreferrer">Open Demo</a>',
            obj.demo_url,
        )

    demo_preview_link.short_description = "Generated demo"


@admin.register(Experience)
class ExperienceAdmin(BaseAdmin):
    list_display = (
        "role",
        "company",
        "is_current",
        "start_date",
        "sort_order",
        "edit_link",
    )
    list_filter = ("is_current",)
    list_editable = ("is_current", "sort_order")
    search_fields = ("role", "company", "location", "summary")


@admin.register(Testimonial)
class TestimonialAdmin(BaseAdmin):
    list_display = (
        "author_name",
        "author_role",
        "sort_order",
        "updated_at",
        "edit_link",
    )
    list_editable = ("sort_order",)
    search_fields = ("author_name", "author_role", "quote")


@admin.register(ManagedPage)
class ManagedPageAdmin(BaseAdmin):
    list_display = (
        "title",
        "slug",
        "caption",
        "sort_order",
        "updated_at",
        "edit_link",
    )
    list_editable = ("sort_order",)
    search_fields = ("title", "slug", "description", "body_markdown")
