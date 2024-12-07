import pandas as pd
import numpy as np
from datetime import datetime, timezone
from .fc_address import fc_address_list


def bgdeldup(dateName:str, minDate: datetime, client: str, bgTable:str):
    """
    Delete the data from the declared minDate to avoid duplicate in the database

    Parameters:
    - dateName: the name of the date column
    - minDate: the start date that will be deleted to avoid duplicate
    - client: the BigQuery client name
    - bgTable: the BigQuery Table address

    Returns:
    - delete the data to avoid duplicate
    """
    delDataQuery = f"""
    DELETE FROM
    `{bgTable}`
    WHERE
    {dateName} >= '{minDate}'
    """

    delData = client.query(delDataQuery)
    delData = delData.result()

    return delData

def bgdeldupf(dateName:str, minDate: datetime, client: str, bgTable:str):
    """
    Delete the data from the declared minDate to avoid duplicate in the database
    (free version of BigQuery)

    Parameters:
    - dateName: the name of the date column
    - minDate: the start date that will be deleted to avoid duplicate
    - client: the BigQuery client name
    - bgTable: the BigQuery Table address

    Returns:
    - delete the data to avoid duplicate
    """
    delDataQuery = f"""
    CREATE OR REPLACE TABLE `{bgTable}` AS

    SELECT *
    FROM `{bgTable}`
    WHERE
    {dateName} < '{minDate}'
    """

    delData = client.query(delDataQuery)
    delData = delData.result()

    return delData

def dfbgcolcheck(df: pd.DataFrame, client: str, bgTable: str):
    """
    This function compares the columns of DataFrame and existing BigQuery Table

    Paremeters:
    - df: Data frame to check
    - client: name of BigQuery client
    - bgTable: the address of BigQuery Table

    Returns:
    - True if it matches
    - ValueError if not
    """
    existingDataQuery = f"""
    SELECT
    *
    FROM
    `{bgTable}`
    LIMIT 10
    """

    existingData = client.query(existingDataQuery).to_dataframe()

    columnsCheck = existingData.columns.equals(df.columns)
    if columnsCheck:
        print("Column names and positions are the same.")
        return True
    else:
        raise ValueError("Error: Column names and positions are not the same.")

def lowfeereport(filePath:str):
    """
    This function process and clean the Amazon Economics Report.
    It extracts the low level inventory data

    Paremeters:
    - filePath: the path where the report is saved

    Returns:
    - DataFrame of the cleaned report
    - Flase if there is no data related to low level inventory fee
    """
    lowFeeDf = pd.read_csv(filePath)

    checkCol = [
        'Low-inventory-level fee per unit',
        'Low-inventory-level fee quantity',
        'Low-inventory-level fee total'
    ]

    colCheck = all(col in lowFeeDf.columns for col in checkCol)

    if colCheck:
        lowFeeDf = lowFeeDf[[
            'Start date',
            'End date',
            'ASIN',
            'MSKU',
            'Low-inventory-level fee per unit',
            'Low-inventory-level fee quantity',
            'Low-inventory-level fee total'
        ]]

        lowFeeDf = lowFeeDf.rename(columns=lambda x:x.replace('-','_').replace(' ','_').lower())
        lowFeeDf['start_date'] = pd.to_datetime(lowFeeDf['start_date'])
        lowFeeDf['end_date'] = pd.to_datetime(lowFeeDf['end_date'])

        schema = {
                'start_date': 'datetime64[ns]',
                'end_date': 'datetime64[ns]',
                'asin': str,
                'msku': str,
                'low_inventory_level_fee_per_unit': float,
                'low_inventory_level_fee_quantity': float,
                'low_inventory_level_fee_total': float
        }

        lowFeeDf = lowFeeDf.astype(schema)
        return lowFeeDf
    else:
        return False
    
