import base64
import datetime
import json
import time
import urllib.parse
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import bech32
import pandas as pd
import pytz
import requests
from requests.adapters import HTTPAdapter, Retry

from strideutils import types
from strideutils.stride_config import config

ACCOUNT_QUERY = "cosmos/auth/v1beta1/accounts/{address}"
ACCOUNT_BALANCE_QUERY = "cosmos/bank/v1beta1/balances/{address}"
ACCOUNT_DELEGATIONS_QUERY = "cosmos/staking/v1beta1/delegations/{delegator_address}"
ACCOUNT_UNBONDINGS_QUERY = "cosmos/staking/v1beta1/delegators/{delegator_address}/unbonding_delegations"
MODULE_ACCOUNTS_QUERY = "cosmos/auth/v1beta1/module_accounts"
SUPPLY_QUERY = "cosmos/bank/v1beta1/supply/by_denom"
VALIDATORS_QUERY = "cosmos/staking/v1beta1/validators"
VALIDATOR_SLASHES_QUERY = "cosmos/distribution/v1beta1/validators/{validator_address}/slashes"
DELEGATIONS_QUERY = "cosmos/staking/v1beta1/delegations/{delegator_address}"

CONNECTION_QUERY = "ibc/core/connection/v1/connections/{connection_id}"
CHANNELS_QUERY = "ibc/core/channel/v1/connections/{connection_id}/channels"
CHANNEL_QUERY = "ibc/core/channel/v1/channels/{channel_id}/ports/{port_id}"

TXS_QUERY = "cosmos/tx/v1beta1/txs"
TX_BY_ACCOUNT_EVENT = "tx.acc_seq='{address}/{sequence}'"

HOST_ZONE_QUERY = "Stride-Labs/stride/stakeibc/host_zone"
EPOCHS_QUERY = "Stridelabs/stride/epochs"
PENDING_ICQ_QUERY = "Stride-Labs/stride/interchainquery/pending_queries"
RATE_LIMIT_QUERY = "Stride-Labs/ibc-rate-limiting/ratelimit/ratelimits"
DEPOSIT_RECORDS_QUERY = "Stride-Labs/stride/records/deposit_record_by_host_zone/{chain_id}"
UNBONDING_RECORDS_QUERY = "Stride-Labs/stride/records/epoch_unbonding_record"
REDEMPTION_RECORDS_QUERY = "Stride-Labs/stride/records/user_redemption_record"
LSM_RECORDS_QUERY = "Stride-Labs/stride/stakeibc/lsm_deposits"
CALLBACK_DATA_QUERY = "Stride-Labs/stride/icacallbacks/callback_data"

STAKETIA = "staketia"
STAKEDYM = "stakedym"

DYMENSION_CHAIN_ID = "dymension_1100-1"
CELESTIA_CHAIN_ID = "celestia"

MULTISIG_HOST_ZONE_QUERY = "Stride-Labs/stride/{module}/host_zone"
MULTISIG_DELEGATION_RECORDS_QUERY = "Stride-Labs/stride/{module}/delegation_records"
MULTISIG_UNBONDING_RECORDS_QUERY = "Stride-Labs/stride/{module}/unbonding_records"
MULTISIG_REDEMPTION_RECORDS_QUERY = "Stride-Labs/stride/{module}/redemption_records"

COSMWASM_CONTRACT_QUERY = "cosmwasm/wasm/v1/contract/{contract_address}/smart/{query}"

CHANNELS_SUMMARY_QUERY_BY_HOST = "https://channels.main.stridenet.co/api/data/{chain_id}"
CHANNELS_SUMMARY_QUERY = "https://channels.main.stridenet.co/api/data"

requests_session = requests.Session()

retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[400, 403, 404, 500, 502, 503, 504])

requests_session.mount("http://", HTTPAdapter(max_retries=retries))
requests_session.mount("https://", HTTPAdapter(max_retries=retries))


def request(
    url: str,
    headers: dict[str, str] = {},
    params: Union[dict, List[Tuple[str, str]]] = {},
    data: Optional[str] = None,
    block_height: int = 0,
    cache_response: bool = False,
    _cache: Dict[str, Any] = {},
):
    """
    This returns a JSON output from the given URL, and then parses the JSON output
    returning the field specified by json_path

    E.g. request(
        "https://lcd.osmosis.zone/osmosis/mint/v1beta1/params",
        ["params", "distribution_proportions", "community_pool"]
    ) = 0.05

    If cache is true, will save the output for the future.
    """
    cache_key = f"{url}{headers}{params}{block_height}"
    if cache_key in _cache:
        return _cache[cache_key]

    headers = headers or {}
    headers["x-cosmos-block-height"] = str(block_height)
    headers["Content-Type"] = "application/json"

    # Both dictionaries and tuples are supported for params, in case
    # the same key needs to be repeated
    if type(params) is dict:
        params = list(params.items())

    resp = requests_session.get(url, headers=headers, params=params, data=data)

    # Handle non-200 responses.
    if not resp.ok:
        error_msg = f"Error fetching {url}: {resp.status_code} {resp.json()}"
        try:
            error_details = resp.json()
            error_msg += f" {error_details}"
        except requests.exceptions.JSONDecodeError:
            error_msg += f" {resp.text}"

        print(error_msg)
        raise Exception(error_msg)

    # Handle empty responses.
    if not resp.text:
        error_msg = f"Empty response received from {url}"
        print(error_msg)
        raise Exception(error_msg)

    # Try to parse JSON response.
    try:
        out = resp.json()
    except requests.exceptions.JSONDecodeError as e:
        error_msg = f"Invalid JSON response received from {url}: {resp.text[:200]}..."
        print(error_msg)
        raise Exception(error_msg) from e

    if cache_response:
        _cache[cache_key] = out
    return out


