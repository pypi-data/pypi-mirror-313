// 特殊字符
const string LINE_SEP = "\n"
const string ROLE_CONTENT_SEP = "："
const string START_INDICATOR = "<|im_start|>"
const string END_INDICATOR = "<|im_end|>"
const string SYSTEM_INDICATOR = "system"
const string ASSISTANT_INDICATOR = "assistant"
const string INSTRUCTION_INDICATOR = "instruction"
const string USER_INDICATOR = "user"
const string KNOWLEDGE_INDICATOR = "knowledge"
const string COMMA_SEP = "\n"

// prompt拼接字段
const string PROMPT_0 = "现在请你假扮"
const string PROMPT_1 = "与我进行对话"
const string PROMPT_2 = "接下来的对话里，你需要扮演"
const string PROMPT_3 = "我将扮演："
const string PROMPT_4 = "我们的关系是："
const string PROMPT_5 = "[开始对话]"
const string PROMPT_6 = "指令："
const string PROMPT_7 = "是"
const string RAG_PROMPT = "下面会给你提供一段背景知识，请你在回答之前参考这段知识进行回答。"
// prompt拼接字段list类型
const list<string> PROMPT_0_LIST = ["现在请你假扮","现在请你扮演","你是角色扮演大师，你将扮演","你是一名知名演员，你要演绎",'现在请你扮演','请你此刻假装成','现在，我需要你假装自己是','现在，请你扮演一下','请你现在开始扮演','此刻，请你假扮成','现在，请你进行角色扮演','请你现在假扮成那个','现在请你进入角色扮演模式，扮演']
const list<string> PROMPT_1_LIST = ["与我进行对话",'与我展开交流','与我进行交谈','与我进行沟通对话','与我进行语言交流','和我对话一番','与我进行互动对话','和我展开对话交流','与我进行深入的对话','与我进行对话交流吧']
const list<string> PROMPT_2_LIST = ["接下来的对话里，你需要扮演",'在接下来的对话中，你需要扮演','在接下来的交流中，你需要担当','接下来的对话中，需要你扮演','请你在接下来的对话中，扮演','接下来的交流里，你的角色是','请你在接下来的对话中，担任','在对话的接下来部分，你需要扮演','接下来的对话中，你的任务是扮演','在接下来的对话环节，你需要化身']
const list<string> PROMPT_3_LIST = ["我将扮演：",'我将扮演起：', '我将化身为：', '我将饰演：', '我将模仿：', '我将充当：', '我将演绎：', '我将假扮：', '我是']
const list<string> PROMPT_4_LIST = ["我们的关系是：","你和我之间的关系是：","我们之间的关系是：","关系是"]
const list<string> PROMPT_5_LIST = ["[开始对话]",'[展开对话]','[发起对话]','[启动对话]','[进行对话交流]','[开展对话]','[进行对话]','[开始交谈]','[发起沟通]','[展开交流]','[发起对话交流]']
const list<string> PROMPT_6_LIST = ["指令：","命令：","你将要：","你需要："]
const list<string> PROMPT_7_LIST = ["是","为"]
const list<string> RAG_PROMPT_LIST = ["下面会给你提供一段背景知识，请你在回答之前参考这段知识进行回答。",'在你回答之前，我会先给你一段背景知识，请务必参考它。','请在回答之前，仔细阅读我提供的这段背景知识，以便更好地理解问题。','为了帮助你更好地回答，我会先给出一段背景知识，请务必参考。','在你给出答案之前，请确保已经阅读并理解了这段背景知识。','请参考我提供的背景知识来回答，这样你的答案会更加准确和全面。','在你开始回答之前，先阅读一下这段背景知识，这对你会有帮助的。','为了确保你的回答更加精准，请先参考我提供的这段背景知识。','在你构思答案时，请务必参考我所提供的背景知识。','我会先给出一段背景知识，你在回答时请以此为参考。','为了使你的回答更加有依据，请在阅读并理解这段背景知识后再进行回答。']
// prompt大框架需要固定
const string BASIC_INFO_TEXT = "基本信息"
const string PERSONALITY_TEXT = "的性格"
const string RELATIONSHIP_TEXT = "人物关系"
const string EXPERIENCE_TEXT = "的主要经历"
const string LANG_STYLE_TEXT = "的语言风格"
const string RELATED_PEOPLE_TEXT = "相关人物"
const string STORY_TEXT = "故事梗概"
// prompt大框架需要固定
const list<string> BASIC_INFO_TEXT_LIST = ["基本信息",'基础资料', '主要信息', '基础数据', '基本内容', '重要数据', '必要信息', '概况信息', '初步资料']
const list<string> PERSONALITY_TEXT_LIST = ["的性格",'的个性特征', '的脾气秉性', '的性格特质', '的品行性格', '的人格特点', '的气质性格', '的性格倾向', '的性格属性', '的性情特点', '的个性倾向']
const list<string> RELATIONSHIP_TEXT_LIST = ["人物关系",'人物之间的关联', '人物间的联系', '人物关联状态', '人物间的交往关系', '人物间的互动情况',  '人物之间的情感联系', '人物间的联系状态', '人物间的交往情况']
const list<string> EXPERIENCE_TEXT_LIST = ["的主要经历",'的重要历程', '的关键经历', '的主要事迹', '的核心经历', '的重大经历', '的重要过往', '的关键历程', '的主要历史']
const list<string> LANG_STYLE_TEXT_LIST = ["的语言风格",'的说话方式', '的表达方式', '的言辞特点', '的叙述风格', '的说话风格', '的文字风格', '的话语格调', '的表述风格', '的讲话特色', '的语言特色']
const list<string> RELATED_PEOPLE_TEXT_LIST = ["相关人物",'涉及人物', '相关个体', '关联人物', '相关人士', '涉及人士', '相关角色', '关联个体', '相关人员', '关联人士', '涉及角色']
const list<string> STORY_TEXT_LIST = ["故事梗概",'情节概述', '概要介绍', '大意简述', '线索简述', '框架概述', '概要描述', '主要情节', '核心内容', '大体脉络', '大体梗概']