def promoreport(filePath:str):
    """
    Clean the raw file downloaded in Amazon Seller Central Promotions Report

    Parameter:
    - filePath: the path where the downloaded Promotions Report is located

    Return:
    - DataFrame of the cleaned report
    """
    promoDf = pd.read_csv(filePath)
    promoDf = promoDf.rename(columns=lambda x:x.replace('?','').replace('"','').replace('-','_').lower())
    promoDf['shipment_date'] = pd.to_datetime(promoDf['shipment_date'], utc=True)

    schema = {
        'shipment_date': 'datetime64[ns, UTC]',
        'currency': str,
        'item_promotion_discount': float,
        'item_promotion_id': str,
        'description': str,
        'promotion_rule_value': str,
        'amazon_order_id': str,
        'shipment_id': str,
        'shipment_item_id': str
    }
    promoDf = promoDf.astype(schema)

    return promoDf

def spstreport(filePath:str):
    spSearchTermDf = pd.read_excel(filePath)
    spSearchTermDf = spSearchTermDf.rename(columns=lambda X:X.replace('7','_7').replace('-','').replace('#','').replace('(','').replace(')','').replace(' ','_').lower())

    schema = {
        'date': 'datetime64[ns]',
        'portfolio_name': str,
        'currency': str,
        'campaign_name': str,
        'ad_group_name': str,
        'targeting': str,
        'match_type': str,
        'customer_search_term': str,
        'impressions': float,
        'clicks': float,
        'clickthru_rate_ctr': float,
        'cost_per_click_cpc': float,
        'spend': float,
        '_7_day_total_sales_': float,
        'total_advertising_cost_of_sales_acos_': float,
        'total_return_on_advertising_spend_roas': float,
        '_7_day_total_orders_': float,
        '_7_day_total_units_': float,
        '_7_day_conversion_rate': float,
        '_7_day_advertised_sku_units_': float,
        '_7_day_other_sku_units_': float,
        '_7_day_advertised_sku_sales_': float,
        '_7_day_other_sku_sales_': float
    }

    spSearchTermDf = spSearchTermDf.astype(schema)

    return spSearchTermDf

def sbstreport(filePath:str):
    sbSearchTermDf = pd.read_excel(filePath)
    sbSearchTermDf = sbSearchTermDf.rename(columns=lambda X:X.replace('14','_14').replace('-','').replace('#','').replace('(','').replace(')','').replace(',','').replace(' ','_').lower())

    schema = {
        'date': 'datetime64[ns]',
        'portfolio_name': str,
        'currency': str,
        'campaign_name': str,
        'ad_group_name': str,
        'targeting': str,
        'match_type': str,
        'customer_search_term': str,
        'cost_type': str,
        'impressions': float,
        'viewable_impressions': float,
        'clicks': float,
        'clickthru_rate_ctr': float,
        'spend': float,
        'cost_per_click_cpc': float,
        'cost_per_1000_viewable_impressions_vcpm': float,
        'total_advertising_cost_of_sales_acos_': float,
        'total_return_on_advertising_spend_roas': float,
        '_14_day_total_sales_': float,
        '_14_day_total_orders_': float,
        '_14_day_total_units_': float,
        '_14_day_conversion_rate': float,
        'total_advertising_cost_of_sales_acos__click': float,
        'total_return_on_advertising_spend_roas__click': float,
        '_14_day_total_sales__click': float,
        '_14_day_total_orders___click': float,
        '_14_day_total_units___click': float
    }

    sbSearchTermDf = sbSearchTermDf.astype(schema)

    return sbSearchTermDf

def sdtreport(filePath:str):
    sdTargetingDf = pd.read_excel(filePath)
    sdTargetingDf = sdTargetingDf.rename(columns=lambda X:X.replace('14','_14').replace('-','').replace('#','').replace('(','').replace(')','').replace(',','').replace(' ','_').lower())

    schema = {
        'date': 'datetime64[ns]',
        'currency': str,
        'campaign_name': str,
        'portfolio_name': str,
        'cost_type': str,
        'ad_group_name': str,
        'targeting': str,
        'bid_optimization': str,
        'impressions': float,
        'viewable_impressions': float,
        'clicks': float,
        'clickthru_rate_ctr': float,
        '_14_day_detail_page_views_dpv': float,
        'spend': float,
        'cost_per_click_cpc': float,
        'cost_per_1000_viewable_impressions_vcpm': float,
        'total_advertising_cost_of_sales_acos_': float,
        'total_return_on_advertising_spend_roas': float,
        '_14_day_total_orders_': float,
        '_14_day_total_units_': float,
        '_14_day_total_sales_': float,
        '_14_day_newtobrand_orders_': float,
        '_14_day_newtobrand_sales': float,
        '_14_day_newtobrand_units_': float,
        'total_advertising_cost_of_sales_acos__click': float,
        'total_return_on_advertising_spend_roas__click': float,
        '_14_day_total_orders___click': float,
        '_14_day_total_units___click': float,
        '_14_day_total_sales__click': float,
        '_14_day_newtobrand_orders___click': float,
        '_14_day_newtobrand_sales__click': float,
        '_14_day_newtobrand_units___click': float
    }

    sdTargetingDf = sdTargetingDf.astype(schema)

    return sdTargetingDf

