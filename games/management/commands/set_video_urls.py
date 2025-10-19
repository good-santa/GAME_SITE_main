from urllib.parse import quote_plus

from django.core.management.base import BaseCommand

from games.models import Game


class Command(BaseCommand):
    help = "Set default video_url for games (YouTube search '<title> trailer')"

    def add_arguments(self, parser):
        parser.add_argument(
            "--suffix",
            default="trailer",
            help="Suffix to append to title when building the search query (default: 'trailer')",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing video_url values as well",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only show what would change without saving",
        )

    def handle(self, *args, **opts):
        suffix = (opts.get("suffix") or "").strip()
        force = bool(opts.get("force"))
        dry = bool(opts.get("dry_run"))

        updated = 0
        for g in Game.objects.all():
            if g.video_url and not force:
                continue
            query = g.title
            if suffix:
                query = f"{g.title} {suffix}"
            url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
            self.stdout.write(f"Set video_url for [{g.id}] {g.title} -> {url}")
            if not dry:
                g.video_url = url
                g.save(update_fields=["video_url"])
                updated += 1

        if dry:
            self.stdout.write(self.style.WARNING("Dry-run: no changes saved."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated {updated} rows."))

