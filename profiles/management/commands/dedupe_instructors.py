from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from profiles.models import Instructor


class Command(BaseCommand):
    help = (
        "Remove duplicate instructors by name. "
        "Keeps the best candidate (active / most-linked classes), "
        "optionally deletes only inactive duplicates, and "
        "reassigns linked classes first."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--first",
            required=True,
            help="Instructor first name (case-insensitive exact match).",
        )
        parser.add_argument(
            "--last",
            required=True,
            help=(
                "Instructor last name prefix (case-insensitive "
                "startswith). Use Sulliv to match Sullivan/"
                "Sulliva typos."
            ),
        )
        parser.add_argument(
            "--include-active-duplicates",
            action="store_true",
            help=(
                "Also delete active duplicates "
                "(default only deletes inactive duplicates)."
            ),
        )
        parser.add_argument(
            "--commit",
            action="store_true",
            help=(
                "Apply changes. Without this flag, command "
                "runs in dry-run mode."
            ),
        )

    def handle(self, *args, **options):
        first = options["first"].strip()
        last_prefix = options["last"].strip()
        include_active_duplicates = options["include_active_duplicates"]
        commit = options["commit"]

        matches = list(
            Instructor.objects.select_related("user").filter(
                user__first_name__iexact=first,
                user__last_name__istartswith=last_prefix,
            )
        )

        if not matches:
            raise CommandError(
                f"No instructors found for first={first!r}, "
                f"last startswith={last_prefix!r}."
            )

        if len(matches) == 1:
            self.stdout.write(
                self.style.SUCCESS(
                    "Only one matching instructor found. "
                    "Nothing to deduplicate."
                )
            )
            self._print_instructors(matches)
            return

        keeper = max(matches, key=self._score)
        duplicates = [
            instructor for instructor in matches if instructor.id != keeper.id
        ]

        if not include_active_duplicates:
            duplicates = [
                instructor
                for instructor in duplicates
                if not instructor.is_active
            ]

        self.stdout.write("Matched instructors:")
        self._print_instructors(matches)
        self.stdout.write("")
        self.stdout.write(
            f"Keeper instructor id={keeper.id} "
            f"({keeper.user.get_full_name() or keeper.user.username})"
        )

        if not duplicates:
            self.stdout.write(
                self.style.SUCCESS(
                    "No duplicate instructors eligible "
                    "for deletion under current flags."
                )
            )
            return

        self.stdout.write("Duplicate instructors targeted for removal:")
        self._print_instructors(duplicates)

        if not commit:
            self.stdout.write(
                self.style.WARNING(
                    "Dry run only. Re-run with --commit to apply changes."
                )
            )
            return

        with transaction.atomic():
            for duplicate in duplicates:
                linked_classes_qs = duplicate.classes.all()
                linked_count = linked_classes_qs.count()

                if linked_count:
                    linked_classes_qs.update(instructor=keeper)
                    self.stdout.write(
                        f"Reassigned {linked_count} class(es) "
                        f"from instructor id={duplicate.id} "
                        f"to keeper id={keeper.id}."
                    )

                duplicate.delete()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Deleted duplicate instructor id={duplicate.id}."
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("Deduplication completed successfully.")
        )

    @staticmethod
    def _score(instructor):
        class_count = instructor.classes.count()
        return (
            1 if instructor.is_active else 0,
            class_count,
            instructor.id,
        )

    def _print_instructors(self, instructors):
        for instructor in sorted(instructors, key=lambda item: item.id):
            name = instructor.user.get_full_name() or instructor.user.username
            class_count = instructor.classes.count()
            self.stdout.write(
                f"  - id={instructor.id}, name={name}, "
                f"active={instructor.is_active}, "
                f"classes={class_count}, user={instructor.user.username}"
            )