def spcreport(filePath:str):
    spCampaignDf = pd.read_csv(filePath)
    spCampaignDf = spCampaignDf.rename(columns=lambda X:X.replace('7','_7').replace('-','').replace('#','').replace('(','').replace(')','').replace(',','').replace(' ','_').lower())

    colRange = spCampaignDf.columns[7:]
    spCampaignDf[colRange] = spCampaignDf[colRange].replace({'%':'','\$':'',',':''}, regex=True)
    spCampaignDf['date'] = pd.to_datetime(spCampaignDf['date'])

    schema = {
        'date': 'datetime64[ns]',
        'portfolio_name': str,
        'campaign_type': str,
        'campaign_name': str,
        'country': str,
        'status': str,
        'currency': str,
        'budget': float,
        'targeting_type': str,
        'bidding_strategy': str,
        'impressions': float,
        'last_year_impressions': float,
        'clicks': float,
        'last_year_clicks': float,
        'clickthru_rate_ctr': float,
        'spend': float,
        'last_year_spend': float,
        'cost_per_click_cpc': float,
        'last_year_cost_per_click_cpc': float,
        '_7_day_total_orders_': float,
        'total_advertising_cost_of_sales_acos_': float,
        'total_return_on_advertising_spend_roas': float,
        '_7_day_total_sales_': float
    }

    spCampaignDf = spCampaignDf.astype(schema)

    return spCampaignDf

def sbcreport(filePath:str):
    sbCampaignDf = pd.read_excel(filePath)
    sbCampaignDf = sbCampaignDf.rename(columns=lambda X:X.replace('14','_14').replace('5','_5').replace('-','').replace('#','').replace('(','').replace(')','').replace(',','').replace(' ','_').lower())

    colRange = sbCampaignDf.columns[6:]
    sbCampaignDf[colRange] = sbCampaignDf[colRange].replace({'%':'','\$':'',',':''}, regex=True)
    sbCampaignDf['date'] = pd.to_datetime(sbCampaignDf['date'])

    schema = {
        'date': 'datetime64[ns]',
        'portfolio_name': str,
        'currency': str,
        'campaign_name': str,
        'cost_type': str,
        'country': str,
        'impressions': float,
        'clicks': float,
        'clickthru_rate_ctr': float,
        'cost_per_click_cpc': float,
        'spend': float,
        'total_advertising_cost_of_sales_acos_': float,
        'total_return_on_advertising_spend_roas': float,
        '_14_day_total_sales_': float,
        '_14_day_total_orders_': float,
        '_14_day_total_units_': float,
        '_14_day_conversion_rate': float,
        'viewable_impressions': float,
        'cost_per_1000_viewable_impressions_vcpm': float,
        'viewthrough_rate_vtr': float,
        'clickthrough_rate_for_views_vctr': float,
        'video_first_quartile_views': float,
        'video_midpoint_views': float,
        'video_third_quartile_views': float,
        'video_complete_views': float,
        'video_unmutes': float,
        '_5_second_views': float,
        '_5_second_view_rate': float,
        '_14_day_branded_searches': float,
        '_14_day_detail_page_views_dpv': float,
        '_14_day_newtobrand_orders_': float,
        '_14_day_%_of_orders_newtobrand': float,
        '_14_day_newtobrand_sales': float,
        '_14_day_%_of_sales_newtobrand': float,
        '_14_day_newtobrand_units_': float,
        '_14_day_%_of_units_newtobrand': float,
        '_14_day_newtobrand_order_rate': float,
        'total_advertising_cost_of_sales_acos__click': float,
        'total_return_on_advertising_spend_roas__click': float,
        '_14_day_total_sales__click': float,
        '_14_day_total_orders___click': float,
        '_14_day_total_units___click': float,
        'newtobrand_detail_page_views': float,
        'newtobrand_detail_page_view_clickthrough_conversions': float,
        'newtobrand_detail_page_view_rate': float,
        'effective_cost_per_newtobrand_detail_page_view': float,
        '_14_day_atc': float,
        '_14_day_atc_clicks': float,
        '_14_day_atcr': float,
        'effective_cost_per_add_to_cart_ecpatc': float,
        'branded_searches_clickthrough_conversions': float,
        'branded_searches_rate': float,
        'effective_cost_per_branded_search': float
    }

    sbCampaignDf = sbCampaignDf.astype(schema)
    
    return sbCampaignDf

