from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar, Literal, Self


class AttributeCategories(StrEnum):
    PAYLOAD_DELIVERY = "Payload delivery"
    ARTIFACTS_DROPPED = "Artifacts dropped"
    PAYLOAD_INSTALLATION = "Payload installation"
    EXTERNAL_ANALYSIS = "External analysis"
    PERSISTENCE_MECHANISM = "Persistence mechanism"
    NETWORK_ACTIVITY = "Network activity"
    ATTRIBUTION = "Attribution"
    SOCIAL_NETWORK = "Social network"
    PERSON = "Person"
    OTHER = "Other"
    INTERNAL_REFERENCE = "Internal reference"
    ANTIVIRUS_DETECTION = "Antivirus detection"
    SUPPORT_TOOL = "Support Tool"
    TARGETING_DATA = "Targeting data"
    PAYLOAD_TYPE = "Payload type"
    FINANCIAL_FRAUD = "Financial fraud"


@dataclass
class AttributeType:
    all_attributes: ClassVar[list] = []

    dbkey: str
    safe_clsname: str
    default_category: AttributeCategories
    categories: frozenset
    to_ids: bool = False

    def __post_init__(self: Self) -> None:
        self.all_attributes.append(self)


AttributeType(
    dbkey="md5",
    safe_clsname="Md5",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)
AttributeType(
    dbkey="sha1",
    safe_clsname="Sha1",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)
AttributeType(
    dbkey="sha256",
    safe_clsname="Sha256",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)

AttributeType(
    dbkey="filename",
    safe_clsname="Filename",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="pdb",
    safe_clsname="Pdb",
    default_category=AttributeCategories.ARTIFACTS_DROPPED,
    categories=frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    to_ids=False,
)


AttributeType(
    dbkey="filename|sha1",
    safe_clsname="FilenameSha1",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|sha256",
    safe_clsname="FilenameSha256",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="ip-src",
    safe_clsname="IpSrc",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="ip-dst",
    safe_clsname="IpDst",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="hostname",
    safe_clsname="Hostname",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="domain",
    safe_clsname="Domain",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="domain|ip",
    safe_clsname="DomainIp",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.EXTERNAL_ANALYSIS, AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=True,
)


AttributeType(
    dbkey="email",
    safe_clsname="Email",
    default_category=AttributeCategories.SOCIAL_NETWORK,
    categories=frozenset(
        {
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PERSON,
            AttributeCategories.SOCIAL_NETWORK,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="email-src",
    safe_clsname="EmailSrc",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {AttributeCategories.SOCIAL_NETWORK, AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.NETWORK_ACTIVITY}
    ),
    to_ids=True,
)


AttributeType(
    dbkey="email-dst",
    safe_clsname="EmailDst",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {AttributeCategories.SOCIAL_NETWORK, AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.NETWORK_ACTIVITY}
    ),
    to_ids=True,
)


AttributeType(
    dbkey="email-subject",
    safe_clsname="EmailSubject",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=False,
)


AttributeType(
    dbkey="email-attachment",
    safe_clsname="EmailAttachment",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=True,
)


AttributeType(
    dbkey="email-body",
    safe_clsname="EmailBody",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=False,
)


AttributeType(
    dbkey="eppn",
    safe_clsname="Eppn",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.SOCIAL_NETWORK, AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=True,
)


AttributeType(
    dbkey="float",
    safe_clsname="Float",
    default_category=AttributeCategories.OTHER,
    categories=frozenset({AttributeCategories.OTHER}),
    to_ids=False,
)


AttributeType(
    dbkey="git-commit-id",
    safe_clsname="GitCommitId",
    default_category=AttributeCategories.INTERNAL_REFERENCE,
    categories=frozenset({AttributeCategories.INTERNAL_REFERENCE}),
    to_ids=False,
)


AttributeType(
    dbkey="url",
    safe_clsname="Url",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="http-method",
    safe_clsname="HttpMethod",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=False,
)


AttributeType(
    dbkey="user-agent",
    safe_clsname="UserAgent",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="ja3-fingerprint-md5",
    safe_clsname="Ja3FingerprintMd5",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="jarm-fingerprint",
    safe_clsname="JarmFingerprint",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="favicon-mmh3",
    safe_clsname="FaviconMmh3",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=True,
)


