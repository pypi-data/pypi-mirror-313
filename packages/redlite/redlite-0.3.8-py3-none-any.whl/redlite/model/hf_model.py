from .._core import NamedModel, Message, MissingDependencyError
from .._util import sha_digest

try:
    from transformers import pipeline
except ImportError as err:
    raise MissingDependencyError("Please install transformers library") from err


class HFModel(NamedModel):
    """
    Model loaded from HuggingFace hub.

    - **hf_name** (`str`): name of the model on HuggingFace hub.
    - **pipeline_params** (`dict[str,Any]`): Other pipeline params, will be passed as-is to the
            HF pipeline constructor.
    """

    def __init__(
        self,
        hf_name: str,
        **pipeline_params,
    ):
        args = {
            "model": hf_name,
            "use_fast": False,
            **pipeline_params,
        }  # allow overwriting "model" (hacky) -MK; allow overwriting "use_fast"
        self.__pipeline = pipeline(task="text-generation", **args)

        name = "hf:" + hf_name
        if len(pipeline_params) > 0:
            obj = {x: str(pipeline_params[x]) for x in pipeline_params}
            name += "@" + sha_digest(obj)[:6]

        super().__init__(name, self.__predict)
        print(f"HFModel {hf_name} placed on device {self.__pipeline.device}")

    def __predict(self, messages: list[Message]) -> str:
        pad_token_id = self.__pipeline.tokenizer.eos_token_id
        out = self.__pipeline(
            [dict(x) for x in messages], pad_token_id=pad_token_id
        )  # deep copy messages as pipeline may mess with them
        assert out[0]["generated_text"][-1]["role"] == "assistant", out
        return out[0]["generated_text"][-1]["content"]
