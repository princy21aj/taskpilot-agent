from agent.config import create_client

client, _ = create_client()
for m in client.models.list().data:
    print(m.id)