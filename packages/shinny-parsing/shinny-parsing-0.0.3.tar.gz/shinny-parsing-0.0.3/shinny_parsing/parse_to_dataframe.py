#!usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'mayanqiong'

from typing import Union, Dict

import pandas as pd


"""
将结算单转为 dataframe 结构
gen_account_df
gen_trade_df
gen_position_df
"""


def table_to_df(user_id, trading_day, account_id, broker_id, table, columns_name_map):
    """将原始构造的表数据转为 dataframe"""
    columns = list(columns_name_map.keys())
    if table is None:
        return pd.DataFrame([], columns=['user_id', 'account_id', 'broker_id', 'trading_day'] + columns)
    else:
        assert all([len(d) == len(table['cols_en']) for d in table['content']]), f'{table["key"]} 数据列和表行列数不相等'
        keys = ['user_id', 'account_id', 'broker_id', 'trading_day']
        index = []
        other_keys = []
        other_values = []  # 结算单可能没有某列，需要手动添加，遇到一个加一个
        for k in columns:
            if isinstance(columns_name_map[k], list):
                # columns_name_map[k] 是一个列表，表示可能在结算单的列名
                for col in columns_name_map[k]:
                    if col in table['cols_en']:
                        keys.append(k)
                        index.append(table['cols_en'].index(col))
                        break
            elif columns_name_map[k] in table['cols_en']:
                keys.append(k)
                index.append(table['cols_en'].index(columns_name_map[k]))
            elif k == "trade_type":
                other_keys.append(k)
                other_values.append('普通成交')
            elif k == 'position_profit':
                # 部分结算单账户资金状况，没有盯市盈亏，只有浮动盈亏，默认为 0
                other_keys.append(k)
                other_values.append(0.0)
            else:
                raise Exception(f"结算单中缺少必要的列 {k}: {columns_name_map[k]}")
        values = [[user_id, account_id, broker_id, trading_day] + [row[i] for i in index] + other_values for row in table['content']]
        keys += other_keys
        data = [dict(zip(keys, val)) for val in values]
        return pd.DataFrame(data, columns=keys)


def gen_trade_df(user_id, trading_day, account_id, broker_id, tables):
    columns_name_map = {
        # 'trade_date': 'Date',  # 成交日期
        'exchange_id': 'Exchange',  # 交易所
        'product_id': 'Product',  # 品种
        'instrument_id': 'Instrument',  # 合约
        'direction': 'B/S',  # 买/卖
        'hedge': 'S/H',  # 投/保
        'price': 'Price',  # 成交价
        'volume': 'Lots',  # 手数
        'amount': 'Turnover',  # 成交额
        'offset': 'O/C',  # 开平
        'commission': 'Fee',  # 手续费
        'close_profit': ['Realized P/L', "Total P/L", "Total  P/L"],  # 平仓盈亏 部分结算单 平仓盈亏 Total P/L （例如 平安期货）
        'premium': 'Premium Received/Paid',  # 权利金收支
        'exchange_trade_id': 'Trans.No.',  # 成交序号
        'trade_type': 'trade type'  # 成交类型
    }
    table = tables.get('成交记录', None)
    df = table_to_df(user_id, trading_day, account_id, broker_id, table, columns_name_map)
    for k in ['price', 'volume', 'amount', 'commission', 'close_profit', 'premium']:
        df[k] = pd.to_numeric(df[k], errors='coerce')
    df['ins_class'] = '期货'
    for i in df.index:
        if df.loc[i, 'product_id'].endswith('期权'):
            df.loc[i, 'ins_class'] = '期权'
    return df


def _append_cols(content: Union[pd.DataFrame, Dict]):
    # 通过成交计算得到的其他字段 exchange_id
    # close_profit commission trade_volumes
    # close_profit_buy_open commission_buy_open trade_volumes_buy_open
    # close_profit_buy_close commission_buy_close trade_volumes_buy_close
    # close_profit_sell_open commission_sell_open trade_volumes_sell_open
    # close_profit_sell_close commission_sell_close trade_volumes_sell_close
    for k in ['commission', 'trade_volumes', 'close_profit']:
        content[k] = 0.0
        for suffix in ['buy_open', 'buy_close', 'sell_open', 'sell_close']:
            content[f"{k}_{suffix}"] = 0.0