def query_list_with_pagination(
    endpoint: str,
    rel_key: str,
    block_height: int = 0,
    max_pages: int = 50,
    params: Union[dict, List[Tuple[str, str]]] = {},
) -> List[Dict]:
    """
    Query a list with pagination
    Returns the concatenated list from all the responses
    """
    data = []
    query_url = endpoint
    query_count = 0

    while True:
        res = request(url=query_url, block_height=block_height, params=params)
        data += res[rel_key]

        query_count += 1
        if query_count >= max_pages:
            print(f"Max pages {max_pages} reached - results are truncated")
            break

        # Break if it's a paginated query
        if "pagination" not in res.keys():
            break

        # Continue looping as long as the pagination key is not null
        pagination_key = res["pagination"]["next_key"]
        if not pagination_key:
            break

        # Update query url with next key
        encoded_pagination_key = urllib.parse.quote_plus(pagination_key)
        query_url = f"{endpoint}?pagination.key={encoded_pagination_key}"

    return data


def get_all_host_zones(include_multisig_hosts: bool = True) -> List[Dict]:
    """
    Queries all host zone structs, returning a list of each host zone json
    By default, this queries both stakeibc and staketia/stakedym; however,
    staketia/stakedym can be disabled by passing include_multisig_hosts = False

    Returns:
        A list of host zone structs
            e.g. [{'chain_id': 'comdex-1',
                  'bech32prefix': 'comdex',
                  'connection_id': 'connection-28',
                  'transfer_channel_id': 'channel-49',
                  'ibc_denom':
                      'ibc/EB66980014602E6BD50A1CB9FFB8FA694DC3EC10A48D2C1C649D732954F88D4A',
                  'host_denom': 'ucmdx',
                  'unbonding_period': '21',
                  'validators': [
                      {'name': 'autostake',
                       'address': 'comdexvaloper195re7mhwh9urewm3rvaj9r7vm6j63c4sd78njd',
                       'weight': '4065',
                       'delegation': '227025044931',
                       'slash_query_progress_tracker': '0',
                       'slash_query_checkpoint': '32170217709',
                       'shares_to_tokens_rate': '1.000000000000000000',
                       'delegation_changes_in_progress': '0',
                       'slash_query_in_progress': False}, ...more validators]
                  'deposit_address':
                      'stride1ayccyk99tdu2ly2xuafuhwexqrwwxj3c58yueccn28gp4p3cm7ysajdr5w',
                  'withdrawal_ica_address':
                      'comdex1frwz448nerqg0cvt2277mua3gu6tw5tu85csst270klagenw47lsrlnn85',
                  'fee_ica_address':
                      'comdex16gsggz28xvam6sq5qu6llthg2nrwdx3w0guluhh6afgdpssel3pqgpzlag',
                  'delegation_ica_address':
                      'comdex1qj6rdc6qwqnat5scej42299meeke455gpxy4cyan7ktfasd3wt5q06dyv6',
                  'redemption_ica_address':
                      'comdex1p4pkh5af7fdyhk2ug8zg9xtgwyypgj2ejqwgkklty3u9usx2wgvqqu663c',
                  'total_delegations': '3931191365862',
                  'last_redemption_rate': '1.162131533280880561',
                  'redemption_rate': '1.162388595082765474',
                  'min_redemption_rate': '1.033653977192886878',
                  'max_redemption_rate': '1.196862499907553227',
                  'min_inner_redemption_rate': '1.138890000000000000',
                  'max_inner_redemption_rate': '1.171390000000000000',
                  'lsm_liquid_stake_enabled': False,
                  'halted': False},
                  ...more host zones]

    """
    stakeibc_response = request(f"{config.stride.api_endpoint}/{HOST_ZONE_QUERY}")
    stakeibc_host_zones = stakeibc_response["host_zone"]

    if not include_multisig_hosts:
        return stakeibc_host_zones

    staketia_host_zone = get_host_zone(CELESTIA_CHAIN_ID, cast_types=False)
    stakedym_host_zone = get_host_zone(DYMENSION_CHAIN_ID, cast_types=False)

    stakedym_response = request(f"{config.stride.api_endpoint}/{MULTISIG_HOST_ZONE_QUERY.format(module=STAKEDYM)}")
    stakedym_host_zone = stakedym_response["host_zone"]

    return stakeibc_host_zones + [staketia_host_zone, stakedym_host_zone]


def _cast_host_zone_fields(host_zone: Dict[str, Any]) -> Dict[str, Any]:
    """
    Casts the host zone int and float types
    """
    float_columns = [
        "redemption_rate",
        "min_redemption_rate",
        "max_redemption_rate",
        "min_inner_redemption_rate",
        "max_inner_redemption_rate",
        "total_delegations",
    ]
    int_columns = ["unbonding_period", "delegated_balance"]

    for column in [c for c in float_columns if c in host_zone]:
        host_zone[column] = float(host_zone[column])
    for column in [c for c in int_columns if c in host_zone]:
        host_zone[column] = int(host_zone[column])

    return host_zone


def get_host_zone(chain_id: str, cast_types: bool = True, **kwargs) -> Dict[str, Any]:
    """
    Queries a stakeibc host zone, returning a dict with the host zone structure and fields casted
    """
    query = f"Stride-Labs/stride/stakeibc/host_zone/{chain_id}"
    if chain_id in [CELESTIA_CHAIN_ID, DYMENSION_CHAIN_ID]:
        query = MULTISIG_HOST_ZONE_QUERY.format(module=STAKETIA)
    if chain_id == "dymension_1100-1":
        query = MULTISIG_HOST_ZONE_QUERY.format(module=STAKEDYM)

    host_zone = request(f"{config.stride.api_endpoint}/{query}", **kwargs)["host_zone"]

    if cast_types:
        host_zone = _cast_host_zone_fields(host_zone)

    return host_zone


def get_deposit_records(
    chain_id: str,
    status: Optional[types.DepositRecordStatus] = None,
    block_height: int = 0,
) -> List[Dict[str, Any]]:
    """
    Queries all the deposit records for a given host zone with optional status filter

    E.g.
    [
        {
            "id": "36310",
            "amount": "5305210",
            "denom": "uluna",
            "host_zone_id": "phoenix-1",
            "status": "DELEGATION_QUEUE",
            "deposit_epoch_number": "2424",
            "source": "STRIDE"
        },
    ]
    """
    url = f"{config.stride.api_endpoint}/{DEPOSIT_RECORDS_QUERY.format(chain_id=chain_id)}"
    deposit_records = request(url, block_height=block_height)["deposit_record"]
    if status:
        deposit_records = [dr for dr in deposit_records if dr["status"] == status]
    return deposit_records