def sdcreport(filePath:str):
    sdCampaignDf = pd.read_excel(filePath)
    sdCampaignDf = sdCampaignDf.rename(columns=lambda X:X.replace('14','_14').replace('-','').replace('#','').replace('(','').replace(')','').replace(',','').replace(' ','_').lower())

    colRange = sdCampaignDf.columns[4:]
    sdCampaignDf[colRange] = sdCampaignDf[colRange].replace({'%':'','\$':'',',':''}, regex=True)
    sdCampaignDf['date'] = pd.to_datetime(sdCampaignDf['date'])

    schema = {
        'date': 'datetime64[ns]',
        'country': str,
        'status': str,
        'currency': str,
        'budget': float,
        'campaign_name': str,
        'portfolio_name': str,
        'cost_type': str,
        'impressions': float,
        'viewable_impressions': float,
        'clicks': float,
        'clickthru_rate_ctr': float,
        '_14_day_detail_page_views_dpv': float,
        'spend': float,
        'cost_per_click_cpc': float,
        'cost_per_1000_viewable_impressions_vcpm': float,
        'total_advertising_cost_of_sales_acos_': float,
        'total_return_on_advertising_spend_roas': float,
        '_14_day_total_orders_': float,
        '_14_day_total_units_': float,
        '_14_day_total_sales_': float,
        '_14_day_newtobrand_orders_': float,
        '_14_day_newtobrand_sales': float,
        '_14_day_newtobrand_units_': float,
        'total_advertising_cost_of_sales_acos__click': float,
        'total_return_on_advertising_spend_roas__click': float,
        '_14_day_total_orders___click': float,
        '_14_day_total_units___click': float,
        '_14_day_total_sales__click': float,
        '_14_day_newtobrand_orders___click': float,
        '_14_day_newtobrand_sales__click': float,
        '_14_day_newtobrand_units___click': float,
        'newtobrand_detail_page_views': float,
        'newtobrand_detail_page_view_viewthrough_conversions': float,
        'newtobrand_detail_page_view_clickthrough_conversions': float,
        'newtobrand_detail_page_view_rate': float,
        'effective_cost_per_newtobrand_detail_page_view': float,
        '_14_day_atc': float,
        '_14_day_atc_views': float,
        '_14_day_atc_clicks': float,
        '_14_day_atcr': float,
        'effective_cost_per_add_to_cart_ecpatc': float,
        '_14_day_branded_searches': float,
        'branded_searches_viewthrough_conversions': float,
        'branded_searches_clickthrough_conversions': float,
        'branded_searches_rate': float,
        'effective_cost_per_branded_search': float
    }

    sdCampaignDf = sdCampaignDf.astype(schema)

    return sdCampaignDf

