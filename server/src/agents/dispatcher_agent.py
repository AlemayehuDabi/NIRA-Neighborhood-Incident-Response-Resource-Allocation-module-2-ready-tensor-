from src.core.message_schema import AgentMessage

class DispatcherAgent:
    def assign_volunteer(self, state:AgentMessage):
        # find nearest responder, send task / for now send it admin
        print("final state: ", state)
        pass