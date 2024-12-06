# Copyright (c) 2024 Huawei Technologies Co., Ltd.
# Copyright 2018 The HuggingFace Inc. team
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
from typing import Callable, Dict, Optional, List, Union, Any
import torch

from ...utils.constants import Backends, Tasks
from ...utils import is_vision_available
from ...utils.logging import get_logger, set_verbosity_info
from ..base import PTBasePipeline
from .hf_utils import PIPELINE_CREATOR_MAPPING

if is_vision_available():
    from PIL.Image import Image
    import numpy as np

    PIPELINE_INPUT_IMAGE_TYPE = Union[
        Image,
        np.ndarray,
        torch.Tensor,
        List[Image],
        List[np.ndarray],
        List[torch.Tensor],
    ]
else:
    PIPELINE_INPUT_IMAGE_TYPE = None

logger = get_logger()
set_verbosity_info()


class HFPipeline(PTBasePipeline):
    backend = Backends.transformers
    requirement_dependency = [
        "accelerate",
        "transformers",
    ]

    def __init__(
        self,
        model: str = None,
        config: str = None,
        tokenizer: str = None,
        feature_extractor: str = None,
        image_processor: str = None,
        model_kwargs: Dict = None,
        **kwargs,
    ):
        self.model = model
        self.config = config
        self.tokenizer = tokenizer
        self.feature_extractor = feature_extractor
        self.image_processor = image_processor
        self.model_kwargs = copy.deepcopy(model_kwargs)

        self.kwargs = copy.deepcopy(kwargs)
        self.task = self.kwargs.pop("task", None)
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
            config=self.config,
            tokenizer=self.tokenizer,
            feature_extractor=self.feature_extractor,
            image_processor=self.image_processor,
            model_kwargs=self.model_kwargs,
            **self.kwargs,
        )

    def __call__(self, *args, **kwargs):
        return self.pipeline(*args, **kwargs)


def _get_generated_text(res):
    if isinstance(res, str):
        return res
    elif isinstance(res, dict):
        return res["generated_text"]
    elif isinstance(res, list):
        if len(res) == 1:
            return _get_generated_text(res[0])
        else:
            return [_get_generated_text(r) for r in res]
    else:
        raise ValueError(f"Unsupported result type in _get_generated_text: {type(res)}")


class TextClassificationPipeline(HFPipeline):
    """
    Text classification pipeline using any `ModelForSequenceClassification`.
    Belowing docstring is mostly adapted from transformers.pipelines.TextClassificationPipeline

    Example:

    ```python
    >>> from openmind import pipeline

    >>> classifier = pipeline(task="text-classification", model="PyTorch-NPU/distilbert_base_uncased_finetuned_sst_2_english")

    ```

    If multiple classification labels are available (`model.config.num_labels >= 2`), the pipeline will run a softmax
    over the results. If there is a single label, the pipeline will run a sigmoid over the result. In case of regression
    tasks (`model.config.problem_type == "regression"`), will not apply any function on the output.

    """

    task = Tasks.text_classification

    def __call__(
        self,
        inputs: Union[str, List[str]],
        **kwargs,
    ):
        """
        Classify the text(s) given as inputs.

        Args:
            inputs (`str` or `List[str]` or `Dict[str]`, or `List[Dict[str]]`):
                One or several texts to classify. In order to use text pairs for your classification, you can send a dictionary containing `{"text", "text_pair"}` keys, or a list of those.
            **kwargs:
                top_k (`int`, *optional*, defaults to `1`):
                    How many results to return.
                function_to_apply (`str`, *optional*, defaults to `"default"`):
                    The function to apply to the model outputs in order to retrieve the scores. Accepts four different
                    values:

                    If this argument is not specified, then it will apply the following functions according to the number
                    of labels:

                    - If problem type is regression, will not apply any function on the output.
                    - If the model has a single label, will apply the sigmoid function on the output.
                    - If the model has several labels, will apply the softmax function on the output.

                    Possible values are:

                    - `"sigmoid"`: Applies the sigmoid function on the output.
                    - `"softmax"`: Applies the softmax function on the output.
                    - `"none"`: Does not apply any function on the output.

        Return:
            A list or a list of list of `dict`: Each result comes as list of dictionaries with the following keys:

            - **label** (`str`) -- The label predicted.
            - **score** (`float`) -- The corresponding probability.

            If `top_k` is used, one such dictionary is returned per label.
        """

        return self.pipeline(inputs=inputs, **kwargs)


class TextGenerationPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.TextGenerationPipeline

    Language generation pipeline using any `ModelWithLMHead`. This pipeline predicts the words that will follow a
    specified text prompt. When the underlying model is a conversational model, it can also accept one or more chats,
    in which case the pipeline will operate in chat mode and will continue the chat(s) by adding its response(s).
    Each chat takes the form of a list of dicts, where each dict contains "role" and "content" keys.

    Examples:

    ```python
    >>> from openmind import pipeline

    >>> generator = pipeline(task="text-generation", model="Baichuan/Baichuan2_7b_chat_pt")
    ```
    """

    task = Tasks.text_generation

    def __call__(
        self,
        text_inputs,
        **kwargs,
    ) -> Union[str, List[str]]:
        """
        Complete the prompt(s) given as inputs.

        Args:
            text_inputs (`str`, `List[str]`, List[Dict[str, str]], or `List[List[Dict[str, str]]]`):
                One or several prompts (or one list of prompts) to complete. If strings or a list of string are
                passed, this pipeline will continue each prompt. Alternatively, a "chat", in the form of a list
                of dicts with "role" and "content" keys, can be passed, or a list of such chats. When chats are passed,
                the model's chat template will be used to format them before passing them to the model.
            **kwargs:
                top_k(int): Determine the topK numbers token id as candidate. This should be a positive number.
                    If set None, it follows the setting in the configureation in the model.
                top_p(float): The accumulation probability of the candidate token ids below the top_p
                    will be select as the condaite ids. The valid value of top_p is between (0, 1]. If the value
                    is larger than 1, top_K algorithm will be enabled. If set None, it follows the setting in the
                    configureation in the model.
                return_full_text (`bool`, *optional*, defaults to `True`):
                    If set to `False` only added text is returned, otherwise the full text is returned. Cannot be
                    specified at the same time as `return_text`.
                generate_kwargs (`dict`, *optional*):
                    Additional keyword arguments to pass along to the generate method of the model (see the generate method
                    corresponding to your framework [here](./text_generation)).

        Return:
            A list or a list of lists of `dict`: Returns one of the following dictionaries (cannot return a combination
            of both `generated_text` and `generated_token_ids`):

            - **generated_text** (`str`, present when `return_text=True`) -- The generated text.
            - **generated_token_ids** (`torch.Tensor` or `tf.Tensor`, present when `return_tensors=True`) -- The token
              ids of the generated text.
        """
        res = self.pipeline(
            text_inputs,
            **kwargs,
        )

        return _get_generated_text(res)


class VisualQuestionAnsweringPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.VisualQuestionAnsweringPipeline

    Visual Question Answering pipeline using a `AutoModelForVisualQuestionAnswering`. This pipeline is currently only
    available in PyTorch.

    Example:

    ```python
    >>> from openmind import pipeline

    >>> pipeline(task="visual-question-answering", model="PyTorch-NPU/blip_vqa_base")

    """

    task = Tasks.visual_question_answering

    def __call__(
        self,
        image: Union[str, List[str], "Image", List["Image"]],
        question: Union[str, List[str]] = None,
        **kwargs,
    ):
        r"""
        Answers open-ended questions about images. The pipeline accepts several types of inputs which are detailed
        below:

        - `pipeline(image=image, question=question)`
        - `pipeline({"image": image, "question": question})`
        - `pipeline([{"image": image, "question": question}])`
        - `pipeline([{"image": image, "question": question}, {"image": image, "question": question}])`

        Args:
            image (`str`, `List[str]`, `Image` or `List[Image]`):
                The pipeline handles three types of images:

                - A string containing a http link pointing to an image
                - A string containing a local path to an image
                - An image loaded in PIL directly

                The pipeline accepts either a single image or a batch of images. If given a single image, it can be
                broadcasted to multiple questions.
            question (`str`, `List[str]`):
                The question(s) asked. If given a single question, it can be broadcasted to multiple images.
                If multiple images and questions are given, each and every question will be broadcasted to all images
                (same effect as a Cartesian product)
            **kwargs:
                top_k (`int`, *optional*, defaults to 5):
                    The number of top labels that will be returned by the pipeline. If the provided number is higher than
                    the number of labels available in the model configuration, it will default to the number of labels.
                timeout (`float`, *optional*, defaults to None):
                    The maximum time in seconds to wait for fetching images from the web. If None, no timeout is set and
                    the call may block forever.

        Return:
            A dictionary or a list of dictionaries containing the result. The dictionaries contain the following keys:

            - **label** (`str`) -- The label identified by the model.
            - **score** (`int`) -- The score attributed by the model for that label.
        """

        return self.pipeline(
            image=image,
            question=question,
            **kwargs,
        )


class ZeroShotObjectDetectionPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.ZeroShotObjectDetectionPipeline

    Zero shot object detection pipeline using `OwlViTForObjectDetection`. This pipeline predicts bounding boxes of
    objects when you provide an image and a set of `candidate_labels`.

    Example:

    ```python
    >>> from openmind import pipeline

    >>> detector = pipeline(model="PyTorch-NPU/owlvit_base_patch32", task="zero-shot-object-detection")
    """

    task = Tasks.zero_shot_object_detection

    def __call__(
        self,
        image: Union[str, "Image", List[Dict[str, Any]]],
        candidate_labels: Union[str, List[str]] = None,
        **kwargs,
    ):
        """
        Detect objects (bounding boxes & classes) in the image(s) passed as inputs.

        Args:
            image (`str`, `PIL.Image` or `List[Dict[str, Any]]`):
                The pipeline handles three types of images:

                - A string containing an http url pointing to an image
                - A string containing a local path to an image
                - An image loaded in PIL directly

            **kwargs:
                candidate_labels (`str` or `List[str]` or `List[List[str]]`):
                    What the model should recognize in the image.

                threshold (`float`, *optional*, defaults to 0.1):
                    The probability necessary to make a prediction.

                top_k (`int`, *optional*, defaults to None):
                    The number of top predictions that will be returned by the pipeline. If the provided number is `None`
                    or higher than the number of predictions available, it will default to the number of predictions.

                timeout (`float`, *optional*, defaults to None):
                    The maximum time in seconds to wait for fetching images from the web. If None, no timeout is set and
                    the call may block forever.

        Return:
            A list of lists containing prediction results, one list per input image. Each list contains dictionaries
            with the following keys:

            - **label** (`str`) -- Text query corresponding to the found object.
            - **score** (`float`) -- Score corresponding to the object (between 0 and 1).
            - **box** (`Dict[str,int]`) -- Bounding box of the detected object in image's original size. It is a
              dictionary with `x_min`, `x_max`, `y_min`, `y_max` keys.
        """

        return self.pipeline(
            image=image,
            candidate_labels=candidate_labels,
            **kwargs,
        )


class ZeroShotClassificationPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.ZeroShotClassificationPipeline

    NLI-based zero-shot classification pipeline using a `ModelForSequenceClassification` trained on NLI (natural
    language inference) tasks. Equivalent of `text-classification` pipelines, but these models don't require a
    hardcoded number of potential classes, they can be chosen at runtime. It usually means it's slower but it is
    **much** more flexible.

    Example:

    ```python
    >>> from openmind import pipeline

    >>> oracle = pipeline(task="zero-shot-classification", model="PyTorch-NPU/deberta_v3_large_zeroshot_v2.0")
    """

    task = Tasks.zero_shot_classification

    def __call__(
        self,
        sequences: Union[str, List[str]],
        *args,
        **kwargs,
    ):
        """
        Args:
            sequences (`str` or `List[str]`):
                The sequence(s) to classify, will be truncated if the model input is too large.
            candidate_labels (`str` or `List[str]`):
                The set of possible class labels to classify each sequence into. Can be a single label, a string of
                comma-separated labels, or a list of labels.

        Return:
            A `dict` or a list of `dict`: Each result comes as a dictionary with the following keys:

            - **sequence** (`str`) -- The sequence for which this is the output.
            - **labels** (`List[str]`) -- The labels sorted by order of likelihood.
            - **scores** (`List[float]`) -- The probabilities for each of the labels.
        """

        return self.pipeline(
            sequences=sequences,
            **kwargs,
        )


class DepthEstimationPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.DepthEstimationPipeline

    Depth estimation pipeline using any `AutoModelForDepthEstimation`. This pipeline predicts the depth of an image.

    Example:

    ```python
    >>> from openmind import pipeline
    >>> from tests.constants import PIPELINE_COCO_IMAGE_URL

    >>> depth_estimator = pipeline(task="depth-estimation", model="PyTorch-NPU/dpt_large")
    >>> output = depth_estimator(PIPELINE_COCO_IMAGE_URL)
    >>> output["predicted_depth"].shape
    ```
    """

    task = Tasks.depth_estimation

    def __call__(
        self,
        inputs: Union[str, List[str], "Image", List["Image"]] = None,
        **kwargs,
    ):
        """
        Predict the depth(s) of the image(s) passed as inputs.

        Args:
            inputs (`str`, `List[str]`, `Image` or `List[Image]`):
                The pipeline handles three types of images:

                - A string containing a http link pointing to an image
                - A string containing a local path to an image
                - An image loaded in PIL directly

                The pipeline accepts either a single image or a batch of images, which must then be passed as a string.
                Images in a batch must all be in the same format: all as http links, all as local paths, or all as PIL
                images.
            **kwargs:
                parameters (`Dict`, *optional*):
                    A dictionary of argument names to parameter values, to control pipeline behaviour.
                    The only parameter available right now is `timeout`, which is the length of time, in seconds,
                    that the pipeline should wait before giving up on trying to download an image.

        Return:
            A dictionary or a list of dictionaries containing result. If the input is a single image, will return a
            dictionary, if the input is a list of several images, will return a list of dictionaries corresponding to
            the images.

            The dictionaries contain the following keys:

            - **predicted_depth** (`torch.Tensor`) -- The predicted depth by the model as a `torch.Tensor`.
            - **depth** (`PIL.Image`) -- The predicted depth by the model as a `Image`.
        """
        return self.pipeline(
            inputs,
            **kwargs,
        )


class ImageToImagePipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.ImageToImagePipeline

    Image to Image pipeline using any `AutoModelForImageToImage`. This pipeline generates an image based on a previous
    image input.

    Example:

    ```python
    >>> from PIL import Image
    >>> from tests.constants import PIPELINE_COCO_IMAGE_URL

    >>> from openmind import pipeline

    >>> upscaler = pipeline("image-to-image", model="PyTorch-NPU/swin2SR_classical_sr_x2_64")
    >>> img = Image.open(requests.get(PIPELINE_COCO_IMAGE_URL, stream=True).raw)
    >>> img = img.resize((64, 64))
    >>> upscaled_img = upscaler(img)
    >>> img.size
    (64, 64)

    >>> upscaled_img.size
    (144, 144)
    ```
    """

    task = Tasks.image_to_image

    def __call__(
        self,
        images: Union[str, List[str], "Image", List["Image"]] = None,
        **kwargs,
    ) -> Union["Image", List["Image"]]:
        """
        Transform the image(s) passed as inputs.

        Args:
            images (`str`, `List[str]`, `Image` or `List[Image]`):
                The pipeline handles three types of images:

                - A string containing a http link pointing to an image
                - A string containing a local path to an image
                - An image loaded in PIL directly

                The pipeline accepts either a single image or a batch of images, which must then be passed as a string.
                Images in a batch must all be in the same format: all as http links, all as local paths, or all as PIL
                images.

        Return:
            An image (Image.Image) or a list of images (List["Image.Image"]) containing result(s). If the input is a
            single image, the return will be also a single image, if the input is a list of several images, it will
            return a list of transformed images.
        """
        return self.pipeline(
            images=images,
            **kwargs,
        )


class MaskGenerationPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.MaskGenerationPipeline

    The pipeline works in 3 steps:
        1. `preprocess`: A grid of 1024 points evenly separated is generated along with bounding boxes and point
           labels.
            For more details on how the points and bounding boxes are created, check the `_generate_crop_boxes`
            function. The image is also preprocessed using the `image_processor`. This function `yields` a minibatch of
            `points_per_batch`.

        2. `forward`: feeds the outputs of `preprocess` to the model. The image embedding is computed only once.
            Calls both `self.model.get_image_embeddings` and makes sure that the gradients are not computed, and the
            tensors and models are on the same device.

        3. `postprocess`: The most important part of the automatic mask generation happens here. Three steps
            are induced:
                - image_processor.postprocess_masks (run on each minibatch loop): takes in the raw output masks,
                  resizes them according
                to the image size, and transforms there to binary masks.
                - image_processor.filter_masks (on each minibatch loop): uses both `pred_iou_thresh` and
                  `stability_scores`. Also
                applies a variety of filters based on non maximum suppression to remove bad masks.
                - image_processor.postprocess_masks_for_amg applies the NSM on the mask to only keep relevant ones.

    Example:

    ```python
    >>> from openmind import pipeline
    >>> from tests.constants import PIPELINE_COCO_IMAGE_URL

    >>> generator = pipeline(model="PyTorch-NPU/sam_vit_base", task="mask-generation")
    >>> outputs = generator(PIPELINE_COCO_IMAGE_URL)
    ```
    """

    task = Tasks.mask_generation
    requirement_dependency = ["torchvision"]

    def __call__(self, image, *args, num_workers=None, batch_size=None, **kwargs):
        """
        Generates binary segmentation masks

        Args:
            image (`np.ndarray` or `bytes` or `str` or `dict`):
                Image or list of images.

        Return:
            `Dict`: A dictionary with the following keys:
                - **mask** (`PIL.Image`) -- A binary mask of the detected object as a PIL Image of shape `(width,
                  height)` of the original image. Returns a mask filled with zeros if no object is found.
                - **score** (*optional* `float`) -- Optionally, when the model is capable of estimating a confidence of
                  the "object" described by the label and the mask.

        """

        return self.pipeline(
            image=image,
            *args,
            num_works=num_workers,
            batch_size=batch_size,
            **kwargs,
        )


class ZeroShotImageClassificationPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.ZeroShotImageClassificationPipeline

    Zero shot image classification pipeline using `CLIPModel`. This pipeline predicts the class of an image when you
    provide an image and a set of `candidate_labels`.

    Example:

    ```python
    >>> from openmind import pipeline

    >>> classifier = pipeline(model="PyTorch-NPU/siglip_so400m_patch14_384")
    """

    task = Tasks.zero_shot_image_classification

    def __call__(
        self,
        image: Union[str, List[str], "Image", List["Image"]],
        **kwargs,
    ) -> Union[str, List[str]]:
        """
        Assign labels to the image(s) passed as inputs.

        Args:
            image (`str`, `List[str]`, `Image` or `List[Image]`):
                The pipeline handles three types of images:

                - A string containing a http link pointing to an image
                - A string containing a local path to an image
                - An image loaded in PIL directly

        Return:
            A list of dictionaries containing one entry per proposed label. Each dictionary contains the
            following keys:
            - **label** (`str`) -- One of the suggested *candidate_labels*.
            - **score** (`float`) -- The score attributed by the model to that label. It is a value between
                0 and 1, computed as the `softmax` of `logits_per_image`.
        """

        return self.pipeline(
            image,
            **kwargs,
        )


class FeatureExtractionPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.FeatureExtractionPipeline

    Feature extraction pipeline uses no model head. This pipeline extracts the hidden states from the base
    transformer, which can be used as features in downstream tasks.

    Example:

    ```python
    >>> from openmind import pipeline

    >>> extractor = pipeline(model="PyTorch-NPU/xlnet_base_cased", task="feature-extraction")
    """

    task = Tasks.feature_extraction

    def __call__(
        self,
        *args,
        **kwargs,
    ) -> Union[str, List[str]]:
        """
        Extract the features of the input(s).

        Args:
            args (`str` or `List[str]`): One or several texts (or one list of texts) to get the features of.

        Return:
            A nested list of `float`: The features computed by the model.
        """
        return self.pipeline(
            *args,
            **kwargs,
        )


class ImageClassificationPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.ImageClassificationPipeline

    Image classification pipeline using any `AutoModelForImageClassification`. This pipeline predicts the class of an
    image.

    Example:

    ```python
    >>> from openmind import pipeline

    >>> classifier = pipeline(task="image-classification", model="PyTorch-NPU/beit_base_patch16_224")
    """

    task = Tasks.image_classification

    def __call__(
        self,
        inputs: Union[str, List[str], "Image", List["Image"]],
        **kwargs,
    ) -> Union[str, List[str]]:
        """
        Assign labels to the image(s) passed as inputs.

        Args:
            inputs (`str`, `List[str]`, `Image` or `List[Image]`):
                The pipeline handles three types of images:

                - A string containing a http link pointing to an image
                - A string containing a local path to an image
                - An image loaded in PIL directly

                The pipeline accepts either a single image or a batch of images, which must then be passed as a string.
                Images in a batch must all be in the same format: all as http links, all as local paths, or all as PIL
                images.

        Return:
            A dictionary or a list of dictionaries containing result. If the input is a single image, will return a
            dictionary, if the input is a list of several images, will return a list of dictionaries corresponding to
            the images.

            The dictionaries contain the following keys:

            - **label** (`str`) -- The label identified by the model.
            - **score** (`int`) -- The score attributed by the model for that label.
        """

        return self.pipeline(
            inputs,
            **kwargs,
        )


class ImageToTextPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.ImageToTextPipeline

    Image To Text pipeline using a `AutoModelForVision2Seq`. This pipeline predicts a caption for a given image.

    Example:

    ```python
    >>> from openmind import pipeline

    >>> captioner = pipeline(model="PyTorch-NPU/blip_image_captioning_large")
    """

    task = Tasks.image_to_text

    def __call__(
        self,
        inputs: Union[str, List[str], "Image", List["Image"]],
        **kwargs,
    ) -> Union[str, List[str]]:
        """
        Assign labels to the image(s) passed as inputs.

        Args:
            inputs (`str`, `List[str]`, `Image` or `List[Image]`):
                The pipeline handles three types of images:

                - A string containing a HTTP(s) link pointing to an image
                - A string containing a local path to an image
                - An image loaded in PIL directly

                The pipeline accepts either a single image or a batch of images.

            generate_kwargs (`Dict`, *optional*):
                Pass it to send all of these arguments directly to `generate` allowing full control of this function.

        Return:
            A list or a list of list of `dict`: Each result comes as a dictionary with the following key:

            - **generated_text** (`str`) -- The generated text.
        """

        return self.pipeline(
            inputs,
            **kwargs,
        )


class Text2TextGenerationPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.Text2TextGenerationPipeline

    Pipeline for text to text generation using seq2seq models.

    Example:

    ```python
    >>> from openmind import pipeline

    >>> generator = pipeline(task="text2text-generation", model="PyTorch-NPU/flan_t5_base")
    ```
    """

    task = Tasks.text2text_generation

    def __call__(
        self,
        *args,
        **kwargs,
    ) -> Union[str, List[str]]:
        r"""
        Generate the output text(s) using text(s) given as inputs.

        Args:
            args (`str` or `List[str]`):
                Input text for the encoder.
            generate_kwargs:
                Additional keyword arguments to pass along to the generate method of the model (see the generate method
                corresponding to your framework [here](./text_generation)).

        Return:
            A list or a list of list of `dict`: Each result comes as a dictionary with the following keys:

            - **generated_text** (`str`, present when `return_text=True`) -- The generated text.
            - **generated_token_ids** (`torch.Tensor` or `tf.Tensor`, present when `return_tensors=True`) -- The token
              ids of the generated text.
        """

        return self.pipeline(
            *args,
            **kwargs,
        )


class TokenClassificationPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.TokenClassificationPipeline

    Named Entity Recognition pipeline using any `ModelForTokenClassification`.

    Example:

    ```python
    >>> from openmind import pipeline

    >>> token_classifier = pipeline(task="token-classification", model="PyTorch-NPU/camembert_ner")
    """

    task = Tasks.token_classification

    def __call__(
        self,
        inputs: Union[str, List[str]],
        **kwargs,
    ) -> Union[str, List[str]]:
        """
        Classify each token of the text(s) given as inputs.

        Args:
            inputs (`str` or `List[str]`):
                One or several texts (or one list of texts) for token classification.

        Return:
            A list or a list of list of `dict`: Each result comes as a list of dictionaries (one for each token in the
            corresponding input, or each entity if this pipeline was instantiated with an aggregation_strategy) with
            the following keys:

            - **word** (`str`) -- The token/word classified. This is obtained by decoding the selected tokens. If you
              want to have the exact string in the original sentence, use `start` and `end`.
            - **score** (`float`) -- The corresponding probability for `entity`.
            - **entity** (`str`) -- The entity predicted for that token/word (it is named *entity_group* when
              *aggregation_strategy* is not `"none"`.
            - **index** (`int`, only present when `aggregation_strategy="none"`) -- The index of the corresponding
              token in the sentence.
            - **start** (`int`, *optional*) -- The index of the start of the corresponding entity in the sentence. Only
              exists if the offsets are available within the tokenizer
            - **end** (`int`, *optional*) -- The index of the end of the corresponding entity in the sentence. Only
              exists if the offsets are available within the tokenizer
        """

        return self.pipeline(
            inputs,
            **kwargs,
        )


class FillMaskPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.FillMaskPipeline

    Masked language modeling prediction pipeline using any `ModelWithLMHead`.

    Example:

    ```python
    >>> from openmind import pipeline

    >>> fill_masker = pipeline(model="PyTorch-NPU/bert_base_uncased")
    >>> fill_masker("This is a simple [MASK].")
    ```
    """

    task = Tasks.fill_mask

    def __call__(self, inputs, *args, **kwargs):
        """
        Fill the masked token in the text(s) given as inputs.

        Args:
            args (`str` or `List[str]`):
                One or several texts (or one list of prompts) with masked tokens.
            **kwargs:
                targets (`str` or `List[str]`, *optional*):
                    When passed, the model will limit the scores to the passed targets instead of looking up in the whole
                    vocab. If the provided targets are not in the model vocab, they will be tokenized and the first
                    resulting token will be used (with a warning, and that might be slower).
                top_k (`int`, *optional*):
                    When passed, overrides the number of predictions to return.

        Return:
            A list or a list of list of `dict`: Each result comes as list of dictionaries with the following keys:

            - **sequence** (`str`) -- The corresponding input with the mask token prediction.
            - **score** (`float`) -- The corresponding probability.
            - **token** (`int`) -- The predicted token id (to replace the masked one).
            - **token_str** (`str`) -- The predicted token (to replace the masked one).
        """

        return self.pipeline(
            inputs=inputs,
            *args,
            **kwargs,
        )


class QuestionAnsweringPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.QuestionAnsweringPipeline

    Question Answering pipeline using any `ModelForQuestionAnswering`.

    Example:

    ```python
    >>> from openmind import pipeline

    >>> question_answerer = pipeline(task="question-answering", model="PyTorch-NPU/roberta_base_squad2")
    >>> outputs = question_answerer(question="Is Shakespeare British?", context="Yes, Shakespeare is British.")
    ```
    """

    task = Tasks.question_answering

    def __call__(
        self,
        *args,
        **kwargs,
    ):
        """
        Answer the question(s) given as inputs by using the context(s).

        Args:
            question (`str` or `List[str]`):
                One or several question(s) (must be used in conjunction with the `context` argument).
            context (`str` or `List[str]`):
                One or several context(s) associated with the question(s) (must be used in conjunction with the
                `question` argument).
            **kwargs:
                top_k (`int`, *optional*, defaults to 1):
                    The number of answers to return (will be chosen by order of likelihood). Note that we return less than
                    top_k answers if there are not enough options available within the context.
                doc_stride (`int`, *optional*, defaults to 128):
                    If the context is too long to fit with the question for the model, it will be split in several chunks
                    with some overlap. This argument controls the size of that overlap.
                max_answer_len (`int`, *optional*, defaults to 15):
                    The maximum length of predicted answers (e.g., only answers with a shorter length are considered).
                max_seq_len (`int`, *optional*, defaults to 384):
                    The maximum length of the total sentence (context + question) in tokens of each chunk passed to the
                    model. The context will be split in several chunks (using `doc_stride` as overlap) if needed.
                max_question_len (`int`, *optional*, defaults to 64):
                    The maximum length of the question after tokenization. It will be truncated if needed.
                handle_impossible_answer (`bool`, *optional*, defaults to `False`):
                    Whether or not we accept impossible as an answer.
                align_to_words (`bool`, *optional*, defaults to `True`):
                    Attempts to align the answer to real words. Improves quality on space separated languages. Might hurt on
                    non-space-separated languages (like Japanese or Chinese)

        Return:
            A `dict` or a list of `dict`: Each result comes as a dictionary with the following keys:

            - **score** (`float`) -- The probability associated to the answer.
            - **start** (`int`) -- The character start index of the answer (in the tokenized version of the input).
            - **end** (`int`) -- The character end index of the answer (in the tokenized version of the input).
            - **answer** (`str`) -- The answer to the question.
        """

        return self.pipeline(
            *args,
            **kwargs,
        )


class SummarizationPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.SummarizationPipeline

    Usage:

    ```python
    >>> summarizer = pipeline("summarization", model="PyTorch-NPU/bart_large_cnn")
    ```
    """

    task = Tasks.summarization

    def __call__(self, *args, **kwargs):
        r"""
        Summarize the text(s) given as inputs.

        Args:
            documents (*str* or `List[str]`):
                One or several articles (or one list of articles) to summarize.
            **kwargs:
                return_text (`bool`, *optional*, defaults to `True`):
                    Whether or not to include the decoded texts in the outputs
                return_tensors (`bool`, *optional*, defaults to `False`):
                    Whether or not to include the tensors of predictions (as token indices) in the outputs.
                clean_up_tokenization_spaces (`bool`, *optional*, defaults to `False`):
                    Whether or not to clean up the potential extra spaces in the text output.
                generate_kwargs:
                    Additional keyword arguments to pass along to the generate method of the model (see the generate method
                    corresponding to your framework [here](./text_generation)).

        Return:
            A list or a list of list of `dict`: Each result comes as a dictionary with the following keys:

            - **summary_text** (`str`, present when `return_text=True`) -- The summary of the corresponding input.
            - **summary_token_ids** (`torch.Tensor` or `tf.Tensor`, present when `return_tensors=True`) -- The token
              ids of the summary.
        """

        return self.pipeline(
            *args,
            **kwargs,
        )


class TableQuestionAnsweringPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.TableQuestionAnsweringPipeline

    Table Question Answering pipeline using a `ModelForTableQuestionAnswering`. This pipeline is only available in
    PyTorch.

    Example:

    ```python
    >>> from openmind import pipeline

    >>> table_querier = pipeline("table-question-answering", model="PyTorch-NPU/tapas_base_finetuned_wtq")

    """

    task = Tasks.table_question_answering

    def __call__(self, *args, **kwargs):
        r"""
        Answers queries according to a table. The pipeline accepts several types of inputs which are detailed below:

        - `pipeline(table, query)`
        - `pipeline(table, [query])`
        - `pipeline(table=table, query=query)`
        - `pipeline(table=table, query=[query])`
        - `pipeline({"table": table, "query": query})`
        - `pipeline({"table": table, "query": [query]})`
        - `pipeline([{"table": table, "query": query}, {"table": table, "query": query}])`

        Args:
            table (`pd.DataFrame` or `Dict`):
                Pandas DataFrame or dictionary that will be converted to a DataFrame containing all the table values.
                See above for an example of dictionary.
            query (`str` or `List[str]`):
                Query or list of queries that will be sent to the model alongside the table.
            **kwargs:
                sequential (`bool`, *optional*, defaults to `False`):
                    Whether to do inference sequentially or as a batch. Batching is faster, but models like SQA require the
                    inference to be done sequentially to extract relations within sequences, given their conversational
                    nature.
                padding (`bool`, `str` or [`~utils.PaddingStrategy`], *optional*, defaults to `False`):
                    Activates and controls padding. Accepts the following values:

                    - `True` or `'longest'`: Pad to the longest sequence in the batch (or no padding if only a single
                    sequence if provided).
                    - `'max_length'`: Pad to a maximum length specified with the argument `max_length` or to the maximum
                    acceptable input length for the model if that argument is not provided.
                    - `False` or `'do_not_pad'` (default): No padding (i.e., can output a batch with sequences of different
                    lengths).

                truncation (`bool`, `str` or [`TapasTruncationStrategy`], *optional*, defaults to `False`):
                    Activates and controls truncation. Accepts the following values:

                    - `True` or `'drop_rows_to_fit'`: Truncate to a maximum length specified with the argument `max_length`
                    or to the maximum acceptable input length for the model if that argument is not provided. This will
                    truncate row by row, removing rows from the table.
                    - `False` or `'do_not_truncate'` (default): No truncation (i.e., can output batch with sequence lengths
                    greater than the model maximum admissible input size).


        Return:
            A dictionary or a list of dictionaries containing results: Each result is a dictionary with the following
            keys:

            - **answer** (`str`) -- The answer of the query given the table. If there is an aggregator, the answer will
              be preceded by `AGGREGATOR >`.
            - **coordinates** (`List[Tuple[int, int]]`) -- Coordinates of the cells of the answers.
            - **cells** (`List[str]`) -- List of strings made up of the answer cell values.
            - **aggregator** (`str`) -- If the model has an aggregator, this returns the aggregator.
        """

        return self.pipeline(
            *args,
            **kwargs,
        )


class TranslationPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from transformers.pipelines.TranslationPipeline

    Translates from one language to another.

    Examples:

    ```python
    >>> from openmind import pipeline

    >>> translator = pipeline("translation", model="PyTorch-NPU/t5_base")
    >>> translator("Her name is Sarsh and she lives in London.")
    ```
    """

    task = Tasks.translation

    def __call__(
        self,
        *args,
        **kwargs,
    ):
        r"""
        Translate the text(s) given as inputs.

        Args:
            args (`str` or `List[str]`):
                Texts to be translated.
            **kwargs:
                return_tensors (`bool`, *optional*, defaults to `False`):
                    Whether or not to include the tensors of predictions (as token indices) in the outputs.
                return_text (`bool`, *optional*, defaults to `True`):
                    Whether or not to include the decoded texts in the outputs.
                clean_up_tokenization_spaces (`bool`, *optional*, defaults to `False`):
                    Whether or not to clean up the potential extra spaces in the text output.
                src_lang (`str`, *optional*):
                    The language of the input. Might be required for multilingual models. Will not have any effect for
                    single pair translation models
                tgt_lang (`str`, *optional*):
                    The language of the desired output. Might be required for multilingual models. Will not have any effect
                    for single pair translation models
                generate_kwargs:
                    Additional keyword arguments to pass along to the generate method of the model (see the generate method
                    corresponding to your framework [here](./text_generation)).

        Return:
            A list or a list of list of `dict`: Each result comes as a dictionary with the following keys:

            - **translation_text** (`str`, present when `return_text=True`) -- The translation.
            - **translation_token_ids** (`torch.Tensor` or `tf.Tensor`, present when `return_tensors=True`) -- The
              token ids of the translation.
        """

        return self.pipeline(
            *args,
            **kwargs,
        )


class TextToImagePipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from diffusers.pipelines.AutoPipelineForText2Image

    Pipeline for text-to-image generation.

    Examples:

    ```python
    >>> from openmind import pipeline

    >>> pipe = pipeline("text-to-image", model="PyTorch-NPU/stable-diffusion-xl-base-1_0")
    >>> image = pipe("Astronaut in a jungle, cold color palette, muted colors, detailed, 8k")
    ```
    """

    task = Tasks.text_to_image
    backend = Backends.diffusers

    def __call__(
        self,
        prompt: Union[str, List[str]],
        seed: Optional[Union[int, List[int]]] = None,
        **kwargs,
    ):
        r"""
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
                This parameter does not support model FLUX.
            negative_prompt_2 (`str` or `List[str]`, *optional*):
                The prompt or prompts not to guide the image generation to be sent to `tokenizer_2` and
                `text_encoder_2`.
                This parameter does not support model FLUX.
            num_images_per_prompt (`int`, *optional*, defaults to 1):
                The number of images to generate per prompt.
            seed (`int` or `List[int]`, *optional*):
                Utilize to generate generator object that oversees the algorithm's state for producing
                pseudo-random numbers.

        Returns:
            The generated image(s).
        """

        if seed is not None:
            if not isinstance(seed, list):
                seed = [seed]
            generator = [torch.Generator(device="cpu").manual_seed(s) for s in seed]
        else:
            generator = None

        return self.pipeline(
            prompt,
            generator=generator,
            **kwargs,
        ).images[0]


class DiffusersImageToImagePipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from diffusers.pipelines.AutoPipelineForImage2Image

    Pipeline for image-to-image generation.

    Examples:

    ```python
    >>> from openmind import pipeline
    >>> from PIL import Image

    >>> pipe = pipeline("image-to-image", model="PyTorch-NPU/stable-diffusion-xl-base-1_0")
    >>> image = Image.open(your_image_path)
    >>> generated_image = pipe("Astronaut in a jungle, cold color palette, muted colors, detailed, 8k", image=image)
    ```
    """

    task = Tasks.image_to_image
    backend = Backends.diffusers
    requirement_dependency = ["pillow"]

    def __call__(
        self,
        prompt: Union[str, List[str]],
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
                This parameter does not support model FLUX.
            negative_prompt_2 (`str` or `List[str]`, *optional*):
                The prompt or prompts not to guide the image generation to be sent to `tokenizer_2` and
                `text_encoder_2`.
                This parameter does not support model FLUX.
            num_images_per_prompt (`int`, *optional*, defaults to 1):
                The number of images to generate per prompt.
            seed (`int` or `List[int]`, *optional*):
                Utilize to generate generator object that oversees the algorithm's state for producing
                pseudo-random numbers.

        Returns:
            The generated image(s).
        """

        if seed is not None:
            if not isinstance(seed, list):
                seed = [seed]
            generator = [torch.Generator(device="cpu").manual_seed(s) for s in seed]
        else:
            generator = None

        return self.pipeline(
            prompt,
            generator=generator,
            **kwargs,
        ).images[0]


class TextToVideoPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from diffusers.pipelines.DiffusionPipeline

    Pipeline for text-to-video generation.

    Examples:

    ```python
    >>> from openmind import pipeline

    >>> pipe = pipeline("text-to-video", model="AI-Research/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16")
    >>> video = pipe("Spiderman is surfing")
    ```
    """

    task = Tasks.text_to_video
    backend = Backends.diffusers

    def __call__(
        self,
        prompt: Union[str, List[str]],
        seed: Optional[Union[int, List[int]]] = None,
        **kwargs,
    ):
        r"""
        Function invoked when calling the pipeline for text2video generation.

        Args:
            prompt (`str` or `List[str]`):
                The prompt or prompts to guide the video generation.
            height (`int`, *optional*):
                The height in pixels of the generated video.
            width (`int`, *optional*):
                The width in pixels of the generated video.
            num_inference_steps (`int`, *optional*, defaults to 50):
                The number of denoising steps. More denoising steps usually lead to a higher quality video at the
                expense of slower inference.
            negative_prompt (`str` or `List[str]`, *optional*):
                The prompt or prompts not to guide the video generation.
                This parameter does not support model FLUX.
            seed (`int` or `List[int]`, *optional*):
                Utilize to generate generator object that oversees the algorithm's state for producing
                pseudo-random numbers.

        Returns:
            The generated video.
        """

        if seed is not None:
            if not isinstance(seed, list):
                seed = [seed]
            generator = [torch.Generator(device="cpu").manual_seed(s) for s in seed]
        else:
            generator = None

        return self.pipeline(
            prompt,
            generator=generator,
            **kwargs,
        ).frames[0]


class InpaintingPipeline(HFPipeline):
    """
    Belowing docstring is mostly adapted from diffusers.pipelines.AutoPipelineForInpainting

    Pipeline for inpainting task.

    Examples:

    ```python
    >>> from openmind import pipeline
    >>> from PIL import Image

    >>> pipe = pipeline("inpainting", model="PyTorch-NPU/stable-diffusion-xl-base-1_0")
    >>> init_image = Image.open(your_image_path)
    >>> mask_image = Image.open(your_mask_path)
    >>> image = pipe(prompt="a black cat", image=init_image, mask_image=mask_image)
    ```
    """

    task = Tasks.inpainting
    backend = Backends.diffusers
    requirement_dependency = ["pillow"]

    def __call__(
        self,
        prompt: Union[str, List[str]],
        seed: Optional[Union[int, List[int]]] = None,
        **kwargs,
    ):
        r"""
        Function invoked when calling the pipeline for inpainting task.

        Args:
            prompt (`str` or `List[str]`):
                The prompt or prompts to guide the image generation.
            prompt_2 (`str` or `List[str]`, *optional*):
                The prompt or prompts to be sent to the `tokenizer_2` and `text_encoder_2`.
            image  (`PIL.Image.Image`):
                The image(s) to modify with the pipeline.
            mask_image (`PIL.Image.Image`):
                White pixels in the mask will be repainted, while black pixels will be preserved.
            height (`int`, *optional*):
                The height in pixels of the generated image.
            width (`int`, *optional*):
                The width in pixels of the generated image.
            strength (`float`, *optional*, defaults to 0.9999):
                Conceptually, indicates how much to transform the masked portion of the reference `image`. Must be
                between 0 and 1.
            num_inference_steps (`int`, *optional*, defaults to 50):
                The number of denoising steps. More denoising steps usually lead to a higher quality image at the
                expense of slower inference.
            negative_prompt (`str` or `List[str]`, *optional*):
                The prompt or prompts not to guide the image generation.
                This parameter does not support model FLUX.
            negative_prompt_2 (`str` or `List[str]`, *optional*):
                The prompt or prompts not to guide the image generation to be sent to `tokenizer_2` and
                `text_encoder_2`.
                This parameter does not support model FLUX.
            num_images_per_prompt (`int`, *optional*, defaults to 1):
                The number of images to generate per prompt.
            seed (`int` or `List[int]`, *optional*):
                Utilize to generate generator object that oversees the algorithm's state for producing
                pseudo-random numbers.

        Returns:
            The generated image.
        """

        if seed is not None:
            if not isinstance(seed, list):
                seed = [seed]
            generator = [torch.Generator(device="cpu").manual_seed(s) for s in seed]
        else:
            generator = None

        return self.pipeline(
            prompt,
            generator=generator,
            **kwargs,
        ).images[0]
