from django.core.management.base import BaseCommand
from games.models import Game


class Command(BaseCommand):
    help = "Remove duplicate Game rows keeping the earliest (by id) per (title, platform) pair."

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Only show what would be deleted')

    def handle(self, *args, **options):
        dry = options['dry_run']
        seen = {}
        to_delete = []
        for game in Game.objects.order_by('id'):
            key = (game.title.strip().lower(), game.platform.strip().lower())
            if key in seen:
                to_delete.append(game.id)
            else:
                seen[key] = game.id

        if not to_delete:
            self.stdout.write(self.style.SUCCESS('No duplicates found.'))
            return

        if dry:
            self.stdout.write(f"Would delete {len(to_delete)} rows: {to_delete}")
            return

        deleted, _ = Game.objects.filter(id__in=to_delete).delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted} duplicate rows."))

