from django.test import TestCase
from ..models import Portfolio, Project, Skill


class ModelTestCase(TestCase):
    fixtures = ["tests.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        portfolio = Portfolio.objects.get(pk=1)
        Project.objects.create(name="Landing Page", portfolio=portfolio)
        Skill.objects.create(name="Tailwindcss", portfolio=portfolio)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_printed_portfolio(self):
        mod = Portfolio.objects.get(pk=1)
        self.assertEqual(mod.__str__(), f"Portfolio:{mod.title}:{mod.owner.username}")

    def test_printed_project(self):
        proj = Project.objects.get(pk=1)
        self.assertEqual(
            proj.__str__(), f"Project:{proj.name}:{proj.portfolio.owner.username}"
        )

    def test_printed_skill(self):
        skill = Skill.objects.get(pk=1)
        self.assertEqual(
            skill.__str__(), f"Skill:{skill.name}:{skill.portfolio.owner.username}"
        )
