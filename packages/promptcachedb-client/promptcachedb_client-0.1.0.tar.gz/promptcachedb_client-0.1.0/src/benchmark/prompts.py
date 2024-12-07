from typing import Literal

SHORT_PROMPT_PREFIX="""
Prompt caching + persistent prompt db

# Goal

- Release a library that can be used in conjunction with any HF model, that provides the following:
    - cache_activation(model, prompt)
    - run_with_activation(model, cached_prompt, prompt_suffix)
    - The cached activations should be stored in a persistent database
- I really like one of the extensions—making a publicly available prompt cache api
"""

SHORT_PROMPT_SUFFIXES = [
    "\n# Project Name",
    "\n# Next Steps",
    "\n# Potential issues",
    "\n# Thoughts",
    "\n# Key Design Decisions",
    "\n# Core Features",
    "\n# Implementation Plan",
    "\n# Testing Strategy",
    "\n# Optimization Tips",
    "\n# Future Enhancements",
    "\n# Database Options",
    "\n# Security Considerations",
    "\n# User Documentation",
    "\n# API Design",
    "\n# Performance Benchmarks",
    "\n# Scalability Concerns",
    "\n# Caching Strategy",
    "\n# Error Handling",
    "\n# Compatibility with HF Models",
    "\n# Open-source Licenses",
    "\n# Deployment Plan",
    "\n# Logging and Monitoring",
    "\n# Example Workflows",
    "\n# User Feedback Loop",
    "\n# Edge Cases",
    "\n# Community Engagement",
    "\n# Initial Release Milestones",
    "\n# Schema Design for Prompt Storage",
    "\n# Query Optimization",
    "\n# Data Retention Policies",
    "\n# Integration with Existing Tools",
    "\n# Documentation Outline",
    "\n# UI/UX for Web Interface",
    "\n# Performance Analysis",
    "\n# Code Review Checklist",
    "\n# CI/CD Pipeline Setup",
    "\n# Project Roadmap",
    "\n# User Access Controls",
    "\n# Debugging Procedures",
    "\n# API Rate Limiting",
    "\n# Customization Options",
    "\n# Model Compatibility Testing",
    "\n# Release Versioning",
    "\n# Data Backup Plan",
    "\n# Model-Specific Optimizations",
    "\n# Community Contributions",
    "\n# Load Testing Metrics",
    "\n# API Key Management",
    "\n# Documentation for Endpoints",
    "\n# Project Retrospective",
]


