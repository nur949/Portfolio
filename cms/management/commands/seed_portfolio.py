from datetime import date

from django.core.management.base import BaseCommand

from cms.models import (
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


class Command(BaseCommand):
    help = "Seed the portfolio CMS with professional Django developer content."

    def handle(self, *args, **options):
        site_settings, _ = SiteSettings.objects.update_or_create(
            id=1,
            defaults={
                "site_name": "Nur",
                "site_tagline": "Django Developer | APIs, Admin Panels, and Production Systems",
                "owner_name": "Md. Nur Jamal Miah",
                "role_title": "Django Developer",
                "seo_description": (
                    "Md. Nur Jamal Miah is a Django Developer based in Savar, Dhaka, building "
                    "REST APIs, admin dashboards, business automation tools, and deploy-ready web "
                    "applications with Django, PostgreSQL, and modern frontend collaboration."
                ),
                "location": "Savar, Dhaka, Bangladesh",
                "primary_email": "nurjamalbabu949@gmail.com",
                "phone": "+8801739391331",
                "availability_text": (
                    "Available for Django backend development, REST API implementation, admin "
                    "dashboard projects, bug fixing, and deployment support."
                ),
                "resume_url": "",
                "github_url": "https://github.com/nur949",
                "linkedin_url": "https://linkedin.com/in/nur949",
                "twitter_url": "https://x.com/nur949",
                "figma_url": "",
                "source_code_url": "https://github.com/nur949",
                "design_concept_url": "",
                "last_update_url": "https://github.com/nur949",
                "footer_about_title": "Django Developer",
                "footer_text": (
                    "I build dependable Django applications for real business use cases: clean "
                    "REST APIs, structured admin panels, stable database design, and deployment "
                    "workflows that are easy to maintain after launch."
                ),
                "copyright_name": "Md. Nur Jamal Miah",
            },
        )

        HomePage.objects.update_or_create(
            id=1,
            defaults={
                "eyebrow": "Django developer focused on production-ready backend delivery",
                "hero_title": "I build scalable Django applications with clean architecture and reliable delivery.",
                "hero_intro": "Backend-focused web development for APIs, dashboards, CMS platforms, and business systems.",
                "hero_description": (
                    "From data modeling and admin workflows to REST APIs, testing, and deployment, "
                    "I build Django solutions that are practical, maintainable, and ready for real users."
                ),
                "greeting": "hi!",
                "name": "Nur",
                "full_name": "Md. Nur Jamal Miah",
                "role": "Django Developer",
                "role_description": "building APIs, admin panels, and deploy-ready web applications.",
                "primary_cta_label": "Explore Projects",
                "primary_cta_url": "/projects",
                "secondary_cta_label": "Discuss a Project",
                "secondary_cta_url": "/work/contact",
                "highlight_title": "Backend systems built for long-term use",
                "highlight_body": (
                    "I focus on maintainable architecture, readable code, practical admin experiences, "
                    "and deployment workflows that help projects move smoothly from idea to production."
                ),
                "quote_line_one": "Clean",
                "quote_line_two_prefix": "backend",
                "quote_line_two_suffix": "delivery",
                "quote_line_three_prefix": "is a",
                "quote_line_three_highlight": "must.",
                "detail_title": "Thoughtful data models and dependable admin workflows.",
                "detail_description": (
                    "I design structured models, intuitive Django admin experiences, and practical "
                    "content workflows so teams can manage products without friction."
                ),
                "optimized_title": "Readable code, stable APIs, and deployment-ready builds.",
                "optimized_description": (
                    "My work prioritizes maintainability, performance, and production readiness with "
                    "clear structure across backend, database, and deployment layers."
                ),
            },
        )

        feature_cards = [
            (
                "Django Architecture",
                "Designing maintainable project structure, reusable apps, and practical admin workflows.",
                "amber",
                "sparkles",
            ),
            (
                "REST API Delivery",
                "Building authentication-ready APIs, serializers, business logic, and data integrations.",
                "pink",
                "heart",
            ),
            (
                "Deployment & Support",
                "Preparing projects for Render, PostgreSQL, static files, migrations, and post-launch updates.",
                "sky",
                "code",
            ),
        ]
        HomeFeatureCard.objects.all().delete()
        for index, (title, description, color, icon) in enumerate(feature_cards, start=1):
            HomeFeatureCard.objects.create(
                title=title,
                description=description,
                color=color,
                icon=icon,
                sort_order=index,
            )

        tech_stack = [
            ("Python", "python"),
            ("Django", "django"),
            ("Django REST Framework", "drf"),
            ("PostgreSQL", "postgresql"),
            ("Docker", "docker"),
            ("Divider", "divider"),
            ("Redis", "redis"),
            ("Render", "render"),
        ]
        HomeTechStackItem.objects.all().delete()
        for index, (label, icon) in enumerate(tech_stack, start=1):
            HomeTechStackItem.objects.create(
                label=label,
                icon=icon,
                sort_order=index,
            )

        social_links = [
            ("GitHub", "https://github.com/nur949", "github"),
            ("LinkedIn", "https://linkedin.com/in/nur949", "linkedin"),
            ("Twitter / X", "https://x.com/nur949", "twitter"),
            ("Email", "mailto:nurjamalbabu949@gmail.com", "mail"),
        ]
        SocialLink.objects.all().delete()
        for index, (label, url, icon) in enumerate(social_links, start=1):
            SocialLink.objects.create(
                label=label,
                url=url,
                icon=icon,
                sort_order=index,
            )

        services = [
            (
                "Backend Planning",
                "Turn product requirements into clear Django app structure, database models, and implementation scope.",
                "Technical planning",
            ),
            (
                "API & Admin Development",
                "Build secure APIs, business logic, Django admin tools, and content workflows for internal teams.",
                "Core development",
            ),
            (
                "Deployment & Maintenance",
                "Prepare projects for production with environment configuration, static files, migrations, and support.",
                "Production ready",
            ),
        ]
        Service.objects.all().delete()
        for index, (title, summary, highlight) in enumerate(services, start=1):
            Service.objects.create(
                title=title,
                summary=summary,
                highlight=highlight,
                sort_order=index,
            )

        Skill.objects.all().delete()
        SkillGroup.objects.all().delete()
        backend_group = SkillGroup.objects.create(
            title="Django Backend Engineering",
            description="Application structure, business logic, REST APIs, and maintainable backend delivery.",
            sort_order=1,
        )
        data_group = SkillGroup.objects.create(
            title="Database & Infrastructure",
            description="Persistence, deployment, configuration, and production support.",
            sort_order=2,
        )
        collaboration_group = SkillGroup.objects.create(
            title="Frontend Collaboration & Delivery",
            description="Working smoothly with UI layers, product requirements, and release workflows.",
            sort_order=3,
        )

        skill_items = [
            (backend_group, "Python", "Clean application logic, utilities, and backend feature development.", "expert", 1),
            (backend_group, "Django", "Models, views, admin customization, forms, and scalable app structure.", "expert", 2),
            (backend_group, "Django REST Framework", "Serializers, API design, permissions, and integration-friendly endpoints.", "advanced", 3),
            (backend_group, "Authentication & Authorization", "Session auth, role handling, permissions, and admin access control.", "advanced", 4),
            (data_group, "PostgreSQL", "Relational schema design, query optimization, and production database setup.", "advanced", 5),
            (data_group, "SQLite", "Fast local iteration, prototypes, and content-driven backend builds.", "advanced", 6),
            (data_group, "Deployment on Render", "Environment setup, migrations, static assets, and production rollout.", "advanced", 7),
            (data_group, "Docker Basics", "Container-ready local setup and deployment-friendly backend packaging.", "intermediate", 8),
            (collaboration_group, "HTML / CSS / Bootstrap", "Backend-connected UI implementation for dashboards and content sites.", "advanced", 9),
            (collaboration_group, "JavaScript / React Collaboration", "Working with frontend requirements, API contracts, and integration flows.", "advanced", 10),
            (collaboration_group, "Git & Release Workflow", "Clean iteration, debugging, fixes, and production support.", "advanced", 11),
        ]
        for group, name, summary, level, sort_order in skill_items:
            Skill.objects.create(
                group=group,
                name=name,
                summary=summary,
                level=level,
                sort_order=sort_order,
            )

        projects = [
            {
                "title": "Django Commerce Platform",
                "summary": "A backend-driven commerce system with product management, order handling, customer workflows, and admin control.",
                "description": (
                    "Built to manage products, categories, customer orders, stock flow, and internal administration with a reliable Django structure."
                ),
                "stack": "Python, Django, PostgreSQL, Bootstrap, Render",
                "repo_url": "",
                "live_url": "",
                "featured": True,
                "sort_order": 1,
            },
            {
                "title": "Operations Dashboard & CMS",
                "summary": "A custom admin-focused web app for managing content, services, staff workflows, and internal reporting.",
                "description": (
                    "Focused on fast content management, role-aware workflows, dashboard usability, and maintainable backend logic for everyday operations."
                ),
                "stack": "Python, Django, Django Admin, SQLite, JavaScript",
                "repo_url": "",
                "live_url": "",
                "featured": True,
                "sort_order": 2,
            },
            {
                "title": "Portfolio CMS with Render Deployment",
                "summary": "A Django-powered portfolio CMS with API support, project demos, media handling, and production deployment setup.",
                "description": (
                    "Includes Django admin content management, REST API output, managed pages, project demo previews, and deploy-ready configuration for Render."
                ),
                "stack": "Python, Django, DRF, WhiteNoise, Render",
                "repo_url": "",
                "live_url": "",
                "featured": True,
                "sort_order": 3,
            },
        ]
        Project.objects.all().delete()
        for item in projects:
            Project.objects.create(**item)

        Experience.objects.all().delete()
        Experience.objects.create(
            role="Django Developer",
            company="Freelance & Contract Projects",
            location="Remote / Bangladesh",
            start_date=date(2023, 1, 1),
            is_current=True,
            summary=(
                "Develop backend systems, admin dashboards, and REST APIs for business websites "
                "and content-driven applications using Django and related tooling."
            ),
            achievements=(
                "Built Django applications from database modeling to deployment-ready delivery\n"
                "Implemented REST APIs, admin customization, and business-focused dashboard workflows\n"
                "Configured environments, static/media handling, and production deployment on Render\n"
                "Worked on bug fixing, refactoring, and long-term maintainability improvements"
            ),
            sort_order=1,
        )
        Experience.objects.create(
            role="Junior Web Developer",
            company="Training, Internship & Client Support Work",
            location="Dhaka, Bangladesh",
            start_date=date(2022, 1, 1),
            end_date=date(2022, 12, 31),
            summary=(
                "Supported frontend and backend implementation tasks, learned practical delivery "
                "workflows, and contributed to feature updates for small business websites."
            ),
            achievements=(
                "Assisted with feature implementation across Django-based web projects\n"
                "Improved UI integration and backend debugging during delivery cycles\n"
                "Practiced database updates, deployment basics, and issue resolution"
            ),
            sort_order=2,
        )

        Testimonial.objects.all().delete()
        Testimonial.objects.create(
            author_name="Product Owner Placeholder",
            author_role="Client / Team Lead",
            quote=(
                "Nur delivers Django work with care, structure, and a strong focus on making "
                "admin workflows and backend logic practical for real use."
            ),
            sort_order=1,
        )

        managed_pages = [
            (
                "experience",
                "Professional Experience",
                "A concise overview of my Django-focused development journey and delivery approach.",
                "Background",
                """
I work as a Django Developer focused on building backend systems that are practical to maintain after launch.

## Core strengths

- Django application architecture
- Django REST Framework API development
- Django admin customization and CMS workflows
- Database design with PostgreSQL and SQLite
- Production deployment on Render

## Delivery mindset

I prefer readable code, clear business logic, structured models, and workflows that help both developers and non-technical teams use the product comfortably.
                """.strip(),
            ),
            (
                "skills-and-tools",
                "Skills & Tools",
                "The backend stack, deployment tools, and collaboration skills I use to ship Django products.",
                "Capability",
                """
My strongest value comes from combining backend engineering with practical delivery.

## Backend

- Python
- Django
- Django REST Framework
- Authentication and permissions

## Data & infrastructure

- PostgreSQL
- SQLite
- Render deployment
- Static and media file handling

## Collaboration

- API integration support
- Admin workflow design
- Maintenance and bug fixing
                """.strip(),
            ),
            (
                "contact",
                "Let's Build with Django",
                "If you need a Django developer for APIs, dashboards, CMS tools, or deployment support, let's talk.",
                "Contact",
                """
I'm available for freelance work, contract backend development, and production support for Django-based projects.

You can reach me for:

- Django backend development
- REST API implementation
- Admin panel and CMS customization
- Deployment setup on Render
- Performance improvements and bug fixing
                """.strip(),
            ),
            (
                "studio",
                "How I Build Django Projects",
                "My workflow from planning through release, with an emphasis on maintainable backend delivery.",
                "Process",
                """
## Discovery & planning

Understand the product requirements, user roles, data relationships, and delivery scope.

## Backend implementation

Build the Django apps, models, admin tools, APIs, and business logic with maintainability in mind.

## Testing & release

Prepare static files, environment variables, migrations, deployment configuration, and post-launch fixes.
                """.strip(),
            ),
        ]
        ManagedPage.objects.all().delete()
        for index, (slug, title, description, caption, body_markdown) in enumerate(
            managed_pages,
            start=1,
        ):
            ManagedPage.objects.create(
                slug=slug,
                title=title,
                description=description,
                caption=caption,
                body_markdown=body_markdown,
                sort_order=index,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded professional Django developer content for {site_settings.site_name}."
            )
        )
