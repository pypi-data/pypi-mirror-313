class Page_Utils:
    pass

    def map_breadcrumbs(self, request):

        breadcrumbs = [
            {'name': 'Home', 'url'  : '#'},
            #{'name': 'Section F'    , 'url': '#'},
            {'name': 'Dev', 'url': None}
        ]
        return breadcrumbs