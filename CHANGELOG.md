# Changelog
## [0.8.0] - 2024-10-03

### Added
 - Added `Task()` subclasses such as`TextGenerationTask()`, `YesNoTask()`
 to make benchmark creation easier by simplifying the common cases.
- Added `Category` `.add_task()` / `delete_task()` / `get_task()` to simplify the benchmark creation
- Added `Task` `.add_question()` / `.delete_question()` / `get_question()`

### Changed
- Improved the `quick_receipts` notebook
- Storage system now use `sqlite` for increased compatibility and performance.

### Fixed
- Serialization where images were uncessarily compressed
- Multiples smalls bugs


## [0.7.0] - 2024-09-20

### Changed
- File format to support multi-shot and multi-step execution
- Moved from poetry to uv
- Improved pandas data export to include tokens / cost and time tracking

### Removed
- Uselss dependencies now that we rely on litellm for many of the models.

### Fixed

- Serialization bugs
- hello world colab


## [0.6.0] - 2024-09-13

### Added

- Tokens and cost count per response.
- response Timestamp
- Vertex Support including anthropic and mistral models
- Ollama support
- support Gemini safe and unsafe version (filter disabled)
- Batch API
- OpenAI model support
- Image support including storing deduped media and reloading from arxiv.
- Benchmark files manifest
- Cookbooks with some receipts on how to use the system.

### Changed

- Model API now use LLMLite under the hood for added stability and extra-features
- Replaced zip archive format with LMDB to support file replacements and improve speed.
- Refactored storage code to use an `Archive()` object that allows to store to other format / places.
- Simplified Gemini() API to auto fetch the key if not provided.

### Fixed
- Fixed the get_task() api so it doesn't rely on special caracters
- Increased test coverage.



## [0.5.1] - 2024-07-12

### Added

- Added utility to decompress benchmark on disk to help debugging.

### Changed

- Multiple choices answers order and letters assignement executed only at first rendering.


## [0.5.0] - 2024-07-11

### Added
- Support for custom prompts
- Detect when the real answer is incorrectly in alternative choices for multi-choice evaluation.

### Changed
- Fixed typo so it is now correctly `Evaluator.generate_answer()`

### Fixed
- Planning report output
- `etask.score`, `etask.puting` and `etask.error` are now working
- Gemini unit tests

## [0.4.1] - 2024-07-01

### Added
#### Evaluator v2
- Intial version of the new evaluator which support:
  - Plannification
  - Multi-prompts
  - Prompt typing : ensure prompts only apply to specific questions type e.g boolean prompt to boolean question

#### Prompts
- Added `TrueOrFalseAnswerPrompt()` boolean scorer
- Added `MultiChoicesPrompt()` multi_choices scorer

#### Scorers
- Added `TextContain` scorer
- Added `BooleanQuestionScorer` that is robust to various way model say yes or no and how people specificy boolean questions.
- Added `TextContainInsensitive` scorer which is more robust and easier choice for multi choices questions.

#### Metadata
- Last update
- Author list instead of single cretor

#### Engine
- Conditonal support for `orjson` to speedup serialization - default to `json` if not found.
- metadata and summary files compression with DEFLATE instead of no compression before.

#### notebooks
- Harry potter dataset with dataset creation and dataset evaluation notebooks

#### testing
- More tests
- End to end testing


#### Changed
- Replaced the evaluator with a far more extensive one that support advance plannibg
- Metadata format so they are clearer
- Refactored prompts for better text cleanup and better naming convention.
- Simplified questions and tasks
- Refactored a lot of fields
- Gemini use by default 1.5 flash instead of requiring to explictly pass a version. Simplify the tests


## [0.3.0] - 2024-06-24

### Added
- Benchmark compression: now compress the benchmark prior to compression

### Changed
- Moved crypto to use `tink` instead of `cryptography`


## [0.0.2] - 2024-06-21

### Added
- Multi-prompts evaluation support
- Added `Prompt()` meta-class to allow the re-use of prompts and support versioning
- Added Ollama models support

### Changed
- Benchmark format to support multi-prompt
- Summary to report prompts
- Removed auto import to allow ondemand model API support




Using: https://keepachangelog.com/en/1.1.0/