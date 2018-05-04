from django.shortcuts import render
from webmoni.models import MonitorData
from webmoni.models import DomainName
from webmoni.models import Project

# Create your views here.
def areas(request):
    if request.method == 'GET':
        projectList = {}
        projectsObj = Project.objects.all().order_by('id')
        for projectObj in projectsObj:
            projectList[projectObj.name] = projectObj.domainname_set.all()

        defaultDomainData = {}
        defaultDomain = DomainName.objects.first()
        defaultDomainData[defaultDomain.url] = defaultDomain.monitordata_set.all().values()
        print(defaultDomainData)
        return render(request,'show_areas.html',{'project_list':projectList,
                                                 'defaultDomainData':defaultDomainData})
