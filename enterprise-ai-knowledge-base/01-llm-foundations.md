# Module 1 — LLM Foundations

> **Why this module exists:** Every design decision in later modules — RAG, tool calling, agents, evaluation, cost management — is downstream of *how a language model actually works*. If you understand tokenization, embeddings, attention, context windows, and why models hallucinate, the rest of the series stops being magic and becomes engineering. This module is the physics; everything after is the architecture built on top of it.

**Module map**
1.1 What an LLM fundamentally is
1.2 Tokenization
1.3 Embeddings and vector spaces
1.4 The transformer architecture
1.5 Attention
1.6 Context windows
1.7 Training stages: pretraining → fine-tuning → instruction-tuning → alignment
1.8 Inference parameters: temperature, sampling, logprobs
1.9 Why hallucinations occur

---

## 1.1 What an LLM fundamentally is

**(a) What it is / why it matters.**
A Large Language Model is, at its core, a **next-token predictor**: given a sequence of text, it outputs a probability distribution over what the next chunk of text is likely to be. That's it. It is not a database, not a search engine, not a reasoning oracle with a fact store. Every impressive behavior — writing code, drafting a contract clause, planning a multi-step task — is an *emergent consequence* of doing next-token prediction extraordinarily well over a vast amount of text.

This single fact explains most of the enterprise architecture that follows. Because the model **reasons fluently but knows unreliably**, we bolt on retrieval (Module 3), structured knowledge (Module 4), and tools (Module 2) to supply trustworthy, current, permissioned facts and the ability to act on the world.

**Analogy.** Think of an LLM as an extraordinarily well-read improv actor. It has absorbed the *patterns* of language, code, and argument from reading nearly everything, and it can extend any prompt in a plausible, stylistically appropriate way. But ask it for a specific customer's contract renewal date and it will produce something that *sounds* exactly like a renewal date — whether or not it has ever seen the real one. The actor's job is fluency, not truth. Our job as system builders is to feed it the script (facts) and give it a phone (tools).

**(b) Mechanics.** The model is a large neural network (billions of parameters) that maps an input sequence of tokens to a probability distribution over the next token. Generation is **autoregressive**: predict one token, append it, feed the whole thing back in, predict the next, and repeat until a stop condition. There is no separate "lookup" step — knowledge is smeared across the weights as statistical regularities learned during training.

**(e) Pitfall.** The single most expensive enterprise misconception is treating the model as a knowledge base. It is a *reasoning-and-language engine*. Knowledge must be supplied or verified externally.

---

## 1.2 Tokenization

**(a) What it is / why it matters.**
Models don't read characters or words — they read **tokens**, sub-word units produced by a tokenizer. "Tokenization" is the process of chopping text into these units and mapping each to an integer ID. It matters for three practical reasons: **cost** (you're billed per token), **context limits** (windows are measured in tokens), and **behavior** (weird tokenization causes weird failures, e.g. on numbers, code, and non-English text).

**(b) Mechanics.**
The dominant scheme is **Byte-Pair Encoding (BPE)** and its variants (WordPiece, SentencePiece, tiktoken-style byte-level BPE). BPE starts from characters/bytes and iteratively merges the most frequent adjacent pairs into a fixed vocabulary (commonly 50k–200k+ tokens). Common words become single tokens ("the", " customer"); rare words split into pieces ("Salesforce" → "Sales" + "force" perhaps); arbitrary strings fall back to bytes.

Rules of thumb (English): **~4 characters per token**, or **~0.75 words per token** — so ~1,000 tokens ≈ 750 words. But treat this as a **tokenizer-specific, drifting** heuristic, not a law: it degrades for code, JSON, non-Latin scripts, and long numbers, and it changes when a vendor changes tokenizers. Concrete example: Anthropic's tokenizer introduced with **Claude Opus 4.7 (and later models) produces roughly 30% more tokens for the same text** than earlier Claude models — enough to blow a word-count-derived budget estimate.

**(c) Tools.** Each model family has its own tokenizer; token counts are **not** interchangeable across vendors — **and not even across generations from the same vendor** (recount whenever the tokenizer changes, per the Opus 4.7 example above). Use the vendor's tokenizer/counter (e.g., OpenAI's `tiktoken`, Anthropic's token-counting endpoint, HuggingFace tokenizers) to estimate cost and fit.

**(d) Decision criteria.** When estimating cost or truncation risk, always count with the *target model's* tokenizer, not a generic word count. When designing prompts that include tabular or numeric data, remember it tokenizes expensively.

