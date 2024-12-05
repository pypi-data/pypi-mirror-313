namespace py proto

//角色都有哪些
enum Role {
  BIZ = 0,
  SYSTEM = 1,
  USER = 2,
  ASSISTANT = 3,
  KNOWLEDGE = 4,
  TOOL = 5
}

enum ToolType{
  FUNCTION = 0,//当前只有function这一种tool
}
struct Property {
  1:required string name;  // property_name 
  2:required string value; // property value
}
struct Parameter {
  1: required string type; // object
  2: required list<Property> property;
  // map<string, string> properties = 20; // key: property name, value: json schema string
  3: required list<string> required;//必须有传入值的入参的列表
}
struct Function {
  1: required string name;//function 的名字
  2: required string description;//function的描述｜介绍
  3: required Parameter parameter;//function的每一个入参的解释
}
struct Tool {
  1: required ToolType type;//当前只有function这一种tool
  2: required Function function;
}


struct FunctionCall {
    1: required string function_name;
    // Json Format String of function aguments
    2: required string arguments;
}

struct ToolCall {
  1: required ToolType type; // function, retrieval, codeinterpreter 当前只有function
  2: required FunctionCall function;//选用的是什么function以及function的参数
  3: required string id;
}

enum ContentType{
    TEXT=0;
    IMAGE=1;
    IMAGE_URL=2;
}
struct Content {
    1: required ContentType type; // text, img
    2: required string value;
}


struct Message {
  // 角色
  1: required Role role;
  // 对话内容
  
  2: required list<Content> content;

  // when role=assistant
  3: optional list<ToolCall> tool_calls;
  4: optional string tool_call_id;
}

struct Meta{
    1: required string source;
}
struct Context{
    1: required list<Message> messages;
    2: optional list<Tool> tools;
    3: optional Meta meta;
}

