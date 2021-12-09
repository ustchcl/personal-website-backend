from website.apps.core.renderers import WebsiteJSONRenderer


class ArticleJSONRenderer(WebsiteJSONRenderer):
    object_label = 'article'
    pagination_object_label = 'articles'
    pagination_count_label = 'articlesCount'


class CommentJSONRender(WebsiteJSONRenderer):
    object = 'comment'
    pagination_object_label = 'comments'
    pagination_count_label = 'commentCount'