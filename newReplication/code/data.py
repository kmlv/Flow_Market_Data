from common import *
from helpers import *
from config import *
import sys

data_directory = code_dir + os.sep

required_files= [
    'data_interval.csv', 
    'data_period.csv', 
    'data_second.csv', 
    'data_profits.csv', 
    'data_liquidity.csv', 

]

def abs_flat(list):
    res = [abs(item) for sublist in list for item in sublist 
        if not np.isnan(item) 
        and item != 0
        ]
    return res

def flat(list):
    res = [item for sublist in list for item in sublist 
        if not np.isnan(item) 
        and item != 0
        ]
    return res

def getFirstHalf(full, lastHalf):
    res = full
    for i in lastHalf:
        res.remove(i)
    return res

def calculate_diff(group):
    return group.iloc[0] - group.iloc[-1]

# round all floats to 2 decimals
def remove_paren(s, dec):
    if isinstance(s, list):
        return '[{}, {}]'.format(str(round(s[0], dec)), str(round(s[1], dec)))
    elif isinstance(s, str) and s and s[0] == '(' and s[-1] == ')':
        return '(' + str(round(float(s[1:-1]))) + ')' if dec == 0 else '(' + str(round(float(s[1:-1]), dec)) + ')'
    else:
        return s

from config import *

def main():
    print("params imported")

if __name__ == "__main__":
    main()

print('liquidity')
exec(open(data_directory + 'liquidity_cda.py').read())
exec(open(data_directory + 'liquidity_flow.py').read())

regress_data_liquidity = pd.concat([liquidity_cda_period[['period', 'format', 'block', 'group', 'interval', 'ppi']], liquidity_flow_period[['period', 'format', 'block', 'group', 'interval', 'ppi']]], ignore_index=True)
regress_data_liquidity['group_id'] = regress_data_liquidity['group']
regress_data_liquidity['group'] = regress_data_liquidity['format'] + regress_data_liquidity['group'].astype(str)
regress_data_liquidity = regress_data_liquidity.drop('format', axis=1)


