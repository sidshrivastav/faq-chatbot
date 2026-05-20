# Task Log

- T032: Wrote failing service tests for retrieval and mocked LLM boundaries, then implemented the chat service stack; verified with focused tests plus full backend/frontend suites.
- T033: Wrote failing chat API tests covering answered, unsupported, no-active-source, inactive-source exclusion, and auth failure cases; verified through the backend chat suite.
- T034: Wrote failing frontend chat state tests; verified through the frontend chat suite.
- T035: Added chat request/response schemas; verified through the backend chat suite.
- T036: Added deterministic retrieval scoring and active-source filtering; verified through the backend chat suite.
- T037: Added the LLM provider boundary, prompt builder, and fake provider; verified through the backend chat suite.
- T038: Added answer orchestration for answered, unsupported, no-active-source, and error states; verified through the backend chat suite.
- T039: Added chat API routing and in-memory persistence; verified through the backend chat suite.
- T040: Added the static Chat screen with grounded/unsupported/no-active-source states; verified through the frontend chat suite.
- T041: Added chat and use-case frontend service adapters; verified through the frontend service suite and full frontend build.
