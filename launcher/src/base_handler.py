import tornado


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_cookie("ate_launcher")

    def has_permission(self, user, action):
        return True
