#
# Alexandria3k Crossref bibliographic metadata processing
# Copyright (C) 2022  Diomidis Spinellis
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""Populate journal, funder, OA data tables"""

import codecs
import csv
import re
import sqlite3
from urllib.request import urlopen

from virtual_db import ColumnMeta, TableMeta

RE_URL = re.compile(r"\w+://")


def data_source(source):
    """Given a file path or a URL return a readable source for its contents"""
    if RE_URL.match(source):
        return urlopen(source)
    else:
        return open(source, "rb")


def record_source(source):
    """Given a file path or a URL return a record source for its contents"""
    with data_source(source) as raw_input:
        reader = csv.reader(codecs.iterdecode(raw_input, "utf-8"))
        next(reader, None)  # Skip header row
        for i in reader:
            yield i


# Crossref journal data http://ftp.crossref.org/titlelist/titleFile.csv
journals_table = TableMeta(
    "journal_names",
    columns=[
        ColumnMeta("title"),
        ColumnMeta("id"),
        ColumnMeta("publisher"),
        ColumnMeta("issn_print"),
        ColumnMeta("issn_eprint"),
        ColumnMeta("issns_additional"),
        ColumnMeta("doi"),
        ColumnMeta("volume_info"),
    ],
    post_population_command="""UPDATE journal_names
        SET issn_print=REPLACE(issn_print, "-", ""),
          issn_eprint=REPLACE(issn_eprint, "-", "")""",
)

# Crossref funder data https://doi.crossref.org/funderNames?mode=list
# https://www.crossref.org/services/funder-registry/
funders_table = TableMeta(
    "funder_names",
    columns=[
        ColumnMeta("url"),
        ColumnMeta("name"),
        ColumnMeta("replaced"),
    ],
)

# DOAJ open access journal metadata data
# https://doaj.org/csv
open_access_table = TableMeta(
    "open_access_journals",
    columns=[
        ColumnMeta("name", description="Journal title"),
        ColumnMeta("url", description="Journal URL"),
        ColumnMeta("doaj_ur", description="URL in DOAJ"),
        ColumnMeta(
            "oaj_start",
            description="When did the journal start to publish all content using an open license?",
        ),
        ColumnMeta("alternative_name", description="Alternative title"),
        ColumnMeta("issn_print", description="Journal ISSN (print version)"),
        ColumnMeta(
            "issn_eprint", description="Journal EISSN (online version)"
        ),
        ColumnMeta("keywords", description="Keywords"),
        ColumnMeta(
            "languages",
            description="Languages in which the journal accepts manuscripts",
        ),
        ColumnMeta("publisher", description="Publisher"),
        ColumnMeta("pubisher_country", description="Country of publisher"),
        ColumnMeta("society", description="Society or institution"),
        ColumnMeta(
            "society_country", description="Country of society or institution"
        ),
        ColumnMeta("license", description="Journal license"),
        ColumnMeta("license_attributes", description="License attributes"),
        ColumnMeta("license_terms_url", description="URL for license terms"),
        ColumnMeta(
            "license_embedded",
            description="Machine-readable CC licensing information embedded or displayed in articles",
        ),
        ColumnMeta(
            "example_license_embedded_url",
            description="URL to an example page with embedded licensing information",
        ),
        ColumnMeta(
            "author_copyright",
            description="Author holds copyright without restrictions",
        ),
        ColumnMeta(
            "copyright_info_url", description="Copyright information URL"
        ),
        ColumnMeta("review_process", description="Review process"),
        ColumnMeta(
            "review_process_url", description="Review process information URL"
        ),
        ColumnMeta(
            "plagiarism_screening",
            description="Journal plagiarism screening policy",
        ),
        ColumnMeta(
            "plagiarism_info_url", description="Plagiarism information URL"
        ),
        ColumnMeta(
            "aims_scope_url", description="URL for journal's aims & scope"
        ),
        ColumnMeta(
            "board_url", description="URL for the Editorial Board page"
        ),
        ColumnMeta(
            "author_instructions_url",
            description="URL for journal's instructions for authors",
        ),
        ColumnMeta(
            "sub_pub_weeks",
            description="Average number of weeks between article submission and publication",
        ),
        ColumnMeta("apc", description="APC"),
        ColumnMeta("apc_info_url", description="APC information URL"),
        ColumnMeta("apc_amount", description="APC amount"),
        ColumnMeta(
            "apc_waiver",
            description="Journal waiver policy (for developing country authors etc)",
        ),
        ColumnMeta(
            "apc_waiver_info_url", description="Waiver policy information URL"
        ),
        ColumnMeta("other_fees", description="Has other fees"),
        ColumnMeta(
            "other_fees_info_url", description="Other fees information URL"
        ),
        ColumnMeta(
            "preservation_services", description="Preservation Services"
        ),
        ColumnMeta(
            "preservation_national_library",
            description="Preservation Service: national library",
        ),
        ColumnMeta(
            "preservation_info_url", description="Preservation information URL"
        ),
        ColumnMeta(
            "deposit_policy_directory", description="Deposit policy directory"
        ),
        ColumnMeta(
            "deposit_policy_directory_url",
            description="URL for deposit policy",
        ),
        ColumnMeta(
            "persistent_article_identifiers",
            description="Persistent article identifiers",
        ),
        ColumnMeta(
            "orcid_in_metadata", description="Article metadata includes ORCIDs"
        ),
        ColumnMeta(
            "i4oc_compliance",
            description="Journal complies with I4OC standards for open citations",
        ),
        ColumnMeta(
            "doaj_oa_compliance",
            description="Does the journal comply to DOAJ's definition of open access?",
        ),
        ColumnMeta(
            "oa_statement_url",
            description="URL for journal's Open Access statement",
        ),
        ColumnMeta("continues", description="Continues"),
        ColumnMeta("continued_by", description="Continued By"),
        ColumnMeta("lcc_codes", description="LCC Codes"),
        ColumnMeta("subjects", description="Subjects"),
        ColumnMeta("doaj_Seal", description="DOAJ Seal"),
        ColumnMeta("added_on", description="Added on Date"),
        ColumnMeta("last_updated", description="Last updated Date"),
        ColumnMeta(
            "article_records_number", description="Number of Article Records"
        ),
        ColumnMeta(
            "most_recent_addition", description="Most Recent Article Added"
        ),
    ],
)


def load_csv_data(database_path, table_meta, source):
    """Populate specified table of database with data from source"""
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute(f"DROP TABLE IF EXISTS {table_meta.get_name()}")
    cur.execute(table_meta.table_schema())
    cur.executemany(table_meta.insert_statement(), record_source(source))
    post_population_command = table_meta.get_post_population_command()
    if post_population_command:
        cur.execute(post_population_command)
    con.commit()
    con.close()