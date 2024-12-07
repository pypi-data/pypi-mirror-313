import os.path
import ast

import aiofiles
import asyncio
import httpx
import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, IO, Iterable, List, Optional, Tuple, Union
from collections import defaultdict
from h2o_authn import AsyncTokenProvider
from urllib.parse import quote

from h2ogpte.errors import (
    ErrorResponse,
    HTTPError,
    InternalServerError,
    InvalidArgumentError,
    ObjectNotFoundError,
    UnauthorizedError,
)
from h2ogpte.h2ogpte import unmarshal_dict
from h2ogpte.session_async import SessionAsync
from h2ogpte.types import (
    Answer,
    ChatMessage,
    ChatMessageFull,
    ChatMessageMeta,
    ChatMessageReference,
    ChatSessionCount,
    ChatSessionForCollection,
    ChatSessionInfo,
    Chunk,
    Chunks,
    Collection,
    CollectionCount,
    CollectionInfo,
    Document,
    DocumentCount,
    DocumentInfo,
    DocumentInfoSummary,
    SuggestedQuestion,
    ExtractionAnswer,
    Identifier,
    Job,
    JobKind,
    Meta,
    ObjectCount,
    SharePermission,
    QuestionReplyData,
    QuestionReplyDataCount,
    Result,
    SchedulerStats,
    SearchResult,
    SearchResults,
    SessionError,
    ShareResponseStatus,
    Tag,
    User,
    LLMUsage,
    LLMUsageLimit,
    PromptTemplate,
    PromptTemplateCount,
    ProcessedDocument,
    DocumentSummary,
    LLMPerformance,
    UserWithLLMUsage,
    LLMWithUserUsage,
    ChatSessionForDocument,
    UserPermission,
    UserRole,
)
from h2ogpte.utils import _process_pdf_with_annotations, import_pymupdf
from h2ogpte.connectors import (
    S3Credential,
    GCSServiceAccountCredential,
    AzureKeyCredential,
    AzureSASCredential,
    create_ingest_job_from_s3,
    create_ingest_job_from_gcs,
    create_ingest_job_from_azure_blob_storage,
)