def unifiedRepo(filePath:str):
    unifiedDf = pd.read_csv(filePath, skiprows=7)
    unifiedDf = unifiedDf.rename(columns=lambda x:x.replace(' ','_').replace('-','_').replace('(','').replace(')','').replace('/','_'))

    unifiedDf['quantity'] = unifiedDf['quantity'].replace({np.nan:0},regex=True)
    colmChange = unifiedDf.columns[14:]
    unifiedDf[colmChange] = unifiedDf[colmChange].replace({',':''},regex=True)

    unifiedDf['date_time'] = pd.to_datetime(unifiedDf['date_time'].replace({' PDT':'', ' PST':''}, regex=True))
    unifiedDf['date_time'] = unifiedDf['date_time'].dt.tz_localize('America/Los_Angeles', ambiguous=True)

    req_columns = [
        'date_time',
        'settlement_id',
        'type',
        'order_id',
        'sku',
        'description',
        'quantity',
        'marketplace',
        'account_type',
        'fulfillment',
        'order_city',
        'order_state',
        'order_postal',
        'tax_collection_model',
        'product_sales',
        'product_sales_tax',
        'shipping_credits',
        'shipping_credits_tax',
        'gift_wrap_credits',
        'giftwrap_credits_tax',
        'Regulatory_Fee',
        'Tax_On_Regulatory_Fee',
        'promotional_rebates',
        'promotional_rebates_tax',
        'marketplace_withheld_tax',
        'selling_fees',
        'fba_fees',
        'other_transaction_fees',
        'other',
        'total'    
    ]

    for col in req_columns:
        if col not in unifiedDf.columns:
            unifiedDf[col] = np.nan

    unifiedDf = unifiedDf[req_columns]

    schema = {
        'date_time': 'datetime64[ns, America/Los_Angeles]',
        'settlement_id': str,
        'type': str,
        'order_id': str,
        'sku': str,
        'description': str,
        'quantity': int,
        'marketplace': str,
        'account_type': str,
        'fulfillment': str,
        'order_city': str,
        'order_state': str,
        'order_postal': str,
        'tax_collection_model': str,
        'product_sales': float,
        'product_sales_tax': float,
        'shipping_credits': float,
        'shipping_credits_tax': float,
        'gift_wrap_credits': float,
        'giftwrap_credits_tax': float,
        'Regulatory_Fee': float,
        'Tax_On_Regulatory_Fee': float,
        'promotional_rebates': float,
        'promotional_rebates_tax': float,
        'marketplace_withheld_tax': float,
        'selling_fees': float,
        'fba_fees': float,
        'other_transaction_fees': float,
        'other': float,
        'total': float
    }

    unifiedDf = unifiedDf.astype(schema)

    return unifiedDf

def storageFeeReport(filePath:str):
    try:
        storageFeeDf = pd.read_csv(filePath)
    except UnicodeDecodeError:
        storageFeeDf = pd.read_csv(filePath, encoding='ISO-8859-1')

    storageFeeDf['month_of_charge'] = pd.to_datetime(storageFeeDf['month_of_charge'])

    req_columns = [
        'asin',
        'fnsku',
        'product_name',
        'fulfillment_center',
        'country_code',
        'longest_side',
        'median_side',
        'shortest_side',
        'measurement_units',
        'weight',
        'weight_units',
        'item_volume',
        'volume_units',
        'product_size_tier',
        'average_quantity_on_hand',
        'average_quantity_pending_removal',
        'estimated_total_item_volume',
        'month_of_charge',
        'storage_utilization_ratio',
        'storage_utilization_ratio_units',
        'base_rate',
        'utilization_surcharge_rate',
        'avg_qty_for_sus',
        'est_vol_for_sus',
        'est_base_msf',
        'est_sus',
        'currency',
        'estimated_monthly_storage_fee',
        'dangerous_goods_storage_type',
        'eligible_for_inventory_discount',
        'qualifies_for_inventory_discount',
        'total_incentive_fee_amount',
        'breakdown_incentive_fee_amount',
        'average_quantity_customer_orders'
    ]

    for col in req_columns:
        if col not in storageFeeDf.columns:
            storageFeeDf[col] = np.nan

    storageFeeDf = storageFeeDf[req_columns]

    schema = {
        'asin': str,
        'fnsku': str,
        'product_name': str,
        'fulfillment_center': str,
        'country_code': str,
        'longest_side': float,
        'median_side': float,
        'shortest_side': float,
        'measurement_units': str,
        'weight': float,
        'weight_units': str,
        'item_volume': float,
        'volume_units': str,
        'product_size_tier': str,
        'average_quantity_on_hand': float,
        'average_quantity_pending_removal': float,
        'estimated_total_item_volume': float,
        'month_of_charge': 'datetime64[ns]',
        'storage_utilization_ratio': str,
        'storage_utilization_ratio_units': str,
        'base_rate': float,
        'utilization_surcharge_rate': float,
        'avg_qty_for_sus': float,
        'est_vol_for_sus': float,
        'est_base_msf': float,
        'est_sus': float,
        'currency': str,
        'estimated_monthly_storage_fee': float,
        'dangerous_goods_storage_type': str,
        'eligible_for_inventory_discount': str,
        'qualifies_for_inventory_discount': str,
        'total_incentive_fee_amount': float,
        'breakdown_incentive_fee_amount': str,
        'average_quantity_customer_orders': float
    }
    storageFeeDf = storageFeeDf.astype(schema)

    return storageFeeDf

