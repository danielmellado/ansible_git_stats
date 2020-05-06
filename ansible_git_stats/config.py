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


from oslo_config import cfg
from oslo_log import log as logging

from ansible_git_stats._i18n import _

LOG = logging.getLogger(__name__)

ansible_git_stats_opts = [
    cfg.StrOpt('category',
               help=_('Category to search to (issue/pull_request)'),
               default='issue'),
    cfg.StrOpt('repo',
               help=_('repository to use.'),
               default='ansible-collections/junipernetworks.junos'),
    cfg.StrOpt('gh_token',
               help=_('github token to use.'),
               secret=True,
               required=True),
    cfg.StrOpt('log_file_path',
               help=_('Log file to use'),
               default='/tmp/ansible_git_stats.log')
]

CONF = cfg.CONF
CONF.register_cli_opts(ansible_git_stats_opts)

logging.register_options(CONF)


def init(args, **kwargs):
    CONF(args=args, project='ansible_git_stats', **kwargs)


def setup_logging():
    logging.setup(CONF, 'ansible_git_stats')
    logging.set_defaults(default_log_levels=logging.get_default_log_levels())
    LOG.debug("Logging has been set up")
