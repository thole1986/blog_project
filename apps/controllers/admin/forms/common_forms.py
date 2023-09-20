from flask_wtf import FlaskForm
from wtforms import FileField, FloatField, IntegerField
from apps.constant.forms import ERROR_NOT_VALID_VALUE


class CommonImageForm(FlaskForm):
    image = FileField('Hình đại diện')


class SubFloatField(FloatField):
    """
    Subclass that handles floats of this format 1.2 or 1,2.
    """
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(",", "."))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext(ERROR_NOT_VALID_VALUE))


class SubIntField(IntegerField):

    def process_formdata(self, valuelist):
        if not valuelist:
            return

        try:
            self.data = int(valuelist[0])
        except ValueError as exc:
            self.data = None
            raise ValueError(self.gettext(ERROR_NOT_VALID_VALUE)) from exc