def get_unbonding_records(
    chain_id: str,
    status: Optional[types.UnbondingRecordStatus] = None,
    block_height: int = 0,
) -> List[Dict[str, Any]]:
    """
    Queries all the unbonding records for a given host zone with optional status filter

    E.g.
    [
        {
            "epoch_number": "575",
            "st_token_amount": "3218590",
            "native_token_amount": "0",
            "denom": "ucmdx",
            "host_zone_id": "comdex-1",
            "unbonding_time": "1713812526371636619",
            "status": "CLAIMABLE",
            "user_redemption_records": [
                "comdex-1.575.comdex1gwnfjj65zhxmtnpxzy625cpx692lfjuwlqeg8p",
                ...
            ]
        },
        ...
    ]
    """
    # Query the epoch unbonding records
    url = f"{config.stride.api_endpoint}/{UNBONDING_RECORDS_QUERY}"
    epoch_unbondings = query_list_with_pagination(url, rel_key="epoch_unbonding_record", block_height=block_height)

    # The structure from the response consists of:
    # - List of epoch unbonding records - one record per epoch
    # - Within each epoch unbonding record, there's one host zone unbonding record per host
    # This function returns the host zone unbonding record
    host_zone_unbondings = []
    for epoch_unbonding in epoch_unbondings:
        epoch_number = epoch_unbonding["epoch_number"]
        for host_zone_unbonding in epoch_unbonding["host_zone_unbondings"]:
            chain_id_match = host_zone_unbonding["host_zone_id"] == chain_id
            status_match = not status or host_zone_unbonding["status"] == status

            if chain_id_match and status_match:
                host_zone_unbonding["epoch_number"] = epoch_number
                host_zone_unbondings.append(host_zone_unbonding)

    return host_zone_unbondings


def get_unbonding_queue_records(chain_id: str, block_height: int = 0) -> List[Dict[str, Any]]:
    """
    Queries all the unbonding records that are ready to initiate an unbonding
    This is identified by records in status UNBONDING_QUEUE with a non-zero unbonding amount
    """
    unbonding_records = get_unbonding_records(
        chain_id=chain_id,
        block_height=block_height,
        status=types.UnbondingRecordStatus.UNBONDING_QUEUE,
    )
    return [ur for ur in unbonding_records if int(ur["native_token_amount"]) > 0]


def get_unbonded_records(
    chain_id: str,
    block_height: int = 0,
    filter_unbonded_last_epoch: bool = False,
) -> List[Dict[str, Any]]:
    """
    Queries the list of all unbonding records records that have finished unbonding
    This is identified by records in status EXIT_TRANSFER_QUEUE with an unbonding time
    in the past
    Optionally filter to records that just unbonded last epoch
    """
    unbonding_records = get_unbonding_records(
        chain_id=chain_id,
        block_height=block_height,
        status=types.UnbondingRecordStatus.EXIT_TRANSFER_QUEUE,
    )

    # If we're fetching an older block, use that block's time as the "current time"
    current_time = int(datetime.datetime.now().timestamp() * 1e9)
    if block_height != 0:
        current_time = int(get_block_time(block_height).timestamp() * 1e9)

    # Filter to the records that have finished unbonding, and optionally also
    # filter to records that just finished during the last epoch
    day = 24 * 60 * 60 * 1e9
    filtered_unbonding_records = []
    for unbonding_record in unbonding_records:
        unbonding_time = int(unbonding_record["unbonding_time"])

        # Ignore records that haven't finished unbonding yet
        if unbonding_time > current_time:
            continue

        # If filtering from last epoch, ignore records that unbonded over a day ago
        if filter_unbonded_last_epoch and (current_time - unbonding_time) > day:
            continue

        filtered_unbonding_records.append(unbonding_record)

    return filtered_unbonding_records


def get_user_redemption_records(chain_id: Optional[str] = None) -> list[dict]:
    """
    Queries all user redemption records with optional chain_id filter

    [
        {
            "id": "comdex-1.601.comdex1fq0klaec7s59drpl93w6yycgqqtd3d38d34zn0",
            "receiver": "comdex1fq0klaec7s59drpl93w6yycgqqtd3d38d34zn0",
            "native_token_amount": "63303481323",
            "denom": "ucmdx",
            "host_zone_id": "comdex-1",
            "epoch_number": "601",
            "claim_is_pending": false,
            "st_token_amount": "51025461480"
        },
        ...
    """
    url = f"{config.stride.api_endpoint}/{REDEMPTION_RECORDS_QUERY}"
    redemption_records = query_list_with_pagination(url, rel_key="user_redemption_record", max_pages=50)

    if not chain_id:
        return redemption_records

    redemption_records = [rr for rr in redemption_records if rr["host_zone_id"] == chain_id]
    return redemption_records


def _get_host_zone_redemption_rate_slack(host_zone_id: str) -> Dict[str, float]:
    """
    Calculates the slack (margin) between current redemption rate and its bounds
    for a given host zone. Slack is measured in basis points (bps), where 100 bps = 1%.

    Args:
        host_zone_id: The ID of the host zone to check

    Returns:
        Dict containing redemption rate info:
            rr: current redemption rate
            down_slack: slack to lower bound in bps
            up_slack: slack to upper bound in bps
            halted: whether zone is halted
    """
    host_zone = get_host_zone(host_zone_id)

    rr = float(host_zone['redemption_rate'])
    min_rr = float(host_zone['min_redemption_rate'])
    max_rr = float(host_zone['max_redemption_rate'])
    inner_min_rr = float(host_zone['min_inner_redemption_rate'])
    inner_max_rr = float(host_zone['max_inner_redemption_rate'])

    tighter_bound_min = max(min_rr, inner_min_rr)
    tighter_bound_max = min(max_rr, inner_max_rr)

    down_slack = (rr - tighter_bound_min) * 100 * 100 / rr
    up_slack = (tighter_bound_max - rr) * 100 * 100 / rr

    return {'rr': rr, 'down_slack': down_slack, 'up_slack': up_slack, 'halted': host_zone['halted']}