**(e) Pitfalls & failure modes.**
- **Arithmetic and digit handling** are historically weak partly because numbers tokenize awkwardly (a long number can split into odd fragments). Prefer tool-calling to a calculator for anything that must be exact.
- **Non-English content** costs more tokens and can degrade quality.
- **Silent truncation:** if input exceeds the window, middle content may be dropped or the request rejected. Always budget tokens explicitly.

**(f) Enterprise example.** A CPQ assistant that pastes a 40-page master services agreement into the prompt may find the PDF is 60k tokens — blowing the budget and the cost model. This is exactly the pressure that pushes you toward **retrieval** (Module 3): fetch only the relevant clauses instead of the whole document.

---

## 1.3 Embeddings and vector spaces

**(a) What it is / why it matters.**
An **embedding** is a list of numbers (a vector, e.g. 768 or 1,536 or 3,072 dimensions) that represents the *meaning* of a piece of text as a **point in high-dimensional space**. The key property: **semantically similar things land near each other.** "Cancel my subscription" and "I want to end my plan" produce nearby vectors even with no shared words. Embeddings are the mathematical foundation of semantic search and therefore of RAG (Module 3).

**Analogy.** Imagine a vast library where books are shelved not by title but by *meaning* — cookbooks near each other, noir novels in another region, tax code in another. An embedding is the shelf coordinate. To find relevant material you don't match keywords; you go to the right neighborhood.

**(b) Mechanics.**
An embedding model (often a transformer encoder) maps text → vector such that **cosine similarity** (the angle between vectors) or dot product correlates with semantic similarity. *How does text come to have "meaningful" coordinates?* The model is trained **contrastively**: shown millions of related pairs (a question and its answer, a sentence and its paraphrase) and unrelated pairs, and tuned to **pull related pairs close together and push unrelated ones apart** in the vector space. Do that at scale and the geometry ends up encoding meaning — which is also *why* you must embed queries and documents with the **same** model (they must share one geometry) and why some models use different "query" vs. "passage" encodings (3.3). The famous (if oversimplified) illustration: the vector for "king," minus "man," plus "woman," lands near "queen" — relationships become directions in the space.

Two distinct notions of "embedding" appear in this series:
- **Token embeddings** — internal to the model; each token maps to a vector the transformer processes (Module 1.4).
- **Sentence/document embeddings** — a single vector for a whole passage, produced by a dedicated embedding model, used for retrieval (Module 3.3).

**(c) Tools/vendors.** As of mid-2026 the leaders have shifted: **Google Gemini Embedding** and open-weight **Qwen3-Embedding** top MTEB, with **Cohere Embed v4** (multimodal, long-context) and **Voyage-3.5** strong for domain retrieval; OpenAI's `text-embedding-3` family and open models (`bge`, `e5`, `nomic`, `gte`, Jina) remain widely used. The open-vs-proprietary quality gap has largely closed. They differ in dimensionality, max input length, multilingual/multimodal quality, domain fit, and cost. Some support **Matryoshka** embeddings (truncatable dimensions for a size/quality tradeoff). *(Rankings drift monthly — verify on the current MTEB leaderboard.)*

**(d) Decision criteria.** Choose an embedding model on: retrieval quality on *your* data (measure it — see 3.9), dimensionality (storage/latency cost), max input length (affects chunking), multilingual needs, and whether you can self-host for data-residency reasons. **Do not** assume the biggest model is best for retrieval; domain-tuned smaller models often win.

**(e) Pitfalls.**
- **Model mismatch:** you must embed queries and documents with the **same model**; mixing embedding models corrupts the geometry.
- **Re-embedding cost:** changing embedding models means re-indexing your whole corpus.
- **Embeddings capture semantics, not truth or recency** — two false statements about the same topic sit close together.

**(f) Enterprise example.** A support agent bot embeds every knowledge-base article and every incoming ticket. A ticket saying "the widget won't sync after the update" retrieves the article "Resolving synchronization failures following firmware upgrades" — no shared keywords, but neighbors in vector space.

---

## 1.4 The transformer architecture

**(a) What it is / why it matters.**
The **transformer** (Vaswani et al., *Attention Is All You Need*, 2017) is the neural network architecture behind virtually all modern LLMs. Its breakthrough was replacing sequential recurrence with **attention** (1.5), which lets the model process all positions in parallel and directly relate any token to any other. This is why models could scale to hundreds of billions of parameters and long contexts — parallelism is trainable on modern hardware.

