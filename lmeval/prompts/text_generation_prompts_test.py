from lmeval.prompts.text_generation_prompts import QuestionOnlyPrompt

def test_custom_prompt():
    name = "mycustom prompt"
    template = "this is a custom prompt - question: {{question}} -  answer: {{answer}}"
    prompt = QuestionOnlyPrompt(name=name, template=template)
    assert prompt.name == name
    assert prompt.template == template