WIKIPEDIA_PROMPT_PREFIX="""
History

The training compute of notable large models in FLOPs vs publication date over the period 2010-2024. For overall notable models (top left), frontier models (top right), top language models (bottom left) and top models within leading companies (bottom right). The majority of these models are language models.

The training compute of notable large AI models in FLOPs vs publication date over the period 2017-2024. The majority of large models are language models or multimodal models with language capacity.
Before 2017, there were a few language models that were large as compared to capacities then available. In the 1990s, the IBM alignment models pioneered statistical language modelling. A smoothed n-gram model in 2001 trained on 0.3 billion words achieved then-SOTA (state of the art) perplexity.[5] In the 2000s, as Internet use became prevalent, some researchers constructed Internet-scale language datasets ("web as corpus"[6]), upon which they trained statistical language models.[7][8] In 2009, in most language processing tasks, statistical language models dominated over symbolic language models, as they can usefully ingest large datasets.[9]

After neural networks became dominant in image processing around 2012,[10] they were applied to language modelling as well. Google converted its translation service to Neural Machine Translation in 2016. As it was before Transformers, it was done by seq2seq deep LSTM networks.


An illustration of main components of the transformer model from the original paper, where layers were normalized after (instead of before) multiheaded attention
At the 2017 NeurIPS conference, Google researchers introduced the transformer architecture in their landmark paper "Attention Is All You Need". This paper's goal was to improve upon 2014 Seq2seq technology,[11] and was based mainly on the attention mechanism developed by Bahdanau et al. in 2014.[12] The following year in 2018, BERT was introduced and quickly became "ubiquitous".[13] Though the original transformer has both encoder and decoder blocks, BERT is an encoder-only model.

Although decoder-only GPT-1 was introduced in 2018, it was GPT-2 in 2019 that caught widespread attention because OpenAI at first deemed it too powerful to release publicly, out of fear of malicious use.[14] GPT-3 in 2020 went a step further and as of 2024 is available only via API with no offering of downloading the model to execute locally. But it was the 2022 consumer-facing browser-based ChatGPT that captured the imaginations of the general population and caused some media hype and online buzz.[15] The 2023 GPT-4 was praised for its increased accuracy and as a "holy grail" for its multimodal capabilities.[16] OpenAI did not reveal high-level architecture and the number of parameters of GPT-4.

Competing language models have for the most part been attempting to equal the GPT series, at least in terms of number of parameters.[17]

Since 2022, source-available models have been gaining popularity, especially at first with BLOOM and LLaMA, though both have restrictions on the field of use. Mistral AI's models Mistral 7B and Mixtral 8x7b have the more permissive Apache License. As of June 2024, The Instruction fine tuned variant of the Llama 3 70 billion parameter model is the most powerful open LLM according to the LMSYS Chatbot Arena Leaderboard, being more powerful than GPT-3.5 but not as powerful as GPT-4.[18]

As of 2024, the largest and most capable models are all based on the Transformer architecture. Some recent implementations are based on other architectures, such as recurrent neural network variants and Mamba (a state space model).[19][20][21]

Dataset preprocessing
See also: List of datasets for machine-learning research § Internet
Tokenization

Because machine learning algorithms process numbers rather than text, the text must be converted to numbers. In the first step, a vocabulary is decided upon, then integer indices are arbitrarily but uniquely assigned to each vocabulary entry, and finally, an embedding is associated to the integer index. Algorithms include byte-pair encoding (BPE) and WordPiece. There are also special tokens serving as control characters, such as [MASK] for masked-out token (as used in BERT), and [UNK] ("unknown") for characters not appearing in the vocabulary. Also, some special symbols are used to denote special text formatting. For example, "Ġ" denotes a preceding whitespace in RoBERTa and GPT. "##" denotes continuation of a preceding word in BERT.[22]

For example, the BPE tokenizer used by GPT-3 (Legacy) would split tokenizer: texts -> series of numerical "tokens" as

token	izer	:	 texts	 ->	series	 of	 numerical	 "	t	ok	ens	"
Tokenization also compresses the datasets. Because LLMs generally require input to be an array that is not jagged, the shorter texts must be "padded" until they match the length of the longest one. How many tokens are, on average, needed per word depends on the language of the dataset.[23][24]

BPE
Main article: Byte pair encoding
As an example, consider a tokenizer based on byte-pair encoding. In the first step, all unique characters (including blanks and punctuation marks) are treated as an initial set of n-grams (i.e. initial set of uni-grams). Successively the most frequent pair of adjacent characters is merged into a bi-gram and all instances of the pair are replaced by it. All occurrences of adjacent pairs of (previously merged) n-grams that most frequently occur together are then again merged into even lengthier n-gram, until a vocabulary of prescribed size is obtained (in case of GPT-3, the size is 50257).[25] After a tokenizer is trained, any text can be tokenized by it, as long as it does not contain characters not appearing in the initial-set of uni-grams.[26]

Problems
A token vocabulary based on the frequencies extracted from mainly English corpora uses as few tokens as possible for an average English word. An average word in another language encoded by such an English-optimized tokenizer is however split into suboptimal amount of tokens. GPT-2 tokenizer can use up to 15 times more tokens per word for some languages, for example for the Shan language from Myanmar. Even more widespread languages such as Portuguese and German have "a premium of 50%" compared to English.[27]

Greedy tokenization also causes subtle problems with text completion.[28]

Dataset cleaning
Main article: Data cleansing
In the context of training LLMs, datasets are typically cleaned by removing toxic passages from the dataset, discarding low-quality data, and de-duplication.[29] Cleaned datasets can increase training efficiency and lead to improved downstream performance.[30][31] A trained LLM can be used to clean datasets for training a further LLM.[32]

With the increasing proportion of LLM-generated content on the web, data cleaning in the future may include filtering out such content. LLM-generated content can pose a problem if the content is similar to human text (making filtering difficult) but of lower quality (degrading performance of models trained on it).[33]

Synthetic data
Main article: Synthetic data
Training of largest language models might need more linguistic data than naturally available, or that the naturally occurring data is of insufficient quality. In these cases, synthetic data might be used. Microsoft's Phi series of LLMs is trained on textbook-like data generated by another LLM.[34]

Training and architecture
See also: Fine-tuning (machine learning)
Reinforcement learning from human feedback (RLHF)
Main article: Reinforcement learning from human feedback
Reinforcement learning from human feedback (RLHF) through algorithms, such as proximal policy optimization, is used to further fine-tune a model based on a dataset of human preferences.[35]

Instruction tuning
Using "self-instruct" approaches, LLMs have been able to bootstrap correct responses, replacing any naive responses, starting from human-generated corrections of a few cases. For example, in the instruction "Write an essay about the main themes represented in Hamlet," an initial naive completion might be "If you submit the essay after March 17, your grade will be reduced by 10% for each day of delay," based on the frequency of this textual sequence in the corpus.[36]

Mixture of experts
Main article: Mixture of experts
The largest LLM may be too expensive to train and use directly. For such models, mixture of experts (MoE) can be applied, a line of research pursued by Google researchers since 2017 to train models reaching up to 1 trillion parameters.[37][38][39]

Prompt engineering, attention mechanism, and context window
See also: Prompt engineering and Attention (machine learning)
Most results previously achievable only by (costly) fine-tuning, can be achieved through prompt engineering, although limited to the scope of a single conversation (more precisely, limited to the scope of a context window).[40]


When each head calculates, according to its own criteria, how much other tokens are relevant for the "it_" token, note that the second attention head, represented by the second column, is focusing most on the first two rows, i.e. the tokens "The" and "animal", while the third column is focusing most on the bottom two rows, i.e. on "tired", which has been tokenized into two tokens.[41]
In order to find out which tokens are relevant to each other within the scope of the context window, the attention mechanism calculates "soft" weights for each token, more precisely for its embedding, by using multiple attention heads, each with its own "relevance" for calculating its own soft weights. For example, the small (i.e. 117M parameter sized) GPT-2 model has had twelve attention heads and a context window of only 1k tokens.[42] In its medium version it has 345M parameters and contains 24 layers, each with 12 attention heads. For the training with gradient descent a batch size of 512 was utilized.[26]

The largest models, such as Google's Gemini 1.5, presented in February 2024, can have a context window sized up to 1 million (context window of 10 million was also "successfully tested").[43] Other models with large context windows includes Anthropic's Claude 2.1, with a context window of up to 200k tokens.[44] Note that this maximum refers to the number of input tokens and that the maximum number of output tokens differs from the input and is often smaller. For example, the GPT-4 Turbo model has a maximum output of 4096 tokens.[45]

Length of a conversation that the model can take into account when generating its next answer is limited by the size of a context window, as well. If the length of a conversation, for example with ChatGPT, is longer than its context window, only the parts inside the context window are taken into account when generating the next answer, or the model needs to apply some algorithm to summarize the too distant parts of conversation.

The shortcomings of making a context window larger include higher computational cost and possibly diluting the focus on local context, while making it smaller can cause a model to miss an important long-range dependency. Balancing them are a matter of experimentation and domain-specific considerations.

A model may be pre-trained either to predict how the segment continues, or what is missing in the segment, given a segment from its training dataset.[46] It can be either

autoregressive (i.e. predicting how the segment continues, the way GPTs do it): for example given a segment "I like to eat", the model predicts "ice cream", or "sushi".
"masked" (i.e. filling in the parts missing from the segment, the way "BERT"[47] does it): for example, given a segment "I like to [__] [__] cream", the model predicts that "eat" and "ice" are missing.
Models may be trained on auxiliary tasks which test their understanding of the data distribution, such as Next Sentence Prediction (NSP), in which pairs of sentences are presented and the model must predict whether they appear consecutively in the training corpus.[47] During training, regularization loss is also used to stabilize training. However regularization loss is usually not used during testing and evaluation.

Infrastructure
Substantial infrastructure is necessary for training the largest models.[48][49][50]
"""

