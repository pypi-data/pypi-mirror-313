# MIT License
#
# Copyright (c) 2022 Clivern
#
# This software is licensed under the MIT License. The full text of the license
# is provided below.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from okazaki.api import Issue
from okazaki.util import Logger


class AutoTriageV1Plugin:
    """Auto Triage Plugin V1"""

    def __init__(self, app, repo_name, plugin_rules, logger):
        self._app = app
        self._issue = Issue(app)
        self._repo_name = repo_name
        self._plugin_rules = plugin_rules
        self._logger = Logger().get_logger(__name__) if logger is None else logger

    def run(self):
        issues = self._issue.get_issues(self._repo_name, "open")

        for issue in issues:
            issue_title = issue.title.lower()
            issue_body = issue.body.lower()
            issue_number = issue.number
            issue_labels = [label.name for label in issue.labels]

            # Skip if the issue has already been triaged
            if self._plugin_rules.triagedLabel in issue_labels:
                continue

            labels_to_add = []

            for rule in self._plugin_rules.rules:
                label = rule.label
                terms = rule.terms

                if any(
                    term.lower() in issue_title or term.lower() in issue_body
                    for term in terms
                ):
                    labels_to_add.append(label)

            if labels_to_add:
                labels_to_add.append(self._plugin_rules.triagedLabel)

                try:
                    self._issue.add_labels(self._repo_name, issue_number, labels_to_add)
                    self._logger.info(
                        f"Added labels {labels_to_add} to issue #{issue_number} in repository {self._repo_name}"
                    )
                except Exception as e:
                    self._logger.error(
                        f"Failed to add labels {labels_to_add} to issue #{issue_number} in repository {self._repo_name}: {str(e)}"
                    )

        return True
