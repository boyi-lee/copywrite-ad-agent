from pathlib import Path
import importlib.util, json, unittest
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("framework",ROOT/"scripts/validate_framework_application.py")
F=importlib.util.module_from_spec(SPEC); assert SPEC.loader is not None; SPEC.loader.exec_module(F)

class FrameworkApplicationTests(unittest.TestCase):
    def test_callaway_traces_have_real_quotes_and_feb_chain(self):
        payload=json.loads((ROOT/"tests/fixtures/callaway-real-brief.json").read_text())
        traces=[a["application_trace"] for a in payload["angles"]]
        self.assertEqual([],F.validate({"framework_application":traces}))
    def test_label_without_trace_fails(self):
        self.assertTrue(F.validate({"framework_application":[{"selected_message_framework":"AIDAS","selected_value_framework":"FEB","final_draft_text":"x","application_steps":[]}]}))

if __name__=="__main__": unittest.main()