def overAgeFeeReport(filepath:str):
    try:
        overAgeDf = pd.read_csv(filepath)
    except UnicodeDecodeError:
        overAgeDf = pd.read_csv(filepath, encoding='ISO-8859-1')

    overAgeDf = overAgeDf.rename(columns=lambda x:x.replace('-','_').lower())

    overAgeDf['snapshot_date'] = pd.to_datetime(overAgeDf['snapshot_date'])

    req_columns = [
        'snapshot_date',
        'sku',
        'fnsku',
        'asin',
        'product_name',
        'condition',
        'per_unit_volume',
        'currency',
        'volume_unit',
        'country',
        'qty_charged',
        'amount_charged',
        'surcharge_age_tier',
        'rate_surcharge'
    ]

    for col in req_columns:
        if col not in overAgeDf.columns:
            overAgeDf[col] = np.nan

    overAgeDf = overAgeDf[req_columns]

    schema = {
        'snapshot_date': 'datetime64[ns, UTC]',
        'sku': str,
        'fnsku': str,
        'asin': str,
        'product_name': str,
        'condition': str,
        'per_unit_volume': float,
        'currency': str,
        'volume_unit': str,
        'country': str,
        'qty_charged': float,
        'amount_charged': float,
        'surcharge_age_tier': str,
        'rate_surcharge': float
    }

    overAgeDf = overAgeDf.astype(schema)

    return overAgeDf

def returnProcessFeeReport(filepath:str):
    try:
        returnFeeDf = pd.read_csv(filepath)
    except UnicodeDecodeError:
        returnFeeDf = pd.read_csv(filepath, encoding='ISO-8859-1')

    returnFeeDf['month_of_charge'] = pd.to_datetime(returnFeeDf['month_of_charge'])
    returnFeeDf['month_of_shipment'] = pd.to_datetime(returnFeeDf['month_of_shipment'])

    req_columns = [
        'asin',
        'asin_fee_category',
        'fnsku',
        'product_name',
        'longest_side',
        'median_side',
        'shortest_side',
        'measurement-units',
        'unit_weight',
        'dimensional_weight',
        'shipping_weight',
        'weight_units',
        'sku_sizetier',
        'month_of_shipment',
        'asin_shipped_units',
        'asin_return_threshold_percent',
        'asin_return_threshold_units',
        'asin_returned_units',
        'sku_returned_units_NSP_exempted',
        'sku_returned_units_charged',
        'sku_fee_per_unit',
        'sku_returns_fee',
        'month_of_charge',
        'currency'
    ]

    for col in req_columns:
        if col not in returnFeeDf.columns:
            returnFeeDf[col] = np.nan

    returnFeeDf = returnFeeDf[req_columns]

    schema = {
        'asin': str,
        'asin_fee_category': str,
        'fnsku': str,
        'product_name': str,
        'longest_side': float,
        'median_side': float,
        'shortest_side': float,
        'measurement-units': str,
        'unit_weight': float,
        'dimensional_weight': float,
        'shipping_weight': float,
        'weight_units': str,
        'sku_sizetier': str,
        'month_of_shipment': 'datetime64[ns]',
        'asin_shipped_units': float,
        'asin_return_threshold_percent': float,
        'asin_return_threshold_units': float,
        'asin_returned_units': float,
        'sku_returned_units_NSP_exempted': float,
        'sku_returned_units_charged': float,
        'sku_fee_per_unit': float,
        'sku_returns_fee': float,
        'month_of_charge': 'datetime64[ns]',
        'currency': str
    }

    returnFeeDf = returnFeeDf.astype(schema)

    return returnFeeDf