def get_redemption_rate_slack() -> pd.DataFrame:
    """
    Gets redemption rate slack information for all host zones.
    Slack is measured in basis points (bps), where 100 bps = 1%.

    Returns:
        DataFrame with columns:
            rr: current redemption rate
            down_slack: slack to lower bound in bps
            up_slack: slack to upper bound in bps
            halted: whether zone is halted
        Indexed by host_zone_id
    """
    df_list: List[Dict[str, Any]] = []

    for host_zone in config.host_zones:
        slack_data = _get_host_zone_redemption_rate_slack(host_zone.id)
        df_list.append({'host_zone_id': host_zone.id, **slack_data})

    # Handle empty df_list case
    if not df_list:
        return pd.DataFrame(columns=['rr', 'down_slack', 'up_slack', 'halted'])

    return pd.DataFrame(df_list).set_index('host_zone_id')


def get_redemption_rate_slack_string() -> str:
    """
    Gets formatted string representation of redemption rate slack for all host zones.
    Slack is measured in basis points (bps), where 100 bps = 1%.

    Returns:
        Formatted string showing slack values for each host zone
    """
    df = get_redemption_rate_slack()
    output = ""

    for i, r in df.iterrows():
        output += '{:<16}\tRR: {:.6f}\tDown Slack: {:.2f}bps\tUp Slack: {:.2f}bps\n'.format(
            i, r['rr'], r['down_slack'], r['up_slack']
        )

    return output


def get_lsm_deposit_records(chain_id: str) -> List[Dict[str, Any]]:
    """
    Queries all the LSM deposit records

    [
        {
            "deposit_id": "800000.cosmoshub-4.strideXXX.cosmosvaloperXXX/1",
            "chain_id": "cosmoshub-4",
            "ibc_denom": "ibc/cosmosvaloperXXX/1",
            "staker_address": "strideXXX",
            "validator_address": "cosmosvaloperXXX",
            "amount": "10000",
            "st_token": {
                "amount": "10000",
                "denom": "stuatom"
            }
            "status": "DEPOSIT_PENDING"
        },
    ]
    """
    params = {"chain_id": chain_id}
    url = f"{config.stride.api_endpoint}/{LSM_RECORDS_QUERY}"
    deposit_records = request(url, params=params)["deposits"]
    return deposit_records


def get_multisig_delegation_records(module: str, include_archived: bool = False) -> List[Dict]:
    """
    Queries the delegation records from staketia or stakedym
    Optionally include archive records

    Example response:
    [
        {
            'id': '515',
            'native_amount': '195100000',
            'status': 'DELEGATION_QUEUE',
            'tx_hash': ''
        },
        ...
    }
    """
    url = f"{config.stride.api_endpoint}/{MULTISIG_DELEGATION_RECORDS_QUERY.format(module=module)}"
    params = {"include_archived": include_archived}
    delegation_records = request(url, params=params)
    return delegation_records["delegation_records"]


def get_multisig_unbonding_records(module: str, include_archived: bool = False) -> List[Dict]:
    """
    Queries the celestia unbonding records from staketia or stakedym
    Optionally include archive records

    Args:
      module: str
      Custom multisig module name. e.g. `staketia` and `stakedym`

    Example response:
    [
        {
            'id': '1',
            'status': 'ACCUMULATING_REDEMPTIONS',
            'st_token_amount': '0',
            'native_amount': '0',
            'unbonding_completion_time_seconds': '0',
            'undelegation_tx_hash': '',
            'unbonded_token_sweep_tx_hash': '',
        },
        ...
    ]
    """
    url = f"{config.stride.api_endpoint}/{MULTISIG_UNBONDING_RECORDS_QUERY.format(module=module)}"
    params = {"include_archived": include_archived}
    unbonding_records = request(url, params=params)
    return unbonding_records["unbonding_records"]


def get_multisig_redemption_records(
    module: str,
    address: Optional[str] = None,
    unbonding_record_id: Optional[int] = None,
) -> List[Dict]:
    """
    Queries the celestia redemption records from staketia or stakedym
    Optionally include archive records

    Args:
      module: str
      Custom multisig module name. e.g. `staketia` and `stakedym`
    """
    params: Dict[str, Any] = {}
    if address:
        params["address"] = address
    if unbonding_record_id is not None:
        params["unbonding_record_id"] = unbonding_record_id

    url = f"{config.stride.api_endpoint}/{MULTISIG_REDEMPTION_RECORDS_QUERY.format(module=module)}"
    redemption_records = request(url, params=params)
    return redemption_records["redemption_record_responses"]


def get_rate_limits(**kwargs):
    """
    Queries all rate limits

    Returns:
      rate_limits: List[Dict]
      e.g. [{'path': {'denom': 'staevmos', 'channel_id': 'channel-9'},
            'quota': {'max_percent_send': '25',
             'max_percent_recv': '25',
             'duration_hours': '24'},
            'flow': {'inflow': '1065895546366311315936',
             'outflow': '1476888293332989296879000',
             'channel_value': '15104662663116448541290611'}}, ...]
    """
    endpoint = f"{config.stride.api_endpoint}/{RATE_LIMIT_QUERY}"
    host_zone = request(endpoint, **kwargs)["rate_limits"]
    return host_zone


