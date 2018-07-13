from django.forms import Form
from django.forms import fields
from django.forms import widgets
from saltstack.models import Project



class PlayBookForm(Form):
    project = fields.ChoiceField(
        widget = widgets.Select(attrs={'placeholder':'选择项目组'})
    )
    description = fields.CharField(
        max_length=28,
        widget = widgets.Input(attrs={"placeholder":"输入描述信息，最大长度28字节"})
    )

    def __init__(self,*args,**kwargs):
        super(PlayBookForm,self).__init__(*args,**kwargs)
        self.fields['project'].widget.choices = Project.objects.all().values_list('id','name')