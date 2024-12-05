import unittest
import json

from insightconnect_plugin_runtime.api.endpoints import Endpoints
from insightconnect_plugin_runtime.plugin import Plugin
from insightconnect_plugin_runtime.action import Action
from insightconnect_plugin_runtime import Input
from insightconnect_plugin_runtime.connection import Connection


class TestDefinitionsAllActions(unittest.TestCase):
    def setUp(self) -> None:
        self.endpoints = Endpoints(
            logger=None,
            plugin=None,
            spec=None,
            debug=None,
            workers=None,
            threads=None,
            master_pid=None,
        )

        plugin = Plugin(
            name="Example",
            vendor="NoVendor",
            description="Example Plugin",
            version="0.0.1",
            connection=Connection(input=None),
        )

        self.endpoints.plugin = plugin

    def test_input_good(self):
        schema = json.loads(
            """
                   {
                  "type": "object",
                  "title": "Variables",
                  "properties": {
                    "name": {
                      "type": "string",
                      "title": "Name",
                      "description": "Name to say goodbye to",
                      "order": 1
                    }
                  },
                  "required": [
                    "name"
                  ]
                }
                    """
        )

        self.endpoints.plugin.actions = {
            "test": Action(
                name="test",
                description="test action",
                input=Input(schema=schema),
                output=None,
            )
        }

        expected = {
            "actionsDefinitions": [
                {
                    "identifier": "test",
                    "inputJsonSchema": {
                        "properties": {
                            "name": {
                                "description": "Name to say goodbye to",
                                "order": 1,
                                "title": "Name",
                                "type": "string",
                            }
                        },
                        "required": ["name"],
                        "title": "Variables",
                        "type": "object",
                    },
                }
            ]
        }

        actual = self.endpoints._create_action_definitions_payload()

        self.assertEqual(expected, actual)

    def test_input_good_no_inputs(self):
        schema = json.loads("{}")

        self.endpoints.plugin.actions = {
            "test": Action(
                name="test",
                description="test action",
                input=Input(schema=schema),
                output=None,
            )
        }

        expected = {
            "actionsDefinitions": [{"identifier": "test", "inputJsonSchema": {}}]
        }

        actual = self.endpoints._create_action_definitions_payload()

        self.assertEqual(expected, actual)

    def test_input_invalid_format_misspell_actionsDefinitions(self):
        schema = json.loads(
            """
                   {
                  "type": "object",
                  "title": "Variables",
                  "properties": {
                    "name": {
                      "type": "string",
                      "title": "Name",
                      "description": "Name to say goodbye to",
                      "order": 1
                    }
                  },
                  "required": [
                    "name"
                  ]
                }
                    """
        )

        self.endpoints.plugin.actions = {
            "test": Action(
                name="test",
                description="test action",
                input=Input(schema=schema),
                output=None,
            )
        }

        expected = {
            "actionDefinition": [
                {
                    "identifier": "test",
                    "inputJsonSchema": {
                        "properties": {
                            "name": {
                                "description": "Name to say goodbye to",
                                "order": 1,
                                "title": "Name",
                                "type": "string",
                            }
                        },
                        "required": ["name"],
                        "title": "Variables",
                        "type": "object",
                    },
                }
            ]
        }

        actual = self.endpoints._create_action_definitions_payload()

        self.assertNotEqual(expected, actual)

    def test_input_invalid_format_missing_identifier(self):
        schema = json.loads(
            """
                   {
                  "type": "object",
                  "title": "Variables",
                  "properties": {
                    "name": {
                      "type": "string",
                      "title": "Name",
                      "description": "Name to say goodbye to",
                      "order": 1
                    }
                  },
                  "required": [
                    "name"
                  ]
                }
                    """
        )

        self.endpoints.plugin.actions = {
            "test": Action(
                name="test",
                description="test action",
                input=Input(schema=schema),
                output=None,
            )
        }

        expected = {
            "actionsDefinitions": [
                {
                    "inputJsonSchema": {
                        "properties": {
                            "name": {
                                "description": "Name to say goodbye to",
                                "order": 1,
                                "title": "Name",
                                "type": "string",
                            }
                        },
                        "required": ["name"],
                        "title": "Variables",
                        "type": "object",
                    }
                }
            ]
        }

        actual = self.endpoints._create_action_definitions_payload()

        self.assertNotEqual(expected, actual)
