from website.apps.core.renderers import WebsiteJSONRenderer

class UserJsonRenderer(WebsiteJSONRenderer):
    charset = 'utf-8'
    object_label = 'user'
    pagination_object_label = 'users'
    pagination_object_count = 'usersCount'

    def render(self, data, media_type=None, renderer_context=None):
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return super(UserJsonRenderer, self).render(data)