def gen_position_df(user_id, trading_day, account_id, broker_id, tables, trades_df=None):
    columns_name_map = {
        'product_id': 'Product',  # 品种
        'instrument_id': 'Instrument',  # 合约
        'pos_long': 'Long Pos.',  # 买持
        'pos_long_avg_price': 'Avg Buy Price',  # 买均价
        'pos_short': 'Short Pos.',  # 卖持
        'pos_short_avg_price': 'Avg Sell Price',  # 卖均价
        'pre_settlement': 'Prev. Sttl',  # 昨结算
        'settlement': 'Sttl Today',  # 今结算
        'position_profit': 'MTM P/L',  # 持仓盯市盈亏
        'margin': 'Margin Occupied',  # 保证金占用
        'hedge': 'S/H',  # 投/保
        'market_value_long': 'Market Value(Long)',  # 多头期权市值
        'market_value_short': 'Market Value(Short)',  # 空头期权市值
    }
    table = tables.get('持仓汇总', None)
    df = table_to_df(user_id, trading_day, account_id, broker_id, table, columns_name_map)
    df['exchange_id'] = ''  # 补充字段
    _append_cols(df)
    if trades_df.shape[0] > 0:
        for k, grouped_df in trades_df.groupby('instrument_id'):
            if any(df['instrument_id'] == k):
                df.loc[df['instrument_id'] == k, ['exchange_id']] = grouped_df.iloc[0]['exchange_id']
                df.loc[df['instrument_id'] == k, ['commission']] = grouped_df['commission'].sum()
                df.loc[df['instrument_id'] == k, ['trade_volumes']] = grouped_df['volume'].sum()
                df.loc[df['instrument_id'] == k, ['close_profit']] = grouped_df['close_profit'].sum()
            else:
                item = {
                    'user_id': user_id,
                    'account_id': account_id,
                    'broker_id': broker_id,
                    'trading_day': trading_day,
                    'exchange_id': grouped_df.iloc[0]['exchange_id'],
                    'instrument_id': k,
                    'product_id': grouped_df.iloc[0]['product_id'],
                    'hedge': grouped_df.iloc[0]['hedge'],
                    'pre_settlement': 0.0,  # 没有这个信息
                    'settlement': 0.0,  # 没有这个信息
                    'pos_long': 0,
                    'pos_short': 0,
                    'pos_long_avg_price': 0.0,
                    'pos_short_avg_price': 0.0,
                    'margin': 0.0,
                    'position_profit': 0.0,
                    'market_value_long': 0.0,
                    'market_value_short': 0.0,
                    'close_profit': grouped_df['close_profit'].sum(),  # 平仓盈亏
                    'commission': grouped_df['commission'].sum(),  # 今日手续费
                    'trade_volumes': grouped_df['volume'].sum()  # 今日成交手数
                }
                _append_cols(item)
                df.loc[df.shape[0]] = item  # pd.DataFrame([item], columns=columns).iloc[0]
            for (dire, offset), dir_grouped_df in grouped_df.groupby(['direction', 'offset']):
                if dire == '买':
                    suffix = 'buy_open' if offset == '开' else 'buy_close'
                else:
                    suffix = 'sell_open' if offset == '开' else 'sell_close'
                df.loc[df['instrument_id'] == k, ['commission_' + suffix]] = grouped_df['commission'].sum()
                df.loc[df['instrument_id'] == k, ['trade_volumes_' + suffix]] = grouped_df['volume'].sum()
                df.loc[df['instrument_id'] == k, ['close_profit_' + suffix]] = grouped_df['close_profit'].sum()
    pos_detail_df = gen_position_detail_df(user_id, trading_day, account_id, broker_id, tables)
    for k, grouped_df in pos_detail_df.groupby(by='instrument_id'):
        df.loc[df['instrument_id'] == k, 'exchange_id'] = grouped_df.iloc[0]['exchange_id']
    df['ins_class'] = '期货'
    for i in df.index:
        if df.loc[i, 'product_id'].endswith('期权'):
            df.loc[i, 'ins_class'] = '期权'
    return df


