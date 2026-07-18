import importlib.util
import os
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
            env_file="",
        )

        self.assertEqual(settings.provider, "openai-compatible")
        self.assertEqual(settings.model, "deepseek/deepseek-chat")
        self.assertEqual(settings.api_key, "openai-compatible-key")
        self.assertEqual(settings.base_url, "https://openrouter.ai/api/v1")

    def test_get_ai_settings_supports_openrouter_api_key(self):
        triage = load_triage_module()
        settings = triage.get_ai_settings(
            {
                "AI_PROVIDER": "openai-compatible",
                "AI_MODEL": "google/gemini-2.5-flash",
                "OPENROUTER_API_KEY": "openrouter-key",
                "OPENROUTER_BASE_URL": "https://openrouter.ai/api/v1",
            },
            env_file="",
        )

        self.assertEqual(settings.provider, "openai-compatible")
        self.assertEqual(settings.model, "google/gemini-2.5-flash")
        self.assertEqual(settings.api_key, "openrouter-key")
        self.assertEqual(settings.base_url, "https://openrouter.ai/api/v1")

    def test_triage_findings_processes_every_finding_and_writes_unique_reports(self):
        triage = load_triage_module()
        calls = []

        def fake_generate_ai_response(prompt, settings):
            calls.append(prompt)
            return f"report {len(calls)}"

        triage.generate_ai_response = fake_generate_ai_response
        settings = triage.AiSettings(
            provider="openai-compatible",
            model="google/gemini-2.5-flash",
            api_key="openrouter-key",
            base_url="https://openrouter.ai/api/v1",
        )
        findings = [
            {
                "check_id": "javascript.security.first-rule",
                "path": "backend/server.js",
                "start": {"line": 10},
                "extra": {"message": "first issue", "lines": "const a = 1;"},
            },
            {
                "check_id": "javascript.security.second-rule",
                "path": "backend/routes.js",
                "start": {"line": 20},
                "extra": {"message": "second issue", "lines": "const b = 2;"},
            },
        ]

        old_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                output_files = triage.triage_findings(findings, settings)
            finally:
                os.chdir(old_cwd)

            self.assertEqual(len(calls), 2)
            self.assertEqual(
                output_files,
                [
                    "AI_Triage_001_first-rule.md",
                    "AI_Triage_002_second-rule.md",
                ],
            )
            self.assertEqual(
                (Path(tmpdir) / "AI_Triage_001_first-rule.md").read_text(encoding="utf-8"),
                "# AI Triage Report: javascript.security.first-rule\n\nreport 1",
            )
            self.assertEqual(
                (Path(tmpdir) / "AI_Triage_002_second-rule.md").read_text(encoding="utf-8"),
                "# AI Triage Report: javascript.security.second-rule\n\nreport 2",
            )


if __name__ == "__main__":
    unittest.main()
