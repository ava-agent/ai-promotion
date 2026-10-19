"""Offline regression tests: synthetic credentials, no HTTP requests."""

import contextlib
import importlib.util
import io
import os
from pathlib import Path
import sys
from types import ModuleType
import unittest
from unittest.mock import Mock, patch


SCRIPT = Path(__file__).resolve().parents[1] / "content/devto/2026-03/devto_publish.py"


class PublishTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("devto_publish_test", SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        self.requests = ModuleType("requests")
        self.requests.RequestException = type("SyntheticRequestError", (Exception,), {})
        self.requests.post = Mock(return_value=Mock(status_code=201))
        self.output = io.StringIO()
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.dict(os.environ, {}, clear=True))
        self.stack.enter_context(patch.dict(sys.modules, {"requests": self.requests}))
        self.stack.enter_context(patch("socket.create_connection", side_effect=AssertionError("No network")))
        self.stack.enter_context(contextlib.redirect_stdout(self.output))
        self.stack.enter_context(contextlib.redirect_stderr(self.output))
        spec.loader.exec_module(self.module)

    def test_import_does_not_publish(self):
        self.requests.post.assert_not_called()

    def test_missing_key_fails_before_file_or_network(self):
        with patch.object(Path, "read_text") as read:
            self.assertEqual(self.module.publish_article(), 1)
            read.assert_not_called()
        self.requests.post.assert_not_called()

    def test_blank_key_is_missing(self):
        os.environ["DEVTO_API_KEY"] = "  "
        self.assertEqual(self.module.publish_article(), 1)
        self.requests.post.assert_not_called()

    def test_environment_key_and_timeout(self):
        os.environ["DEVTO_API_KEY"] = "synthetic-devto-test-only"
        with patch.object(Path, "read_text", return_value="# synthetic article"):
            self.assertEqual(self.module.publish_article("article.md"), 0)
        args, kwargs = self.requests.post.call_args
        self.assertEqual(args, ("https://dev.to/api/articles",))
        self.assertEqual(kwargs["headers"]["api-key"], os.environ["DEVTO_API_KEY"])
        self.assertEqual(kwargs["timeout"], 30)
        self.assertTrue(kwargs["json"]["article"]["published"])
        self.assertNotIn(os.environ["DEVTO_API_KEY"], self.output.getvalue())
        self.assertNotIn("# synthetic article", self.output.getvalue())
        self.requests.post.return_value.json.assert_not_called()

    def test_missing_article_does_not_send(self):
        os.environ["DEVTO_API_KEY"] = "synthetic-devto-test-only"
        with patch.object(Path, "read_text", side_effect=OSError("synthetic-private-path")):
            self.assertEqual(self.module.publish_article(), 1)
        self.requests.post.assert_not_called()
        self.assertNotIn("synthetic-private-path", self.output.getvalue())

    def test_network_exception_details_not_logged(self):
        os.environ["DEVTO_API_KEY"] = "synthetic-devto-test-only"
        self.requests.post.side_effect = self.requests.RequestException(os.environ["DEVTO_API_KEY"])
        with patch.object(Path, "read_text", return_value="synthetic article"):
            self.assertEqual(self.module.publish_article(), 1)
        self.assertNotIn(os.environ["DEVTO_API_KEY"], self.output.getvalue())

    def test_http_error_only_prints_status(self):
        os.environ["DEVTO_API_KEY"] = "synthetic-devto-test-only"
        self.requests.post.return_value.status_code = 401
        with patch.object(Path, "read_text", return_value="synthetic article"):
            self.assertEqual(self.module.publish_article(), 1)
        self.assertEqual(self.output.getvalue(), "Status: 401\n")


if __name__ == "__main__":
    unittest.main()
