from ._main import ai

def streamai(messages_or_prompt,*args, **kwargs):
    for x in ai(messages_or_prompt=messages_or_prompt,
                stream=True,*args, **kwargs):
        print(x.choices[0].delta.content,end = "",flush=True)

def yieldai(messages_or_prompt,*args, **kwargs):
    for x in ai(messages_or_prompt=messages_or_prompt,
                stream=True,*args, **kwargs):
        yield x.choices[0].delta.content
