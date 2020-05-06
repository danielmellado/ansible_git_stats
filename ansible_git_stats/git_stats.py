# Copyright 2020 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re
import sys

from oslo_log import log as logging
from perceval.backends.core.github import GitHub
from prettytable import PrettyTable

from ansible_git_stats import config

CONF = config.CONF
LOG = logging.getLogger(__name__)


class GitHubParser():
    """Get GitHub Issues for Ansible Networking Collections

    This class relies on grimoirelabs' perceval to handle issues and data from
    Ansible Networking repositories.
    """

    def __init__(self):
        self.table = PrettyTable()
        self.table.field_names = ["Ansible Repo",
                                  "Category",
                                  "State",
                                  "Url",
                                  "ID",
                                  "Title",
                                  "Assignee"]
        self.table_data = []

    def get_github_data(self):
        owner, repository = CONF.repo.split('/')
        repo = GitHub(owner=owner, repository=repository,
                      api_token=CONF.gh_token)
        data = repo.fetch('issue')
        self.check_if_open(data)
        return self.table

    def check_if_open(self, data):
        for item in data:
            if item['data']['state'] != 'closed':
                self.parse_data(item)
        for row in self.table_data:
            self.table.add_row(row)
        self.table.sortby = 'Category'
        self.table.reversesort = True

    def parse_data(self, data):
        assignee = data['data'].get('assignee')
        if assignee:
            assignee_login = assignee['login']
        else:
            assignee_login = "TBD"

        number_id = data['data']['number']
        category = data['category']

        if re.findall('/pull/', data['data']['html_url']):
            category = 'pull_request'

        table_row = [CONF.repo,
                     category,
                     data['data']['state'],
                     data['data']['html_url'],
                     number_id,
                     data['data']['title'],
                     assignee_login]

        self.table_data.append(table_row)


def main():
    parser = GitHubParser()
    config.init(sys.argv[1:])
    config.setup_logging()
    print(parser.get_github_data())


if __name__ == "__main__":
    main()
