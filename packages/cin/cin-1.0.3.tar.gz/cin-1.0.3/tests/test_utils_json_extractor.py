# tests/test_utils_json_extractor.py

import unittest
import json
import sys
import os

sys.path.append('src')
from cin.utils import extract_json


class TestExtractJson(unittest.TestCase):
    def test_with_json_wrapper(self):
        """
        Test extracting JSON with the ```json wrapper.
        """
        input_str = '```json\n[\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the coordinates for New York."\n            }\n        ],\n        "reasoning": "To obtain the current weather for New York, its geographic coordinates are needed."\n    },\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the coordinates for Brisbane."\n            }\n        ],\n        "reasoning": "To obtain the current weather for Brisbane, its geographic coordinates are needed."\n    },\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the coordinates for Switzerland."\n            }\n        ],\n        "reasoning": "To obtain the current weather for Switzerland, its geographic coordinates are needed."\n    }\n]\n```'
        expected = [
                {
                    "name": "Geospatial agent",
                    "parameters": [
                        {
                            "request": "I am requesting the coordinates for New York."
                        }
                    ],
                    "reasoning": "To obtain the current weather for New York, its geographic coordinates are needed."
                },
                {
                    "name": "Geospatial agent",
                    "parameters": [
                        {
                            "request": "I am requesting the coordinates for Brisbane."
                        }
                    ],
                    "reasoning": "To obtain the current weather for Brisbane, its geographic coordinates are needed."
                },
                {
                    "name": "Geospatial agent",
                    "parameters": [
                        {
                            "request": "I am requesting the coordinates for Switzerland."
                        }
                    ],
                    "reasoning": "To obtain the current weather for Switzerland, its geographic coordinates are needed."
                }
            ]
        result = json.loads(extract_json(input_str))
        self.assertEqual(result, expected, "Failed to extract JSON from the first example.")

    def test_with_json_wrapper_and_text_prior(self):
        """
        Test extracting JSON with the ```json wrapper.
        """
        input_str = 'hello im just tesitng it```json\n[\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the coordinates for New York."\n            }\n        ],\n        "reasoning": "To obtain the current weather for New York, its geographic coordinates are needed."\n    },\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the coordinates for Brisbane."\n            }\n        ],\n        "reasoning": "To obtain the current weather for Brisbane, its geographic coordinates are needed."\n    },\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the coordinates for Switzerland."\n            }\n        ],\n        "reasoning": "To obtain the current weather for Switzerland, its geographic coordinates are needed."\n    }\n]\n```'
        expected = [
                {
                    "name": "Geospatial agent",
                    "parameters": [
                        {
                            "request": "I am requesting the coordinates for New York."
                        }
                    ],
                    "reasoning": "To obtain the current weather for New York, its geographic coordinates are needed."
                },
                {
                    "name": "Geospatial agent",
                    "parameters": [
                        {
                            "request": "I am requesting the coordinates for Brisbane."
                        }
                    ],
                    "reasoning": "To obtain the current weather for Brisbane, its geographic coordinates are needed."
                },
                {
                    "name": "Geospatial agent",
                    "parameters": [
                        {
                            "request": "I am requesting the coordinates for Switzerland."
                        }
                    ],
                    "reasoning": "To obtain the current weather for Switzerland, its geographic coordinates are needed."
                }
            ]

        result = json.loads(extract_json(input_str))
        self.assertEqual(result, expected, "Failed to extract JSON from the first example.")

    def test_with_json_wrapper_and_text_after(self):
        """
        Test extracting JSON with the ```json wrapper.
        """
        input_str = '```json\n[\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the coordinates for New York."\n            }\n        ],\n        "reasoning": "To obtain the current weather for New York, its geographic coordinates are needed."\n    },\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the coordinates for Brisbane."\n            }\n        ],\n        "reasoning": "To obtain the current weather for Brisbane, its geographic coordinates are needed."\n    },\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the coordinates for Switzerland."\n            }\n        ],\n        "reasoning": "To obtain the current weather for Switzerland, its geographic coordinates are needed."\n    }\n]\n``` I am some more testing code'
        expected = [
                {
                    "name": "Geospatial agent",
                    "parameters": [
                        {
                            "request": "I am requesting the coordinates for New York."
                        }
                    ],
                    "reasoning": "To obtain the current weather for New York, its geographic coordinates are needed."
                },
                {
                    "name": "Geospatial agent",
                    "parameters": [
                        {
                            "request": "I am requesting the coordinates for Brisbane."
                        }
                    ],
                    "reasoning": "To obtain the current weather for Brisbane, its geographic coordinates are needed."
                },
                {
                    "name": "Geospatial agent",
                    "parameters": [
                        {
                            "request": "I am requesting the coordinates for Switzerland."
                        }
                    ],
                    "reasoning": "To obtain the current weather for Switzerland, its geographic coordinates are needed."
                }
            ]

        result = json.loads(extract_json(input_str))
        self.assertEqual(result, expected, "Failed to extract JSON from the first example.")

    def test_normal_multiple_json_arrays(self):
        """
        Test extracting JSON with the ```json wrapper.
        """
        input_str = '\n[\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the coordinates for New York."\n            }\n        ],\n        "reasoning": "To obtain the current weather for New York, its geographic coordinates are needed."\n    },\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the coordinates for Brisbane."\n            }\n        ],\n        "reasoning": "To obtain the current weather for Brisbane, its geographic coordinates are needed."\n    },\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the coordinates for Switzerland."\n            }\n        ],\n        "reasoning": "To obtain the current weather for Switzerland, its geographic coordinates are needed."\n    }\n]\n'
        expected = [
                {
                    "name": "Geospatial agent",
                    "parameters": [
                        {
                            "request": "I am requesting the coordinates for New York."
                        }
                    ],
                    "reasoning": "To obtain the current weather for New York, its geographic coordinates are needed."
                },
                {
                    "name": "Geospatial agent",
                    "parameters": [
                        {
                            "request": "I am requesting the coordinates for Brisbane."
                        }
                    ],
                    "reasoning": "To obtain the current weather for Brisbane, its geographic coordinates are needed."
                },
                {
                    "name": "Geospatial agent",
                    "parameters": [
                        {
                            "request": "I am requesting the coordinates for Switzerland."
                        }
                    ],
                    "reasoning": "To obtain the current weather for Switzerland, its geographic coordinates are needed."
                }
            ]
        result = json.loads(extract_json(input_str))
        self.assertEqual(result, expected, "Failed to extract JSON from the first example.")

    def test_another_test(self):
        """
        Test extracting JSON with the ```json wrapper.
        """
        input_str = '```json\n[\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the latitude and longitude for New York."\n            }\n        ],\n        "reasoning": "To obtain geographic coordinates for New York necessary for fetching current weather data."\n    },\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the latitude and longitude for Brisbane."\n            }\n        ],\n        "reasoning": "To obtain geographic coordinates for Brisbane necessary for fetching current weather data."\n    },\n    {\n        "name": "Geospatial agent",\n        "parameters": [\n            {\n                "request": "I am requesting the latitude and longitude for Switzerland."\n            }\n        ],\n        "reasoning": "To obtain geographic coordinates for Switzerland necessary for fetching current weather data."\n    }\n]\n```'
        expected = [
                    {
                        "name": "Geospatial agent",
                        "parameters": [
                            {
                                "request": "I am requesting the latitude and longitude for New York."
                            }
                        ],
                        "reasoning": "To obtain geographic coordinates for New York necessary for fetching current weather data."
                    },
                    {
                        "name": "Geospatial agent",
                        "parameters": [
                            {
                                "request": "I am requesting the latitude and longitude for Brisbane."
                            }
                        ],
                        "reasoning": "To obtain geographic coordinates for Brisbane necessary for fetching current weather data."
                    },
                    {
                        "name": "Geospatial agent",
                        "parameters": [
                            {
                                "request": "I am requesting the latitude and longitude for Switzerland."
                            }
                        ],
                        "reasoning": "To obtain geographic coordinates for Switzerland necessary for fetching current weather data."
                    }
                ]


        result = json.loads(extract_json(input_str))
        self.assertEqual(result, expected, "Failed to extract JSON from the first example.")