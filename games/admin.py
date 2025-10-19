from django.contrib import admin
from django.conf import settings
from django.utils.text import slugify
from pathlib import Path
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'platform', 'price')
    list_display_links = ('title',)
    list_filter = ('genre', 'platform')
    search_fields = ('title', 'description')
    ordering = ('title',)
    list_per_page = 50
    fieldsets = (
        ('Основне', {
            'fields': ('title', 'description', 'genre', 'platform')
        }),
        ('Ціни', {
            'fields': ('price', 'original_price')
        }),
        ('Медіа', {
            'fields': ('cover', 'screenshot')
        }),
    )
    actions = ("attach_images_by_title", "attach_images_by_pk",)

    def _find_image(self, stem: str):
        media = Path(settings.MEDIA_ROOT)
        images_dir = media / 'images'
        covers_dir = media / 'covers'
        screenshots_dir = media / 'screenshots'
        candidates = []
        # search common extensions
        for folder in (images_dir, covers_dir, screenshots_dir):
            if not folder.exists():
                continue
            for ext in ('.jpg', '.jpeg', '.png', '.webp'):
                p = folder / f"{stem}{ext}"
                if p.exists():
                    candidates.append(p)
        return candidates[0] if candidates else None

    @admin.action(description="Прив'язати обкладинки/скріншоти за назвою (slug)")
    def attach_images_by_title(self, request, queryset):
        updated = 0
        media = Path(settings.MEDIA_ROOT)
        for g in queryset:
            stem = slugify(g.title or '')
            changed = False
            if not g.cover:
                p = self._find_image(stem)
                if p:
                    g.cover.name = p.relative_to(media).as_posix()
                    changed = True
            if not g.screenshot:
                p = self._find_image(stem + "_screenshot") or self._find_image(stem + "-screenshot") or self._find_image(stem)
                if p:
                    g.screenshot.name = p.relative_to(media).as_posix()
                    changed = True
            if changed:
                g.save(update_fields=['cover', 'screenshot'])
                updated += 1
        self.message_user(request, f"Оновлено {updated} запис(ів).")

    @admin.action(description="Прив'язати обкладинки/скріншоти за ID (pk)")
    def attach_images_by_pk(self, request, queryset):
        updated = 0
        media = Path(settings.MEDIA_ROOT)
        for g in queryset:
            stem = str(g.pk)
            changed = False
            if not g.cover:
                p = self._find_image(stem)
                if p:
                    g.cover.name = p.relative_to(media).as_posix()
                    changed = True
            if not g.screenshot:
                p = self._find_image(stem + "_screenshot") or self._find_image(stem + "-screenshot") or self._find_image(stem)
                if p:
                    g.screenshot.name = p.relative_to(media).as_posix()
                    changed = True
            if changed:
                g.save(update_fields=['cover', 'screenshot'])
                updated += 1
        self.message_user(request, f"Оновлено {updated} запис(ів).")