def fbaFeeReport(filePath:str):
    try:
        fbaFeeDf = pd.read_csv(filePath)
    except UnicodeDecodeError:
        fbaFeeDf = pd.read_csv(filePath, encoding='ISO-8859-1')

    fbaFeeDf = fbaFeeDf.rename(columns=lambda x:x.replace('?"sku"','sku').replace('-','_').lower())
    fbaFeeDf.insert(0, 'date', datetime.now(timezone.utc).date())
    fbaFeeDf['date'] = pd.to_datetime(fbaFeeDf['date'])

    req_columns = [
        'date',
        'sku',
        'fnsku',
        'asin',
        'amazon_store',
        'product_name',
        'product_group',
        'brand',
        'fulfilled_by',
        'your_price',
        'sales_price',
        'longest_side',
        'median_side',
        'shortest_side',
        'length_and_girth',
        'unit_of_dimension',
        'item_package_weight',
        'unit_of_weight',
        'product_size_tier',
        'currency',
        'estimated_fee_total',
        'estimated_referral_fee_per_unit',
        'estimated_variable_closing_fee',
        'estimated_order_handling_fee_per_order',
        'estimated_pick_pack_fee_per_unit',
        'estimated_weight_handling_fee_per_unit',
        'expected_fulfillment_fee_per_unit'
    ]

    for col in req_columns:
        if col not in fbaFeeDf.columns:
            fbaFeeDf[col] = np.nan

    fbaFeeDf = fbaFeeDf[req_columns]

    schema = {
        'date': 'datetime64[ns]',
        'sku': str,
        'fnsku': str,
        'asin': str,
        'amazon_store': str,
        'product_name': str,
        'product_group': str,
        'brand': str,
        'fulfilled_by': str,
        'your_price': float,
        'sales_price': float,
        'longest_side': float,
        'median_side': float,
        'shortest_side': float,
        'length_and_girth': float,
        'unit_of_dimension': str,
        'item_package_weight': float,
        'unit_of_weight': str,
        'product_size_tier': str,
        'currency': str,
        'estimated_fee_total': float,
        'estimated_referral_fee_per_unit': float,
        'estimated_variable_closing_fee': str,
        'estimated_order_handling_fee_per_order': str,
        'estimated_pick_pack_fee_per_unit': str,
        'estimated_weight_handling_fee_per_unit': str,
        'expected_fulfillment_fee_per_unit': float
    }

    fbaFeeDf = fbaFeeDf.astype(schema)

    return fbaFeeDf

def inboundPlacementReport(filePath:str):
    try:
        inboundPlacementDf = pd.read_csv(filePath)
    except UnicodeDecodeError:
        inboundPlacementDf = pd.read_csv(filePath, encoding='ISO-8859-1')

    inboundPlacementDf = inboundPlacementDf.rename(columns=lambda x:x.replace('(','').replace(')','').replace(' ','_').lower())
    inboundPlacementDf['transaction_date'] = pd.to_datetime(inboundPlacementDf['transaction_date'])

    req_columns = [
        'transaction_date',
        'shipping_plan_id',
        'fba_shipment_id',
        'country',
        'fnsku',
        'asin',
        'planned_fba_inbound_placement_service',
        'planned_number_of_shipments',
        'compliant_number_of_shipments',
        'inbound_defect_type',
        'actual_charge_tier',
        'planned_inbound_region',
        'actual_inbound_region',
        'actual_received_quantity',
        'product_size_tier',
        'shipping_weight',
        'unit_of_weight',
        'fba_inbound_placement_service_fee_rate_per_unit',
        'eligible_applied_incentive',
        'currency',
        'total_fba_inbound_placement_service_fee_charge',
        'total_charges'
    ]

    for col in req_columns:
        if col not in inboundPlacementDf.columns:
            inboundPlacementDf[col] = np.nan

    inboundPlacementDf = inboundPlacementDf[req_columns]

    schema = {
        'transaction_date': 'datetime64[ns]',
        'shipping_plan_id': str,
        'fba_shipment_id': str,
        'country': str,
        'fnsku': str,
        'asin': str,
        'planned_fba_inbound_placement_service': str,
        'planned_number_of_shipments': float,
        'compliant_number_of_shipments': float,
        'inbound_defect_type': str,
        'actual_charge_tier': str,
        'planned_inbound_region': str,
        'actual_inbound_region': str,
        'actual_received_quantity': float,
        'product_size_tier': str,
        'shipping_weight': float,
        'unit_of_weight': str,
        'fba_inbound_placement_service_fee_rate_per_unit': float,
        'eligible_applied_incentive': float,
        'currency': str,
        'total_fba_inbound_placement_service_fee_charge': float,
        'total_charges': float
    }

    inboundPlacementDf = inboundPlacementDf.astype(schema)

    return inboundPlacementDf

