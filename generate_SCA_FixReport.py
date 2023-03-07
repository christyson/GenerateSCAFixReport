import sys
import requests
import argparse
import json
import datetime
from beautifultable import BeautifulTable
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_py import VeracodeAPI as vapi
from veracode_api_py import Workspaces as Workspaces
api_target = "https://analysiscenter.veracode.com/api/5.0/deletebuild.do"
headers = {"User-Agent": "Python HMAC Example"}

def build_report(the_findings, csv=False, no_table=False):
    table = BeautifulTable(maxwidth=100)
    for each_finding in the_findings:
        
        fix_ver = each_finding.get('fix_info', {}).get('fixed_version')
        fix_safe = each_finding.get('fix_info', {}).get('latest_safe_version')
        vtitle = each_finding.get('vulnerability', {}).get('title')
        vcvss3 = each_finding.get('vulnerability', {}).get('cvss3_score')
        direct = each_finding.get('library',{}).get('direct')
        table.rows.append([each_finding['workspace'], each_finding['project_name'], each_finding['library']['id'], each_finding['library']['name'],each_finding['library']['version'],each_finding['issue_status'], direct, fix_ver, fix_safe, vtitle, vcvss3])
           
    table.columns.header = ['Workspace','Project Name','Library ID','Library Name', 'Version','Issue Status', 'Direct', 'Fixed Version', 'Latest Safe Version','Vulnerability', 'CVSS 3 Score']
    table.columns.header.alignment = BeautifulTable.ALIGN_CENTER
    table.columns.alignment['Workspace'] = BeautifulTable.ALIGN_LEFT
    table.columns.alignment['Project Name'] = BeautifulTable.ALIGN_LEFT
    table.columns.alignment['Library ID'] = BeautifulTable.ALIGN_LEFT
    table.columns.alignment['Library Name'] = BeautifulTable.ALIGN_LEFT
    table.columns.alignment['Version'] = BeautifulTable.ALIGN_LEFT
    table.columns.alignment['Issue Status'] = BeautifulTable.ALIGN_LEFT
    table.columns.alignment['Direct'] = BeautifulTable.ALIGN_LEFT
    table.columns.alignment['Fixed Version'] = BeautifulTable.ALIGN_LEFT
    table.columns.alignment['Latest Safe Version'] = BeautifulTable.ALIGN_LEFT
    table.columns.alignment['Vulnerability'] = BeautifulTable.ALIGN_LEFT
    table.columns.alignment['CVSS 3 Score'] = BeautifulTable.ALIGN_LEFT
    table.set_style(BeautifulTable.STYLE_COMPACT)
    print()

    if not no_table:
       print(table)

    #format findings list

    if csv:
        the_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = 'SCA_Fix-{}.csv'.format(the_time)

        table.to_csv(file_name = filename)

def main():

    parser = argparse.ArgumentParser(
        description='This script builds a csv report with SCA findings and their fix version and latest safe version.')
    parser.add_argument('-w', '--workspace_name', help='Works Space name to generate Issues for or by default it will do the whole organization',required=False)
    parser.add_argument('-c', '--csv', action='store_true', help='Set to save the output as a CSV file.', required=False)
    parser.add_argument('-nt', '--no_table', action='store_true', help='If selected a table will be output to the screen',required=False)

    args = parser.parse_args()
    type = args.workspace_name
    if (type is None):
       print("Generating list for whole organization")
       workspace_list = vapi().get_workspaces()
    else:
       print("Generating list for: "+str(args.workspace_name))
       workspace_list = vapi().get_workspace_by_name(args.workspace_name)
    #workspace_list = vapi().get_workspace_by_name(args.workspace_name)
    #print("Workspaces are: "+str(workspace_list))
    csv = args.csv
    no_table = args.no_table
    the_issues=[]
    for workspace in workspace_list:
        workspace_guid = workspace.get("id")
        workspace_name = workspace.get('name')
        #print("Workspace id is: "+str(workspace_guid))
        #print("Workspace Name is: "+str(workspace_name))
        issues = vapi().get_issues(workspace_guid)
        #print("Issues list: "+str(issues))
        for issue in issues:
            issue_id = issue.get("id")
            issue_type = issue.get("issue_type")
            if issue_type == "vulnerability":
               #print("Issue is: "+str(issue))
               #rint("Issue id is: "+str(issue_id))
               #issue_details = vapi().get_vulnerability(issue_id)
               issue_details = Workspaces().get_issue(issue_id)
               issue_details['workspace']=workspace_name
               #vtitle = issue_details.get('vulnerability', {}).get('title')
               #if vtitle == None:
               #   print("Issue details are: "+str(issue_details))
               #   print("Issue is: "+str(issue))
               the_issues.append(issue_details)
            elif issue_type == "library":
               #print ("Library issue")
               pass
            elif issue_type == "license":
               #print ("License issue")
               pass
            else:
               #print ("Unknow issue type: "+issue_type)
               pass
        # construct report
    build_report(the_issues, csv, no_table)
    exit(0)
  
if __name__ == '__main__':
    main()
