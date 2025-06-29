import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from apps.projects.models import Project
from apps.tasks.models import Task, TaskStatus
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Seeds the database with users, projects, and tasks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.clear_data()
        self.seed_users()
        self.seed_projects()
        self.seed_tasks()

    def clear_data(self):
        self.stdout.write(self.style.WARNING("Clearing existing data..."))
        Task.objects.all().delete()
        Project.objects.all().delete()
        CustomUser.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Data cleared!"))

    def seed_users(self):
        self.stdout.write("Creating users...")
        first_names = [
            "James",
            "John",
            "Robert",
            "Michael",
            "William",
            "David",
            "Richard",
            "Joseph",
            "Thomas",
            "Charles",
            "Mary",
            "Patricia",
            "Jennifer",
            "Linda",
            "Elizabeth",
            "Barbara",
            "Susan",
            "Jessica",
            "Sarah",
            "Karen",
        ]

        last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Miller",
            "Davis",
            "Garcia",
            "Rodriguez",
            "Wilson",
            "Martinez",
            "Anderson",
            "Taylor",
            "Thomas",
            "Hernandez",
            "Moore",
            "Martin",
            "Jackson",
            "Thompson",
            "White",
        ]

        domains = ["example.com", "test.org", "demo.net", "company.io"]

        self.users = []
        for i in range(20):  # Create 20 users
            first = random.choice(first_names)
            last = random.choice(last_names)
            email = f"{first.lower()}.{last.lower()}@{random.choice(domains)}"
            username = f"{first.lower()}{last.lower()}{random.randint(1, 99)}"

            user = CustomUser.objects.create(
                first_name=first,
                last_name=last,
                email=email,
                username=username,
                password=make_password("password123"),
                last_seen=timezone.now()
                - timezone.timedelta(days=random.randint(0, 30)),
            )
            self.users.append(user)
            self.stdout.write(f"Created user {i+1}/20: {email}")

    def seed_projects(self):
        self.stdout.write("\nCreating projects...")
        project_names = [
            "Website Redesign",
            "Mobile App Development",
            "Data Migration",
            "CRM Implementation",
            "E-commerce Platform",
            "API Integration",
            "Cloud Infrastructure",
            "DevOps Pipeline",
            "AI Model Training",
            "Database Optimization",
            "UI/UX Overhaul",
            "Payment System Upgrade",
            "Content Management System",
            "Marketing Automation",
            "Analytics Dashboard",
            "IoT Solution",
            "Blockchain Prototype",
            "AR/VR Experience",
            "Cybersecurity Audit",
            "Legacy System Modernization",
        ]

        descriptions = [
            "Complete overhaul of the existing system with modern technologies",
            "Implementation of new features to improve user experience",
            "Migration from old platform to new infrastructure",
            "Integration with third-party services and APIs",
            "Development of a scalable solution for future growth",
            "Performance optimization and bottleneck resolution",
            "Creation of a proof-of-concept for innovative technology",
            "Security enhancements and vulnerability patching",
            "Data processing pipeline for business intelligence",
            "Cross-platform compatibility improvements",
        ]

        self.projects = []
        for i in range(15):  # Create 15 projects
            name = f"{random.choice(project_names)} {random.randint(1, 1000)}"
            description = random.choice(descriptions)
            owner = random.choice(self.users)

            project = Project.objects.create(
                name=name, description=description, owner=owner
            )

            # Add random members (excluding owner)
            potential_members = [user for user in self.users if user != owner]
            if potential_members:
                num_members = random.randint(0, len(potential_members))
                members = random.sample(potential_members, num_members)
                project.members.set(members)

            self.projects.append(project)
            self.stdout.write(
                f"Created project {i+1}/15: {name} (Owner: {owner.email})"
            )

    def seed_tasks(self):
        self.stdout.write("\nCreating tasks...")
        task_titles = [
            "Implement user authentication",
            "Design database schema",
            "Create API endpoints",
            "Write unit tests",
            "Optimize database queries",
            "Refactor legacy code",
            "Implement payment gateway",
            "Create admin dashboard",
            "Fix browser issues",
            "Improve mobile responsiveness",
            "Add search functionality",
            "Implement file upload",
            "Set up CI/CD pipeline",
            "Write documentation",
            "Perform security audit",
            "Optimize images",
            "Implement caching",
            "Add analytics",
            "Create onboarding",
            "Fix bugs",
        ]

        task_descriptions = [
            "Implement the complete authentication flow",
            "Design a scalable database structure",
            "API endpoints should follow REST conventions",
            "Test coverage should be at least 80%",
            "Identify and optimize slow-running queries",
            "Update old code to follow best practices",
            "Integration with payment provider",
            "Dashboard with required metrics",
            "Ensure cross-browser compatibility",
            "UI should adapt to mobile devices",
            "Search across all relevant data",
            "Support multiple file formats",
            "Configure deployment pipeline",
            "Document all new features",
            "Review for security vulnerabilities",
            "Compress and optimize images",
            "Reduce database load with caching",
            "Track key user actions",
            "Smooth onboarding experience",
            "Address critical bugs",
        ]

        for i in range(100):  # Create 100 tasks
            project = random.choice(self.projects)
            title = random.choice(task_titles)
            description = random.choice(task_descriptions)
            status = random.choice(TaskStatus.choices)[0]
            assigned_to = random.choice(self.users) if random.random() > 0.2 else None
            is_archived = random.random() < 0.1

            # Create with random date in past 6 months
            days_ago = random.randint(0, 180)
            task = Task.objects.create(
                title=title,
                description=description,
                status=status,
                assigned_to=assigned_to,
                project=project,
                is_archived=is_archived,
                created_at=timezone.now() - timezone.timedelta(days=days_ago),
            )

            self.stdout.write(
                f"Created task {i+1}/100: {title} (Project: {project.name}, Status: {status})"
            )

        self.stdout.write(self.style.SUCCESS("\nSeeding complete!"))
        self.stdout.write(f"- Created {len(self.users)} users")
        self.stdout.write(f"- Created {len(self.projects)} projects")
        self.stdout.write(f"- Created 100 tasks")
