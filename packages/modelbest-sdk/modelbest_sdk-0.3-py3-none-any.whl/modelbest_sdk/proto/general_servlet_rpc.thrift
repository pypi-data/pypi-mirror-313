namespace py proto

include "proto/chatdoc.thrift"

enum InferType {
  RANDOM_SEARCH = 0,
  BEAM_SEARCH = 1,
}

struct LlmInferParams {
  1: InferType type
  2: double temperature = 0.8
  3: i32 seed = 366788428
  4: i32 max_length = 1024

  5: double repetition_penalty = 1.05
  6: double ngram_penalty = 1.02
  7: double top_p = 0.4
  8: i32 num_results = 16

  // 调用模型的标识符
  9: optional string model_version
}

struct LlmRequest {
  // request的uuid, 方便定位追查问题使用
  1: string id = "0"
  // 历史对话和提问
  2: chatdoc.ChatSession chat_session
  // 请求模型的超参
  3: optional LlmInferParams llm_infer_params
  // 历史对话轮数：-1使用所有历史对话
  4: optional i16 hist_dialogue_round = -1
  // Verbose level of debug information to be passed back.
  5: optional i16 default_debug_level = 0
  // Log level for logging.
  6: optional i16 default_log_level = 0
  // 业务线id, 方便后续数据飞轮和log闭环使用
  7: optional string business_id = "0"
}

struct LlmResponse {
  // response 的id, 方便定位追查问题使用
  1: string id = "0"
  // 多套返回结果
  2: list<chatdoc.ChatSession> chat_session
  // Per-response debug information (May include HTML), which is controlled
  // by default_debug_level.
  3: optional string debug_info
  // 响应时间
  4: optional double duration
  // 业务线id, 方便后续数据飞轮和log闭环使用
  5: optional string business_id = "0"
}

// ****************************** GeneralServlet **************************
service LlmService {
  LlmResponse LlmInfer(1: LlmRequest request);
}