AttributeType(
    dbkey="hassh-md5",
    safe_clsname="HasshMd5",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="hasshserver-md5",
    safe_clsname="HasshserverMd5",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="regkey",
    safe_clsname="Regkey",
    default_category=AttributeCategories.PERSISTENCE_MECHANISM,
    categories=frozenset(
        {
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.EXTERNAL_ANALYSIS,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="regkey|value",
    safe_clsname="RegkeyValue",
    default_category=AttributeCategories.PERSISTENCE_MECHANISM,
    categories=frozenset(
        {
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.EXTERNAL_ANALYSIS,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="AS",
    safe_clsname="As",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="bro",
    safe_clsname="Bro",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.EXTERNAL_ANALYSIS, AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=True,
)


AttributeType(
    dbkey="zeek",
    safe_clsname="Zeek",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.EXTERNAL_ANALYSIS, AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=True,
)


AttributeType(
    dbkey="community-id",
    safe_clsname="CommunityId",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.EXTERNAL_ANALYSIS, AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=True,
)


AttributeType(
    dbkey="pattern-in-file",
    safe_clsname="PatternInFile",
    default_category=AttributeCategories.PAYLOAD_INSTALLATION,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="aba-rtn",
    safe_clsname="AbaRtn",
    default_category=AttributeCategories.FINANCIAL_FRAUD,
    categories=frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    to_ids=True,
)


AttributeType(
    dbkey="anonymised",
    safe_clsname="Anonymised",
    default_category=AttributeCategories.OTHER,
    categories=frozenset(
        {
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.PAYLOAD_TYPE,
            AttributeCategories.SOCIAL_NETWORK,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.FINANCIAL_FRAUD,
            AttributeCategories.TARGETING_DATA,
            AttributeCategories.INTERNAL_REFERENCE,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.SUPPORT_TOOL,
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.OTHER,
            AttributeCategories.PERSON,
            AttributeCategories.ARTIFACTS_DROPPED,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="attachment",
    safe_clsname="Attachment",
    default_category=AttributeCategories.EXTERNAL_ANALYSIS,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.SUPPORT_TOOL,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="authentihash",
    safe_clsname="Authentihash",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="azure-application-id",
    safe_clsname="AzureApplicationId",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_INSTALLATION, AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=True,
)


AttributeType(
    dbkey="bank-account-nr",
    safe_clsname="BankAccountNr",
    default_category=AttributeCategories.FINANCIAL_FRAUD,
    categories=frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    to_ids=True,
)


AttributeType(
    dbkey="bic",
    safe_clsname="Bic",
    default_category=AttributeCategories.FINANCIAL_FRAUD,
    categories=frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    to_ids=True,
)


AttributeType(
    dbkey="bin",
    safe_clsname="Bin",
    default_category=AttributeCategories.FINANCIAL_FRAUD,
    categories=frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    to_ids=True,
)


AttributeType(
    dbkey="boolean",
    safe_clsname="Boolean",
    default_category=AttributeCategories.OTHER,
    categories=frozenset({AttributeCategories.OTHER}),
    to_ids=False,
)


AttributeType(
    dbkey="btc",
    safe_clsname="Btc",
    default_category=AttributeCategories.FINANCIAL_FRAUD,
    categories=frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    to_ids=True,
)


AttributeType(
    dbkey="campaign-id",
    safe_clsname="CampaignId",
    default_category=AttributeCategories.ATTRIBUTION,
    categories=frozenset({AttributeCategories.ATTRIBUTION}),
    to_ids=False,
)


AttributeType(
    dbkey="campaign-name",
    safe_clsname="CampaignName",
    default_category=AttributeCategories.ATTRIBUTION,
    categories=frozenset({AttributeCategories.ATTRIBUTION}),
    to_ids=False,
)


AttributeType(
    dbkey="cc-number",
    safe_clsname="CcNumber",
    default_category=AttributeCategories.FINANCIAL_FRAUD,
    categories=frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    to_ids=True,
)


AttributeType(
    dbkey="cdhash",
    safe_clsname="Cdhash",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="chrome-extension-id",
    safe_clsname="ChromeExtensionId",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_INSTALLATION, AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=True,
)


AttributeType(
    dbkey="comment",
    safe_clsname="Comment",
    default_category=AttributeCategories.OTHER,
    categories=frozenset(
        {
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.PAYLOAD_TYPE,
            AttributeCategories.SOCIAL_NETWORK,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.FINANCIAL_FRAUD,
            AttributeCategories.TARGETING_DATA,
            AttributeCategories.INTERNAL_REFERENCE,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.SUPPORT_TOOL,
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.OTHER,
            AttributeCategories.PERSON,
            AttributeCategories.ARTIFACTS_DROPPED,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="cookie",
    safe_clsname="Cookie",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.ARTIFACTS_DROPPED, AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=False,
)


AttributeType(
    dbkey="cortex",
    safe_clsname="Cortex",
    default_category=AttributeCategories.EXTERNAL_ANALYSIS,
    categories=frozenset({AttributeCategories.EXTERNAL_ANALYSIS}),
    to_ids=False,
)


AttributeType(
    dbkey="counter",
    safe_clsname="Counter",
    default_category=AttributeCategories.OTHER,
    categories=frozenset({AttributeCategories.OTHER}),
    to_ids=False,
)


AttributeType(
    dbkey="country-of-residence",
    safe_clsname="CountryOfResidence",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="cpe",
    safe_clsname="Cpe",
    default_category=AttributeCategories.EXTERNAL_ANALYSIS,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.OTHER,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="dash",
    safe_clsname="Dash",
    default_category=AttributeCategories.FINANCIAL_FRAUD,
    categories=frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    to_ids=True,
)


AttributeType(
    dbkey="datetime",
    safe_clsname="Datetime",
    default_category=AttributeCategories.OTHER,
    categories=frozenset({AttributeCategories.OTHER}),
    to_ids=False,
)


AttributeType(
    dbkey="date-of-birth",
    safe_clsname="DateOfBirth",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="dkim",
    safe_clsname="Dkim",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=False,
)


AttributeType(
    dbkey="dkim-signature",
    safe_clsname="DkimSignature",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=False,
)


AttributeType(
    dbkey="dns-soa-email",
    safe_clsname="DnsSoaEmail",
    default_category=AttributeCategories.ATTRIBUTION,
    categories=frozenset({AttributeCategories.ATTRIBUTION}),
    to_ids=False,
)


AttributeType(
    dbkey="email-dst-display-name",
    safe_clsname="EmailDstDisplayName",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=False,
)


AttributeType(
    dbkey="email-header",
    safe_clsname="EmailHeader",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=False,
)


AttributeType(
    dbkey="email-message-id",
    safe_clsname="EmailMessageId",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=False,
)


AttributeType(
    dbkey="email-mime-boundary",
    safe_clsname="EmailMimeBoundary",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=False,
)


AttributeType(
    dbkey="email-reply-to",
    safe_clsname="EmailReplyTo",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=False,
)


AttributeType(
    dbkey="email-src-display-name",
    safe_clsname="EmailSrcDisplayName",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=False,
)


AttributeType(
    dbkey="email-thread-index",
    safe_clsname="EmailThreadIndex",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=False,
)


AttributeType(
    dbkey="email-x-mailer",
    safe_clsname="EmailXMailer",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=False,
)


AttributeType(
    dbkey="filename|authentihash",
    safe_clsname="FilenameAuthentihash",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|impfuzzy",
    safe_clsname="FilenameImpfuzzy",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|imphash",
    safe_clsname="FilenameImphash",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|md5",
    safe_clsname="FilenameMd5",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename-pattern",
    safe_clsname="FilenamePattern",
    default_category=AttributeCategories.PAYLOAD_INSTALLATION,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|pehash",
    safe_clsname="FilenamePehash",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|sha224",
    safe_clsname="FilenameSha224",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|sha384",
    safe_clsname="FilenameSha384",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|sha3-224",
    safe_clsname="FilenameSha3224",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|sha3-256",
    safe_clsname="FilenameSha3256",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|sha3-384",
    safe_clsname="FilenameSha3384",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|sha3-512",
    safe_clsname="FilenameSha3512",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|sha512",
    safe_clsname="FilenameSha512",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|sha512/224",
    safe_clsname="FilenameSha512224",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|sha512/256",
    safe_clsname="FilenameSha512256",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|ssdeep",
    safe_clsname="FilenameSsdeep",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|tlsh",
    safe_clsname="FilenameTlsh",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="filename|vhash",
    safe_clsname="FilenameVhash",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="first-name",
    safe_clsname="FirstName",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="frequent-flyer-number",
    safe_clsname="FrequentFlyerNumber",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="full-name",
    safe_clsname="FullName",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="gender",
    safe_clsname="Gender",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="gene",
    safe_clsname="Gene",
    default_category=AttributeCategories.ARTIFACTS_DROPPED,
    categories=frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    to_ids=False,
)


AttributeType(
    dbkey="github-organisation",
    safe_clsname="GithubOrganisation",
    default_category=AttributeCategories.SOCIAL_NETWORK,
    categories=frozenset({AttributeCategories.SOCIAL_NETWORK}),
    to_ids=False,
)


AttributeType(
    dbkey="github-repository",
    safe_clsname="GithubRepository",
    default_category=AttributeCategories.SOCIAL_NETWORK,
    categories=frozenset({AttributeCategories.EXTERNAL_ANALYSIS, AttributeCategories.SOCIAL_NETWORK}),
    to_ids=False,
)


AttributeType(
    dbkey="github-username",
    safe_clsname="GithubUsername",
    default_category=AttributeCategories.SOCIAL_NETWORK,
    categories=frozenset({AttributeCategories.SOCIAL_NETWORK}),
    to_ids=False,
)


AttributeType(
    dbkey="hex",
    safe_clsname="Hex",
    default_category=AttributeCategories.OTHER,
    categories=frozenset(
        {
            AttributeCategories.FINANCIAL_FRAUD,
            AttributeCategories.INTERNAL_REFERENCE,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.SUPPORT_TOOL,
            AttributeCategories.OTHER,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.ARTIFACTS_DROPPED,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="hostname|port",
    safe_clsname="HostnamePort",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=True,
)


AttributeType(
    dbkey="iban",
    safe_clsname="Iban",
    default_category=AttributeCategories.FINANCIAL_FRAUD,
    categories=frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    to_ids=True,
)


AttributeType(
    dbkey="identity-card-number",
    safe_clsname="IdentityCardNumber",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="impfuzzy",
    safe_clsname="Impfuzzy",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="imphash",
    safe_clsname="Imphash",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="integer",
    safe_clsname="MispInteger",
    default_category=AttributeCategories.OTHER,
    categories=frozenset({AttributeCategories.OTHER}),
    to_ids=False,
)


AttributeType(
    dbkey="ip-dst|port",
    safe_clsname="IpDstPort",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="ip-src|port",
    safe_clsname="IpSrcPort",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="issue-date-of-the-visa",
    safe_clsname="IssueDateOfTheVisa",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="jabber-id",
    safe_clsname="JabberId",
    default_category=AttributeCategories.SOCIAL_NETWORK,
    categories=frozenset({AttributeCategories.SOCIAL_NETWORK}),
    to_ids=False,
)


AttributeType(
    dbkey="kusto-query",
    safe_clsname="KustoQuery",
    default_category=AttributeCategories.ARTIFACTS_DROPPED,
    categories=frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    to_ids=False,
)


AttributeType(
    dbkey="last-name",
    safe_clsname="LastName",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="link",
    safe_clsname="Link",
    default_category=AttributeCategories.EXTERNAL_ANALYSIS,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.INTERNAL_REFERENCE,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.SUPPORT_TOOL,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="mac-address",
    safe_clsname="MacAddress",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="mac-eui-64",
    safe_clsname="MacEui64",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="malware-sample",
    safe_clsname="MalwareSample",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="malware-type",
    safe_clsname="MalwareType",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_INSTALLATION, AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=False,
)


AttributeType(
    dbkey="middle-name",
    safe_clsname="MiddleName",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="mime-type",
    safe_clsname="MimeType",
    default_category=AttributeCategories.ARTIFACTS_DROPPED,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="mobile-application-id",
    safe_clsname="MobileApplicationId",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_INSTALLATION, AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=True,
)


AttributeType(
    dbkey="mutex",
    safe_clsname="Mutex",
    default_category=AttributeCategories.ARTIFACTS_DROPPED,
    categories=frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    to_ids=True,
)


AttributeType(
    dbkey="named pipe",
    safe_clsname="NamedPipe",
    default_category=AttributeCategories.ARTIFACTS_DROPPED,
    categories=frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    to_ids=False,
)


AttributeType(
    dbkey="nationality",
    safe_clsname="Nationality",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="other",
    safe_clsname="Other",
    default_category=AttributeCategories.OTHER,
    categories=frozenset(
        {
            AttributeCategories.FINANCIAL_FRAUD,
            AttributeCategories.INTERNAL_REFERENCE,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.PERSON,
            AttributeCategories.PAYLOAD_TYPE,
            AttributeCategories.SUPPORT_TOOL,
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.OTHER,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.SOCIAL_NETWORK,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="passenger-name-record-locator-number",
    safe_clsname="PassengerNameRecordLocatorNumber",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="passport-country",
    safe_clsname="PassportCountry",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="passport-expiration",
    safe_clsname="PassportExpiration",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="passport-number",
    safe_clsname="PassportNumber",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="pattern-in-memory",
    safe_clsname="PatternInMemory",
    default_category=AttributeCategories.PAYLOAD_INSTALLATION,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="pattern-in-traffic",
    safe_clsname="PatternInTraffic",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="payment-details",
    safe_clsname="PaymentDetails",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="pehash",
    safe_clsname="Pehash",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_INSTALLATION, AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=True,
)


AttributeType(
    dbkey="pgp-private-key",
    safe_clsname="PgpPrivateKey",
    default_category=AttributeCategories.PERSON,
    categories=frozenset(
        {
            AttributeCategories.PERSON,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.OTHER,
            AttributeCategories.SOCIAL_NETWORK,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="pgp-public-key",
    safe_clsname="PgpPublicKey",
    default_category=AttributeCategories.PERSON,
    categories=frozenset(
        {
            AttributeCategories.PERSON,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.OTHER,
            AttributeCategories.SOCIAL_NETWORK,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="phone-number",
    safe_clsname="PhoneNumber",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON, AttributeCategories.FINANCIAL_FRAUD, AttributeCategories.OTHER}),
    to_ids=False,
)


AttributeType(
    dbkey="place-of-birth",
    safe_clsname="PlaceOfBirth",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="place-port-of-clearance",
    safe_clsname="PlacePortOfClearance",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="place-port-of-onward-foreign-destination",
    safe_clsname="PlacePortOfOnwardForeignDestination",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="place-port-of-original-embarkation",
    safe_clsname="PlacePortOfOriginalEmbarkation",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="port",
    safe_clsname="Port",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.NETWORK_ACTIVITY, AttributeCategories.OTHER}),
    to_ids=False,
)


AttributeType(
    dbkey="primary-residence",
    safe_clsname="PrimaryResidence",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="process-state",
    safe_clsname="ProcessState",
    default_category=AttributeCategories.ARTIFACTS_DROPPED,
    categories=frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    to_ids=False,
)


AttributeType(
    dbkey="prtn",
    safe_clsname="Prtn",
    default_category=AttributeCategories.FINANCIAL_FRAUD,
    categories=frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    to_ids=True,
)


AttributeType(
    dbkey="redress-number",
    safe_clsname="RedressNumber",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="sha224",
    safe_clsname="Sha224",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.ARTIFACTS_DROPPED,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="sha384",
    safe_clsname="Sha384",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="sha3-224",
    safe_clsname="Sha3224",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="sha3-256",
    safe_clsname="Sha3256",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="sha3-384",
    safe_clsname="Sha3384",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="sha3-512",
    safe_clsname="Sha3512",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="sha512",
    safe_clsname="Sha512",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="sha512/224",
    safe_clsname="Sha512224",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="sha512/256",
    safe_clsname="Sha512256",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="sigma",
    safe_clsname="Sigma",
    default_category=AttributeCategories.PAYLOAD_INSTALLATION,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="size-in-bytes",
    safe_clsname="SizeInBytes",
    default_category=AttributeCategories.OTHER,
    categories=frozenset({AttributeCategories.OTHER}),
    to_ids=False,
)


AttributeType(
    dbkey="snort",
    safe_clsname="Snort",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.EXTERNAL_ANALYSIS, AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=True,
)


AttributeType(
    dbkey="special-service-request",
    safe_clsname="SpecialServiceRequest",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="ssdeep",
    safe_clsname="Ssdeep",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="ssh-fingerprint",
    safe_clsname="SshFingerprint",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=False,
)


AttributeType(
    dbkey="stix2-pattern",
    safe_clsname="Stix2Pattern",
    default_category=AttributeCategories.PAYLOAD_INSTALLATION,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="target-email",
    safe_clsname="TargetEmail",
    default_category=AttributeCategories.TARGETING_DATA,
    categories=frozenset({AttributeCategories.TARGETING_DATA}),
    to_ids=False,
)


AttributeType(
    dbkey="target-external",
    safe_clsname="TargetExternal",
    default_category=AttributeCategories.TARGETING_DATA,
    categories=frozenset({AttributeCategories.TARGETING_DATA}),
    to_ids=False,
)


AttributeType(
    dbkey="target-location",
    safe_clsname="TargetLocation",
    default_category=AttributeCategories.TARGETING_DATA,
    categories=frozenset({AttributeCategories.TARGETING_DATA}),
    to_ids=False,
)


AttributeType(
    dbkey="target-machine",
    safe_clsname="TargetMachine",
    default_category=AttributeCategories.TARGETING_DATA,
    categories=frozenset({AttributeCategories.TARGETING_DATA}),
    to_ids=False,
)


AttributeType(
    dbkey="target-org",
    safe_clsname="TargetOrg",
    default_category=AttributeCategories.TARGETING_DATA,
    categories=frozenset({AttributeCategories.TARGETING_DATA}),
    to_ids=False,
)


AttributeType(
    dbkey="target-user",
    safe_clsname="TargetUser",
    default_category=AttributeCategories.TARGETING_DATA,
    categories=frozenset({AttributeCategories.TARGETING_DATA}),
    to_ids=False,
)


AttributeType(
    dbkey="telfhash",
    safe_clsname="Telfhash",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="text",
    safe_clsname="Text",
    default_category=AttributeCategories.OTHER,
    categories=frozenset(
        {
            AttributeCategories.FINANCIAL_FRAUD,
            AttributeCategories.INTERNAL_REFERENCE,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.PERSON,
            AttributeCategories.PAYLOAD_TYPE,
            AttributeCategories.SUPPORT_TOOL,
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.OTHER,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.SOCIAL_NETWORK,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="threat-actor",
    safe_clsname="ThreatActor",
    default_category=AttributeCategories.ATTRIBUTION,
    categories=frozenset({AttributeCategories.ATTRIBUTION}),
    to_ids=False,
)


AttributeType(
    dbkey="tlsh",
    safe_clsname="Tlsh",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset({AttributeCategories.PAYLOAD_INSTALLATION, AttributeCategories.PAYLOAD_DELIVERY}),
    to_ids=True,
)


AttributeType(
    dbkey="travel-details",
    safe_clsname="TravelDetails",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="twitter-id",
    safe_clsname="TwitterId",
    default_category=AttributeCategories.SOCIAL_NETWORK,
    categories=frozenset({AttributeCategories.SOCIAL_NETWORK}),
    to_ids=False,
)


AttributeType(
    dbkey="uri",
    safe_clsname="Uri",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset({AttributeCategories.NETWORK_ACTIVITY}),
    to_ids=True,
)


AttributeType(
    dbkey="vhash",
    safe_clsname="Vhash",
    default_category=AttributeCategories.PAYLOAD_DELIVERY,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="visa-number",
    safe_clsname="VisaNumber",
    default_category=AttributeCategories.PERSON,
    categories=frozenset({AttributeCategories.PERSON}),
    to_ids=False,
)


AttributeType(
    dbkey="vulnerability",
    safe_clsname="Vulnerability",
    default_category=AttributeCategories.EXTERNAL_ANALYSIS,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.PAYLOAD_DELIVERY,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="weakness",
    safe_clsname="Weakness",
    default_category=AttributeCategories.EXTERNAL_ANALYSIS,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.PAYLOAD_DELIVERY,
        }
    ),
    to_ids=False,
)


AttributeType(
    dbkey="whois-creation-date",
    safe_clsname="WhoisCreationDate",
    default_category=AttributeCategories.ATTRIBUTION,
    categories=frozenset({AttributeCategories.ATTRIBUTION}),
    to_ids=False,
)


AttributeType(
    dbkey="whois-registrant-email",
    safe_clsname="WhoisRegistrantEmail",
    default_category=AttributeCategories.ATTRIBUTION,
    categories=frozenset(
        {AttributeCategories.ATTRIBUTION, AttributeCategories.SOCIAL_NETWORK, AttributeCategories.PAYLOAD_DELIVERY}
    ),
    to_ids=False,
)


AttributeType(
    dbkey="whois-registrant-name",
    safe_clsname="WhoisRegistrantName",
    default_category=AttributeCategories.ATTRIBUTION,
    categories=frozenset({AttributeCategories.ATTRIBUTION}),
    to_ids=False,
)


AttributeType(
    dbkey="whois-registrant-org",
    safe_clsname="WhoisRegistrantOrg",
    default_category=AttributeCategories.ATTRIBUTION,
    categories=frozenset({AttributeCategories.ATTRIBUTION}),
    to_ids=False,
)


AttributeType(
    dbkey="whois-registrant-phone",
    safe_clsname="WhoisRegistrantPhone",
    default_category=AttributeCategories.ATTRIBUTION,
    categories=frozenset({AttributeCategories.ATTRIBUTION}),
    to_ids=False,
)


AttributeType(
    dbkey="whois-registrar",
    safe_clsname="WhoisRegistrar",
    default_category=AttributeCategories.ATTRIBUTION,
    categories=frozenset({AttributeCategories.ATTRIBUTION}),
    to_ids=False,
)


AttributeType(
    dbkey="windows-scheduled-task",
    safe_clsname="WindowsScheduledTask",
    default_category=AttributeCategories.ARTIFACTS_DROPPED,
    categories=frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    to_ids=False,
)


AttributeType(
    dbkey="windows-service-displayname",
    safe_clsname="WindowsServiceDisplayname",
    default_category=AttributeCategories.ARTIFACTS_DROPPED,
    categories=frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    to_ids=False,
)


AttributeType(
    dbkey="windows-service-name",
    safe_clsname="WindowsServiceName",
    default_category=AttributeCategories.ARTIFACTS_DROPPED,
    categories=frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    to_ids=False,
)


AttributeType(
    dbkey="x509-fingerprint-md5",
    safe_clsname="X509FingerprintMd5",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="x509-fingerprint-sha1",
    safe_clsname="X509FingerprintSha1",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="x509-fingerprint-sha256",
    safe_clsname="X509FingerprintSha256",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)


AttributeType(
    dbkey="xmr",
    safe_clsname="Xmr",
    default_category=AttributeCategories.FINANCIAL_FRAUD,
    categories=frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    to_ids=True,
)


AttributeType(
    dbkey="yara",
    safe_clsname="Yara",
    default_category=AttributeCategories.PAYLOAD_INSTALLATION,
    categories=frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    to_ids=True,
)

AttributeType(
    dbkey="dom-hash",
    safe_clsname="DomHash",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    to_ids=True,
)

AttributeType(
    dbkey="onion-address",
    safe_clsname="OnionAddress",
    default_category=AttributeCategories.NETWORK_ACTIVITY,
    categories=frozenset(
        {
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_DELIVERY,
        }
    ),
    to_ids=True,
)


mapper_val_safe_clsname = {x.dbkey: x.safe_clsname for x in AttributeType.all_attributes}
mapper_safe_clsname_val = dict((v, k) for k, v in mapper_val_safe_clsname.items())
literal_valid_attribute_types = Literal[tuple([k for k in mapper_val_safe_clsname.keys()])]  # type:ignore[valid-type]
default_category = {x.dbkey: x.default_category for x in AttributeType.all_attributes}
categories = {x.dbkey: x.categories for x in AttributeType.all_attributes}

inverted_categories = defaultdict(list)

for key, value in categories.items():
    for category in value:
        inverted_categories[category.value].append(key)

to_ids = {x.dbkey: x.to_ids for x in AttributeType.all_attributes}
