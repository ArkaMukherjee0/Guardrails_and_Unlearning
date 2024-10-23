# Guarded LLM with Multimodal Safety

This repository provides a robust framework for implementing safety guardrails in large language models (LLMs), particularly those with multimodal capabilities (handling both text and images). It focuses on preventing the model from generating harmful or inappropriate content, ensuring responsible and ethical use.

## Key Features

* **Comprehensive Safety Checks:** Employs both text and image analysis to detect harmful content.
* **Text Analysis:**  Utilizes NLP techniques (spaCy, WordNet, NLTK) for in-depth text analysis, including:
    * **Evasion Detection:** Identifies common evasion techniques like leetspeak, character substitutions, and separators.
    * **Concept Expansion:** Expands predefined harmful concepts with synonyms, variations, and potential misspellings to enhance detection.
    * **Contextual Analysis:**  Analyzes text within sliding windows to consider the context of potentially harmful words.
* **Image Analysis:** Leverages the CLIP model for image understanding and harmful content detection.
* **Strict Enforcement:** Implements strict thresholds and multiple checks at different stages (input, output, and intermediate steps) to minimize the risk of harmful content generation.
* **Graceful Handling:** Provides informative error messages and safe responses when harmful content is detected, ensuring a user-friendly experience.
* **Model-Level Guardrails:** The `GuardedModelWrapper` class seamlessly integrates with Hugging Face Transformers, wrapping the model and processor to enforce safety checks without requiring extensive code modification.
* **Customizable Configuration:**  Allows easy configuration of harmful concepts, thresholds, and severity levels through a `clip_config.json` file.
* **Logging:**  Provides detailed logging for monitoring and debugging.

## Classes

### `TextAnalyzer`

* **Purpose:** Analyzes text input for harmful content using NLP techniques.
* **Key Functionality:**
    * Preprocesses text (e.g., expands contractions).
    * Identifies and expands harmful concepts.
    * Generates variations of words to catch evasion attempts.
    * Analyzes text using regex patterns for efficient concept matching.
    * Calculates the probability of harmful content based on various factors (e.g., number of matches, unique variations).
    * Provides a `check_harmful_content` method to determine if the text exceeds predefined thresholds.

### `CLIPAnalyzer`

* **Purpose:** Analyzes images for harmful content using the CLIP model.
* **Key Functionality:**
    * Preprocesses images for CLIP input.
    * Encodes images and concepts into a shared embedding space.
    * Calculates the similarity between image embeddings and harmful concept embeddings.
    * Checks if the similarity scores exceed predefined thresholds.

### `GuardedModelWrapper`

* **Purpose:** Wraps a Hugging Face Transformer model and processor to enforce safety guardrails.
* **Key Functionality:**
    * Integrates `TextAnalyzer` and `CLIPAnalyzer` for comprehensive safety checks.
    * Wraps the `generate` and `batch_decode` methods to intercept and analyze model input and output.
    * Extracts images from various input formats.
    * Provides graceful handling of harmful content by returning safe responses.
    * Prevents direct modification of model and processor attributes to maintain security.
