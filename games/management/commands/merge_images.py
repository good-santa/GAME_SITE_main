import os
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from games.models import Game


class Command(BaseCommand):
    help = (
        "Move existing files from media/covers and media/screenshots into media/images, "
        "update DB paths, and avoid collisions by prefixing with the game id if needed."
    )

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Only show actions without moving files')

    def handle(self, *args, **opts):
        dry = opts['dry_run']
        media = Path(settings.MEDIA_ROOT)
        images_dir = media / 'images'
        images_dir.mkdir(parents=True, exist_ok=True)

        moved = 0
        for g in Game.objects.all():
            # Cover
            if g.cover and g.cover.name and g.cover.name.startswith('covers/'):
                src = media / g.cover.name
                if src.exists():
                    filename = src.name
                    dest = images_dir / filename
                    # Avoid collisions
                    if dest.exists():
                        stem, ext = os.path.splitext(filename)
                        dest = images_dir / f"{g.id}_{stem}{ext}"
                    self.stdout.write(f"Move cover: {src} -> {dest}")
                    if not dry:
                        shutil.move(str(src), str(dest))
                        g.cover.name = dest.relative_to(media).as_posix()
                        moved += 1
            # Screenshot
            if g.screenshot and g.screenshot.name and g.screenshot.name.startswith('screenshots/'):
                src = media / g.screenshot.name
                if src.exists():
                    filename = src.name
                    dest = images_dir / filename
                    if dest.exists():
                        stem, ext = os.path.splitext(filename)
                        dest = images_dir / f"{g.id}_{stem}{ext}"
                    self.stdout.write(f"Move screenshot: {src} -> {dest}")
                    if not dry:
                        shutil.move(str(src), str(dest))
                        g.screenshot.name = dest.relative_to(media).as_posix()
                        moved += 1
            if not dry:
                g.save(update_fields=['cover', 'screenshot'])

        if dry:
            self.stdout.write(self.style.WARNING('Dry-run: no changes saved.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Moved/updated {moved} file references.'))