WIKIPEDIA_PROMPT_SUFFIXES = [
    "\nWhat's an LLM?",
    "\nIn order to build an LLM,",
    "\nSome shortcomings of LLMs",
    "\nHow are LLMs trained?",
    "\nWhat are the costs involved in training LLMs?",
    "\nCan LLMs learn multiple languages?",
    "\nWhy are LLMs popular for NLP?",
    "\nWhat distinguishes LLMs from other models?",
    "\nHow does tokenization affect LLM performance?",
    "\nWhat is the Transformer architecture?",
    "\nWhich companies develop LLMs?",
    "\nHow can LLMs be fine-tuned for specific tasks?",
    "\nHow do context windows limit LLMs?",
    "\nWhy are large datasets important for LLMs?",
    "\nWhat is instruction tuning?",
    "\nHow do LLMs handle different languages?",
    "\nWhat are some ethical concerns with LLMs?",
    "\nWhat is reinforcement learning from human feedback?",
    "\nWhat are the main challenges of LLMs?",
    "\nHow does the size of a context window affect an LLM?",
    "\nWhat is an autoregressive model?",
    "\nWhat are masked language models?",
    "\nWhat are some preprocessing techniques for LLMs?",
    "\nHow is synthetic data used in LLMs?",
    "\nHow can LLMs create synthetic data?",
    "\nWhat is prompt engineering?",
    "\nHow does an attention mechanism work?",
    "\nHow is RLHF implemented in LLMs?",
    "\nWhat is the difference between BERT and GPT?",
    "\nWhy is dataset cleaning important for LLMs?",
    "\nWhat is the importance of vocabulary size in tokenization?",
    "\nWhat are the latest advancements in LLM architectures?",
    "\nHow do fine-tuned models differ from pre-trained ones?",
    "\nWhat are some applications of LLMs?",
    "\nWhy do LLMs need high computational resources?",
    "\nHow is a mixture of experts used in LLMs?",
    "\nWhat are some limitations of tokenization?",
    "\nHow can LLMs be optimized for specific industries?",
    "\nWhat is the purpose of Next Sentence Prediction?",
    "\nWhat are soft weights in attention mechanisms?",
    "\nWhat is byte-pair encoding?",
    "\nHow can LLMs be evaluated?",
    "\nWhat are the memory requirements for LLMs?",
    "\nWhat impact do LLMs have on society?",
    "\nHow can LLMs process longer texts?",
    "\nWhy are attention heads used in Transformers?",
    "\nHow is overfitting avoided in LLM training?",
    "\nWhat is the significance of embedding layers?",
    "\nHow is model drift managed in LLMs?",
    "\nWhat is a multimodal LLM?",
    "\nHow does self-supervised learning apply to LLMs?",
]

PromptName = Literal["short_markdown", "wikipedia_llms"]

prompts = {
    "short_markdown": (SHORT_PROMPT_PREFIX, SHORT_PROMPT_SUFFIXES),
    "wikipedia_llms": (WIKIPEDIA_PROMPT_PREFIX, WIKIPEDIA_PROMPT_SUFFIXES),
}