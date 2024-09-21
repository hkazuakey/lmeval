from collections import defaultdict
from datetime import datetime
from typing import List

from lmeval import utils
from lmeval.archive import LMDBArchive
from lmeval.custom_model import CustomModel
from lmeval.enums import ScorerType, Modality, TaskLevel
from lmeval.logger import log
from lmeval.prompts import Prompt
from lmeval.scorers import get_scorer
from lmeval.scorers import Scorer
from lmeval.task import Task
import pandas as pd
from pydantic import Field
from tabulate import tabulate
from tqdm.auto import tqdm


BENCHMARK_FNAME = "benchmark.json"
METADATA_FNAME = "metadata.json"
STATS_FNAME = "stats.json"

# [Categories]
class Category(CustomModel):
    name: str
    description: str = Field(default="")
    instruction: str = Field(default="")
    tasks: List[Task] = Field(default_factory=list)

    def __str__(self) -> str:
        return str(self.name)


# [Benchmark]
class Benchmark(CustomModel):
    name: str
    category: str = Field(default="")
    description: str = Field(default="")
    url: str = Field(default="")
    authors: list[str] = Field(default_factory=list)
    version: str = Field(default="")
    license: str = Field(default="")
    contact: str = Field(default="")
    last_update: str = Field(default="")  # tracking changes
    punt_scorer: Scorer | None = Field(default=None)
    prompts: List[Prompt] = Field(default_factory=list)
    categories: List[Category] = Field(default_factory=list)

    def __str__(self) -> str:
        return str(self.name)

    def to_dataframe(self) -> pd.DataFrame:
        "Return benchmark results as a pandas dataframe"
        records = []
        for category in self.categories:
            for task in category.tasks:
                for qid, question in enumerate(task.questions):
                    for prompt_version, data in question.lm_answers.items():
                        for model_version, resp in data.items():
                            records.append({
                                "qid": qid,
                                "category": category.name,
                                "task": task.name,
                                "task_type": task.type,
                                "prompt": prompt_version,
                                "model": model_version,
                                "score": resp.score,
                                "punting": int(resp.ispunting)
                            })
        return pd.DataFrame(records)

    def save(self, path: str, debug: bool = False, archive = None, use_tempfile: bool | None = None):
        "save the benchmark to a file path"

        # FIXME: perform benchmark checks with validate()
        # add it to the evaluator() as well
        # call check in the eval as well.
        # check category names are unique
        # check category have tasks
        # check task names are unique
        # check tasks have questions
        # check question ids are unique
        # check prompt are unique
        # check model versions are unique
        # check prompt versions are unique

        if use_tempfile is None:
            use_tempfile = utils.is_google()
        # use default serializer if needed
        if not archive:
            archive = LMDBArchive(path, use_tempfile=use_tempfile, restore=False)

        # only perform fname check for ondisk
        if isinstance(archive, LMDBArchive):
            if not path.endswith(".lmarxiv"):
                raise ValueError("Path should end with .lmarxiv")

            # create path if it doesn't exist
            utils.Path(path).parent.mkdir(parents=True, exist_ok=True)

        # update last update time
        self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")

        # load media content into memory
        # we do in two steps to show progress bar
        to_load = []
        for category in self.categories:
            for task in category.tasks:
                for question in task.questions:
                    for media in question.medias:
                        to_load.append(media)
        if to_load:
            for media in tqdm(to_load, desc="Saving medias content in benchmark archive"):
                fname = f"media/{media.filename}"

                # already stored -- we dedup accross questions
                if media.is_stored:
                    assert fname in archive.list_files(), f"media {fname} not found in archive but marked as stored"
                    continue

                if not utils.Path(media.original_path).exists():
                    raise ValueError(f"media {media.original_path} not found")

                # load and save content in the arxiv
                content = utils.Path(media.original_path).read_bytes()
                archive.write(fname, content, encrypted=True)

                # remove potential PII and mark as stored
                media.original_path = ""
                media.is_stored = True

        # metadata
        metadata = {"name": self.name,
                    "version": self.version,
                    "description": self.description,
                    "authors": self.authors,
                    "license": self.license,
                    "contact": self.contact,
                    "last_update": self.last_update,
                    "storage_format": archive.version_string(),
                    "url": self.url}
        archive.write_json(METADATA_FNAME, metadata, encrypted=False)

        #stats
        archive.write_json(STATS_FNAME, self.get_stats(), encrypted=False)

        # serialize the benchmark data
        archive.write(BENCHMARK_FNAME, self.model_dump_json().encode(), encrypted=True)


        if debug:
            print(f"Saved benchmark to {path}")

    def get_category(self, category_name: str) -> Category:
        """Get a category by name

        Args:
            category_name: Category name

        Raises:
            ValueError: Category not found

        Returns:
            Category: The category
        """
        for category in self.categories:
            if category.name == category_name:
                return category
        raise ValueError(f"Category {category_name} not found")

    def get_task(self, category_name: str, task_name: str) -> Task:
        """Get a task group by path: category_name/task_group_name

        Args:
            category_name: Category name
            task_name: Task group name

        Raises:
            ValueError: Task group not found

        Returns:
            TaskGroup: The task group
        """

        category = self.get_category(category_name)
        for task in category.tasks:
            if task.name == task_name:
                return task
        task_names = [task.name for task in category.tasks]
        raise ValueError(f"Task {task_name} not found - available tasks: {task_names}")


    def get_stats(self):
        models_stats = {}
        categories_stats = {}
        task_stats = defaultdict(dict)
        prompt_stats = {}
        num_answers = 0
        num_questions = 0

        for category in self.categories:
            num_questions_per_category = sum([len(task.questions) for task in category.tasks])
            num_questions += num_questions_per_category
            cat_answers = 0
            cat_models = set()
            category_cnts = defaultdict(int)

            for task in category.tasks:
                # task levels
                task_stats[category.name][task.name] = {
                    "type": task.type,
                    "modality": task.modality.value,
                    'level': task.level.value,
                    "questions": len(task.questions),
                    "images": 0,
                    "audio": 0,
                    "video": 0,
                    "models": 0,
                    "answers": 0,
                    "prompts": 0,
                    "punts": 0,
                }

                for question in task.questions:
                    for media in question.medias:
                        if media.modality == Modality.image:
                            task_stats[category.name][task.name]['images'] += 1
                            print('yep')
                            category_cnts['images'] += 1
                        elif media.modality == Modality.audio:
                            task_stats[category.name][task.name]['audio'] += 1
                            category_cnts['audio'] += 1
                        elif media.modality == Modality.video:
                            category_cnts['video'] += 1
                            task_stats[category.name][task.name]['video'] += 1

                    for prompt_version, data in question.lm_answers.items():
                        cat_answers += len(data)
                        cat_models.add(prompt_version)
                        task_stats[category.name][task.name]['prompts'] += 1

                        if prompt_version not in prompt_stats:
                            prompt_stats[prompt_version] = {
                                "answers": 0,
                                "score": 0,
                                "punts": 0,
                                "models": len(data),
                            }

                        task_stats[category.name][task.name]['models'] += len(data)


                        for model_version, resp in data.items():
                            prompt_stats[prompt_version]['answers'] += 1
                            prompt_stats[prompt_version]['score'] += resp.score
                            prompt_stats[prompt_version]['punts'] += resp.ispunting

                            if model_version not in models_stats:
                                models_stats[model_version] = {
                                    "answers": 0,
                                    "score": 0,
                                    "punts": 0,
                                }

                            models_stats[model_version]['answers'] += 1
                            models_stats[model_version]['score'] += resp.score
                            models_stats[model_version]['punts'] += resp.ispunting
                            category_cnts['punts'] += resp.ispunting


                            task_stats[category.name][task.name]['answers'] += 1
                            task_stats[category.name][task.name]['punts'] += resp.ispunting



            categories_stats[category.name] = {
                                               "tasks": len(category.tasks),
                                               "prompts": len(prompt_stats),
                                               "questions": num_questions_per_category,
                                               "answers": cat_answers,
                                               "models": len(cat_models),
                                               "punts": category_cnts['punts'],
                                               'images': category_cnts['images'],
                                               'audio': category_cnts['audio'],
                                               'video': category_cnts['video'],
                                            }
            num_answers += cat_answers

        return {
            "questions": num_questions,
            "answers": num_answers,
            "prompts": prompt_stats,
            "categories_stats": categories_stats,
            "tasks_stats": task_stats,
            "models_stats": models_stats
        }

    def summary(self):
        stats = self.get_stats()
        print(f"-={self.name} ({self.last_update})=-")
        print(f"{self.description}")
        print(f"|-Authors: {', '.join(self.authors)} ({self.contact})")
        print(f"|-Version: {self.version} - License: {self.license}")
        print(f"|-URL: {self.url}")
        print(f"|-Questions: {stats['questions']}")
        print(f"|-Answers: {stats['answers']}")

        print("\n[Questions Stats]")
        rows = []
        for cat_name, tdata in stats['tasks_stats'].items():
            if len(rows):
                rows.append(["", "", "", "", "", "", "", ""])

            k = f"{cat_name}"
            rows.append([k, '', '',
                         stats['categories_stats'][cat_name]['questions'],
                          '', '', '',
                         stats['categories_stats'][cat_name]['prompts'],
                         stats['categories_stats'][cat_name]['models'],
                         stats['categories_stats'][cat_name]['answers'],
                         stats['categories_stats'][cat_name]['punts']])

            for task_name, c in tdata.items():
                k = f"|- {task_name}"
                rows.append([k,
                             c['type'],
                             c['level'],
                             c['questions'],
                             c['images'],
                             c['audio'],
                             c['video'],
                             c['prompts'],
                             c['models'],
                             c['answers'],
                             c['punts']])
        print(tabulate(rows, headers=["", "Type", "Level", "Questions", "Images", "Audios", "Videos", "Prompts", "Models", "Answers", "Punts"]))


        if stats['answers']:
            print("\n[Answers Stats]")
            rows = [[k, v['answers'], v['score']/v['answers'], v['punts']] for k, v in stats['models_stats'].items()]
            print(tabulate(rows, headers=["Model", "Num Answers", "Avg Score", "Num Punts"]))


