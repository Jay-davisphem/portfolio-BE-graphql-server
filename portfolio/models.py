from django.db import models
from .utils.image_dir_path import project_dir_path, skill_dir_path


class Portfolio(models.Model):
    owner = models.ForeignKey('auth.User', related_name='porfolios', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["owner", "title"], name="unique porfolio")
        ]

    def __str__(self):
        return f"Portfolio:{self.title}:{self.owner.username}"


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=project_dir_path)
    deployed_at = models.URLField()
    code_url = models.URLField()
    portfolio = models.ManyToManyField(Portfolio, related_name="projects")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name"], name="unique project")]

    def __str__(self):
        return f"Project:{self.name}:{self.portfolio.owner.username}"


class Skill(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=skill_dir_path)
    portfolio = models.ManyToManyField(Portfolio, related_name="skills")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name"], name="unique skill")]

    def __str__(self):
        return f"Skill:{self.name}:{self.portfolio.owner.username}"
