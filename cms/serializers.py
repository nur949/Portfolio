import markdown

from rest_framework import serializers

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


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"


class HomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePage
        fields = "__all__"


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class HomeFeatureCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeFeatureCard
        fields = "__all__"


class HomeTechStackItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeTechStackItem
        fields = "__all__"


class SkillGroupSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta:
        model = SkillGroup
        fields = "__all__"

    def get_skills(self, obj):
        return [
            {
                "id": skill.id,
                "name": skill.name,
                "summary": skill.summary,
                "level": skill.level,
                "sort_order": skill.sort_order,
            }
            for skill in obj.skills.all()
        ]


class ProjectSerializer(serializers.ModelSerializer):
    stack_items = serializers.SerializerMethodField()
    demo_url = serializers.SerializerMethodField()
    has_template_demo = serializers.SerializerMethodField()
    cover_image_upload_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    def get_stack_items(self, obj):
        return [item.strip() for item in obj.stack.split(",") if item.strip()]

    def get_demo_url(self, obj):
        request = self.context.get("request")
        demo_url = obj.demo_url
        if request and demo_url:
            return request.build_absolute_uri(demo_url)
        return demo_url

    def get_has_template_demo(self, obj):
        return bool(obj.demo_entry_path)

    def get_cover_image_upload_url(self, obj):
        request = self.context.get("request")
        image_url = obj.cover_image_upload_url
        if request and image_url:
            return request.build_absolute_uri(image_url)
        return image_url


class ExperienceSerializer(serializers.ModelSerializer):
    achievement_items = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = "__all__"

    def get_achievement_items(self, obj):
        return [item.strip() for item in obj.achievements.splitlines() if item.strip()]


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"


class ManagedPageSerializer(serializers.ModelSerializer):
    body_html = serializers.SerializerMethodField()

    class Meta:
        model = ManagedPage
        fields = "__all__"

    def get_body_html(self, obj):
        return markdown.markdown(
            obj.body_markdown,
            extensions=["extra", "sane_lists", "nl2br"],
        )
