import django_tables2 as tables

class VMTable(tables.Table):
    vm_name = tables.Column(verbose_name="VM Name", accessor='name')
    cpu = tables.Column(verbose_name="CPU Usage")
    memory = tables.Column(verbose_name="Memory Usage")
    network = tables.Column(verbose_name="Network Usage")

    class Meta:
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-striped table-hover"}
