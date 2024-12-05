namespace cpp proto

enum DocType {
    UNKNOWN = 0,
    TXT = 1,
    IMG = 2,
    AUDIO = 3,
    VIDEO = 4,
    AUDIO_SNIPPET = 5,
}

struct AudioToken {
    10: required i32 start,   # 片段开始时间，ms
    20: required i32 stop,     # 片段结束时间，ms
    30: optional string text, # 音频片段对应的文本
}

struct AudioSnippet {
    10: required string wav_file_path,    # 音频文件路径
    20: required i32 start,               # 片段开始时间，ms
    30: required i32 stop,                 # 片段结束时间，ms
    40: optional string text,             # 音频片段对应的文本
    50: optional list<AudioToken> tokens,
}

struct Audio {
    10: required binary wav,  # 音频二进制    
    11: optional binary token_buffer, # tokenized audio token id to bytes
    20: optional string text, # 音频对应的文本
    30: optional list<AudioToken> tokens,
}

struct Content {
    10: required DocType dtype,
    # 当 dtype 为 AUDIO_SNIPPET 时，value为 AudioSnippet 的序列化值；
    # 当 dtype 为 AUDIO 时，value为 Audio 的序列化值；
    20: optional binary value,
}

struct Msg {
    // 角色: system, user, assistant
    10: required string role,
    // 内容
    20: required list<Content> content,
    // 说话者
    30: optional string name,
    40: optional string reserved_column,
}

struct Metadata {
    10: optional string wav_file_path,
}

struct Messages {
    10: required list<Msg> messages,
    20: optional Metadata metadata,
    30: optional string reserved_column,
}