liquidity = [
    ['PPI',
    liquidity_cda_period[liquidity_cda_period['format'] == 'CDA']['liquidity'].mean(), 
    liquidity_flow_period[(liquidity_flow_period['format'] == 'FLOW') & (liquidity_flow_period['group'] <= num_flow30)]['liquidity'].mean(),
    liquidity_flow_period[(liquidity_flow_period['format'] == 'FLOW') & (liquidity_flow_period['group'] > num_flow30)]['liquidity'].mean(),
    liquidity_cda_period[(liquidity_cda_period['format'] == 'CDA') & (liquidity_cda_period['period'] > (num_periods - prac_periods) // 2)]['liquidity'].mean(), 
    liquidity_flow_period[(liquidity_flow_period['format'] == 'FLOW') & (liquidity_flow_period['period'] > (num_periods - prac_periods) // 2) & (liquidity_flow_period['group'] <= num_flow30)]['liquidity'].mean(),
    liquidity_flow_period[(liquidity_flow_period['format'] == 'FLOW') & (liquidity_flow_period['period'] > (num_periods - prac_periods) // 2) & (liquidity_flow_period['group'] > num_flow30)]['liquidity'].mean()],
]

liquidity_all20 = [
    ['PPI',
    liquidity_cda_period[liquidity_cda_period['format'] == 'CDA']['liquidity'].mean(), 
    liquidity_flow_period[(liquidity_flow_period['format'] == 'FLOW') & (liquidity_flow_period['group'] <= num_flow30)]['liquidity'].mean(),
    liquidity_flow_period[(liquidity_flow_period['format'] == 'FLOW') & (liquidity_flow_period['group'] > num_flow30)]['liquidity'].mean(),
    liquidity_cda_period[(liquidity_cda_period['format'] == 'CDA') & (liquidity_cda_period['period'] <= (num_periods - prac_periods) // 2)]['liquidity'].mean(), 
    liquidity_flow_period[(liquidity_flow_period['format'] == 'FLOW') & (liquidity_flow_period['period'] <= (num_periods - prac_periods) // 2) & (liquidity_flow_period['group'] <= num_flow30)]['liquidity'].mean(),
    liquidity_flow_period[(liquidity_flow_period['format'] == 'FLOW') & (liquidity_flow_period['period'] <= (num_periods - prac_periods) // 2) & (liquidity_flow_period['group'] > num_flow30)]['liquidity'].mean(),
    liquidity_cda_period[(liquidity_cda_period['format'] == 'CDA') & (liquidity_cda_period['period'] > (num_periods - prac_periods) // 2)]['liquidity'].mean(), 
    liquidity_flow_period[(liquidity_flow_period['format'] == 'FLOW') & (liquidity_flow_period['period'] > (num_periods - prac_periods) // 2) & (liquidity_flow_period['group'] <= num_flow30)]['liquidity'].mean(),
    liquidity_flow_period[(liquidity_flow_period['format'] == 'FLOW') & (liquidity_flow_period['period'] > (num_periods - prac_periods) // 2) & (liquidity_flow_period['group'] > num_flow30)]['liquidity'].mean()],
]

for i, sublist in enumerate(liquidity):
    for j, element in enumerate(sublist):
        if isinstance(element, float):
            liquidity[i][j] = round(element, 2)

print('FLOW trader/period')
exec(open(data_directory + 'flow_trader_period.py').read())

print('CDA RESULTS')
exec(open(data_directory + 'cda.py').read())

print('FLOW RESULTS')
exec(open(data_directory + 'flow.py').read())

print('CDA INDIVIDUAL RESULTS')
exec(open(data_directory + 'cda_individual.py').read())

print('FLOW INDIVIDUAL RESULTS')
exec(open(data_directory + 'flow_individual.py').read())

if price_interval_size == 5:
    exec(open(data_directory + 'new_plots.py').read())

# temp
check_negative_flow = list(filter(lambda x: x < 0, profits_buy_flow30_ind_all20 + profits_sell_flow30_ind_all20 + profits_buy_flow60_ind_all20 + profits_sell_flow60_ind_all20))
check_negative_cda = list(filter(lambda x: x < 0, profits_buy_cda_ind_all20 + profits_sell_cda_ind_all20))
print(
    'overall negative end-of-period profits count: ', round((len(check_negative_flow) + len(check_negative_cda)) / len(profits_buy_cda_ind_all20 + profits_sell_cda_ind_all20 + profits_buy_flow30_ind_all20 + profits_sell_flow30_ind_all20 + profits_buy_flow60_ind_all20 + profits_sell_flow60_ind_all20), 4), 
    '\nCDA negative end-of-period profits count: ', round(len(check_negative_cda) / len(profits_buy_cda_ind_all20 + profits_sell_cda_ind_all20), 4),
    '\nFLOW negative end-of-period profits count: ', round(len(check_negative_flow) / len(profits_buy_flow30_ind_all20 + profits_sell_flow30_ind_all20 + profits_buy_flow60_ind_all20 + profits_sell_flow60_ind_all20), 4),
)

# create data frames for regressions 
regress_data_direction = pd.concat([regress_cda_ind, regress_flow_ind], ignore_index=True)

regress_data_direction.to_csv(os.path.join(intermediate_dir, 'regress_data_direction.csv'), index=False)

regress_data_profits = regress_data_direction.groupby(['format', 'period', 'group',]).apply(lambda x: pd.Series({
    'gross_profits': x['cash'].sum(),
    'gross_norm_diff': calculate_diff(x['gross_profits_norm']),
    'total_ce_profit': x['ce_profit'].sum(),
    'overall_order_num': x['order_num'].sum(),
    'overall_order_price_low': x['order_price_low'].mean(), # simple avg between buy and sell
    'overall_order_price_high':  x['order_price_high'].mean(),
    'overall_order_quantity': x['order_quantity'].mean(),
    'overall_order_rate': x['order_rate'].mean(),
    'overall_order_price_low_initial': x['order_price_low_initial'].mean(), 
    'overall_order_price_high_initial': x['order_price_high_initial'].mean(),
    'overall_order_quantity_initial': x['order_quantity_initial'].mean(),
    'overall_order_rate_initial': x['order_rate_initial'].mean(),
    'max_quantity/rate_orders_buy': x['max_quantity/rate_orders_buy'].mean(), 
    'max_quantity/rate_orders_sell': x['max_quantity/rate_orders_sell'].mean(), 
    '%no_trans': x['no_trans'].mean() / round_length, 
})).reset_index()
regress_data_profits['max_quantity/rate_orders'] = regress_data_profits['max_quantity/rate_orders_buy'] + regress_data_profits['max_quantity/rate_orders_sell']
regress_buy = regress_data_direction[regress_data_direction['direction'] == 'buy'][['format', 'period', 'group', 'cash', 'ce_profit', 'order_num', 'order_price_low', 'order_price_high', 'order_quantity', 'order_rate', 'order_price_low_initial', 'order_price_high_initial', 'order_quantity_initial', 'order_rate_initial']]
regress_sell = regress_data_direction[regress_data_direction['direction'] == 'sell'][['format', 'period', 'group', 'cash', 'ce_profit', 'order_num', 'order_price_low', 'order_price_high', 'order_quantity', 'order_rate', 'order_price_low_initial', 'order_price_high_initial', 'order_quantity_initial', 'order_rate_initial']]
regress_data_profits = pd.merge(regress_data_profits, regress_buy, on=['format', 'period', 'group'], how='left')
regress_data_profits.rename(columns={'cash': 'buyer_profit', 'ce_profit': 'buyer_ce_profit', 'order_num': 'buyer_order_num', 'order_price_low': 'buyer_order_price_low', 'order_price_high': 'buyer_order_price_high', 'order_quantity': 'buyer_order_quantity', 'order_rate': 'buyer_order_rate', 'order_price_low_initial': 'buyer_order_price_low_initial', 'order_price_high_initial': 'buyer_order_price_high_initial', 'order_quantity_initial': 'buyer_order_quantity_initial', 'order_rate_initial': 'buyer_order_rate_initial'}, inplace=True)
regress_data_profits = pd.merge(regress_data_profits, regress_sell, on=['format', 'period', 'group'], how='left')
regress_data_profits.rename(columns={'cash': 'seller_profit', 'ce_profit': 'seller_ce_profit', 'order_num': 'seller_order_num', 'order_price_low': 'seller_order_price_low', 'order_price_high': 'seller_order_price_high', 'order_quantity': 'seller_order_quantity', 'order_rate': 'seller_order_rate', 'order_price_low_initial': 'seller_order_price_low_initial', 'order_price_high_initial': 'seller_order_price_high_initial', 'order_quantity_initial': 'seller_order_quantity_initial', 'order_rate_initial': 'seller_order_rate_initial'}, inplace=True)
regress_data_profits['%max_quantity/rate_orders_buy'] = regress_data_profits['max_quantity/rate_orders_buy'] / regress_data_profits['buyer_order_num']
regress_data_profits['%max_quantity/rate_orders_sell'] = regress_data_profits['max_quantity/rate_orders_sell'] / regress_data_profits['seller_order_num']
regress_data_profits['%max_quantity/rate_orders'] = regress_data_profits[['%max_quantity/rate_orders_buy', '%max_quantity/rate_orders_sell']].mean(axis=1) # simple avg
regress_data_profits['group_id'] = regress_data_profits['group']
regress_data_profits['group'] = regress_data_profits['format'] + regress_data_profits['group'].astype(str)
regress_data_profits['block'] = regress_data_profits['period'] // ((num_periods - prac_periods) // blocks) + (regress_data_profits['period'] % ((num_periods - prac_periods) // blocks) != 0)
regress_data_profits['seller_realized_surplus'] = regress_data_profits['seller_profit'] / regress_data_profits['seller_ce_profit']
regress_data_profits['buyer_realized_surplus'] = regress_data_profits['buyer_profit'] / regress_data_profits['buyer_ce_profit']
regress_data_profits.rename(columns={'cash': 'profits'})

# df for each 5-second time interval
regress_data_interval = pd.concat([regress_cda, regress_flow], ignore_index=True)
interval_dummies = pd.get_dummies(regress_data_interval['block'], prefix='block')
regress_data_interval = regress_data_interval.join(interval_dummies)
regress_data_interval['group_id'] = regress_data_interval['group']
regress_data_interval['group'] = regress_data_interval['format'] + regress_data_interval['group'].astype(str)
categorical_cols = ['format']
regress_data_interval[categorical_cols] = regress_data_interval[categorical_cols].astype('category')
format_mapping = {'CDA': 0, 'Flow30': 1, 'Flow60': 2}
regress_data_interval['format_num'] = regress_data_interval['format'].map(format_mapping)
regress_data_interval['price_deviation_log'] = np.log(np.where(regress_data_interval['price_deviation'] == 0, 0.001, regress_data_interval['price_deviation']))
regress_data_interval['price_change_log'] = np.log(np.abs(np.where(regress_data_interval['price_change'] == 0, 0.001, regress_data_interval['price_change'])))
regress_data_interval['log_wprice'] = np.log(regress_data_interval['weighted_price'])
regress_data_interval['change_log_wprice'] = regress_data_interval.groupby(['format', 'group', 'period'])['log_wprice'].diff()

# add ppi
regress_data_interval = regress_data_interval.merge(regress_data_liquidity, on=['period', 'block', 'group', 'interval', 'group_id'], how='left')

interval_std = regress_data_interval.groupby(['format', 'group', 'period', 'group_id'], observed=True)['change_log_wprice'].std() # new price volatility measure


# df for each second
regress_data_second = pd.concat([regress_cda_second, regress_flow_second], ignore_index=True)
second_dummies = pd.get_dummies(regress_data_second['block'], prefix='block')
regress_data_second = regress_data_second.join(second_dummies)
regress_data_second['group_id'] = regress_data_second['group']
regress_data_second['group'] = regress_data_second['format'] + regress_data_second['group'].astype(str)
regress_data_second['format_num'] = regress_data_second['format'].map(format_mapping)
regress_data_second['log_price'] = np.log(regress_data_second['clearing_price'])
regress_data_second['change_log_price'] = regress_data_second.groupby(['format', 'group', 'period'])['log_price'].diff()
regress_data_second['price_change'] = regress_data_second.groupby(['format', 'group', 'period'])['clearing_price'].diff()
regress_data_second['price_deviation'] = regress_data_second['clearing_price'] - regress_data_second['ce_price']

second_std = regress_data_second.groupby(['format', 'group', 'period'])['change_log_price'].std() # new price volatility measure


# df for each period/period

regress_data_period = pd.concat([regress_cda_period, regress_flow_period], ignore_index=True)
period_dummies = pd.get_dummies(regress_data_period['block'], prefix='block')
regress_data_period = regress_data_period.join(period_dummies)
regress_data_period['group_id'] = regress_data_period['group']
regress_data_period['group'] = regress_data_period['format'] + regress_data_period['group'].astype(str)
regress_data_period[categorical_cols] = regress_data_period[categorical_cols].astype('category')
regress_data_period['format_num'] = regress_data_period['format'].map(format_mapping)
# regress_data_period['test'] = (regress_data_period['period'] - (num_periods - prac_periods)) * regress_data_period['format_num']
# regress_data_period['test_new'] = (1 - regress_data_period['period'] / (num_periods - prac_periods)) * regress_data_period['format_num']
regress_data_period['realized_surplus_percent'] = 100 * regress_data_period['realized_surplus']
regress_data_period['filled_contract_percent'] = 100 * regress_data_period['filled_contract']
regress_data_period = regress_data_period.merge(interval_std,  on = ['format', 'period', 'group'], how='left')
regress_data_period = regress_data_period.merge(second_std, on = ['format', 'period', 'group'], how='left')
regress_data_period['Traded/CE Quantity'] = regress_data_period['traded_volume'] / regress_data_period['ce_quantity']
regress_data_period = pd.merge(regress_data_period, regress_data_profits,  on=['format', 'period', 'group', 'block'], how='left')
regress_data_period['order_size'] = 2 * regress_data_period['traded_volume'] / regress_data_period['overall_order_num']
regress_data_period['gross_diff'] = (regress_data_period['buyer_profit'] - regress_data_period['buyer_ce_profit']) - (regress_data_period['seller_profit'] - regress_data_period['seller_ce_profit'])

regress_data_interval.to_csv(os.path.join(intermediate_dir, 'data_interval.csv'), index=False)
regress_data_period.to_csv(os.path.join(intermediate_dir, 'data_period.csv'), index=False)
regress_data_second.to_csv(os.path.join(intermediate_dir, 'data_second.csv'), index=False)
regress_data_profits.to_csv(os.path.join(intermediate_dir, 'data_profits.csv'), index=False)
regress_data_liquidity.to_csv(os.path.join(intermediate_dir, 'data_liquidity.csv'), index=False)


### use raw prices from each second
print("unweighted price statistics", 
    '\nAverage Price & {} & {} & {} & {} & {} & {} & {} & {} & {}'.format(
    regress_data_second[(regress_data_second['format'] == 'CDA')]['clearing_price'].mean().round(2),
    regress_data_second[(regress_data_second['format'] == 'Flow30')]['clearing_price'].mean().round(2),
    regress_data_second[(regress_data_second['format'] == 'Flow60')]['clearing_price'].mean().round(2),
    regress_data_second[(regress_data_second['period'] <= (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'CDA')]['clearing_price'].mean().round(2),
    regress_data_second[(regress_data_second['period'] <= (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'Flow30')]['clearing_price'].mean().round(2),
    regress_data_second[(regress_data_second['period'] <= (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'Flow60')]['clearing_price'].mean().round(2),
    regress_data_second[(regress_data_second['period'] > (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'CDA')]['clearing_price'].mean().round(2),
    regress_data_second[(regress_data_second['period'] > (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'Flow30')]['clearing_price'].mean().round(2),
    regress_data_second[(regress_data_second['period'] > (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'Flow60')]['clearing_price'].mean().round(2),
    ),
    '\n|Price - P_CE| & {} & {} & {} & {} & {} & {} & {} & {} & {}'.format(
    regress_data_second[(regress_data_second['format'] == 'CDA')]['price_deviation'].mean().round(2),
    regress_data_second[(regress_data_second['format'] == 'Flow30')]['price_deviation'].mean().round(2),
    regress_data_second[(regress_data_second['format'] == 'Flow60')]['price_deviation'].mean().round(2),
    regress_data_second[(regress_data_second['period'] <= (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'CDA')]['price_deviation'].mean().round(2),
    regress_data_second[(regress_data_second['period'] <= (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'Flow30')]['price_deviation'].mean().round(2),
    regress_data_second[(regress_data_second['period'] <= (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'Flow60')]['price_deviation'].mean().round(2),
    regress_data_second[(regress_data_second['period'] > (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'CDA')]['price_deviation'].mean().round(2),
    regress_data_second[(regress_data_second['period'] > (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'Flow30')]['price_deviation'].mean().round(2),
    regress_data_second[(regress_data_second['period'] > (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'Flow60')]['price_deviation'].mean().round(2),
    ),
    '\n|P_t - P_t - 1| & {} & {} & {} & {} & {} & {} & {} & {} & {}'.format(
    abs(regress_data_second[(regress_data_second['format'] == 'CDA')]['price_change']).mean().round(2),
    abs(regress_data_second[(regress_data_second['format'] == 'Flow30')]['price_change']).mean().round(2),
    abs(regress_data_second[(regress_data_second['format'] == 'Flow60')]['price_change']).mean().round(2),
    abs(regress_data_second[(regress_data_second['period'] <= (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'CDA')]['price_change']).mean().round(2),
    abs(regress_data_second[(regress_data_second['period'] <= (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'Flow30')]['price_change']).mean().round(2),
    abs(regress_data_second[(regress_data_second['period'] <= (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'Flow60')]['price_change']).mean().round(2),
    abs(regress_data_second[(regress_data_second['period'] > (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'CDA')]['price_change']).mean().round(2),
    abs(regress_data_second[(regress_data_second['period'] > (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'Flow30')]['price_change']).mean().round(2),
    abs(regress_data_second[(regress_data_second['period'] > (num_periods - prac_periods) // 2) & (regress_data_second['format'] == 'Flow60')]['price_change']).mean().round(2),
    ),
    '\nStd(ln P_t - ln P_t - 1) & {} & {} & {} & {} & {} & {} & {} & {} & {}'.format(
    regress_data_period[(regress_data_period['format'] == 'CDA')]['change_log_price'].mean().round(2),
    regress_data_period[(regress_data_period['format'] == 'Flow30')]['change_log_price'].mean().round(2),
    regress_data_period[(regress_data_period['format'] == 'Flow60')]['change_log_price'].mean().round(2),
    regress_data_period[(regress_data_period['period'] <= (num_periods - prac_periods) // 2) & (regress_data_period['format'] == 'CDA')]['change_log_price'].mean().round(2),
    regress_data_period[(regress_data_period['period'] <= (num_periods - prac_periods) // 2) & (regress_data_period['format'] == 'Flow30')]['change_log_price'].mean().round(2),
    regress_data_period[(regress_data_period['period'] <= (num_periods - prac_periods) // 2) & (regress_data_period['format'] == 'Flow60')]['change_log_price'].mean().round(2),
    regress_data_period[(regress_data_period['period'] > (num_periods - prac_periods) // 2) & (regress_data_period['format'] == 'CDA')]['change_log_price'].mean().round(2),
    regress_data_period[(regress_data_period['period'] > (num_periods - prac_periods) // 2) & (regress_data_period['format'] == 'Flow30')]['change_log_price'].mean().round(2),
    regress_data_period[(regress_data_period['period'] > (num_periods - prac_periods) // 2) & (regress_data_period['format'] == 'Flow60')]['change_log_price'].mean().round(2),
    )
)

# Save Table S8 (unweighted price statistics) to .tex
_half = (num_periods - prac_periods) // 2
_s8_rows = []
_s8_rows.append(['Average Price'] + [
    regress_data_second[regress_data_second['format'] == f]['clearing_price'].mean().round(2)
    for f in ['CDA', 'Flow30', 'Flow60']] + [
    regress_data_second[(regress_data_second['period'] <= _half) & (regress_data_second['format'] == f)]['clearing_price'].mean().round(2)
    for f in ['CDA', 'Flow30', 'Flow60']] + [
    regress_data_second[(regress_data_second['period'] > _half) & (regress_data_second['format'] == f)]['clearing_price'].mean().round(2)
    for f in ['CDA', 'Flow30', 'Flow60']])
_s8_rows.append(['$|P_t - P_{CE}|$'] + [
    regress_data_second[regress_data_second['format'] == f]['price_deviation'].mean().round(2)
    for f in ['CDA', 'Flow30', 'Flow60']] + [
    regress_data_second[(regress_data_second['period'] <= _half) & (regress_data_second['format'] == f)]['price_deviation'].mean().round(2)
    for f in ['CDA', 'Flow30', 'Flow60']] + [
    regress_data_second[(regress_data_second['period'] > _half) & (regress_data_second['format'] == f)]['price_deviation'].mean().round(2)
    for f in ['CDA', 'Flow30', 'Flow60']])
_s8_rows.append(['$|P_t - P_{t-1}|$'] + [
    abs(regress_data_second[regress_data_second['format'] == f]['price_change']).mean().round(2)
    for f in ['CDA', 'Flow30', 'Flow60']] + [
    abs(regress_data_second[(regress_data_second['period'] <= _half) & (regress_data_second['format'] == f)]['price_change']).mean().round(2)
    for f in ['CDA', 'Flow30', 'Flow60']] + [
    abs(regress_data_second[(regress_data_second['period'] > _half) & (regress_data_second['format'] == f)]['price_change']).mean().round(2)
    for f in ['CDA', 'Flow30', 'Flow60']])
_s8_rows.append([r'Std$(\ln P_t - \ln P_{t-1})$'] + [
    regress_data_period[regress_data_period['format'] == f]['change_log_price'].mean().round(2)
    for f in ['CDA', 'Flow30', 'Flow60']] + [
    regress_data_period[(regress_data_period['period'] <= _half) & (regress_data_period['format'] == f)]['change_log_price'].mean().round(2)
    for f in ['CDA', 'Flow30', 'Flow60']] + [
    regress_data_period[(regress_data_period['period'] > _half) & (regress_data_period['format'] == f)]['change_log_price'].mean().round(2)
    for f in ['CDA', 'Flow30', 'Flow60']])

_s8_tex = r"""\begin{table}[!htbp] \centering
\caption{Summary Statistics with Unweighted Prices}
\begin{tabular}{@{\extracolsep{5pt}}lccccccccc}
\\[-1.8ex]\hline
\hline \\[-1.8ex]
 & \multicolumn{3}{c}{All Periods (T1--T20)} & \multicolumn{3}{c}{First Half (T1--T10)} & \multicolumn{3}{c}{Second Half (T11--T20)} \\
 & CDA & Flow30 & Flow60 & CDA & Flow30 & Flow60 & CDA & Flow30 & Flow60 \\
\hline \\[-1.8ex]
"""
for row in _s8_rows:
    _s8_tex += ' {} & {} \\\\\n'.format(row[0], ' & '.join(str(v) for v in row[1:]))
_s8_tex += r"""\hline
\hline \\[-1.8ex]
\end{tabular}
\end{table}"""

if price_interval_size == 5:
    with open(os.path.join(tables_dir, 'TableS8_Unweighted_Prices.tex'), 'w') as f:
        f.write(_s8_tex)
    print('Table S8 saved to TableS8_Unweighted_Prices.tex')


summary_market_all20 = [
    [None, 'CDA', 'Flow30', 'Flow60', 'CDA', 'Flow30', 'FLOw_H', 'CDA', 'Flow30', 'Flow60', ], 
    [None, 'T1 - T20', 'T1 - T20', 'T1 - T20', 'T1 - T10', 'T1 - T10', 'T1 - T10', 'T11 - T20', 'T11 - T20', 'T11 - T20', ], 
    ['Clearing Price', 
        regress_data_interval[(regress_data_interval['format'] == 'CDA')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['format'] == 'Flow30')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['format'] == 'Flow60')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['period'] <= (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'CDA')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['period'] <= (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow30')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['period'] <= (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow60')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'CDA')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow30')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow60')]['weighted_price'].mean(),
    ],
    ['Std. Dev.', 
        '({})'.format(regress_data_interval[(regress_data_interval['format'] == 'CDA')]['weighted_price'].std()), 
        '({})'.format(regress_data_interval[(regress_data_interval['format'] == 'Flow30')]['weighted_price'].std()),
        '({})'.format(regress_data_interval[(regress_data_interval['format'] == 'Flow60')]['weighted_price'].std()),
        '({})'.format(regress_data_interval[(regress_data_interval['period'] <= (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'CDA')]['weighted_price'].std()), 
        '({})'.format(regress_data_interval[(regress_data_interval['period'] <= (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow30')]['weighted_price'].std()), 
        '({})'.format(regress_data_interval[(regress_data_interval['period'] <= (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow60')]['weighted_price'].std()),
        '({})'.format(regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'CDA')]['weighted_price'].std()), 
        '({})'.format(regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow30')]['weighted_price'].std()),
        '({})'.format(regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow60')]['weighted_price'].std()),
    ], 
    ['|P_{t} - P_{t - 1}|', 
        regress_data_interval[(regress_data_interval['format'] == 'CDA')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['format'] == 'Flow30')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['format'] == 'Flow60')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['period'] <= (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'CDA')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['period'] <= (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow30')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['period'] <= (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow60')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'CDA')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow30')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow60')]['price_change'].abs().mean(),
        ], 
    [r'Std. Dev. of (\ln P_{t} - \ln P_{t - 1})', 
        regress_data_period[regress_data_period['format'] == 'CDA']['change_log_wprice'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['change_log_wprice'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['change_log_wprice'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['change_log_wprice'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['change_log_wprice'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['change_log_wprice'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['change_log_wprice'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['change_log_wprice'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['change_log_wprice'].mean(),
        ],
    ['PPI',
        liquidity_cda_period[liquidity_cda_period['format'] == 'CDA']['ppi'].mean(), 
        liquidity_flow_period[(liquidity_flow_period['format'] == 'Flow30')]['ppi'].mean(),
        liquidity_flow_period[(liquidity_flow_period['format'] == 'Flow60')]['ppi'].mean(),
        liquidity_cda_period[(liquidity_cda_period['format'] == 'CDA') & (liquidity_cda_period['period'] <= (num_periods - prac_periods) // 2)]['ppi'].mean(), 
        liquidity_flow_period[(liquidity_flow_period['format'] == 'Flow30') & (liquidity_flow_period['period'] <= (num_periods - prac_periods) // 2)]['ppi'].mean(),
        liquidity_flow_period[(liquidity_flow_period['format'] == 'Flow60') & (liquidity_flow_period['period'] <= (num_periods - prac_periods) // 2)]['ppi'].mean(),
        liquidity_cda_period[(liquidity_cda_period['format'] == 'CDA') & (liquidity_cda_period['period'] > (num_periods - prac_periods) // 2)]['ppi'].mean(), 
        liquidity_flow_period[(liquidity_flow_period['format'] == 'Flow30') & (liquidity_flow_period['period'] > (num_periods - prac_periods) // 2)]['ppi'].mean(),
        liquidity_flow_period[(liquidity_flow_period['format'] == 'Flow60') & (liquidity_flow_period['period'] > (num_periods - prac_periods) // 2)]['ppi'].mean(), 
        ],
    ['Traded Volume (shares)', 
        regress_data_period[regress_data_period['format'] == 'CDA']['traded_volume'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow30']['traded_volume'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['traded_volume'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['traded_volume'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['traded_volume'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['traded_volume'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['traded_volume'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['traded_volume'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['traded_volume'].mean(),
        ],  
    [r'Traded Vol. /Q\_{CE} (%)', 
        100 * regress_data_period[regress_data_period['format'] == 'CDA']['Traded/CE Quantity'].mean(), 
        100 * regress_data_period[regress_data_period['format'] == 'Flow30']['Traded/CE Quantity'].mean(),
        100 * regress_data_period[regress_data_period['format'] == 'Flow60']['Traded/CE Quantity'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['Traded/CE Quantity'].mean(), 
        100 * regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['Traded/CE Quantity'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['Traded/CE Quantity'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['Traded/CE Quantity'].mean(), 
        100 * regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['Traded/CE Quantity'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['Traded/CE Quantity'].mean(),
        ],
    [r'Filled Contract / Q\_{CE} (%)', 
        100 * regress_data_period[regress_data_period['format'] == 'CDA']['filled_contract'].mean(),
        100 * regress_data_period[regress_data_period['format'] == 'Flow30']['filled_contract'].mean(),
        100 * regress_data_period[regress_data_period['format'] == 'Flow60']['filled_contract'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['filled_contract'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['filled_contract'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['filled_contract'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['filled_contract'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['filled_contract'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['filled_contract'].mean(),
        ],
    ['Num. of Transactions', 
        int(statistics.mean(transaction_number_cda_all20)), None, None,
        int(statistics.mean(transaction_number_cda_first10)), None, None,
        int(statistics.mean(transaction_number_cda_last10)), None, None,
        ],
    ['Mean Transaction Size', 
        int(statistics.mean(volume_volatility_cda_all20)), None, None,
        int(statistics.mean(volume_volatility_cda_first10)), None, None,
        int(statistics.mean(volume_volatility_cda_last10)), None, None,
        ],
    ['Std. Dev.', 
        '({})'.format(statistics.stdev(volume_volatility_cda_all20)), None, None,
        '({})'.format(statistics.stdev(volume_volatility_cda_first10)), None, None,
        '({})'.format(statistics.stdev(volume_volatility_cda_last10)), None, None,
        ],
    ['Clearing Rate', 
        None, statistics.mean(clearing_rate_flow30_all20), statistics.mean(clearing_rate_flow60_all20),
        None, statistics.mean(clearing_rate_flow30_first10), statistics.mean(clearing_rate_flow60_first10),
        None, statistics.mean(clearing_rate_flow30_last10), statistics.mean(clearing_rate_flow60_last10),
       ], 
    ['Std. Dev.', 
        None, '({})'.format(statistics.stdev(clearing_rate_flow30_all20)), '({})'.format(statistics.stdev(clearing_rate_flow60_all20)),
        None, '({})'.format(statistics.stdev(clearing_rate_flow30_first10)), '({})'.format(statistics.stdev(clearing_rate_flow60_first10)),
        None, '({})'.format(statistics.stdev(clearing_rate_flow30_last10)), '({})'.format(statistics.stdev(clearing_rate_flow60_last10)),
        ], 
    ['Time with no FLOW Trans (%)',
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['%no_trans'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['%no_trans'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['%no_trans'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['%no_trans'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%no_trans'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%no_trans'].mean(),
    ],
    ['Info. Effic.: |Price - P_{CE}|', 
        regress_data_interval[(regress_data_interval['format'] == 'CDA')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['format'] == 'Flow30')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['format'] == 'Flow60')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['period'] <= (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'CDA')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['period'] <= (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow30')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['period'] <= (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow60')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'CDA')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow30')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow60')]['price_deviation'].mean(),
        ], 
    [r'Alloc. Effic.: \Pi / \Pi_{CE} (x100)', 
        100 * regress_data_period[regress_data_period['format'] == 'CDA']['realized_surplus'].mean(),
        100 * regress_data_period[regress_data_period['format'] == 'Flow30']['realized_surplus'].mean(),
        100 * regress_data_period[regress_data_period['format'] == 'Flow60']['realized_surplus'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['realized_surplus'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['realized_surplus'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['realized_surplus'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['realized_surplus'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['realized_surplus'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['realized_surplus'].mean(),
        ],
    [r'\Pi^{buy} / \Pi^{buy}_{CE} - \Pi^{sell} / \Pi^{sell}_{CE}',
        100 * regress_data_period[regress_data_period['format'] == 'CDA']['gross_norm_diff'].mean(), 
        100 * regress_data_period[regress_data_period['format'] == 'Flow30']['gross_norm_diff'].mean(),
        100 * regress_data_period[regress_data_period['format'] == 'Flow60']['gross_norm_diff'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['gross_norm_diff'].mean(), 
        100 * regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['gross_norm_diff'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['gross_norm_diff'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['gross_norm_diff'].mean(), 
        100 * regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['gross_norm_diff'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['gross_norm_diff'].mean(),
        ],
]

summary_market_short = [
    [None, 'CDA', 'Flow30', 'Flow60', 'CDA', 'Flow30', 'Flow60', ], 
    [None, 'T1 - T20', 'T1 - T20', 'T1 - T20', 'T11 - T20', 'T11 - T20', 'T11 - T20', ], 
    ['Clearing Price', 
        regress_data_interval[(regress_data_interval['format'] == 'CDA')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['format'] == 'Flow30')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['format'] == 'Flow60')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'CDA')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow30')]['weighted_price'].mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow60')]['weighted_price'].mean(),
    ],
    ['Std. Dev.', 
        '({})'.format(regress_data_interval[(regress_data_interval['format'] == 'CDA')]['weighted_price'].std()), 
        '({})'.format(regress_data_interval[(regress_data_interval['format'] == 'Flow30')]['weighted_price'].std()),
        '({})'.format(regress_data_interval[(regress_data_interval['format'] == 'Flow60')]['weighted_price'].std()),
        '({})'.format(regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'CDA')]['weighted_price'].std()), 
        '({})'.format(regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow30')]['weighted_price'].std()),
        '({})'.format(regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow60')]['weighted_price'].std()),
    ], 
    ['|P_{t} - P_{t - 1}|', 
        regress_data_interval[(regress_data_interval['format'] == 'CDA')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['format'] == 'Flow30')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['format'] == 'Flow60')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'CDA')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow30')]['price_change'].abs().mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow60')]['price_change'].abs().mean(),
        ], 
    [r'Std. Dev. of (\ln P_{t} - \ln P_{t - 1})', 
        regress_data_period[regress_data_period['format'] == 'CDA']['change_log_wprice'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['change_log_wprice'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['change_log_wprice'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['change_log_wprice'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['change_log_wprice'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['change_log_wprice'].mean(),
        ],
    ['PPI',
        liquidity_cda_period[liquidity_cda_period['format'] == 'CDA']['ppi'].mean(), 
        liquidity_flow_period[(liquidity_flow_period['format'] == 'Flow30') & (liquidity_flow_period['group'] <= num_flow30)]['ppi'].mean(),
        liquidity_flow_period[(liquidity_flow_period['format'] == 'Flow60') & (liquidity_flow_period['group'] > num_flow30)]['ppi'].mean(),
        liquidity_cda_period[(liquidity_cda_period['format'] == 'CDA') & (liquidity_cda_period['period'] > (num_periods - prac_periods) // 2)]['ppi'].mean(), 
        liquidity_flow_period[(liquidity_flow_period['format'] == 'Flow30') & (liquidity_flow_period['period'] > (num_periods - prac_periods) // 2)]['ppi'].mean(),
        liquidity_flow_period[(liquidity_flow_period['format'] == 'Flow60') & (liquidity_flow_period['period'] > (num_periods - prac_periods) // 2)]['ppi'].mean(), 
        ],
    ['Traded Volume (shares)', 
        regress_data_period[regress_data_period['format'] == 'CDA']['traded_volume'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow30']['traded_volume'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['traded_volume'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['traded_volume'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['traded_volume'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['traded_volume'].mean(),
        ],  
    [r'Traded Vol. /Q\_{CE} (%)', 
        100 * regress_data_period[regress_data_period['format'] == 'CDA']['Traded/CE Quantity'].mean(), 
        100 * regress_data_period[regress_data_period['format'] == 'Flow30']['Traded/CE Quantity'].mean(),
        100 * regress_data_period[regress_data_period['format'] == 'Flow60']['Traded/CE Quantity'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['Traded/CE Quantity'].mean(), 
        100 * regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['Traded/CE Quantity'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['Traded/CE Quantity'].mean(),
        ],
    [r'Filled Contract / Q\_{CE} (%)', 
        100 * regress_data_period[regress_data_period['format'] == 'CDA']['filled_contract'].mean(),
        100 * regress_data_period[regress_data_period['format'] == 'Flow30']['filled_contract'].mean(),
        100 * regress_data_period[regress_data_period['format'] == 'Flow60']['filled_contract'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['filled_contract'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['filled_contract'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['filled_contract'].mean(),
        ],
    ['Num. of Transactions', 
        int(statistics.mean(transaction_number_cda_all20)), None, None,
        int(statistics.mean(transaction_number_cda_last10)), None, None,
        ],
    ['Mean Transaction Size', 
        int(statistics.mean(volume_volatility_cda_all20)), None, None,
        int(statistics.mean(volume_volatility_cda_last10)), None, None,
        ],
    ['Std. Dev.', 
        '({})'.format(statistics.stdev(volume_volatility_cda_all20)), None, None,
        '({})'.format(statistics.stdev(volume_volatility_cda_last10)), None, None,
        ],
    ['Clearing Rate', 
        None, statistics.mean(clearing_rate_flow30_all20), statistics.mean(clearing_rate_flow60_all20),
        None, statistics.mean(clearing_rate_flow30_last10), statistics.mean(clearing_rate_flow30_last10),
       ], 
    ['Std. Dev.', 
        None, '({})'.format(statistics.stdev(clearing_rate_flow30_all20)), '({})'.format(statistics.stdev(clearing_rate_flow60_all20)),
        None, '({})'.format(statistics.stdev(clearing_rate_flow30_last10)), '({})'.format(statistics.stdev(clearing_rate_flow60_last10)),
        ], 
    ['Time with no FLOW Trans (%)',
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['%no_trans'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['%no_trans'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%no_trans'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%no_trans'].mean(),
    ],
    ['Info. Effic.: |Price - P_{CE}|', 
        regress_data_interval[(regress_data_interval['format'] == 'CDA')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['format'] == 'Flow30')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['format'] == 'Flow60')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'CDA')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow30')]['price_deviation'].mean(),
        regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['format'] == 'Flow60')]['price_deviation'].mean(),
        ], 
    [r'Alloc. Effic.: \Pi / \Pi_{CE} (x100)', 
        100 * regress_data_period[regress_data_period['format'] == 'CDA']['realized_surplus'].mean(),
        100 * regress_data_period[regress_data_period['format'] == 'Flow30']['realized_surplus'].mean(),
        100 * regress_data_period[regress_data_period['format'] == 'Flow60']['realized_surplus'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['realized_surplus'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['realized_surplus'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['realized_surplus'].mean(),
        ],
    [r'\Pi^{buy} / \Pi^{buy}_{CE} - \Pi^{sell} / \Pi^{sell}_{CE}',
        100 * regress_data_period[regress_data_period['format'] == 'CDA']['gross_norm_diff'].mean(), 
        100 * regress_data_period[regress_data_period['format'] == 'Flow30']['gross_norm_diff'].mean(),
        100 * regress_data_period[regress_data_period['format'] == 'Flow60']['gross_norm_diff'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['gross_norm_diff'].mean(), 
        100 * regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['gross_norm_diff'].mean(),
        100 * regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['gross_norm_diff'].mean(),
        ],
]

summary_trader_all20 = [
    [None, 'CDA', 'Flow30', 'Flow60', 'CDA', 'Flow30', 'FLOw_H', 'CDA', 'Flow30', 'Flow60', ], 
    [None, 'T1 - T20', 'T1 - T20', 'T1 - T20', 'T1 - T10', 'T1 - T10', 'T1 - T10', 'T11 - T20', 'T11 - T20', 'T11 - T20', ], 
    ['Number of Orders', 
        regress_data_period[regress_data_period['format'] == 'CDA']['overall_order_num'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_num'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_num'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_num'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_num'].mean(),
        ],
    ['Seller', 
        regress_data_period[regress_data_period['format'] == 'CDA']['seller_order_num'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_num'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_num'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_num'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_num'].mean(),
    ], 
    ['Buyer', 
        regress_data_period[regress_data_period['format'] == 'CDA']['buyer_order_num'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_num'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_num'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_num'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_num'].mean(),
    ], 
    ['Quant. per Order', 
        regress_data_period[regress_data_period['format'] == 'CDA']['overall_order_quantity'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_quantity'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_quantity'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_quantity'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_quantity'].mean(),
    ],
    ['Seller', 
        regress_data_period[regress_data_period['format'] == 'CDA']['seller_order_quantity'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_quantity'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_quantity'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_quantity'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_quantity'].mean(),
    ], 
    ['Buyer', 
        regress_data_period[regress_data_period['format'] == 'CDA']['buyer_order_quantity'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_quantity'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_quantity'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_quantity'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_quantity'].mean(),
    ], 
    ['Order Price', 
        regress_data_period[regress_data_period['format'] == 'CDA']['overall_order_price_low'].mean(), 
        [regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_price_low'].mean(), regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_price_high'].mean()],
        [regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_price_low'].mean(), regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_price_high'].mean()],
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_price_low'].mean(), 
        [regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_price_high'].mean()],
        [regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_price_high'].mean()],
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_low'].mean(), 
        [regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_high'].mean()],
        [regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_high'].mean()],
    ],
    ['Seller', 
        regress_data_period[regress_data_period['format'] == 'CDA']['seller_order_price_low'].mean(), 
        [regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_price_low'].mean(), regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_price_high'].mean()],
        [regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_price_low'].mean(), regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_price_high'].mean()],
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_price_low'].mean(), 
        [regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_price_high'].mean()],
        [regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_price_high'].mean()],
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_low'].mean(), 
        [regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_high'].mean()],
        [regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_high'].mean()],
    ],
    ['Buyer', 
        regress_data_period[regress_data_period['format'] == 'CDA']['buyer_order_price_low'].mean(), 
        [regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_price_low'].mean(), regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_price_high'].mean()],
        [regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_price_low'].mean(), regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_price_high'].mean()],
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_price_low'].mean(), 
        [regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_price_high'].mean()],
        [regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_price_high'].mean()],
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_low'].mean(), 
        [regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_high'].mean()],
        [regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_high'].mean()],
    ],
    ['Order Max Rate', 
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_rate'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_rate'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_rate'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['overall_order_rate'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_rate'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_rate'].mean(),
    ],
    ['Seller', 
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_rate'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_rate'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_rate'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['seller_order_rate'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_rate'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_rate'].mean(),
    ],
    ['Buyer', 
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_rate'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_rate'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_rate'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['buyer_order_rate'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_rate'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_rate'].mean(),
    ],
    ['%Order at Max Quantity', 
        regress_data_period[regress_data_period['format'] == 'CDA']['%max_quantity/rate_orders'].mean(), None, None, 
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders'].mean(), None, None,
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders'].mean(), None, None, 
    ],
    ['Seller', 
        regress_data_period[regress_data_period['format'] == 'CDA']['%max_quantity/rate_orders_sell'].mean(), None, None,
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_sell'].mean(), None, None,
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_sell'].mean(), None, None,
    ],
    ['Buyer', 
        regress_data_period[regress_data_period['format'] == 'CDA']['%max_quantity/rate_orders_buy'].mean(), None, None,
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_buy'].mean(), None, None,
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_buy'].mean(), None, None,
    ],
    ['%Order at Max Rate', 
        None, 
        regress_data_period[regress_data_period['format'] == 'Flow30']['%max_quantity/rate_orders'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['%max_quantity/rate_orders'].mean(),
        None,
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders'].mean(),
        None,        
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders'].mean(),
    ],
    ['Seller', 
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['%max_quantity/rate_orders_sell'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['%max_quantity/rate_orders_sell'].mean(),
        None,
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_sell'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_sell'].mean(),
        None,
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_sell'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_sell'].mean(),
    ],
    ['Buyer', 
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['%max_quantity/rate_orders_buy'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['%max_quantity/rate_orders_buy'].mean(),
        None,
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_buy'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] <= (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_buy'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_buy'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_buy'].mean(),
    ],
]

summary_trader_short = [
    [None, 'CDA', 'Flow30', 'Flow60', 'CDA', 'Flow30', 'Flow60',], 
    [None, 'T1 - T20', 'T1 - T20', 'T1 - T20', 'T11 - T20', 'T11 - T20', 'T11 - T20', ], 
    ['Number of Orders', 
        regress_data_period[regress_data_period['format'] == 'CDA']['overall_order_num'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_num'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_num'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_num'].mean(),
        ],
    ['Seller', 
        regress_data_period[regress_data_period['format'] == 'CDA']['seller_order_num'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_num'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_num'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_num'].mean(),
    ], 
    ['Buyer', 
        regress_data_period[regress_data_period['format'] == 'CDA']['buyer_order_num'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_num'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_num'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_num'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_num'].mean(),
    ], 
    ['Quant. per Order', 
        regress_data_period[regress_data_period['format'] == 'CDA']['overall_order_quantity'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_quantity'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_quantity'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_quantity'].mean(),
    ],
    ['Seller', 
        regress_data_period[regress_data_period['format'] == 'CDA']['seller_order_quantity'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_quantity'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_quantity'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_quantity'].mean(),
    ], 
    ['Buyer', 
        regress_data_period[regress_data_period['format'] == 'CDA']['buyer_order_quantity'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_quantity'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_quantity'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_quantity'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_quantity'].mean(),
    ], 

    ['Quant. per Order (early)', 
        regress_data_period[regress_data_period['format'] == 'CDA']['overall_order_quantity_initial'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_quantity_initial'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_quantity_initial'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_quantity_initial'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_quantity_initial'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_quantity_initial'].mean(),
    ],
    ['Seller', 
        regress_data_period[regress_data_period['format'] == 'CDA']['seller_order_quantity_initial'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_quantity_initial'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_quantity_initial'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_quantity_initial'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_quantity_initial'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_quantity_initial'].mean(),
    ], 
    ['Buyer', 
        regress_data_period[regress_data_period['format'] == 'CDA']['buyer_order_quantity_initial'].mean(), 
        regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_quantity_initial'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_quantity_initial'].mean(),
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_quantity_initial'].mean(), 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_quantity_initial'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_quantity_initial'].mean(),
    ], 


    ['Order Price', 
        regress_data_period[regress_data_period['format'] == 'CDA']['overall_order_price_low'].mean(), 
        [regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_price_low'].mean(), regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_price_high'].mean()],
        [regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_price_low'].mean(), regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_price_high'].mean()],
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_low'].mean(), 
        [regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_high'].mean()],
        [regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_high'].mean()],
    ],
    ['Seller', 
        regress_data_period[regress_data_period['format'] == 'CDA']['seller_order_price_low'].mean(), 
        [regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_price_low'].mean(), regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_price_high'].mean()],
        [regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_price_low'].mean(), regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_price_high'].mean()],
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_low'].mean(), 
        [regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_high'].mean()],
        [regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_high'].mean()],
    ],
    ['Buyer', 
        regress_data_period[regress_data_period['format'] == 'CDA']['buyer_order_price_low'].mean(), 
        [regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_price_low'].mean(), regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_price_high'].mean()],
        [regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_price_low'].mean(), regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_price_high'].mean()],
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_low'].mean(), 
        [regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_high'].mean()],
        [regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_low'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_high'].mean()],
    ],

    ['Order Price (early)',
        regress_data_period[regress_data_period['format'] == 'CDA']['overall_order_price_low_initial'].mean(),
        [regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_price_low_initial'].mean(), regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_price_high_initial'].mean()],
        [regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_price_low_initial'].mean(), regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_price_high_initial'].mean()],
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_low_initial'].mean(),
        [regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_low_initial'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_high_initial'].mean()],
        [regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_low_initial'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_price_high_initial'].mean()],
    ],
    ['Seller',
        regress_data_period[regress_data_period['format'] == 'CDA']['seller_order_price_low_initial'].mean(), 
        [regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_price_low_initial'].mean(), regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_price_high_initial'].mean()],
        [regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_price_low_initial'].mean(), regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_price_high_initial'].mean()],
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_low_initial'].mean(), 
        [regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_low_initial'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_high_initial'].mean()],
        [regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_low_initial'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_price_high_initial'].mean()],
    ],
    ['Buyer',
        regress_data_period[regress_data_period['format'] == 'CDA']['buyer_order_price_low_initial'].mean(), 
        [regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_price_low_initial'].mean(), regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_price_high_initial'].mean()],
        [regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_price_low_initial'].mean(), regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_price_high_initial'].mean()],
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_low_initial'].mean(), 
        [regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_low_initial'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_high_initial'].mean()],
        [regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_low_initial'].mean(), regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_price_high_initial'].mean()],
    ],
    
    ['Order Max Rate', 
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_rate'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_rate'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_rate'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_rate'].mean(),
    ],
    ['Seller', 
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_rate'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_rate'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_rate'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_rate'].mean(),
    ],
    ['Buyer', 
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_rate'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_rate'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_rate'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_rate'].mean(),
    ],

    ['Order Max Rate (early)',
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['overall_order_rate_initial'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['overall_order_rate_initial'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_rate_initial'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['overall_order_rate_initial'].mean(),
    ],
    ['Seller',
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['seller_order_rate_initial'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['seller_order_rate_initial'].mean(),
        None,   
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_rate_initial'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_order_rate_initial'].mean(),
    ],
    ['Buyer',
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_order_rate_initial'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_order_rate_initial'].mean(),
        None,
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_rate_initial'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_order_rate_initial'].mean(),
    ],

    ['%Order at Max Quantity', 
        regress_data_period[regress_data_period['format'] == 'CDA']['%max_quantity/rate_orders'].mean(), None, None, 
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders'].mean(), None, None, 
    ],
    ['Seller', 
        regress_data_period[regress_data_period['format'] == 'CDA']['%max_quantity/rate_orders_sell'].mean(), None, None,
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_sell'].mean(), None, None,
    ],
    ['Buyer', 
        regress_data_period[regress_data_period['format'] == 'CDA']['%max_quantity/rate_orders_buy'].mean(), None, None,
        regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_buy'].mean(), None, None,
    ],
    ['%Order at Max Rate', 
        None, 
        regress_data_period[regress_data_period['format'] == 'Flow30']['%max_quantity/rate_orders'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['%max_quantity/rate_orders'].mean(),
        None,        
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders'].mean(),
    ],
    ['Seller', 
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['%max_quantity/rate_orders_sell'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['%max_quantity/rate_orders_sell'].mean(),
        None,
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_sell'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_sell'].mean(),
    ],
    ['Buyer', 
        None,
        regress_data_period[regress_data_period['format'] == 'Flow30']['%max_quantity/rate_orders_buy'].mean(),
        regress_data_period[regress_data_period['format'] == 'Flow60']['%max_quantity/rate_orders_buy'].mean(),
        None, 
        regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_buy'].mean(),
        regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['%max_quantity/rate_orders_buy'].mean(),
    ],
]


summary_market_short = [[round(num, 2) if isinstance(num, float) else remove_paren(num, 2) for num in sublist] for sublist in summary_market_short]
summary_market_all20 = [[round(num, 2) if isinstance(num, float) else remove_paren(num, 2) for num in sublist] for sublist in summary_market_all20]  
summary_trader_short = [[round(num, 2) if isinstance(num, float) else remove_paren(num, 2) for num in sublist] for sublist in summary_trader_short]
summary_trader_all20 = [[round(num, 2) if isinstance(num, float) else remove_paren(num, 2) for num in sublist] for sublist in summary_trader_all20]
summary_market_short_int = [[round(num) if isinstance(num, float) else remove_paren(num, 0) for num in sublist] for sublist in summary_market_short]
summary_market_all20_int = [[round(num) if isinstance(num, float) else remove_paren(num, 0) for num in sublist] for sublist in summary_market_all20]
summary_trader_short_int = [[round(num) if isinstance(num, float) else remove_paren(num, 0) for num in sublist] for sublist in summary_trader_short]
summary_trader_all20_int = [[round(num) if isinstance(num, float) else remove_paren(num, 0) for num in sublist] for sublist in summary_trader_all20]

# output to a latex table
if price_interval_size == 5:
    # table 1
    summary_trader_short_table = tabulate(summary_trader_short, headers='firstrow', tablefmt='latex')
    print('summary_trader_short_table')
    with open(os.path.join(tables_dir, 'Table1_Summary_Traders_T11-T20.tex'), 'w') as f:
        f.write(summary_trader_short_table)

    # table 1 with integer values
    summary_trader_short_table_int = tabulate(summary_trader_short_int, headers='firstrow', tablefmt='latex')
    print('summary_trader_short_table_int')
    with open(os.path.join(intermediate_dir, 'Table1_Summary_Traders_T11-T20_int.tex'), 'w') as f:
        f.write(summary_trader_short_table_int)

    # table 2
    summary_market_short_table = tabulate(summary_market_short, headers='firstrow', tablefmt='latex')
    print('Table 2 (T11-T20)')
    with open(os.path.join(tables_dir, 'Table2_Summary_Market_T11-T20.tex'), 'w') as f:
        f.write(summary_market_short_table)

    # table 2 with integer values
    summary_market_short_table_int = tabulate(summary_market_short_int, headers='firstrow', tablefmt='latex')
    with open(os.path.join(intermediate_dir, 'Table2_Summary_Market_T11-T20_int.tex'), 'w') as f:
        f.write(summary_market_short_table_int)

if price_interval_size == 5:
    summary_trader_all20_table = tabulate(summary_trader_all20, headers='firstrow', tablefmt='latex')
    print('Table 1 (T1-T20)')
    with open(os.path.join(tables_dir, 'Table1_Summary_Traders_T1-T20.tex'), 'w') as f:
        f.write(summary_trader_all20_table)

    summary_trader_all20_table_int = tabulate(summary_trader_all20_int, headers='firstrow', tablefmt='latex')
    with open(os.path.join(intermediate_dir, 'Table1_Summary_Traders_T1-T20_int.tex'), 'w') as f:
        f.write(summary_trader_all20_table_int)

    summary_market_all20_table = tabulate(summary_market_all20, headers='firstrow', tablefmt='latex')
    print('Table 2 (T1-T20)')
    with open(os.path.join(tables_dir, 'Table2_Summary_Market_T1-T20.tex'), 'w') as f:
        f.write(summary_market_all20_table)

    summary_market_all20_table_int = tabulate(summary_market_all20_int, headers='firstrow', tablefmt='latex')
    with open(os.path.join(intermediate_dir, 'Table2_Summary_Market_T1-T20_int.tex'), 'w') as f:
        f.write(summary_market_all20_table_int)




block_names = ['block_{}'.format(i) for i in range(1, blocks + 1)]

# regression for price deviation 
price_dev_formula = 'price_deviation ~ format + period + interval'
for dummy in block_names[:-1]:
    price_dev_formula += ' + ' + dummy
weights = 'quantity'
price_dev_model = sm.WLS.from_formula(price_dev_formula, data=regress_data_interval, weights=regress_data_interval[weights])
price_dev_res = price_dev_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_interval['group']), 'maxlags': 1})
price_dev_wald = price_dev_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False) 


price_dev_last10_formula = 'price_deviation ~ format + period + interval'
for dummy in block_names[:-1]:
    price_dev_last10_formula += ' + ' + dummy
weights = 'quantity'
price_dev_last10_model = sm.WLS.from_formula(price_dev_last10_formula, data=regress_data_interval[regress_data_interval['period'] > (num_periods - prac_periods) // 2], weights=regress_data_interval[regress_data_interval['period'] > (num_periods - prac_periods) // 2][weights])
price_dev_last10_res = price_dev_last10_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_interval[regress_data_interval['period'] > (num_periods - prac_periods) // 2]['group']), 'maxlags': 1})
price_dev_last10_wald = price_dev_last10_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)


# regression for ppi
ppi_formula = 'ppi ~ format + period + interval'
for dummy in block_names[:-1]:
    ppi_formula += ' + ' + dummy
ppi_model = sm.OLS.from_formula(ppi_formula, data=regress_data_interval)
ppi_res = ppi_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_interval['group']), 'maxlags': 1})
ppi_wald = ppi_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)


ppi_last10_formula = 'ppi ~ format + period + interval'
for dummy in block_names[:-1]:
    ppi_last10_formula += ' + ' + dummy
ppi_last10_model = sm.OLS.from_formula(ppi_last10_formula, data=regress_data_interval[regress_data_interval['period'] > (num_periods - prac_periods) // 2])
ppi_last10_res = ppi_last10_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_interval[regress_data_interval['period'] > (num_periods - prac_periods) // 2]['group']), 'maxlags': 1})
ppi_last10_wald = ppi_last10_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)



# regression for price volatility 
# use quantity-weighted prices for each 5-second interval
price_vol_formula = 'change_log_wprice ~ format + period'
for dummy in block_names[:-1]:
    price_vol_formula += ' + ' + dummy
price_vol_model = sm.OLS.from_formula(price_vol_formula, data=regress_data_period)
price_vol_res = price_vol_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period[regress_data_period['change_log_wprice'].notna()]['group']), 'maxlags': 1})
price_vol_wald = price_vol_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)

price_vol_last10_formula = 'change_log_wprice ~ format + period'
for dummy in block_names[:-1]:
    price_vol_last10_formula += ' + ' + dummy
price_vol_last10_model = sm.OLS.from_formula(price_vol_last10_formula, data=regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2])
price_vol_last10_res = price_vol_last10_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period[(regress_data_period['period'] > (num_periods - prac_periods) // 2) & (regress_data_period['change_log_wprice'].notna())]['group']), 'maxlags': 1})
price_vol_last10_wald = price_vol_last10_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)


# use absolute price change
price_vol_abs_formula = 'np.abs(price_change) ~ format + period + interval'
for dummy in block_names[:-1]:
    price_vol_abs_formula += ' + ' + dummy
weights = 'quantity'
price_vol_abs_model = sm.WLS.from_formula(price_vol_abs_formula, data=regress_data_interval, weights=regress_data_interval[weights])
price_vol_abs_res = price_vol_abs_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_interval[regress_data_interval['price_change'].notna()]['group']), 'maxlags': 1})
price_vol_abs_wald = price_vol_abs_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)

price_vol_abs_last10_formula = 'np.abs(price_change) ~ format + period + interval'
for dummy in block_names[:-1]:
    price_vol_abs_last10_formula += ' + ' + dummy
weights = 'quantity'
price_vol_abs_last10_model = sm.WLS.from_formula(price_vol_abs_last10_formula, data=regress_data_interval[regress_data_interval['period'] > (num_periods - prac_periods) // 2], weights=regress_data_interval[regress_data_interval['period'] > (num_periods - prac_periods) // 2][weights])
price_vol_abs_last10_res = price_vol_abs_last10_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_interval[(regress_data_interval['period'] > (num_periods - prac_periods) // 2) & (regress_data_interval['price_change'].notna())]['group']), 'maxlags': 1})
price_vol_abs_last10_wald = price_vol_abs_last10_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)


# regression for realized surplus 
surplus_formula = 'realized_surplus ~ format + period'
for dummy in block_names[:-1]:
    surplus_formula += ' + ' + dummy
surplus_model = sm.OLS.from_formula(surplus_formula, data=regress_data_period)
surplus_res = surplus_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period['group']), 'maxlags': 1})
surplus_wald = surplus_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)

surplus_last10_formula = 'realized_surplus ~ format + period'
for dummy in block_names[:-1]:
    surplus_last10_formula += ' + ' + dummy
surplus_last10_model = sm.OLS.from_formula(surplus_last10_formula, data=regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2])
surplus_last10_res = surplus_last10_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2]['group']), 'maxlags': 1})
surplus_last10_wald = surplus_last10_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)


# regression for traded volume
volume_formula = 'traded_volume ~ format + period'
for dummy in block_names[:-1]:
    volume_formula += ' + ' + dummy
volume_model = sm.OLS.from_formula(volume_formula, data=regress_data_period)
volume_res = volume_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period['group']), 'maxlags': 1})
volume_wald = volume_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)

volume_last10_formula = 'traded_volume ~ format + period'
for dummy in block_names[:-1]:
    volume_last10_formula += ' + ' + dummy
volume_last10_model = sm.OLS.from_formula(volume_last10_formula, data=regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2])
volume_last10_res = volume_last10_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2]['group']), 'maxlags': 1})
volume_last10_wald = volume_last10_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)


# regression for filled CE quantity
filled_volume_formula = 'filled_contract ~ format + period'
for dummy in block_names[:-1]:
    filled_volume_formula += ' + ' + dummy
filled_volume_model = sm.OLS.from_formula(filled_volume_formula, data=regress_data_period)
filled_volume_res = filled_volume_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period['group']), 'maxlags': 1})
filled_volume_wald = filled_volume_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)

filled_volume_last10_formula = 'filled_contract ~ format + period'
for dummy in block_names[:-1]:
    filled_volume_last10_formula += ' + ' + dummy
filled_volume_last10_model = sm.OLS.from_formula(filled_volume_last10_formula, data=regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2])
filled_volume_last10_res = filled_volume_last10_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2]['group']), 'maxlags': 1})
filled_volume_last10_wald = filled_volume_last10_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)


# regression for number of orders
order_number_formula = 'overall_order_num ~ format + period'
for dummy in block_names[:-1]:
    order_number_formula += ' + ' + dummy
order_number_model = sm.OLS.from_formula(order_number_formula, data=regress_data_period)
order_number_res = order_number_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period['group']), 'maxlags': 1})
order_number_wald = order_number_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)

order_number_last10_formula = 'overall_order_num ~ format + period'
for dummy in block_names[:-1]:
    order_number_last10_formula += ' + ' + dummy
order_number_last10_model = sm.OLS.from_formula(order_number_last10_formula, data=regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2])
order_number_last10_res = order_number_last10_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2]['group']), 'maxlags': 1})
order_number_last10_wald = order_number_last10_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)


# regression for order quantity
order_size_formula = 'overall_order_quantity ~ format + period'
for dummy in block_names[:-1]:
    order_size_formula += ' + ' + dummy
order_size_model = sm.OLS.from_formula(order_size_formula, data=regress_data_period)
order_size_res = order_size_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period['group']), 'maxlags': 1})
order_size_wald = order_size_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)

order_size_last10_formula = 'overall_order_quantity ~ format + period'
for dummy in block_names[:-1]:
    order_size_last10_formula += ' + ' + dummy
order_size_last10_model = sm.OLS.from_formula(order_size_last10_formula, data=regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2])
order_size_last10_res = order_size_last10_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2]['group']), 'maxlags': 1})
order_size_last10_wald = order_size_last10_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)


# regression for gross diff
gross_diff_formula = 'gross_diff ~ format + period'
for dummy in block_names[:-1]:
    gross_diff_formula += ' + ' + dummy
gross_diff_model = sm.OLS.from_formula(gross_diff_formula, data=regress_data_period)
gross_diff_res = gross_diff_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period['group']), 'maxlags': 1})
gross_diff_wald = gross_diff_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)

gross_diff_last10_formula = 'gross_diff ~ format + period'
for dummy in block_names[:-1]:
    gross_diff_last10_formula += ' + ' + dummy
gross_diff_last10_model = sm.OLS.from_formula(gross_diff_last10_formula, data=regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2])
gross_diff_last10_res = gross_diff_last10_model.fit(cov_type='hac-panel', cov_kwds={'groups': np.asarray(regress_data_period[regress_data_period['period'] > (num_periods - prac_periods) // 2]['group']), 'maxlags': 1})
gross_diff_last10_wald = gross_diff_last10_res.wald_test('format[T.Flow30] - format[T.Flow60] = 0', scalar=False)


model_choice_price_vol = [
    price_vol_abs_res, price_vol_abs_last10_res, 
    price_vol_res, price_vol_last10_res, 
    ppi_res, ppi_last10_res, 
    ]

model_choice_trader_behavior = [
    order_number_res, order_number_last10_res,
    order_size_res, order_size_last10_res,
    ]

model_choice_volume = [
    volume_res, volume_last10_res,
    filled_volume_res, filled_volume_last10_res, 
]

model_choice_efficiency = [
    price_dev_res, price_dev_last10_res, 
    surplus_res, surplus_last10_res, 
    gross_diff_res, gross_diff_last10_res,
    ]

stargazer_price = Stargazer(model_choice_price_vol)
stargazer_trader = Stargazer(model_choice_trader_behavior)
stargazer_volume = Stargazer(model_choice_volume)
stargazer_efficiency = Stargazer(model_choice_efficiency)

# Helper to format Wald p-values
def _fmt_pval(w):
    p = float(w.pvalue)
    if p < 0.001:
        return '$<$ 0.001'
    return '{:.3f}'.format(p)

# Helper to compute CDA average of dependent variable
_cda_all = regress_data_period[regress_data_period['format'] == 'CDA']
_cda_last = regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]
_cda_int_all = regress_data_interval[regress_data_interval['format'] == 'CDA']
_cda_int_last = regress_data_interval[(regress_data_interval['format'] == 'CDA') & (regress_data_interval['period'] > (num_periods - prac_periods) // 2)]

# Add CDA avg. and Wald test rows to each stargazer table

# Table 3: Trader Behavior (order_number, order_size)
stargazer_trader.add_line('CDA avg.', [
    '{:.1f}'.format(_cda_all['overall_order_num'].mean()),
    '{:.1f}'.format(_cda_last['overall_order_num'].mean()),
    '{:.1f}'.format(_cda_all['overall_order_quantity'].mean()),
    '{:.1f}'.format(_cda_last['overall_order_quantity'].mean()),
])
stargazer_trader.add_line('Flow30 $=$ Flow60? (p)', [
    _fmt_pval(order_number_wald), _fmt_pval(order_number_last10_wald),
    _fmt_pval(order_size_wald), _fmt_pval(order_size_last10_wald),
])

# Table 4: Price Volatility (price_vol_abs on interval, price_vol on period, ppi on interval)
stargazer_price.add_line('CDA avg.', [
    '{:.2f}'.format(np.abs(_cda_int_all['price_change']).mean()),
    '{:.2f}'.format(np.abs(_cda_int_last['price_change']).mean()),
    '{:.2f}'.format(_cda_all['change_log_wprice'].mean()),
    '{:.2f}'.format(_cda_last['change_log_wprice'].mean()),
    '{:.2f}'.format(_cda_int_all['ppi'].mean()),
    '{:.2f}'.format(_cda_int_last['ppi'].mean()),
])
stargazer_price.add_line('Flow30 $=$ Flow60? (p)', [
    _fmt_pval(price_vol_abs_wald), _fmt_pval(price_vol_abs_last10_wald),
    _fmt_pval(price_vol_wald), _fmt_pval(price_vol_last10_wald),
    _fmt_pval(ppi_wald), _fmt_pval(ppi_last10_wald),
])

# Table 5: Volume (traded_volume, filled_contract)
stargazer_volume.add_line('CDA avg.', [
    '{:.1f}'.format(_cda_all['traded_volume'].mean()),
    '{:.1f}'.format(_cda_last['traded_volume'].mean()),
    '{:.2f}'.format(_cda_all['filled_contract'].mean()),
    '{:.2f}'.format(_cda_last['filled_contract'].mean()),
])
stargazer_volume.add_line('Flow30 $=$ Flow60? (p)', [
    _fmt_pval(volume_wald), _fmt_pval(volume_last10_wald),
    _fmt_pval(filled_volume_wald), _fmt_pval(filled_volume_last10_wald),
])

# Table 6: Efficiency (price_dev on interval, surplus on period, gross_diff on period)
stargazer_efficiency.add_line('CDA avg.', [
    '{:.2f}'.format(_cda_int_all['price_deviation'].mean()),
    '{:.2f}'.format(_cda_int_last['price_deviation'].mean()),
    '{:.3f}'.format(_cda_all['realized_surplus'].mean()),
    '{:.3f}'.format(_cda_last['realized_surplus'].mean()),
    '{:.1f}'.format(_cda_all['gross_diff'].mean()),
    '{:.1f}'.format(_cda_last['gross_diff'].mean()),
])
stargazer_efficiency.add_line('Flow30 $=$ Flow60? (p)', [
    _fmt_pval(price_dev_wald), _fmt_pval(price_dev_last10_wald),
    _fmt_pval(surplus_wald), _fmt_pval(surplus_last10_wald),
    _fmt_pval(gross_diff_wald), _fmt_pval(gross_diff_last10_wald),
])

print('WALD TEST')
print('trader behavior\n',
      order_number_wald.pvalue, order_number_last10_wald.pvalue,
      order_size_wald.pvalue, order_size_last10_wald.pvalue)
print('price\n',
      price_vol_abs_wald.pvalue, price_vol_abs_last10_wald.pvalue,
      price_vol_wald.pvalue, price_vol_last10_wald.pvalue,
      ppi_wald.pvalue, ppi_last10_wald.pvalue)
print('trade volume\n',
      volume_wald.pvalue, volume_last10_wald.pvalue,
      filled_volume_wald.pvalue, filled_volume_last10_wald.pvalue)
print('efficiency\n',
      price_dev_wald.pvalue, price_dev_last10_wald.pvalue,
      surplus_wald.pvalue, surplus_last10_wald.pvalue,
      gross_diff_wald.pvalue, gross_diff_last10_wald.pvalue)


if price_interval_size == 5:
    print('Table 3: Trader Behavior Regression')
    trader_behavior_regression_table = stargazer_trader.render_latex()
    with open(os.path.join(tables_dir, 'Table3_Regression_Trader_Behavior.tex'), 'w') as f:
        f.write(trader_behavior_regression_table)

    print('Table 4: Price Volatility Regression')
    price_regression_table = stargazer_price.render_latex()
    with open(os.path.join(tables_dir, 'Table4_Regression_Price_Volatility.tex'), 'w') as f:
        f.write(price_regression_table)

    print('Table 5: Volume Regression')
    trade_volume_regression_table = stargazer_volume.render_latex()
    with open(os.path.join(tables_dir, 'Table5_Regression_Volume.tex'), 'w') as f:
        f.write(trade_volume_regression_table)

    print('Table 6: Efficiency Regression')
    efficiency_regression_table = stargazer_efficiency.render_latex()
    with open(os.path.join(tables_dir, 'Table6_Regression_Efficiency.tex'), 'w') as f:
        f.write(efficiency_regression_table)

# Generate robustness-check tables for non-default intervals
if price_interval_size in (10, 2):
    if price_interval_size == 10:
        _s_summary_name = 'TableS2_Summary_Market_10s.tex'
        _s_price_name = 'TableS3_Regression_Price_Volatility_10s.tex'
        _s_eff_name = 'TableS4_Regression_Efficiency_10s.tex'
        _s_label = '10-second'
    else:
        _s_summary_name = 'TableS5_Summary_Market_2s.tex'
        _s_price_name = 'TableS6_Regression_Price_Volatility_2s.tex'
        _s_eff_name = 'TableS7_Regression_Efficiency_2s.tex'
        _s_label = '2-second'

    # Save regression tables (same format as Tables 4 and 6)
    print(f'Saving {_s_label} Price Volatility Regression')
    with open(os.path.join(tables_dir, _s_price_name), 'w') as f:
        f.write(stargazer_price.render_latex())

    print(f'Saving {_s_label} Efficiency Regression')
    with open(os.path.join(tables_dir, _s_eff_name), 'w') as f:
        f.write(stargazer_efficiency.render_latex())

    # Build S summary table (subset of market summary: price stats + info efficiency)
    # Extract relevant rows from summary_market_short (indices 2-6 = price stats, 16 = info effic.)
    _s_price_rows = summary_market_short[2:7]  # Clearing Price, Std Dev, |P-P|, Std Dev ln, PPI
    _s_info_row = summary_market_short[16]      # Info. Effic.: |Price - P_{CE}|
    _s_summary_tex = r"""\begin{table}[!htbp] \centering
\caption{Summary Statistics: Market Performance (""" + _s_label + r""" intervals)}
\resizebox{\textwidth}{!}{
\begin{threeparttable}
\begin{tabular}{lcccccc}
\toprule
 & \multicolumn{3}{c}{T1 -- T20} & \multicolumn{3}{c}{T11 -- T20} \\
 & CDA & Flow30 & Flow60 & CDA & Flow30 & Flow60 \\
\midrule
\\[-1.8ex]
\multicolumn{7}{l}{\textit{\textbf{(a)} Price Statistics} (Avg.\ Equil.\ Price = $9.8$ ECUs)} \\
\\[-1.8ex]
"""
    _row_labels = [
        r'Clearing Prices ($P_\tau$, ECUs)',
        r'\hspace{3mm}(Std.\ Dev.)',
        r'$\lvert P_{\tau} - P_{\tau-1} \rvert$',
        r'Std.\ Dev.\ of $(\ln P_{\tau} - \ln P_{\tau-1})$',
        r'PPI',
    ]
    for label, row in zip(_row_labels, _s_price_rows):
        vals = ' & '.join(str(v) for v in row[1:])
        _s_summary_tex += f' {label} & {vals} \\\\\n'
    _s_summary_tex += r"""\multicolumn{7}{l}{\textit{\textbf{(c)} Efficiency and Buyer-Seller Inequality}} \\
\\[-1.8ex]
"""
    _info_vals = ' & '.join(str(v) for v in _s_info_row[1:])
    _s_summary_tex += r' Info.\ Effic.: $\lvert P_\tau - P_{\text{CE}} \rvert$ & ' + _info_vals + ' \\\\\n'
    _s_summary_tex += r"""\bottomrule
\end{tabular}
\end{threeparttable}}
\end{table}"""

    print(f'Saving {_s_label} Summary Statistics')
    with open(os.path.join(tables_dir, _s_summary_name), 'w') as f:
        f.write(_s_summary_tex)




if price_interval_size != 5:
    print(f'Robustness tables saved for {price_interval_size}s intervals. Skipping figures.')
    sys.exit(0)

cumsum_cda_mean = regress_data_interval[regress_data_interval['format'] == 'CDA'].groupby(['period', 'interval'])['%cumsum'].mean()
cumsum_flow30_mean = regress_data_interval[regress_data_interval['format'] == 'Flow30'].groupby(['period', 'interval'])['%cumsum'].mean()
cumsum_flow60_mean = regress_data_interval[regress_data_interval['format'] == 'Flow60'].groupby(['period', 'interval'])['%cumsum'].mean()

cumsum_cda_mean_agg = regress_data_interval[regress_data_interval['format'] == 'CDA'].groupby(['interval'])['%cumsum'].mean()
cumsum_flow30_mean_agg = regress_data_interval[regress_data_interval['format'] == 'Flow30'].groupby(['interval'])['%cumsum'].mean()
cumsum_flow60_mean_agg = regress_data_interval[regress_data_interval['format'] == 'Flow60'].groupby(['interval'])['%cumsum'].mean()

plot_df = pd.DataFrame(
    {
        'interval': [i for i in range(1, len(cumsum_cda_mean.values) + 1)],
        'cda_mean': cumsum_cda_mean.values,
        'flow30_mean': cumsum_flow30_mean.values,
        'flow60_mean': cumsum_flow60_mean.values,
    }
)

agg_plot_df = pd.DataFrame(
    {
        'interval': cumsum_cda_mean_agg.index,
        'cda_mean': cumsum_cda_mean_agg.values,
        'flow30_mean': cumsum_flow30_mean_agg.values,
        'flow60_mean': cumsum_flow60_mean_agg.values,
    }
)



##### profits distribution #####
# all periods
sorted_gross_cda_buy_group = np.sort(regress_data_period[regress_data_period['format'] == 'CDA']['buyer_realized_surplus'].tolist())
cumulative_gross_cda_buy_group = np.arange(len(sorted_gross_cda_buy_group)) / len(sorted_gross_cda_buy_group)
sorted_gross_cda_sell_group = np.sort(regress_data_period[regress_data_period['format'] == 'CDA']['seller_realized_surplus'].tolist())
cumulative_gross_cda_sell_group = np.arange(len(sorted_gross_cda_sell_group)) / len(sorted_gross_cda_sell_group)
sorted_gross_flow30_buy_group = np.sort(regress_data_period[regress_data_period['format'] == 'Flow30']['buyer_realized_surplus'].tolist())
cumulative_gross_flow30_buy_group = np.arange(len(sorted_gross_flow30_buy_group)) / len(sorted_gross_flow30_buy_group)
sorted_gross_flow30_sell_group = np.sort(regress_data_period[regress_data_period['format'] == 'Flow30']['seller_realized_surplus'].tolist())
cumulative_gross_flow30_sell_group = np.arange(len(sorted_gross_flow30_sell_group)) / len(sorted_gross_flow30_sell_group)
sorted_gross_flow60_buy_group = np.sort(regress_data_period[regress_data_period['format'] == 'Flow60']['buyer_realized_surplus'].tolist())
cumulative_gross_flow60_buy_group = np.arange(len(sorted_gross_flow60_buy_group)) / len(sorted_gross_flow60_buy_group)
sorted_gross_flow60_sell_group = np.sort(regress_data_period[regress_data_period['format'] == 'Flow60']['seller_realized_surplus'].tolist())
cumulative_gross_flow60_sell_group = np.arange(len(sorted_gross_flow60_sell_group)) / len(sorted_gross_flow60_sell_group)   


plt.plot(sorted_gross_cda_buy_group, cumulative_gross_cda_buy_group, marker=',', linestyle='solid', color=(0, 128/255, 0), markersize=5, label='CDA buyer')
plt.plot(sorted_gross_cda_sell_group, cumulative_gross_cda_sell_group, marker=',', linestyle='solid', color=(128/255, 0,  128/255), markersize=5, label='CDA seller')
plt.plot(sorted_gross_flow30_buy_group, cumulative_gross_flow30_buy_group, marker=',', linestyle='dashed', color=(0, 128/255, 0), markersize=5, label='Flow30 buyer')
plt.plot(sorted_gross_flow30_sell_group, cumulative_gross_flow30_sell_group, marker=',', linestyle='dashed', color=(128/255, 0, 128/255), markersize=5, label='Flow30 seller')
plt.plot(sorted_gross_flow60_buy_group, cumulative_gross_flow60_buy_group, marker=',', linestyle='dotted', color=(0, 128/255, 0), markersize=5, label='Flow60 buyer')
plt.plot(sorted_gross_flow60_sell_group, cumulative_gross_flow60_sell_group, marker=',', linestyle='dotted', color=(128/255, 0, 128/255), markersize=5, label='Flow60 seller')
plt.title('CDF of Normalized Gross Profits')
plt.xlabel('Gross / CE Profits')
plt.ylabel('Cumulative Probability')
plt.grid(True)
plt.legend(loc='lower right')
plt.savefig(os.path.join(figures_dir, 'Figure6_Profit_CDF.png'))
plt.close()


sorted_gross_cda_buy_group_last10 = np.sort(regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_realized_surplus'].tolist())
cumulative_gross_cda_buy_group_last10 = np.arange(len(sorted_gross_cda_buy_group_last10)) / len(sorted_gross_cda_buy_group_last10)
sorted_gross_cda_sell_group_last10 = np.sort(regress_data_period[(regress_data_period['format'] == 'CDA') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_realized_surplus'].tolist())
cumulative_gross_cda_sell_group_last10 = np.arange(len(sorted_gross_cda_sell_group_last10)) / len(sorted_gross_cda_sell_group_last10)
sorted_gross_flow30_buy_group_last10 = np.sort(regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_realized_surplus'].tolist())
cumulative_gross_flow30_buy_group_last10 = np.arange(len(sorted_gross_flow30_buy_group_last10)) / len(sorted_gross_flow30_buy_group_last10)
sorted_gross_flow30_sell_group_last10 = np.sort(regress_data_period[(regress_data_period['format'] == 'Flow30') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_realized_surplus'].tolist())
cumulative_gross_flow30_sell_group_last10 = np.arange(len(sorted_gross_flow30_sell_group_last10)) / len(sorted_gross_flow30_sell_group_last10)
sorted_gross_flow60_buy_group_last10 = np.sort(regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['buyer_realized_surplus'].tolist())
cumulative_gross_flow60_buy_group_last10 = np.arange(len(sorted_gross_flow60_buy_group_last10)) / len(sorted_gross_flow60_buy_group_last10)
sorted_gross_flow60_sell_group_last10 = np.sort(regress_data_period[(regress_data_period['format'] == 'Flow60') & (regress_data_period['period'] > (num_periods - prac_periods) // 2)]['seller_realized_surplus'].tolist())
cumulative_gross_flow60_sell_group_last10 = np.arange(len(sorted_gross_flow60_sell_group_last10)) / len(sorted_gross_flow60_sell_group_last10)

plt.plot(sorted_gross_cda_buy_group_last10, cumulative_gross_cda_buy_group_last10, marker=',', linestyle='solid', color=(0, 128/255, 0), markersize=5, label='CDA Buyer')
plt.plot(sorted_gross_cda_sell_group_last10, cumulative_gross_cda_sell_group_last10, marker=',', linestyle='solid', color=(128/255, 0, 128/255), markersize=5, label='CDA Seller')
plt.plot(sorted_gross_flow30_buy_group_last10, cumulative_gross_flow30_buy_group_last10, marker=',', linestyle='dashed', color=(0, 128/255, 0), markersize=5, label='Flow30 Buyer')
plt.plot(sorted_gross_flow30_sell_group_last10, cumulative_gross_flow30_sell_group_last10, marker=',', linestyle='dashed', color=(128/255, 0, 128/255), markersize=5, label='Flow30 Seller')
plt.plot(sorted_gross_flow60_buy_group_last10, cumulative_gross_flow60_buy_group_last10, marker=',', linestyle='dotted', color=(0, 128/255, 0), markersize=5, label='Flow60 Buyer')
plt.plot(sorted_gross_flow60_sell_group_last10, cumulative_gross_flow60_sell_group_last10, marker=',', linestyle='dotted', color=(128/255, 0, 128/255), markersize=5, label='Flow60 Seller')
plt.title('CDF of Normalized Gross Profits')
plt.xlabel('Gross / CE Profits')
plt.ylabel('Cumulative Probability')
plt.grid(True)
plt.legend(loc='lower right')
plt.savefig(os.path.join(figures_dir, 'FigureS3_Profit_CDF_Last10.png'))
plt.close()

compress_df_cda = market_per_second_cda[(market_per_second_cda['group_id'] == 1)].copy()
compress_df_cda['timestamp'] = compress_df_cda['timestamp'] % round_length
compress_df_cda['timestamp'] = compress_df_cda['timestamp'].replace(0, round_length)
compress_df_cda['mean_cumulative_quantity_percent'] = compress_df_cda['mean_cumulative_quantity'] / compress_df_cda['ce_quantity']
summary_cda = compress_df_cda.groupby('timestamp').agg({'mean_cumulative_quantity_percent': 'mean'}).reset_index()

compress_df_flow30 = market_per_second_flow[(market_per_second_flow['group_id'] == 1)].copy()
compress_df_flow30['timestamp'] = compress_df_flow30['timestamp'] % round_length
compress_df_flow30['timestamp'] = compress_df_flow30['timestamp'].replace(0, round_length)
compress_df_flow30['mean_cumulative_quantity_percent'] = compress_df_flow30['mean_cumulative_quantity'] / compress_df_flow30['ce_quantity']
summary_flow30 = compress_df_flow30.groupby('timestamp').agg({'mean_cumulative_quantity_percent': 'mean'}).reset_index()

compress_df_flow60 = market_per_second_flow[(market_per_second_flow['group_id'] == 6)].copy()
compress_df_flow60['timestamp'] = compress_df_flow60['timestamp'] % round_length
compress_df_flow60['timestamp'] = compress_df_flow60['timestamp'].replace(0, round_length)
compress_df_flow60['mean_cumulative_quantity_percent'] = compress_df_flow60['mean_cumulative_quantity'] / compress_df_flow60['ce_quantity']
summary_flow60 = compress_df_flow60.groupby('timestamp').agg({'mean_cumulative_quantity_percent': 'mean'}).reset_index()

plt.figure(figsize=(8, 5))
plt.plot(summary_cda['timestamp'], summary_cda['mean_cumulative_quantity_percent'], linestyle='solid', c='green', label='CDA')
plt.plot(summary_flow30['timestamp'], summary_flow30['mean_cumulative_quantity_percent'], c='green', linestyle='dashed', label='Flow30')
plt.plot(summary_flow60['timestamp'], summary_flow60['mean_cumulative_quantity_percent'], c='green', linestyle='dotted', label='Flow60')
plt.hlines(y=1, xmin=1, xmax=round_length, colors='plum', linestyles='--')
plt.xticks(np.arange(1, round_length + 2, 10), np.arange(0, round_length + 1, 10))
plt.xlabel('Time')
plt.ylabel('Percent')
plt.ylim(0, 1.1)
plt.legend(loc='lower right')
plt.savefig(os.path.join(figures_dir, 'Figure8_Cumulative_Volume.png'))
plt.close()