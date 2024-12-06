# Copyright (c) 2024 Huawei Technologies Co., Ltd.
# Copyright (c) Lepton AI, Inc. All rights reserved.
#
# Adapted from
# https://github.com/leptonai/leptonai/blob/main/leptonai/photon/hf/hf.py
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
from functools import cached_property
from typing import Callable, List, Union, Optional
import mindspore as ms

from ...utils.constants import Backends, Tasks
from ...utils import is_vision_available
from ...utils.logging import get_logger, set_verbosity_info
from ..base import MSBasePipeline
from .ms_utils import PIPELINE_CREATOR_MAPPING

if is_vision_available():
    from PIL.Image import Image
    import numpy as np

    PIPELINE_INPUT_IMAGE_TYPE = Union[
        Image,
        np.ndarray,
        ms.Tensor,
        List[Image],
        List[np.ndarray],
        List[ms.Tensor],
    ]
else:
    PIPELINE_INPUT_IMAGE_TYPE = None

logger = get_logger()
set_verbosity_info()


class MSPipeline(MSBasePipeline):
    backend = Backends.mindformers

    def __init__(
        self,
        task: str = None,
        model: str = None,
        **kwargs,
    ):
        self.task = task
        self.model = model

        self.kwargs = copy.deepcopy(kwargs)
        self.framework = self.kwargs.pop("framework", None)
        self.backend = self.kwargs.pop("backend", None)

        # check dependencies
        self.check_dependency()

        # access pipeline here to trigger download and load
        self.pipeline

    @cached_property
    def pipeline(self) -> Callable:
        try:
            pipeline_creator = PIPELINE_CREATOR_MAPPING.get(self.task).get(self.backend)
        except Exception as e:
            # If any error occurs, we issue a warning, but don't exit immediately.
            logger.warning("An error occurred while trying to get pipline creator. Error" f" details: {e}")
            pipeline_creator = None
        if pipeline_creator is None:
            raise ValueError(f"Could not find pipeline creator for {self.task}:{self.framework}:{self.backend}")

        logger.info(
            f"Creating pipeline for {self.task}(framework={self.framework}, backend={self.backend},"
            f" model={self.model}, revision={self.kwargs.get('revision')}).\n"
            "openMind download might take a while, please be patient..."
        )

        return pipeline_creator(
            task=self.task,
            model=self.model,
            **self.kwargs,
        )

    def __call__(self, *args, **kwargs):
        return self.pipeline(*args, **kwargs)


class TextGenerationPipeline(MSPipeline):
    """
    Pipeline for Text Generation

    Args:
        model (Union[PretrainedModel, Model]):
            The model used to perform task, the input should be a model instance inherited from PretrainedModel.
        tokenizer (Optional[PreTrainedTokenizer]):
            A tokenizer (None or PreTrainedTokenizer) for text processing.
        **kwargs:
            Specific parametrization of `generate_config` and/or additional model-specific kwargs that will be
            forwarded to the `forward` function of the model. Supported `generate_config` keywords can be
            checked in [`GenerationConfig`]'s documentation. Mainly used Keywords are shown below:

    Raises:
        TypeError:
            If input model and tokenizer's types are not corrected.
        ValueError:
            If the input model is not in support list.

    Examples:
        >>> from openmind import pipeline
        >>> pipe = pipeline("text-generation", model="MindSpore-Lab/glm2_6b", framework="ms", backend="mindformers")
        >>> pipe("Give me some advice on how to stay healthy.")
    """

    task = Tasks.text_generation
    requirement_dependency = ["mindformers==1.3.0"]

    def __call__(
        self,
        inputs: Union[str, List[str]],
        **kwargs,
    ) -> Union[str, List[str]]:
        return self.pipeline(
            inputs,
            **kwargs,
        )


class TextGenerationPipelineForMindNLP(MSPipeline):
    """
    Belowing docstring is mostly adapted from mindnlp.transformers.pipelines.TextGenerationPipeline

    Language generation pipeline using any `ModelWithLMHead`. This pipeline predicts the words that will follow a
    specified text prompt. When the underlying model is a conversational model, it can also accept one or more chats,
    in which case the pipeline will operate in chat mode and will continue the chat(s) by adding its response(s).
    Each chat takes the form of a list of dicts, where each dict contains "role" and "content" keys.

    Examples:

    ```python
    >>> from openmind import pipeline

    >>> generator = pipeline(task="text-generation", model="AI-Research/Qwen2-7B", framework="ms", backend="mindnlp")
    ```
    """

    task = Tasks.text_generation
    requirement_dependency = ["mindnlp>=0.4.0"]

    def __call__(
        self,
        inputs: Union[str, List[str]],
        **kwargs,
    ) -> Union[str, List[str]]:
        return self.pipeline(
            inputs,
            **kwargs,
        )


