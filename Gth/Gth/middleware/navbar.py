from datetime import datetime

class Page:
    def _init(self):
        self.dashboard = ''
        self.users = ''
        self.buses = ''
        self.reports = ''
        self.report_models = ''

active_const = 'active'


def process_request(request):
    page, title = get_active(request.path)
       
    return {
        'page': page, 
        'title': title
    }


def get_active(url):
    page = Page()
    title = ''
    if '/' == url:
        page.dashboard = active_const
        title = 'Dashboard'
    elif 'login' in url:
        title = 'Login'
    elif 'users' in url:
        page.users = active_const
        title = 'Users'
    elif 'services' in url:
        page.buses = active_const
        title = 'Services'
    elif 'buses' in url:
        page.buses = active_const
        title = 'Buses'
    elif 'reports' in url:
        page.reports = active_const
        title = 'Reports'
    elif 'models' in url:
        page.report_models = active_const
        title = 'Report Models'
    return page, title


