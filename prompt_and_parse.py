# -*- coding: utf-8 -*-
import re
def construct_prompt(d):
    """
    构造用于大语言模型的提示词

    参数:
        d (dict): jsonl数据文件的一行，为字典类型的变量

    返回:
        list: OpenAI API的message格式列表，允许设计多轮对话式的prompt
    """
    user_id = d.get("user_id")
    item_list = d.get("item_list", [])
    candidates = d.get("candidates", [])

    history_str = "\n".join([
        f"- {title}（电影ID：{movie_id}，时间排名：{i+1}）"
        for i, (movie_id, title) in enumerate(item_list)
    ])

    candidate_str = "\n".join([
        f"{i+1}. {title}（电影ID：{movie_id}）"
        for i, (movie_id, title) in enumerate(candidates)
    ])
    
    ### Change Your Prompt Here.
    system_message = {
        "role": "system",
        "content": (
            "你是一位电影推荐专家模型，任务是根据用户最近的观影行为预测其下一部最可能观看的电影，"
            "并对给定的候选电影列表进行精准排序，输出推荐强度从高到低的电影ID数组，以最大化排序评估指标NDCG@10。\n\n"
            "【排序目标】\n"
            "- 推荐重点在于预测真实用户行为，而非泛兴趣匹配；\n"
            "- 候选列表中**包含真实目标电影**，应最大程度地将其排序前置，确保NDCG@10达到或超过0.8。\n\n"
            "【推荐逻辑流程】\n"
            "1. 提取用户最近3部观影记录中的偏好特征（类型、题材、情绪氛围、导演风格），形成兴趣画像；\n"
            "2. 对每部候选电影构建对应的四维内容标签，需基于真实内容描述，不可仅依标题推测；\n"
            "3. 计算候选电影与用户兴趣的匹配程度，生成推荐强度；\n"
            "4. 综合排序逻辑如下：\n"
            "   - 【强匹配】：类型+题材完全一致，风格/情绪贴合 → 排前2位；\n"
            "   - 【中匹配】：类型或题材匹配，且有风格或情绪相似点 → 排第3-5位；\n"
            "   - 【容错匹配】：风格或情绪较接近，但题材创新或偏离主流兴趣 → 排第6-8位；\n"
            "   - 【弱匹配】：标签脱节，风格差异大，与近期行为不符 → 排末位；\n"
            "   - 若候选项虽匹配度不强但有潜在行为目标特征（如冷门探索、片单延续等），允许其容错前移排序。\n\n"
            "【强化要求】\n"
            "- 对真实目标电影（若能识别）应排序在前3位；\n"
            "- 对内容标签缺失或类型模糊的电影，需根据剧情、氛围、设定合理推理填补；\n"
            "- 不得基于标题或流行度主观推测，应以结构化分析为准。\n\n"
            "【输出格式】\n"
            "- 输出格式必须为JSON数组；\n"
            "- 数组内容仅含候选电影ID，顺序表示推荐强度，由高到低；\n"
            "- 禁止任何解释、注释或标签信息；\n"
            "- 示例输出：[522, 706, 554, 738, 659, 729, 751, 405, 549, 475]"
        )
    }



    user_message = {
        "role": "user",
        "content": (
            f"请根据以下用户的观影记录，预测其当前偏好，并对候选电影进行排序：\n\n"
            f"【用户ID】：{user_id}\n\n"
            f"【观影历史】（按时间排序，越后越近期）：\n{history_str}\n\n"
            f"【候选电影列表】：\n{candidate_str}\n\n"
            f"任务要求：\n"
            f"- 提取最近3部电影中的偏好特征（类型/题材/情绪/风格）。\n"
            f"- 为每部候选电影生成内容标签并比对。\n"
            f"- 排序目标是预测用户的下一部观看行为，而不仅仅是相似兴趣。\n"
            f"- 候选中包含用户真实观看的目标电影，请尽量将其排在前列，但也要考虑整体匹配逻辑。\n"
            f"- 输出格式为JSON数组，长度与候选电影数量一致，仅包含ID，如：[2492, 684, 738, ...]。\n"
            f"- 禁止输出任何解释、标签或注释内容。"
        )
    }

    return [system_message, user_message]


def parse_output(text):
    """
    解析大语言模型的输出文本，提取推荐重排列表

    参数:
    text (str): 大语言模型的输出文本

    返回:
    list of int: 推荐的电影ID顺序
    """
    match = re.search(r'\[([0-9,\s]+)\]', text)
    if not match: return []
    index_list = [int(x.strip()) for x in match.group(1).split(',') if x.strip().isdigit()]
    return index_list
