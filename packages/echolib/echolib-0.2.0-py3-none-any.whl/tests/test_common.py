import unittest
from echolib.common import config_manager, HFToken, ModelPreset
from echolib.common.models import HFModel

class TestCommon(unittest.TestCase):
    def test_config_manager_load_tokens(self):
        tokens = config_manager.tokens
        self.assertIsInstance(tokens, list)
        for token in tokens:
            self.assertIsInstance(token, HFToken)
            self.assertIsInstance(token.id, int)
            self.assertIsInstance(token.name, str)
            self.assertIsInstance(token.value, str)

    def test_config_manager_load_presets(self):
        presets = config_manager.presets
        self.assertIsInstance(presets, list)
        for preset in presets:
            self.assertIsInstance(preset, ModelPreset)
            self.assertIsInstance(preset.id, int)
            self.assertIsInstance(preset.name, str)

    def test_config_manager_load_hf_models(self):
        hf_models = config_manager.hf_models
        self.assertIsInstance(hf_models, list)
        for model in hf_models:
            self.assertIsInstance(model, HFModel)
            self.assertIsInstance(model.id, int)
            self.assertIsInstance(model.name, str)
            self.assertIsInstance(model.type, str)
            self.assertIsInstance(model.kwargs, dict)
            self.assertIsInstance(model.preset, int)

if __name__ == '__main__':
    unittest.main()
