from django.forms.widgets import ClearableFileInput

class MultipleImageInput(ClearableFileInput):
    allow_multiple_selected = True