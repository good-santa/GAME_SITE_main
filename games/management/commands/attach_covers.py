import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from games.models import Game


def find_first_by_stem(folder: Path, stem: str):
    stem = stem.lower()
    if not folder.exists():
        return None
    for name in os.listdir(folder):
        p = folder / name
        if not p.is_file():
            continue
        if p.stem.lower() == stem:
            return p
    return None


class Command(BaseCommand):
    help = (
        "Attach cover/screenshot files from MEDIA to Game objects. "
        "Looks in MEDIA_ROOT/covers and MEDIA_ROOT/screenshots by either PK or slugified title."
    )

    def add_arguments(self, parser):
        parser.add_argument('--by', choices=['pk', 'title'], default='pk', help='Match files by pk or slugified title (default: pk)')
        parser.add_argument('--screens', action='store_true', help='Also attach screenshots')
        parser.add_argument('--dry-run', action='store_true', help='Only show what would change')

    def handle(self, *args, **opts):
        by = opts['by']
        do_screens = opts['screens']
        dry = opts['dry_run']

        media = Path(settings.MEDIA_ROOT)
        # Prefer unified images/ if present, fallback to old covers/screenshots
        images_dir = media / 'images'
        covers_dir = media / 'covers'
        screens_dir = media / 'screenshots'

        updated = 0
        for g in Game.objects.all():
            # Cover
            if not g.cover:
                stem = str(g.pk) if by == 'pk' else slugify(g.title or '')
                cover_path = None
                if images_dir.exists():
                    cover_path = find_first_by_stem(images_dir, stem)
                if cover_path is None:
                    cover_path = find_first_by_stem(covers_dir, stem)
                if cover_path is not None:
                    rel = cover_path.relative_to(media).as_posix()
                    self.stdout.write(f"Set cover for [{g.id}] {g.title} -> {rel}")
                    if not dry:
                        g.cover.name = rel
                        updated += 1

            # Screenshot
            if do_screens and not g.screenshot:
                stem = str(g.pk) if by == 'pk' else slugify(g.title or '')
                shot_path = None
                if images_dir.exists():
                    shot_path = find_first_by_stem(images_dir, stem)
                if shot_path is None:
                    shot_path = find_first_by_stem(screens_dir, stem)
                if shot_path is not None:
                    rel = shot_path.relative_to(media).as_posix()
                    self.stdout.write(f"Set screenshot for [{g.id}] {g.title} -> {rel}")
                    if not dry:
                        g.screenshot.name = rel
                        updated += 1

            if not dry:
                g.save(update_fields=['cover', 'screenshot'])

        if dry:
            self.stdout.write(self.style.WARNING('Dry-run: no changes saved.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated file fields on {updated} assignments.'))