def get_pending_interchain_queries(chain_id: Optional[str] = None, block_height: int = 0) -> List[Dict[str, Any]]:
    """
    Gets the list of all pending ICQs on stride

    E.g.
    [
        {
            "id": "86170fade2b01f18a1f5e448c8a9dabdc60293151828f881a40708396ec383e0",
            "connection_id": "connection-0",
            "chain_id": "cosmoshub-4",
            "query_type": "store/bank/key",
            "request_data": ...bytestring...,
            "callback_module": "stakeibc",
            "callback_id": "withdrawalbalance",
            "callback_data": ...bytestring...,
            "timeout_policy": "REJECT_QUERY_RESPONSE",
            "timeout_duration": "1hr",
            "timeout_timestamp": "1714689884000000000",
            "request_sent": true,
            "submission_height": 80000
        }
        ...
    ]
    """
    url = f"{config.stride.api_endpoint}/{PENDING_ICQ_QUERY}"
    queries = request(url, block_height=block_height)["pending_queries"]
    if chain_id:
        queries = [query for query in queries if query["chain_id"] == chain_id]
    return queries


def get_callback_data(
    chain_id: Optional[str] = None,
    channel_id: Optional[str] = None,
    port_id: Optional[str] = None,
    callback_id: Optional[str] = None,
    block_height: int = 0,
) -> List[Dict[str, Any]]:
    """
    Gets all the ica or ibc callback data stored on stride, with optional filters

    E.g.
    [
        {
            "callback_key": "icacontroller-cosmoshub-4.DELEGATION.channel-1.23",
            "port_id": "icacontroller-cosmoshub-4.DELEGATION",
            "channel_id": "channel-1",
            "sequence": "23",
            "callback_id": "delegate",
            "callback_args": "...bytestring..."
        }
    ]
    """
    url = f"{config.stride.api_endpoint}/{CALLBACK_DATA_QUERY}"
    callback_data = query_list_with_pagination(url, rel_key="callback_data", block_height=block_height)

    filtered_callback_data = []
    for data in callback_data:
        chain_id_match = not chain_id or chain_id in data["port_id"]
        channel_id_match = not channel_id or data["channel_id"] == channel_id
        port_id_match = not port_id or data["port_id"] == port_id
        callback_id_match = not callback_id or data["callback_id"] == callback_id

        if all([chain_id_match, channel_id_match, port_id_match, callback_id_match]):
            filtered_callback_data.append(data)

    return filtered_callback_data


def get_validators(api_endpoint: str = config.stride.api_endpoint) -> List[Dict[str, Any]]:
    """
    Queries the list of validators from a chain
    """
    url = f"{api_endpoint}/{VALIDATORS_QUERY}"
    return query_list_with_pagination(url, rel_key="validators")


def get_validator_slashes(api_endpoint: str, validator_address: str) -> List[Dict[str, str]]:
    """
    Queries the list of all slashes for a particular validator
    The start and end heights are required with the query
    An arbitrarily large end height to get all slashes
    """
    url = f"{api_endpoint}/{VALIDATOR_SLASHES_QUERY.format(validator_address=validator_address)}"
    params = {"starting_height": "0", "ending_height": "10000000000000000"}
    return query_list_with_pagination(url, rel_key="slashes", params=params)


def get_redemption_rate(token: str) -> float:
    """
    Queries the redemption rate for a particular token
    """
    chain_config_id = config.get_chain(ticker=token).id
    if token == 'TIA':
        chain_config_id = config.get_chain(name='celestia').id
    host_zone = get_host_zone(chain_config_id)
    return float(host_zone["redemption_rate"])


def get_tvl_in_utokens(host_zone_id: str) -> float:
    """
    Queries the stride TVL for a given zone (denominated in the native token)
    """
    host_zone_config = config.get_chain(id=host_zone_id)
    host_zone = get_host_zone(host_zone_id)
    delegation_key = "total_delegations" if host_zone_config.ica_enabled else "delegated_balance"
    return int(host_zone[delegation_key]) / pow(10, host_zone_config.denom_decimals)


def get_latest_block(rpc_endpoint: str = config.stride.rpc_endpoint) -> int:
    """
    Queries the latest block time for a given chain
    """
    url = f"{rpc_endpoint}/status"
    resp = request(url)
    return int(resp["result"]["sync_info"]["latest_block_height"])


def convert_cosmos_address(address: str, new_prefix: str) -> str:
    """
    Converts a Cosmos address to a different zone

    e.g. convert_cosmos_address("stride1am99pcvynqqhyrwqfvfmnvxjk96rn46le9j65c", "osmo")
         would return "osmo1am99pcvynqqhyrwqfvfmnvxjk96rn46lj4pkkx"
    """
    _, data = bech32.bech32_decode(address)
    if data is None:
        raise ValueError("invalid address")
    return bech32.bech32_encode(new_prefix, cast(List[int], data))


def get_balances(
    address: str,
    block_height: int = 0,
    api_endpoint: str = config.stride.api_endpoint,
    cache_response: bool = False,
) -> Dict[str, int]:
    """
    Returns the balance of the given address across all tokens,
    returned as a dictionary of token -> balance
    """
    url = f"{api_endpoint}/{ACCOUNT_BALANCE_QUERY.format(address=address)}"
    response = request(url, block_height=block_height, cache_response=cache_response)
    return {balance["denom"]: int(balance["amount"]) for balance in response["balances"]}


def get_balance(
    address: str,
    denom: str,
    block_height: int = 0,
    api_endpoint: str = config.stride.api_endpoint,
    cache_response: bool = False,
) -> int:
    """
    Returns the balance for a given address and token
    """
    url = f"{api_endpoint}/{ACCOUNT_BALANCE_QUERY.format(address=address)}/by_denom"
    params = {"denom": denom}
    response = request(url, block_height=block_height, params=params, cache_response=cache_response)
    return int(response["balance"]["amount"])


def get_supply(
    denom: str,
    block_height: int = 0,
    api_endpoint: str = config.stride.api_endpoint,
    cache_response: bool = False,
) -> int:
    """
    Returns the total token supply of a given token
    """
    url = f"{api_endpoint}/{SUPPLY_QUERY}"
    params = {"denom": denom}
    resp = request(url, block_height=block_height, params=params, cache_response=cache_response)
    return int(resp["amount"]["amount"])


