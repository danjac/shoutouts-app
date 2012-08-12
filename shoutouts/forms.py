from wtforms import (
    TextField,
    HiddenField,
    PasswordField,
    SelectField,
    SubmitField,
    FieldList,
    ValidationError,
    validators,
    widgets,
    fields,
)

from wtforms.ext.csrf import SecureForm

from .models import User

class Form(SecureForm):

   def generate_csrf_token(self, csrf_context):
        return csrf_context.session.get_csrf_token()


class QuerySetSelectField(fields.SelectFieldBase):
    widget = widgets.Select()

    def __init__(self, label=u'', validators=None, queryset=None, 
                 label_attr='', allow_blank=False, 
                 blank_text=u'---', **kwargs):
        super(QuerySetSelectField, self).__init__(label, validators, **kwargs)
        self.label_attr = label_attr
        self.allow_blank = allow_blank
        self.blank_text = blank_text
        self.queryset = queryset or []

    def iter_choices(self):
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is None)

        if not self.queryset:
            return

        self.queryset.rewind()
        for obj in self.queryset:
            label = self.label_attr and getattr(obj, self.label_attr) or obj
            yield (obj.id, label, obj == self.data)

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '__None':
                self.data = None
            else:
                if not self.queryset:
                    self.data = None
                    return

                self.queryset.rewind()
                for obj in self.queryset:
                    if str(obj.id) == valuelist[0]:
                        self.data = obj
                        break
                else:
                    self.data = None

    def pre_validate(self, form):
        if not self.allow_blank or self.data is not None:
            if not self.data:
                raise ValidationError(u'Not a valid choice')



class ModelSelectField(QuerySetSelectField):
    def __init__(self, label=u'', validators=None, model=None, **kwargs):
        super(ModelSelectField, self).__init__(
                label, validators, queryset=model.objects, **kwargs)


class PrioritiesForm(Form):
    """
    The weekly priorities form
    """

    shoutout = ModelSelectField(model=User, allow_blank=True)

    shoutout_reason = TextField(
        validators=(
            validators.Required(),
        ),
    )

    one_pc = ModelSelectField(model=User, allow_blank=True)

    one_pc_reason = TextField()

    lessons_learned = TextField()
    tasks = FieldList(TextField(), min_entries=3)

    complete = SubmitField("I'm done")
    postpone = SubmitField("Save and finish later")


class LoginForm(Form):

    next = HiddenField()

    email = TextField(
        u"Email address",
        (
            validators.Required(),
            validators.Email(),
        )
    )

    password = PasswordField(
        u"Password",
        (
            validators.Required(),
        )
    )

    submit = SubmitField("Login")


