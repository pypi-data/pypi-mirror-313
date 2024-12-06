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

from okazaki.api import Client
from okazaki.api import App
from okazaki.config import RemoteConfigReader
from okazaki.config import LocalConfigReader
from okazaki.config import ConfigParser


# -------------------------
# app_id = 18984
# installation_id = 57652995
# private_key = (
#     "/Users/ahmetwal/space/personal/Ropen/storage/secrets/github_app_private.key"
# )

# client = Client()

# result = client.fetch_access_token(private_key, app_id, installation_id)

# print(result)

# app = App(app_id, private_key, installation_id, result["permissions"])
# app.init()

# rc = RemoteConfigReader(app, "clivern/abc", ".github/workflows/release.yml")

# print(rc.get_configs())
# -------------------------


lc = LocalConfigReader("/Users/ahmetwal/space/personal/Okazaki/.ropen.yml")
print(lc.get_configs())

cp = ConfigParser(lc.get_configs()["configs"])
print(cp.parse())
