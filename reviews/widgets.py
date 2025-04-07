# reviews/widgets.py
from django import forms
from django.forms.widgets import FILE_INPUT_CONTRADICTION

class MultipleImageInput(forms.Widget):
    """
    다중 이미지 업로드를 위한 커스텀 위젯
    """
    template_name = 'widgets/multiple_image_input.html'
    input_type = 'file'
    needs_multipart_form = True
    
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['multiple'] = True
    
    def render(self, name, value, attrs=None, renderer=None):
        """
        이 위젯의 HTML 표현을 렌더링합니다.
        """
        final_attrs = self.build_attrs(self.attrs, attrs)
        final_attrs['name'] = name
        
        if 'class' not in final_attrs:
            final_attrs['class'] = 'form-control'
            
        attrs_str = " ".join([f'{k}="{v}"' for k, v in final_attrs.items()])
        return f'<input type="file" multiple="multiple" {attrs_str}>'
    
    def value_from_datadict(self, data, files, name):
        """
        파일 목록을 반환합니다.
        """
        if files:
            return files.getlist(name)
        return None
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['multiple'] = True
        return context