def campAttribReport(filePath:str):
    attCampDf = pd.read_excel(filePath)
    attCampDf = attCampDf.rename(columns=lambda x:x.replace('14','_14').replace(' ','_').lower())

    req_columns = [
        'date',
        'advertiser_country',
        'order_currency',
        'advertiser',
        'publisher',
        'channel',
        'campaign_name',
        'ad_group_name',
        'clicks',
        '_14_day_total_dpv',
        '_14_day_total_atc',
        '_14_day_total_purchases',
        '_14_day_total_units_sold',
        '_14_day_total_sales_',
        '_14_day_total_dpvr_clicks',
        '_14_day_total_atcr_clicks',
        '_14_day_total_purchase_rate_clicks',
        '_14_day_dpv',
        '_14_day_atc',
        '_14_day_purchases',
        '_14_day_units_sold',
        '_14_day_product_sales'
    ]

    for col in req_columns:
        if col not in attCampDf.columns:
            attCampDf[col] = np.nan

    attCampDf = attCampDf[req_columns]

    schema = {
        'date': 'datetime64[ns]',
        'advertiser_country': str,
        'order_currency': str,
        'advertiser': str,
        'publisher': str,
        'channel': str,
        'campaign_name': str,
        'ad_group_name': str,
        'clicks': float,
        '_14_day_total_dpv': float,
        '_14_day_total_atc': float,
        '_14_day_total_purchases': float,
        '_14_day_total_units_sold': float,
        '_14_day_total_sales_': float,
        '_14_day_total_dpvr_clicks': float,
        '_14_day_total_atcr_clicks': float,
        '_14_day_total_purchase_rate_clicks': float,
        '_14_day_dpv': float,
        '_14_day_atc': float,
        '_14_day_purchases': float,
        '_14_day_units_sold': float,
        '_14_day_product_sales': float
    }

    attCampDf = attCampDf.astype(schema)

    return attCampDf

def invWarehouseLoc(filePath:str):
    invWarehouseDf = pd.read_csv(filePath)
    invWarehouseDf = invWarehouseDf.rename(columns=lambda x:x.replace(' ','_').replace('/','_').lower())

    invWarehouseDf['date'] = pd.to_datetime(invWarehouseDf['date'])

    req_columns = [
        'date',
        'fnsku',
        'asin',
        'msku',
        'title',
        'disposition',
        'starting_warehouse_balance',
        'in_transit_between_warehouses',
        'receipts',
        'customer_shipments',
        'customer_returns',
        'vendor_returns',
        'warehouse_transfer_in_out',
        'found',
        'lost',
        'damaged',
        'disposed',
        'other_events',
        'ending_warehouse_balance',
        'unknown_events',
        'location',
        'store'
    ]

    for col in req_columns:
        if col not in invWarehouseDf.columns:
            invWarehouseDf[col] = np.nan

    invWarehouseDf = invWarehouseDf[req_columns]

    schema = {
        'date': 'datetime64[ns]',
        'fnsku': str,
        'asin': str,
        'msku': str,
        'title': str,
        'disposition': str,
        'starting_warehouse_balance': float,
        'in_transit_between_warehouses': float,
        'receipts': float,
        'customer_shipments': float,
        'customer_returns': float,
        'vendor_returns': float,
        'warehouse_transfer_in_out': float,
        'found': float,
        'lost': float,
        'damaged': float,
        'disposed': float,
        'other_events': float,
        'ending_warehouse_balance': float,
        'unknown_events': float,
        'location': str,
        'store': str
    }

    invWarehouseDf = invWarehouseDf.astype(schema)
    return invWarehouseDf