def gen_close_position_df(user_id, trading_day, account_id, broker_id, tables):
    columns_name_map = {
        'close_date': 'Close Date',  # 平仓日期
        'exchange_id': 'Exchange',  # 交易所
        'product_id': 'Product',  # 品种
        'instrument_id': 'Instrument',  # 合约
        'open_date': 'Open Date',  # 开仓日期
        'directions': 'B/S',  # 买/卖
        'volume': 'Lots',  # 手数
        'open_price': 'Pos. Open Price',  # 开仓价
        'pre_settlement': 'Prev. Sttl',  # 昨结算
        'price': 'Trans. Price',  # 成交价
        'close_profit': ['Realized P/L', "Total P/L", "Total  P/L"],  # 平仓盈亏
        'premium': 'Premium Received/Paid',  # 权利金收支
        'trade_type': 'trade type',  # 成交类型
    }
    table = tables.get('平仓明细', None)
    df = table_to_df(user_id, trading_day, account_id, broker_id, table, columns_name_map)
    for k in ['volume', 'open_price', 'pre_settlement', 'price', 'close_profit', 'premium', 'trade_type']:
        df[k] = pd.to_numeric(df[k], errors='coerce')
    return df


def gen_position_detail_df(user_id, trading_day, account_id, broker_id, tables):
    columns_name_map = {
        'exchange_id': 'Exchange',  # 交易所
        'product_id': 'Product',  # 品种
        'instrument_id': 'Instrument',  # 合约
        'open_date': 'Open Date',  # 开仓日期
        'hedge': 'S/H',  # 投/保
        'direction': 'B/S',  # 买/卖
        'pos': 'Positon',  # 持仓量
        'open_price': 'Pos. Open Price',  # 开仓价
        'pre_settlement': 'Prev. Sttl',  # 昨结算
        'settlement': 'Settlement Price',  # 结算价
        'float_profit': 'Accum. P/L',  # 浮动盈亏
        'position_profit': 'MTM P/L',  # 盯市盈亏
        'margin': 'Margin',  # 保证金
        'market_value': 'Market Value(Options)',  # 期权市值
    }
    table = tables.get('持仓明细', None)
    df = table_to_df(user_id, trading_day, account_id, broker_id, table, columns_name_map)
    for k in ['pos', 'open_price', 'pre_settlement', 'settlement', 'float_profit', 'position_profit', 'margin', 'market_value']:
        df[k] = pd.to_numeric(df[k], errors='coerce')
    return df


def gen_account_df(user_id, trading_day, account_id, broker_id, tables):
    columns_name_map = {
        'pre_balance': ['Balance b/f', 'Balance B/F'],  # 期初结存 （Balance B/F 长江期货）
        'transfer': 'Deposit/Withdrawal',  # 出入金
        'balance': ['Balance c/f', 'Balance C/F'],  # 期末结存
        'close_profit': 'Realized P/L',  # 平仓盈亏
        'position_profit': 'MTM P/L',  # 持仓盯市盈亏
        'exercise_profit': 'Exercise P/L',  # 期权执行盈亏
        'commission': 'Commission',  # 手 续 费
        'margin': 'Margin Occupied',  # 保证金占用
        'market_value_long': ['Market value(long)', 'Market Value(long)'],  # 多头期权市值
        'market_value_short': ['Market value(short)', 'Market Value(short)'],  # 空头期权市值
        'market_value': ['Market value(equity)', 'Market Value(equity)'],  # 市值权益
        'premium_received': ['Premium received', 'Premium Received'],  # 权利金收入
        'premium_paid': ['Premium paid', 'Premium Paid'],  # 权利金支出
        # 'delivery_margin': 'Delivery Margin',  # 交割保证金
        # 'exercise_commission': 'Exercise Fee',  # 行权手续费
        # 'delivery_commission': 'Delivery Fee',  # 交割手续费
        # '': 'Initial Margin',  # 基础保证金
        # '': 'Pledge Amount',  # 质 押 金
        # '': 'Client Equity',  # 客户权益
        # '': 'FX Pledge Occ.',  # 货币质押保证金占用
        # '': 'New FX Pledge',  # 货币质入
        # '': 'FX Redemption',  # 货币质出
        # '': 'Chg in Pledge Amt',  # 质押变化金额
        # '': 'Fund Avail.',  # 可用资金
        # '': 'Risk Degree',  # 风 险 度
        # '': 'Margin Call',  # 应追加资金
        # '': 'Chg in FX Pledge'  # 货币质押变化金额
    }
    table = tables.get('资金状况', None)
    df = table_to_df(user_id, trading_day, account_id, broker_id, table, columns_name_map)
    df['currency'] = 'CNY'  # 币种 默认都是 CNY
    for k in columns_name_map.keys():
        df[k] = pd.to_numeric(df[k], errors='coerce')
    df['premium'] = df['premium_received'] - df['premium_paid']
    return df