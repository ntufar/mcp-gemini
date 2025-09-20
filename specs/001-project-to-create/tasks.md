# Tasks: MCP Server for Local File Browsing

**Input**: Design documents from `/specs/001-project-to-create/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [ ] T001 Create project structure (src/, tests/)
- [ ] T002 Initialize Python project with FastAPI and Uvicorn
- [ ] T003 [P] Configure linting (e.g., Black, Flake8) and formatting (e.g., Black) tools

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T004 [P] Contract test for `fs.listDirectory` (tests/contract/test_list_directory.py)
- [ ] T005 [P] Contract test for `fs.readFile` (tests/contract/test_read_file.py)
- [ ] T006 [P] Integration test for sandboxing (tests/integration/test_sandboxing.py)
- [ ] T007 [P] Integration test for non-existent paths (tests/integration/test_error_handling.py)
- [ ] T008 [P] Integration test for file size limit (tests/integration/test_file_size.py)
- [ ] T009 [P] Integration test for binary file handling (tests/integration/test_binary_files.py)
- [ ] T010 [P] Integration test for MCP compliance (tests/integration/test_mcp_compliance.py)

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T011 [P] Implement directory listing logic (src/services/file_browser.py)
- [ ] T012 [P] Implement file reading logic (src/services/file_browser.py)
- [ ] T013 Implement FastAPI application setup (src/main.py)
- [ ] T014 Implement `fs.listDirectory` endpoint (src/main.py)
- [ ] T015 Implement `fs.readFile` endpoint (src/main.py)
- [ ] T016 Implement sandboxing mechanism (src/utils/security.py)
- [ ] T017 Implement error handling for non-existent paths (src/main.py)
- [ ] T018 Implement file size limit check (src/services/file_browser.py)
- [ ] T019 Implement binary file delivery (src/services/file_browser.py)
- [ ] T020 Implement MCP compliance logic (src/services/mcp_compliance.py)

## Phase 3.4: Integration
- [ ] T021 Configure structured logging (src/utils/logger.py)
- [ ] T022 Integrate logging into API endpoints (src/main.py)

## Phase 3.5: Polish
- [ ] T023 [P] Unit tests for file_browser.py (tests/unit/test_file_browser.py)
- [ ] T024 [P] Unit tests for security.py (tests/unit/test_security.py)
- [ ] T025 [P] Update API documentation (docs/api.md)
- [ ] T026 Performance tests for API endpoints
- [ ] T027 Review and refactor code for maintainability

## Dependencies
- Tests (T004-T010) before implementation (T011-T020)
- T011, T012, T016, T018, T019, T020 block T014, T015, T017
- T021 blocks T022
- Implementation before polish (T023-T027)

## Parallel Example
```
# Launch T004-T010 together:
Task: "Contract test for `fs.listDirectory` (tests/contract/test_list_directory.py)"
Task: "Contract test for `fs.readFile` (tests/contract/test_read_file.py)"
Task: "Integration test for sandboxing (tests/integration/test_sandboxing.py)"
Task: "Integration test for non-existent paths (tests/integration/test_error_handling.py)"
Task: "Integration test for file size limit (tests/integration/test_file_size.py)"
Task: "Integration test for binary file handling (tests/integration/test_binary_files.py)"
Task: "Integration test for MCP compliance (tests/integration/test_mcp_compliance.py)"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**: (Not applicable yet, contracts/ directory is empty)
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**: (Not applicable yet, data-model.md is empty)
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**: (Covered by integration tests)
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks
- [ ] All tests come before implementation
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task