#!/usr/bin/env python

import os
import logging
import argparse
import json
from azure_key_vault_report import azure_key_vault_report
from cert_report import certs as crt
from reports import reports
from reports import payloads as webhook_payloads
from message_handler import message_handler
from .post_payloads import post_payloads


########################################################################################################################


class Monitoring(object):
    """Creates alerts and reports from azure key vault records and ssl cert check. The alerts and reports may be posted
    to Slack or MS Teams webhooks.

        - azure_key_vault_report.AzureKeyVaultReport() : to create Key Vault reports or alert
        - cert_report.Certs() : to fetch the SSL certificate status from the URLs
        - cert_report.Report() : to create SSL certificate reports
        - message_handler.MessageHandler() : to post the payloads with the reports and alerts


       Attributes
       ----------
        args : parse_args() object from argparse.ArgumentParser()
            The arguments, passed from command line or the specified default values.
        input_file_ending = string
            The default file ending of json files to be read from (default: ".json")
        json_output_file = string
            The filename of the json log output file
        csv_kv_output_file = string
            The Key Vault report csv output filename
        md_kv_summary_output_file = string
            The Markdown Key Vault summary output filename
        md_kv_report_output_file = string
            The Markdown Key Vault report output filename
        report_full : dict
            The full report which are written to file. To be posted to API -> DB.
        kv : azure_key_vault_report.AzureKeyVaultReport() object
            The object to be called in order to generate the Key Vault reports and/or alerts.
        success : boolean
            If at least one payload is posted it is considered a success, then the notify webhook can be triggered.
        payloads : list
            The list of payloads to be posted.
        slack_workflow_posts : list
            The list of Slack WORKFLOW posts to be posted.
        slack_app : boolean
            Set to true if the webhook is detected to be a Slack APP (and not a Slack WORKFLOW).
        teams_output : boolean
            Set to true if webhook not detected to be a Slack webhook.
        msg_handler : message_handler.MessageHandler() object
            The object to be called in order to post the payloads.
        certs_report : The crt_report.Report() object
            The object to be called in order to generate the SSL certificate reports.
        certs_json = list
            The list of reports as dict for each SSL certificate. To be added to the report_full dict.
        json_data = list
            The list where the read json data will be stored


        Methods
        -------

        set_webhooks(webhook)
            Initiates the MessageHandler() with the provided webhook (if it starts with 'https')

            Also determines if the passed webhook is one of the following types:
            'Slack APP'
            'Slack WEBHOOK'

            If not, it is considered to a 'MS Teams' kind of webhook.

        read_json()
            Try to read every .json file in the json directory.
            If failed to read the file as json, data will be read from file as default text.
            The json files are expected to contain piped json output from 'az keyvault' commands.

        key_vault_report()
            Executes the az keyvault list commands on each provided Key Vault.
            The output results are stored as list of dict objects.

            Then azure_key_vault_report.AzureKeyVaultReport() is initiated with the list of outputs from the
            az commands.

            The methods of the AzureKeyVaultReport() are called based on the provided argparse arguments.

        report_full_json()
            Set 'report_full' to the value of what the called get_report_full() method of the AzureKeyVaultReport()
            returns (dict).

            It also enriches 'report_full' some other key / values (to be passed to API -> DB):
                name: workflow_output_name
                repository_name: GITHUB_REPOSITORY (ENV) (only the name part)
                client_id: AZURE_CLIENT_ID (ENV) (the 'Application ID' of the Azure App. Reg.)
                subscription_id: AZURE_SUBSCRIPTION_ID (ENV) (the Azure subscription id)
                tenant_id: AZURE_TENANT_ID (ENV) (the Azure tenant id)

            The full ssl certificate json report is also added to the 'report_full' dict.

        write_report_full_json()
            Writes the report_full as json to the file provided in the workflow_output_file argparse argument.

        write_kv_report_full_csv()
            Writes full csv Key Vault report.

        write_md_report()
            Writes Markdown Key Vault summary and report.

        kv_alert()
            If the 'alert_threshold' (INT) argument is provided then alert methods of
            AzureKeyVaultReport() will be called in order to return the alert payloads:

            get_teams_payloads() if webhook is detected to not be a Slack kind of webhook
            get_slack_payloads() if the webhook is previously determined to be a Slack APP webhook

        kv_report()
            One of the report methods of AzureKeyVaultReport() will be called in order to return the report payloads:

            get_slack_payloads() if the webhook is previously determined to be a Slack APP webhook
            get_slack_payloads(app=False) if the webhook is previously determined to be a Slack WORKFLOW webhook
            get_teams_payloads() if the webhook is previously determined to be an MS Teams webhook
                If the returned MS Team payload is too large, get_teams_payloads() will be recalled with custom text
                provided. The payload will then only contain the 'facts' from the report (the summary).

        ssl_cert()
            Initiates the crt_report.Report() object with the provided arguments:
                the urls to the SSL certs
                the warning and critical thresholds
                if to include all SSL certs in report (even the OK ones)

           Calls the gen_report() method of crt_report.Report() and
           the certs_report.get_report_json() (to be used in the 'report_full' -> API -> DB)

        ssl_cert_report()
            Calls the get_slack_report() method of crt_report.Report() if the webhook is previously determined
            to be a Slack APP webhook.
                The result will be added to the list of payloads to be posted.
            Calls the get_html_report() method of crt_report.Report() if the webhook is previously determined
            to be an MS Teams webhook
                The result (HTML table) is uses to create an MS Teams payload which are added to the list of payloads.

        prepare_and_post()
            If no payload, then assume to be posted to a Slack Workflow

            If payload to post then check if any additional info should be added prior to posting.
            Posting is done by post_payloads function, which will set success to True if at least one of the posts are
            posted to the report webhook (the value of 'WEBHOOK_REPORT')
            At least one post has to be posted to be considered to be a success.

            If success an empty post to the notify webhook will be posted (the value of 'WEBHOOK_NOTIFY')

        get_success()
            returns the success status

            This is used to determine if an empty post to the notify webhook will be posted
            (the value of 'WEBHOOK_NOTIFY')

          """

    def __init__(self, args):
        """
        Parameters
        ----------
        args : parse_args() object from argparse.ArgumentParser()
        """

        self.args = args
        self.json_dir = "/tmp/az_json"
        self.input_file_ending = ".json"
        self.json_output_file = f"output.json"
        self.csv_kv_output_file = "key_vault_report.csv"
        self.md_kv_summary_output_file = "key_vault_summary.md"
        self.md_kv_report_output_file = "key_vault_report.md"
        self.html_styling_kv = {5: {"will expire in": "yellow",
                                    "expired": "red",
                                    "disabled": "grey"}
                                }
        self.html_styling_ssl = "default"
        self.report_full = {}
        self.kv = None
        self.success = False
        self.payloads = []
        self.slack_workflow_posts = []
        self.slack_app = False
        self.teams_output = False
        self.msg_handler = None
        self.certs_report = None
        self.certs_json = []
        self.json_data = []
        self.md_kv_summary_output = ""
        self.md_kv_report_output = ""

    def set_webhooks(self, webhook):
        """initiates the MessageHandler() with the provided webhook (if it starts with 'https')

        Parameters
        ----------
        webhook : string
            The URL of the webhook
        """

        if "slack.com/services" in str(webhook):
            logging.info("Slack services webhook detected.")
            self.slack_app = True
        elif "slack.com" not in str(webhook):
            logging.info("No slack webhook detected. Assuming post to MS Teams.")
            self.teams_output = True

        if str(webhook).startswith("https"):
            self.msg_handler = message_handler.MessageHandler(webhook)
        else:
            logging.info("No proper webhook detected.")

    def read_json(self):
        """reads .json files from the json dir"""
        if not os.path.isdir(self.json_dir):
            logging.error(f"'{self.json_dir}' dir not found.")
            return

        for json_filename in os.listdir(self.json_dir):
            if json_filename.endswith(self.input_file_ending):
                json_file = os.path.join(self.json_dir, json_filename)

                if not os.path.isfile(json_file):
                    continue

                safe_path = os.path.realpath(json_file)
                common_base = os.path.commonpath([self.json_dir, safe_path])
                if common_base != self.json_dir:
                    continue

                if os.path.basename(safe_path) != json_filename:
                    continue

                with open(json_file) as f:
                    json_data = {}
                    failed = False
                    if os.stat(json_file).st_size > 0:
                        try:
                            json_data = json.load(f)
                        except ValueError:
                            logging.error(f"Unable to read file '{json_file}' as json")
                            failed = True

                    if json_data:
                        self.json_data.append(json_data)

                    if failed:
                        with open(json_file) as e:
                            error_message = e.read()
                            if error_message:
                                logging.error(f"Content of '{json_file}' read as error message")
                                self.json_data.append(str(error_message))

        if self.json_data:
            return True

    def key_vault_report(self):
        """Initiates the key vault report."""

        # Return if no vaults to parse
        if not self.json_data:
            logging.error("No Key Vault json data to parse.")
            return

        # The report is generated by using the pip package ops-py-azure-key-vault-report
        # If argument 'include_no_expiration' is not provided, then the variable
        # 'ignore_no_expiration' is then set to True
        self.kv = azure_key_vault_report.AzureKeyVaultReport(self.json_data)
        self.kv.parse_results()
        self.kv.add_summary()
        self.kv.add_report(expire_threshold=self.args.expire_threshold,
                           ignore_no_expiration=self.args.include_no_expiration,
                           include_all=self.args.include_all,
                           alert_threshold=self.args.alert_threshold,
                           teams_alerts=self.teams_output
                           )

    def report_full_json(self):
        """set 'report_full' to the return value of get_report_full() method of the AzureKeyVaultReport()"""

        if self.kv:
            self.report_full = self.kv.get_report_full()
            workflow_output_name = str(WORKFLOW_OUTPUT_NAME).strip().lower().replace(" ", "_")[:40]
            self.report_full["name"] = workflow_output_name
            self.report_full["repository_name"] = str(GITHUB_REPOSITORY).split("/")[-1]
            self.report_full["client_id"] = AZURE_CLIENT_ID
            self.report_full["subscription_id"] = AZURE_SUBSCRIPTION_ID
            self.report_full["tenant_id"] = AZURE_TENANT_ID

        self.report_full["ssl_certs"] = self.certs_json

    def write_report_full_json(self):
        """writes the report_full as json to the file provided set in the workflow_output_file argparse argument"""

        # Write full report as json to file
        with open(self.json_output_file, 'w') as f:
            json.dump(self.report_full, f, default=str)

    def write_kv_report_full_csv(self):
        """writes full csv Key Vault report"""

        out = ""
        if self.report_full:
            report = self.report_full.get("report")
            if report:
                rows = report.get("rows")
                if rows:
                    out = reports.dict_to_csv(rows)

        if out:
            with open(self.csv_kv_output_file, 'w') as f:
                f.write(out)

    def create_md_report(self):
        """writes Markdown Key Vault summary and report"""

        summary = self.kv.get_summary()
        if summary:
            rows = []
            for k, v in summary.items():
                rows.append([k, v])
            if rows:
                rows.insert(0, ["Description", "Count"])
                md = reports.Markdown(rows)
                md.set_widths()
                self.md_kv_summary_output = md.get_output(1)

        report = self.kv.get_report()
        rows = reports.dict_to_rows(report)
        if rows:
            md = reports.Markdown(rows)
            md.set_widths()
            self.md_kv_report_output = md.get_output()

    def write_md_report(self):
        """writes Markdown Key Vault summary and report"""

        if not self.md_kv_summary_output or not self.md_kv_report_output:
            self.create_md_report()

        if self.md_kv_summary_output:
            with open(self.md_kv_summary_output_file, 'w') as f:
                f.write(self.md_kv_summary_output)

        if self.md_kv_report_output:
            with open(self.md_kv_report_output_file, 'w') as f:
                f.write(self.md_kv_report_output)

    def kv_alert(self):
        """calls the AzureKeyVaultReport() in order to return the alert payloads to be used"""

        if not self.kv:
            logging.error("Key Vault reports not found.")
            return

        payloads = None
        if isinstance(self.args.alert_threshold, int):

            # If the webhook is previously determined to be an MS Teams webhook, then get the teams alert payloads
            if self.teams_output:
                payloads = self.kv.get_teams_alerts()

            # If the webhook is previously determined to be a Slack App webhook, then get the slack alert payloads
            if self.slack_app:
                payloads = self.kv.get_slack_alerts()

        if payloads:
            self.payloads += payloads

    def kv_report(self):
        """calls one of the report methods of AzureKeyVaultReport() order to return the report payloads"""

        if not self.kv:
            logging.error("Key Vault reports not found.")
            return

        # If the webhook is previously determined to be a Slack App webhook, then get the slack report payloads
        if self.slack_app:
            self.create_md_report()

            # Payload 1 - The Summary
            title = f"{self.args.title} - Summary"
            slack_app = webhook_payloads.SlackApp(title, self.md_kv_summary_output,
                                                  max_chars=self.args.slack_split_chars)
            payload = slack_app.get_payloads()
            if payload:
                self.payloads += payload

            # Payload 2 -> n: The report
            slack_app = webhook_payloads.SlackApp(self.args.title, self.md_kv_report_output,
                                                  max_chars=self.args.slack_split_chars)
            payloads = slack_app.get_payloads()
            if payloads:
                self.payloads += payloads

        if self.teams_output:
            summary = self.kv.get_summary()
            rows = reports.dict_to_rows(self.kv.get_report())
            header = rows.pop(0)

            html_table = reports.HTMLTable(header, skip_ok=False)
            html_table.init_html_table()
            for row in rows:
                html_table.add_html_row(*row, styling=self.html_styling_kv)
            html = html_table.get_table()

            ms_teams_payload = webhook_payloads.MSTeamsPayload(self.args.title, html, summary)
            ms_teams_payload.set_json_facts()
            payload = ms_teams_payload.get_payload()

            # If payload is too large with the report as html, a new payload is generated.
            # A custom text is provided instead, which will be used instead of the html report.
            if len(payload) > self.args.teams_max_chars:
                warning_msg = (f"The {self.args.title} length is above the character limit count "
                               f"of {self.args.teams_max_chars}")
                logging.warning(warning_msg)
                title = f"WARNING! {warning_msg}"
                text = "The html report have been omitted from the report due to size limits."
                ms_teams_payload = webhook_payloads.MSTeamsPayload(title, text, summary)
                ms_teams_payload.set_json_facts()
                payload = ms_teams_payload.get_payload()

            if payload:
                self.payloads.append(payload)

    def ssl_cert(self):
        """initiates the cert report classes and calls needed methods to generate reports"""

        # Return if no vaults to parse
        if not self.args.ssl_certs:
            logging.error("No SSL certs provided.")
            return

        ssl_certs = self.args.ssl_certs

        # If only one key vault to check, ensure it is treated as a list
        if isinstance(ssl_certs, str):
            ssl_certs = [ssl_certs]

        if ssl_certs:
            self.certs_report = crt.Certs(ssl_certs,
                                          warning=self.args.ssl_warning_threshold,
                                          critical=self.args.ssl_critical_threshold)
            self.certs_report.parse_certs()
            self.certs_report.gen_report()
            self.certs_json = self.certs_report.get_report()

    def ssl_cert_report(self):
        """set the ssl cert payloads by calling the needed methods of the cert_report object"""

        # Return if no vaults to parse
        if not self.certs_json:
            return

        if self.slack_app:
            slack_messages = reports.SlackMessages()
            text = slack_messages.get_ssl_report(self.certs_json, skip_ok=self.args.ssl_include_ok)
            rows = str(text).split("\n")[1:]
            for row in rows:
                if row:
                    self.payloads.append({"text": text})
                    break

        if self.teams_output:
            title = "SSL certificates report -"
            r = self.certs_report.get_report(delete=("code", "expire_age"))
            rows = reports.dict_to_rows(r)

            header = rows.pop(0)
            for i, x in enumerate(header):
                header[i] = str(x).title().replace("_", " ")

            html_table = reports.HTMLTable(header, skip_ok=self.args.ssl_include_ok)
            html_table.init_html_table()
            if not rows:
                return

            for row in rows:
                html_table.add_html_row(*row, styling=self.html_styling_ssl)
            html = html_table.get_table()

            if title and html:
                ms_teams_payload = webhook_payloads.MSTeamsPayload(title, html)
                payload = ms_teams_payload.get_payload()
                self.payloads.append(payload)

    def prepare_and_post(self):
        """prepare the list of payloads and calls the post function to be used

         Call the post_payload function in order to post the payloads or
         the slack_workflow_report function to post to a Slack Workflow if no payloads."""

        # Return if no message handler object
        if not self.msg_handler:
            return

        # Return if no payloads.
        if not self.payloads:
            return

        # Payloads to post.
        # First check if additional info are provided by the ADDITIONAL_INFO env. variable.
        # If so, ensure that it is a list, then to be converted to json
        additional_info = ""
        additional_info_added = False
        if ADDITIONAL_INFO:
            logging.info(f"'ADDITIONAL_INFO': {str(ADDITIONAL_INFO)}")
            if not str(ADDITIONAL_INFO).startswith("["):
                additional_info = [ADDITIONAL_INFO]
            else:
                try:
                    additional_info = json.loads(ADDITIONAL_INFO)
                except:
                    logging.error("'ADDITIONAL_INFO' not valid.")

        # Payloads to be posted to Teams
        # Add additional info (if any) as facts
        if self.teams_output:
            for i, p in enumerate(self.payloads):
                if not isinstance(p, dict):
                    p = json.loads(self.payloads[0])

                sections = p.get("sections")
                if additional_info and sections and not additional_info_added:
                    for section in sections:
                        if "facts" in section:
                            facts = section.get("facts")
                            if isinstance(facts, list):
                                for item in additional_info:
                                    if isinstance(item, dict):
                                        f = item.popitem()
                                        fact = {'name': f[0], 'value': f[1]}
                                    else:
                                        fact = {'name': str(item), 'value': ' '}
                                    facts.append(fact)
                                    additional_info_added = True
                    self.payloads[i] = p

            # Post the payload to Teams
            self.success = post_payloads(self.msg_handler, self.payloads)
            return

        # Payloads to be posted to Slack App
        # Add the additional info (if any) to the summary post
        if additional_info:
            for payload in self.payloads:

                # Get the summary payload (the first one)
                text = payload.get("text")
                md_ending = "```"
                add_ending = False

                if not text or additional_info_added:
                    continue

                # If the additional info does not contain a html url, it can just be added to the current
                # plain text summary block. The ``` ending has to be removed and then re-added after additional info
                # have been added
                if "https://" not in str(additional_info) and "http://" not in str(additional_info):
                    text = text.rstrip(md_ending)
                    add_ending = True

                for item in additional_info:
                    if isinstance(item, dict):
                        f = item.popitem()
                        new_line = f"*{f[0]}:* {f[1]}\n"
                    else:
                        new_line = f"{str(item)}\n"
                    text += f"\n{new_line}"

                    if add_ending:
                        text += md_ending

                # Replace the "old" summary with the new which contains the additional info
                payload['text'] = text
                additional_info_added = True

        # Post all payloads to Slack App Webhook
        self.success = post_payloads(self.msg_handler, self.payloads)

    def get_success(self):
        """returns the success variable"""

        return self.success


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    # The list of key vaults to check passed as command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--alert_threshold", type=int,
                        help="If set then only records that are +/- this value in days till expire/expired "
                             "will be alerted. Records will be alerted as individual Slack messages. "
                             "Summary report and other reports will not be posted.")

    parser.add_argument("-e", "--expire_threshold", type=int,
                        help="If a value (int) is set. The days to the record's Expiration Date must be below "
                             "this threshold in order to be included in the report (Default: not set).")

    parser.add_argument("-a", "--include_all", action='store_true',
                        help="Include all records in output (verbose) if provided.")

    parser.add_argument("-i", "--include_no_expiration", action='store_false',
                        help="Also include records which has no Expiration Date set.")

    parser.add_argument("-l", "--ssl_certs", nargs='+',
                        help="List of ssl certs to check. E.g. kv-dev kv-test")

    parser.add_argument("-R", "--ssl_include_ok", action='store_false',
                        help="If provided all SSL certs will included in the report")

    parser.add_argument("-W", "--ssl_warning_threshold", type=int, default=29,
                        help="The SSL cert expire days warning threshold.")

    parser.add_argument("-C", "--ssl_critical_threshold", type=int, default=14,
                        help="The SSL cert expire days critical threshold.")

    parser.add_argument("-t", "--report_types", nargs='+', default=["kv_report"],
                        help="Kind of report to be posted: kv_report kv_alert cert_report")

    parser.add_argument("-m", "--write_md_report", action='store_true',
                        help="If provided Markdown Key Vault report and a summary will be written.")

    parser.add_argument("-V", "--write_csv_report", action='store_true',
                        help="If provided a full Key Vault report in csv format will be written.")

    parser.add_argument("-T", "--title", type=str, default="Azure Key Vault report",
                        help="The title of the message posted in Slack or MS Teams")

    parser.add_argument("-L", "--slack_split_chars", type=int, default=3300,
                        help="Slack message above this value will be split into multiple post messages.")

    parser.add_argument("-M", "--teams_max_chars", type=int, default=17367,
                        help="The max characters the report can have due to the MS Teams payload size limits")

    parser.add_argument("-w", "--workflow_output_file", type=str, default="output.json",
                        help="The file where the full json report will be written.")

    parser.add_argument("-s", "--silence", action='store_true',
                        help="If provided the workflow will run and log, but no messages to Slack or MS Teams and "
                             "no print to stdout.")

    args = parser.parse_args()

    # Log each argparse argument
    for k, v in sorted(vars(args).items()):
        logging.info(f"Argument '{k}': '{v}'")

    ####################################################################################################################

    # Determines if a webhook is set, and if it is for a Slack App or a Slack Workflow. If not we assume for MS Teams.
    if not WEBHOOK_REPORT:
        logging.warning("'WEBHOOK_REPORT' not provided. Messages will not be posted to the message handler.")

    monitoring = Monitoring(args)
    monitoring.set_webhooks(WEBHOOK_REPORT)
    if monitoring.read_json():
        monitoring.key_vault_report()

    if args.ssl_certs:
        monitoring.ssl_cert()

    monitoring.report_full_json()
    monitoring.write_report_full_json()

    if args.write_csv_report:
        monitoring.write_kv_report_full_csv()

    if args.write_md_report:
        monitoring.write_md_report()

    # If the 'silence' argument is provided, then we are done once the json output file is written
    if args.silence:
        return

    if args.report_types:
        report_types = args.report_types
        if isinstance(args.report_types, str):
            report_types = args.report_types.split()

        # Do the reporting, alerting, ssl certs checks...
        if 'kv_report' in report_types:
            monitoring.kv_report()

        if 'kv_alert' in report_types:
            monitoring.kv_alert()

        if 'cert_report' in report_types:
            monitoring.ssl_cert_report()

        # Prepare and post the payloads
        monitoring.prepare_and_post()

    # If success and 'WEBHOOK_NOTIFY' is provided
    # an additional notify will be posted to the 'WEBHOOK_NOTIFY' webhook
    if monitoring.get_success() and WEBHOOK_NOTIFY:
        logging.info(f"Trigger additional alert about new report message(s)...")
        alert = message_handler.MessageHandler(WEBHOOK_NOTIFY)
        alert.post_payload()

########################################################################################################################


if __name__ == '__main__':
    # The actual report will be posted to the webhook exported in
    # the following environment variable
    WEBHOOK_REPORT = os.getenv("WEBHOOK_REPORT")

    # When all the reports have been posted, an additional POST is performed
    # to the webhook exported in following environment variable:
    WEBHOOK_NOTIFY = os.getenv("WEBHOOK_NOTIFY")

    # Additional info to be included in Summary report.
    ADDITIONAL_INFO = os.getenv("ADDITIONAL_INFO", "")

    # The value of the name key in the full json logfile
    WORKFLOW_OUTPUT_NAME = os.getenv("WORKFLOW_OUTPUT_NAME", "")

    # The value of the github_repo name key in the full json logfile
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY", "")

    # These Azure environment variables will be used in the full json logfile
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")

    main()
