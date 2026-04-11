import shutil
import subprocess
import zipfile
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from PIL import Image


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(TimestampedModel):
    site_name = models.CharField(max_length=120, default="Your Name")
    site_tagline = models.CharField(
        max_length=180, default="Designer, developer, and digital problem solver."
    )
    owner_name = models.CharField(max_length=120, default="Your Name")
    role_title = models.CharField(max_length=120, default="Front-End Developer")
    seo_description = models.TextField(
        default="A modern portfolio website powered by Django and Next.js."
    )
    location = models.CharField(max_length=120, blank=True)
    primary_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    availability_text = models.CharField(
        max_length=160, default="Available for freelance and full-time opportunities."
    )
    resume_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    figma_url = models.URLField(blank=True)
    source_code_url = models.URLField(blank=True)
    design_concept_url = models.URLField(blank=True)
    last_update_url = models.URLField(blank=True)
    footer_about_title = models.CharField(max_length=80, default="About Me")
    footer_text = models.CharField(
        max_length=180, default="Built for ambitious brands and thoughtful digital products."
    )
    copyright_name = models.CharField(max_length=120, default="Your Name")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.site_name


class HomePage(TimestampedModel):
    eyebrow = models.CharField(max_length=80, default="Superadmin managed portfolio")
    greeting = models.CharField(max_length=40, default="hi!")
    name = models.CharField(max_length=120, default="Enji")
    full_name = models.CharField(max_length=160, default="Enji Kusnadi")
    role = models.CharField(max_length=120, default="Front-End Developer")
    role_description = models.CharField(
        max_length=240,
        default="who loves intuitive, clean and modern UI design.",
    )
    hero_title = models.CharField(
        max_length=180, default="I build polished digital experiences that feel effortless."
    )
    hero_intro = models.CharField(
        max_length=160, default="Full-stack portfolio powered by Django + SQLite + Next.js"
    )
    hero_description = models.TextField(
        default=(
            "This site is fully manageable from a superadmin dashboard. Update projects, "
            "skills, timeline entries, and contact details without touching code."
        )
    )
    primary_cta_label = models.CharField(max_length=40, default="View Projects")
    primary_cta_url = models.CharField(max_length=160, default="/projects")
    secondary_cta_label = models.CharField(max_length=40, default="Contact Me")
    secondary_cta_url = models.CharField(max_length=160, default="/work/contact")
    highlight_title = models.CharField(max_length=120, default="Why this setup works")
    highlight_body = models.TextField(
        default=(
            "Django admin gives the superadmin a familiar control center, while the public "
            "site stays fast and design-forward on the frontend."
        )
    )
    quote_line_one = models.CharField(max_length=80, default="Beautiful")
    quote_line_two_prefix = models.CharField(max_length=80, default="inside")
    quote_line_two_suffix = models.CharField(max_length=80, default="out")
    quote_line_three_prefix = models.CharField(max_length=80, default="is a")
    quote_line_three_highlight = models.CharField(max_length=80, default="must.")
    detail_title = models.CharField(
        max_length=160, default="Keen Eye for Spotting Small Details."
    )
    detail_description = models.CharField(
        max_length=220,
        default="Awareness to ease of access, User Interface consistency, and improved User Experience.",
    )
    optimized_title = models.CharField(
        max_length=160, default="Comprehensible and Optimized Code."
    )
    optimized_description = models.CharField(
        max_length=220,
        default="Writing clean code is a top priority while keeping it as optimized as possible.",
    )

    class Meta:
        verbose_name = "Home page"
        verbose_name_plural = "Home page"

    def __str__(self):
        return self.hero_title


class SocialLink(TimestampedModel):
    ICON_CHOICES = [
        ("github", "GitHub"),
        ("linkedin", "LinkedIn"),
        ("twitter", "Twitter"),
        ("website", "Website"),
        ("mail", "Mail"),
    ]

    label = models.CharField(max_length=80)
    url = models.CharField(max_length=255)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="website")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "label"]

    def __str__(self):
        return self.label


class HomeFeatureCard(TimestampedModel):
    COLOR_CHOICES = [
        ("amber", "Amber"),
        ("pink", "Pink"),
        ("sky", "Sky"),
    ]
    ICON_CHOICES = [
        ("sparkles", "Sparkles"),
        ("heart", "Heart"),
        ("code", "Code"),
    ]

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=220)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default="amber")
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="sparkles")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title


class HomeTechStackItem(TimestampedModel):
    ICON_CHOICES = [
        ("python", "Python"),
        ("django", "Django"),
        ("drf", "Django REST Framework"),
        ("postgresql", "PostgreSQL"),
        ("docker", "Docker"),
        ("divider", "Divider"),
        ("redis", "Redis"),
        ("render", "Render"),
    ]

    label = models.CharField(max_length=80)
    icon = models.CharField(max_length=30, choices=ICON_CHOICES)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "label"]

    def __str__(self):
        return self.label


