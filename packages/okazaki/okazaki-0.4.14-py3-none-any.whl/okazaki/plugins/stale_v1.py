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
from datetime import datetime, timedelta
from dateutil.tz import tzutc


class StaleV1Plugin:
    def __init__(self, app, repo_name, stale_rules, logger):
        self._app = app
        self._issue = Issue(app)
        self._repo_name = repo_name
        self._stale_rules = stale_rules
        self._logger = Logger().get_logger(__name__) if logger is None else logger

    def run(self):
        self._logger.info(f"Running Stale V1 Plugin for repository: {self._repo_name}")

        if not self._stale_rules.enabled:
            self._logger.info("Stale rules are not enabled. Skipping.")
            return

        self._process_issues()
        self._process_pull_requests()

    def _process_issues(self):
        issues = self._issue.get_issues(self._repo_name, state="open")
        for issue in issues:
            # Process if not a pull request
            if issue.pull_request is None:
                self._process_item(issue, self._stale_rules.issues)

    def _process_pull_requests(self):
        pulls = self._issue.get_issues(self._repo_name, state="open")
        for pull in pulls:
            # Process if it is a pull request
            if pull.pull_request is not None:
                self._process_item(pull, self._stale_rules.pulls)

    def _process_item(self, item, rules):
        if self._is_exempt(item):
            return

        last_updated = item.updated_at
        now = datetime.now(tzutc())

        if self._is_stale(item, last_updated, now, rules):
            self._mark_as_stale(item, rules)
        elif self._should_close(item, last_updated, now, rules):
            self._close_item(item, rules)

    def _is_exempt(self, item):
        return any(
            label.name in self._stale_rules.exemptLabels for label in item.labels
        )

    def _is_stale(self, item, last_updated, now, rules):
        return (now - last_updated).days >= rules[
            "daysUntilStale"
        ] and not self._has_stale_label(item, rules)

    def _should_close(self, item, last_updated, now, rules):
        return (now - last_updated).days >= (
            rules["daysUntilStale"] + rules["daysUntilClose"]
        ) and self._has_stale_label(item, rules)

    def _has_stale_label(self, item, rules):
        return any(label.name == rules["staleLabel"] for label in item.labels)

    def _mark_as_stale(self, item, rules):
        self._logger.info(f"Marking item #{item.number} as stale")
        self._issue.add_labels(self._repo_name, item.number, [rules["staleLabel"]])
        self._issue.add_comment(self._repo_name, item.number, rules["markComment"])

    def _close_item(self, item, rules):
        self._logger.info(f"Closing stale item #{item.number}")
        self._issue.close_issue(self._repo_name, item.number)
        self._issue.add_comment(self._repo_name, item.number, rules["closeComment"])
