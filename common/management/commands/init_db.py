from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from common.models import Class, Subject, User, Semester, Task, AssignedTask
from django.utils import timezone
import datetime
import os
import random
import string


def create_user(username: str, is_teacher: bool):
    user, created = User.objects.get_or_create(username=username, email=f"{username}@email.com")
    if created:
        user.set_password("admin")
        user.save()
    if is_teacher:
        teachers_group = Group.objects.get(name="teachers")
        teachers_group.user_set.add(user)
    return user


def create_semesters(date: datetime, num_semesters: int):
    semesters = []
    for i in range(num_semesters):
        summer = 1 < date.month < 7
        begin = datetime.datetime.strptime(
            f"{date.year}-02-01" if summer else f"{date.year}-10-01", "%Y-%m-%d"
        ).date()
        end = datetime.datetime.strptime(
            f"{date.year}-07-31" if summer else f"{date.year + 1}-01-31", "%Y-%m-%d"
        ).date()
        semester, _ = Semester.objects.get_or_create(
            begin=begin,
            end=end,
            year=f"{date.year}",
            winter=not summer,
            active=i == 0,
            inbus_semester_id=124 + i,
        )
        semesters.append(semester)
        if summer:
            date = date.replace(month=8)
            date = date.replace(year=date.year - 1)
        else:
            date = date.replace(month=3)
    return semesters


def create_subject(name: str, abbr: str):
    subj, _ = Subject.objects.get_or_create(name=name, abbr=abbr)
    return subj


def create_class(
    code: str, teacher: User, semester: Semester, subject: Subject, day: Class.Day, time: datetime
):
    created_class, _ = Class.objects.get_or_create(
        code=code, teacher=teacher, semester=semester, subject=subject, day=day, time=time
    )
    return created_class


class Command(BaseCommand):
    SUBJECTS = [
        ("Úvod do Programovaní", "UPR"),
        ("Programovaní v Rustu", "PvR"),
        ("Biologicky Inspirované Algoritmy", "BIA"),
        ("Algoritmy 1", "ALG1"),
        ("Algoritmy 2", "ALG2"),
    ]
    NUM_STUDENTS = 10  # Num students to create overall
    NUM_CLASSES = 10  # Num classes to create overall
    NUM_TASKS = 10  # Num tasks to create for each subject in each semester
    USERNAME = "teacher"  # Username of the created user

    def handle(self, *args, **opts):
        teacher = create_user(self.USERNAME, True)
        students = [
            create_user(f"{username}{id}", False)
            for username, id in [
                (
                    "".join(random.choices(string.ascii_uppercase, k=3)),
                    "".join(random.choices(string.digits, k=3)),
                )
                for i in range(self.NUM_STUDENTS)
            ]
        ]

        date = datetime.datetime.now(tz=timezone.utc)
        semesters = create_semesters(date, 4)
        subjects = [create_subject(name, abbr) for (name, abbr) in self.SUBJECTS]
        classes: list[Class] = []
        for i in range(self.NUM_CLASSES):
            code = f"{random.choice(string.ascii_uppercase)}/{''.join(random.choices(string.digits, k=2))}"
            chosen_semester = random.choice(semesters)
            chosen_subject = random.choice(subjects)
            day = random.choice(Class.Day.choices)[0]
            time = datetime.time(
                hour=random.choice(range(7, 19)), minute=random.choice(range(0, 60, 15))
            )

            created_class = create_class(code, teacher, chosen_semester, chosen_subject, day, time)

            created_class.students.add(
                *random.sample(students, k=random.randint(1, self.NUM_STUDENTS))
            )
            classes.append(created_class)

        for semester in semesters:
            classes_from_semester = list(filter(lambda x: x.semester == semester, classes))
            for subject in subjects:
                clasess_with_subject = list(
                    filter(lambda x: x.subject == subject, classes_from_semester)
                )
                tasks: list[Task] = []
                for i in range(self.NUM_TASKS):
                    name = f"Task_{subject.abbr}_{i}"
                    code = "/".join([subject.abbr, str(semester), name.lower()])
                    created_task, _ = Task.objects.get_or_create(
                        name=name,
                        code=code,
                        subject=subject,
                        announce=True,
                        plagiarism_key=None,
                        type=random.choice(Task.TaskType.choices)[0],
                    )
                    tasks.append(created_task)

                files_to_create = [".taskid", "config.yaml", "readme.md"]
                for c in clasess_with_subject:
                    to_be_assigned_tasks = random.choices(tasks, k=random.randint(0, len(tasks)))
                    for task in to_be_assigned_tasks:
                        assigned_date = semester.begin + datetime.timedelta(
                            days=random.randint(0, (semester.end - semester.begin).days)
                        )
                        assigned_date = datetime.datetime.combine(assigned_date, datetime.time.min)
                        AssignedTask.objects.get_or_create(
                            task_id=task.pk,
                            clazz_id=c.pk,
                            defaults={
                                "assigned": timezone.make_aware(assigned_date),
                                "deadline": timezone.make_aware(
                                    assigned_date + datetime.timedelta(days=7)
                                ),
                                "max_points": random.randint(1, 5),
                            },
                        )

                        task_base_dir = task.dir()
                        os.makedirs(task_base_dir, exist_ok=True)

                        for file in files_to_create:
                            with open(os.path.join(task_base_dir, file), "a") as _:
                                continue
