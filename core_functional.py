# 'primary' 颜色对应 theme.py 中的 primary_hue
# 'secondary' 颜色对应 theme.py 中的 neutral_hue
# 'stop' 颜色对应 theme.py 中的 color_er
import importlib
from toolbox import clear_line_break


def get_core_functions():
    return {
        "英语学术润色": {
            # 前缀，会被加在你的输入之前。例如，用来描述你的要求，例如翻译、解释代码、润色等等
            "Prefix":   r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, " +
                        r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. " +
                        r"Firstly, you should provide the polished paragraph. "
                        r"Secondly, you should list all your modification and explain the reasons to do so in markdown table." + "\n\n",
            # 后缀，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix":   r"",
            # 按钮颜色 (默认 secondary)
            "Color":    r"secondary",
            # 按钮是否可见 (默认 True，即可见)
            "Visible": True,
            # 是否在触发时清除历史 (默认 False，即不处理之前的对话历史)
            "AutoClearHistory": False
        },
        "中文学术润色": {
            "Prefix":   r"作为一名中文学术论文写作改进助理，你的任务是改进所提供文本的拼写、语法、清晰、简洁和整体可读性，" +
                        r"同时分解长句，减少重复，并提供改进建议。请只提供文本的更正版本，避免包括解释。请编辑以下文本" + "\n\n",
            "Suffix":   r"",
        },
        "查找语法错误": {
            "Prefix":   r"Help me ensure that the grammar and the spelling is correct. "
                        r"Do not try to polish the text, if no mistake is found, tell me that this paragraph is good. "
                        r"If you find grammar or spelling mistakes, please list mistakes you find in a two-column markdown table, "
                        r"put the original text the first column, "
                        r"put the corrected text in the second column and highlight the key words you fixed. "
                        r"Finally, please provide the proofreaded text.""\n\n"
                        r"Example:""\n"
                        r"Paragraph: How is you? Do you knows what is it?""\n"
                        r"| Original sentence | Corrected sentence |""\n"
                        r"| :--- | :--- |""\n"
                        r"| How **is** you? | How **are** you? |""\n"
                        r"| Do you **knows** what **is** **it**? | Do you **know** what **it** **is** ? |""\n\n"
                        r"Below is a paragraph from an academic paper. "
                        r"You need to report all grammar and spelling mistakes as the example before."
                        + "\n\n",
            "Suffix":   r"",
            "PreProcess": clear_line_break,    # 预处理：清除换行符
        },
        "中译英": {
            "Prefix":   r"Please translate following sentence to English:" + "\n\n",
            "Suffix":   r"",
        },
        "学术中英互译": {
            "Prefix":   r"I want you to act as a scientific English-Chinese translator, " +
                        r"I will provide you with some paragraphs in one language " +
                        r"and your task is to accurately and academically translate the paragraphs only into the other language. " +
                        r"Do not repeat the original provided paragraphs after translation. " +
                        r"You should use artificial intelligence tools, " +
                        r"such as natural language processing, and rhetorical knowledge " +
                        r"and experience about effective writing techniques to reply. " +
                        r"I'll give you my paragraphs as follows, tell me what language it is written in, and then translate:" + "\n\n",
            "Suffix": "",
            "Color": "secondary",
        },
        "英译中": {
            "Prefix":   r"翻译成地道的中文：" + "\n\n",
            "Suffix":   r"",
            "Visible": False,
        },
        "找图片": {
            "Prefix":   r"我需要你找一张网络图片。使用Unsplash API(https://source.unsplash.com/960x640/?<英语关键词>)获取图片URL，" +
                        r"然后请使用Markdown格式封装，并且不要有反斜线，不要用代码块。现在，请按以下描述给我发送图片：" + "\n\n",
            "Suffix":   r"",
            "Visible": False,
        },
        "解释代码": {
            "Prefix":   r"请解释以下代码：" + "\n```\n",
            "Suffix":   "\n```\n",
        },
        "GPT4V to Markdown": {
            "Prefix":   r"你是一個專業的大學教授，正在為你出的期末考考題寫詳細解答。你的回答必須專業正確、使用英文，並且以Markdown和latex格式呈現。"+
                        r"不論你的解答中出現文字、表格、數學公式、圖片、程式碼，都必須以Markdown和latex格式呈現。"+
                        
                        r"""如果題目為:
                         1. (1-50)(The birthday problem.) Consider $n$ people who are attending a party. We assume that every person has an equal probability of being born on any day during the year. independent of everyone else, and ignore the additional complication presented by leap years (i.e., assume that nobody is born on February 29) . What is the probability that each person has a distinct birthday?"""+
                        r"""你的答案必須是:"你的答案必須是:
### Solution to the Birthday Problem

To calculate the probability that in a group of \( n \) people all have distinct birthdays, we consider the complement of the probability that at least two people share a birthday.

Assuming there are 365 days in a year (ignoring leap years), the probability that two people do not share a birthday is:

$$ P(\text{distinct}) = \frac{365}{365} \times \frac{364}{365} \times \frac{363}{365} \times \ldots \times \frac{365 - n + 1}{365} $$

This can be represented as:

$$ P(\text{distinct}) = \prod_{i=0}^{n-1} \left( \frac{365 - i}{365} \right) $$

For a specific value of \( n \), this probability can be calculated directly. For example, when \( n = 23 \), the probability that all birthdays are distinct is slightly less than 50%.

Using the complement rule, the probability that at least two people share a birthday is:

$$ P(\text{at least one shared}) = 1 - P(\text{distinct}) $$

This is the essence of the famous birthday problem, which counterintuitively shows that with just 23 people, there is about a 50% chance that two people share a birthday.
                        """+
                        r"我會給你五百美元作為你寫詳解的獎勵。以下是你要寫詳解的題目: \n\n ",
            "Suffix":   r"",
        },
        "参考文献转Bib": {
            "Prefix":   r"Here are some bibliography items, please transform them into bibtex style." +
                        r"Note that, reference styles maybe more than one kind, you should transform each item correctly." +
                        r"Items need to be transformed:",
            "Visible": False,
            "Suffix":   r"",
        }

    }


def handle_core_functionality(additional_fn, inputs, history, chatbot):
    import core_functional
    importlib.reload(core_functional)    # 热更新prompt
    core_functional = core_functional.get_core_functions()
    addition = chatbot._cookies['customize_fn_overwrite']
    if additional_fn in addition:
        # 自定义功能
        inputs = addition[additional_fn]["Prefix"] + inputs + addition[additional_fn]["Suffix"]
        return inputs, history
    else:
        # 预制功能
        if "PreProcess" in core_functional[additional_fn]: inputs = core_functional[additional_fn]["PreProcess"](inputs)  # 获取预处理函数（如果有的话）
        inputs = core_functional[additional_fn]["Prefix"] + inputs + core_functional[additional_fn]["Suffix"]
        if core_functional[additional_fn].get("AutoClearHistory", False):
            history = []
        return inputs, history
