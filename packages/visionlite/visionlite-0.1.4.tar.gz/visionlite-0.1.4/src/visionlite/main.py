from parselite import parse
from searchlite import google, bing
from wordllama import WordLlama

llm = WordLlama.load()


def vision(query,k=1,max_urls=5,animation=False):
    try:
        res = llm.topk(query, llm.split("".join(parse(google(query,max_urls=max_urls,
                                                         animation=animation)))),k=k)
    except:
        return "Error Google Search query Not Found Results."
    return "\n".join(res)

def visionbing(query,k=1,max_urls=5,animation=False):
    try:
        res = llm.topk(query, llm.split("".join(parse(bing(query,max_urls=max_urls,
                                                         animation=animation)))),k=k)
    except:
        return "Error Bing Search query Not Found Results."
    return "\n".join(res)
