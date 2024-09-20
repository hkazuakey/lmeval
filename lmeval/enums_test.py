from lmeval.enums import ScorerType, TaskType, TaskLevel, FileType


def test_scorer_type_consistency():
    for s in ScorerType:
        print(str(s.name) + ' ' + str(s.value))
        assert str(s.name) == str(s.value)

def test_task_type_consistency():
    for s in TaskType:
        print(str(s.name) + ' ' + str(s.value))
        assert str(s.name) == str(s.value)

def test_task_level_consistency():
    for s in TaskLevel:
        print(str(s.name) + ' ' + str(s.value))
        assert str(s.name) == str(s.value)
