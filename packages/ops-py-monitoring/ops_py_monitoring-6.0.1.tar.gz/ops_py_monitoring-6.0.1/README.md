# ops-py-monitoring  
  
## Description  
  
- Uses the [ops-py-azure-key-vault-report](https://pypi.org/project/ops-py-azure-key-vault-report) tool to generate
  - Azure Key Vault reports 
  - Azure Key Vault alerts on individual records 

- Uses the [ops-py-cert-report](https://github.com/equinor/ops-py-cert-report) tool to generate
  - SSL certificate reports 
     
### Azure Key Vault reports
May be posted to a *Slack App* webhook, *Slack Workflow* webhook, or an *MS Teams* webhook.  
  
The output is formatted as a *Slack Code Block* when posted Slack. The content is output as a two plaintext Markdown tables:     
the Summary and the Report.    
  
Long reports will be split into multiple parts. Part number will then be added to each part.     
  
When posted to a MS Teams payload the Summary is formatted as *Facts*, followed by the Report as an HTML Table.  

The az keyvault command outputs must be stored in separate files with a `.json` ending. The files must be placed in a folder named `/tmp/az_json`, e.g.:   
`/tmp/az_json/my-kv_secret.json`
  
### Azure Key Vault Slack alerts     
Each alert message is formatted as Slack Markdown.  
  
### Azure Key Vault MS Teams alerts  
Each alert message is formatted as `AdaptiveCard` with `TextBlock`s.  
 
### SSL certificate reports
Posted to a *Slack App* webhook.
 
  
## Installation  
`pip install ops-py-monitoring`  
  
## Usage  
  
### Environment variables  
Export the webhook url(s) as environment variables:  
  
- `WEBHOOK_REPORT` This is where the reports(s) or alerts will be posted. It is automatically detected if the webook is of type:  
  - *Slack App*    
 When the webhook contains `slack.com/services`.  
  
  - *Slack Workflow*    
 When the webhook contains `slack.com`, but not the `slack.com/services` part.  
  
  - *MS Teams*    
 When the webhook **does not** contain `slack.com`.  
  
  *Example:* `export WEBHOOK_REPORT="https://hooks.slack.com/workflows/T02XYZ..."`  
  
- `WEBHOOK_NOTIFY`  
If set, then when the result has been posted to the `WEBHOOK_REPORT`webhook, an additional empty POST is performed to the value of this webhook.  
  
**NOTE:** The actual post requests are handled by the [ops-py-message-handler](https://pypi.org/project/ops-py-message-handler).  
  
---  
  
### Arguments  
  
`-l`, `--ssl_certs` *STRING (space separated)* The list of ssl certs to check
*Example:*  `-l example.com equinor.com`  

`-W`, `--ssl_warning_threshold` *INT - Default:* `29`  The SSL cert expire days warning threshold.  

`-C`, `--ssl_critical_threshold` *INT - Default:* `14`  The SSL cert expire days critical threshold.  

`-R` `--ssl_include_ok` If provided all SSL certs will be included in the report.

`-t` `--report_types` *Default:* `kv_report` Kind of report to be posted.
*Example:* `-t kv_report kv_alert cert_report`

`-c`, `--alert_threshold` *INT - Default: not set* If set, then only the records that are +/- this value in days till expire/expired will be alerted on, as individual messages.     
*Example:* `--alert_threshold 7` This will alert on records which will expire within the next 7 days OR the record that has expired, but only for less than 7 days ago.    
If specified, the *summary* and other *reports* will not be posted. Only the alert messages about the records which are caught by this `alert_threshold`filter will be posted.  
  
`-e`, `--expire_threshold` *INT - Default: not set* If this argument is provided, the days to the record's *Expiration Date* must be below this threshold in order to be included in the report.     
*Example:* `--expire_threshold 60` This will include the record in the report only if the record will expire within the next 60 days.     
  
`-i`, `--include_no_expiration` *Default: not set* If this argument is provided, the report will also include the records which has no *Expiration Date* set.  
The default behavior is simply to ignore records which do not have a `Expiration Date` set.     
  
`-a`, `--include_all` *Default: not set* If this argument is provided, the report will include all the records (verbose) for the specified Record Types.  
Records which have been *disabled* will also be included.     
  
`-T`, `--title` *Default:* `Azure Key Vault report` The title of the message posted in Slack or MS Teams.     
  
`-L`, `--slack_split_chars` *INT - Default:* `3500` If the Slack message is above this value it will be split into multiple posts.  
Each post will then include a maximum characters specified by this value.     
  
`-M`, `--teams_max_chars` *INT - Default:* `17367` The max characters the report can have due to the MS Teams payload size limits.     
**NOTE:** If the message is above this threshold then only the facts (summary) will be posted to MS Teams.  
The HTML table will in this case not be included.     
  
`-w`, `--workflow_output_file` *STRING - Default:* `output.json` The file where a full json report will be written.     
  
`-s`, `--silence` *Default: not set* If provided the workflow will run, log and write to the `workflow_output_file` and stdout, but no messages to Slack or MS Teams will be posted.     

`-m`, `--write_md_report` *Default: not set* If provided, plain text markdown files will be written.

`-V`, `--write_csv_report` *Default: not set* If provided, plain text comma separated csv files will be written.


  
## Examples  
  
**Generate a Key Vault report and summary of all records for specified Key Vaults**   
Example: `python3 -m monitoring.monitoring --ssl_certs example.com google.com --report_types kv_report cert_report --write_md_report --write_csv_report --include_all`  
  
This will include all the Key Vault records found in the output files in the `/tmp/az_json` directory, even the records which are disabled and the records which has no Expiration Date set.  
The result will be a *summary report* and a *full report*, which are posted to the webhook exported in `WEBHOOK_REPORT`  
The status of the two provided ssl certificates will be generated. CSV and Markdown report text files will also be written.

To only print the result to stdout and not post to the webhook, append the `-S`argument  
  
**To only include the records which will expire within the next 60 days**     
Example: `python3 -m monitoring.monitoring --ssl_certs example.com google.com --report_types kv_report cert_report --write_md_report --write_csv_report --expire_threshold 60`  

The reports will then only include records will expire within the next 60 days and records which have already expired.    
  
*The summary* will contain info about *every record parsed*, even if the record is not included to be output in the report.     
**NOTE:** If no records are included in the report (none expired and none expiring within the threshold), the summary will still be posted.    
  
**For specified Key Vaults, alert only (no report) if any records is about to expire within the next 14 days or if any record has expired within the last 14 days**  
`python3 -m monitoring.monitoring --report_types kv_alert --alert_threshold 14`  
  
**NOTE:** Each record will be alerted on in separate messages.     
**NOTE:** E.g. if a record then has expired for 15 days or more, it will not be alerted on.    
  
**Log all output** A summary and a full report is always written to file. This may then be used to post to an Monitoring service API etc., e.g.:     
```  
curl --request POST \    
  --header 'Content-Type: application/json' \    
  --header 'X-Api-Key: MY-SUPER-SECRET-KEY' \    
  --data @output.json \    
  https://my-superb-api.com  
```
