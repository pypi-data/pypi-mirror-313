# encoding=utf-8

import xutils
from xnote.core import xauth, xtemplate, xconfig
from xutils import Storage, webutil, dateutil
from xutils.textutil import quote
from . import dao as msg_dao
from . import message_utils
from .message_model import MessageTag
from xutils.text_parser import TokenType

"""
随手记的标签处理
页面对应的是 ajax/message_tag_ajax.html 
"""
MAX_LIST_LIMIT = 1000


def get_tag_list():
    user_name = xauth.current_name()
    offset = 0
    msg_list, amount = msg_dao.list_by_tag(
        user_name, "key", offset, MAX_LIST_LIMIT)
    return webutil.SuccessResult(data=msg_list)

def get_tag_list_by_msg_list(msg_list, date=""):
    p = message_utils.MessageListParser(msg_list)
    p.parse()
    result = p.get_keywords()
    server_home = xconfig.WebConfig.server_home
    for tag_info in result:
        tag_name = tag_info.name
        tag_info.url = f"{server_home}/message/calendar?tag=log.date&date={date}&filterKey={quote(tag_name)}"
        tag_info.badge_info = f"{tag_info.amount}"
    result.sort(key = lambda x:x.amount, reverse=True)
    return result

def get_tag_list_by_month(user_id=0, month="2000-01"):
    date_start = month + "-01"
    date_end = dateutil.date_str_add(date_start, months=1)
    msg_list, amount = msg_dao.list_by_date_range(user_id=user_id, date_start=date_start, date_end=date_end)
    result = get_tag_list_by_msg_list(msg_list, date=month)
    return result

def get_log_tags_page():
    """随手记的话题标签页面"""
    orderby = xutils.get_argument_str("orderby", "")

    kw = Storage(
        tag="key",
        search_type="message",
        show_tag_btn=False,
        show_attachment_btn=False,
        show_system_tag=True,
        message_placeholder="添加标签/关键字/话题",
        show_side_tags=False,
    )

    kw.show_input_box = False
    kw.show_sub_link = False
    kw.orderby = orderby
    kw.search_ext_dict = dict(tag="search")
    kw.show_left_tags = False
    kw.message_left_class = "hide"
    kw.message_right_class = "row"

    return xtemplate.render("message/page/message_list_view.html", **kw)


def filter_standard_msg_list(msg_list):
    result = []
    for item in msg_list:
        if message_utils.is_standard_tag(item.content):
            result.append(item)
    return result

def list_message_tags(user_name, offset, limit, *, orderby = "amount_desc", only_standard=False):
    msg_list, amount = msg_dao.list_by_tag(
        user_name, "key", 0, MAX_LIST_LIMIT)
    
    if only_standard:
        msg_list = filter_standard_msg_list(msg_list)

    p = message_utils.MessageKeyWordProcessor(msg_list)
    p.process()
    p.sort(orderby)

    return msg_list[offset:offset+limit], len(msg_list)

def get_recent_keywords(user_name: str, tag="search", limit =20):
    """获取最近访问的标签"""
    msg_list, amount = list_message_tags(user_name, 0, limit, orderby = "recent", only_standard=True)
    parser = message_utils.MessageListParser(msg_list, tag=tag)
    parser.parse()
    result = parser.get_message_list()
    for item in result:
        item.badge_info = ""
    return result

def add_tag_to_content(content="", new_tag=""):
    msg_struct = message_utils.mark_text_to_tokens(content=content)

    tags = []
    rest_str_list = []
    is_rest = False

    for token in msg_struct.tokens:
        if is_rest:
            rest_str_list.append(token.value)
        else:
            trim_value = token.value.strip()
            if token.is_topic():
                tags.append(token.value)
                continue
            
            if trim_value == "":
                continue

            # 既不是标签也不是空格
            is_rest = True
            rest_str_list.append(token.value)

    if new_tag not in tags:
        tags.append(new_tag)

    rest_text = "".join(rest_str_list).strip()
    return " ".join(tags) + "\n" + rest_text

