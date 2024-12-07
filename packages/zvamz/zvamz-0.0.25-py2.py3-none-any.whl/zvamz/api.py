import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import time
from .ratelimit import RateLimiter
from .fcmap import fc_to_country
from .marketplaces import marketplaces
import gzip
import shutil
import os
import urllib.parse

def zv_client_access(username, region):
    """
    This is authentication process for amazon.
    Only works for ZV Data Automation Clients
    """
    url = "https://zvdataautomation.com//zvapiauth/"
    payload = {"username": username, "region": region}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        access_token = response.json()['access_token']
        print('Access Token granted 1 hour validity.')
        return access_token
    else:
        return ValueError('Error: Not Authenticated')
    
def shipment_status(marketplace_action, access_token, past_days):
    """
    This will pull all shipment and its status for specified marketplace

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - past_days: number of days from today's date (UTC)

    return:
    - data frame of the list of shipments and its status
    """
    ShipmentStatusLists =[
        'WORKING', 'READY_TO_SHIP', 'SHIPPED', 'RECEIVING',
        'CANCELLED', 'DELETED', 'CLOSED', 'ERROR',
        'IN_TRANSIT', 'DELIVERED', 'CHECKED_IN'
    ]

    rate_limiter = RateLimiter(tokens_per_second=2, capacity=30)
    NextToken = None
    records = []

    regionUrl, MarketplaceId = marketplace_action()
    endpoint = '/fba/inbound/v0/shipments'
    url = regionUrl + endpoint
    headers = {
        'x-amz-access-token': access_token,
        'Content-Type': 'application/json'
    }

    LastUpdatedAfter = (datetime.now(timezone.utc) - timedelta(days=past_days)).isoformat()
    LastUpdatedBefore = datetime.now(timezone.utc).isoformat()

    for ShipmentStatusList in ShipmentStatusLists:
        request_params = {
            'MarketplaceId': MarketplaceId,
            'QueryType': 'DATE_RANGE',
            'ShipmentStatusList': ShipmentStatusList,
            'LastUpdatedAfter': LastUpdatedAfter,
            'LastUpdatedBefore': LastUpdatedBefore,
            'NextToken': NextToken
        }

        try:
            response = requests.get(url, headers=headers, params=request_params)
            records.extend(response.json()['payload']['ShipmentData'])

            try:
                NextToken = response.json()['payload']['NextToken']
            except:
                NextToken = None

            while NextToken:
                request_params_next = {
                    'MarketplaceId': MarketplaceId,
                    'QueryType': 'NEXT_TOKEN',
                    'NextToken': NextToken
                }
                response = rate_limiter.send_request(requests.get, url, headers=headers, params=request_params_next)
                records.extend(response.json()['payload']['ShipmentData'])

                try:
                    NextToken = response.json()['payload']['NextToken']
                except:
                    NextToken = None

            print('end of list')

        except Exception as e:            
            print(response.json()['errors'][0]['message'])
            print(response.json()['errors'][0]['details'])

    shipments = []
    for record in records:
        shipments.append({
            'shipment_id': record['ShipmentId'],
            'shipment_name': record['ShipmentName'],
            'shipment_status': record['ShipmentStatus'],
            'destination_fulfillment_center': record['DestinationFulfillmentCenterId']
        })

    df = pd.DataFrame(shipments)
    df['country'] = df['destination_fulfillment_center'].map(fc_to_country)

    return df

def shipment_items(marketplace_action, access_token, past_days):
    """
    This will pull all shipment and items inside it for specified marketplace.
    Together with the quantity shipped vs received

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - past_days: number of days from today's date (UTC)

    return:
    - data frame of the list of shipments and items inside it
    """
    rate_limiter = RateLimiter(tokens_per_second=2, capacity=30)
    NextToken = None
    records = []


    regionUrl, marketplace_id = marketplace_action()
    endpoint = f'/fba/inbound/v0/shipmentItems'
    url = regionUrl + endpoint
    headers = {
        'x-amz-access-token': access_token,
        'Content-Type': 'application/json'
    }

    LastUpdatedAfter = (datetime.now(timezone.utc) - timedelta(days=past_days)).isoformat()
    LastUpdatedBefore = datetime.now(timezone.utc).isoformat()

    request_params = {
        'MarketplaceId': marketplace_id,
        'LastUpdatedAfter': LastUpdatedAfter,
        'LastUpdatedBefore': LastUpdatedBefore,
        'QueryType': 'DATE_RANGE'
    }
    
    try:
        response = requests.get(url, headers=headers, params=request_params)
        records.extend(response.json()['payload']['ItemData'])

        try:
            NextToken = response.json()['payload']['NextToken']
        except:
            NextToken = None

        while NextToken:
            request_params_next = {
                'MarketplaceId': marketplace_id,
                'QueryType': 'NEXT_TOKEN',
                'NextToken': NextToken
            }
            response = rate_limiter.send_request(requests.get, url, headers=headers, params=request_params_next)
            records.extend(response.json()['payload']['ItemData'])

            try:
                NextToken = response.json()['payload']['NextToken']
            except:
                NextToken = None

        print('end of list')

    except Exception as e:
        print(response.json()['errors'][0]['message'])
        print(response.json()['errors'][0]['details'])

    df = []
    for record in records:

        if len(record['PrepDetailsList']) > 0:
            df.append({
                'shipment_id': record['ShipmentId'],
                'sku': record['SellerSKU'],
                'fnsku': record['FulfillmentNetworkSKU'],
                'shipped_qty': record['QuantityShipped'],
                'received_qty': record['QuantityReceived'],
                'case_qty': record['QuantityInCase'],
                'prep_instruction': record['PrepDetailsList'][0]['PrepInstruction'],
                'prep_owner': record['PrepDetailsList'][0]['PrepOwner']
            })
        else:
            df.append({
                'shipment_id': record['ShipmentId'],
                'sku': record['SellerSKU'],
                'fnsku': record['FulfillmentNetworkSKU'],
                'shipped_qty': record['QuantityShipped'],
                'received_qty': record['QuantityReceived'],
                'case_qty': record['QuantityInCase'],
                'prep_instruction': np.nan,
                'prep_owner': np.nan
            })
    shipmentItemsDf = pd.DataFrame(df)
    return shipmentItemsDf 

def shipment_summary(marketplace_action, access_token, past_days):
    """
    This will pull all shipment and items inside it for specified marketplace.
    And Summarise the Report

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - past_days: number of days from today's date (UTC)

    return:
    - data frame of the report summary
    """
    shipmentDf = shipment_status(marketplace_action, access_token, past_days)
    shipmentItemsDf = shipment_items(marketplace_action, access_token, past_days)

    shipmentSummaryDf = shipmentDf.merge(shipmentItemsDf, how='inner', on='shipment_id')
    shipmentSummaryDf.insert(0,'date',datetime.now(timezone.utc).strftime('%F'))

    schema = {
        'date': 'datetime64[ns]',
        'shipment_id': str,
        'shipment_name': str,
        'shipment_status': str,
        'destination_fulfillment_center': str,
        'country': str,
        'sku': str,
        'fnsku': str,
        'shipped_qty': float,
        'received_qty': float,
        'case_qty': float,
        'prep_instruction': str,
        'prep_owner': str
    }
    shipmentSummaryDf = shipmentSummaryDf.astype(schema)

    return shipmentSummaryDf

def narf_eligibility(access_token, file_path_name):
    """
    This will pull the report for NARF eligibility of the SKUs

    Parameter:
    - access_token: matching access token of the marketplace
    - file_path_name: the file path where to save the report up to its file name

    return:
    - data frame of the NARF Eligibility report
    """
    # Create Report
    regionUrl, marketplace_id = marketplaces.US()
    endpoint = f'/reports/2021-06-30/reports'
    url = regionUrl + endpoint
    headers = {
        'x-amz-access-token': access_token,
        'Content-Type': 'application/json'
    }

    request_params = {
        'marketplaceIds': [marketplace_id],
        'reportType': 'GET_REMOTE_FULFILLMENT_ELIGIBILITY'
    }

    create_response = requests.post(url, headers=headers, json=request_params,)
    report_id = create_response.json()['reportId']

    # Check Report Status
    endpoint = f'/reports/2021-06-30/reports/{report_id}'
    url = regionUrl + endpoint

    while True:
        status_response = requests.get(url, headers=headers)
        status = status_response.json().get("processingStatus")
        
        if status == "DONE":
            print("Report is ready for download!")
            document_id = status_response.json()["reportDocumentId"]
            break
        elif status == "CANCELLED":
            raise ValueError("Report creation was cancelled.")
        elif status == "FATAL":
            raise ValueError("Report creation failed.")
        else:
            print(f"Report status: {status}. Waiting for report to be ready...")
            time.sleep(60)  # Wait before checking again

    # Download Report
    endpoint = f'/reports/2021-06-30/documents/{document_id}'
    url = regionUrl + endpoint
    document_response = requests.get(url, headers=headers)

    if document_response.status_code == 200:
        download_url = document_response.json()["url"]
        report_data = requests.get(download_url)

        with open(file_path_name, "wb") as f:
            f.write(report_data.content)
    else:
        print("Failed to get the report document:", document_response.json())

    #prepare DF
    narfDf = pd.read_excel(file_path_name,sheet_name='Enrollment',skiprows=3)
    narfDf = narfDf.rename(columns=lambda x:x.replace('.1','').replace('.2','').replace('(Yes/No)','')
                                    .replace(' Brazil ','').replace(' Canada ','').replace(' Mexico ','')
                                    .replace('/','_').replace(' ','_')
                                    .lower())

    brNarfDf = narfDf.iloc[:,:6]
    brNarfDf.insert(0,'marketplace','Brazil')

    caNarfDf = pd.concat([narfDf.iloc[:,:3],narfDf.iloc[:,6:9]], axis = 1)
    caNarfDf.insert(0,'marketplace','Canada')

    mxNarfDf = pd.concat([narfDf.iloc[:,:3],narfDf.iloc[:,9:12]], axis = 1)
    mxNarfDf.insert(0,'marketplace','Mexico')

    narfFinalDf = pd.concat([brNarfDf,caNarfDf,mxNarfDf], axis=0, ignore_index=True)
    narfFinalDf.insert(0,'date',datetime.now(timezone.utc).strftime('%F'))

    schema = {
        'date': 'datetime64[ns]',
    'marketplace': str,
    'merchant_sku': str,
    'asin': str,
    'product_name': str,
    'offer_status': str,
    'more_details': str,
    'enable_disable': str
    }

    narfFinalDf = narfFinalDf.astype(schema)

    return narfFinalDf

