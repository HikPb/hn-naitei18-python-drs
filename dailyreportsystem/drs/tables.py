from .models import Form
from table import Table
from table.columns import Column
from django.urls import reverse_lazy

class RequestFormTable(Table):
    id = Column(field='id')
    title = Column(field='title')
    created_at = Column(field='created_at')

    class Meta:
        model = Form
        ajax = True
        ajax_source = reverse_lazy('table_data')