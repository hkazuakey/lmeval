from enum import Enum

class StepType(Enum):
  lmgeneration = "lmgeneration"
  lmrating = "lmrating"
  retrieval = "retrieval"
  ranking = "ranking"
  scoring = "scoring"

# [Benchmark]

class Modality(Enum):
  auto = "auto"  # used for auto detection in question media add
  text = "text"
  image = "image"
  code = "code"
  audio = "audio"
  video = "video"
  document = "document"
  multimodal = "multimodal"   # used for scorers that can handle multiple modalities

class BenchmarkLicence(Enum):
  cc_40_by = "cc-40-by"
  cc_40_by_nc = "cc-40-by-nc"


# [Scorers]
class Regex(Enum):
  "common regex patterns"
  boolean_answer = r'answer: +(.{2,3})'
  multi_choice = r'answer: +(.)'


class ScorerType(Enum):
  # dummy scorers
  always_0 = "always_0"
  always_1 = "always_1"

  # boolean scorers
  boolean_answer = "boolean_answer"

  # mutiple choices scorers that look at the letter
  contains_answer_letter_insensitive = "contains_answer_letter_insensitive"

  # simple text matching scorers
  text_exact_sensitive = "text_exact_sensitive"
  text_exact_insensitive = "text_exact_insensitive"

  # text containt scorers
  contain_text_sensitive = "contain_text_sensitive"
  contain_text_insensitive = "contain_text_insensitive"

  # regex text matching scorers
  text_regex_sensitive = "text_regex_sensitive"
  text_regex_insensitive = "text_regex_insensitive"

  # llm based scorers
  punt_detector = "punt_detector"
  llm_rater = "llm_rater"

  # NLP scorers
  rouge = "rouge"
  blue = "blue"
  meteor = "meteor"
  mauve = "mauve"



# [question]
class FileType(Enum):
    auto = "auto"
    jpeg = "jepg"
    jpg = "jpeg"  # we need this to pass the right filetype to models
    png = "png"
    gif = "gif"
    mp4 = "mp4"
    mp3 = "mp3"
    wav = "wav"
    txt = "txt"
    python = "py"
    pdf = "pdf"
    html = "html"
    json = "json"


# [Tasks]
class TaskType(Enum):
  boolean = "boolean"
  multiple_choices = "multiple_choices"
  text_generation = "text_generation"
  image_generation = "image_generation"
  python_generation = "python_generation"

  red_text_generation = "red_text_generation"


class TaskLevel(Enum):
  basic = "basic"
  intermediate = "intermediate"
  advanced = "advanced"


class MultiShotStrategy(Enum):
  single = "single"  # no multi-shot scoring
  average = "average"   # take average score
  max = "max" # take the max score
  majority = "majority"  # take the majority score