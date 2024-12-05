from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import PositiveIntegerField
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class ProgressBarField(PositiveIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [MinValueValidator(0), MaxValueValidator(100)]
        super().__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        value = super().clean(value, model_instance)
        if value < 0 or value > 100:
            raise ValidationError(_('Value must be between 0 and 100.'))
        return value

    def get_progress_bar_html(self, value):
        """Generiert den HTML-Code für den Fortschrittsbalken."""
        value = value or 0
        return format_html(
            f'''
            <div class="progress milea-refresh-progress" id="{str(self)}">
                <div class="progress-bar progress-bar-striped progress-bar-animated bg-success" style="width: {value}%" role="progressbar" aria-valuenow="{value}" aria-valuemin="0" aria-valuemax="100" aria-label="{value}% Complete">
                <span class="visually-hidden">{value}% Complete</span>
                </div>
            </div>
            '''
        )
