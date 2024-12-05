namespace py proto

struct MapItem {
    1: string k,
    2: string v,
}

struct Dialogue {
    // 角色
    10: string role,
    // 对话内容
    20: string content,
    // 动态指令信息
    30: list<string> dynamic_instruction,
    // 回复参考信息 for rag
    40: list<string> reference,
}

enum InstructionType {
    // 括号文学
    KUO_HAO_WEN_XUE = 0,
    // 主动性
    ZHU_DONG_XING = 1,
    // 英语
    ENGLISH = 2,
    // 恋爱
    LIANAI = 3,
    // 偶像剧
    OU_XIANG_JU = 4,
    // 闲聊
    XIAN_LIAO = 5,
    // 颜文字
    YAN_WEN_ZI = 6,
    // 豆瓣论坛
    DOU_BAN_LUN_TAN = 7,
    // 答疑解惑
    DA_YI_JIE_HU = 8,
    // 舞台逗趣
    WU_TAI_DOU_QU = 9;
    // 安全指令
    SAFETY = 10;
    // B站
    BILIBILI = 11;
    // 微博
    WEIBO = 12;
    // Hindi
    HINDI = 13;
    // 表情包
    STICKER = 14;
    // nsfw-0
    NSFW_ZERO_LEVEL = 15;
    // nsfw-1
    NSFW_FIRST_LEVEL = 16;
    // nsfw-2
    NSFW_SECOND_LEVEL = 17;
    // nsfw-3
    NSFW_THIRD_LEVEL = 18;
}

struct Profile {
    // 模型角色自称
    10: string role,
    // 基本信息
    20: optional string basic_info,
    // 性格
    30: optional string personality,
    // 角色-关系映射
    40: optional list<MapItem> role_relationship,
    // 主要经历
    50: optional string experience,
    // 语言风格
    60: optional string lang_style,
    // 相关人物
    70: optional list<MapItem> related_characters,
    // 人口学信息
    // 昵称
    80: optional list<string> nickname,
    // 性别
    90: optional string gender,
    // 物种
    100: optional string species,
    // 年龄
    110: optional string age,
    // 工作
    120: list<string> job,
    // 身高
    130: optional string height,
    // 体重
    140: optional string weight,
    // 居住地
    150: optional string residence,
    // 恋爱状态
    160: optional string love_status,
    // 爱好
    170: optional list<string> hobby,
    // 血型
    180: optional string blood_type,
    // 三围
    190: optional string three_size,
    // 家乡
    200: optional string hometown,
    // 技能
    210: optional list<string> skill,
    // 生日
    220: optional string birthday,
    // 生肖
    230: optional string zodiac,
    // 星座
    240: optional string sign,
    // 智商
    250: optional string iq,
    // 情商
    260: optional string eq,
    // 喜欢的事情/东西
    270: optional list<string> likes,
    // 不喜欢的事情/东西
    280: optional list<string> dislikes,
    // 经典台词
    290: optional list<string> stage_lines,
    // 口头禅
    300: optional list<string> pet_phrase,
    // 开场白
    310: optional string prologue,
    // story
    320: optional string story,
    // 其他信息
    330: optional string annotation,
    // 记忆
    340: optional string memory
}

struct RoleTrainDoc {
    // 模型扮演角色
    10: string act_as,
    // 对话内容
    20: list<Dialogue> chat_session,
    // 模型扮演角色人物profile
    30: Profile profile,
    // 指令类型
    40: optional list<InstructionType> global_instruction_type,
    // 标签
    50: optional list<string> tag,
}

struct ChatSession {
    10: list<Dialogue> messages,
    20: optional list<string> tag,
}