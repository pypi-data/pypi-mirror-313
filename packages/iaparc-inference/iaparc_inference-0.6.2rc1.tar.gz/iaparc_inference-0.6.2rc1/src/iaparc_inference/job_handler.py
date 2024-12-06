"""
IA Parc Job Handler
"""
import uuid
from iaparc_inference.config import LOGGER
from .listener import IAPListener


class IAPJobHandler:
    def __init__(self, 
                 inputs: str, 
                 outputs: str,
                 decode=True, 
                 config_path: str = "/opt/pipeline/pipeline.json"):
        """
        Constructor for IAPJobHandler
        Arguments:
        - inputs:    Job input name
        - outputs:   Job output name
        Optional Arguments:
        - decode:    Whether to decode the output
        - config_path: Path to the pipeline configuration file        
        """
        self.uuid = str(uuid.uuid4())
        self.inputs = inputs + "." + self.uuid
        self.outputs = outputs + "." + self.uuid
        self.listener = IAPListener(
            self.handle_reply, 
            decode=decode, 
            inputs=self.outputs, 
            outputs=self.inputs, 
            config_path=config_path)
        if inputs not in self.listener.inputs:
            LOGGER.error(f"Input {inputs} not found in pipeline")
            raise ValueError(f"Input {inputs} not found in pipeline")
        if outputs not in self.listener.outputs:
            LOGGER.error(f"Output {outputs} not found in pipeline")
            raise ValueError(f"Output {outputs} not found in pipeline")
        input_item = self.listener.inputs[inputs]
        self.listener.error_queue = self.listener.queue + "." + input_item["link"] 


    # def handle_reply(self, data):
        