class ManagedPage(TimestampedModel):
    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=160)
    description = models.CharField(max_length=220)
    caption = models.CharField(max_length=80, blank=True)
    body_markdown = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title


class Service(TimestampedModel):
    title = models.CharField(max_length=120)
    summary = models.TextField()
    highlight = models.CharField(max_length=120, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title


class SkillGroup(TimestampedModel):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=180, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title


class Skill(TimestampedModel):
    LEVEL_CHOICES = [
        ("expert", "Expert"),
        ("advanced", "Advanced"),
        ("intermediate", "Intermediate"),
    ]

    group = models.ForeignKey(
        SkillGroup, on_delete=models.CASCADE, related_name="skills"
    )
    name = models.CharField(max_length=80)
    summary = models.CharField(max_length=180, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="advanced")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class Project(TimestampedModel):
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    summary = models.CharField(max_length=220)
    description = models.TextField()
    stack = models.CharField(
        max_length=240, help_text="Comma separated technologies, e.g. Next.js, Django, Tailwind"
    )
    repo_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    cover_image = models.ImageField(
        upload_to="project_covers/",
        blank=True,
        help_text="Upload a project cover image to display on the portfolio site.",
    )
    template_zip = models.FileField(
        upload_to="project_templates/zips/",
        blank=True,
        validators=[FileExtensionValidator(["zip"])],
        help_text="Upload a static HTML/CSS/JS zip file with an index.html entry point.",
    )
    demo_entry_path = models.CharField(max_length=255, blank=True)
    cover_image_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "title"]

    def clean(self):
        super().clean()
        if not self.template_zip:
            return

        file_obj = self.template_zip.file
        original_position = None

        try:
            if hasattr(file_obj, "tell"):
                original_position = file_obj.tell()
            if hasattr(file_obj, "seek"):
                file_obj.seek(0)

            with zipfile.ZipFile(file_obj) as archive:
                self._validate_archive(archive)
        except zipfile.BadZipFile as exc:
            raise ValidationError({"template_zip": "Upload a valid zip archive."}) from exc
        finally:
            if original_position is not None and hasattr(file_obj, "seek"):
                file_obj.seek(original_position)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        previous_zip_name = ""
        previous_slug = ""
        if self.pk:
            previous_zip_name, previous_slug = (
                Project.objects.filter(pk=self.pk)
                .values_list("template_zip", "slug")
                .first()
                or ("", "")
            )

        super().save(*args, **kwargs)

        current_zip_name = self.template_zip.name if self.template_zip else ""
        should_sync_demo = bool(current_zip_name) and (
            current_zip_name != previous_zip_name
            or previous_slug != self.slug
            or not self.demo_entry_path
        )

        if should_sync_demo:
            self.sync_template_demo(previous_slug=previous_slug)
        elif not current_zip_name and self.demo_entry_path:
            self.clear_template_demo(previous_slug=previous_slug)

    def delete(self, *args, **kwargs):
        self.clear_template_demo(remove_zip=False, previous_slug=self.slug)
        if self.template_zip:
            self.template_zip.delete(save=False)
        super().delete(*args, **kwargs)

    def get_demo_directory(self, slug=None) -> Path:
        return Path(settings.MEDIA_ROOT) / "project_demos" / (slug or self.slug)

    def clear_template_demo(self, remove_zip=False, previous_slug=""):
        demo_dir = self.get_demo_directory(previous_slug)
        if demo_dir.exists():
            shutil.rmtree(demo_dir)

        preview_path = self.get_demo_preview_image_path(previous_slug)
        if preview_path.exists():
            preview_path.unlink()

        updates = {"demo_entry_path": ""}
        if remove_zip:
            updates["template_zip"] = ""
        Project.objects.filter(pk=self.pk).update(**updates)
        self.demo_entry_path = ""
        if remove_zip:
            self.template_zip = ""

    def _validate_archive(self, archive):
        has_index = False
        for member in archive.infolist():
            member_path = Path(member.filename)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise ValidationError(
                    {"template_zip": "The uploaded zip contains an unsafe file path."}
                )

            if member_path.name.lower() == "index.html":
                has_index = True

        if not has_index:
            raise ValidationError(
                {"template_zip": "The uploaded zip must include an index.html file."}
            )

    def sync_template_demo(self, previous_slug=""):
        if not self.template_zip:
            self.clear_template_demo()
            return

        if previous_slug and previous_slug != self.slug:
            old_demo_dir = self.get_demo_directory(previous_slug)
            if old_demo_dir.exists():
                shutil.rmtree(old_demo_dir)

        demo_dir = self.get_demo_directory()
        if demo_dir.exists():
            shutil.rmtree(demo_dir)
        demo_dir.mkdir(parents=True, exist_ok=True)

        found_index = None

        with zipfile.ZipFile(self.template_zip.path) as archive:
            self._validate_archive(archive)
            for member in archive.infolist():
                member_path = Path(member.filename)

                target_path = demo_dir / member_path
                target_path_resolved = target_path.resolve(strict=False)
                demo_dir_resolved = demo_dir.resolve()
                if demo_dir_resolved not in target_path_resolved.parents and (
                    target_path_resolved != demo_dir_resolved
                ):
                    raise ValidationError(
                        {"template_zip": "The uploaded zip tries to write outside the demo directory."}
                    )

                if member.is_dir():
                    target_path.mkdir(parents=True, exist_ok=True)
                    continue

                target_path.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(member) as source, open(target_path, "wb") as destination:
                    shutil.copyfileobj(source, destination)

                if target_path.name.lower() == "index.html" and found_index is None:
                    found_index = target_path

        if found_index is None:
            shutil.rmtree(demo_dir, ignore_errors=True)
            raise ValidationError(
                {"template_zip": "The uploaded zip must include an index.html file."}
            )

        relative_entry = found_index.relative_to(Path(settings.MEDIA_ROOT)).as_posix()
        Project.objects.filter(pk=self.pk).update(demo_entry_path=relative_entry)
        self.demo_entry_path = relative_entry
        self.generate_demo_preview_image(found_index)

    def get_demo_preview_image_path(self, slug=None) -> Path:
        return Path(settings.MEDIA_ROOT) / "project_previews" / f"{slug or self.slug}.png"

    def generate_demo_preview_image(self, entry_file: Path):
        preview_path = self.get_demo_preview_image_path()
        preview_path.parent.mkdir(parents=True, exist_ok=True)
        if preview_path.exists():
            preview_path.unlink()

        browser_candidates = [
            Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
            Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        ]
        browser_path = next((candidate for candidate in browser_candidates if candidate.exists()), None)
        if not browser_path:
            return

        command = [
            str(browser_path),
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=4000",
            "--window-size=1600,980",
            f"--screenshot={preview_path}",
            entry_file.resolve().as_uri(),
        ]

        try:
            subprocess.run(
                command,
                check=True,
                timeout=45,
                capture_output=True,
                text=True,
            )
        except (subprocess.SubprocessError, OSError):
            if preview_path.exists():
                preview_path.unlink()
            return

        self._cleanup_preview_image(preview_path)

    def _cleanup_preview_image(self, preview_path: Path):
        if not preview_path.exists():
            return

        try:
            with Image.open(preview_path) as image:
                width, height = image.size
                crop_right = width
                crop_bottom = height

                # Trim bright scrollbar-like stripes from the right edge.
                for x in range(width - 1, max(width - 300, 0), -1):
                    sample_points = [
                        image.getpixel((x, max(0, min(height - 1, int(height * ratio)))))
                        for ratio in (0.05, 0.2, 0.35, 0.5, 0.7)
                    ]
                    if all(sum(pixel[:3]) >= 735 for pixel in sample_points):
                        crop_right = x
                    else:
                        break

                # Trim bright footer-like strip from the bottom edge.
                for y in range(height - 1, max(height - 300, 0), -1):
                    sample_points = [
                        image.getpixel((max(0, min(width - 1, int(width * ratio))), y))
                        for ratio in (0.05, 0.25, 0.5, 0.75)
                    ]
                    if all(sum(pixel[:3]) >= 735 for pixel in sample_points):
                        crop_bottom = y
                    else:
                        break

                crop_left = 0
                crop_top = 0

                if crop_right < width or crop_bottom < height:
                    image = image.crop((crop_left, crop_top, crop_right, crop_bottom))

                image.save(preview_path)
        except OSError:
            return

    @property
    def demo_url(self):
        if not self.demo_entry_path:
            return ""
        return f"{settings.MEDIA_URL}{self.demo_entry_path}".replace("//", "/")

    @property
    def demo_preview_image_url(self):
        preview_path = self.get_demo_preview_image_path()
        if not preview_path.exists():
            return ""
        relative_path = preview_path.relative_to(Path(settings.MEDIA_ROOT)).as_posix()
        return f"{settings.MEDIA_URL}{relative_path}".replace("//", "/")

    @property
    def cover_image_upload_url(self):
        if not self.cover_image:
            return ""
        return self.cover_image.url

    def __str__(self):
        return self.title


class Experience(TimestampedModel):
    role = models.CharField(max_length=140)
    company = models.CharField(max_length=140)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    summary = models.TextField()
    achievements = models.TextField(
        blank=True,
        help_text="One bullet per line. These will be split into a list in the API.",
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-start_date"]

    def __str__(self):
        return f"{self.role} at {self.company}"


class Testimonial(TimestampedModel):
    quote = models.TextField()
    author_name = models.CharField(max_length=120)
    author_role = models.CharField(max_length=160)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "author_name"]

    def __str__(self):
        return self.author_name
