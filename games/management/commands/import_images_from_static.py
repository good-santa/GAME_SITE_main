import os
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from games.models import Game


class Command(BaseCommand):
    help = (
        "Copy images from games/static/games/img to media/images and attach"
        " to Game.cover when filename matches game title slug or pk."
    )

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Only show what would change')

    def handle(self, *args, **opts):
        dry = opts['dry_run']
        base = Path(settings.BASE_DIR)
        src = base / 'games' / 'static' / 'games' / 'img'
        dst = Path(settings.MEDIA_ROOT) / 'images'
        dst.mkdir(parents=True, exist_ok=True)

        exts = {'.jpg', '.jpeg', '.png', '.webp'}
        updated = 0
        copied = 0
        skipped = 0

        if not src.exists():
            self.stdout.write(self.style.WARNING(f'Source folder not found: {src}'))
            return

        for name in os.listdir(src):
            p = src / name
            if not p.is_file():
                continue
            if p.suffix.lower() not in exts:
                continue
            if 'placeholder' in p.name.lower():
                continue

            stem = p.stem
            dest_name = f"{slugify(stem)}{p.suffix.lower()}"
            dest = dst / dest_name

            if not dry:
                try:
                    shutil.copyfile(p, dest)
                    copied += 1
                except Exception:
                    pass

            # Match game by pk or slugified title
            game = None
            if stem.isdigit():
                game = Game.objects.filter(pk=int(stem)).first()
            if game is None:
                s = slugify(stem)
                for g in Game.objects.all():
                    if slugify(g.title) == s:
                        game = g
                        break
            if game:
                if not game.cover:
                    rel = dest.relative_to(Path(settings.MEDIA_ROOT)).as_posix()
                    self.stdout.write(f"Set cover for [{game.id}] {game.title} -> {rel}")
                    if not dry:
                        game.cover.name = rel
                        game.save(update_fields=['cover'])
                        updated += 1
                else:
                    skipped += 1

        if dry:
            self.stdout.write(self.style.WARNING('Dry-run: no changes saved.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Copied {copied} files; updated {updated} covers; skipped {skipped} (already set).'))