class TextToImagePipelineForMindOne(MSPipeline):
    """
    Pipeline for text-to-image generation.

    Examples:

    ```python
    >>> from openmind import pipeline

    >>> pipe = pipeline("text-to-image", model="PyTorch-NPU/stable-diffusion-xl-base-1_0", backend="mindone", framework="ms")
    >>> image = pipe("Astronaut in a jungle, cold color palette, muted colors, detailed, 8k")
    ```
    """

    task = Tasks.text_to_image
    backend = Backends.mindone
    requirement_dependency = ["mindone==0.2.0"]

    def __call__(
        self,
        prompt: Union[str, List[str]],
        prompt_2: Optional[Union[str, List[str]]] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
        num_inference_steps: int = 50,
        negative_prompt: Optional[Union[str, List[str]]] = None,
        negative_prompt_2: Optional[Union[str, List[str]]] = None,
        num_images_per_prompt: Optional[int] = 1,
        seed: Optional[Union[int, List[int]]] = None,
        **kwargs,
    ):
        """
        Function invoked when calling the pipeline for text2image generation.

        Args:
            prompt (`str` or `List[str]`):
                The prompt or prompts to guide the image generation.
            prompt_2 (`str` or `List[str]`, *optional*):
                The prompt or prompts to be sent to the `tokenizer_2` and `text_encoder_2`.
            height (`int`, *optional*):
                The height in pixels of the generated image.
            width (`int`, *optional*):
                The width in pixels of the generated image.
            num_inference_steps (`int`, *optional*, defaults to 50):
                The number of denoising steps. More denoising steps usually lead to a higher quality image at the
                expense of slower inference.
            negative_prompt (`str` or `List[str]`, *optional*):
                The prompt or prompts not to guide the image generation.
            negative_prompt_2 (`str` or `List[str]`, *optional*):
                The prompt or prompts not to guide the image generation to be sent to `tokenizer_2` and
                `text_encoder_2`.
            num_images_per_prompt (`int`, *optional*, defaults to 1):
                The number of images to generate per prompt.
            seed (`int` or `List[int]`, *optional*):
                Utilize to generate generator object that oversees the algorithm's state for producing
                pseudo-random numbers.

        Returns:
            The generated image(s).
        """
        import mindspore

        if seed is not None:
            if not isinstance(seed, list):
                seed = [seed]
            generator = [mindspore.Generator(device="cpu").manual_seed(s) for s in seed]
        else:
            generator = None

        return self.pipeline(
            prompt,
            prompt_2=prompt_2,
            height=height,
            width=width,
            num_inference_steps=num_inference_steps,
            negative_prompt=negative_prompt,
            negative_prompt_2=negative_prompt_2,
            num_images_per_prompt=num_images_per_prompt,
            generator=generator,
            **kwargs,
        )


class ImageToImagePipelineForMindOne(MSPipeline):
    """
    Belowing docstring is mostly adapted from diffusers.pipelines.AutoPipelineForImage2Image

    Pipeline for image-to-image generation.

    Examples:

    ```python
    >>> from openmind import pipeline
    >>> from PIL import Image

    >>> pipe = pipeline("image-to-image", model="PyTorch-NPU/stable-diffusion-xl-base-1_0", framework="ms", backend="mindone")
    >>> image = Image.open(your_image_path)
    >>> generated_image = pipe("Astronaut in a jungle, cold color palette, muted colors, detailed, 8k", image=image)
    ```
    """

    task = Tasks.image_to_image
    backend = Backends.mindone
    requirement_dependency = ["mindone==0.2.0"]

    def __call__(
        self,
        prompt: Union[str, List[str]],
        prompt_2: Optional[Union[str, List[str]]] = None,
        image: PIPELINE_INPUT_IMAGE_TYPE = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
        num_inference_steps: int = 50,
        negative_prompt: Optional[Union[str, List[str]]] = None,
        negative_prompt_2: Optional[Union[str, List[str]]] = None,
        num_images_per_prompt: Optional[int] = 1,
        seed: Optional[Union[int, List[int]]] = None,
        **kwargs,
    ):
        r"""
        Function invoked when calling the pipeline for image2image generation.

        Args:
            prompt (`str` or `List[str]`):
                The prompt or prompts to guide the image generation.
            prompt_2 (`str` or `List[str]`, *optional*):
                The prompt or prompts to be sent to the `tokenizer_2` and `text_encoder_2`.
            image (`torch.Tensor` or `PIL.Image.Image` or `np.ndarray` or `List[torch.Tensor]` or `List[PIL.Image.Image]` or `List[np.ndarray]`):
                The image(s) to modify with the pipeline.
            height (`int`, *optional*):
                The height in pixels of the generated image.
            width (`int`, *optional*):
                The width in pixels of the generated image.
            num_inference_steps (`int`, *optional*, defaults to 50):
                The number of denoising steps. More denoising steps usually lead to a higher quality image at the
                expense of slower inference.
            negative_prompt (`str` or `List[str]`, *optional*):
                The prompt or prompts not to guide the image generation.
            negative_prompt_2 (`str` or `List[str]`, *optional*):
                The prompt or prompts not to guide the image generation to be sent to `tokenizer_2` and
                `text_encoder_2`.
            num_images_per_prompt (`int`, *optional*, defaults to 1):
                The number of images to generate per prompt.
            seed (`int` or `List[int]`, *optional*):
                Utilize to generate generator object that oversees the algorithm's state for producing
                pseudo-random numbers.

        Returns:
            The generated image(s).
        """
        import mindspore

        if seed is not None:
            if not isinstance(seed, list):
                seed = [seed]
            generator = [mindspore.Generator(device="cpu").manual_seed(s) for s in seed]
        else:
            generator = None

        return self.pipeline(
            prompt,
            prompt_2=prompt_2,
            image=image,
            height=height,
            width=width,
            num_inference_steps=num_inference_steps,
            negative_prompt=negative_prompt,
            negative_prompt_2=negative_prompt_2,
            num_images_per_prompt=num_images_per_prompt,
            generator=generator,
            **kwargs,
        )
