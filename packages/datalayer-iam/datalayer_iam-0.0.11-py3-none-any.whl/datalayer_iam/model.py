# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer IAM Model classes."""

class DatalayerUrn():
    """
    Datalayer Uniform Resource Name (URN)

    @see https://en.wikipedia.org/wiki/Uniform_Resource_Name
    @see https://learn.microsoft.com/en-us/linkedin/shared/api-guide/concepts/urns
    @see https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html

    urn:partition:service:region:account:type:uid
    urn:partition:service:region:account:type:uid/path/subpath

    Examples:
    - Account should be the uid.
    - We are using in the examples some names to make it easier to read.

    IAM Account
    - urn:dla:iam:::user:eric
    - urn:dla:iam:::organization:datalayer
    - urn:dla:iam:::team:developers

    IAM Providers
    - urn:dla:iam:ext::github:xyz

    Objects
    - urn:dla:spacer:::space:space-1
    - urn:dla:spacer:::notebook:data-analysis/data-analysis.ipynb
    - urn:dla:spacer:::cell:a-simple-cell
    - urn:dla:spacer:us-east-1::dataset:cities/cities.csv
    - urn:dla:edu:::course:course-1
    - urn:dla:edu:::lesson:advanced-python/advanced-python.ipynb
    - urn:dla:edu:::exercise:loop-with-python
    - urn:dla:library:::notebook:notebook-1
    - urn:dla:app:::panel:new-york-taxis

    Relations
    - urn:dla:iam::run:relation:CourseInstructor/python-advanced
    - urn:dla:iam::run:relation:OrganizationMember
    - urn:dla:iam::run:relation:ReadCourseNotebook/python-advanced
    - urn:dla:iam::run:relation:SpaceReader/simple-analysis
    - urn:dla:iam::run:relation:TeamMember/developers
    """

    partition: str
    service: str
    region: str
    account: str
    type: str
    uid: str
    path: str

    def __init__(self, service, region, account, type, uid, path = "", partition = "dla"):
        self.partition = partition
        self.service = service
        self.region = region
        self.account = account
        self.type = type
        self.uid = uid
        self.path = path

    def __str__(self):
        return f"urn:{self.partition}:{self.service}:{self.region}:{self.account}:{self.type}:{self.uid}{self.path}"

    def to_string(self):
        return self.__str__()

    def to_solr(self):
        return {
            "partition_s": self.partition,
            "service_s": self.service,
            "region_s": self.region,
            "account_s": self.account,
            "type_s": self.type,
            "uid_s": self.uid,
            "path_s": self.path,
        }