class H2OGPTEAsync:
    """
    Connect to and interact with an h2oGPTe server, via an async interface.
    """

    # Timeout for HTTP requests
    TIMEOUT = 3600.0

    INITIAL_WAIT_INTERVAL = 0.1
    MAX_WAIT_INTERVAL = 1.0
    WAIT_BACKOFF_FACTOR = 1.4

    def __init__(
        self,
        address: str,
        api_key: Optional[str] = None,
        token_provider: Optional[AsyncTokenProvider] = None,
        verify: Union[bool, str] = True,
        strict_version_check: bool = False,
    ) -> None:
        """
        Creates a new async H2OGPTE client.
        Args:
            address:
                Full URL of the h2oGPTe server to connect to, e.g.
                "https://h2ogpte.h2o.ai".
            api_key:
                API key for authentication to the h2oGPTe server. Users can generate
                a key by accessing the UI and navigating to the Settings.
            token_provider:
                User's token provider.
            verify:
                Whether to verify the server's TLS/SSL certificate.
                Can be a boolean or a path to a CA bundle. Defaults to True.
            strict_version_check:
                Indicate whether a version check should be enforced.
        """
        self._address = address.rstrip("/ ")
        self._api_key = api_key
        self._verify = verify
        self._token_provider = token_provider
        self._session_id = str(uuid.uuid4())

        if self._api_key is None and self._token_provider is None:
            raise RuntimeError(
                f"Please use either an API key or a Token provider to authenticate."
            )

        if self._api_key is not None and self._token_provider is not None:
            print(
                "Warning: The token_provider parameter will be ignored in favor of the provided api_key"
            )

        self._client = httpx.AsyncClient(
            verify=verify,
        )

        # asyncio.run(self._check_version(strict_version_check))

    async def _get_auth_header(self) -> Dict:
        if self._api_key is not None:
            return {
                "Authorization": f"Bearer {self._api_key}",
            }
        elif self._token_provider is not None:
            token = await self._token_provider.token()
            return {
                "Authorization": f"Token-Bearer {token}",
                "Session-Id": self._session_id,
            }
        else:
            raise Exception(
                "Please provide either an api_key or a token_provider to authenticate."
            )

    async def answer_question(
        self,
        question: str,
        system_prompt: Union[
            str, None
        ] = "",  # "" to disable, 'auto' to use LLMs default, None for h2oGPTe default
        pre_prompt_query: Union[
            str, None
        ] = None,  # "" to disable, None for h2oGPTe default
        prompt_query: Union[
            str, None
        ] = None,  # "" to disable, None for h2oGPTe default
        text_context_list: Optional[List[str]] = None,
        llm: Union[str, int, None] = None,
        llm_args: Optional[Dict[str, Any]] = None,
        chat_conversation: Optional[List[Tuple[str, str]]] = None,
        guardrails_settings: Optional[Dict] = None,
        timeout: Union[float, None] = None,
        **kwargs: Any,
    ) -> Answer:
        """Send a message and get a response from an LLM.

        Note: This method is only recommended if you are passing a chat conversation or for low-volume testing.
        For general chat with an LLM, we recommend session.query() for higher throughput in multi-user environments,
        like this:

        chat_session_id = client.create_chat_session()
        with client.connect(chat_session_id) as session:
            reply = session.query("Hi")

        Format of input content::

            {text_context_list}
            \"\"\"\\n{chat_conversation}{question}

        Args:
            question:
                Text query to send to the LLM.
            text_context_list:
                List of raw text strings to be included, will be converted to a string like this: "\n\n".join(text_context_list)
            system_prompt:
                Text sent to models which support system prompts. Gives the model
                overall context in how to respond. Use `auto` for the model default,
                or None for h2oGPTe default. Defaults to '' for no system prompt.
            pre_prompt_query:
                Text that is prepended before the contextual document chunks in text_context_list. Only used if text_context_list is provided.
            prompt_query:
                Text that is appended after the contextual document chunks in text_context_list. Only used if text_context_list is provided.
            llm:
                Name or index of LLM to send the query. Use `H2OGPTE.get_llms()` to
                see all available options.
                Default value is to use the first model (0th index).
            llm_args:
                Dictionary of kwargs to pass to the llm. Valid keys:
                    temperature (float, default: 0) — The value used to modulate the next token probabilities. Most deterministic: 0, Most creative: 1
                    top_k (int, default: 1) — The number of highest probability vocabulary tokens to keep for top-k-filtering.
                    top_p (float, default: 1.0) — If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation.
                    seed (int, default: 0) — The seed for the random number generator when sampling during generation (if temp>0 or top_k>1 or top_p<1), seed=0 picks a random seed.
                    repetition_penalty (float, default: 1.07) — The parameter for repetition penalty. 1.0 means no penalty.
                    max_new_tokens (int, default: 1024) — Maximum number of new tokens to generate. This limit applies to each (map+reduce) step during summarization and each (map) step during extraction.
                    min_max_new_tokens (int, default: 512) — minimum value for max_new_tokens when auto-adjusting for content of prompt, docs, etc.
                    response_format (str, default: "text") — Output type, one of ["text", "json_object", "json_code"].
                    guided_json (dict, default: None) — If specified, the output will follow the JSON schema.
                    guided_regex (str, default: "") — If specified, the output will follow the regex pattern. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_choice (Optional[List[str]], default: None — If specified, the output will be exactly one of the choices. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_grammar (str, default: "") — If specified, the output will follow the context free grammar. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_whitespace_pattern (str, default: "") — If specified, will override the default whitespace pattern for guided json decoding. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
            chat_conversation:
                List of tuples for (human, bot) conversation that will be pre-appended
                to an (question, None) case for a query.
           guardrails_settings:
                Guardrails Settings.
            timeout:
                Timeout in seconds.
            kwargs:
                Dictionary of kwargs to pass to h2oGPT. Not recommended, see https://github.com/h2oai/h2ogpt for source code. Valid keys:
                    h2ogpt_key: str = ""
                    chat_conversation: list[tuple[str, str]] | None = None
                    docs_ordering_type: str | None = "best_near_prompt"
                    max_input_tokens: int = -1
                    docs_token_handling: str = "split_or_merge"
                    docs_joiner: str = "\n\n"
                    image_file: Union[str, list] = None
        Returns:
            Answer: The response text and any errors.
        Raises:
            TimeoutError: If response isn't completed in timeout seconds.
        """
        ret = await self._lang(
            "answer_question_using_context",
            prompt=question,
            system_prompt=system_prompt,
            pre_prompt_query=pre_prompt_query,
            prompt_query=prompt_query,
            text_context_list=text_context_list,
            llm=llm,
            llm_args=llm_args,
            chat_conversation=chat_conversation,
            guardrails_settings=guardrails_settings,
            timeout=timeout,
            **kwargs,
        )
        if ret["error"]:
            raise SessionError(ret["error"])
        return Answer(**ret)

    async def summarize_content(
        self,
        text_context_list: Optional[List[str]] = None,
        system_prompt: str = "",  # '' to disable, 'auto' to use LLMs default
        pre_prompt_summary: Optional[str] = None,
        prompt_summary: Optional[str] = None,
        llm: Union[str, int, None] = None,
        llm_args: Optional[Dict[str, Any]] = None,
        guardrails_settings: Optional[Dict] = None,
        timeout: Union[float, None] = None,
        **kwargs: Any,
    ) -> Answer:
        """Summarize one or more contexts using an LLM.

        Format of summary content::

            "{pre_prompt_summary}\"\"\"
            {text_context_list}
            \"\"\"\\n{prompt_summary}"

        Args:
            text_context_list:
                List of raw text strings to be summarized.
            system_prompt:
                Text sent to models which support system prompts. Gives the model
                overall context in how to respond. Use `auto` for the model default or
                None for h2oGPTe defaults. Defaults to '' for no system prompt.
            pre_prompt_summary:
                Text that is prepended before the list of texts. The default can be
                customized per environment, but the standard default is :code:`"In
                order to write a concise single-paragraph or bulleted list summary,
                pay attention to the following text:\\\\n"`
            prompt_summary:
                Text that is appended after the list of texts. The default can be
                customized per environment, but the standard default is :code:`"Using
                only the text above, write a condensed and concise summary of key
                results (preferably as bullet points):\\\\n"`
            llm:
                Name or index of LLM to send the query. Use `H2OGPTE.get_llms()` to
                see all available options. Default value is to use the first model
                (0th index).
            llm_args:
                Dictionary of kwargs to pass to the llm. Valid keys:
                    temperature (float, default: 0) — The value used to modulate the next token probabilities. Most deterministic: 0, Most creative: 1
                    seed (int, default: 0) — The seed for the random number generator, only used if temperature > 0, seed=0 will pick a random number for each call, seed > 0 will be fixed.
                    top_k (int, default: 1) — The number of highest probability vocabulary tokens to keep for top-k-filtering.
                    top_p (float, default: 1.0) — If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation.
                    repetition_penalty (float, default: 1.07) — The parameter for repetition penalty. 1.0 means no penalty.
                    max_new_tokens (int, default: 1024) — Maximum number of new tokens to generate. This limit applies to each (map+reduce) step during summarization and each (map) step during extraction.
                    min_max_new_tokens (int, default: 512) — minimum value for max_new_tokens when auto-adjusting for content of prompt, docs, etc.
                    response_format (str, default: "text") — Output type, one of ["text", "json_object", "json_code"].
                    guided_json (dict, default: None) — If specified, the output will follow the JSON schema.
                    guided_regex (str, default: "") — If specified, the output will follow the regex pattern. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_choice (Optional[List[str]], default: None — If specified, the output will be exactly one of the choices. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_grammar (str, default: "") — If specified, the output will follow the context free grammar. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_whitespace_pattern (str, default: "") — If specified, will override the default whitespace pattern for guided json decoding. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
            guardrails_settings:
                Guardrails Settings.
            timeout:
                Timeout in seconds.
            kwargs:
                Dictionary of kwargs to pass to h2oGPT. Not recommended, see https://github.com/h2oai/h2ogpt for source code. Valid keys:
                    h2ogpt_key: str = ""
                    chat_conversation: list[tuple[str, str]] | None = None
                    docs_ordering_type: str | None = "best_near_prompt"
                    max_input_tokens: int = -1
                    docs_token_handling: str = "split_or_merge"
                    docs_joiner: str = "\n\n"
                    image_file: Union[str, list] = None
        Returns:
            Answer: The response text and any errors.
        Raises:
            TimeoutError: If response isn't completed in timeout seconds.
        """
        ret = await self._lang(
            "create_summary_from_context",
            text_context_list=text_context_list,
            system_prompt=system_prompt,
            pre_prompt_summary=pre_prompt_summary,
            prompt_summary=prompt_summary,
            llm=llm,
            llm_args=llm_args,
            guardrails_settings=guardrails_settings,
            timeout=timeout,
            **kwargs,
        )
        if ret["error"]:
            raise SessionError(ret["error"])
        return Answer(**ret)

    async def extract_data(
        self,
        text_context_list: Optional[List[str]] = None,
        system_prompt: str = "",
        pre_prompt_extract: Optional[str] = None,
        prompt_extract: Optional[str] = None,
        llm: Union[str, int, None] = None,
        llm_args: Optional[Dict[str, Any]] = None,
        guardrails_settings: Optional[Dict] = None,
        timeout: Union[float, None] = None,
        **kwargs: Any,
    ) -> ExtractionAnswer:
        """
        Extract information from one or more contexts using an LLM.
        pre_prompt_extract and prompt_extract variables must be used together. If these
        variables are not set, the inputs texts will be summarized into bullet points.
        Format of extract content::

            "{pre_prompt_extract}\"\"\"
            {text_context_list}
            \"\"\"\\n{prompt_extract}"

        Examples::

            extract = h2ogpte.extract_data(
                text_context_list=chunks,
                pre_prompt_extract="Pay attention and look at all people. Your job
                                    is to collect their names.\\n",
                prompt_extract="List all people's names as JSON.",
            )

        Args:
            text_context_list:
                List of raw text strings to extract data from.
            system_prompt:
                Text sent to models which support system prompts. Gives the model
                overall context in how to respond. Use `auto` or None for the model
                default. Defaults to '' for no system prompt.
            pre_prompt_extract:
                Text that is prepended before the list of texts. If not set,
                the inputs will be summarized.
            prompt_extract:
                Text that is appended after the list of texts. If not set, the inputs
                will be summarized.
            llm:
                Name or index of LLM to send the query. Use `H2OGPTE.get_llms()` to
                see all available options.
                Default value is to use the first model (0th index).
            llm_args:
                Dictionary of kwargs to pass to the llm. Valid keys:
                    temperature (float, default: 0) — The value used to modulate the next token probabilities. Most deterministic: 0, Most creative: 1
                    seed (int, default: 0) — The seed for the random number generator, only used if temperature > 0, seed=0 will pick a random number for each call, seed > 0 will be fixed.
                    top_k (int, default: 1) — The number of highest probability vocabulary tokens to keep for top-k-filtering.
                    top_p (float, default: 1.0) — If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation.
                    repetition_penalty (float, default: 1.07) — The parameter for repetition penalty. 1.0 means no penalty.
                    max_new_tokens (int, default: 1024) — Maximum number of new tokens to generate. This limit applies to each (map+reduce) step during summarization and each (map) step during extraction.
                    min_max_new_tokens (int, default: 512) — minimum value for max_new_tokens when auto-adjusting for content of prompt, docs, etc.
                    response_format (str, default: "text") — Output type, one of ["text", "json_object", "json_code"].
                    guided_json (dict, default: None) — If specified, the output will follow the JSON schema.
                    guided_regex (str, default: "") — If specified, the output will follow the regex pattern. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_choice (Optional[List[str]], default: None — If specified, the output will be exactly one of the choices. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_grammar (str, default: "") — If specified, the output will follow the context free grammar. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_whitespace_pattern (str, default: "") — If specified, will override the default whitespace pattern for guided json decoding. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
            guardrails_settings:
                Guardrails Settings.
            timeout:
                Timeout in seconds.
            kwargs:
                Dictionary of kwargs to pass to h2oGPT. Not recommended, see https://github.com/h2oai/h2ogpt for source code. Valid keys:
                    h2ogpt_key: str = ""
                    chat_conversation: list[tuple[str, str]] | None = None
                    docs_ordering_type: str | None = "best_near_prompt"
                    max_input_tokens: int = -1
                    docs_token_handling: str = "split_or_merge"
                    docs_joiner: str = "\n\n"
                    image_file: Union[str, list] = None
        Returns:
            ExtractionAnswer: The list of text responses and any errors.
        Raises:
            TimeoutError: If response isn't completed in timeout seconds.
        """
        ret = await self._lang(
            "extract_data_from_context",
            text_context_list=text_context_list,
            system_prompt=system_prompt,
            pre_prompt_extract=pre_prompt_extract,
            prompt_extract=prompt_extract,
            llm=llm,
            llm_args=llm_args,
            guardrails_settings=guardrails_settings,
            timeout=timeout,
            **kwargs,
        )
        if ret["error"]:
            raise SessionError(ret["error"])
        return ExtractionAnswer(**ret)

    async def cancel_job(self, job_id: str) -> Result:
        """
        Stops a specific job from running on the server.

        Args:
            job_id:
                String id of the job to cancel.
        Returns:
            Result: Status of canceling the job.
        """
        ret = await self._job(".Cancel", job_id=job_id)
        return Result(**ret)

    async def count_chat_sessions(self) -> int:
        """
        Returns the count of chat sessions owned by the user.
        """
        ret = await self._db("count_chat_sessions")
        return ChatSessionCount(**ret).chat_session_count

    async def count_chat_sessions_for_collection(self, collection_id: str) -> int:
        """
        Counts number of chat sessions in a specific collection.

        Args:
            collection_id:
                String id of the collection to count chat sessions for.
        Returns:
            int: The count of chat sessions in that collection.
        """
        ret = await self._db("count_chat_sessions_for_collection", collection_id)
        return ChatSessionCount(**ret).chat_session_count

    async def count_collections(self) -> int:
        """
        Counts number of collections owned by the user.

        Returns:
            int: The count of collections owned by the user.
        """
        ret = await self._db("count_collections")
        return CollectionCount(**ret).collection_count

    async def count_documents(self) -> int:
        """
        Returns the count of documents accessed by the user.
        """
        ret = await self._db("count_documents")
        return DocumentCount(**ret).document_count

    async def count_documents_owned_by_me(self) -> int:
        """
        Returns the counts of documents owned by the user.
        """
        ret = await self._db("count_documents_owned_by_me")
        return DocumentCount(**ret).document_count

    async def count_documents_in_collection(self, collection_id: str) -> int:
        """
        Counts the number of documents in a specific collection.

        Args:
            collection_id:
                String id of the collection to count documents for.
        Returns:
            int: The number of documents in that collection.
        """
        ret = await self._db("count_documents_in_collection", collection_id)
        return DocumentCount(**ret).document_count

    async def count_assets(self) -> ObjectCount:
        """
        Counts number of objects owned by the user.

        Returns:
            ObjectCount: The count of chat sessions, collections, and documents.
        """
        ret = await self._db("count_assets")
        return ObjectCount(**ret)

    async def create_chat_session(self, collection_id: Optional[str] = None) -> str:
        """
        Creates a new chat session for asking questions (of documents).

        Args:
            collection_id:
                String id of the collection to chat with.
                If None, chat with LLM directly.
        Returns:
            str: The ID of the newly created chat session.
        """
        ret = await self._db("create_chat_session", collection_id)
        return _to_id(ret)

    async def create_chat_session_on_default_collection(self) -> str:
        """
        Creates a new chat session for asking questions of documents on the default
        collection.

        Returns:
            str: The ID of the newly created chat session.
        """
        ret = await self._db("create_chat_session_on_default_collection")
        return _to_id(ret)

    async def list_embedding_models(self) -> List[str]:
        return list((await self._lang("get_embedding_models_dict")).keys())

    async def run_selftest(self, llm: str, mode: str) -> dict:
        """
        Run a self-test for a given LLM
        Args:
            llm:
                Name of LLM
            mode:
                one of ["quick", "rag", "full", "stress"]
        Returns:
            Dictionary with performance stats. If "error" is filled, the test failed.
        """
        return await self._lang("selftest_sync", llm=llm, mode=mode)

    async def get_guardrails_settings(
        self,
        action: str = "redact",
        sensitive: bool = True,
        non_sensitive: bool = True,
        all_guardrails: bool = True,
        guardrails_settings: Union[dict, None] = None,
    ) -> Dict[str, Union[str, List[str]]]:
        """
        Helper to get reasonable (easy to use) defaults for Guardrails/PII settings. To be further customized.
        :param action: what to do when detecting PII, either "redact" or "fail" ("allow" would keep PII intact). Guardrails models always fail upon detecting safety violations.
        :param sensitive: whether to include the most sensitive PII entities like SSN, bank account info
        :param non_sensitive: whether to include all non-sensitive PII, such as IP addresses, locations, names, e-mail addresses etc.
        :param all_guardrails: whether to include all possible entities for prompt guard and guardrails models, or just system defaults
        :param guardrails_settings: existing guardrails settings (e.g., from collection settings) to obtain guardrails entities and guardrails_entities_to_flag from instead of system defaults
        :return: dictionary to pass to collection creation or process_document method
        """
        return await self._lang(
            "get_guardrails_settings",
            action=action,
            sensitive=sensitive,
            non_sensitive=non_sensitive,
            all_guardrails=all_guardrails,
            guardrails_settings=guardrails_settings,
        )

    async def create_collection(
        self,
        name: str,
        description: str,
        embedding_model: Union[str, None] = None,
        prompt_template_id: Union[str, None] = None,
        collection_settings: Union[dict, None] = None,
    ) -> str:
        """
        Creates a new collection.

        Args:
            name:
                Name of the collection.
            description:
                Description of the collection
            embedding_model:
                embedding model to use. call list_embedding_models() to list of options.
            prompt_template_id:
                ID of the prompt template to get the prompts from. None to fall back to system defaults.
            collection_settings:
                (Optional) Dictionary with key/value pairs to configure certain collection specific settings
                max_tokens_per_chunk: Approximate max. number of tokens per chunk for text-dominated document pages. For images, chunks can be larger.
                chunk_overlap_tokens: Approximate number of tokens that are overlapping between successive chunks.
                guardrails_settings itself is a dictionary of the following keys.
                    disallowed_regex_patterns: list of regular expressions that match custom PII
                    presidio_labels_to_flag: list of entities to be flagged as PII by the built-in Presidio model.
                    pii_labels_to_flag: list of entities to be flagged as PII by the built-in PII model.
                    pii_detection_parse_action: what to do when PII is detected during parsing of documents. One of ["allow", "redact", "fail"]. Redact will replace disallowed content in the ingested documents with redaction bars.
                    pii_detection_llm_input_action: what to do when PII is detected in the input to the LLM (document content and user prompts). One of ["allow", "redact", "fail"]. Redact will replace disallowed content with placeholders.
                    pii_detection_llm_output_action: what to do when PII is detected in the output of the LLM. One of ["allow", "redact", "fail"]. Redact will replace disallowed content with placeholders.
                    prompt_guard_labels_to_flag: list of entities to be flagged as safety violations in user prompts by the built-in prompt guard model.
                    guardrails_labels_to_flag: list of entities to be flagged as safety violations in user prompts. Must be a subset of guardrails_entities, if provided.
                    guardrails_entities: (Optional) dictionary of entities and their descriptions for the guardrails model to classify. The first entry is the "safe" class, the rest are "unsafe" classes.
                Example:
                    Note: Call client.get_guardrails_settings() to see all options for guardrails_settings.

                    collection_settings=dict(
                        max_tokens_per_chunk=320,
                        chunk_overlap_tokens=0,
                        guardrails_settings=dict(
                            disallowed_regex_patterns=["secret_disallowed_word", r"(?!0{3})(?!6{3})[0-8]\d{2}-(?!0{2})\d{2}-(?!0{4})\d{4}"],
                            presidio_labels_to_flag=["IBAN_CODE", "US_SSN"],
                            pii_labels_to_flag=["IBAN", "SSN"],
                            pii_detection_parse_action="redact",
                            pii_detection_llm_input_action="redact",
                            pii_detection_llm_output_action="allow",
                            prompt_guard_labels_to_flag=["JAILBREAK"],
                            guardrails_labels_to_flag=[
                                "Violent Crimes",
                                "Non-Violent Crimes",
                                "Intellectual Property",
                                "Code Interpreter Abuse",
                            ],
                            guardrails_entities={
                                "Safe": "Messages that do not contain any of the following unsafe content",  # must be first, not used as potential label to flag
                                "Violent Crimes": "Messages that enable, encourage, or endorse the commission of violent crimes, including: (1) unlawful violence toward people (ex: terrorism, genocide, murder, hate-motivated violent crimes, child abuse, assault, battery, kidnapping) and (2) unlawful violence toward animals (ex: animal abuse)",
                                "Non-Violent Crimes": "Messages that enable, encourage, or endorse the commission of non-violent crimes, including: (1) personal crimes (ex: labor trafficking, threats, intimidation, hate-motivated non-violent crimes), (2) financial crimes (ex: fraud, scams, money laundering), (3) property crimes (ex: theft, arson, vandalism), (4) drug crimes (ex: creating or using regulated substances), (5) weapons crimes (ex: producing unlicensed firearms), and (6) cyber crimes (ex: hacking)",
                                "Defamation": "Messages that are both verifiably false and likely to injure a living person’s reputation",
                                "Specialized Advice": "Messages that contain specialized financial, medical, or legal advice, or that indicate dangerous activities or objects are safe",
                                "Intellectual Property": "Messages that may violate the intellectual property rights of any third party",
                                "Code Interpreter Abuse": "Messages that seek to abuse code interpreters, including those that enable denial of service attacks, container escapes or privilege escalation exploits",
                            }
                        ),
                    )
        Returns:
            str: The ID of the newly created collection.
        """
        if embedding_model is None:
            embedding_model = await self._lang("get_default_embedding_model")
        collection_id = _to_id(
            await self._db(
                "create_collection",
                name,
                description,
                embedding_model,
                json.dumps(collection_settings or {}),
            )
        )
        if prompt_template_id is not None:
            await self.set_collection_prompt_template(collection_id, prompt_template_id)
        return collection_id

    async def create_topic_model(
        self,
        collection_id: str,
        timeout: Union[float, None] = None,
    ) -> Job:
        ret = (
            await self._job("crawl.CreateTopicModelJob", collection_id=collection_id),
        )
        return await self._wait_for_completion(_to_id(ret), timeout=timeout)

    async def delete_chat_sessions(
        self,
        chat_session_ids: Iterable[str],
        timeout: Union[float, None] = None,
    ) -> Job:
        """Deletes chat sessions and related messages.

        Args:
            chat_session_ids:
                List of string ids of chat sessions to delete from the system.
            timeout:
                Timeout in seconds.

        Returns:
            Result: The delete job.
        """
        ret = await self._job(
            "crawl_quick.DeleteChatSessionsJob", chat_session_ids=chat_session_ids
        )
        return await self._wait_for_completion(_to_id(ret), timeout=timeout)

    async def delete_chat_messages(self, chat_message_ids: Iterable[str]) -> Result:
        """Deletes specific chat messages.

        Args:
            chat_message_ids:
                List of string ids of chat messages to delete from the system.

        Returns:
            Result: Status of the delete job.
        """
        ret = await self._db("delete_chat_messages", chat_message_ids)
        return Result(**ret)

    async def delete_document_summaries(self, summaries_ids: Iterable[str]) -> Result:
        """Deletes document summaries.

        Args:
            summaries_ids:
                List of string ids of a document summary to delete from the system.

        Returns:
            Result: Status of the delete job.
        """
        ret = await self._db("delete_document_summaries", summaries_ids)
        return Result(**ret)

    async def get_collection_questions(
        self, collection_id: str, limit: int
    ) -> List[SuggestedQuestion]:
        """List suggested questions

        Args:
            collection_id:
                A collection ID of which to return the suggested questions
            limit:
                How many questions to return.

        Returns:
            List: A list of questions.
        """
        return [
            SuggestedQuestion(**d)
            for d in await self._db("get_collection_questions", collection_id, limit)
        ]

    async def get_chat_session_questions(
        self, chat_session_id: str, limit: int
    ) -> List[SuggestedQuestion]:
        """List suggested questions

        Args:
            chat_session_id:
                A chat session ID of which to return the suggested questions
            limit:
                How many questions to return.

        Returns:
            List: A list of questions.
        """
        return [
            SuggestedQuestion(**d)
            for d in await self._db(
                "get_chat_session_questions", chat_session_id, limit
            )
        ]

    async def delete_collections(
        self,
        collection_ids: Iterable[str],
        timeout: Union[float, None] = None,
    ) -> Job:
        """
        Deletes collections from the environment.
        Documents in the collection will not be deleted.

        Args:
            collection_ids:
                List of string ids of collections to delete from the system.
            timeout:
                Timeout in seconds.
        """
        ret = await self._job(
            "crawl_quick.DeleteCollectionsJob", collection_ids=collection_ids
        )
        return await self._wait_for_completion(_to_id(ret), timeout=timeout)

    async def delete_documents(
        self,
        document_ids: Iterable[str],
        timeout: Union[float, None] = None,
    ) -> Job:
        """
        Deletes documents from the system.

        Args:
            document_ids:
                List of string ids to delete from the system and all collections.
            timeout:
                Timeout in seconds.
        """
        ret = await self._job(
            "crawl_quick.DeleteDocumentsJob", document_ids=document_ids
        )
        return await self._wait_for_completion(_to_id(ret), timeout=timeout)

    async def delete_documents_from_collection(
        self,
        collection_id: str,
        document_ids: Iterable[str],
        timeout: Union[float, None] = None,
    ) -> Job:
        """Removes documents from a collection.

        See Also: H2OGPTE.delete_documents for completely removing the document from
        the environment.

        Args:
            collection_id:
                String of the collection to remove documents from.
            document_ids:
                List of string ids to remove from the collection.
            timeout:
                Timeout in seconds.
        """
        ret = await self._job(
            "crawl_quick.DeleteDocumentsFromCollectionJob",
            collection_id=collection_id,
            document_ids=document_ids,
        )
        return await self._wait_for_completion(_to_id(ret), timeout=timeout)

    async def import_collection_into_collection(
        self,
        collection_id: str,
        src_collection_id: str,
        gen_doc_summaries: bool = False,
        gen_doc_questions: bool = False,
        ocr_model: str = "auto",
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
    ):
        """Import all documents from a collection into an existing collection

        Args:
            collection_id:
                Collection ID to add documents to.
            src_collection_id:
                Collection ID to import documents from.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds.
        """
        ret = await self._job(
            "crawl.ImportCollectionIntoCollectionJob",
            collection_id=collection_id,
            src_collection_id=src_collection_id,
            gen_doc_summaries=gen_doc_summaries,
            gen_doc_questions=gen_doc_questions,
            ocr_model=ocr_model,
            tesseract_lang=tesseract_lang,
            keep_tables_as_one_chunk=keep_tables_as_one_chunk,
            chunk_by_page=chunk_by_page,
            handwriting_check=handwriting_check,
        )
        return await self._wait_for_completion(_to_id(ret), timeout=timeout)

    async def import_document_into_collection(
        self,
        collection_id: str,
        document_id: str,
        gen_doc_summaries: bool = False,
        gen_doc_questions: bool = False,
        copy_document: bool = False,
        ocr_model: str = "auto",
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
    ):
        """Import an already stored document to an existing collection

        Args:
            collection_id:
                Collection ID to add documents to.
            document_id:
                Document ID to add.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            copy_document:
                Whether to save a new copy of the document
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds.
        """
        ret = await self._job(
            "crawl.ImportDocumentIntoCollectionJob",
            collection_id=collection_id,
            document_id=document_id,
            gen_doc_summaries=gen_doc_summaries,
            gen_doc_questions=gen_doc_questions,
            copy_document=copy_document,
            ocr_model=ocr_model,
            tesseract_lang=tesseract_lang,
            keep_tables_as_one_chunk=keep_tables_as_one_chunk,
            chunk_by_page=chunk_by_page,
            handwriting_check=handwriting_check,
        )
        return await self._wait_for_completion(_to_id(ret), timeout=timeout)

    async def summarize_document(self, *args, **kwargs) -> DocumentSummary:
        assert not kwargs.get("keep_intermediate_results", False), (
            "Must not set keep_intermediate_results for summarize_document to preserve backward compatibility. "
            "Use process_document instead."
        )
        ret = await self.process_document(*args, **kwargs)
        return DocumentSummary(**ret.model_dump())

    async def process_document(
        self,
        document_id: str,
        system_prompt: Union[str, None] = None,
        pre_prompt_summary: Union[str, None] = None,
        prompt_summary: Union[str, None] = None,
        image_batch_image_prompt: Optional[str] = None,
        image_batch_final_prompt: Optional[str] = None,
        llm: Union[str, int, None] = None,
        llm_args: Optional[Dict[str, Any]] = None,
        max_num_chunks: Union[int, None] = None,
        sampling_strategy: Union[str, None] = None,
        pages: Union[List[int], None] = None,
        schema: Union[Dict[str, Any], None] = None,
        keep_intermediate_results: Union[bool, None] = None,
        guardrails_settings: Optional[Dict] = None,
        meta_data_to_include: Optional[Dict[str, bool]] = None,
        timeout: Optional[float] = None,
    ) -> ProcessedDocument:
        """Processes a document to either create a global or piecewise summary/extraction/transformation of a document.

        Args:
            document_id:
                String id of the document to create a summary from.
            system_prompt:
                System Prompt
            pre_prompt_summary:
                Prompt that goes before each large piece of text to summarize
            prompt_summary:
                Prompt that goes after each large piece of text to summarize
            image_batch_final_prompt:
                Prompt for each image batch for vision models
            image_batch_image_prompt:
                Prompt to reduce all answers each image batch for vision models
            llm:
                LLM to use
            llm_args:
                Dictionary of kwargs to pass to the llm. Valid keys:
                    temperature (float, default: 0) — The value used to modulate the next token probabilities. Most deterministic: 0, Most creative: 1
                    seed (int, default: 0) — The seed for the random number generator, only used if temperature > 0, seed=0 will pick a random number for each call, seed > 0 will be fixed.
                    top_k (int, default: 1) — The number of highest probability vocabulary tokens to keep for top-k-filtering.
                    top_p (float, default: 1.0) — If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation.
                    repetition_penalty (float, default: 1.07) — The parameter for repetition penalty. 1.0 means no penalty.
                    max_new_tokens (int, default: 1024) — Maximum number of new tokens to generate. This limit applies to each (map+reduce) step during summarization and each (map) step during extraction.
                    min_max_new_tokens (int, default: 512) — minimum value for max_new_tokens when auto-adjusting for content of prompt, docs, etc.
                    response_format (str, default: "text") — Output type, one of ["text", "json_object", "json_code"].
                    guided_json (dict, default: None) — If specified, the output will follow the JSON schema.
                    guided_regex (str, default: "") — If specified, the output will follow the regex pattern. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_choice (Optional[List[str]], default: None — If specified, the output will be exactly one of the choices. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_grammar (str, default: "") — If specified, the output will follow the context free grammar. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_whitespace_pattern (str, default: "") — If specified, will override the default whitespace pattern for guided json decoding. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    enable_vision (str, default: "auto") - Controls vision mode, send images to the LLM instead of text chunks. Only for LLMs that support vision, use get_vision_capable_llm_names() to see list. One of ["on", "off", "auto"].
                    visible_vision_models (List[str], default: ["auto"]) - Controls which vision model to use when processing images. Use get_vision_capable_llm_names() to see list. Must provide exactly one model. ["auto"] for automatic.
            max_num_chunks:
                Max limit of chunks to send to the summarizer
            sampling_strategy:
                How to sample if the document has more chunks than max_num_chunks.
                Options are "auto", "uniform", "first", "first+last", default is "auto" (a hybrid of them all).
            pages:
                List of specific pages (of the ingested document in PDF form) to use from the document. 1-based indexing.
            schema:
                Optional JSON schema to use for guided json generation.
            keep_intermediate_results:
                Whether to keep intermediate results. Default: disabled.
                If disabled, further LLM calls are applied to the intermediate results until one global summary is obtained: map+reduce (i.e., summary).
                If enabled, the results' content will be a list of strings (the results of applying the LLM to different pieces of document context): map (i.e., extract).
            guardrails_settings:
                Guardrails Settings.
            meta_data_to_include:
                A dictionary containing flags that indicate whether each piece of document metadata is to be included as part of the context given to the LLM. Only used if enable_vision is disabled.
                Default is {
                    "name": True,
                    "text": True,
                    "page": True,
                    "captions": True,
                    "uri": False,
                    "connector": False,
                    "original_mtime": False,
                    "age": False,
                    "score": False,
                }
            timeout:
                Amount of time in seconds to allow the request to run. The default is 86400 seconds.

        Returns:
            ProcessedDocument: Processed document. The content is either a string (keep_intermediate_results=False) or a list of strings (keep_intermediate_results=True).
        Raises:
            TimeoutError: The request did not complete in time.
            SessionError: No summary or extraction created. Document wasn't part of a collection, or LLM timed out, etc.
        """
        job_id = str(uuid.uuid4())
        ret = await self._job(
            "crawl.DocumentProcessJob",
            job_id=job_id,
            document_id=document_id,
            system_prompt=system_prompt,
            pre_prompt_summary=pre_prompt_summary,
            prompt_summary=prompt_summary,
            llm=llm,
            llm_args=llm_args,
            max_num_chunks=max_num_chunks,
            sampling_strategy=sampling_strategy,
            pages=pages,
            keep_intermediate_results=keep_intermediate_results,
            schema=schema,
            guardrails_settings=guardrails_settings,
            meta_data_to_include=meta_data_to_include,
            timeout=timeout,
            image_batch_image_prompt=image_batch_image_prompt,
            image_batch_final_prompt=image_batch_final_prompt,
        )
        process_job = await self._wait_for_completion(_to_id(ret), timeout=timeout)

        if process_job.failed:
            raise SessionError(str(process_job.errors))

        res = await self._db("get_document_summary", job_id)
        if len(res) == 0:
            raise ObjectNotFoundError(
                {
                    "error": f"Failed to generate the document summary "
                    f"for the document: {document_id}, with job {job_id}"
                }
            )
        if res[0]["error"]:
            raise SessionError(res[0]["error"])
        if keep_intermediate_results:
            res[0]["content"] = ast.literal_eval(res[0]["content"])
        ret = ProcessedDocument(**res[0])
        if ret.error:
            raise SessionError(ret.error)
        return ret

    async def list_recent_document_summaries(
        self, document_id: str, offset: int, limit: int
    ) -> List[ProcessedDocument]:
        """Fetches recent document summaries/extractions/transformations

        Args:
            document_id:
                document ID for which to return summaries
            offset:
                How many summaries to skip before returning summaries.
            limit:
                How many summaries to return.
        """
        ret = [
            ProcessedDocument(**d)
            for d in await self._db(
                "list_recent_document_summaries", document_id, offset, limit
            )
        ]
        for r in ret:
            kwargs = json.loads(r.kwargs)
            if kwargs.get("keep_intermedidate_results"):
                r.content = ast.literal_eval(r.content)
        return ret

    async def encode_for_retrieval(
        self, chunks: Iterable[str], embedding_model: Union[str, None] = None
    ) -> List[List[float]]:
        """
        Encode texts for semantic searching.

        See Also: H2OGPTE.match for getting a list of chunks that semantically match
        each encoded text.

        Args:
            chunks:
                List of strings of texts to be encoded.
            embedding_model:
                embedding model to use. call list_embedding_models() to list of options.
        Returns:
            List of list of floats: Each list in the list is the encoded original text.
        """
        if embedding_model is None:
            embedding_model = await self._lang("get_default_embedding_model")
        return await self._lang(
            "encode_for_retrieval", chunks=chunks, embedding_model=embedding_model
        )

    async def get_chunks(
        self, collection_id: str, chunk_ids: Iterable[int]
    ) -> List[Chunk]:
        """
        Get the text of specific chunks in a collection.

        Args:
            collection_id:
                String id of the collection to search in.
            chunk_ids:
                List of ints for the chunks to return. Chunks are indexed starting at 1.
        Returns:
            Chunk: The text of the chunk.
        Raises:
            Exception: One or more chunks could not be found.
        """
        res = await self._vex("get_chunks", collection_id, chunk_ids=list(chunk_ids))
        return Chunks(**res).result

    async def get_collection(self, collection_id: str) -> Collection:
        """
        Get metadata about a collection.

        Args:
            collection_id:
                String id of the collection to search for.
        Returns:
            Collection: Metadata about the collection.
        Raises:
            KeyError: The collection was not found.
        """
        res = await self._db("get_collection", collection_id)
        if len(res) == 0:
            raise ObjectNotFoundError(
                {"error": f"Collection {collection_id} not found"}
            )
        res[0]["collection_settings"] = json.loads(
            res[0]["collection_settings"]
        )  # str -> dict
        return Collection(**res[0])

    async def get_collection_for_chat_session(self, chat_session_id: str) -> Collection:
        """
        Get metadata about the collection of a chat session.

        Args:
            chat_session_id:
                String id of the chat session to search for.
        Returns:
            Collection: Metadata about the collection.
        """
        res = await self._db("get_collection_for_chat_session", chat_session_id)
        if len(res) == 0:
            raise ObjectNotFoundError({"error": "Collection not found"})
        unmarshal_dict(res[0])
        return Collection(**res[0])

    async def get_document(self, document_id: str) -> Document:
        """
        Fetches information about a specific document.

        Args:
            document_id:
                String id of the document.
        Returns:
            Document: Metadata about the Document.
        Raises:
            KeyError: The document was not found.
        """
        res = await self._db("get_document", document_id)
        if len(res) == 0:
            raise ObjectNotFoundError({"error": f"Document {document_id} not found"})
        unmarshal_dict(res[0])
        return Document(**res[0])

    async def get_job(self, job_id: str) -> Job:
        """
        Fetches information about a specific job.

        Args:
            job_id:
                String id of the job.
        Returns:
            Job: Metadata about the Job.
        """
        res = await self._job(".Get", job_id=job_id)
        if len(res) == 0:
            raise ObjectNotFoundError({"error": f"Job {job_id} not found"})
        return Job(**(res[0]))

    async def get_meta(self) -> Meta:
        """
        Returns various information about the server environment, including the
        current build version, license information, the user, etc.
        """
        response = await self._get("/rpc/meta")
        return Meta(**response)

    async def get_llm_usage_24h(self) -> float:
        return await self._db("get_llm_usage_24h")

    async def get_llm_usage_24h_by_llm(self) -> List[LLMUsage]:
        return [LLMUsage(**d) for d in await self._db("get_llm_usage_24h_by_llm")]

    async def get_llm_usage_24h_with_limits(self) -> LLMUsageLimit:
        res = await self._db("get_llm_usage_24h_with_limits")
        if len(res) == 0:
            raise ObjectNotFoundError({"error": "Cost limit settings not found"})
        return LLMUsageLimit(**res[0])

    async def get_llm_usage_6h(self) -> float:
        return await self._db("get_llm_usage_6h")

    async def get_llm_usage_6h_by_llm(self) -> List[LLMUsage]:
        res = await self._db("get_llm_usage_6h_by_llm")
        return [LLMUsage(**d) for d in res]

    async def get_llm_usage_with_limits(self, interval: str) -> LLMUsageLimit:
        res = await self._db("get_llm_usage_with_limits", interval)
        return LLMUsageLimit(**res)

    async def get_llm_usage_by_llm(self, interval: str) -> List[LLMUsage]:
        res = await self._db("get_llm_usage_by_llm", interval)
        return [LLMUsage(**d) for d in res]

    async def get_llm_usage_by_user(self, interval: str) -> List[UserWithLLMUsage]:
        res = await self._db("get_llm_usage_by_user", interval)
        return [UserWithLLMUsage(**d) for d in res]

    async def get_llm_usage_by_llm_and_user(
        self, interval: str
    ) -> List[LLMWithUserUsage]:
        res = await self._db("get_llm_usage_by_llm_and_user", interval)
        return [LLMWithUserUsage(**d) for d in res]

    async def get_llm_performance_by_llm(self, interval: str) -> List[LLMPerformance]:
        res = await self._db("get_llm_performance_by_llm", interval)
        return [LLMPerformance(**d) for d in res]

    async def get_scheduler_stats(self) -> SchedulerStats:
        """
        Count the number of global, pending jobs on the server.

        Returns:
            SchedulerStats: The queue length for number of jobs.
        """
        ret = await self._job(".Stats")
        return SchedulerStats(**ret)

    async def ingest_from_plain_text(
        self,
        collection_id: str,
        plain_text: str,
        file_name: str,
        gen_doc_summaries: bool = False,
        gen_doc_questions: bool = False,
        timeout: Union[float, None] = None,
    ):
        """Add plain text to a collection.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            plain_text:
                String of the plain text to ingest.
            file_name:
                String of the file name to use for the document.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            timeout:
                Timeout in seconds
        """
        ret = await self._job(
            "crawl.IngestPlainTextJob",
            collection_id=collection_id,
            plain_text=plain_text,
            file_name=file_name,
            gen_doc_summaries=gen_doc_summaries,
            gen_doc_questions=gen_doc_questions,
        )
        return await self._wait_for_completion(_to_id(ret), timeout=timeout)

    async def ingest_from_file_system(
        self,
        collection_id: str,
        root_dir: str,
        glob: str,
        gen_doc_summaries: bool = False,
        gen_doc_questions: bool = False,
        audio_input_language: str = "auto",
        ocr_model: str = "auto",
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
    ) -> Job:
        """
        Add files from the local system into a collection.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            root_dir:
                String path of where to look for files.
            glob:
                String of the glob pattern used to match files in the root directory.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds
        """
        ret = await self._job(
            "crawl.IngestFromFileSystemJob",
            collection_id=collection_id,
            root_dir=root_dir,
            glob=glob,
            gen_doc_summaries=gen_doc_summaries,
            gen_doc_questions=gen_doc_questions,
            audio_input_language=audio_input_language,
            ocr_model=ocr_model,
            tesseract_lang=tesseract_lang,
            keep_tables_as_one_chunk=keep_tables_as_one_chunk,
            chunk_by_page=chunk_by_page,
            handwriting_check=handwriting_check,
        )
        return await self._wait_for_completion(_to_id(ret), timeout=timeout)

    async def ingest_from_s3(
        self,
        collection_id: str,
        url: Union[str, List[str]],
        region: str = "us-east-1",
        credentials: Union[S3Credential, None] = None,
        gen_doc_summaries: bool = False,
        gen_doc_questions: bool = False,
        audio_input_language: str = "auto",
        ocr_model: str = "auto",
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
    ):
        """Add files from the AWS S3 storage into a collection.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            url:
                The path or list of paths of S3 files or directories. Examples: s3://bucket/file, s3://bucket/../dir/
            region:
                The name of the region used for interaction with AWS services.
            credentials:
                The object with S3 credentials. If the object is not provided, only public buckets will be accessible.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds
        """
        res = await create_ingest_job_from_s3(
            h2ogpte_client=self,
            collection_id=collection_id,
            url=url,
            region=region,
            credentials=credentials,
            gen_doc_summaries=gen_doc_summaries,
            gen_doc_questions=gen_doc_questions,
            audio_input_language=audio_input_language,
            ocr_model=ocr_model,
            tesseract_lang=tesseract_lang,
            keep_tables_as_one_chunk=keep_tables_as_one_chunk,
            chunk_by_page=chunk_by_page,
            handwriting_check=handwriting_check,
        )
        return await self._wait_for_completion(_to_id(res), timeout=timeout)

    async def ingest_from_gcs(
        self,
        collection_id: str,
        url: Union[str, List[str]],
        credentials: Union[GCSServiceAccountCredential, None] = None,
        gen_doc_summaries: bool = False,
        gen_doc_questions: bool = False,
        audio_input_language: str = "auto",
        ocr_model: str = "auto",
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
    ):
        """Add files from the Google Cloud Storage into a collection.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            url:
                The path or list of paths of GCS files or directories. Examples: gs://bucket/file, gs://bucket/../dir/
            credentials:
                The object holding a path to a JSON key of Google Cloud service account. If the object is not provided,
                only public buckets will be accessible.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds
        """
        res = await create_ingest_job_from_gcs(
            h2ogpte_client=self,
            collection_id=collection_id,
            url=url,
            credentials=credentials,
            gen_doc_summaries=gen_doc_summaries,
            gen_doc_questions=gen_doc_questions,
            audio_input_language=audio_input_language,
            ocr_model=ocr_model,
            tesseract_lang=tesseract_lang,
            keep_tables_as_one_chunk=keep_tables_as_one_chunk,
            chunk_by_page=chunk_by_page,
            handwriting_check=handwriting_check,
        )
        return await self._wait_for_completion(_to_id(res), timeout=timeout)

    async def ingest_from_azure_blob_storage(
        self,
        collection_id: str,
        container: str,
        path: Union[str, List[str]],
        account_name: str,
        credentials: Union[AzureKeyCredential, AzureSASCredential, None] = None,
        gen_doc_summaries: bool = False,
        gen_doc_questions: bool = False,
        audio_input_language: str = "auto",
        ocr_model: str = "auto",
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
    ):
        """Add files from the Azure Blob Storage into a collection.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            container:
                Name of the Azure Blob Storage container.
            path:
                Path or list of paths to files or directories within an Azure Blob Storage container.
                Examples: file1, dir1/file2, dir3/dir4/
            account_name:
                Name of a storage account
            credentials:
                The object with Azure credentials. If the object is not provided,
                only a public container will be accessible.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds
        """
        res = await create_ingest_job_from_azure_blob_storage(
            h2ogpte_client=self,
            collection_id=collection_id,
            container=container,
            path=path,
            account_name=account_name,
            credentials=credentials,
            gen_doc_summaries=gen_doc_summaries,
            gen_doc_questions=gen_doc_questions,
            audio_input_language=audio_input_language,
            ocr_model=ocr_model,
            tesseract_lang=tesseract_lang,
            keep_tables_as_one_chunk=keep_tables_as_one_chunk,
            chunk_by_page=chunk_by_page,
            handwriting_check=handwriting_check,
        )
        return await self._wait_for_completion(_to_id(res), timeout=timeout)

    async def ingest_uploads(
        self,
        collection_id: str,
        upload_ids: Iterable[str],
        gen_doc_summaries: bool = False,
        gen_doc_questions: bool = False,
        audio_input_language: str = "auto",
        ocr_model: str = "auto",
        restricted: bool = False,
        permissions: Union[List[SharePermission], None] = None,
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
    ) -> Job:
        """
        Add uploaded documents into a specific collection.

        See Also:
            upload: Upload the files into the system to then be ingested into a
                collection.
            delete_upload: Delete uploaded file.
        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            upload_ids:
                List of string ids of each uploaded document to add to the collection.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            restricted:
                Whether the document should be restricted only to certain users.
            permissions:
                List of permissions. Each permission is a SharePermission object.
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds.
        """
        ret = await self._job(
            "crawl.IngestUploadsJob",
            collection_id=collection_id,
            upload_ids=upload_ids,
            gen_doc_summaries=gen_doc_summaries,
            gen_doc_questions=gen_doc_questions,
            audio_input_language=audio_input_language,
            ocr_model=ocr_model,
            tesseract_lang=tesseract_lang,
            keep_tables_as_one_chunk=keep_tables_as_one_chunk,
            chunk_by_page=chunk_by_page,
            handwriting_check=handwriting_check,
            restricted=restricted,
            permissions=[permission.username for permission in permissions]
            if permissions
            else None,
        )
        return await self._wait_for_completion(_to_id(ret), timeout=timeout)

    async def ingest_website(
        self,
        collection_id: str,
        url: str,
        gen_doc_summaries: bool = False,
        gen_doc_questions: bool = False,
        follow_links: bool = False,
        max_depth: int = -1,
        max_documents: Union[int, None] = None,
        audio_input_language: str = "auto",
        ocr_model: str = "auto",
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
    ) -> Job:
        """
        Crawl and ingest a URL into a collection.

        The web page or document linked from this URL will be imported.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            url:
                String of the url to crawl.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            follow_links:
                Whether to import all web pages linked from this URL will be imported.
                External links will be ignored. Links to other pages on the same domain will
                be followed as long as they are at the same level or below the URL you specify.
                Each page will be transformed into a PDF document.
            max_depth:
                Max depth of recursion when following links, only when follow_links is True.
                Max_depth of 0 means don't follow any links, max_depth of 1 means follow only top-level links, etc.
                Use -1 for automatic (system settings).
            max_documents:
                Max number of documents when following links, only when follow_links is True.
                Use None for automatic (system defaults).
                Use -1 for max (system limit).
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds
        """
        ret = await self._job(
            "crawl.IngestWebsiteJob",
            collection_id=collection_id,
            url=url,
            gen_doc_summaries=gen_doc_summaries,
            gen_doc_questions=gen_doc_questions,
            follow_links=follow_links,
            max_depth=max_depth,
            max_documents=max_documents,
            audio_input_language=audio_input_language,
            ocr_model=ocr_model,
            tesseract_lang=tesseract_lang,
            keep_tables_as_one_chunk=keep_tables_as_one_chunk,
            chunk_by_page=chunk_by_page,
            handwriting_check=handwriting_check,
        )
        return await self._wait_for_completion(_to_id(ret), timeout=timeout)

    async def list_chat_messages(
        self, chat_session_id: str, offset: int, limit: int
    ) -> List[ChatMessage]:
        """
        Fetch chat message and metadata for messages in a chat session.

        Messages without a `reply_to` are from the end user, messages with a `reply_to`
        are from an LLM and a response to a specific user message.

        Args:
            chat_session_id:
                String id of the chat session to filter by.
            offset:
                How many chat messages to skip before returning.
            limit:
                How many chat messages to return.
        Returns:
            list of ChatMessage: Text and metadata for chat messages.
        """
        ret = await self._db("list_chat_messages", chat_session_id, offset, limit)
        return [ChatMessage(**{k: v for k, v in d.items() if v != [None]}) for d in ret]

    async def list_chat_message_references(
        self, message_id: str
    ) -> List[ChatMessageReference]:
        """
        Fetch metadata for references of a chat message.

        References are only available for messages sent from an LLM, an empty list
        will be returned for messages sent by the user.

        Args:
            message_id:
                String id of the message to get references for.
        Returns:
            list of ChatMessageReference: Metadata including the document name,
            polygon information, and score.
        """
        ret = await self._db("list_chat_message_references", message_id)
        return [ChatMessageReference(**d) for d in ret]

    async def list_list_chat_message_meta(
        self, message_id: str
    ) -> List[ChatMessageMeta]:
        """
        Fetch chat message meta information.

        Args:
            message_id:
                Message id to which the metadata should be pulled.

        Returns:
            list of ChatMessageMeta: Metadata about the chat message.
        """
        ret = await self._db("list_chat_message_meta", message_id)
        return [ChatMessageMeta(**d) for d in ret]

    async def list_chat_message_meta_part(
        self, message_id: str, info_type: str
    ) -> ChatMessageMeta:
        """
        Fetch one chat message meta information.

        Args:
            message_id:
                Message id to which the metadata should be pulled.
            info_type:
                Metadata type to fetch.
                Valid choices are: "self_reflection", "usage_stats", "prompt_raw", "llm_only", "hyde1"

        Returns:
            ChatMessageMeta: Metadata information about the chat message.
        """
        res = await self._db("list_chat_message_meta_part", message_id, info_type)
        if len(res) == 0:
            raise ObjectNotFoundError(
                {"error": f"Chat meta type not found for {info_type}"}
            )
        return ChatMessageMeta(**res[0])

    async def list_chat_messages_full(
        self, chat_session_id: str, offset: int, limit: int
    ) -> List[ChatMessageFull]:
        """
        Fetch chat message and metadata for messages in a chat session.

        Messages without a `reply_to` are from the end user, messages with a `reply_to`
        are from an LLM and a response to a specific user message.

        Args:
            chat_session_id:
                String id of the chat session to filter by.
            offset:
                How many chat messages to skip before returning.
            limit:
                How many chat messages to return.
        Returns:
            list of ChatMessageFull: Text and metadata for chat messages.
        """
        ret = await self._db("list_chat_messages_full", chat_session_id, offset, limit)
        return [
            ChatMessageFull(**{k: v for k, v in d.items() if v != [None]}) for d in ret
        ]

    async def list_chat_sessions_for_collection(
        self, collection_id: str, offset: int, limit: int
    ) -> List[ChatSessionForCollection]:
        """
        Fetch chat session metadata for chat sessions in a collection.

        Args:
            collection_id:
                String id of the collection to filter by.
            offset:
                How many chat sessions to skip before returning.
            limit:
                How many chat sessions to return.

        Returns:
            list of ChatSessionForCollection: Metadata about each chat session
            including the latest message.
        """
        ret = await self._db(
            "list_chat_sessions_for_collection", collection_id, offset, limit
        )
        return [ChatSessionForCollection(**d) for d in ret]

    async def list_chat_sessions_for_document(
        self, document_id: str, offset: int, limit: int
    ) -> List[ChatSessionForDocument]:
        """Fetch chat session metadata for chat session that produced a specific document (typically through agents).

        Args:
            document_id:
                String id of the document to filter by.
            offset:
                How many chat sessions to skip before returning.
            limit:
                How many chat sessions to return.

        Returns:
            list of ChatSessionForDocument: Metadata about each chat session including the
            latest message.
        """
        ret = await self._db(
            "list_chat_sessions_for_document", document_id, offset, limit
        )
        return [ChatSessionForDocument(**d) for d in ret]

    async def rename_chat_session(self, chat_session_id: str, name: str):
        """Update a chat session name

        Args:
            chat_session_id:
                String id of the document to search for.
            name:
                The new chat session name.
        """
        await self._db("rename_chat_session", chat_session_id, name)

    async def list_collections_for_document(
        self, document_id: str, offset: int, limit: int
    ) -> List[CollectionInfo]:
        """
        Fetch metadata about each collection the document is a part of.
        At this time, each document will only be available in a single collection.

        Args:
            document_id:
                String id of the document to search for.
            offset:
                How many collections to skip before returning.
            limit:
                How many collections to return.

        Returns:
            list of CollectionInfo: Metadata about each collection.
        """
        ret = await self._db(
            "list_collections_for_document", document_id, offset, limit
        )
        return [CollectionInfo(**d) for d in ret]

    async def get_default_collection(self) -> CollectionInfo:
        """Get the default collection, to be used for collection API-keys.

        Returns:
            CollectionInfo: Default collection info.
        """
        res = await self._db("get_default_collection")
        if len(res) == 0:
            raise ObjectNotFoundError(
                {
                    "error": f"Collection not found, "
                    f"or not applicable to non collection API keys"
                }
            )
        return CollectionInfo(**res[0])

    async def list_documents_in_collection(
        self, collection_id: str, offset: int, limit: int
    ) -> List[DocumentInfo]:
        """
        Fetch document metadata for documents in a collection.

        Args:
            collection_id:
                String id of the collection to filter by.
            offset:
                How many documents to skip before returning.
            limit:
                How many documents to return.

        Returns:
            list of DocumentInfo: Metadata about each document.
        """
        dicts = await self._db(
            "list_documents_in_collection", collection_id, offset, limit
        )
        for d in dicts:
            unmarshal_dict(d)
        return [DocumentInfo(**d) for d in dicts]

    async def list_jobs(self) -> List[Job]:
        """
        List the user's jobs.

        Returns:
            list of Job:
        """
        ret = await self._job(".List")
        return [Job(**d) for d in ret if d.get("kind", None) in JobKind.__members__]

    async def list_recent_chat_sessions(
        self, offset: int, limit: int
    ) -> List[ChatSessionInfo]:
        """
        Fetch user's chat session metadata sorted by last update time.
        Chats across all collections will be accessed.

        Args:
            offset:
                How many chat sessions to skip before returning.
            limit:
                How many chat sessions to return.
        Returns:
            list of ChatSessionInfo: Metadata about each chat session including the
            latest message.
        """
        ret = await self._db("list_recent_chat_sessions", offset, limit)
        return [ChatSessionInfo(**d) for d in ret]

    async def list_question_reply_feedback_data(
        self, offset: int, limit: int
    ) -> List[QuestionReplyData]:
        """Fetch user's questions and answers.

        Questions and answers with metadata.

        Args:
            offset:
                How many conversations to skip before returning.
            limit:
                How many conversations to return.

        Returns:
            list of QuestionReplyData: Metadata about questions and answers.
        """
        ret = await self._db("list_question_reply_feedback_data", offset, limit)
        return [QuestionReplyData(**d) for d in ret]

    async def update_question_reply_feedback(
        self, reply_id: str, expected_answer: str, user_comment: str
    ):
        """Update feedback for a specific answer to a question.

        Args:
            reply_id:
                UUID of the reply.
            expected_answer:
                Expected answer.
            user_comment:
                User comment.

        Returns:
            None
        """
        await self._db(
            "update_expected_answer_text", reply_id, expected_answer, user_comment
        )

    async def count_question_reply_feedback(self) -> int:
        """Fetch user's questions and answers count.

        Returns:
            int: the count of questions and replies.
        """
        ret = await self._db("count_question_reply_feedback")
        return QuestionReplyDataCount(**ret).question_reply_data_count

    async def list_recent_collections(
        self, offset: int, limit: int
    ) -> List[CollectionInfo]:
        """
        Fetch user's collection metadata sorted by last update time.

        Args:
            offset:
                How many collections to skip before returning.
            limit:
                How many collections to return.
        Returns:
            list of CollectionInfo: Metadata about each collection.
        """
        ret = await self._db("list_recent_collections", offset, limit)
        return [CollectionInfo(**d) for d in ret]

    async def list_recent_collections_sort(
        self, offset: int, limit: int, sort_column: str, ascending: bool
    ) -> List[CollectionInfo]:
        """
        Fetch user's collection metadata sorted by last update time.

        Args:
            offset:
                How many collections to skip before returning.
            limit:
                How many collections to return.
            sort_column:
                Sort column.
            ascending:
                When True, return sorted by sort_column in ascending order.
        Returns:
            list of CollectionInfo: Metadata about each collection.
        """
        ret = await self._db(
            "list_recent_collections_sort", offset, limit, sort_column, ascending
        )
        return [CollectionInfo(**d) for d in ret]

    async def list_recent_collections_filter(
        self,
        offset: int,
        limit: int,
        current_user_only: bool = False,
        name_filter: str = "",
    ) -> List[CollectionInfo]:
        """
        Fetch user's collection metadata sorted by last update time.

        Args:
            offset:
                How many collections to skip before returning.
            limit:
                How many collections to return.
            current_user_only:
                When true, will only return the user owned collections.
            name_filter:
                Only returns collections with names matching this filter.
        Returns:
            list of CollectionInfo: Metadata about each collection.
        """
        ret = await self._db(
            "list_recent_collections_filter",
            offset,
            limit,
            current_user_only,
            name_filter,
        )
        return [CollectionInfo(**d) for d in ret]

    async def list_collection_permissions(
        self, collection_id: str
    ) -> List[SharePermission]:
        """
        Returns a list of access permissions for a given collection.

        The returned list of permissions denotes who has access to
        the collection and their access level.

        Args:
            collection_id:
                ID of the collection to inspect.
        Returns:
            list of SharePermission: Sharing permissions list for the given collection.
        """
        ret = await self._db("list_collection_permissions", collection_id)
        return [SharePermission(**d) for d in ret]

    async def list_users(self, offset: int, limit: int) -> List[User]:
        """
        List system users.

        Returns a list of all registered users fo the system, a registered user,
        is a users that has logged in at least once.

        Args:
            offset:
                How many users to skip before returning.
            limit:
                How many users to return.
        Returns:
            list of User: Metadata about each user.
        """
        ret = await self._db("list_users", offset, limit)
        return [User(**d) for d in ret]

    async def share_collection(
        self, collection_id: str, permission: SharePermission
    ) -> ShareResponseStatus:
        """
        Share a collection to a user.

        The permission attribute defined the level of access,
        and who can access the collection, the collection_id attribute
        denotes the collection to be shared.

        Args:
            collection_id:
                ID of the collection to share.
            permission:
                Defines the rule for sharing, i.e. permission level.
        Returns:
            ShareResponseStatus: Status of share request.
        """
        ret = await self._db("share_collection", collection_id, permission.username)
        return ShareResponseStatus(**ret)

    async def unshare_collection(
        self, collection_id: str, permission: SharePermission
    ) -> ShareResponseStatus:
        """Remove sharing of a collection to a user.
        The permission attribute defined the level of access,
        and who can access the collection, the collection_id attribute
        denotes the collection to be shared.
        In case of un-sharing, the SharePermission's user is sufficient.

        Args:
            collection_id:
                ID of the collection to un-share.
            permission:
                Defines the user for which collection access is revoked.
        ShareResponseStatus: Status of share request.
        """
        ret = await self._db("unshare_collection", collection_id, permission.username)
        return ShareResponseStatus(**ret)

    async def unshare_collection_for_all(
        self, collection_id: str
    ) -> ShareResponseStatus:
        """Remove sharing of a collection to all other users but the original owner.

        Args:
            collection_id:
                ID of the collection to un-share.
        ShareResponseStatus: Status of share request.
        """
        ret = await self._db("unshare_collection_for_all", collection_id)
        return ShareResponseStatus(**ret)

    async def make_collection_public(self, collection_id: str) -> None:
        """Make a collection public
        Once a collection is public, it will be accessible to all
        authenticated users of the system.

        Args:
            collection_id:
                ID of the collection to make public.
        """
        await self._db("make_collection_public", collection_id)

    async def make_collection_private(self, collection_id: str):
        """Make a collection private
        Once a collection is private, other users will no longer
        be able to access chat history or documents related to
        the collection.

        Args:
            collection_id:
                ID of the collection to make private.
        """
        await self._db("make_collection_private", collection_id)

    async def list_recent_documents(
        self, offset: int, limit: int
    ) -> List[DocumentInfo]:
        """Fetch user's document metadata sorted by last update time.
        All documents owned by the user, regardless of collection, are accessed.

        Args:
            offset:
                How many documents to skip before returning.
            limit:
                How many documents to return.
        Returns:
            list of DocumentInfo: Metadata about each document.
        """
        dicts = await self._db("list_recent_documents", offset, limit)
        for d in dicts:
            unmarshal_dict(d)
        return [DocumentInfo(**d) for d in dicts]

    async def list_recent_documents_with_summaries(
        self, offset: int, limit: int
    ) -> List[DocumentInfoSummary]:
        """Fetch user's document metadata sorted by last update time, including the latest document summary.
        All documents owned by the user, regardless of collection, are accessed.

        Args:
            offset:
                How many documents to skip before returning.
            limit:
                How many documents to return.

        Returns:
            list of DocumentInfoSummary: Metadata about each document.
        """
        dicts = await self._db("list_recent_documents_with_summaries", offset, limit)
        for d in dicts:
            unmarshal_dict(d)
        return [DocumentInfoSummary(**d) for d in dicts]

    async def list_recent_documents_with_summaries_sort(
        self, offset: int, limit: int, sort_column: str, ascending: bool
    ) -> List[DocumentInfoSummary]:
        """Fetch user's document metadata sorted by last update time, including the latest document summary.
        All documents owned by the user, regardless of collection, are accessed.

        Args:
            offset:
                How many documents to skip before returning.
            limit:
                How many documents to return.
            sort_column:
                Sort column.
            ascending:
                When True, return sorted by sort_column in ascending order.

        Returns:
            list of DocumentInfoSummary: Metadata about each document.
        """
        dicts = await self._db(
            "list_recent_documents_with_summaries_sort",
            offset,
            limit,
            sort_column,
            ascending,
        )
        for d in dicts:
            unmarshal_dict(d)
        return [DocumentInfoSummary(**d) for d in dicts]

    async def match_chunks(
        self,
        collection_id: str,
        vectors: List[List[float]],
        topics: List[str],
        offset: int,
        limit: int,
        cut_off: float = 0,
        width: int = 0,
    ) -> List[SearchResult]:
        """Find chunks related to a message using semantic search.
        Chunks are sorted by relevance and similarity score to the message.
        See Also: H2OGPTE.encode_for_retrieval to create vectors from messages.

        Args:
            collection_id:
                ID of the collection to search within.
            vectors:
                A list of vectorized message for running semantic search.
            topics:
                A list of document_ids used to filter which documents in the collection
                to search.
            offset:
                How many chunks to skip before returning chunks.
            limit:
                How many chunks to return.
            cut_off:
                Exclude matches with distances higher than this cut off.
            width:
                How many chunks before and after a match to return - not implemented.
        Returns:
            list of SearchResult: The document, text, score and related information of
            the chunk.
        """
        res = await self._vex(
            "match_chunks",
            collection_id,
            vectors=vectors,
            topics=topics,
            offset=offset,
            limit=limit,
            cut_off=cut_off,
            width=width,
        )
        return SearchResults(**res).result

    async def search_chunks(
        self, collection_id: str, query: str, topics: List[str], offset: int, limit: int
    ) -> List[SearchResult]:
        """Find chunks related to a message using lexical search.
        Chunks are sorted by relevance and similarity score to the message.

        Args:
            collection_id:
                ID of the collection to search within.
            query:
                Question or imperative from the end user to search a collection for.
            topics:
                A list of document_ids used to filter which documents in the collection to search.
            offset:
                How many chunks to skip before returning chunks.
            limit:
                How many chunks to return.
        Returns:
            list of SearchResult: The document, text, score and related information of the chunk.
        """
        res = await self._vex(
            "search_chunks",
            collection_id,
            query=query,
            topics=topics,
            offset=offset,
            limit=limit,
        )
        return SearchResults(**res).result

    async def list_document_chunks(
        self, document_id: str, collection_id: Optional[str] = None
    ) -> List[SearchResult]:
        """Returns all chunks for a specific document.

        Args:
            document_id:
                ID of the document.
            collection_id:
                ID of the collection the document belongs to. If not specified, an arbitrary collections containing
                the document is chosen.
        Returns:
            list of SearchResult: The document, text, score and related information of the chunk.
        """
        if collection_id is None:
            collections = await self.list_collections_for_document(document_id, 0, 1)
            if len(collections) == 0:
                raise ValueError(
                    "The specified document is not associated with any collection."
                )
            collection_id = collections[0].id

        res = await self._vex(
            "search_chunks",
            collection_id,
            query=None,
            topics=[
                document_id,
            ],
            offset=0,
            limit=10000000000,
        )
        return SearchResults(**res).result

    async def set_chat_message_votes(self, chat_message_id: str, votes: int) -> Result:
        """Change the vote value of a chat message.
        Set the exact value of a vote for a chat message. Any message type can
        be updated, but only LLM response votes will be visible in the UI.
        The expectation is 0: unvoted, -1: dislike, 1 like. Values outside of this will
        not be viewable in the UI.

        Args:
            chat_message_id:
                ID of a chat message, any message can be used but only
                LLM responses will be visible in the UI.
            votes:
                Integer value for the message. Only -1 and 1 will be visible in the
                UI as dislike and like respectively.
        Returns:
            Result: The status of the update.
        Raises:
            Exception: The upload request was unsuccessful.
        """
        ret = await self._db("set_chat_message_votes", chat_message_id, votes)
        return Result(**ret)

    async def update_collection(
        self, collection_id: str, name: str, description: str
    ) -> str:
        """Update the metadata for a given collection.
        All variables are required. You can use `h2ogpte.get_collection(<id>).name` or
        description to get the existing values if you only want to change one or the
        other.

        Args:
            collection_id:
                ID of the collection to update.
            name:
                New name of the collection, this is required.
            description:
                New description of the collection, this is required.
        Returns:
            str: ID of the updated collection.
        """
        ret = await self._db("update_collection", collection_id, name, description)
        return _to_id(ret)

    async def update_collection_rag_type(
        self, collection_id: str, name: str, description: str, rag_type
    ) -> str:
        """Update the metadata for a given collection.
        All variables are required. You can use `h2ogpte.get_collection(<id>).name` or
        description to get the existing values if you only want to change one or the
        other.

        Args:
            collection_id:
                ID of the collection to update.
            name:
                New name of the collection, this is required.
            description:
                New description of the collection, this is required.
            rag_type: str one of
                    :code:`"auto"` Automatically select the best rag_type.
                    :code:`"llm_only"` LLM Only - Answer the query without any supporting document contexts.
                        Requires 1 LLM call.
                    :code:`"rag"` RAG (Retrieval Augmented Generation) - Use supporting document contexts
                        to answer the query. Requires 1 LLM call.
                    :code:`"hyde1"` LLM Only + RAG composite - HyDE RAG (Hypothetical Document Embedding).
                        Use 'LLM Only' response to find relevant contexts from a collection for generating
                        a response. Requires 2 LLM calls.
                    :code:`"hyde2"` HyDE + RAG composite - Use the 'HyDE RAG' response to find relevant
                        contexts from a collection for generating a response. Requires 3 LLM calls.
                    :code:`"rag+"` Summary RAG - Like RAG, but uses more context and recursive
                        summarization to overcome LLM context limits. Keeps all retrieved chunks, puts
                        them in order, adds neighboring chunks, then uses the summary API to get the
                        answer. Can require several LLM calls.
                    :code:`"all_data"` All Data RAG - Like Summary RAG, but includes all document
                        chunks. Uses recursive summarization to overcome LLM context limits.
                        Can require several LLM calls.

        Returns:
            str: ID of the updated collection.
        """
        ret = await self._db(
            "update_collection_rag_type", collection_id, name, description, rag_type
        )
        return _to_id(ret)

    async def reset_collection_prompt_settings(self, collection_id: str) -> str:
        """Reset the prompt settings for a given collection.

        Args:
            collection_id:
                ID of the collection to update.
        Returns:
            str: ID of the updated collection.
        """
        ret = await self._db(
            "reset_collection_prompt_settings",
            collection_id,
        )
        return _to_id(ret)

    async def update_collection_settings(
        self, collection_id: str, collection_settings: dict
    ) -> str:
        """
        Set the new collection settings, must be complete.
        Be careful not to delete any settings you want to keep.

        Args:
            collection_id:
                ID of the collection to update.
            collection_settings:
                Dictionary containing the new collection settings.

        Returns:
            str: ID of the updated collection.
        """
        ret = await self._db(
            "update_collection_settings", collection_id, json.dumps(collection_settings)
        )
        return _to_id(ret)

    async def update_document_name(self, document_id: str, name: str) -> str:
        """Update the name metadata for a given document.

        Args:
            document_id:
                ID of the document to update.
            name:
                New name of the document, must include file extension.

        Returns:
            str: ID of the updated document.
        """

        ret = await self._db("update_document_name", document_id, name.strip())
        return _to_id(ret)

    async def update_document_uri(self, document_id: str, uri: str) -> str:
        """Update the URI metadata for a given document.

        Args:
            document_id:
                ID of the document to update.
            uri:
                New URI of the document, this is required.

        Returns:
            str: ID of the updated document.
        """
        ret = await self._db("update_document_uri", document_id, uri.strip())
        return _to_id(ret)

    async def upload(
        self, file_name: str, file: Union[IO[bytes], bytes], uri: Optional[str] = None
    ) -> str:
        """Upload a file to the H2OGPTE backend.
        Uploaded files are not yet accessible and need to be ingested into a collection.

        See Also:
            ingest_uploads: Add the uploaded files to a collection.
            delete_upload: Delete uploaded file

        Args:
            file_name:
                What to name the file on the server, must include file extension.
            file:
                File object to upload, often an opened file from `with open(...) as f`.
            uri:
                Optional - URI you would like to associate with the file.
        Returns:
            str: The upload id to be used in ingest jobs.
        Raises:
            Exception: The upload request was unsuccessful.
        """
        headers = await self._get_auth_header()
        mtime = ""
        try:
            mtime = str(
                int(Path(file.name).stat().st_mtime) * 1000
            )  # millis since Epoch
        except:
            pass

        files_data = {
            "file": (file_name, file),
            "mtime": (None, mtime),
            "uri": (None, uri or ""),
        }

        res = await self._client.put(
            f"{self._address}/rpc/fs",
            files=files_data,
            headers=headers,
        )
        self._raise_error_if_any(res)
        return _to_id(json.loads(res.text))

    async def list_upload(self) -> List[str]:
        """List pending file uploads to the H2OGPTE backend.
        Uploaded files are not yet accessible and need to be ingested into a collection.

        See Also:
            upload: Upload the files into the system to then be ingested into a collection.
            ingest_uploads: Add the uploaded files to a collection.
            delete_upload: Delete uploaded file

        Returns:
            List[str]: The pending upload ids to be used in ingest jobs.

        Raises:
            Exception: The upload list request was unsuccessful.
        """
        headers = await self._get_auth_header()
        res = await self._client.get(
            f"{self._address}/rpc/fs",
            headers=headers,
        )
        self._raise_error_if_any(res)
        return json.loads(res.text)

    async def delete_upload(self, upload_id: str) -> str:
        """Delete a file previously uploaded with the "upload" method.

        See Also:
            upload: Upload the files into the system to then be ingested into a collection.
            ingest_uploads: Add the uploaded files to a collection.
        Args:
            upload_id:
                ID of a file to remove
        Returns:
            upload_id: The upload id of the removed.
        Raises:
            Exception: The delete upload request was unsuccessful.
        """
        res = await self._delete(f"rpc/fs?id={upload_id}")
        return _to_id(res)

    def connect(
        self,
        chat_session_id: str,
        rag_type: Optional[str] = None,
        prompt_template_id: Optional[str] = None,
    ) -> SessionAsync:
        """Create and participate in a chat session.
        This is a live connection to the H2OGPTE server contained to a specific
        chat session on top of a single collection of documents. Users will find all
        questions and responses in this session in a single chat history in the UI.

        Args:
            chat_session_id:
                ID of the chat session to connect to.
            rag_type:
                RAG type to use.
            prompt_template_id:
                ID of the prompt template to use.

        Returns:
            Session: Live chat session connection with an LLM.
        """
        return SessionAsync(
            chat_session_id=chat_session_id,
            client=self,
            prompt_template_id=prompt_template_id,
        )

    async def get_llms(self) -> List[Dict[str, Any]]:
        """
        Lists metadata information about available LLMs in the environment.

        Returns:
            list of dict (string, ANY): Name and details about each available model.
        """
        return await self._lang("get_llms")

    async def get_llm_names(self) -> List[str]:
        """
        Lists names of available LLMs in the environment.

        Returns:
            list of string: Name of each available model.
        """
        return await self._lang("get_llm_names")

    async def get_vision_capable_llm_names(self) -> List[str]:
        """Lists names of available vision-capable multi-modal LLMs (that can natively handle images as input) in the environment.

        Returns:
            list of string: Name of each available model.

        """
        return await self._lang("get_vision_capable_llm_names")

    async def get_llm_and_auto_vision_llm_names(self) -> Dict[str, str]:
        """
        Get mapping of llm to its vision_model when ["auto"] is passed as visible_vision_models

        Returns:
            dictionary {'llm1': 'llm1_vision_llm', etc.}
        """
        return await self._lang("get_llm_and_auto_vision_llm_names")

    async def download_document(
        self,
        destination_directory: Union[str, Path],
        destination_file_name: str,
        document_id: str,
    ) -> Path:
        """Downloads a document to a local system directory.

        Args:
            destination_directory:
                Destination directory to save file into.
            destination_file_name:
                Destination file name.
            document_id:
                Document ID.

        Returns:
            The Path to the file written to disk.
        """
        destination_directory = Path(destination_directory)
        destination_file = destination_directory / destination_file_name
        if not destination_directory.is_dir():
            raise FileNotFoundError("Destination directory does not exist")
        if destination_file.exists():
            raise FileExistsError(f"File {destination_file} already exists")

        headers = await self._get_auth_header()
        res = await self._client.get(
            f"{self._address}/file?id={document_id}&name={quote(destination_file_name)}",
            headers=headers,
        )
        self._raise_error_if_any(res)

        async with aiofiles.open(destination_file, "wb") as f:
            await f.write(res.content)
        return destination_file

    async def list_recent_prompt_templates(
        self, offset: int, limit: int
    ) -> List[PromptTemplate]:
        """Fetch user's prompt templates sorted by last update time.

        Args:
            offset:
                How many prompt templates to skip before returning.
            limit:
                How many prompt templates to return.

        Returns:
            list of PromptTemplate: set of prompts
        """
        return [
            PromptTemplate(**d)
            for d in await self._db("list_recent_prompt_templates", offset, limit)
        ]

    async def list_recent_prompt_templates_sort(
        self, offset: int, limit: int, sort_column: str, ascending: bool
    ) -> List[PromptTemplate]:
        """Fetch user's prompt templates sorted by last update time.

        Args:
            offset:
                How many prompt templates to skip before returning.
            limit:
                How many prompt templates to return.
            sort_column:
                Sort column.
            ascending:
                When True, return sorted by sort_column in ascending order.

        Returns:
            list of PromptTemplate: set of prompts
        """
        return [
            PromptTemplate(**d)
            for d in await self._db(
                "list_recent_prompt_templates_sort",
                offset,
                limit,
                sort_column,
                ascending,
            )
        ]

    async def get_prompt_template(self, id: Optional[str] = None) -> PromptTemplate:
        """Get a prompt template

        Args:
            id:
                String id of the prompt template to retrieve or None for default

        Returns:
            PromptTemplate: prompts

        Raises:
            KeyError: The prompt template was not found.
        """
        if id is None:
            res = await self._lang("get_default_prompt_template")
            return PromptTemplate(**res)
        res = await self._db("get_prompt_template", id)
        if len(res) == 0:
            raise ObjectNotFoundError({"error": f"Prompt Template {id} not found"})
        return PromptTemplate(**res[0])

    async def delete_prompt_templates(self, ids: Iterable[str]) -> Result:
        """Deletes prompt templates

        Args:
            ids:
                List of string ids of prompte templates to delete from the system.

        Returns:
            Result: Status of the delete job.
        """
        res = await self._db("delete_prompt_templates", ids)
        return Result(**res)

    async def update_prompt_template(
        self,
        id: str,
        name: str,
        description: Union[str, None] = None,
        lang: Union[str, None] = None,
        system_prompt: Union[str, None] = None,
        pre_prompt_query: Union[str, None] = None,
        prompt_query: Union[str, None] = None,
        hyde_no_rag_llm_prompt_extension: Union[str, None] = None,
        pre_prompt_summary: Union[str, None] = None,
        prompt_summary: Union[str, None] = None,
        system_prompt_reflection: Union[str, None] = None,
        pre_prompt_reflection: Union[str, None] = None,
        prompt_reflection: Union[str, None] = None,
        auto_gen_description_prompt: Union[str, None] = None,
        auto_gen_document_summary_pre_prompt_summary: Union[str, None] = None,
        auto_gen_document_summary_prompt_summary: Union[str, None] = None,
        auto_gen_document_sample_questions_prompt: Union[str, None] = None,
        default_sample_questions: Union[List[str], None] = None,
        image_batch_image_prompt: Union[str, None] = None,
        image_batch_final_prompt: Union[str, None] = None,
    ) -> str:
        """
        Update a prompt template

        Args:
            id:
                String ID of the prompt template to update
            name:
                Name of the prompt template
            description:
                Description of the prompt template
            lang:
                Language code
            system_prompt:
                System Prompt
            pre_prompt_query:
                Text that is prepended before the contextual document chunks.
            prompt_query:
                Text that is appended to the beginning of the user's message.
            hyde_no_rag_llm_prompt_extension:
                LLM prompt extension.
            pre_prompt_summary:
                Prompt that goes before each large piece of text to summarize
            prompt_summary:
                Prompt that goes after each large piece of text to summarize
            system_prompt_reflection:
                System Prompt for self-reflection
            pre_prompt_reflection:
                Deprecated - ignored
            prompt_reflection:
                Template for self-reflection, must contain two occurrences of %s for full previous prompt (including system prompt, document related context and prompts if applicable, and user prompts) and answer
            auto_gen_description_prompt:
                prompt to create a description of the collection.
            auto_gen_document_summary_pre_prompt_summary:
                pre_prompt_summary for summary of a freshly imported document (if enabled).
            auto_gen_document_summary_prompt_summary:
                prompt_summary for summary of a freshly imported document (if enabled).
            auto_gen_document_sample_questions_prompt:
                prompt to create sample questions for a freshly imported document (if enabled).
            default_sample_questions:
                default sample questions in case there are no auto-generated sample questions.
            image_batch_final_prompt:
                Prompt for each image batch for vision models
            image_batch_image_prompt:
                Prompt to reduce all answers each image batch for vision models

        Returns:
            str: The ID of the updated prompt template.
        """
        if prompt_reflection is not None:
            assert prompt_reflection.count("%s") == 2, (
                "prompt reflection must contain exactly two occurrences of %s "
                "(one for the full previous prompt including system prompt, document related context and prompts if applicable, and user prompts and one for the response)"
            )
        if pre_prompt_reflection:
            raise DeprecationWarning(
                "pre_prompt_reflection is no longer used, can be added to the beginning of prompt_reflection."
            )
        return _to_id(
            await self._db(
                "update_prompt_template",
                id,
                name,
                description,
                lang,
                system_prompt,
                pre_prompt_query,
                prompt_query,
                hyde_no_rag_llm_prompt_extension,
                pre_prompt_summary,
                prompt_summary,
                system_prompt_reflection,
                pre_prompt_reflection,
                prompt_reflection,
                auto_gen_description_prompt,
                auto_gen_document_summary_pre_prompt_summary,
                auto_gen_document_summary_prompt_summary,
                auto_gen_document_sample_questions_prompt,
                default_sample_questions,
                image_batch_image_prompt,
                image_batch_final_prompt,
            )
        )

    async def create_prompt_template(
        self,
        name: str,
        description: Union[str, None] = None,
        lang: Union[str, None] = None,
        system_prompt: Union[str, None] = None,
        pre_prompt_query: Union[str, None] = None,
        prompt_query: Union[str, None] = None,
        hyde_no_rag_llm_prompt_extension: Union[str, None] = None,
        pre_prompt_summary: Union[str, None] = None,
        prompt_summary: Union[str, None] = None,
        system_prompt_reflection: Union[str, None] = None,
        pre_prompt_reflection: Union[str, None] = None,
        prompt_reflection: Union[str, None] = None,
        auto_gen_description_prompt: Union[str, None] = None,
        auto_gen_document_summary_pre_prompt_summary: Union[str, None] = None,
        auto_gen_document_summary_prompt_summary: Union[str, None] = None,
        auto_gen_document_sample_questions_prompt: Union[str, None] = None,
        default_sample_questions: Union[List[str], None] = None,
        image_batch_image_prompt: Union[str, None] = None,
        image_batch_final_prompt: Union[str, None] = None,
    ) -> str:
        """
        Create a new prompt template

        Args:
            name:
                Name of the prompt template
            description:
                Description of the prompt template
            lang:
                Language code
            system_prompt:
                System Prompt
            pre_prompt_query:
                Text that is prepended before the contextual document chunks.
            prompt_query:
                Text that is appended to the beginning of the user's message.
            hyde_no_rag_llm_prompt_extension:
                LLM prompt extension.
            pre_prompt_summary:
                Prompt that goes before each large piece of text to summarize
            prompt_summary:
                Prompt that goes after each large piece of text to summarize
            system_prompt_reflection:
                System Prompt for self-reflection
            pre_prompt_reflection:
                Deprecated - ignored
            prompt_reflection:
                Template for self-reflection, must contain two occurrences of %s for full previous prompt (including system prompt, document related context and prompts if applicable, and user prompts) and answer
            auto_gen_description_prompt:
                prompt to create a description of the collection.
            auto_gen_document_summary_pre_prompt_summary:
                pre_prompt_summary for summary of a freshly imported document (if enabled).
            auto_gen_document_summary_prompt_summary:
                prompt_summary for summary of a freshly imported document (if enabled).
            auto_gen_document_sample_questions_prompt:
                prompt to create sample questions for a freshly imported document (if enabled).
            default_sample_questions:
                default sample questions in case there are no auto-generated sample questions.
            image_batch_final_prompt:
                Prompt for each image batch for vision models
            image_batch_image_prompt:
                Prompt to reduce all answers each image batch for vision models

        Returns:
            str: The ID of the newly created prompt template.
        """
        if prompt_reflection is not None:
            assert prompt_reflection.count("%s") == 2, (
                "prompt reflection must contain exactly two occurrences of %s "
                "(one for the full previous prompt including system prompt, document related context and prompts if applicable, and user prompts and one for the response)"
            )
        if pre_prompt_reflection:
            raise DeprecationWarning(
                "pre_prompt_reflection is no longer used, can be added to the beginning of prompt_reflection."
            )
        res = await self._db(
            "create_prompt_template",
            name,
            description,
            lang,
            system_prompt,
            pre_prompt_query,
            prompt_query,
            hyde_no_rag_llm_prompt_extension,
            pre_prompt_summary,
            prompt_summary,
            system_prompt_reflection,
            pre_prompt_reflection,
            prompt_reflection,
            auto_gen_description_prompt,
            auto_gen_document_summary_pre_prompt_summary,
            auto_gen_document_summary_prompt_summary,
            auto_gen_document_sample_questions_prompt,
            default_sample_questions,
            image_batch_image_prompt,
            image_batch_final_prompt,
        )
        return _to_id(res)

    async def count_prompt_templates(self) -> int:
        """Counts number of prompt templates

        Returns:
            int: The count of prompt templates
        """
        res = await self._db("count_prompt_templates")
        return PromptTemplateCount(**res).prompt_template_count

    async def share_prompt(
        self, prompt_id: str, permission: SharePermission
    ) -> ShareResponseStatus:
        """Share a prompt template to a user.

        Args:
            prompt_id:
                ID of the prompt template to share.
            permission:
                Defines the rule for sharing, i.e. permission level.

        Returns:
            ShareResponseStatus: Status of share request.
        """
        ret = await self._db("share_prompt", prompt_id, permission.username)
        return ShareResponseStatus(**ret)

    async def unshare_prompt(
        self, prompt_id: str, permission: SharePermission
    ) -> ShareResponseStatus:
        """Remove sharing of a prompt template to a user.

        Args:
            prompt_id:
                ID of the prompt template to un-share.
            permission:
                Defines the user for which collection access is revoked.

        ShareResponseStatus: Status of share request.
        """
        ret = await self._db("unshare_prompt", prompt_id, permission.username)
        return ShareResponseStatus(**ret)

    async def unshare_prompt_for_all(self, prompt_id: str) -> ShareResponseStatus:
        """Remove sharing of a prompt template to all other users but the original owner

        Args:
            prompt_id:
                ID of the prompt template to un-share.

        ShareResponseStatus: Status of share request.
        """
        ret = await self._db("unshare_prompt_for_all", prompt_id)
        return ShareResponseStatus(**ret)

    async def list_prompt_permissions(self, prompt_id: str) -> List[SharePermission]:
        """Returns a list of access permissions for a given prompt template.

        The returned list of permissions denotes who has access to
        the prompt template and their access level.

        Args:
            prompt_id:
                ID of the prompt template to inspect.

        Returns:
            list of SharePermission: Sharing permissions list for the given prompt template.
        """
        ret = await self._db("list_prompt_permissions", prompt_id)
        return [SharePermission(**d) for d in ret]

    async def set_collection_prompt_template(
        self,
        collection_id: str,
        prompt_template_id: Union[str, None],
        strict_check: bool = False,
    ) -> str:
        """Set the prompt template for a collection

        Args:
            collection_id:
                ID of the collection to update.
            prompt_template_id:
                ID of the prompt template to get the prompts from. None to delete and fall back to system defaults.
            strict_check:
                whether to check that the collection's embedding model and the prompt template are optimally compatible

        Returns:
            str: ID of the updated collection.
        """
        if prompt_template_id is None:
            res = await self._db(
                "reset_collection_prompt_template",
                collection_id,
            )
        else:
            prompt_template = await self.get_prompt_template(prompt_template_id)
            embedding_model = (await self.get_collection(collection_id)).embedding_model
            if embedding_model:
                emb_dict = await self._lang("get_embedding_models_dict")
                if embedding_model in emb_dict:
                    langs = emb_dict[embedding_model]["languages"]
                    if (
                        langs
                        and prompt_template.lang
                        and prompt_template.lang not in langs
                    ):
                        msg = (
                            f"Warning: The embedding model only supports the following languages: {langs}, "
                            f"but the prompt template specifies the following language: {prompt_template.lang}. "
                            f"Retrieval performance may not be ideal."
                        )
                        print(msg)
                        if strict_check:
                            raise RuntimeError(msg)
            res = await self._db(
                "set_collection_prompt_template",
                collection_id,
                prompt_template_id,
            )
        return _to_id(res)

    async def get_collection_prompt_template(
        self, collection_id: str
    ) -> Union[PromptTemplate, None]:
        """Get the prompt template for a collection

        Args:
            collection_id:
                ID of the collection

        Returns:
            str: ID of the prompt template.
        """
        res = await self._db(
            "get_collection_prompt_template",
            collection_id,
        )
        if len(res) == 0:
            raise ObjectNotFoundError(
                {"error": f"Collection {collection_id} not found"}
            )
        prompt_template_id = res[0]["prompt_template_id"]
        if prompt_template_id is None:
            return None
        res = await self._db("get_prompt_template", prompt_template_id)
        if len(res) == 0:
            raise ObjectNotFoundError(
                {"error": f"Prompt Template {prompt_template_id} not found"}
            )
        return PromptTemplate(**res[0])

    async def set_chat_session_prompt_template(
        self, chat_session_id: str, prompt_template_id: Union[str, None]
    ) -> str:
        """Set the prompt template for a chat_session

        Args:
            chat_session_id:
                ID of the chat session
            prompt_template_id:
                ID of the prompt template to get the prompts from. None to delete and fall back to system defaults.

        Returns:
            str: ID of the updated chat session
        """
        if prompt_template_id is None:
            res = await self._db("reset_chat_session_prompt_template", chat_session_id)
        else:
            res = await self._db(
                "set_chat_session_prompt_template",
                chat_session_id,
                prompt_template_id,
            )
        return _to_id(res)

    async def get_chat_session_prompt_template(
        self, chat_session_id: str
    ) -> Union[PromptTemplate, None]:
        """Get the prompt template for a chat_session

        Args:
            chat_session_id:
                ID of the chat session

        Returns:
            str: ID of the prompt template.
        """
        res = await self._db(
            "get_chat_session_prompt_template",
            chat_session_id,
        )
        if len(res) == 0:
            raise ObjectNotFoundError(
                {"error": f"Chat session {chat_session_id} not found"}
            )
        prompt_template_id = res[0]["prompt_template_id"]
        if prompt_template_id is None:
            return None
        res = await self._db("get_prompt_template", prompt_template_id)
        if len(res) == 0:
            raise ObjectNotFoundError(
                {"error": f"Prompt Template {prompt_template_id} not found"}
            )
        return PromptTemplate(**res[0])

    async def set_chat_session_collection(
        self, chat_session_id: str, collection_id: Union[str, None]
    ) -> str:
        """Set the prompt template for a chat_session

        Args:
            chat_session_id:
                ID of the chat session
            collection_id:
                ID of the collection, or None to chat with the LLM only.

        Returns:
            str: ID of the updated chat session
        """
        res = await self._db(
            "set_chat_session_collection",
            chat_session_id,
            collection_id,
        )
        return _to_id(res)

    async def download_reference_highlighting(
        self, message_id: str, destination_directory: str, output_type: str = "combined"
    ) -> list:
        """Get PDFs with reference highlighting

        Args:
            message_id:
                ID of the message to get references from
            destination_directory:
                Destination directory to save files into.
            output_type: str one of
                :code:`"combined"` Generates a PDF file for each source document, with all relevant chunks highlighted
          in each respective file. This option consolidates all highlights for each source document
          into a single PDF, making it easy to view all highlights related to that document at once.
                :code:`"split"` Generates a separate PDF file for each chunk, with only the relevant chunk
          highlighted in each file. This option is useful for focusing on individual sections without
          interference from other parts of the text. The output files names will be in the format "{document_id}_{chunk_id}.pdf"

        Returns:
            list[Path]: List of paths of downloaded documents with highlighting

        """
        if not os.path.exists(destination_directory) or not os.path.isdir(
            destination_directory
        ):
            raise FileNotFoundError("Destination directory does not exist")

        chat_references = await self.list_chat_message_references(message_id)
        doc_chat_references = defaultdict(list)
        for chat_ref in chat_references:
            doc_chat_references[(chat_ref.document_id, chat_ref.document_name)].append(
                chat_ref
            )

        doc_dict = {}
        files_list = []
        for (document_id, document_name), chat_refs in doc_chat_references.items():
            headers = await self._get_auth_header()
            res = await self._client.get(
                f"{self._address}/file?id={document_id}&name={quote(document_name)}",
                headers=headers,
            )
            if res.status_code != 200:
                print(
                    f"Warning: HTTP error: {res.status_code}. document_id={document_id}"
                )
                continue

            if not res.content:
                print(f"Warning: received an empty response. document_id={document_id}")
                continue

            pymupdf = import_pymupdf()
            pdf_document = pymupdf.open("pdf", res.content)
            markers = []

            for ref in chat_refs:
                markers.append(ref.model_dump_json())

            filepaths = _process_pdf_with_annotations(
                pdf_document, markers, destination_directory, document_id, output_type
            )
            files_list.extend(filepaths)

        return files_list

    async def tag_document(self, document_id: str, tag_name: str) -> str:
        """Adds a tag to a document.

        Args:
            document_id:
                String id of the document to attach the tag to.
            tag_name:
                String representing the tag to attach.

        Returns:
            String: The id of the newly created tag.
        """
        res = await self._db("tag_document", document_id, tag_name)

        return _to_id(res)

    async def untag_document(self, document_id: str, tag_name: str) -> str:
        """Removes an existing tag from a document.

        Args:
            document_id:
                String id of the document to remove the tag from.
            tag_name:
                String representing the tag to remove.

        Returns:
            String: The id of the removed tag.
        """
        res = await self._db("untag_document", document_id, tag_name)

        return _to_id(res)

    async def get_tag(self, tag_name: str) -> Tag:
        """Returns an existing tag.

        Args:
            tag_name:
                String The name of the tag to retrieve.

        Returns:
            Tag: The requested tag.

        Raises:
            KeyError: The tag was not found.
        """
        res = await self._db("get_tag", tag_name)

        if len(res) == 0:
            raise ObjectNotFoundError({"error": f"Tag {tag_name} not found"})
        return Tag(**res[0])

    async def create_tag(self, tag_name: str) -> str:
        """Creates a new tag.

        Args:
            tag_name:
                String representing the tag to create.

        Returns:
            String: The id of the created tag.
        """
        res = await self._db("create_tag", tag_name)

        return _to_id(res)

    async def update_tag(self, tag_name: str, description: str, format: str) -> str:
        """Updates a  tag.

        Args:
            tag_name:
                String representing the tag to update.
            description:
                String describing the tag.
            format:
                String representing the format of the tag.

        Returns:
            String: The id of the updated tag.
        """
        res = await self._db("update_tag", tag_name, description, format)

        return _to_id(res)

    async def list_all_tags(self) -> List[Tag]:
        """Lists all existing tags.

        Returns:
            List of Tags: List of existing tags.
        """

        return [Tag(**d) for d in await self._db("list_all_tags")]

    async def list_documents_from_tags(
        self, collection_id: str, tags: List[str]
    ) -> List[Document]:
        """Lists documents that have the specified set of tags within a collection.
        Args:
            collection_id:
                String The id of the collection to find documents in.
            tags:
                List of Strings representing the tags to retrieve documents for.

        Returns:
            List of Documents: All the documents with the specified tags.
        """

        res = [
            await self.get_document(d["document_id"])
            for d in await self._db("list_documents_from_tags", collection_id, tags)
        ]
        return res

    async def add_user_document_permission(
        self, user_id: str, document_id: str
    ) -> [str, str]:
        """Associates a user with a document they have permission on.
        Args:
            user_id:
                String The id of the user that has the permission.
            document_id:
                String The id of the document that the permission is for.

        Returns:
            [user_id, document_id]: A tuple containing the user_id and document_id.
        """

        res = await self._db("add_user_document_permission", user_id, document_id)

        return res

    async def list_system_permissions(self) -> List[UserPermission]:
        return [UserPermission(**p) for p in await self._db("get_permissions")]

    async def list_system_roles(self) -> List[UserRole]:
        return [UserRole(**r) for r in await self._db("get_roles")]

    async def list_user_roles(self, user_id: Optional[str] = None) -> List[UserRole]:
        if user_id:
            return [
                UserRole(**r) for r in await self._db("get_other_user_roles", user_id)
            ]
        return [UserRole(**r) for r in await self._db("get_user_roles")]

    async def list_user_permissions(
        self, user_id: Optional[str] = None
    ) -> List[UserPermission]:
        if user_id:
            return [
                UserPermission(**p)
                for p in await self._db("get_other_user_permissions", user_id)
            ]
        return [UserPermission(**p) for p in await self._db("get_user_permissions")]

    async def list_user_role_permissions(
        self, roles: List[str]
    ) -> List[UserPermission]:
        return [
            UserPermission(**p) for p in await self._db("get_role_permissions", roles)
        ]

    async def add_role_to_user(self, user_id: str, roles: List[str]) -> List[UserRole]:
        return [
            UserRole(**r) for r in await self._db("add_role_to_user", user_id, roles)
        ]

    async def reset_roles_for_user(
        self, user_id: str, roles: List[str]
    ) -> List[UserRole]:
        return [
            UserRole(**r)
            for r in await self._db("reset_roles_for_user", user_id, roles)
        ]

    async def remove_role_from_user(
        self, user_id: str, roles: List[str]
    ) -> List[UserRole]:
        return [
            UserRole(**r)
            for r in await self._db("remove_role_from_user", user_id, roles)
        ]

    async def is_permission_granted(self, permission: str) -> bool:
        return bool(await self._db("is_permission_granted", permission))

    async def is_collection_permission_granted(
        self, collection_id: str, permission: str
    ) -> bool:
        return bool(
            self._db("is_collection_permission_granted", collection_id, permission)
        )

    async def create_user_role(self, name: str, description: str) -> UserRole:
        res = await self._db("create_user_role", name, description)
        if len(res) == 0:
            raise ObjectNotFoundError({"error": "Role not found"})
        return UserRole(**res[0])

    async def delete_user_roles_by_ids(self, roles_ids: Iterable[str]) -> Result:
        ret = await self._db("delete_user_roles_by_ids", roles_ids)
        return Result(**ret)

    async def delete_user_roles_by_names(self, roles_names: Iterable[str]) -> Result:
        ret = await self._db("delete_user_roles_by_names", roles_names)
        return Result(**ret)

    async def assign_permissions_to_role(
        self, role_name: str, permission_names: Iterable[str]
    ) -> Result:
        ret = await self._db("assign_permissions_to_role", role_name, permission_names)
        return Result(**ret)

    # ----------------------------------------------------------------------------------
    # Private
    # ----------------------------------------------------------------------------------

    async def _check_version(self, strict: bool):
        from h2ogpte import __version__ as client_version

        server_version = (await self.get_meta()).version
        server_version = server_version.lstrip("v")

        if server_version != client_version:
            msg = (
                f"Server version {server_version} doesn't match client "
                f"version {client_version}, unexpected errors may occur.\n"
                f"Please install the correct version of H2OGPTE "
                f"with `pip install h2ogpte=={server_version}`."
            )
            if strict:
                raise RuntimeError(msg)
            else:
                print(
                    f"Warning: {msg}\n"
                    "You can enable strict version checking by passing "
                    "strict_version_check=True."
                )

    async def _get(self, endpoint: str) -> Any:
        headers = await self._get_auth_header()
        res = await self._client.get(
            self._address + endpoint,
            timeout=H2OGPTEAsync.TIMEOUT,
            headers=headers,
        )
        self._raise_error_if_any(res)
        return res.json()

    async def _post(self, endpoint: str, data: Any) -> Any:
        headers = await self._get_auth_header()
        content = json.dumps(data, allow_nan=False, separators=(",", ":"))
        res = await self._client.post(
            self._address + endpoint,
            content=content,
            timeout=H2OGPTEAsync.TIMEOUT,
            headers=headers,
        )
        self._raise_error_if_any(res)
        return res.json()

    async def _delete(self, endpoint: str) -> Any:
        headers = await self._get_auth_header()
        res = await self._client.delete(
            self._address + endpoint,
            timeout=H2OGPTEAsync.TIMEOUT,
            headers=headers,
        )
        self._raise_error_if_any(res)
        return res.json()

    async def _db(self, method: str, *args: Any) -> Any:
        return await self._post("/rpc/db", [method, *args])

    async def _lang(self, method: str, **kwargs: Any) -> Any:
        res = await self._post("/rpc/lang", {"method": method, "params": kwargs})
        ret = res["result"]
        if isinstance(ret, dict) and ret.get("error"):
            raise SessionError(ret["error"])
        return ret

    async def _vex(self, method: str, collection_id: str, **kwargs: Any) -> Any:
        return await self._post(
            "/rpc/vex",
            {"method": method, "collection_id": collection_id, "params": kwargs},
        )

    async def _job(self, method: str, **kwargs: Any) -> Any:
        request_id = str(uuid.uuid4())
        return await self._post("/rpc/job", [method, kwargs, request_id])

    async def _wait_for_completion(
        self, job_id: str, timeout: Optional[float] = None
    ) -> Job:
        if timeout is None:
            timeout = 86400
        deadline = time.time() + timeout
        dt = H2OGPTEAsync.INITIAL_WAIT_INTERVAL
        last_job: Optional[Job] = None
        while True:
            job = await self.get_job(job_id)
            if job.completed or job.canceled:
                break
            if last_job is not None and last_job.progress == job.progress:
                if time.time() > deadline:
                    raise TimeoutError(
                        f"Job {job.kind} ({job_id}) timed out after {timeout} seconds"
                    )
            else:
                last_job = job
                deadline = time.time() + timeout
            await asyncio.sleep(dt)
            dt = min(
                H2OGPTEAsync.MAX_WAIT_INTERVAL, dt * H2OGPTEAsync.WAIT_BACKOFF_FACTOR
            )
        return job

    def _raise_error_if_any(self, res: httpx.Response) -> None:
        if res.status_code == 200:
            return
        error: ErrorResponse
        try:
            error = res.json()
        except:
            error = {"error": res.content.decode(errors="replace")}

        self._http_code_to_error(res.status_code, error)

    @staticmethod
    def _http_code_to_error(http_code, error) -> None:
        if http_code == 200:
            return
        if http_code == 400:
            raise InvalidArgumentError(error)
        elif http_code == 401:
            raise UnauthorizedError(error)
        elif http_code == 404:
            raise ObjectNotFoundError(error)
        elif http_code == 500:
            raise InternalServerError(error)
        else:
            raise HTTPError(error, http_code)


def _to_id(data: Any) -> str:
    return Identifier(**data).id
