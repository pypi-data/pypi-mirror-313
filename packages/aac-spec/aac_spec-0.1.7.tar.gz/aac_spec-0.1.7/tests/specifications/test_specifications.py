from unittest import TestCase
from tempfile import TemporaryDirectory
import os
from typing import Tuple
from click.testing import CliRunner
from aac.execute.command_line import cli, initialize_cli
from aac.execute.aac_execution_result import (
    ExecutionResult,
    ExecutionStatus,
    ExecutionMessage,
    MessageLevel,
)
from aac.context.language_context import LanguageContext

from specifications.specifications_impl import plugin_name, spec_csv, before_spec_csv_check


class TestSpecifications(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.maxDiff = None

    def test_spec_csv(self):
        with TemporaryDirectory() as tempdir:
            context = LanguageContext()
            result = spec_csv(VALID_SPEC, tempdir)
            self.assertTrue(result.is_success())

            # Assert each spec has its own file.
            generated_file_names = os.listdir(tempdir)
            self.assertEqual(3, len(generated_file_names))

            self.assertIn("Subsystem.csv", generated_file_names)
            self.assertIn("Module.csv", generated_file_names)

            # Assert Subsystem.csv contents
            with open(os.path.join(tempdir, "Subsystem.csv")) as subsystem_csv_file:
                subsystem_csv_contents = subsystem_csv_file.read()
                # it's not clear what does and doesn't get quoted by the CSV writer, so eliminate quotes
                subsystem_csv_contents = subsystem_csv_contents.replace('"', "")
                # Assert csv contents are present
                self.assertIn("Spec Name,Section,ID,Requirement,Parents,Children", subsystem_csv_contents)
                self.assertIn(
                    "Subsystem,,SUB-1,When receiving a message, the subsystem shall respond with a value.,,",
                    subsystem_csv_contents,
                )
                self.assertIn("Subsystem,Other Requirements,SUB-2,Do things.,,", subsystem_csv_contents)

            # Assert Module.csv contents
            with open(os.path.join(tempdir, "Module.csv")) as module_csv_file:
                module_csv_contents = module_csv_file.read()
                # it's not clear what does and doesn't get quoted by the CSV writer, so eliminate quotes
                module_csv_contents = module_csv_contents.replace('"', "")
                # Assert csv contents are present
                self.assertIn("Spec Name,Section,ID,Requirement,Parents,Children", module_csv_contents)
                self.assertIn(
                    "Module,,MOD-1,When receiving a message, the module shall respond with a value.,SUB-1,",
                    module_csv_contents,
                )
                self.assertIn("Module,,MOD-2,When receiving a message, do things.,SUB-2,", module_csv_contents)

    def test_bad_data_spec_csv(self):
        with TemporaryDirectory() as tempdir:
            context = LanguageContext()
            result = spec_csv(INVALID_SPEC_MISSING_REQ_ID, tempdir)
            self.assertFalse(result.is_success(), "Expected Failure")



VALID_SPEC = """
req_spec:
  name: Subsystem
  description:  This is a representative subsystem requirement specification.
  requirements:
    - "SUB-1"
  sections:
    - Other Requirements
---
req_spec:
    name: Other Requirements
    description: Other requirements
    requirements:
        - "SUB-2"
---
req:
    name: SUB-1
    id: "SUB-1"
    shall: When receiving a message, the subsystem shall respond with a value.
    attributes:
        - name: TADI
          value: Test
---
req:
    name: SUB-2
    id: "SUB-2"
    shall: Do things.
    attributes:
        - name: TADI
          value: Test
---
req_spec:
  name: Module
  description:  This is a representative module requirement specification.
  requirements:
    - "MOD-1"
    - "MOD-2"
---
req:
    name: MOD-1
    id: "MOD-1"
    shall:  When receiving a message, the module shall respond with a value.
    parents:
        - "SUB-1"
    attributes:
        - name: TADI
          value: Test
---
req:
    name: MOD-2
    id: "MOD-2"
    shall:  When receiving a message, do things.
    parents:
        - "SUB-2"
    attributes:
        - name: TADI
          value: Test
"""

INVALID_SPEC_MISSING_REQ_ID = """
req_spec:
  name: Subsystem
  description:  This is a representative subsystem requirement specification.
  requirements:
    - "SUB-1"
  sections:
    - Other Requirements
---
req_spec:
    name: Other Requirements
    description: Other requirements
    requirements:
        - "SUB-2"
---
req:
    name: SUB-1
    id: "SUB-1"
    shall: When receiving a message, the subsystem shall respond with a value.
    attributes:
        - name: TADI
          value: Test
---
req:
    name: SUB-2
    id: "SUB-2"
    shall: Do things.
    attributes:
        - name: TADI
          value: Test
---
req_spec:
  name: Module
  description:  This is a representative module requirement specification.
  requirements:
    - "MOD-1"
    - "MOD-2"
---
req:
    name: MOD-1
    id: "MOD-1"
    shall:  When receiving a message, the module shall respond with a value.
    parents:
        - "SUB-3"
    attributes:
        - name: TADI
          value: Test
---
req:
    name: MOD-2
    id: "MOD-2"
    shall:  When receiving a message, do things.
    parents:
        - "SUB-2"
    attributes:
        - name: TADI
          value: Test
"""
