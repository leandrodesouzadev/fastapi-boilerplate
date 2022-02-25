from main.infra import middleware, orm, routing, wsgi


app = wsgi.get_wsgi_application()

middleware.add_middlewares_to_wsgi_application(app)
orm.register_orm_on_wsgi_application(app)
routing.inject_routers_on_wsgi_application(app)