def fba_inventory(marketplace_action, access_token, file_path, marketplace_ids):
    """
    This will pull all FBA Inventory Report for the sepcified marketplaces

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - file_path: the specific file path where to save the raw report Example: '/content'
    - marketplace_ids: lists of marketplace ids

    return:
    - data frame of FBA Inventory Report for all marketplaces
    """
    id_count = len(marketplace_ids)
    counter = 1
    # pulling of report
    for marketplace_id in marketplace_ids:
        print('Preparing for report request.')
        # set file path
        file_path_name = os.path.join(file_path, (marketplace_id + '_fbaInv.txt'))
        # Create Report
        regionUrl, mid = marketplace_action()
        endpoint = f'/reports/2021-06-30/reports'
        url = regionUrl + endpoint
        headers = {
            'x-amz-access-token': access_token,
            'Content-Type': 'application/json'
        }

        request_params = {
            'marketplaceIds': [marketplace_id],
            'reportType': 'GET_FBA_INVENTORY_PLANNING_DATA'
        }

        create_response = requests.post(url, headers=headers, json=request_params,)
        report_id = create_response.json()['reportId']

        # Check Report Status
        endpoint = f'/reports/2021-06-30/reports/{report_id}'
        url = regionUrl + endpoint

        while True:
            status_response = requests.get(url, headers=headers)
            status = status_response.json().get("processingStatus")
            
            if status == "DONE":
                print("Report is ready for download!")
                document_id = status_response.json()["reportDocumentId"]
                break
            elif status == "CANCELLED":
                raise ValueError("Report creation was cancelled.")
            elif status == "FATAL":
                raise ValueError("Report creation failed.")
            else:
                print(f"Report status: {status}. Waiting for report to be ready...")
                time.sleep(60)  # Wait before checking again

        # Download Report
        endpoint = f'/reports/2021-06-30/documents/{document_id}'
        url = regionUrl + endpoint
        document_response = requests.get(url, headers=headers)

        if document_response.status_code == 200:
            download_url = document_response.json()["url"]
            report_data = requests.get(download_url)

            with open(file_path_name, "wb") as f:
                f.write(report_data.content)
        else:
            print("Failed to get the report document:", document_response.json())
        
        if counter < id_count:
            time.sleep(1200) #Wait before next report
            counter = counter + 1

    # create df
    fbaInvDf = []

    for marketplace_id in marketplace_ids:
        file_path_name = os.path.join(file_path, (marketplace_id + '_fbaInv.txt'))
        fbaInvInitDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t')
        fbaInvDf.append(fbaInvInitDf)

    fbaInvFinalDf = pd.concat(fbaInvDf, ignore_index=True)
    fbaInvFinalDf = fbaInvFinalDf.rename(columns=lambda x:x.replace('-','_').replace('?','').replace('(','')
                                        .replace(')','').replace(' ','').lower())

    req_columns = [
        'snapshot_date',
        'sku',
        'fnsku',
        'asin',
        'product_name',
        'condition',
        'available',
        'pending_removal_quantity',
        'inv_age_0_to_90_days',
        'inv_age_91_to_180_days',
        'inv_age_181_to_270_days',
        'inv_age_271_to_365_days',
        'inv_age_365_plus_days',
        'currency',
        'units_shipped_t7',
        'units_shipped_t30',
        'units_shipped_t60',
        'units_shipped_t90',
        'alert',
        'your_price',
        'sales_price',
        'lowest_price_new_plus_shipping',
        'lowest_price_used',
        'recommended_action',
        'deprecatedhealthy_inventory_level',
        'recommended_sales_price',
        'recommended_sale_duration_days',
        'recommended_removal_quantity',
        'estimated_cost_savings_of_recommended_actions',
        'sell_through',
        'item_volume',
        'volume_unit_measurement',
        'storage_type',
        'storage_volume',
        'marketplace',
        'product_group',
        'sales_rank',
        'days_of_supply',
        'estimated_excess_quantity',
        'weeks_of_cover_t30',
        'weeks_of_cover_t90',
        'featuredoffer_price',
        'sales_shipped_last_7_days',
        'sales_shipped_last_30_days',
        'sales_shipped_last_60_days',
        'sales_shipped_last_90_days',
        'inv_age_0_to_30_days',
        'inv_age_31_to_60_days',
        'inv_age_61_to_90_days',
        'inv_age_181_to_330_days',
        'inv_age_331_to_365_days',
        'estimated_storage_cost_next_month',
        'inbound_quantity',
        'inbound_working',
        'inbound_shipped',
        'inbound_received',
        'no_sale_last_6_months',
        'totalreservedquantity',
        'unfulfillable_quantity',
        'quantity_to_be_charged_ais_181_210_days',
        'estimated_ais_181_210_days',
        'quantity_to_be_charged_ais_211_240_days',
        'estimated_ais_211_240_days',
        'quantity_to_be_charged_ais_241_270_days',
        'estimated_ais_241_270_days',
        'quantity_to_be_charged_ais_271_300_days',
        'estimated_ais_271_300_days',
        'quantity_to_be_charged_ais_301_330_days',
        'estimated_ais_301_330_days',
        'quantity_to_be_charged_ais_331_365_days',
        'estimated_ais_331_365_days',
        'quantity_to_be_charged_ais_365_plus_days',
        'estimated_ais_365_plus_days',
        'historical_days_of_supply',
        'fba_minimum_inventory_level',
        'fba_inventory_level_health_status',
        'recommendedship_inquantity',
        'recommendedship_indate',
        'lastupdateddateforhistoricaldaysofsupply',
        'exemptedfromlow_inventory_levelfee',
        'low_inventory_levelfeeappliedincurrentweek',
        'shorttermhistoricaldaysofsupply',
        'longtermhistoricaldaysofsupply',
        'inventoryagesnapshotdate',
        'inventorysupplyatfba',
        'reservedfctransfer',
        'reservedfcprocessing',
        'reservedcustomerorder',
        'totaldaysofsupplyincludingunitsfromopenshipments',
        'healthy_inventory_level'
    ]

    for col in req_columns:
        if col not in fbaInvFinalDf.columns:
            fbaInvFinalDf[col] = np.nan

    fbaInvFinalDf = fbaInvFinalDf[req_columns]

    schema = {
        'snapshot_date': 'datetime64[ns]',
        'sku': str,
        'fnsku': str,
        'asin': str,
        'product_name': str,
        'condition': str,
        'available': float,
        'pending_removal_quantity': float,
        'inv_age_0_to_90_days': float,
        'inv_age_91_to_180_days': float,
        'inv_age_181_to_270_days': float,
        'inv_age_271_to_365_days': float,
        'inv_age_365_plus_days': float,
        'currency': str,
        'units_shipped_t7': float,
        'units_shipped_t30': float,
        'units_shipped_t60': float,
        'units_shipped_t90': float,
        'alert': str,
        'your_price': float,
        'sales_price': float,
        'lowest_price_new_plus_shipping': float,
        'lowest_price_used': float,
        'recommended_action': str,
        'deprecatedhealthy_inventory_level': float,
        'recommended_sales_price': float,
        'recommended_sale_duration_days': float,
        'recommended_removal_quantity': float,
        'estimated_cost_savings_of_recommended_actions': float,
        'sell_through': float,
        'item_volume': float,
        'volume_unit_measurement': str,
        'storage_type': str,
        'storage_volume': float,
        'marketplace': str,
        'product_group': str,
        'sales_rank': float,
        'days_of_supply': float,
        'estimated_excess_quantity': float,
        'weeks_of_cover_t30': float,
        'weeks_of_cover_t90': float,
        'featuredoffer_price': float,
        'sales_shipped_last_7_days': float,
        'sales_shipped_last_30_days': float,
        'sales_shipped_last_60_days': float,
        'sales_shipped_last_90_days': float,
        'inv_age_0_to_30_days': float,
        'inv_age_31_to_60_days': float,
        'inv_age_61_to_90_days': float,
        'inv_age_181_to_330_days': float,
        'inv_age_331_to_365_days': float,
        'estimated_storage_cost_next_month': float,
        'inbound_quantity': float,
        'inbound_working': float,
        'inbound_shipped': float,
        'inbound_received': float,
        'no_sale_last_6_months': float,
        'totalreservedquantity': float,
        'unfulfillable_quantity': float,
        'quantity_to_be_charged_ais_181_210_days': float,
        'estimated_ais_181_210_days': float,
        'quantity_to_be_charged_ais_211_240_days': float,
        'estimated_ais_211_240_days': float,
        'quantity_to_be_charged_ais_241_270_days': float,
        'estimated_ais_241_270_days': float,
        'quantity_to_be_charged_ais_271_300_days': float,
        'estimated_ais_271_300_days': float,
        'quantity_to_be_charged_ais_301_330_days': float,
        'estimated_ais_301_330_days': float,
        'quantity_to_be_charged_ais_331_365_days': float,
        'estimated_ais_331_365_days': float,
        'quantity_to_be_charged_ais_365_plus_days': float,
        'estimated_ais_365_plus_days': float,
        'historical_days_of_supply': float,
        'fba_minimum_inventory_level': float,
        'fba_inventory_level_health_status': str,
        'recommendedship_inquantity': float,
        'recommendedship_indate': 'datetime64[ns]',
        'lastupdateddateforhistoricaldaysofsupply': 'datetime64[ns]',
        'exemptedfromlow_inventory_levelfee': str,
        'low_inventory_levelfeeappliedincurrentweek': str,
        'shorttermhistoricaldaysofsupply': float,
        'longtermhistoricaldaysofsupply': float,
        'inventoryagesnapshotdate': 'datetime64[ns]',
        'inventorysupplyatfba': float,
        'reservedfctransfer': float,
        'reservedfcprocessing': float,
        'reservedcustomerorder': float,
        'totaldaysofsupplyincludingunitsfromopenshipments': float,
        'healthy_inventory_level': float
    }

    fbaInvFinalDf = fbaInvFinalDf.astype(schema)

    return fbaInvFinalDf

