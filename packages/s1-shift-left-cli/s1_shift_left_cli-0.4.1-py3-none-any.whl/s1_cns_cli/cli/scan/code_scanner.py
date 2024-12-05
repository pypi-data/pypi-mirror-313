import logging

from s1_cns_cli.cli.config import init_config_manager
from s1_cns_cli.cli.registry import CodeTypeSubParser, MissingConfig, GET_CONFIG_DATA_API, HttpMethod
from s1_cns_cli.cli.scan import iac, secret
from s1_cns_cli.cli.scan import vulnerability
from s1_cns_cli.cli.utils import check_if_paths_exist, make_request, read_json_file, get_config_path, upsert_s1_cns_cli

LOGGER = logging.getLogger("cli")


def handle_scan_sub_parser(args, cache_directory):
    global_pre_evaluation(args, cache_directory)
    if args.scan_type_sub_parser == CodeTypeSubParser.IAC:
        return iac.iac_parser(args, cache_directory)
    elif args.scan_type_sub_parser == CodeTypeSubParser.SECRET:
        return secret.secret_parser(args, cache_directory)
    elif args.scan_type_sub_parser == CodeTypeSubParser.VULN:
        return vulnerability.vulnerability_parser(args, cache_directory)


# global_pre_evaluation: will check we have updated s1-cns-cli and configs
def global_pre_evaluation(args, cache_directory):
    global_config_file_path = get_config_path(cache_directory)
    if not check_if_paths_exist([cache_directory, global_config_file_path]):
        raise MissingConfig()

    global_config_data = read_json_file(global_config_file_path)
    management_console_url = global_config_data.get("management_console_url")

    if (hasattr(args, 'list_detectors') and args.list_detectors) or (hasattr(args, 'list_plugins') and args.list_plugins):
        data = {
            "global": global_config_data,
            "secret": {},
            "iac": {},
            "vuln": {}
        }
        init_config_manager(data)
        return

    tag = global_config_data.get("tag")
    scope_type = global_config_data.get("scope_type")
    scope_id = global_config_data.get("scope_id")
    if len(args.tag) > 0:
        tag = args.tag

    if len(tag) == 0:
        raise MissingConfig("Missing 'tag', please reconfigure cli or use the '--tag' flag.")

    if len(management_console_url) == 0:
        raise MissingConfig("'Management_console_url' is required, please reconfigure using '--management_console_url "
                            " flag")

    response = make_request(HttpMethod.GET, management_console_url + GET_CONFIG_DATA_API, global_config_data["service_user_api_token"],
                            {"tag": tag, "scopeType": scope_type, "scopeIds": scope_id})

    data = response.json()["data"]

    # merge cli_global_config with response global_config
    data["global"] = {**data["global"], **global_config_data}
    init_config_manager(data)
    upsert_s1_cns_cli(cache_directory)
