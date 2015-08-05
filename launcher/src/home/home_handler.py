from base_handler import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        self.render('web/index.html')
