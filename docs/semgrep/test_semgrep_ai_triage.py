import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("semgrep_ai_triage.py")


def load_triage_module():
    spec = importlib.util.spec_from_file_location("semgrep_ai_triage", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SemgrepAiTriageConfigTest(unittest.TestCase):
    def test_load_env_file_reads_simple_key_value_pairs(self):
        triage = load_triage_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text(
                "\n".join(
                    [
                        "AI_PROVIDER=openai-compatible",
                        "AI_MODEL=qwen/qwen3-coder",
                        "OPENAI_API_KEY=\"test-key\"",
                        "OPENAI_BASE_URL=https://openrouter.ai/api/v1",
                    ]
                ),
                encoding="utf-8",
            )

            values = triage.load_env_file(env_file)

        self.assertEqual(values["AI_PROVIDER"], "openai-compatible")
        self.assertEqual(values["AI_MODEL"], "qwen/qwen3-coder")
        self.assertEqual(values["OPENAI_API_KEY"], "test-key")
        self.assertEqual(values["OPENAI_BASE_URL"], "https://openrouter.ai/api/v1")

    def test_get_ai_settings_prefers_env_file_and_keeps_gemini_fallback(self):
        triage = load_triage_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text("GEMINI_API_KEY=file-gemini-key\n", encoding="utf-8")

            settings = triage.get_ai_settings({}, env_file)

        self.assertEqual(settings.provider, "gemini")
        self.assertEqual(settings.model, "gemini-2.5-flash")
        self.assertEqual(settings.api_key, "file-gemini-key")
        self.assertIsNone(settings.base_url)

    def test_get_ai_settings_supports_openai_compatible_provider(self):
        triage = load_triage_module()
        settings = triage.get_ai_settings(
            {
                "AI_PROVIDER": "openai-compatible",
                "AI_MODEL": "deepseek/deepseek-chat",
                "OPENAI_API_KEY": "openai-compatible-key",
                "OPENAI_BASE_URL": "https://openrouter.ai/api/v1",
            },
            env_file=None,
        )

        self.assertEqual(settings.provider, "openai-compatible")
        self.assertEqual(settings.model, "deepseek/deepseek-chat")
        self.assertEqual(settings.api_key, "openai-compatible-key")
        self.assertEqual(settings.base_url, "https://openrouter.ai/api/v1")


if __name__ == "__main__":
    unittest.main()
