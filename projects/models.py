from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from core import models as CORE_MODELS


class Project(CORE_MODELS.BaseModel):
    team = models.ManyToManyField("accounts.Profile", related_name="projects")
    MSC = "M"
    RE = "R"
    PROJECT_CATEGORIES = (
        (MSC, "MSC"),
        (RE, "RESPONSIBLE COMPUTING"),
    )
    category = models.CharField(
        _("Category"), choices=PROJECT_CATEGORIES, max_length=1, blank=True, null=True
    )

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})
