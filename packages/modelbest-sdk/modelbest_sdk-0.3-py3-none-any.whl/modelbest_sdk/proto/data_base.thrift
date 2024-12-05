// NOTE: This proto is used by many important components.

namespace cpp proto

// Important:
//  Please keep it consistent to util/content_type/public/doctype_to_string.h
enum DocType {
  NORMAL = 0,
  // except NORMAL, all other types are virtual doc.
  TOPIC = 1,
  REVIEW = 2,
  COMMENT = 3,
  QUESTION = 4,
  ANSWER = 5,
  STATUS_UPDATE = 6,
  BLOG = 7,
  FORUM_POST = 8,
  WEB_QA = 9,  // external QA
  NEWS = 10,
  BBS = 11,
  SHOPPING = 12,
  VIDEO = 13,
  ACTIVITY = 14,
  USER_PROFILE = 15,
  OFFICAL_HOME = 16,
  FRIEND_LINKS = 17,
  SITE_MAP = 18,
  SEARCH_RESULT_PAGE = 19,
  SHOPPING_DETAIL = 20,
  KNOWLEDGE_PAGE = 21,
  NEWS_HUB = 22,
  NEWS_CONTENT = 23,
  BLOG_HUB = 24,
  BLOG_CONTENT = 25,
  BBS_HUB = 26,
  BBS_CONTENT = 27,
  QA_SOLVED = 28,
  HUDONG_CLONE = 29,
  BLOG_PERSON_PROFILE = 30,
  DICT = 31,
  FLASH_HOMEPAGE = 32,
  GROUPBUYING = 33,
  GROUPBUYING_OUT = 34,
  NAVIGATION = 35,  // e.g. 265.com
  DOWNLOAD_PAGE = 36,

  NOVEL_PAGE = 37,
  NOVEL_DETAIL_PAGE = 38,
  NOVEL_HUB_PAGE = 39,
  SEARCH_BY_CLICK_PAGE = 40,
  MUSIC_PAGE = 41,
  MUSIC_PLAYER = 42,
  VIDEO_DETAIL = 43,
  NON_SEARCH_RESULT = 44,
  IMAGE = 45,
  URL_ACTIVITY = 46, // used by social search
  EMPTY_RESULT = 47,
  DOMAIN_SELL_PAGE = 48,
  DEDECMS_PAGE = 49,
  NEWS_TOPIC = 50,
  APP_TOPIC = 51,  // used by mobile_app_merger
  SHORTURL = 52, // used by social search

  MOBILE_WML = 53,
  MOBILE_HTML = 54,

  VIDEO_HUB = 55,
  TAG_PAGE = 56,

  CONTENT_LINK = 57, //some content page with many links, eg http://product.yesky.com/product/882/882809/
  
  DIGIT_LINK = 58,
  CAR_LINK = 59,
  HOUSE_LINK = 60,
  TRAVEL_LINK = 61,
  HOTEL_LINK = 62,
  COOK_LINK = 63,
  
  CONTENT_NEW = 64, //new type added for some missed page, eg http://dqgcxy.whu.edu.cn/xxgk/xytz/2012-05-22/1138.html
  MOBILE_NEWS = 65,
  PC = 66,

  POLICY_CONTENT = 67, // new type added for policy page, eg http://www.gov.cn/zhengce/content/2019-11/07/content_5449754.htm
  SPECIAL_NEWS_HUB = 68, // new type added for policy page, eg http://www.xinhuanet.com/politics/ldzt/yzgskzg/index.htm 

  NEWS_EVENT = 100,
  INVALID_TYPE = 300,
}

enum DocFormat {
  DOCFORMAT_HTML   = 0,
  DOCFORMAT_PDF    = 1,
  DOCFORMAT_MSDOC  = 2,
  DOCFORMAT_PPT    = 3,
  DOCFORMAT_XLS    = 4,
  DOCFORMAT_XML    = 5,
}

enum PageType {
  HOMEPAGE = 1,
  CONTENT = 2,
  TAG = 3,
  UNKNOWN = 4,
}

enum CoreContentType {
  NEWS = 1,
  NOVEL = 2,
  KNOWLEDGE = 3,
  MUSIC = 4,
  VIDEO = 5,
  PICTURE = 6,
  DICT = 7,
  BBS = 8,
  BLOG = 9,
  MICROBLOG = 10,
  QA = 11,
  SHOPPING = 12,
  DOWNLOAD = 13,
  COMMENT = 14,
  OTHER_CONTENT = 15,
  USERPROFILE = 16,
  DOMAIN_SELL = 17,
  STRUCT = 18,
  TAG = 19,
  SEARCH = 20,
  HOMEPAGE = 21,
  NEWS_TOPIC = 22,
  POLICY = 23,
  SPECIAL_NEWS_HUB = 24,

  UNKNOWN = 300,
}

enum ScreenType {
  PC = 1,
  MOBILE = 2,
}

// IMPORTANT: enum values have to be continuous.
// Please keep the list consistent with AnchorTypeToString in
// "indexing/base/enum_to_string.h/cc".
// "indexing/pipeline/base/anchortype_to_string.h".
// Also please reconsider kAnchorPriority weight in
// "indexing/pipeline/inlink/internal/host_cluster_handler.cc
// or contact the internal's current owner
enum AnchorType {
  NORMAL_ANCHOR = 0,
  EXTENDED_ANCHOR = 1,
  ANCHOR_TITLE = 2,
  IMG_ALT = 3, 
  IMG_TITLE = 4,
  INVISIBLE = 5,
  FRIENDLY_LINK = 6,
  OFFICAL_LINK = 7,
  SPAM_LINK = 8
  AREA_ALT = 9,
  BREADCRUMB = 10,
  AD_LINK = 11,
  TRUST_ANCHOR = 12,
  INFERED_TRUST_ANCHOR = 13,
  // add by jike 
  TEXT_LINK = 14,
  MAX_INDEXED_ANCHOR_TYPE = 16,
  // Set AnchorType less than 16 in order to be built to index,
  // otherwise set a bigger one.
  MAX_ANCHOR_TYPE = 17,
} 
  
// IMPORTANT: enum values have to be continuous.
enum FilterType {
  FILTER_NONE = 0,
  FILTER_SPAM = 1,
  FILTER_PORN = 2, 
  FILTER_GOVERNMENT_LAW = 3,
  FILTER_DEADLINK = 4,
}
