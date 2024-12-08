# ReLing: Command-line Tool for Learning Foreign Languages

ReLing allows you to learn or enhance your knowledge of any [major world language](#languages) supported by [GPT models](https://platform.openai.com/docs/models). To use this tool, you must have a paid [OpenAI account](https://platform.openai.com/) with an [API key created](https://platform.openai.com/api-keys).

The program operates as follows:

- [Select a GPT model](#setting-models-and-api-key) to generate a [text](#generating-texts) or [dialogue](#generating-dialogues) on a chosen or random topic.
- View or translate the generated content into any [supported language](#languages).
- Take an  [exam](#taking-exams) to translate the text from one language to another and receive:
  - A score for each sentence on a 10-point scale;
  - Suggestions for improving your translations;
  - The program’s own translation of the sentence.

You can retake exams at your preferred frequency until you achieve perfect scores.

ReLing also enables you to view a [list](#listing-content) of all generated texts and dialogues and their associated [exam histories](#exam-history).

Optionally, the system can vocalize sentences in both the source and target languages and accept your responses via voice or image capture.


## Table of Contents<a id="table-of-contents"></a>

- [Installation](#installation)
- [Generating Texts](#generating-texts)
- [Generating Dialogues](#generating-dialogues)
- [Displaying Content](#displaying-content)
- [Taking Exams](#taking-exams)
- [Exam History](#exam-history)
- [Learning Statistics](#learning-statistics)
- [Listing Content](#listing-content)
- [Archiving Content](#archiving-content)
- [Unarchiving Content](#unarchiving-content)
- [Renaming Content](#renaming-content)
- [Deleting Content](#deleting-content)
- [Exporting Data](#exporting-data)
- [Automatic Content ID](#automatic-content-id)
- [Languages](#languages)
- [Setting Models and API Key](#setting-models-and-api-key)
- [Specifying Genders](#specifying-genders)


## Installation<a id="installation"></a>

Install [Python](https://www.python.org/downloads/) 3.12 or higher and [pipx](https://pipx.pypa.io/stable/installation/), then proceed based on your audio, image, and grammar preferences:

### Without Audio, Image, or Grammar Support

```bash
pipx install reling
```

### With Audio Support

On macOS, first install [Homebrew](https://brew.sh/), then:

```bash
brew install portaudio
```

On Ubuntu, run:

```bash
sudo apt install python3-pyaudio
```

Install the tool with the `audio` extra:

```bash
pipx install "reling[audio]"
```

### With Image Support

If you want to use the [image scanning feature](#taking-exams), install the tool with the `image` extra:

```bash
pipx install "reling[image]"
```

### With Grammar Support

If you want to track grammar-related [learning statistics](#learning-statistics), install the tool with the `grammar` extra:

```bash
pipx install "reling[grammar]"
```

### With Audio, Image, and Grammar Support

Follow the instructions above to install the necessary dependencies, then run the following command:

```bash
pipx install "reling[audio,image,grammar]"
```

### Finalizing Setup

You may need to restart your terminal for the `reling` command to be recognized.

Additionally, to enable command-line completions, execute:

```bash
reling --install-completion
```

For Mac users, you may also need to append `compinit -D` to the end of your `~/.zshrc` file.

### Updating the Tool

To update ReLing to its latest version, run:

```bash
pipx upgrade reling
```

### Uninstalling the Tool

To remove ReLing from your system, execute:

```bash
pipx uninstall reling
```

This will uninstall the tool but will **not** delete your [data storage file](#exporting-data). If you wish to delete this file as well, you must remove it manually.


## Generating Texts<a id="generating-texts"></a>
`reling create text`

The command format is:

```bash
reling create text en [--level basic] [--topic food] [--style news] [--size 5] [--include "cook: a person"] [--model <GPT-MODEL>] [--api-key <OPENAI-KEY>]
```

### Language

Specify a [supported language](#languages) as the only positional argument. The text will be in that language but can be translated later.

### `level`

Choose from three complexity levels:

- `basic`;
- `intermediate` (default);
- `advanced`.

### `topic`

You may select a topic for the text. If unspecified, a random topic from [500 predefined options](src/reling/data/topics.csv) will be chosen.

### `style`

You may also choose a style for the text. If unspecified, a random style from [50 predefined options](src/reling/data/styles.csv) will be chosen.

### `size`

This sets the number of sentences in the text. By default, 10 sentences are generated.

### `include`

This parameter allows you to ensure the inclusion of specific vocabulary in the text. You can specify a simple word (`--include cook`), a word with a specific meaning (`--include "cook: a person"`), or several words or phrases (`--include "cook: a person" --include soup --include "mac and cheese"`).

### `model` & `api-key`

Refer to [Setting Models and API Key](#setting-models-and-api-key).


## Generating Dialogues<a id="generating-dialogues"></a>
`reling create dialogue`

The command format is:

```bash
reling create dialogue en [--level advanced] [--speaker waiter] [--topic food] [--size 5] [--include "cook: a person"] [--speaker-gender male] [--user-gender female] [--model <GPT-MODEL>] [--api-key <OPENAI-KEY>]
```

### Language

Specify a [supported language](#languages) as the only positional argument. The dialogue will be generated in this language and can be translated later.

### `level`

Choose from three complexity levels:

- `basic`;
- `intermediate` (default);
- `advanced`.

### `speaker`

Specify an interlocutor or let the system choose randomly from [200 predefined options](src/reling/data/speakers.csv).

### `topic`

Choose a topic for the dialogue or let it be automatically determined.

### `size`

This parameter sets the number of sentence pairs in the dialogue. The default is 10.

### `include`

This parameter allows you to ensure the inclusion of specific vocabulary in the dialogue. You can specify a simple word (`--include cook`), a word with a specific meaning (`--include "cook: a person"`), or several words or phrases (`--include "cook: a person" --include soup --include "mac and cheese"`).

### `speaker-gender` & `user-gender`

Refer to [Specifying Genders](#specifying-genders).

If the interlocutor’s gender is not specified, it will be randomly chosen as either `male` or `female`.

### `model` & `api-key`

Refer to [Setting Models and API Key](#setting-models-and-api-key).


## Displaying Content<a id="displaying-content"></a>
`reling show`

View or listen to a text or dialogue with:

```bash
reling show <CONTENT-ID> [en] [--read] [--model <GPT-MODEL>] [--tts-model <TTS-MODEL>] [--api-key <OPENAI-KEY>]
```

### Content ID

Specify the identifier of the content to view. This ID is provided when content is created and [listed](#listing-content).

### Language

Optionally, specify a language to view the content in that language, translating if necessary.

### `read`

If enabled, the content will be read aloud. You can stop the reading at any time by pressing `Ctrl + C`.

### `model`, `tts-model` & `api-key`

Refer to [Setting Models and API Key](#setting-models-and-api-key).


## Taking Exams<a id="taking-exams"></a>
`reling exam`

To translate a text or dialogue and receive feedback, run:

```bash
reling exam <CONTENT-ID> [--from en] [--to fr] [--read fr] [--listen] [--scan 0] [--hide-prompts] [--offline-scoring] [--model <GPT-MODEL>] [--tts-model <TTS-MODEL>] [--asr-model <ASR-MODEL>] [--api-key <OPENAI-KEY>]
```

While inputting your answers during an exam, you can press `Ctrl + C` to pause. This affects the calculation of exam duration and, consequently, your [learning statistics](#learning-statistics).

### Content ID

Specify the content identifier for the exam. This ID is provided when content is created and [listed](#listing-content). You may also [use a dot](#automatic-content-id) (`.`) to refer to the last text or dialogue you interacted with or just created.

### `from` & `to`

Specify the languages from which and to which you would like to translate the text or dialogue. If one of the languages is not specified, the original language of the selected text or dialogue will be used.

### `read`

Optionally, you can specify one or both of the selected source and target languages to have the text read aloud. For example, use `--read en --read fr` to hear the content in English and French. You can stop the reading at any time by pressing `Ctrl + C`.

### `listen`

When this flag is enabled, ReLing will accept your responses via voice. You also have the option to switch to manual input mode if needed.

### `scan`

Use this parameter to have ReLing accept your response by capturing an image with one of the available cameras. The value of the parameter is the index of the camera to use. For example, camera 0 might be your laptop’s built-in camera, while camera 1 could be an external webcam or a connected smartphone.

You also have the option to switch to manual input mode if needed.

### `hide-prompts`

This flag allows you to hide the original language text as well as the interlocutor’s turn (if in a dialogue). It can help train recall or listening skills (when the `listen` flag is enabled).

### `offline-scoring`

Use this flag to score answers based on an offline algorithm instead of the OpenAI API.

### `model`, `tts-model`, `asr-model` & `api-key`

Refer to [Setting Models and API Key](#setting-models-and-api-key).


## Exam History<a id="exam-history"></a>
`reling history`

To view your exam history, use the command:

```bash
reling history <CONTENT-ID> [--from en] [--to fr]
```

### Content ID

Specify the identifier of the text or dialogue whose exam history you wish to review.

### `from` & `to`

Limit the display of exam results to translations between specified source and target languages.


## Learning Statistics<a id="learning-statistics"></a>
`reling stats`

The `stats` command provides detailed statistics about your learning progress in specific languages. The command format is:

```bash
reling stats en [--pair fr] [--grammar] [--comprehension] [--production] [--checkpoint 2024-12-01] [--checkpoint "2025-01-01, 15:00"]
```

### Language

Specify a [supported language](#languages) as the only positional argument. The statistics will be shown for this language.

### `pair`

Optionally, specify one or more languages such that the statistics will be displayed for translations between the main language and these languages only.

If you need to specify more than one language, use the `--pair` flag multiple times: `--pair fr --pair es`.

### `grammar`

Use this flag to view statistics on learned word forms and lemmas, classified by part of speech. If this flag is not used, general statistics, such as total time spent in exams, will be displayed. Note that to use this flag, you must [install](#installation) the tool with the `grammar` extra.

### `comprehension` & `production`

You can request statistics related to either comprehension or production, or both. By default, both are displayed unless one is specifically requested.

### `checkpoint`

Optionally, provide one or more date checkpoints (in `YYYY-MM-DD` or `YYYY-MM-DD, HH:MM` format) to see progress since those points in time.


## Listing Content<a id="listing-content"></a>
`reling list`

To view a list of all generated texts and dialogues, execute:

```bash
reling list [--category dialogue] [--level intermediate] [--language en] [--search <REGEX>] [--archive] [--ids-only]
```

### `category`

Choose to display either `text`s or `dialogue`s.

### `level`

Filter content by complexity level: `basic`, `intermediate`, or `advanced`.

### `language`

Display content generated in a specific language.

### `search`

Use a regular expression to search content IDs, text, topics, styles, or interlocutors.

### `archive`

Toggle to view content from the [archive](#archiving-content).

### `ids-only`

Display only the identifiers of texts and dialogues without full details.


## Archiving Content<a id="archiving-content"></a>
`reling archive`

To archive texts and dialogues:

```bash
reling archive <CONTENT-ID>
```

### Content ID

Provide the identifier of the content you wish to archive.


## Unarchiving Content<a id="unarchiving-content"></a>
`reling unarchive`

To restore archived content to the main list:

```bash
reling unarchive <CONTENT-ID>
```

### Content ID

Specify the identifier of the content to be restored from the archive.


## Renaming Content<a id="renaming-content"></a>
`reling rename`

To rename a specific text or dialogue:

```bash
reling rename <CONTENT-ID> <NEW-ID>
```

### Content ID

Enter the identifier of the content you want to rename.

### New ID

Provide the new identifier for the content.


## Deleting Content<a id="deleting-content"></a>
`reling delete`

To remove texts or dialogues permanently:

```bash
reling delete <CONTENT-ID> [--force]
```

### Content ID

Specify the identifier of the content you intend to delete.

### `force`

Enable immediate deletion without confirmation.


## Exporting Data<a id="exporting-data"></a>
`reling db`

To access the data storage file for transferring or backing up content and exam results:

```bash
reling db
```


## Automatic Content ID<a id="automatic-content-id"></a>

If a dot (`.`) is provided in place of a content ID in any command, the system will assume that you are referring to the last text or dialogue you interacted with.


## Languages<a id="languages"></a>

ReLing supports over **180 major languages** [sourced from Wikipedia](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) under the [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/deed.en).

To specify a language in a command argument, you can either write its full name (e.g., `English` or `english`) or use the 2-character or 3-character code for that language (e.g., `en` or `eng` for English).

For languages written in multiple scripts, the system does not currently support specifying a particular script in the commands. The script used will depend on GPT’s output and may vary. Additionally, for right-to-left scripts such as Arabic or Hebrew, punctuation is likely to display incorrectly. If you plan to use the tool with these languages, feel free to request a fix or contribute a solution.


## Setting Models and API Key<a id="setting-models-and-api-key"></a>

To avoid specifying [model names](https://platform.openai.com/docs/models) and entering the [API key](https://platform.openai.com/api-keys) separately for each command, you can set the following environment variables:

- `RELING_API_KEY`: a pre-generated API key for OpenAI’s web API.
- `RELING_MODEL`: the name of the GPT model used for generating text, taking exams, and scanning images (e.g., `gpt-4o`).
- `RELING_TTS_MODEL`: the name of the text-to-speech (TTS) model (e.g., `tts-1`). Since current OpenAI TTS models primarily focus on English and may not perform well in other languages, you can use the additional model `_gtts` (Google Text-to-Speech) for better voice output in other languages (note the leading underscore).
- `RELING_ASR_MODEL`: the name of the automatic speech recognition (ASR) model for voice response recognition (e.g., `whisper-1`).

Parameter values specified in individual commands will take precedence over these environment variables.

If a model or key is not specified in either the command or the environment variable, the program will prompt you to enter it directly.


## Specifying Genders<a id="specifying-genders"></a>

The system requires knowledge of your gender and the gender of your interlocutor to accurately generate dialogues in languages with grammatical gender and to provide voice outputs with appropriate voices.

To avoid specifying your gender each time you generate a new dialogue, you can set the environment variable `RELING_USER_GENDER`.

The system accepts one of the following values for gender: `male`, `female`, or `nonbinary`.