@lru_cache
def get_block_time(height: int, rpc_endpoint: str = config.stride.rpc_endpoint) -> datetime.datetime:
    """
    Returns the timestamp of the given block height on a chain
    """
    url = f"{rpc_endpoint}/block?height={height}"
    resp = request(url)
    block_time = resp["result"]["block"]["header"]["time"]
    block_datetime = datetime.datetime.fromisoformat(block_time)
    return block_datetime


@lru_cache
def get_icns_name(address: str) -> str:
    """
    Returns the ICNS name for the given Cosmos-SDK address, if it exists.
    Queries the ICNS smart contract on Osmosis.

    Args:
        address: The Cosmos-SDK address to look up

    Returns:
        str: The ICNS name if found

    Raises:
        KeyError: If Osmosis configuration is not found
    """
    if "osmosis" not in config.host_zones:
        raise KeyError("Osmosis host zone configuration not found")

    osmosis_config = config.get_host_chain("osmosis")
    contract_address = "osmo1xk0s8xgktn9x5vwcgtjdxqzadg88fgn33p8u9cnpdxwemvxscvast52cdd"
    query_msg = {"primary_name": {"address": address}}

    time.sleep(0.01)  # Rate limiting for API calls
    response = query_wasm_contract(
        contract_address,
        query_msg=query_msg,
        api_endpoint=osmosis_config.api_endpoint,
    )

    return response["name"]


def get_account_info(
    address: str,
    api_endpoint: str = config.stride.api_endpoint,
):
    """
    Returns the account information for a given address (including the sequence number)

     {'account':
         {'@type': '/cosmos.auth.v1beta1.BaseAccount',
          'address': 'stride1am99pcvynqqhyrwqfvfmnvxjk96rn46le9j65c',
          'pub_key': {'@type': '/cosmos.crypto.secp256k1.PubKey',
                      'key': 'A138uH3qwMpMbtRnvtuHgJMO6Cq+9iGlFkGUTYpVRQ9J'},
      'account_number': '90',
      'sequence': '553'}}
    """
    url = f"{api_endpoint}/{ACCOUNT_QUERY.format(address=address)}"
    return request(url)


def get_tx(hash: str, api_endpoint: str = config.stride.api_endpoint) -> Dict:
    """
    Queries a specific transaction from the tx hash
    """
    url = f"{api_endpoint}/{TXS_QUERY}/{hash}"
    return request(url)


def get_txs(event_filters: List[str], api_endpoint: str = config.stride.api_endpoint, limit=None) -> Dict:
    """
    Queries the txs endpoint with event filters
    Event filters are of the form `{event_type}.{event_attribute}={attribute_value}`
    Note: This only returns more recent txs that haven't already been pruned from the node

    E.g. To query for IBC transfer sent from a given address, you could use the filter:
         "ibc_transfer.sender='strideXXX'"

    The returned response structure returns list of txs and tx_responses where the indicies
    line up between the two arrays
    {
        "txs": [...],
        "tx_responses": [...]
    }
    """
    if len(event_filters) == 0:
        raise ValueError("At least one event filter is required when querying txs")

    url = f"{api_endpoint}/{TXS_QUERY}"
    params: List[Tuple[str, str]] = [("events", event_filter) for event_filter in event_filters]
    if limit is not None:
        params.append(('limit', limit))
    txs = request(url, params=params)

    return txs


# TODO: Rename to be more specific with address/sequence account query
def get_tx_info(
    address: str,
    sequence: Union[str, int],
    api_endpoint: str = config.stride.api_endpoint,
) -> Dict:
    """
    Returns the tx info for a given address and sequence number

    Response format:
     {'txs': [...]}
    """
    event_filter = TX_BY_ACCOUNT_EVENT.format(address=address, sequence=sequence)
    return get_txs(event_filters=[event_filter], api_endpoint=api_endpoint)


def generate_vesting_account(
    start_time_in_local_tz: str,
    total_tokens: int,
    seconds_in_period: int = 3600,
    number_of_days: int = 30,
    output_file: str = "vesting_account.json",
) -> str:
    """
    Generates a vesting account configuration that distributes tokens over time.

    Args:
        start_time_in_local_tz: Start time in "YYYY-MM-DD HH:MM" format in local timezone
        total_tokens: Total number of ustrd tokens to vest
        seconds_in_period: Number of seconds in each vesting period
        number_of_days: Total number of days to vest over
        output_file: Output JSON file path

    Returns:
        str: JSON configuration for the vesting account
    """
    # Convert local time to UTC timestamp
    timezone = pytz.timezone(config.timezone)
    start_time_dt = datetime.datetime.strptime(start_time_in_local_tz, "%Y-%m-%d %H:%M")
    local_dt = timezone.localize(start_time_dt)
    utc_dt = local_dt.astimezone(pytz.UTC)
    start_time_ts: int = int(utc_dt.timestamp())  # Explicitly cast to int

    out = '{ "start_time": ' + str(start_time_ts) + ',\n  "periods":[\n'
    num_periods = int(number_of_days * 24 * 60 * 60) // seconds_in_period
    tokens_per_period = int(total_tokens / num_periods)

    for i in range(num_periods):
        out += "    {\n"
        out += f'    "coins": "{tokens_per_period}ustrd",\n'  # noqa: E231
        out += f'    "length_seconds":{seconds_in_period}\n'  # noqa: E231
        out += "  }"
        if i != num_periods - 1:
            out += ","
        out += "\n"
    out += "]}"

    with open(output_file, "w") as f:
        f.write(out)
    return out


