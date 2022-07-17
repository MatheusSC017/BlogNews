from django.db import models


class RattingField(models.PositiveIntegerField):
    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "max_value": 5,
                **kwargs,
            }
        )
