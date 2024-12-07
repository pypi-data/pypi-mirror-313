from langchain_openai import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
import time
import random
import json
import os
import sys
import argparse

print('Importing keywordrich')


def keywordrich(keywordstr='', openai_api_key=''):

    if openai_api_key == '':
        print('请输入deepseek的api_key')
        return None

    if keywordstr == '':
        print('请输入keyword')
        return None

    keywordstr = str(keywordstr)
    llm = ChatOpenAI(
        model='deepseek-chat',
        temperature=0.7,
        openai_api_base='https://api.deepseek.com/v1',
        openai_api_key=openai_api_key
        )

    # 构建输出模板
    response_schemas = [
        ResponseSchema(type='list', name="KeywordRichList",
                       description='这一项是一个包含5个元素的列表，其中的元素根据关键词的相关性从高到低进行排序'),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    # 存放结果数据
    template = """
    给出一个关键词，请根据这个关键词生成一个列表，列表中的元素是给定关键词的长尾关键词，输出的列表中的元素需要根据与关键词的相关性进行排序:
    {format_instructions}

    %管仅此:
    {keywordstr}
    """
    prompt = PromptTemplate(
        input_variables=["keywordstr"],
        partial_variables={"format_instructions": format_instructions},
        template=template,
    )

    try:
        final_prompt = prompt.format(keywordstr=keywordstr)
        llm_output = llm.invoke(final_prompt)
        time.sleep(random.randint(1, 3))
        parsed_result = json.loads(llm_output.content.strip('`').replace('json', ''))
        keywordRichList = parsed_result['KeywordRichList']
        print('长尾关键词已生成！')
        return keywordRichList
    except:
        time.sleep(random.randint(1, 3))
        print('长尾关键词生成失败！')
        return None

