from test_ExternalLM_cpu import TestExternalLM


class TestExternalLMGPU(TestExternalLM):

    def test_d_model_with_quant(self):
        self.logger.info("Test ExternalLM with quantization")
        test_config = {
            "load_in_8bit": True,
            "load_in_4bit": False
        }
        model = self.generate_model(quantization_config=test_config)
        output = model(input_ids=self.string_input_ids).last_hidden_state
        self.logger.info(output.shape)
        self.assertTrue((output.shape[0] == self.string_input_ids.shape[0]) and
                        (output.shape[1] == self.string_input_ids.shape[1]) and
                        (output.shape[2] == 4096))

    def test_e_qlora(self):
        self.logger.info("Test ExternalLM with qlora")
        test_config = {
            "load_in_8bit": True,
            "load_in_4bit": False
        }
        model = self.generate_model(quantization_config=test_config)
        lora_model = self.get_lora_model(model)
        output = lora_model(input_ids=self.string_input_ids).last_hidden_state
        self.logger.info(output.shape)
        self.assertTrue((output.shape[0] == self.string_input_ids.shape[0]) and
                        (output.shape[1] == self.string_input_ids.shape[1]) and
                        (output.shape[2] == 4096))
        self.logger.info("Test Finished")
