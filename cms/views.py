import re
from pathlib import Path
from urllib.parse import urljoin

import markdown
from django.conf import settings

from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Experience,
    HomeFeatureCard,
    HomePage,
    HomeTechStackItem,
    ManagedPage,
    Project,
    Service,
    SiteSettings,
    SkillGroup,
    SocialLink,
    Testimonial,
)
from .serializers import (
    ExperienceSerializer,
    HomeFeatureCardSerializer,
    HomePageSerializer,
    HomeTechStackItemSerializer,
    ManagedPageSerializer,
    ProjectSerializer,
    ServiceSerializer,
    SiteSettingsSerializer,
    SkillGroupSerializer,
    SocialLinkSerializer,
    TestimonialSerializer,
)


WORK_PAGE_ORDER = [
    ("skills-and-tools", "Skills & Tools", "/work/skills-and-tools/"),
    ("experience", "Experience", "/work/experience/"),
    ("studio", "Studio", "/work/studio/"),
    ("contact", "Contact", "/work/contact/"),
]


def _clean_display_name(value):
    cleaned = re.sub(r"^\s*md\.?\s+", "", value or "", flags=re.IGNORECASE).strip()
    return cleaned or (value or "").strip()


def _detect_demo_preview_url(project):
    if not getattr(project, "demo_entry_path", ""):
        return ""

    entry_path = Path(settings.MEDIA_ROOT) / project.demo_entry_path
    if not entry_path.exists():
        return ""

    try:
        content = entry_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""

    candidates = []
    img_matches = re.findall(
        r"""<(?:img|source)[^>]+(?:src|srcset)=["']([^"'#?]+(?:png|jpe?g|webp|gif|svg))[^"']*["']""",
        content,
        flags=re.IGNORECASE,
    )
    candidates.extend(img_matches)

    bg_matches = re.findall(
        r"""url\((?:["'])?([^"')#?]+(?:png|jpe?g|webp|gif|svg))(?:["'])?\)""",
        content,
        flags=re.IGNORECASE,
    )
    candidates.extend(bg_matches)

    priority_patterns = ("hero", "banner", "cover", "bg", "header", "slider")
    normalized = []
    for candidate in candidates:
        cleaned = candidate.strip()
        if not cleaned or cleaned.startswith(("http://", "https://", "data:")):
            continue
        normalized.append(cleaned)

    if not normalized:
        return ""

    normalized.sort(
        key=lambda item: (
            0 if any(pattern in item.lower() for pattern in priority_patterns) else 1,
            len(item),
        )
    )

    selected = normalized[0]
    if selected.startswith("/"):
        return urljoin(settings.MEDIA_URL, selected.lstrip("/"))

    preview_path = (entry_path.parent / selected).resolve(strict=False)
    media_root = Path(settings.MEDIA_ROOT).resolve()
    if media_root not in preview_path.parents and preview_path != media_root:
        return ""

    try:
        relative_preview = preview_path.relative_to(media_root).as_posix()
    except ValueError:
        return ""
    return urljoin(settings.MEDIA_URL, relative_preview)


def _build_public_context():
    site = SiteSettings.objects.order_by("id").first()
    home = HomePage.objects.order_by("id").first()
    social_links = list(SocialLink.objects.all())
    feature_cards = list(HomeFeatureCard.objects.all())
    tech_stack = list(HomeTechStackItem.objects.all())
    services = list(Service.objects.all())
    skill_groups = list(SkillGroup.objects.prefetch_related("skills").all())
    projects = list(Project.objects.all())
    experience = list(Experience.objects.all())
    testimonials = list(Testimonial.objects.all())
    managed_pages = list(ManagedPage.objects.all())
    clean_name = _clean_display_name(
        getattr(home, "full_name", "") or getattr(site, "owner_name", "")
    )
    hero_name_parts = clean_name.split(None, 1) if clean_name else ["Nur", ""]
    hero_first_name = hero_name_parts[0]
    hero_remaining_name = hero_name_parts[1] if len(hero_name_parts) > 1 else ""

    for page in managed_pages:
        page.body_html = markdown.markdown(
            page.body_markdown,
            extensions=["extra", "sane_lists", "nl2br"],
        )

    for item in experience:
        achievements = [line.strip() for line in item.achievements.splitlines() if line.strip()]
        item.achievement_items = achievements
        start = item.start_date.strftime("%b %Y")
        end = "Present" if item.is_current or not item.end_date else item.end_date.strftime("%b %Y")
        item.date_range = f"{start} - {end}"

    for project in projects:
        project.stack_items = [part.strip() for part in project.stack.split(",") if part.strip()]
        project.cover_display_url = project.cover_image_upload_url or project.cover_image_url
        project.demo_preview_url = project.demo_preview_image_url or _detect_demo_preview_url(project)

    return {
        "site": site,
        "home": home,
        "social_links": social_links,
        "home_feature_cards": feature_cards,
        "home_tech_stack": tech_stack,
        "services": services,
        "skill_groups": skill_groups,
        "projects": projects,
        "featured_projects": [project for project in projects if project.featured],
        "experience_items": experience,
        "testimonials": testimonials,
        "managed_pages": managed_pages,
        "work_links": WORK_PAGE_ORDER,
        "hero_first_name": hero_first_name,
        "hero_remaining_name": hero_remaining_name,
    }


