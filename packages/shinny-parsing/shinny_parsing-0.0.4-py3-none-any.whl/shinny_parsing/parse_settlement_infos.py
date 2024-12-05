#!usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'mayanqiong'

import os
import re


def get_arr(line: str) -> list:
    """根据 | 分割为数组"""
    items = line.split('|')
    return [item.strip() for item in items[1: -1]]


def get_item(keys, values) -> object:
    """根据 keys - values 返回 object"""
    return dict(zip(keys, values))


def parse_settlment(content: str):
    """
    将原始的结算单字符串，转为标准的 dict，返回的结构为
    {
        'head': {
            'key': '交易结算单',
            'title': '交易结算单(盯市) Settlement Statement(MTM)',
            'type': 'head',
            'content': {'client_id': '103988', 'client_name': 'yanqiong', 'date': '20210915', 'broker_id': 'SimNow社区系统'}
        },
        'tables': {
            '资金状况': {
                'key': '资金状况',
                'title': '资金状况  币种：人民币  Account Summary  Currency：CNY',
                'type': 'account',
                'cols_zh': ['期初结存', '基础保证金', '出 入 金', '期末结存', '平仓盈亏', '质 押 金', '持仓盯市盈亏', '客户权益', '期权执行盈亏', '货币质押保证金占用', '手 续 费', '保证金占用', '行权手续费', '交割保证金', '交割手续费', '多头期权市值', '货币质', '空头期权市值', '货币质出', '市值权益', '质押变化金额', '可用资金', '权利金收入', '风 险 度', '权利金支出', '应追加资金', '货币质押变化金额'],
                'cols_en': ['Balance b/f', 'Initial Margin', 'Deposit/Withdrawal', 'Balance c/f', 'Realized P/L', 'Pledge Amount', 'MTM P/L', 'Client Equity', 'Exercise P/L', 'FX Pledge Occ.', 'Commission', 'Margin Occupied', 'Exercise Fee', 'Delivery Margin', 'Delivery Fee', 'Market value(long)', 'New FX Pledge', 'Market value(short)', 'FX Redemption', 'Market value(equity)', 'Chg in Pledge Amt', 'Fund Avail.', 'Premium received', 'Risk Degree', 'Premium paid', 'Margin Call', 'Chg in FX Pledge'],
                'content': [
                    ['23946109.11', '0.00', '0.00', '23913900.61', '-20310.00', '0.00', '-11760.00', '23913900.61', '0.00', '0.00', '138.50', '457051.20', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '23913900.61', '0.00', '23456849.41', '0.00', '1.91', '0.00', '0.00', '0.00']
                ]
            },
            '成交记录': {
                'key': '成交记录',
                'title': '成交记录 Transaction Record',
                'type': 'table',
                'cols_zh': ['成交日期', '交易所', '品种', '合约', '买/卖', '投/保', '成交价', '手数', '成交额', '开平', '手续费', '平仓盈亏', '权利金收支', '成交序号', '成交类型'],
                'cols_en': ['Date', 'Exchange', 'Product', 'Instrument', 'B/S', 'S/H', 'Price', 'Lots', 'Turnover', 'O/C', 'Fee', 'Realized P/L', 'Premium Received/Paid', 'Trans.No.', 'trade type'],
                'content': [
                    ['20210915', '上期所', '铝', 'al2110', '买', '投机', '22315.000', '2', '223150.00', '平昨', '6.00', '4650.00', '0.00', '141153', '普通成交'],
                    ['20210915', '郑商所', '苹果', 'AP111', '卖', '投机', '5440.000', '9', '489600.00', '开', '45.00', '0.00', '0.00', '198955', '普通成交'],
                    ['20210915', '中金所', '上证50指数', 'IH2109', '卖', '交易', '3170.200', '4', '3804240.00', '平', '87.50', '-24960.00', '0.00', '138344', '普通成交']
                ]
            },
            '平仓明细': {
                'key': '平仓明细',
                'title': '平仓明细 Position Closed',
                'type': 'table',
                'cols_zh': ['平仓日期', '交易所', '品种', '合约', '开仓日期', '买/卖', '手数', '开仓价', '昨结算', '成交价', '平仓盈亏', '权利金收支', '成交类型'],
                'cols_en': ['Close Date', 'Exchange', 'Product', 'Instrument', 'Open Date', 'B/S', 'Lots', 'Pos. Open Price', 'Prev. Sttl', 'Trans. Price', 'Realized P/L', 'Premium Received/Paid', 'trade type'],
                'content': [
                    ['20210915', '上期所', '铝', 'al2110', '20210914', '买', '2', '22260.000', '22780.000', '22315.000', '4650.00', '0.000', '普通成交'],
                    ['20210915', '中金所', '上证50指', 'IH2109', '20210910', '卖', '4', '3257.200', '3191.000', '3170.200', '-24960.00', '0.000', '普通成交']
                ]
            },
            '持仓明细': {'
                key': '持仓明细',
                'title': '持仓明细 Positions Detail',
                'type': 'table',
                'cols_zh': ['交易所', '品种', '合约', '开仓日期', '投/保', '买/卖', '持仓量', '开仓价', '昨结算', '结算价', '浮动盈亏', '盯市盈亏', '保证金', '期权市值'],
                'cols_en': ['Exchange', 'Product', 'Instrument', 'Open Date', 'S/H', 'B/S', 'Positon', 'Pos. Open Price', 'Prev. Sttl', 'Settlement Price', 'Accum. P/L', 'MTM P/L', 'Margin', 'Market Value(Options)'],
                'content': [
                    ['中金所', '上证50指数', 'IH2109', '20210910', '交易', '买', '1', '3257.200', '3191.000', '3142.400', '-34440.00', '-14580.00', '103699.20', '0.00'],
                    ['中金所', '上证50指数', 'IH2109', '20210914', '交易', '买', '1', '3190.800', '3191.000', '3142.400', '-14520.00', '-14580.00', '103699.20', '0.00'],
                    ['中金所', '上证50指数', 'IH2109', '20210914', '交易', '买', '1', '3190.800', '3191.000', '3142.400', '-14520.00', '-14580.00', '103699.20', '0.00'],
                    ['郑商所', '苹果', 'AP111', '20210915', '投机', '卖', '9', '5440.000', '5410.000', '5418.000', '1980.00', '1980.00', '39009.60', '0.00'],
                    ['上期所', '铝', 'al2110', '20210914', '投机', '卖', '5', '22260.000', '22780.000', '22280.000', '-500.00', '12500.00', '44560.00', '0.00'],
                    ['上期所', '铝', 'al2110', '20210914', '投机', '卖', '1', '22300.000', '22780.000', '22280.000', '100.00', '2500.00', '8912.00', '0.00'],
                    ['上期所', '铝', 'al2110', '20210914', '投机', '卖', '1', '22295.000', '22780.000', '22280.000', '75.00', '2500.00', '8912.00', '0.00'],
                    ['上期所', '铝', 'al2110', '20210914', '投机', '卖', '1', '22290.000', '22780.000', '22280.000', '50.00', '2500.00', '8912.00', '0.00'],
                    ['上期所', '铝', 'al2110', '20210914', '投机', '卖', '1', '22300.000', '22780.000', '22280.000', '100.00', '2500.00', '8912.00', '0.00'],
                    ['上期所', '铝', 'al2110', '20210914', '投机', '卖', '1', '22300.000', '22780.000', '22280.000', '100.00', '2500.00', '8912.00', '0.00'],
                    ['上期所', '铝', 'al2110', '20210914', '投机', '卖', '1', '22305.000', '22780.000', '22280.000', '125.00', '2500.00', '8912.00', '0.00'],
                    ['上期所', '铝', 'al2110', '20210914', '投机', '卖', '1', '22310.000', '22780.000', '22280.000', '150.00', '2500.00', '8912.00', '0.00']
                ]
            },
            '持仓汇总': {
                'key': '持仓汇总',
                'title': '持仓汇总 Positions',
                'type': 'table',
                'cols_zh': ['品种', '合约', '买持', '买均价', '卖持', '卖均价', '昨结算', '今结算', '持仓盯市盈亏', '保证金占用', '投/保', '多头期权市值', '空头期权市值'],
                'cols_en': ['Product', 'Instrument', 'Long Pos.', 'Avg Buy Price', 'Short Pos.', 'Avg Sell Price', 'Prev. Sttl', 'Sttl Today', 'MTM P/L', 'Margin Occupied', 'S/H', 'Market Value(Long)', 'Market Value(Short)'],
                'content': [
                    ['上证50指数', 'IH2109', '3', '3212.933', '0', '0.000', '3191.000', '3142.400', '-43740.00', '311097.60', '交易', '0.00', '0.00'],
                    ['苹果', 'AP111', '0', '0.000', '9', '5440.000', '5410.000', '5418.000', '1980.00', '39009.60', '投机', '0.00', '0.00'],
                    ['铝', 'al2110', '0', '0.000', '12', '22283.333', '22780.000', '22280.000', '30000.00', '106944.00', '投机', '0.00', '0.00']
                ]
            }
        }
    }
    """
    origin_lines = [l.strip() for l in content.split('\n')]
    parse_result = {
        'head': {},
        'tables': {},
    }
    current_section = None
    title = ''
    for index, line in enumerate(origin_lines):
        if index == 0:
            title = line.strip()
            continue
        if is_section_start_line(line):
            current_section = get_section(line)
            continue
        if current_section is None:
            continue
        elif current_section['type'] == 'head':
            if line == '':
                parse_result['head'] = current_section
                current_section = None
            elif line.startswith('客户号'):
                r = re.match(r'客户号 Client ID[:：](.*)客户名称 Client Name[:：](.*)', line)
                if r is None:
                    r = re.match(r'客户号[:：](.*)客户名称[:：](.*)', line)
                if r is None:
                    raise Exception(f"解析客户号和客户名称失败，行内容为：{line}")
                client_id = line[r.regs[1][0]:r.regs[1][1]]
                client_name = line[r.regs[2][0]:r.regs[2][1]]
                current_section['content']['client_id'] = client_id.strip()
                current_section['content']['client_name'] = client_name.strip()
            elif line.startswith('日期'):
                r = re.match(r'日期 Date[:：](.*)', line)
                if r is None:
                    r = re.match(r'日期[:：](.*)', line)
                if r is None:
                    raise Exception(f"解析日期失败，行内容为：{line}")
                date = line[r.regs[1][0]:r.regs[1][1]]
                current_section['content']['date'] = date.strip()
        elif current_section['type'] == 'account':
            if line == '':
                parse_result['tables'][current_section['key']] = current_section
                current_section = None
            elif len(line) == line.count('-'):
                continue
            else:
                zh_matches = re.findall(r'[\u4e00-\u9fa5][\u4e00-\u9fa5\s]+[\u4e00-\u9fa5]+', line)
                en_matches = re.findall(r'[a-zA-Z][a-zA-Z\.\/\(\)\s]+', line)
                number_matches = re.findall(r'-?\d+\.\d\d', line)
                assert len(zh_matches) == len(en_matches) == len(number_matches)
                for i in range(len(zh_matches)):
                    current_section['cols_zh'].append(zh_matches[i])
                    current_section['cols_en'].append(en_matches[i])
                    current_section['content'][0].append(number_matches[i])
        elif current_section['type'] == 'table':
            if len(line) == line.count('-'):
                current_section['read_state'] += 1
                continue
            if current_section['read_state'] == 1:
                current_section['cols_en' if current_section['cols_zh'] else 'cols_zh'] = get_arr(line)
            elif current_section['read_state'] == 2:
                current_section['content'].append(get_arr(line))
            elif current_section['read_state'] == 3:
                parse_result['tables'][current_section['key']] = current_section
                current_section = None
    parse_result['head']['content']['broker_id'] = title
    return parse_result


def is_section_start_line(line):
    if line.startswith('交易结算单') or line.startswith('交易核算单'):
        return True
    for k in ['资金状况', '成交记录', '交割明细', '平仓明细', '持仓明细', '持仓汇总']:
        reg = f"{k}\s.*"
        if line.startswith(k) and re.match(reg, line):
            return True


def get_section(line):
    if line.startswith('交易结算单') or line.startswith('交易核算单'):
        return {
            'key': '交易结算单',
            'title': line,
            'type': 'head',
            'content': {}
        }
    elif line.startswith('资金状况'):
        return {
            'key': '资金状况',
            'title': line,
            'type': 'account',
            'cols_zh': [],
            'cols_en': [],
            'content': [[]]
        }
    elif any([line.startswith(k) for k in ['成交记录', '交割明细', '平仓明细', '持仓明细', '持仓汇总']]):
        return {
            'key': line[0:4],
            'title': line,
            'type': 'table',
            'cols_zh': [],
            'cols_en': [],
            'content': [],
            'read_state': 0  # 1 开始读表头，2 表示开始读表内容
        }