def load_benchmark(path: str, archive = None, use_tempfile: bool | None = None) -> Benchmark:
    "Reload a benchmark from a file path"
    # use default serializer if needed
    if not archive:
        archive = LMDBArchive(path, use_tempfile=use_tempfile, restore=True)


    # reload benchmark data
    benchmark = Benchmark.model_validate(archive.read_json(BENCHMARK_FNAME))

    # reload scorers as their compute function are not serializable
    media_to_load = []
    for category in benchmark.categories:
        for task in category.tasks:
            scorer_name = str(task.scorer.type)
            stype = ScorerType[scorer_name]
            task.scorer = get_scorer(stype)

            # pydantic have hard time serializing enums
            task.modality = Modality[str(task.modality)]
            task.level = TaskLevel[str(task.level)]
            for question in task.questions:
                for media in question.medias:
                    media_to_load.append(media)

    # loading media content
    for media in tqdm(media_to_load, desc="Loading medias content from benchmark archive"):
        fname = f"media/{media.filename}"
        media.content = archive.read(fname)
        media.is_stored = True


    return benchmark


def list_benchmarks(dir_name: str, archive = None, use_tempfile: bool | None = None) -> List[str]:
    "List all benchmarks"
    benchmark_paths = utils.match_files(dir_name, ".*[.]lmarxiv$")
    rows = []
    for idx, path in enumerate(benchmark_paths):
        parent = utils.Path(path).parent.name
        # use default serializer if needed
        if not archive:
            archive = LMDBArchive(path, use_tempfile=use_tempfile)
        files = archive.list_files()
        if METADATA_FNAME in files:
            metadata = archive.read_json(METADATA_FNAME)
            name = metadata['name']
            version = metadata['version']
        else:
            name = version = "n/a"

        if STATS_FNAME in files:
            stats = archive.read_json(STATS_FNAME)
            categories = len(stats['categories_stats'])
            questions = stats['questions']
            models = len(stats['models_stats'])
            answers = stats['answers']
        else:
            models = categories = questions = answers = 'n/a'

        rows.append([idx, name, version, parent, categories, questions, models, answers, path])

    print(tabulate(rows,  headers=['idx', "name", "version", 'parent_dir', 'categories', 'questions',
                                  'evaled models',  'model answers', 'path']))
    return benchmark_paths