def get_block_height_in_past(
    target_time: Optional[datetime.datetime] = None,
    target_time_offset: Optional[datetime.timedelta] = None,
    error_tolerance: datetime.timedelta = datetime.timedelta(minutes=5),
    seconds_per_block: int = 6,
    rpc_endpoint: str = config.stride.rpc_endpoint,
) -> int:
    """
    Gets the block height at a specified time by binary searching at different heights

    Args:
        target_time (datetime): the target time to search for
            (e.g. search for the block at time 2024-01-01 01:00:00 UTC)
        target_time_offset (timedelta): the target time to search for,
            defined as an offset from the current time
            (e.g. search for the block 24 hours ago)
        error_tolerance (timedelta): max time delta before the height is considered found
        seconds_per_block: block time to use for the estimation start

    Returns:
        The block height at the specified time
    """
    # Get the current time and latest block height
    current_time = datetime.datetime.now(tz=datetime.timezone.utc)
    latest_block = get_latest_block(rpc_endpoint=rpc_endpoint)

    # Depending on whether the target time or target_time_offset was used,
    # calculate the parameter that was not provided
    if target_time and not target_time_offset:
        target_time_offset = current_time - target_time
    elif target_time_offset and not target_time:
        target_time = current_time - target_time_offset
    else:
        raise ValueError("Either target time or target time offset must be specified (but not both)")

    # Using the target offset, determine the block delta to start our search, based
    # on the estimated block time
    blocks_in_past = int(target_time_offset.total_seconds() / seconds_per_block)
    estimated_height = latest_block - blocks_in_past

    # Continually loop over the following until we find a block that lines up with
    # our target time (within our margin of error)
    #  - Guess a height
    #  - Find the time at that height
    #  - Check if the time is close enough to our target
    #  - Refine our block height guess and repeat
    while True:
        estimated_time = get_block_time(estimated_height, rpc_endpoint=rpc_endpoint)

        time_error = target_time.timestamp() - estimated_time.timestamp()
        if abs(time_error) < error_tolerance.total_seconds():
            return estimated_height

        blocks_correction = int(time_error / seconds_per_block)
        estimated_height += blocks_correction


def get_block_height_one_day_ago() -> int:
    """
    Get the block height from 1 day ago
    """
    return get_block_height_in_past(target_time_offset=datetime.timedelta(hours=24))


def get_unbonding_tokens_on_address(
    delegator_address: str,
    api_endpoint: str = config.stride.api_endpoint,
) -> Dict[str, int]:
    """
    Returns a dict mapping from "validator_address" to "num tokens delegated", given a delegator address

    Raw response example (unbonding_endpoint)
    {
      "unbonding_responses": [
        {
          "delegator_address": "cosmos10...28",
          "validator_address": "cosmosvaloper1d...h9",
          "entries": [
            {
              "creation_height": "18749801",
              "completion_time": "2024-02-06T19:00:28.676639972Z",
              "initial_balance": "3727000742",
              "balance": "3727000742",
              "unbonding_id": "334505",
              "unbonding_on_hold_ref_count": "1"
            }
          ]
        }, ...],
      "pagination": {...}
    }

    Returns
      e.g. {'valoper1': 10, 'valoper2': 20}
    """
    unbonding_endpoint = f"{api_endpoint}/{ACCOUNT_UNBONDINGS_QUERY.format(delegator_address=delegator_address)}"
    unbondings = query_list_with_pagination(unbonding_endpoint, rel_key="unbonding_responses")
    unbonding_amounts: Dict[str, int] = {}
    for unbonding in unbondings:
        unbonding_amounts[unbonding["validator_address"]] = sum(
            int(entry["initial_balance"]) for entry in unbonding["entries"]
        )
    return unbonding_amounts


def get_delegations(delegator_address: str, api_endpoint: str = config.stride.api_endpoint) -> dict[str, int]:
    """
    Queries all the delegations for a given delegator
    Returned as a mapping of validator addresss to delegation amount
    """
    url = f"{api_endpoint}/{DELEGATIONS_QUERY.format(delegator_address=delegator_address)}"
    delegations = query_list_with_pagination(url, rel_key="delegation_responses")

    delegations_by_validator = {}
    for delegation in delegations:
        validator_address = delegation["delegation"]["validator_address"]
        amount = int(delegation["balance"]["amount"])
        delegations_by_validator[validator_address] = amount

    return delegations_by_validator


def _parse_validator_dict(raw_validators: List[dict[str, Any]]) -> pd.DataFrame:
    """
    Given the output of a host_zone's "validator" field,
    this will parse the data into a Pandas DataFrame.

    Will also cast the relevant columns to ints and floats.
    """
    int_fields = [
        "weight",
        "delegation",
        "slash_query_checkpoint",
        "slash_query_progress_tracker",
    ]
    float_cols = [
        "shares_to_tokens_rate",
    ]
    output_cols = [
        "name",
        "address",
        "weight",
        "delegation",
        "slash_query_in_progress",
        "slash_query_progress_tracker",
        "shares_to_tokens_rate",
    ]

    def parse_validator(field_name: str, field_value: Any) -> Any:
        if field_name in int_fields:
            return int(field_value)
        if field_name in float_cols:
            return float(field_value)
        return field_value

    cast_validators = [{k: parse_validator(k, v) for k, v in val_dict.items()} for val_dict in raw_validators]
    return pd.DataFrame(cast_validators, dtype=object)[output_cols]


def get_host_zone_delegations(host_zone_id: str, include_ground_truth: bool = True) -> pd.DataFrame:
    """
    Given a host zone id, returns a Dataframe of validator delegations.

    If `include_ground_truth=True`, then will also return the "true" delegations
    on the host zone delegaiton account.
    """
    host_zone = get_host_zone(host_zone_id)
    validator_df = _parse_validator_dict(host_zone["validators"])
    # If the ground truth isn't requested, return as is
    if not include_ground_truth:
        return validator_df

    # Otherwise, query the ground truth delegations from the actual host chain
    delegation_ica_account = host_zone["delegation_ica_address"]
    api_endpoint = config.get_chain(id=host_zone_id).api_endpoint
    delegations_by_validator = get_delegations(delegation_ica_account, api_endpoint=api_endpoint)

    validator_df["ground_delegation"] = (validator_df["address"].map(delegations_by_validator)).fillna(0)
    validator_df["ground_delegation"] = validator_df["ground_delegation"].apply(int)
    validator_df["delegation_difference"] = validator_df["ground_delegation"] - validator_df["delegation"]

    return validator_df


