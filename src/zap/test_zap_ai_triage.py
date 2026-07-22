import os
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zap_ai_triage import OpenRouterConfig, build_prompt, call_openrouter, config_from_env


class OpenRouterPromptTests(unittest.TestCase):
    def test_prompt_requires_vulnerability_description_and_real_response_verification(self):
        prompt = build_prompt([], ["frontend_admin_basic.json"])

        self.assertIn("Mô tả lỗ hổng", prompt)
        self.assertIn("PoC", prompt)
        self.assertIn("phản hồi thật từ EShop", prompt)

    def test_config_prefers_openai_key_when_present(self):
        previous_openai_key = os.environ.get("OPENAI_API_KEY")
        previous_openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        os.environ["OPENAI_API_KEY"] = "test-openai-key"
        os.environ.pop("OPENROUTER_API_KEY", None)

        try:
            config = config_from_env(env_path=Path("/tmp/does-not-exist"))
            self.assertEqual(config.provider, "openai")
            self.assertEqual(config.api_key, "test-openai-key")
            self.assertEqual(config.base_url, "https://api.openai.com/v1/chat/completions")
        finally:
            if previous_openai_key is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = previous_openai_key
            if previous_openrouter_key is None:
                os.environ.pop("OPENROUTER_API_KEY", None)
            else:
                os.environ["OPENROUTER_API_KEY"] = previous_openrouter_key

    def test_openai_http_error_is_labeled_as_openai(self):
        config = OpenRouterConfig(
            provider="openai",
            api_key="test-openai-key",
            model="gpt-4o-mini",
            base_url="https://api.openai.com/v1/chat/completions",
            timeout=60,
            max_tokens=1800,
        )
        error = urllib.error.HTTPError(
            url=config.base_url,
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=mock.Mock(read=mock.Mock(return_value=b'{"error":{"message":"bad key"}}')),
        )

        with mock.patch("urllib.request.urlopen", side_effect=error):
            with self.assertRaisesRegex(RuntimeError, "OpenAI API error 401"):
                call_openrouter("prompt", config)

    def test_openrouter_402_retries_with_affordable_max_tokens(self):
        config = OpenRouterConfig(
            provider="openrouter",
            api_key="test-openrouter-key",
            model="google/gemini-2.5-flash",
            base_url="https://openrouter.ai/api/v1/chat/completions",
            timeout=60,
            max_tokens=1800,
        )
        retry_error = urllib.error.HTTPError(
            url=config.base_url,
            code=402,
            msg="Payment Required",
            hdrs={},
            fp=mock.Mock(
                read=mock.Mock(
                    return_value=(
                        b'{"error":{"message":"This request requires more credits, or fewer max_tokens. '
                        b'You requested up to 1800 tokens, but can only afford 547."}}'
                    )
                )
            ),
        )
        response = mock.Mock()
        response.__enter__ = mock.Mock(return_value=response)
        response.__exit__ = mock.Mock(return_value=None)
        response.read = mock.Mock(
            return_value=b'{"choices":[{"message":{"content":"recovered"}}]}'
        )

        with mock.patch("urllib.request.urlopen", side_effect=[retry_error, response]) as urlopen_mock:
            result = call_openrouter("prompt", config)

        self.assertEqual(result, "recovered")
        self.assertEqual(urlopen_mock.call_count, 2)
        self.assertEqual(urlopen_mock.call_args_list[1].kwargs["timeout"], 60)


if __name__ == "__main__":
    unittest.main()
