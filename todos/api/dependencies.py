from todos.container import Container


def get_container():
    container = Container()
    yield container
    container.session_provider.shutdown()