def get_epochs() -> List[Dict]:
    """
    Returns all the epochs on stride

    Example response:
    {
        {
            'identifier': 'day',
            'start_time': '2022-09-04T19:00:00.451745Z',
            'duration': '86400s',
            'current_epoch': '515',
            'current_epoch_start_time': '2024-01-31T19:00:00.451745Z',
            'epoch_counting_started': True,
            'current_epoch_start_height': '7483499'
        },
        ...
    }
    """
    url = f"{config.stride.api_endpoint}/{EPOCHS_QUERY}"
    epochs = request(url)
    return epochs["epochs"]


def get_day_epoch() -> Dict[str, Any]:
    """
    Returns the "day" epoch struct on Stride

    E.g.
    {
        "identifier": "day",
        "start_time": "2022-09-04T19:00:00.451745Z",
        "duration": "86400s",
        "current_epoch": "607",
        "current_epoch_start_time": "2024-05-02T19:00:00.451745Z",
        "epoch_counting_started": true,
        "current_epoch_start_height": "8829138"
    }
    """
    epochs = get_epochs()
    day_epoch = [epoch for epoch in epochs if epoch["identifier"] == "day"][0]
    return day_epoch


def get_stride_epoch() -> Dict[str, Any]:
    """
    Returns the "stride" epoch struct on stride

    E.g.
    {
        "identifier": "stride_epoch",
        "start_time": "2022-09-04T19:00:00.451745Z",
        "duration": "21600s",
        "current_epoch": "2425",
        "current_epoch_start_time": "2024-05-02T19:00:00.451745Z",
        "epoch_counting_started": true,
        "current_epoch_start_height": "8829138"
    }
    """
    epochs = get_epochs()
    stride_epoch = [epoch for epoch in epochs if epoch["identifier"] == "stride_epoch"][0]
    return stride_epoch


def get_stride_epoch_number() -> int:
    """
    Returns the epoch number for the current "stride" epoch
    """
    stride_epoch = get_stride_epoch()
    return int(stride_epoch["current_epoch"])


def get_day_epoch_number() -> int:
    """
    Returns the epoch number for the current "day" epoch
    """
    day_epoch = get_day_epoch()
    return int(day_epoch["current_epoch"])


def get_stride_epoch_start_time() -> datetime.datetime:
    """
    Returns the epoch start time for the current "stride" epoch
    """
    stride_epoch = get_stride_epoch()
    return datetime.datetime.fromisoformat(stride_epoch["current_epoch_start_time"])


def get_day_epoch_start_time() -> datetime.datetime:
    """
    Returns the epoch start time for the current "day" epoch
    """
    day_epoch = get_day_epoch()
    return datetime.datetime.fromisoformat(day_epoch["current_epoch_start_time"])


def get_stride_epoch_start_height() -> int:
    """
    Returns the epoch start time for the current "stride" epoch
    """
    stride_epoch = get_stride_epoch()
    return int(stride_epoch["current_epoch_start_height"])


def get_day_epoch_start_height() -> int:
    """
    Returns the epoch start time for the current "day" epoch
    """
    day_epoch = get_day_epoch()
    return int(day_epoch["current_epoch_start_height"])


def get_all_host_zone_channels() -> List[Dict[str, Any]]:
    """
    Returns the JSON response from the channels endpoint for all the channels across all host zones
    """
    return request(CHANNELS_SUMMARY_QUERY)


def get_host_zone_channels(chain_id: str) -> Dict[str, Any]:
    """
    Returns the JSON response from the channels endpoint, which holds the client and connection info,
    as well as all the ICA channels

    E.g.
    {
        "chain_id": "cosmoshub-4",
        "client_id": "07-tendermint-0",
        "counterparty_client_id": "07-tendermint-913",
        "connection_id": "connection-0",
        "counterparty_connection_id": "connection-635",
        "transfer_channel_id": "channel-0",
        "counterparty_transfer_channel_id": "channel-391",
        "ica_channels": [
            {
            "type": "DELEGATION",
            "port_id": "icacontroller-cosmoshub-4.DELEGATION",
            "channel_id": "channel-203",
            "counterparty_channel_id": "channel-810",
            "state": "STATE_OPEN",
            "counterparty_state": "STATE_OPEN"
            },
        ...
        ]
    }
    """
    return request(CHANNELS_SUMMARY_QUERY_BY_HOST.format(chain_id=chain_id))


def query_wasm_contract(contract_address: str, query_msg: Dict, api_endpoint: str, block_height: int = 0) -> Dict:
    """
    Queries a cosmowasm contract address with the provided query message
    Response structure is dependent on the particular query
    """
    query_msg_string = json.dumps(query_msg)
    query_msg_encoded = base64.b64encode(query_msg_string.encode("utf-8")).decode("utf-8")

    query_path = COSMWASM_CONTRACT_QUERY.format(contract_address=contract_address, query=query_msg_encoded)
    data = request(f"{api_endpoint}/{query_path}", block_height=block_height)

    return data["data"]


def get_module_accounts(api_endpoint: str = config.stride.api_endpoint) -> List[Dict]:
    """
    Queries the list of all module accounts

    Returns a list of accounts like so:
    [
        {
            "@type": "/cosmos.auth.v1beta1.ModuleAccount",
            "base_account": {
                "address": "stride1fl48vsnmsdzcv85q5d2q4z5ajdha8yu3ksfndm",
                "pub_key": null,
                "account_number": "75",
                "sequence": "0"
            },
            "name": "bonded_tokens_pool",
        }
        ...
    """
    return request(f"{api_endpoint}/{MODULE_ACCOUNTS_QUERY}")["accounts"]


def query_evm_method(method: str, params: list[str], rpc_endpoint: str) -> str:
    """
    Generic querier for evm contract calls
    Returns a hex endcoded response specific to the contract call
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }

    response = request(rpc_endpoint, headers=headers, data=json.dumps(payload))
    return response["result"]


def get_evm_balance(address: str, rpc_endpoint: str) -> int:
    """
    Queries the native token balance of an evm address
    Address should be a hex address with an 0x prefix
    """
    params = [address, "latest"]
    balance_raw = query_evm_method("eth_getBalance", params=params, rpc_endpoint=rpc_endpoint)
    balance = int(balance_raw, 16)
    return balance