def home_page(request):
    context = _build_public_context()
    return render(request, "site/home.html", context)


def projects_page(request):
    context = _build_public_context()
    return render(request, "site/projects.html", context)


def managed_work_page(request, slug):
    context = _build_public_context()
    page = next((item for item in context["managed_pages"] if item.slug == slug), None)
    if not page:
        raise Http404("Page not found")
    context["page"] = page
    return render(request, "site/work_page.html", context)


@staff_member_required(login_url="/admin/login/")
def superadmin_dashboard(request):
    context = _build_public_context()
    context["superadmin_cards"] = [
        {
            "title": "Site Settings",
            "description": "Control branding, contact details, footer content, and global links.",
            "manage_url": reverse("admin:cms_sitesettings_changelist"),
        },
        {
            "title": "Home Page",
            "description": "Edit hero content, intro text, quote lines, and homepage highlights.",
            "manage_url": reverse("admin:cms_homepage_changelist"),
        },
        {
            "title": "Projects",
            "description": "Add projects, upload template zip demos, cover images, and reorder cards.",
            "manage_url": reverse("admin:cms_project_changelist"),
        },
        {
            "title": "Managed Pages",
            "description": "Update work pages like contact, experience, skills, and studio from one place.",
            "manage_url": reverse("admin:cms_managedpage_changelist"),
        },
        {
            "title": "Skills",
            "description": "Maintain skill groups and inline skills with levels and summaries.",
            "manage_url": reverse("admin:cms_skillgroup_changelist"),
        },
        {
            "title": "Experience",
            "description": "Manage timeline entries, achievements, and current role history.",
            "manage_url": reverse("admin:cms_experience_changelist"),
        },
        {
            "title": "Social Links",
            "description": "Edit profile links that appear across the public site and contact area.",
            "manage_url": reverse("admin:cms_sociallink_changelist"),
        },
        {
            "title": "Users & Permissions",
            "description": "Manage staff users and permission groups while keeping the default admin intact.",
            "manage_url": reverse("admin:auth_user_changelist"),
        },
    ]
    context["superadmin_stats"] = [
        {"label": "Projects", "value": len(context["projects"])},
        {"label": "Skills", "value": sum(group.skills.count() for group in context["skill_groups"])},
        {"label": "Pages", "value": len(context["managed_pages"])},
        {"label": "Testimonials", "value": len(context["testimonials"])},
    ]
    return render(request, "site/superadmin.html", context)


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"status": "ok"})


class SiteContentView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        site_settings = SiteSettings.objects.order_by("id").first()
        home_page = HomePage.objects.order_by("id").first()
        projects = Project.objects.all()

        payload = {
            "site": SiteSettingsSerializer(site_settings).data if site_settings else None,
            "home": HomePageSerializer(home_page).data if home_page else None,
            "social_links": SocialLinkSerializer(SocialLink.objects.all(), many=True).data,
            "home_feature_cards": HomeFeatureCardSerializer(
                HomeFeatureCard.objects.all(), many=True
            ).data,
            "home_tech_stack": HomeTechStackItemSerializer(
                HomeTechStackItem.objects.all(), many=True
            ).data,
            "services": ServiceSerializer(Service.objects.all(), many=True).data,
            "skill_groups": SkillGroupSerializer(
                SkillGroup.objects.prefetch_related("skills").all(), many=True
            ).data,
            "projects": ProjectSerializer(
                projects, many=True, context={"request": request}
            ).data,
            "featured_projects": ProjectSerializer(
                projects.filter(featured=True),
                many=True,
                context={"request": request},
            ).data,
            "experience": ExperienceSerializer(Experience.objects.all(), many=True).data,
            "testimonials": TestimonialSerializer(
                Testimonial.objects.all(), many=True
            ).data,
            "managed_pages": ManagedPageSerializer(
                ManagedPage.objects.all(), many=True
            ).data,
        }

        return Response(payload)
