from django.contrib.sites.shortcuts import get_current_site

#############
# Requst and Session Utils
def get_site_from_request(request):
    if hasattr(request, 'site'):
        return request.site
    return get_current_site(request)