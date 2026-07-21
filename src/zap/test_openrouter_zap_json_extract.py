import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from openrouter_zap_json_extract import build_prompt, config_from_env


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


if __name__ == "__main__":
    unittest.main()
