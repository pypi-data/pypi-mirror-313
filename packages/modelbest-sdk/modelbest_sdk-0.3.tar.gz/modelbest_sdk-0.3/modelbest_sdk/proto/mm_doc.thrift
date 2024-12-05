namespace cpp proto

enum DocType {
    UNKNOWN = 0,
    TXT = 1,
    IMG = 2,
    AUDIO = 3,
    VIDEO = 4,
}

struct MmDoc {
    10: required DocType dtype,        // 当前doc是哪种类型
    // Deprecated: 文本或语音的token转换的list类型, 效率低.新数据请用binary类型.
    20: optional list<i32> token_info,
    // token_buffer或者text只存其中之一.
    21: optional binary token_buffer,  // 文本或语音的token的binary类型.
    // 原始文本内容, token_buffer或者text只存其中之一.
    22: optional string text,
    // 原始语音内容, token_buffer或者audio_bytes只存其中之一.
    23: optional binary audio_bytes,
    30: optional list<i32> shape,      // 若存token, 表示token的shape
    // 一维数组, true表示不需要算loss.
    // 若存的是token, 大小与shape一维后大小相同. 若存的是text/audio_bytes,长度为1.
    40: optional list<bool> mask,

    // extra info
    // 当前doc的原始id, 图片类型sample此字段为必填. 语音类型填入原始音频来源.
    50: optional string docid,
    // If dtype is IMG, save the md5 of image bytes as well.
    51: optional binary image_md5,
    // If dtype is AUDIO, save the duration of audio.
    52: optional double audio_duration,
    70: optional list<string> tag,     // 当前doc的tag, 可视化使用.
    // op info
    // Deprecated: will store tokenizer version info to metadata.
    80: optional string version,
    // reserved cols
    90: optional string reserved_col,  // 为当前doc预留的字段
}

struct MmDocSeq {
    10: required list<MmDoc> doc_seq,
}

struct MmDocSeqSess {
    10: required list<MmDocSeq> doc_seq_sess,
}