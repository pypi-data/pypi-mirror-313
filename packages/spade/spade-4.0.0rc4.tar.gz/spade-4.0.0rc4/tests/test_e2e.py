from spade.agent import Agent
from spade.container import Container
from pyjabber.server import Server

async def test_create_agent():
    container = Container()
    server = Server(host="localhost", client_port=5222)
    server.database_purge=True
    server.database_path="."   
    agent = Agent("test@localhost", "test")

    await server.run_server()
    await agent.start()

    assert agent.is_alive()
        