**(b) Mechanics — the pipeline.**
1. **Tokenize** input → integer IDs (1.2).
2. **Embed** each token → vector; add **positional information** (so the model knows word order — modern models use rotary or learned relative position encodings).
3. Pass through a stack of **transformer blocks** (dozens to ~100+). Each block does two complementary things:
   - a **multi-head self-attention** layer — the **mixing/routing step**: each token pulls in information from other tokens to build context (1.5); and
   - a **feed-forward network (FFN)** — a per-token nonlinear transformation that is, loosely, **where much of the model's learned "knowledge" and pattern-application lives**: attention decides *what to combine*, the FFN decides *what to do with it*. (This is the mechanical hook for 1.1/1.9's "knowledge is smeared across the weights" — a lot of it sits in these FFN layers.)
   - **Residual connections** (a "bypass lane" that adds each layer's output back to its input, so a layer only has to learn a small *correction* rather than rebuild the whole signal — this is what makes 100-layer networks trainable) and **layer normalization** (rescaling activations to keep them numerically stable).
4. A final layer projects the top representation to a **distribution over the vocabulary** (the next-token probabilities).

*What is the model actually "computing" across those layers?* Roughly: early layers resolve surface features (syntax, references), middle layers build higher-level meaning and relationships, and later layers assemble the prediction — each layer refining the representation a little (the residual "small correction" idea), until the final layer reads out the next-token distribution.

**Decoder-only vs. encoder-only vs. encoder-decoder.** Most generative LLMs (GPT, Claude, Llama, Gemini) are **decoder-only** — they predict the next token given all previous tokens. **Encoder-only** models (BERT-style) are used for embeddings/classification. **Encoder-decoder** (T5, original translation transformers) map an input sequence to an output sequence.

**(c) Variants worth knowing.** **Mixture-of-Experts (MoE)** models activate only a subset of "expert" sub-networks per token, giving large capacity at lower inference cost (several frontier models are believed to use MoE, though labs rarely disclose architectures). **State-space / hybrid models** (Mamba-3 and SSM-transformer hybrids like Jamba and Nemotron-H) have reached **production** for throughput- and long-context-sensitive workloads, trading some peak quality for cheaper long sequences — though transformers still dominate the frontier.

**(e) Pitfalls.** Architecture is rarely something an *enterprise consumer* tunes — you consume models via API. The relevant leverage is knowing that attention cost historically scales roughly with the **square of sequence length** (1.5, 1.6), which is why long contexts are expensive and why retrieval beats "stuff everything in."

**(f) Enterprise example.** You don't build transformers; you *choose* between them (a small fast model for classification vs. a large model for complex reasoning) and *route* between them (Module 8.7). Understanding the architecture is what lets you reason about that cost/quality frontier.

---

## 1.5 Attention

**(a) What it is / why it matters.**
**Attention** is the mechanism by which, when processing a given token, the model decides *which other tokens matter* and how much. It's how the model handles context, resolves references ("it" → which noun?), and connects distant but related information. Attention is the single most important idea in the transformer.

**Analogy.** Reading the sentence "The quote expired because *it* was never countersigned," your brain instantly binds "it" to "quote," not "because." Attention is the model doing that binding — for every token, against every other token, at every layer, simultaneously.

**(b) Mechanics.**
For each token, the model computes three vectors: a **Query** (what am I looking for?), a **Key** (what do I offer?), and a **Value** (what do I contribute if attended to?). The attention score between two tokens is the dot product of one's Query with another's Key; scores are normalized (softmax) into weights; each token's new representation is the weighted sum of all Values. **Multi-head** attention runs several of these in parallel, each learning different relationship types (syntax, coreference, topic), then combines them.

**Self-attention** relates tokens within one sequence. **Causal (masked) attention** in decoder models prevents a token from "seeing" future tokens (essential for next-token prediction).

**(b′) The cost problem.** Naïve attention compares every token to every other token → cost grows with the **square** of sequence length (O(n²)). This is the root of why long context is expensive. Engineering responses include **FlashAttention** (memory-efficient exact attention), **KV-caching** (reuse computed Keys/Values across generation steps — critical for inference speed and the basis of prompt caching, Module 6.5), sparse/sliding-window attention, and grouped-query attention.

**(e) Pitfall — "lost in the middle."** Empirically, models attend most reliably to the **beginning and end** of a long context and can neglect material buried in the middle. Honest framing: the **effect is robustly replicated** (across many models and long-context benchmarks); the precise **mechanism is still debated** (positional-encoding biases, primacy/recency patterns in training data) — so treat it as an empirical constraint to *engineer around*, not a settled law. Practical consequence (revisited in 1.6 and 3): placing critical instructions/data at the edges, and retrieving *less but more relevant* context, beats dumping everything in.

**(f) Enterprise example.** When an agent reads a 30-page contract to answer "what's the termination notice period?", attention is what lets it connect the question to the one relevant clause. But if that clause sits in the middle of a giant stuffed context alongside 20 irrelevant documents, "lost in the middle" can cause it to miss — an argument for precise retrieval and reranking (Module 3.6).

---

## 1.6 Context windows

**(a) What it is / why it matters.**
The **context window** is the maximum number of tokens the model can consider at once — the prompt **plus** the generated output must fit. It is the model's working memory. It has grown from ~2k tokens (2020) to **1M tokens now being standard** across frontier hosted models (recent Claude, Gemini, and others), with some open-weight models (e.g., Llama 4 Scout) advertising **up to 10M** — though, as below, effective recall degrades well before the advertised limit. Context size dictates how much instruction, retrieved data, conversation history, and tool output you can supply — and it caps how big a document you can process in one shot.

**Analogy.** The context window is the model's desk. Anything on the desk it can use right now; anything filed away it cannot see unless you fetch it and put it on the desk. RAG (Module 3) is the process of fetching the right files onto a finite desk.

**(b) Mechanics & caveats.**
- The window covers **everything**: system prompt + tools definitions + history + retrieved docs + the model's own output.
- **Bigger isn't free.** Cost and latency scale with tokens processed; long contexts are slower and pricier.
- **Effective context < advertised context.** A model may *accept* 1M tokens but *use* them unevenly — the "lost in the middle" effect (1.5) and degradation on "needle-in-a-haystack-with-distractors" tasks mean that stuffing the window is not the same as reasoning well over it. **Long-context ≠ a substitute for good retrieval** — now **repeatedly confirmed** on 1M-token models by long-context benchmarks (RULER, LongBench v2, HELMET): larger windows shift the degradation further out but do not remove it.

**(d) Decision criteria — long context vs. RAG.**
- Use **long context** when the *whole* relevant corpus is small enough to fit, changes constantly, and precision of retrieval is hard (e.g., "summarize this one 200-page deposition").
- Use **RAG** when the corpus is large, must be permissioned/filtered, changes per-user, or when cost/latency of stuffing is prohibitive (almost all enterprise knowledge bases). Often you combine them: retrieve a focused set, then use a long window to reason over it.

**(e) Pitfalls.** Blowing the budget with verbose tool outputs or long histories; assuming "1M context" means "reads a million tokens well"; forgetting output tokens count against the window.

**(f) Enterprise example.** A deal-desk agent could theoretically load a customer's entire Salesforce history into a long context, but it's cheaper, safer (entitlement filtering), and more accurate to retrieve the last three opportunities and the active quote (Module 09).

---

## 1.7 Training stages: pretraining → fine-tuning → instruction-tuning → alignment

**(a) What it is / why it matters.**
A production model is built in **stages**, and knowing which stage does what tells you *which lever to pull* when the model isn't behaving: do you need better prompts, retrieval, or actual fine-tuning? (Module 2.5 covers the how of fine-tuning; this is the conceptual map.)

**(b) The stages.**
1. **Pretraining.** The model learns language and world patterns by predicting the next token over a massive, diverse corpus (web, books, code). This is where the bulk of "knowledge" and capability comes from. It's enormously expensive and done by frontier labs, not enterprises. Output: a **base model** — fluent but not helpful; it just continues text.
2. **Supervised fine-tuning (SFT) / instruction-tuning.** The base model is trained on curated (instruction → good response) pairs so it learns to *follow instructions* and answer rather than merely continue. This turns a text-continuation engine into an assistant.
3. **Alignment / preference optimization.** Techniques tune the model toward responses humans prefer — helpful, harmless, honest, correctly formatted, appropriately cautious. Briefly, *how each works*: **RLHF** (Reinforcement Learning from Human Feedback) — humans rank competing model outputs, a **reward model** is trained to mimic those rankings, and the LLM is then optimized to score well against that reward model. **DPO** (Direct Preference Optimization) — skips the separate reward model and optimizes the LLM *directly* on the preference pairs (cheaper and simpler, now common). **Constitutional AI** (Anthropic, Bai et al. 2022) — the model **critiques and revises its own answers against a written set of principles** ("a constitution"), generating much of its own alignment signal and reducing the need for human labels.
4. **(Domain) fine-tuning by enterprises.** On top of an already-aligned model, an enterprise may fine-tune (often with **LoRA/PEFT**, Module 2.5) to specialize style, format, or narrow-domain behavior.

**(c) Key distinction — knowledge vs. behavior.**
- **Fine-tuning changes *behavior/style*, not reliably *knowledge*.** It's excellent for "always output this JSON shape," "adopt our tone," "classify into our 12 categories." It is a **poor and risky way to inject facts** — facts learned this way can't be updated without retraining, may be hallucinated confidently, and can't be permissioned per-user.
- **To give a model current, factual, permissioned knowledge, use RAG (Module 3), not fine-tuning.** This is one of the most important practical rules in the whole series.

**(d) Decision criteria (preview of 2.5).** Prompt first → add retrieval → fine-tune only when you need consistent behavior/format/latency that prompting can't achieve, and you have quality training data and an evaluation harness.

**(e) Pitfall.** "The model doesn't know our products, let's fine-tune it on our catalog." Usually wrong — the catalog changes, and fine-tuning bakes in a stale snapshot. Retrieve the catalog instead.

**(f) Enterprise example.** A bank fine-tunes a model to *always* refuse to give individualized investment advice and to emit disclosures in a fixed format (behavior) — but retrieves the client's actual portfolio at query time (knowledge).

---

## 1.8 Inference parameters: temperature, sampling, logprobs

**(a) What it is / why it matters.**
At generation time you control *how* the model turns its next-token probability distribution into actual text. These knobs trade **determinism/reliability** against **creativity/diversity**. For enterprise systems — especially agents and structured outputs — you usually want the *reliable* end.

**(b) The main knobs.**
- **Temperature** — scales the probability distribution before sampling. **Low (0–0.3):** the model almost always picks the highest-probability token → focused, repeatable, "boring but correct." **High (0.8–1.2):** flatter distribution → more diverse and creative, but more error-prone and less consistent. For extraction, classification, tool-calling, and most agent work, use **low** temperature. For brainstorming/marketing copy, higher.
- **Top-p (nucleus sampling)** — sample only from the smallest set of tokens whose cumulative probability ≥ p (e.g., 0.9). Caps the "long tail" of unlikely tokens.
- **Top-k** — sample only from the k most likely tokens.
- **Max tokens / stop sequences** — cap output length; define where to stop.
- **Frequency/presence penalties** — discourage repetition.
- **Seed** (where supported) — improves reproducibility but does **not** guarantee bit-identical output across infrastructure.

- **Logprobs** — the model can return the **log-probability** of chosen (and alternative) tokens. This is quietly one of the most useful enterprise features: it gives you a **confidence signal**. Uses: flag low-confidence answers for human review, build classifiers/routers, detect when the model is "unsure," and power certain evaluation methods.

**How the knobs combine (so you know what to actually set).** They're applied in sequence: **temperature** first reshapes the distribution (flatter = more random), then **top-p/top-k** truncate its tail. You rarely tune all three at once. Practical default for reliable enterprise tasks: **temperature ≈ 0** and leave top-p/top-k at their defaults; reach for higher temperature (and maybe top-p ≈ 0.9) only for genuinely creative generation.

**(d) Decision criteria.** Default to **low temperature** for anything that must be correct or parseable. Raise it only for genuinely generative tasks. For structured outputs and tool calls, combine low temperature with schema enforcement (Module 2.2).

**(e) Pitfalls.**
- **Determinism is not guaranteed even at temperature 0** — floating-point nondeterminism, batching, and MoE routing can produce small variations. Don't build systems that assume bit-exact reproducibility.
- **High temperature in agents** amplifies compounding errors over a multi-step loop.
- **Confusing "confident" tone with "correct."** Logprobs measure the model's confidence *in its own token choice*, not factual accuracy — a fluent hallucination can have high logprobs.

**(f) Enterprise example.** A quote-generation agent runs at temperature 0 for extracting line items and computing configurations (must be exact), and uses logprobs to route any extraction below a confidence threshold to a human for review before the quote is written back to the SoR (Module 09).

---

## 1.9 Why hallucinations occur

**(a) What it is / why it matters.**
A **hallucination** is a fluent, confident output that is **factually wrong or fabricated** — an invented citation, a made-up API parameter, a plausible but false contract term. It's the defining risk of enterprise LLM deployment. Understanding *why* it happens tells you how to *reduce* it (you rarely eliminate it).

**(b) Why it happens — root causes.**
1. **The objective is plausibility, not truth.** The model is trained to produce *likely* text (1.1). A confident, well-formed falsehood is often more "likely" than "I don't know." Nothing in the base objective rewards truth per se.
2. **Knowledge is lossy and interpolated.** Facts are compressed into weights (1.1); rare or fine-grained facts (a specific customer's data, a niche API signature) are poorly stored and get *interpolated* — the model fills gaps with plausible patterns.
3. **No inherent notion of "I don't know."** Alignment can teach hedging, but the base model has no calibrated uncertainty about facts; it will complete the pattern.
4. **Stale/absent knowledge.** Anything after the training cutoff, or private to your enterprise, simply isn't in the weights.
5. **Prompt/context pressure.** Leading questions, contradictory context, or "lost in the middle" retrieval (1.5) push the model to confabulate.
6. **Reasoning errors.** Multi-step problems accumulate mistakes; the model may state a wrong intermediate result confidently.
7. **Evaluation incentives reward guessing.** A widely-cited 2025 analysis (OpenAI's "Why Language Models Hallucinate," later in *Nature*, 2026) argues models bluff partly because most benchmarks score "I don't know" the same as a wrong answer (zero) and reward a lucky confident guess — so training and model selection favor confident guessing over calibrated abstention. The implied fix is to **reward calibrated uncertainty in evaluations**, not just add hallucination tests.

**(c) Mitigations (each expanded in later modules).**
- **RAG (Module 3):** ground answers in retrieved source text and require citations. The single biggest lever for factual tasks.
- **Tool calling (Module 2.3):** let the model *compute* (calculator, SQL, SoR query) instead of recalling.
- **Structured outputs + validation (Module 2.2):** constrain the shape and check it.
- **Lower temperature (1.8)** and **confidence gating via logprobs.**
- **Prompt techniques:** "answer only from the provided context; if it's not there, say you don't know" (Module 2.1).
- **Verification layers / LLM-as-judge (Modules 2.6, 8.8)** and **human-in-the-loop** for high-stakes outputs (Modules 5.7, 09).
- **Reasoning models (Module 8.1)** reduce *reasoning/arithmetic* errors but do **not** eliminate factual fabrication — and on summarization/faithfulness tasks, extended "thinking" can *increase* hallucination (the long internal chain drifts from the source). Match mode to task: reasoning for math/logic/code, base models for grounded summarization.

**(d) Decision criteria.** Match the mitigation stack to the stakes. A brainstorming assistant tolerates hallucination; an agent that writes a price into a customer quote (Module 09) needs retrieval grounding, tool-based computation, schema validation, and human approval.

**(e) Failure modes to name for the video series.**
- **Fabricated citations/URLs/case law** (a notorious legal example).
- **Confident wrong arithmetic.**
- **Sycophancy** — agreeing with an incorrect premise the user stated.
- **Context override** — ignoring provided source text in favor of parametric "memory."
- **Ungrounded extrapolation** — inventing product features or SLA terms that "sound right."

**(f) Enterprise example.** Ask a bare model "What's ACME Corp's contract renewal date?" and it may confidently invent one. The fix is architectural, not a better prompt: the agent must **retrieve** the record from the CRM SoR and answer *only* from it, citing the record — and say "I don't have that" when retrieval returns nothing. This is the bridge into Modules 2 and 3.

---

### Module 1 takeaways
- An LLM is a **next-token predictor**: fluent reasoning, unreliable knowledge.
- **Tokens** drive cost and limits; **embeddings** encode meaning as geometry and power semantic search.
- The **transformer + attention** make it all scale; attention's O(n²) cost is why long context is expensive and retrieval beats stuffing.
- **Context window** is finite working memory; bigger ≠ better-used.
- **Training stages** separate *behavior* (fine-tunable) from *knowledge* (retrieve, don't fine-tune).
- **Inference knobs** trade determinism for creativity; default low-temperature for enterprise; **logprobs** give a confidence signal.
- **Hallucination** is intrinsic to the objective; you *manage* it with grounding, tools, structure, and human oversight — the subject of the rest of this series.

*Proceed to `02-capability-extension.md`.*