def all_orders(marketplace_action, access_token, file_path_name, past_days):
    """
    This will pull all orders report per region.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - file_path_name: the file path where to save the report up to its file name
    - past_days: number of days from today's date (UTC)

    return:
    - data frame of all orders report
    """
    # Create Report
    regionUrl , marketplace_id = marketplace_action()
    endpoint = f'/reports/2021-06-30/reports'
    url = regionUrl + endpoint
    headers = {
        'x-amz-access-token': access_token,
        'Content-Type': 'application/json'
    }

    dataStartTime = (datetime.now(timezone.utc) - timedelta(days=past_days)).isoformat()

    request_params = {
        'marketplaceIds': [marketplace_id],
        'reportType': 'GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL',
        'dataStartTime': dataStartTime
    }

    create_response = requests.post(url, headers=headers, json=request_params,)
    report_id = create_response.json()['reportId']

    # Check Report Status
    endpoint = f'/reports/2021-06-30/reports/{report_id}'
    url = regionUrl + endpoint

    while True:
        status_response = requests.get(url, headers=headers)
        status = status_response.json().get("processingStatus")

        if status == "DONE":
            print("Report is ready for download!")
            document_id = status_response.json()["reportDocumentId"]
            break
        elif status == "CANCELLED":
            raise ValueError("Report creation was cancelled.")
        elif status == "FATAL":
            raise ValueError("Report creation failed.")
        else:
            print(f"Report status: {status}. Waiting for report to be ready...")
            time.sleep(60)  # Wait before checking again

    # Download Report
    endpoint = f'/reports/2021-06-30/documents/{document_id}'
    url = regionUrl + endpoint
    document_response = requests.get(url, headers=headers)

    if document_response.status_code == 200:
        download_url = document_response.json()["url"]
        compression_algorithm = document_response.json().get("compressionAlgorithm")
        report_data = requests.get(download_url)
        
        if compression_algorithm == "GZIP":
            print('Decompressing...')

            with open(file_path_name + '.gz', 'wb') as f:
                f.write(report_data.content)

            with gzip.open(file_path_name + '.gz', 'rb') as f_in:
                with open(file_path_name, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        else:
            with open(file_path_name, 'wb') as f:
                f.write(report_data.content)

        print('Report Downloaded!')

    else:
        print("Failed to get the report document:", document_response.json())

    # Process DF
    allOrdersDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t')
    allOrdersDf = allOrdersDf.rename(columns=lambda x:x.replace('-','_').replace(' ','_').lower())
    allOrdersDf['purchase_date'] = pd.to_datetime(allOrdersDf['purchase_date'])
    allOrdersDf['last_updated_date'] = pd.to_datetime(allOrdersDf['last_updated_date'])

    req_columns = [
        'amazon_order_id',
        'merchant_order_id',
        'purchase_date',
        'last_updated_date',
        'order_status',
        'fulfillment_channel',
        'sales_channel',
        'order_channel',
        'ship_service_level',
        'product_name',
        'sku',
        'asin',
        'number_of_items',
        'item_status',
        'tax_collection_model',
        'tax_collection_responsible_party',
        'quantity',
        'currency',
        'item_price',
        'item_tax',
        'shipping_price',
        'shipping_tax',
        'gift_wrap_price',
        'gift_wrap_tax',
        'item_promotion_discount',
        'ship_promotion_discount',
        'address_type',
        'ship_city',
        'ship_state',
        'ship_postal_code',
        'ship_country',
        'promotion_ids',
        'payment_method_details',
        'cpf',
        'item_extensions_data',
        'is_business_order',
        'purchase_order_number',
        'price_designation',
        'buyer_company_name',
        'is_replacement_order',
        'is_exchange_order',
        'original_order_id',
        'license_state',
        'license_expiration_date',
        'is_buyer_requested_cancellation',
        'buyer_requested_cancel_reason',
        'is_transparency',
        'ioss_number',
        'signature_confirmation_recommended'
    ]

    for col in req_columns:
        if col not in allOrdersDf.columns:
            allOrdersDf[col] = np.nan

    allOrdersDf = allOrdersDf[req_columns]

    schema = {
        'amazon_order_id': str,
        'merchant_order_id': str,
        'purchase_date': 'datetime64[ns, UTC]',
        'last_updated_date': 'datetime64[ns, UTC]',
        'order_status': str,
        'fulfillment_channel': str,
        'sales_channel': str,
        'order_channel': str,
        'ship_service_level': str,
        'product_name': str,
        'sku': str,
        'asin': str,
        'number_of_items': float,
        'item_status': str,
        'tax_collection_model': str,
        'tax_collection_responsible_party': str,
        'quantity': float,
        'currency': str,
        'item_price': float,
        'item_tax': float,
        'shipping_price': float,
        'shipping_tax': float,
        'gift_wrap_price': float,
        'gift_wrap_tax': float,
        'item_promotion_discount': float,
        'ship_promotion_discount': float,
        'address_type': str,
        'ship_city': str,
        'ship_state': str,
        'ship_postal_code': str,
        'ship_country': str,
        'promotion_ids': str,
        'payment_method_details': str,
        'cpf': str,
        'item_extensions_data': str,
        'is_business_order': bool,
        'purchase_order_number': str,
        'price_designation': str,
        'buyer_company_name': str,
        'is_replacement_order': bool,
        'is_exchange_order': bool,
        'original_order_id': str,
        'license_state': str,
        'license_expiration_date': str,
        'is_buyer_requested_cancellation': bool,
        'buyer_requested_cancel_reason': str,
        'is_transparency': bool,
        'ioss_number': str,
        'signature_confirmation_recommended': bool
    }

    allOrdersDf = allOrdersDf.astype(schema)

    return allOrdersDf

def reimbursement_report(marketplace_action, access_token, file_path_name, past_days):
    """
    This will pull reimbursement report per region.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - file_path_name: the file path where to save the report up to its file name
    - past_days: number of days from today's date (UTC)

    return:
    - data frame of reimbursement report
    """
    # Create Report
    regionUrl, marketplace_id = marketplace_action()
    endpoint = f'/reports/2021-06-30/reports'
    url = regionUrl + endpoint
    headers = {
        'x-amz-access-token': access_token,
        'Content-Type': 'application/json'
    }

    dataStartTime = (datetime.now(timezone.utc) - timedelta(days=past_days)).isoformat()

    request_params = {
        'marketplaceIds': [marketplace_id],
        'reportType': 'GET_FBA_REIMBURSEMENTS_DATA',
        'dataStartTime': dataStartTime
    }

    create_response = requests.post(url, headers=headers, json=request_params,)
    report_id = create_response.json()['reportId']

    # Check Report Status
    endpoint = f'/reports/2021-06-30/reports/{report_id}'
    url = regionUrl + endpoint

    while True:
        status_response = requests.get(url, headers=headers)
        status = status_response.json().get("processingStatus")

        if status == "DONE":
            print("Report is ready for download!")
            document_id = status_response.json()["reportDocumentId"]
            break
        elif status == "CANCELLED":
            raise ValueError("Report creation was cancelled.")
        elif status == "FATAL":
            raise ValueError("Report creation failed.")
        else:
            print(f"Report status: {status}. Waiting for report to be ready...")
            time.sleep(60)  # Wait before checking again

    # Download Report
    endpoint = f'/reports/2021-06-30/documents/{document_id}'
    url = regionUrl + endpoint
    document_response = requests.get(url, headers=headers)

    if document_response.status_code == 200:
        download_url = document_response.json()["url"]
        compression_algorithm = document_response.json().get("compressionAlgorithm")
        report_data = requests.get(download_url)
        
        if compression_algorithm == "GZIP":
            print('Decompressing...')

            with open(file_path_name + '.gz', 'wb') as f:
                f.write(report_data.content)

            with gzip.open(file_path_name + '.gz', 'rb') as f_in:
                with open(file_path_name, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        else:
            with open(file_path_name, 'wb') as f:
                f.write(report_data.content)

        print('Report Downloaded!')
    else:
        print("Failed to get the report document:", document_response.json())

    # Data Frame
    try:
        reimbursementDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t')
    except:
        reimbursementDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t', encoding='ISO-8859-1')

    reimbursementDf = reimbursementDf.rename(columns=lambda x:x.replace('-','_').replace(' ','_').lower())
    reimbursementDf['approval_date'] = pd.to_datetime(reimbursementDf['approval_date'])

    req_columns = [
        'approval_date',
        'reimbursement_id',
        'case_id',
        'amazon_order_id',
        'reason',
        'sku',
        'fnsku',
        'asin',
        'product_name',
        'condition',
        'currency_unit',
        'amount_per_unit',
        'amount_total',
        'quantity_reimbursed_cash',
        'quantity_reimbursed_inventory',
        'quantity_reimbursed_total',
        'original_reimbursement_id',
        'original_reimbursement_type'
    ]

    for col in req_columns:
        if col not in reimbursementDf.columns:
            reimbursementDf[col] = np.nan

    reimbursementDf = reimbursementDf[req_columns]

    schema = {
        'approval_date': 'datetime64[ns, UTC]',
        'reimbursement_id': str,
        'case_id': str,
        'amazon_order_id': str,
        'reason': str,
        'sku': str,
        'fnsku': str,
        'asin': str,
        'product_name': str,
        'condition': str,
        'currency_unit': str,
        'amount_per_unit': float,
        'amount_total': float,
        'quantity_reimbursed_cash': float,
        'quantity_reimbursed_inventory': float,
        'quantity_reimbursed_total': float,
        'original_reimbursement_id': str,
        'original_reimbursement_type': str,
    }

    reimbursementDf = reimbursementDf.astype(schema)

    return reimbursementDf

def inv_ledger(marketplace_action, access_token, file_path_name, past_days):
    """
    This will pull inventory ledger report.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - file_path_name: the file path where to save the report up to its file name
    - past_days: number of days from today's date (UTC)

    return:
    - data frame of inventory ledger report
    """

    # Create Report
    regionUrl, marketplace_id = marketplace_action()
    endpoint = f'/reports/2021-06-30/reports'
    url = regionUrl + endpoint
    headers = {
        'x-amz-access-token': access_token,
        'Content-Type': 'application/json'
    }

    dataStartTime = (datetime.now(timezone.utc) - timedelta(days=past_days)).isoformat()

    request_params = {
        'marketplaceIds': [marketplace_id],
        'reportType': 'GET_LEDGER_DETAIL_VIEW_DATA',
        'dataStartTime': dataStartTime
    }

    create_response = requests.post(url, headers=headers, json=request_params,)
    report_id = create_response.json()['reportId']

    # Check Report Status
    endpoint = f'/reports/2021-06-30/reports/{report_id}'
    url = regionUrl + endpoint

    while True:
        status_response = requests.get(url, headers=headers)
        status = status_response.json().get("processingStatus")

        if status == "DONE":
            print("Report is ready for download!")
            document_id = status_response.json()["reportDocumentId"]
            break
        elif status == "CANCELLED":
            raise ValueError("Report creation was cancelled.")
        elif status == "FATAL":
            raise ValueError("Report creation failed.")
        else:
            print(f"Report status: {status}. Waiting for report to be ready...")
            time.sleep(60)  # Wait before checking again

    # Download Report
    endpoint = f'/reports/2021-06-30/documents/{document_id}'
    url = regionUrl + endpoint
    document_response = requests.get(url, headers=headers)

    if document_response.status_code == 200:
        download_url = document_response.json()["url"]
        compression_algorithm = document_response.json().get("compressionAlgorithm")
        report_data = requests.get(download_url)

        if compression_algorithm == "GZIP":
            print('Decompressing...')

            with open(file_path_name + '.gz', 'wb') as f:
                f.write(report_data.content)

            with gzip.open(file_path_name + '.gz', 'rb') as f_in:
                with open(file_path_name, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        else:
            with open(file_path_name, 'wb') as f:
                f.write(report_data.content)

        print('Report Downloaded!')
    else:
        print("Failed to get the report document:", document_response.json())

    # Data Frame
    try:
        ledgerDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t')
    except:
        ledgerDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t', encoding='ISO-8859-1')

    ledgerDf = ledgerDf.rename(columns=lambda x:x.replace(' ','_').lower())
    ledgerDf['date'] = pd.to_datetime(ledgerDf['date'])

    req_columns = [
        'date',
        'fnsku',
        'asin',
        'msku',
        'title',
        'event_type',
        'reference_id',
        'quantity',
        'fulfillment_center',
        'disposition',
        'reason',
        'country',
        'reconciled_quantity',
        'unreconciled_quantity',
        'date_and_time',
        'store'
    ]

    for col in req_columns:
        if col not in ledgerDf.columns:
            ledgerDf[col] = np.nan

    ledgerDf = ledgerDf[req_columns]

    schema = {
        'date': 'datetime64[ns]',
        'fnsku': str,
        'asin': str,
        'msku': str,
        'title': str,
        'event_type': str,
        'reference_id': str,
        'quantity': float,
        'fulfillment_center': str,
        'disposition': str,
        'reason': str,
        'country': str,
        'reconciled_quantity': float,
        'unreconciled_quantity': float,
        'date_and_time': 'datetime64[ns, UTC]',
        'store': str
    }

    ledgerDf = ledgerDf.astype(schema)

    return ledgerDf

def customer_return(marketplace_action, access_token, file_path_name, past_days):
    """
    This will pull customer return report.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - file_path_name: the file path where to save the report up to its file name
    - past_days: number of days from today's date (UTC)

    return:
    - data frame of customer return report
    """

    # Create Report
    regionUrl, marketplace_id = marketplace_action()
    endpoint = f'/reports/2021-06-30/reports'
    url = regionUrl + endpoint
    headers = {
        'x-amz-access-token': access_token,
        'Content-Type': 'application/json'
    }

    dataStartTime = (datetime.now(timezone.utc) - timedelta(days=past_days)).isoformat()

    request_params = {
        'marketplaceIds': [marketplace_id],
        'reportType': 'GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA',
        'dataStartTime': dataStartTime
    }

    create_response = requests.post(url, headers=headers, json=request_params,)
    report_id = create_response.json()['reportId']

    # Check Report Status
    endpoint = f'/reports/2021-06-30/reports/{report_id}'
    url = regionUrl + endpoint

    while True:
        status_response = requests.get(url, headers=headers)
        status = status_response.json().get("processingStatus")

        if status == "DONE":
            print("Report is ready for download!")
            document_id = status_response.json()["reportDocumentId"]
            break
        elif status == "CANCELLED":
            raise ValueError("Report creation was cancelled.")
        elif status == "FATAL":
            raise ValueError("Report creation failed.")
        else:
            print(f"Report status: {status}. Waiting for report to be ready...")
            time.sleep(60)  # Wait before checking again

    # Download Report
    endpoint = f'/reports/2021-06-30/documents/{document_id}'
    url = regionUrl + endpoint
    document_response = requests.get(url, headers=headers)

    if document_response.status_code == 200:
        download_url = document_response.json()["url"]
        compression_algorithm = document_response.json().get("compressionAlgorithm")
        report_data = requests.get(download_url)

        if compression_algorithm == "GZIP":
            print('Decompressing...')

            with open(file_path_name + '.gz', 'wb') as f:
                f.write(report_data.content)

            with gzip.open(file_path_name + '.gz', 'rb') as f_in:
                with open(file_path_name, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        else:
            with open(file_path_name, 'wb') as f:
                f.write(report_data.content)

        print('Report Downloaded!')
    else:
        print("Failed to get the report document:", document_response.json())

    # Data Frame
    try:
        returnsDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t')
    except:
        returnsDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t', encoding='ISO-8859-1')

    returnsDf = returnsDf.rename(columns=lambda x:x.replace('-','_').lower())
    returnsDf['return_date'] = pd.to_datetime(returnsDf['return_date'], utc=True)

    req_columns = [
        'return_date',
        'order_id',
        'sku',
        'asin',
        'fnsku',
        'product_name',
        'quantity',
        'fulfillment_center_id',
        'detailed_disposition',
        'reason',
        'status',
        'license_plate_number',
        'customer_comments'
    ]

    for col in req_columns:
        if col not in returnsDf.columns:
            returnsDf[col] = np.nan

    returnsDf = returnsDf[req_columns]

    schema = {
        'return_date': 'datetime64[ns, UTC]',
        'order_id': str,
        'sku': str,
        'asin': str,
        'fnsku': str,
        'product_name': str,
        'quantity': int,
        'fulfillment_center_id': str,
        'detailed_disposition': str,
        'reason': str,
        'status': str,
        'license_plate_number': str,
        'customer_comments': str
    }

    returnsDf = returnsDf.astype(schema)

    return returnsDf

def replacements(marketplace_action, access_token, file_path_name, past_days):
    """
    This will pull replacement report.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - file_path_name: the file path where to save the report up to its file name
    - past_days: number of days from today's date (UTC)

    return:
    - data frame of replacement report
    """

    # Create Report
    regionUrl, marketplace_id = marketplace_action()
    endpoint = f'/reports/2021-06-30/reports'
    url = regionUrl + endpoint
    headers = {
        'x-amz-access-token': access_token,
        'Content-Type': 'application/json'
    }

    dataStartTime = (datetime.now(timezone.utc) - timedelta(days=past_days)).isoformat()

    request_params = {
        'marketplaceIds': [marketplace_id],
        'reportType': 'GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_REPLACEMENT_DATA',
        'dataStartTime': dataStartTime
    }

    create_response = requests.post(url, headers=headers, json=request_params,)
    report_id = create_response.json()['reportId']

    # Check Report Status
    endpoint = f'/reports/2021-06-30/reports/{report_id}'
    url = regionUrl + endpoint

    while True:
        status_response = requests.get(url, headers=headers)
        status = status_response.json().get("processingStatus")

        if status == "DONE":
            print("Report is ready for download!")
            document_id = status_response.json()["reportDocumentId"]
            break
        elif status == "CANCELLED":
            raise ValueError("Report creation was cancelled.")
        elif status == "FATAL":
            raise ValueError("Report creation failed.")
        else:
            print(f"Report status: {status}. Waiting for report to be ready...")
            time.sleep(60)  # Wait before checking again

    # Download Report
    endpoint = f'/reports/2021-06-30/documents/{document_id}'
    url = regionUrl + endpoint
    document_response = requests.get(url, headers=headers)

    if document_response.status_code == 200:
        download_url = document_response.json()["url"]
        compression_algorithm = document_response.json().get("compressionAlgorithm")
        report_data = requests.get(download_url)

        if compression_algorithm == "GZIP":
            print('Decompressing...')

            with open(file_path_name + '.gz', 'wb') as f:
                f.write(report_data.content)

            with gzip.open(file_path_name + '.gz', 'rb') as f_in:
                with open(file_path_name, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        else:
            with open(file_path_name, 'wb') as f:
                f.write(report_data.content)

        print('Report Downloaded!')
    else:
        print("Failed to get the report document:", document_response.json())

    # Data Frame
    try:
        replacementDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t')
    except:
        replacementDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t', encoding='ISO-8859-1')

    replacementDf = replacementDf.rename(columns=lambda x:x.replace('-','_').lower())
    replacementDf['shipment_date'] = pd.to_datetime(replacementDf['shipment_date'], utc=True)
    replacementDf.info()

    req_columns = [
        'shipment_date',
        'sku',
        'asin',
        'fulfillment_center_id',
        'original_fulfillment_center_id',
        'quantity',
        'replacement_reason_code',
        'replacement_amazon_order_id',
        'original_amazon_order_id'
    ]

    for col in req_columns:
        if col not in replacementDf.columns:
            replacementDf[col] = np.nan

    replacementDf = replacementDf[req_columns]

    schema = {
        'shipment_date': 'datetime64[ns, UTC]',
        'sku': str,
        'asin': str,
        'fulfillment_center_id': str,
        'original_fulfillment_center_id': str,
        'quantity': float,
        'replacement_reason_code': float,
        'replacement_amazon_order_id': str,
        'original_amazon_order_id': str
    }

    replacementDf = replacementDf.astype(schema)

    return replacementDf

def offers(marketplace_action, access_token, asin_list):
    """
    This will pull offer details for each ASIN in the list.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - asin_list: list of all ASIN, should be in form of list

    return:
    - data frame of offer details of each ASIN
    """

    rate_limiter = RateLimiter(tokens_per_second=0.5, capacity=1)
    records = []
    regionUrl, marketplace_id = marketplace_action()

    for asin in asin_list:
        headers = {
                'x-amz-access-token': access_token
            }

        request_params  = {
            'MarketplaceId': marketplace_id,
            "ItemCondition": "New"
        }

        url = regionUrl + f'/products/pricing/v0/items/{asin}/offers' + '?' + urllib.parse.urlencode(request_params)

        response = rate_limiter.send_request(requests.get, url, headers=headers)
        records.extend([response.json()['payload']])

    offersInitDf = []

    for record in records:
        if not record['Offers']:
            offersInitDf.append({
                'seller_id': np.nan,
                'marketplace_id': record['Identifier']['MarketplaceId'],
                'asin': record['ASIN'],
                'item_condition': record['ItemCondition'],
                'currency': np.nan,
                'buybox_price': np.nan,
                'list_price': np.nan,
                'is_buybox_winner': np.nan
            })
        else:
            offersInitDf.append({
                'seller_id': record['Offers'][0]['SellerId'],
                'marketplace_id': record['Identifier']['MarketplaceId'],
                'asin': record['ASIN'],
                'item_condition': record['ItemCondition'],
                'currency': record['Summary']['BuyBoxPrices'][0]['ListingPrice']['CurrencyCode'],
                'buybox_price': record['Summary']['BuyBoxPrices'][0]['ListingPrice']['Amount'],
                'list_price': record['Offers'][0]['ListingPrice']['Amount'],
                'is_buybox_winner': record['Offers'][0]['IsBuyBoxWinner']
            })

    offersDf = pd.DataFrame(offersInitDf)

    return offersDf

def ss_forecast(marketplace_action, access_token, file_path_name, past_days):
    """
    This will pull S&S Forecast report.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - file_path_name: the file path where to save the report up to its file name
    - past_days: number of days from today's date (UTC)

    return:
    - data frame of S&S Forecast report
    """

    # Create Report
    regionUrl, marketplace_id = marketplace_action()
    endpoint = f'/reports/2021-06-30/reports'
    url = regionUrl + endpoint
    headers = {
        'x-amz-access-token': access_token,
        'Content-Type': 'application/json'
    }

    dataStartTime = (datetime.now(timezone.utc) - timedelta(days=past_days)).isoformat()

    request_params = {
        'marketplaceIds': [marketplace_id],
        'reportType': 'GET_FBA_SNS_FORECAST_DATA',
        'dataStartTime': dataStartTime
    }

    create_response = requests.post(url, headers=headers, json=request_params,)
    report_id = create_response.json()['reportId']

    # Check Report Status
    endpoint = f'/reports/2021-06-30/reports/{report_id}'
    url = regionUrl + endpoint

    while True:
        status_response = requests.get(url, headers=headers)
        status = status_response.json().get("processingStatus")

        if status == "DONE":
            print("Report is ready for download!")
            document_id = status_response.json()["reportDocumentId"]
            break
        elif status == "CANCELLED":
            raise ValueError("Report creation was cancelled.")
        elif status == "FATAL":
            raise ValueError("Report creation failed.")
        else:
            print(f"Report status: {status}. Waiting for report to be ready...")
            time.sleep(60)  # Wait before checking again

    # Download Report
    endpoint = f'/reports/2021-06-30/documents/{document_id}'
    url = regionUrl + endpoint
    document_response = requests.get(url, headers=headers)

    if document_response.status_code == 200:
        download_url = document_response.json()["url"]
        compression_algorithm = document_response.json().get("compressionAlgorithm")
        report_data = requests.get(download_url)

        if compression_algorithm == "GZIP":
            print('Decompressing...')

            with open(file_path_name + '.gz', 'wb') as f:
                f.write(report_data.content)

            with gzip.open(file_path_name + '.gz', 'rb') as f_in:
                with open(file_path_name, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        else:
            with open(file_path_name, 'wb') as f:
                f.write(report_data.content)

        print('Report Downloaded!')
    else:
        print("Failed to get the report document:", document_response.json())

    # Data Frame
    try:
        ssForcastDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t')
    except:
        ssForcastDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t', encoding='ISO-8859-1')

    ssForcastDf = ssForcastDf.rename(columns=lambda x:x.replace('-','_').lower())
    ssForcastDf['snapshot_date'] = pd.to_datetime(ssForcastDf['snapshot_date'])
    ssForcastDf['week_1_start_date'] = pd.to_datetime(ssForcastDf['week_1_start_date'])
    ssForcastDf['estimated_avg_sns_discount_next_8_weeks'] = ssForcastDf['estimated_avg_sns_discount_next_8_weeks'].replace('%', '', regex=True).astype(float) / 100

    req_columns = [
        'offer_state',
        'snapshot_date',
        'sku',
        'fnsku',
        'asin',
        'estimated_avg_sns_discount_next_8_weeks',
        'product_name',
        'country',
        'active_subscriptions',
        'week_1_start_date',
        'scheduled_sns_units_week_1',
        'scheduled_sns_units_week_2',
        'scheduled_sns_units_week_3',
        'scheduled_sns_units_week_4',
        'scheduled_sns_units_week_5',
        'scheduled_sns_units_week_6',
        'scheduled_sns_units_week_7',
        'scheduled_sns_units_week_8'
    ]

    for col in req_columns:
        if col not in ssForcastDf.columns:
            ssForcastDf[col] = np.nan

    ssForcastDf = ssForcastDf[req_columns]

    schema = {
        'offer_state': str,
        'snapshot_date': 'datetime64[ns, UTC]',
        'sku': str,
        'fnsku': str,
        'asin': str,
        'estimated_avg_sns_discount_next_8_weeks': float,
        'product_name': str,
        'country': str,
        'active_subscriptions': float,
        'week_1_start_date': 'datetime64[ns, UTC]',
        'scheduled_sns_units_week_1': float,
        'scheduled_sns_units_week_2': float,
        'scheduled_sns_units_week_3': float,
        'scheduled_sns_units_week_4': float,
        'scheduled_sns_units_week_5': float,
        'scheduled_sns_units_week_6': float,
        'scheduled_sns_units_week_7': float,
        'scheduled_sns_units_week_8': float
    }
    ssForcastDf = ssForcastDf.astype(schema)

    return ssForcastDf

def ss_performance(marketplace_action, access_token, file_path_name, past_days):
    """
    This will pull S&S Performance report.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - file_path_name: the file path where to save the report up to its file name
    - past_days: number of days from today's date (UTC)

    return:
    - data frame of S&S Performance report
    """

    # Create Report
    regionUrl, marketplace_id = marketplace_action()
    endpoint = f'/reports/2021-06-30/reports'
    url = regionUrl + endpoint
    headers = {
        'x-amz-access-token': access_token,
        'Content-Type': 'application/json'
    }

    dataStartTime = (datetime.now(timezone.utc) - timedelta(days=past_days)).isoformat()

    request_params = {
        'marketplaceIds': [marketplace_id],
        'reportType': 'GET_FBA_SNS_PERFORMANCE_DATA',
        'dataStartTime': dataStartTime
    }

    create_response = requests.post(url, headers=headers, json=request_params,)
    report_id = create_response.json()['reportId']

    # Check Report Status
    endpoint = f'/reports/2021-06-30/reports/{report_id}'
    url = regionUrl + endpoint

    while True:
        status_response = requests.get(url, headers=headers)
        status = status_response.json().get("processingStatus")

        if status == "DONE":
            print("Report is ready for download!")
            document_id = status_response.json()["reportDocumentId"]
            break
        elif status == "CANCELLED":
            raise ValueError("Report creation was cancelled.")
        elif status == "FATAL":
            raise ValueError("Report creation failed.")
        else:
            print(f"Report status: {status}. Waiting for report to be ready...")
            time.sleep(60)  # Wait before checking again

    # Download Report
    endpoint = f'/reports/2021-06-30/documents/{document_id}'
    url = regionUrl + endpoint
    document_response = requests.get(url, headers=headers)

    if document_response.status_code == 200:
        download_url = document_response.json()["url"]
        compression_algorithm = document_response.json().get("compressionAlgorithm")
        report_data = requests.get(download_url)

        if compression_algorithm == "GZIP":
            print('Decompressing...')

            with open(file_path_name + '.gz', 'wb') as f:
                f.write(report_data.content)

            with gzip.open(file_path_name + '.gz', 'rb') as f_in:
                with open(file_path_name, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        else:
            with open(file_path_name, 'wb') as f:
                f.write(report_data.content)

        print('Report Downloaded!')
    else:
        print("Failed to get the report document:", document_response.json())

    # Data Frame
    try:
        ssPerformanceDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t')
    except:
        ssPerformanceDf = pd.read_csv(filepath_or_buffer=file_path_name, delimiter='\t', encoding='ISO-8859-1')

    ssPerformanceDf = ssPerformanceDf.drop_duplicates()
    ssPerformanceDf = ssPerformanceDf.rename(columns=lambda x:x.replace('-','_').lower())

    ssPerformanceDf['snapshot_date'] = pd.to_datetime(ssPerformanceDf['snapshot_date'])
    ssPerformanceDf['week_1_start_date'] = pd.to_datetime(ssPerformanceDf['week_1_start_date'])

    for col in ssPerformanceDf.columns:
        if 'oos_rate' in col:
            ssPerformanceDf[col] = ssPerformanceDf[col].replace({'%':''}, regex=True).astype(float) / 100

    for col in ssPerformanceDf.columns:
        if 'sns_discount' in col:
            ssPerformanceDf[col] = ssPerformanceDf[col].replace({'%':''}, regex=True).astype(float) / 100

    req_columns = [
        'offer_state',
        'snapshot_date',
        'sku',
        'fnsku',
        'asin',
        'product_name',
        'country',
        'week_1_start_date',
        'sns_units_shipped_week_1',
        'oos_rate_week_1',
        'sns_sale_price_week_1',
        'sns_discount_week_1',
        'sns_units_shipped_week_2',
        'oos_rate_week_2',
        'sns_sale_price_week_2',
        'sns_discount_week_2',
        'sns_units_shipped_week_3',
        'oos_rate_week_3',
        'sns_sale_price_week_3',
        'sns_discount_week_3',
        'sns_units_shipped_week_4',
        'oos_rate_week_4',
        'sns_sale_price_week_4',
        'sns_discount_week_4'
    ]

    for col in req_columns:
        if col not in ssPerformanceDf.columns:
            ssPerformanceDf[col] = np.nan

    ssPerformanceDf = ssPerformanceDf[req_columns]

    schema = {
        'offer_state': str,
        'snapshot_date': 'datetime64[ns, UTC]',
        'sku': str,
        'fnsku': str,
        'asin': str,
        'product_name': str,
        'country': str,
        'week_1_start_date': 'datetime64[ns, UTC]',
        'sns_units_shipped_week_1': float,
        'oos_rate_week_1': float,
        'sns_sale_price_week_1': float,
        'sns_discount_week_1': float,
        'sns_units_shipped_week_2': float,
        'oos_rate_week_2': float,
        'sns_sale_price_week_2': float,
        'sns_discount_week_2': float,
        'sns_units_shipped_week_3': float,
        'oos_rate_week_3': float,
        'sns_sale_price_week_3': float,
        'sns_discount_week_3': float,
        'sns_units_shipped_week_4': float,
        'oos_rate_week_4': float,
        'sns_sale_price_week_4': float,
        'sns_discount_week_4': float
    }

    ssPerformanceDf = ssPerformanceDf.astype(schema)

    return ssPerformanceDf

def finance_shipmentEventList(marketplace_action, access_token, past_days):
    """
    This will pull Shipment Event List in a region.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - past_days: number of days from today's date (UTC)

    return:
    - data frame of the report summary
    """
    # Pull API Data
    rate_limiter = RateLimiter(tokens_per_second=0.5, capacity=30)
    records = []
    regionUrl, marketplace_id = marketplace_action()
    NextToken = None

    PostedAfter = (datetime.now(timezone.utc) - timedelta(days=past_days)).isoformat()

    headers = {
            'x-amz-access-token': access_token
        }

    request_params  = {
        'PostedAfter': PostedAfter
    }

    try:
        url = regionUrl + f'/finances/v0/financialEvents' + '?' + urllib.parse.urlencode(request_params)
        response = requests.get(url, headers=headers)
        records.extend(response.json()['payload']['FinancialEvents']['ShipmentEventList'])

        try:
            NextToken = response.json()['payload']['NextToken']
        except:
            NextToken = None

        while NextToken:
            request_params_next  = {
                'NextToken': NextToken
            }
            url = regionUrl + f'/finances/v0/financialEvents' + '?' + urllib.parse.urlencode(request_params_next)
            response = rate_limiter.send_request(requests.get, url, headers=headers)
            records.extend(response.json()['payload']['FinancialEvents']['ShipmentEventList'])

            try:
                NextToken = response.json()['payload']['NextToken']
            except:
                NextToken = None
            
        print('End of List')

    except Exception as e:
        print(response.json()['errors'][0]['message'])
        print(response.json()['errors'][0]['details'])

    # set Data Frame
    taxDf = []
    for record in records:
        data ={
            'amazon_order_id': record.get('AmazonOrderId', np.nan),
            'posted_date': record.get('PostedDate', np.nan),
            'marketplace': record.get('MarketplaceName', np.nan),
            'sku': record.get('ShipmentItemList', [{}])[0].get('SellerSKU', np.nan),
            'qty': record.get('ShipmentItemList', [{}])[0].get('QuantityShipped', np.nan),
            'currency': record.get('ShipmentItemList', [{}])[0].get('ItemChargeList', [{}])[0].get('ChargeAmount',{}).get('CurrencyCode', np.nan),
        }

        charges = record.get('ShipmentItemList', [{}])[0].get('ItemChargeList', [])
        for charge in charges:
            data[charge.get('ChargeType')] = charge.get('ChargeAmount', {}).get('CurrencyAmount', np.nan)

        fees = record.get('ShipmentItemList', [{}])[0].get('ItemFeeList', [])
        for fee in fees:
            data[fee.get('FeeType')] = fee.get('FeeAmount', {}).get('CurrencyAmount', np.nan)

        withhelds = record.get('ShipmentItemList', [{}])[0].get('ItemTaxWithheldList', [{}])[0].get('TaxesWithheld',[])
        for withheld in withhelds:
            data[withheld.get('ChargeType')] = withheld.get('ChargeAmount', {}).get('CurrencyAmount', np.nan)

        taxDf.append(data)

    taxDf = pd.DataFrame(taxDf)

    taxDf['posted_date'] = pd.to_datetime(taxDf['posted_date'])

    req_columns = [
        'amazon_order_id',
        'posted_date',
        'marketplace',
        'sku',
        'qty',
        'currency',
        'Principal',
        'Tax',
        'GiftWrap',
        'GiftWrapTax',
        'ShippingCharge',
        'ShippingTax',
        'FBAPerUnitFulfillmentFee',
        'Commission',
        'FixedClosingFee',
        'GiftwrapChargeback',
        'SalesTaxCollectionFee',
        'ShippingChargeback',
        'VariableClosingFee',
        'DigitalServicesFee',
        'FBAPerOrderFulfillmentFee',
        'FBAWeightBasedFee',
        'MarketplaceFacilitatorTax-Principal',
        'MarketplaceFacilitatorTax-Shipping',
        'MarketplaceFacilitatorVAT-Principal',
        'LowValueGoodsTax-Shipping',
        'LowValueGoodsTax-Principal',
        'MarketplaceFacilitatorVAT-Shipping',
        'MarketplaceFacilitatorTax-Other',
        'RenewedProgramFee'
    ]

    for col in req_columns:
        if col not in taxDf.columns:
            taxDf[col] = np.nan

    taxDf = taxDf[req_columns]

    schema = {
        'amazon_order_id': str,
        'posted_date': 'datetime64[ns, UTC]',
        'marketplace': str,
        'sku': str,
        'qty': float,
        'currency': str,
        'Principal': float,
        'Tax': float,
        'GiftWrap': float,
        'GiftWrapTax': float,
        'ShippingCharge': float,
        'ShippingTax': float,
        'FBAPerUnitFulfillmentFee': float,
        'Commission': float,
        'FixedClosingFee': float,
        'GiftwrapChargeback': float,
        'SalesTaxCollectionFee': float,
        'ShippingChargeback': float,
        'VariableClosingFee': float,
        'DigitalServicesFee': float,
        'FBAPerOrderFulfillmentFee': float,
        'FBAWeightBasedFee': float,
        'MarketplaceFacilitatorTax-Principal': float,
        'MarketplaceFacilitatorTax-Shipping': float,
        'MarketplaceFacilitatorVAT-Principal': float,
        'LowValueGoodsTax-Shipping': float,
        'LowValueGoodsTax-Principal': float,
        'MarketplaceFacilitatorVAT-Shipping': float,
        'MarketplaceFacilitatorTax-Other': float,
        'RenewedProgramFee': float
    }

    taxDf = taxDf.astype(schema)

    return taxDf

def fba_inv_live(marketplace_action, access_token):
    """
    This will pull Live Inventory in specific Marketplace.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace

    return:
    - data frame of the Live Inventory Count
    """
    # API Pull
    rate_limiter = RateLimiter(tokens_per_second=2, capacity=2)
    records = []
    regionUrl, marketplace_id = marketplace_action()
    NextToken = None
    url = regionUrl + f'/fba/inventory/v1/summaries'

    headers = {
            'x-amz-access-token': access_token
        }

    request_params  = {
        'granularityType': 'Marketplace',
        'granularityId': marketplace_id,
        'marketplaceIds': marketplace_id,
        'details': True
    }

    try:
        response = requests.get(url, headers=headers, params=request_params)
        records.extend(response.json()['payload']['inventorySummaries'])

        try:
            NextToken = response.json()['pagination']['nextToken']
        except:
            NextToken = None

        while NextToken:
            paginated_params  = {
                'granularityType': 'Marketplace',
                'granularityId': marketplace_id,
                'marketplaceIds': marketplace_id,
                'details': True,
                'nextToken': NextToken
            }
            response = rate_limiter.send_request(requests.get, url, headers=headers, params=paginated_params)
            records.extend(response.json()['payload']['inventorySummaries'])

            try:
                NextToken = response.json()['pagination']['nextToken']
            except:
                NextToken = None

        print('End of List')

    except Exception as e:
        print(response.json()['errors'][0]['message'])
        print(response.json()['errors'][0]['details'])

    # Data Frame
    fbaInventoryDf = []

    for record in records:
        if record.get('lastUpdatedTime') != '':
            data = {
                'update_date': record.get('lastUpdatedTime', np.nan),
                'asin': record.get('asin', np.nan),
                'fnsku': record.get('fnSku', np.nan),
                'sellerSku': record.get('sellerSku', np.nan),
                'product_name': record.get('productName', np.nan),
                'condition': record.get('condition', np.nan),
                'total_qty': record.get('totalQuantity', np.nan),
                'fulfillable_qty': record.get('inventoryDetails',{}).get('fulfillableQuantity', np.nan),
                'inbound_working_qty': record.get('inventoryDetails',{}).get('inboundWorkingQuantity', np.nan),
                'inbound_shipped_qty': record.get('inventoryDetails',{}).get('inboundShippedQuantity', np.nan),
                'inbound_receiving_qty': record.get('inventoryDetails',{}).get('inboundReceivingQuantity', np.nan),
                'total_reserved_qty': record.get('inventoryDetails',{}).get('reservedQuantity', {}).get('totalReservedQuantity', np.nan),
                'customer_reserved_qty': record.get('inventoryDetails',{}).get('reservedQuantity', {}).get('pendingCustomerOrderQuantity', np.nan),
                'fc_transfer_qty': record.get('inventoryDetails',{}).get('reservedQuantity', {}).get('pendingTransshipmentQuantity', np.nan),
                'fc_processing_qty': record.get('inventoryDetails',{}).get('reservedQuantity', {}).get('fcProcessingQuantity', np.nan),
                'total_researching_qty': record.get('inventoryDetails',{}).get('researchingQuantity', {}).get('totalResearchingQuantity', np.nan),
                'total_unfulfillable_qty': record.get('inventoryDetails',{}).get('unfulfillableQuantity', {}).get('totalUnfulfillableQuantity', np.nan),
                'customer_damaged_qty': record.get('inventoryDetails',{}).get('unfulfillableQuantity', {}).get('customerDamagedQuantity', np.nan),
                'warehouse_damaged_qty': record.get('inventoryDetails',{}).get('unfulfillableQuantity', {}).get('warehouseDamagedQuantity', np.nan),
                'distribution_damaged_qty': record.get('inventoryDetails',{}).get('unfulfillableQuantity', {}).get('distributorDamagedQuantity', np.nan),
                'carrier_damaged_qty': record.get('inventoryDetails',{}).get('unfulfillableQuantity', {}).get('carrierDamagedQuantity', np.nan),
                'defective_qty': record.get('inventoryDetails',{}).get('unfulfillableQuantity', {}).get('defectiveQuantity', np.nan),
                'expired_qty': record.get('inventoryDetails',{}).get('unfulfillableQuantity', {}).get('expiredQuantity', np.nan),
                'reserved_future_qty': record.get('inventoryDetails',{}).get('futureSupplyQuantity', {}).get('reservedFutureSupplyQuantity', np.nan),
                'buyable_future_qty': record.get('inventoryDetails',{}).get('futureSupplyQuantity', {}).get('futureSupplyBuyableQuantity', np.nan),
            }

            for r in record.get('inventoryDetails',{}).get('researchingQuantity', {}).get('researchingQuantityBreakdown', []):
                data[r.get('name')] = r.get('quantity')

            fbaInventoryDf.append(data)

    fbaInventoryDf = pd.DataFrame(fbaInventoryDf)

    fbaInventoryDf['update_date'] = pd.to_datetime(fbaInventoryDf['update_date'])

    req_columns = [
        'update_date',
        'asin',
        'fnsku',
        'sellerSku',
        'product_name',
        'condition',
        'total_qty',
        'fulfillable_qty',
        'inbound_working_qty',
        'inbound_shipped_qty',
        'inbound_receiving_qty',
        'total_reserved_qty',
        'customer_reserved_qty',
        'fc_transfer_qty',
        'fc_processing_qty',
        'total_researching_qty',
        'total_unfulfillable_qty',
        'customer_damaged_qty',
        'warehouse_damaged_qty',
        'distribution_damaged_qty',
        'carrier_damaged_qty',
        'defective_qty',
        'expired_qty',
        'reserved_future_qty',
        'buyable_future_qty',
        'researchingQuantityInShortTerm',
        'researchingQuantityInMidTerm',
        'researchingQuantityInLongTerm'
    ]

    for col in req_columns:
        if col not in fbaInventoryDf.columns:
            fbaInventoryDf[col] = np.nan

    fbaInventoryDf = fbaInventoryDf[req_columns]

    schema = {
        'update_date': 'datetime64[ns, UTC]',
        'asin': str,
        'fnsku': str,
        'sellerSku': str,
        'product_name': str,
        'condition': str,
        'total_qty': float,
        'fulfillable_qty': float,
        'inbound_working_qty': float,
        'inbound_shipped_qty': float,
        'inbound_receiving_qty': float,
        'total_reserved_qty': float,
        'customer_reserved_qty': float,
        'fc_transfer_qty': float,
        'fc_processing_qty': float,
        'total_researching_qty': float,
        'total_unfulfillable_qty': float,
        'customer_damaged_qty': float,
        'warehouse_damaged_qty': float,
        'distribution_damaged_qty': float,
        'carrier_damaged_qty': float,
        'defective_qty': float,
        'expired_qty': float,
        'reserved_future_qty': float,
        'buyable_future_qty': float,
        'researchingQuantityInShortTerm': float,
        'researchingQuantityInMidTerm': float,
        'researchingQuantityInLongTerm': float
    }

    fbaInventoryDf = fbaInventoryDf.astype(schema)

    return fbaInventoryDf

def sku_attributes(marketplace_action, access_token, sellerId, sku_list):
    """
    This will pull SKU attributes in specific Marketplace.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - sellerId: the Seller ID of specific region
    - sku_list: list of all the SKUs to pull the attribute details

    return:
    - data frame of the attributes of all the SKU in the list
    """
    # API Pull
    rate_limiter = RateLimiter(tokens_per_second=5, capacity=10)
    records = []
    regionUrl, marketplace_id = marketplace_action()

    for sku in sku_list:
        url = regionUrl + f'/listings/2021-08-01/items/{sellerId}/{sku}'
        headers = {
                'x-amz-access-token': access_token
            }

        request_params  = {
            'marketplaceIds': marketplace_id,
            'includedData': 'attributes'
        }

        try:
            response =  rate_limiter.send_request(requests.get, url, headers=headers, params=request_params)
            records.extend([response.json()])

        except Exception as e:
            print(response.json()['errors'][0]['message'])
            print(response.json()['errors'][0]['details'])

    # Data Frame
    attributesDf = []
    for record in records:
        if record.get('sku') is not None:
            data ={
                'sku': record.get('sku'),
                'item_name': record.get('attributes',{}).get('item_name', [{}])[0].get('value', np.nan),
                'color': record.get('attributes',{}).get('color', [{}])[0].get('value', np.nan),
                'variation_theme': record.get('attributes',{}).get('variation_theme', [{}])[0].get('name', np.nan),
                'item_package_weight': record.get('attributes',{}).get('item_package_weight', [{}])[0].get('value', np.nan),
                'item_package_weight_unit': record.get('attributes',{}).get('item_package_weight', [{}])[0].get('unit', np.nan),
                'manufacturer': record.get('attributes',{}).get('manufacturer', [{}])[0].get('value', np.nan),
                'product_description': record.get('attributes',{}).get('product_description', [{}])[0].get('value', np.nan),
                'brand': record.get('attributes',{}).get('brand', [{}])[0].get('value', np.nan),
                'generic_keyword': record.get('attributes',{}).get('generic_keyword', [{}])[0].get('value', np.nan),
                'item_type_keyword': record.get('attributes',{}).get('item_type_keyword', [{}])[0].get('value', np.nan),
                'condition_type': record.get('attributes',{}).get('condition_type', [{}])[0].get('value', np.nan),
                'number_of_items': record.get('attributes',{}).get('number_of_items', [{}])[0].get('value', np.nan),
                'height': record.get('attributes',{}).get('item_package_dimensions', [{}])[0].get('height', {}).get('value', np.nan),
                'height_unit': record.get('attributes',{}).get('item_package_dimensions', [{}])[0].get('height', {}).get('unit', np.nan),
                'length': record.get('attributes',{}).get('item_package_dimensions', [{}])[0].get('length', {}).get('value', np.nan),
                'length_unit': record.get('attributes',{}).get('item_package_dimensions', [{}])[0].get('length', {}).get('unit', np.nan),
                'width': record.get('attributes',{}).get('item_package_dimensions', [{}])[0].get('width', {}).get('value', np.nan),
                'width_unit': record.get('attributes',{}).get('item_package_dimensions', [{}])[0].get('width', {}).get('unit', np.nan),
                'size': record.get('attributes',{}).get('size', [{}])[0].get('value', np.nan),
                'max_order_quantity': record.get('attributes',{}).get('max_order_quantity', [{}])[0].get('value', np.nan),
                'main_image': record.get('attributes',{}).get('main_product_image_locator', [{}])[0].get('media_location', np.nan),
                'other_image_1': record.get('attributes',{}).get('other_product_image_locator_1', [{}])[0].get('media_location', np.nan),
                'other_image_2': record.get('attributes',{}).get('other_product_image_locator_2', [{}])[0].get('media_location', np.nan),
                'other_image_3': record.get('attributes',{}).get('other_product_image_locator_3', [{}])[0].get('media_location', np.nan),
                'other_image_4': record.get('attributes',{}).get('other_product_image_locator_4', [{}])[0].get('media_location', np.nan),
                'other_image_5': record.get('attributes',{}).get('other_product_image_locator_5', [{}])[0].get('media_location', np.nan),
                'other_image_6': record.get('attributes',{}).get('other_product_image_locator_6', [{}])[0].get('media_location', np.nan),
                'swatch_image': record.get('attributes',{}).get('swatch_product_image_locator', [{}])[0].get('media_location', np.nan),
                'swatch_image': record.get('attributes',{}).get('swatch_product_image_locator', [{}])[0].get('media_location', np.nan),
                'list_price': record.get('attributes',{}).get('list_price', [{}])[0].get('value', np.nan),
                'list_price_currency': record.get('attributes',{}).get('list_price', [{}])[0].get('currency', np.nan),
                'offer_start_date': record.get('attributes',{}).get('purchasable_offer', [{}])[0].get('start_at', {}).get('value', np.nan),
                'offer_end_date': record.get('attributes',{}).get('purchasable_offer', [{}])[0].get('end_at', {}).get('value', np.nan),
                'offer_currency': record.get('attributes',{}).get('purchasable_offer', [{}])[0].get('currency', np.nan),
                'offer_audience': record.get('attributes',{}).get('purchasable_offer', [{}])[0].get('audience', np.nan),
                'your_price': record.get('attributes',{}).get('purchasable_offer', [{}])[0].get('our_price', [{}])[0].get('schedule',[{}])[0].get('value_with_tax', np.nan),
                'maximum_seller_allowed_price': record.get('attributes',{}).get('purchasable_offer', [{}])[0].get('maximum_seller_allowed_price', [{}])[0].get('schedule',[{}])[0].get('value_with_tax', np.nan),
                'minimum_seller_allowed_price': record.get('attributes',{}).get('purchasable_offer', [{}])[0].get('minimum_seller_allowed_price', [{}])[0].get('schedule',[{}])[0].get('value_with_tax', np.nan),
                'sale_start_date': record.get('attributes',{}).get('purchasable_offer', [{}])[0].get('discounted_price', [{}])[0].get('schedule',[{}])[0].get('start_at', np.nan),
                'sale_end_date': record.get('attributes',{}).get('purchasable_offer', [{}])[0].get('discounted_price', [{}])[0].get('schedule',[{}])[0].get('end_at', np.nan),
                'sale_price': record.get('attributes',{}).get('purchasable_offer', [{}])[0].get('discounted_price', [{}])[0].get('schedule',[{}])[0].get('value_with_tax', np.nan),
                'parentage_level': record.get('attributes',{}).get('parentage_level', [{}])[0].get('value', np.nan),
                'child_relationship_type': record.get('attributes',{}).get('child_parent_sku_relationship', [{}])[0].get('child_relationship_type', np.nan),
                'parent_sku': record.get('attributes',{}).get('child_parent_sku_relationship', [{}])[0].get('parent_sku', np.nan),
            }

            for i in range(5):
                try:
                    data[f'bullet_point_{i + 1}'] = record.get('attributes',{}).get('bullet_point', [])[i].get('value', np.nan)
                except:
                    data[f'bullet_point_{i + 1}'] = np.nan

            attributesDf.append(data)

    attributesDf = pd.DataFrame(attributesDf)
    attributesDf.insert(0,'date', datetime.now(timezone.utc).strftime('%Y-%m-%d'))

    req_columns = [
        'date',
        'sku',
        'item_name',
        'color',
        'variation_theme',
        'item_package_weight',
        'item_package_weight_unit',
        'manufacturer',
        'bullet_point_1',
        'bullet_point_2',
        'bullet_point_3',
        'bullet_point_4',
        'bullet_point_5',
        'product_description',
        'brand',
        'generic_keyword',
        'item_type_keyword',
        'condition_type',
        'number_of_items',
        'height',
        'height_unit',
        'length',
        'length_unit',
        'width',
        'width_unit',
        'size',
        'max_order_quantity',
        'main_image',
        'other_image_1',
        'other_image_2',
        'other_image_3',
        'other_image_4',
        'other_image_5',
        'other_image_6',
        'swatch_image',
        'list_price',
        'list_price_currency',
        'offer_start_date',
        'offer_end_date',
        'offer_currency',
        'offer_audience',
        'your_price',
        'maximum_seller_allowed_price',
        'minimum_seller_allowed_price',
        'sale_start_date',
        'sale_end_date',
        'sale_price',
        'parentage_level',
        'child_relationship_type',
        'parent_sku'
    ]

    for col in req_columns:
        if col not in attributesDf.columns:
            attributesDf[col] = np.nan

    attributesDf = attributesDf[req_columns]

    colPrices = ['list_price','your_price','minimum_seller_allowed_price','maximum_seller_allowed_price','sale_price']

    for colPrice in colPrices:
        attributesDf[colPrice] = attributesDf[colPrice].astype(str).replace({',': '.'}, regex=True)
        attributesDf[colPrice] = pd.to_numeric(attributesDf[colPrice], errors='coerce')

    schema = {
        'date': 'datetime64[ns]',
        'sku': str,
        'item_name': str,
        'color': str,
        'variation_theme': str,
        'item_package_weight': float,
        'item_package_weight_unit': str,
        'manufacturer': str,
        'bullet_point_1': str,
        'bullet_point_2': str,
        'bullet_point_3': str,
        'bullet_point_4': str,
        'bullet_point_5': str,
        'product_description': str,
        'brand': str,
        'generic_keyword': str,
        'item_type_keyword': str,
        'condition_type': str,
        'number_of_items': float,
        'height': float,
        'height_unit': str,
        'length': float,
        'length_unit': str,
        'width': float,
        'width_unit': str,
        'size': str,
        'max_order_quantity': float,
        'main_image': str,
        'other_image_1': str,
        'other_image_2': str,
        'other_image_3': str,
        'other_image_4': str,
        'other_image_5': str,
        'other_image_6': str,
        'swatch_image': str,
        'list_price': float,
        'list_price_currency': str,
        'offer_start_date': str,
        'offer_end_date': str,
        'offer_currency': str,
        'offer_audience': str,
        'your_price': float,
        'maximum_seller_allowed_price': float,
        'minimum_seller_allowed_price': float,
        'sale_start_date': str,
        'sale_end_date': str,
        'sale_price': float,
        'parentage_level': str,
        'child_relationship_type': str,
        'parent_sku': str
    }

    attributesDf = attributesDf.astype(schema)

    return attributesDf

def get_sellerId(marketplace_action, access_token, sku):
    """
    This will pull SKU attributes in specific Marketplace.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - sku: sample SKU that is active in the specific region

    return:
    - returns the Seller ID in a specific region
    """
    # API Pull
    rate_limiter = RateLimiter(tokens_per_second=0.5, capacity=1)
    regionUrl, marketplace_id = marketplace_action()

    url = regionUrl + f'/products/pricing/v0/competitivePrice'
    headers = {
            'x-amz-access-token': access_token
        }

    request_params  = {
        'MarketplaceId': marketplace_id,
        'Skus': sku,
        'ItemType': 'Sku'

    }

    try:
        response =  rate_limiter.send_request(requests.get, url, headers=headers, params=request_params)
        sellerId = (response.json().get('payload',[{}])[0].get('Product',{}).get('Identifiers',{}).get('SKUIdentifier',{}).get('SellerId', np.nan))
        return sellerId

    except Exception as e:
            print(response.json()['errors'][0]['message'])
            print(response.json()['errors'][0]['details'])

