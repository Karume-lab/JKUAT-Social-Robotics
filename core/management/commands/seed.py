import json
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from datetime import datetime
from news.models import News
from people.models import Person
from projects.models import Project
from publications.models import Publication
from robots.models import Robot
from events.models import Event
from django.conf import settings
from django.db import IntegrityError
from decouple import config
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Seed data from JSON files into Django models"

    def handle(self, *args, **kwargs):
        self.create_admin()
        BASE_FILE_PATH = f"{settings.BASE_DIR}/data"
        DATA = [
            {
                "name": "people",
                "file_path": f"{BASE_FILE_PATH}/people.json",
                "class": Person,
            },
            {"name": "news", "file_path": f"{BASE_FILE_PATH}/news.json", "class": News},
            {
                "name": "projects",
                "file_path": f"{BASE_FILE_PATH}/projects.json",
                "class": Project,
            },
            {
                "name": "publications",
                "file_path": f"{BASE_FILE_PATH}/publications.json",
                "class": Publication,
            },
            {
                "name": "robots",
                "file_path": f"{BASE_FILE_PATH}/robots.json",
                "class": Robot,
            },
            {
                "name": "events",
                "file_path": f"{BASE_FILE_PATH}/events.json",
                "class": Event,
            },
        ]

        for entry in DATA:
            self.seed_data(entry)

    def create_admin(self):
        User = get_user_model()

        username = config("ADMIN_USERNAME")
        password = config("ADMIN_PASSWORD")

        if not all([username, password]):
            self.stdout.write(
                self.style.ERROR(
                    "Missing environment variables for admin user creation"
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user "{username}" already exists.')
            )
        else:
            User.objects.create_superuser(username=username, password=password)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user "{username}".')
            )

    def seed_data(self, entry):
        try:
            with open(entry["file_path"]) as f:
                data_list = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {entry['file_path']}"))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error decoding JSON in file {entry['file_path']}: {e}"
                )
            )
            return

        for data in data_list:
            if entry["name"] == "projects":
                self.handle_project(data, entry)
            elif entry["name"] == "people":
                self.handle_person(data, entry)
            else:
                self.create_instance(data, entry)

    def handle_person(self, data, entry):
        try:
            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S%f")
            data["slug"] = slugify(
                f"{data['first_name']}-{data['last_name']}___{current_datetime}"
            )
            person, created = Person.objects.get_or_create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                defaults=data,
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created person: {person}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Person already exists: {person}")
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating person: {e}"))

    def handle_project(self, data, entry):
        if "team" in data:
            team_data = data.pop("team")

            project, created = self.create_instance(data, entry)

            if project:
                for member in team_data:
                    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    member["slug"] = slugify(
                        f"{member['first_name']}-{member['last_name']}___{current_datetime}"
                    )

                    person, person_created = Person.objects.get_or_create(
                        first_name=member["first_name"],
                        last_name=member["last_name"],
                        defaults=member,
                    )

                    if person_created:
                        self.stdout.write(
                            self.style.SUCCESS(f"Created new team member: {person}")
                        )

                    if person not in project.team.all():
                        project.team.add(person)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Added team member: {person} to project: {project}"
                            )
                        )
                project.save()
        else:
            # Create the project instance if no team data is provided
            self.create_instance(data, entry)

    def create_instance(self, data, entry):
        try:
            if "slug" not in data:
                current_datetime = datetime.now().strftime("%Y%m%d%H%M%S%f")
                data["slug"] = slugify(f"{data.get('title', '')}___{current_datetime}")

            instance, created = entry["class"].objects.get_or_create(**data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created {entry['name']} instance: {instance}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"{entry['name']} instance already exists: {instance}"
                    )
                )
            return instance, created
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Integrity error creating {entry['name']} instance: {e}"
                )
            )
        except ValidationError as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Validation error creating {entry['name']} instance: {e}"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Unexpected error creating {entry['name']} instance: {e}"
                )
            )
        return None, False
