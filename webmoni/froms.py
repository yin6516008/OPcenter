from django.forms import Form
from django.forms import fields
from django.forms import widgets

class NodeForms(Form):
    node = fields.CharField(
        max_length = 20,
        widget = widgets.Input(attrs={"class":"form-control","placeholder":"请输入节点名称"})
    )
    ip = fields.GenericIPAddressField(
        widget = widgets.Input(attrs={"class":"form-control","placeholder":"请输入节点IP地址"})
    )
    description = fields.CharField(
        max_length = 4096,
        required = False,
        widget = widgets.Textarea(attrs={"class":"form-control","cols":"30","rows":"10","placeholder":"输入节点的描述"})
    )