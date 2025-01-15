from abc import ABC, abstractmethod

# LLMInterface is an abstract class that defines the interface for a language model.

class LLMInterface(ABC):

    @abstractmethod  # to force child classes to implement this method
    def set_generation_model(self, model_id: str):
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass

    @abstractmethod
    def generate_text(self, prompt: str, 
                      chat_history: list=[], 
                      max_output_tokens: int=None,
                      temperature: float = None
                      ):
        pass

    @abstractmethod
    def embed_text(self, text: str, document_type: str = None):
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass