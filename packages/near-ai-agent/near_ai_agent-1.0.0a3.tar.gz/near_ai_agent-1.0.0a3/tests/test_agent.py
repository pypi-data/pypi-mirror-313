import unittest
from near_ai_agent.agent import NearAIAgent

class TestNearAIAgent(unittest.TestCase):
    def test_handle_task(self):
        agent = NearAIAgent()
        self.assertEqual(agent.handle_task("greet"), "Hello! I'm your NEAR AI Agent, here to assist you.")
        self.assertEqual(agent.handle_task("help"), "Here are the things I can do: greet, help.")
        self.assertEqual(agent.handle_task("unknown"), "Task 'unknown' not recognized.")

if __name__ == "__main__":
    unittest.main()
