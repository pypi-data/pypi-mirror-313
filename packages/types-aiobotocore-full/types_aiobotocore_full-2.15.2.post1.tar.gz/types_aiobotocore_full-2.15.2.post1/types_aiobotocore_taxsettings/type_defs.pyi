"""
Type annotations for taxsettings service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/type_defs/)

Usage::

    ```python
    from types_aiobotocore_taxsettings.type_defs import TaxInheritanceDetailsTypeDef

    data: TaxInheritanceDetailsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence, Union

from .literals import (
    AddressRoleTypeType,
    IndustriesType,
    IsraelCustomerTypeType,
    IsraelDealerTypeType,
    MalaysiaServiceTaxCodeType,
    PersonTypeType,
    RegistrationTypeType,
    SaudiArabiaTaxRegistrationNumberTypeType,
    SectorType,
    TaxRegistrationNumberTypeType,
    TaxRegistrationStatusType,
    TaxRegistrationTypeType,
    UkraineTrnTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AccountDetailsTypeDef",
    "AccountMetaDataTypeDef",
    "AdditionalInfoRequestTypeDef",
    "AdditionalInfoResponseTypeDef",
    "AddressTypeDef",
    "BatchDeleteTaxRegistrationErrorTypeDef",
    "BatchDeleteTaxRegistrationRequestRequestTypeDef",
    "BatchDeleteTaxRegistrationResponseTypeDef",
    "BatchPutTaxRegistrationErrorTypeDef",
    "BatchPutTaxRegistrationRequestRequestTypeDef",
    "BatchPutTaxRegistrationResponseTypeDef",
    "BrazilAdditionalInfoTypeDef",
    "CanadaAdditionalInfoTypeDef",
    "DeleteTaxRegistrationRequestRequestTypeDef",
    "DestinationS3LocationTypeDef",
    "EstoniaAdditionalInfoTypeDef",
    "GeorgiaAdditionalInfoTypeDef",
    "GetTaxRegistrationDocumentRequestRequestTypeDef",
    "GetTaxRegistrationDocumentResponseTypeDef",
    "GetTaxRegistrationRequestRequestTypeDef",
    "GetTaxRegistrationResponseTypeDef",
    "IndiaAdditionalInfoTypeDef",
    "IsraelAdditionalInfoTypeDef",
    "ItalyAdditionalInfoTypeDef",
    "JurisdictionTypeDef",
    "KenyaAdditionalInfoTypeDef",
    "ListTaxRegistrationsRequestListTaxRegistrationsPaginateTypeDef",
    "ListTaxRegistrationsRequestRequestTypeDef",
    "ListTaxRegistrationsResponseTypeDef",
    "MalaysiaAdditionalInfoOutputTypeDef",
    "MalaysiaAdditionalInfoTypeDef",
    "MalaysiaAdditionalInfoUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PolandAdditionalInfoTypeDef",
    "PutTaxRegistrationRequestRequestTypeDef",
    "PutTaxRegistrationResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RomaniaAdditionalInfoTypeDef",
    "SaudiArabiaAdditionalInfoTypeDef",
    "SourceS3LocationTypeDef",
    "SouthKoreaAdditionalInfoTypeDef",
    "SpainAdditionalInfoTypeDef",
    "TaxDocumentMetadataTypeDef",
    "TaxInheritanceDetailsTypeDef",
    "TaxRegistrationDocumentTypeDef",
    "TaxRegistrationEntryTypeDef",
    "TaxRegistrationTypeDef",
    "TaxRegistrationWithJurisdictionTypeDef",
    "TurkeyAdditionalInfoTypeDef",
    "UkraineAdditionalInfoTypeDef",
    "VerificationDetailsTypeDef",
)

class TaxInheritanceDetailsTypeDef(TypedDict):
    inheritanceObtainedReason: NotRequired[str]
    parentEntityId: NotRequired[str]

class AddressTypeDef(TypedDict):
    addressLine1: str
    city: str
    countryCode: str
    postalCode: str
    addressLine2: NotRequired[str]
    addressLine3: NotRequired[str]
    districtOrCounty: NotRequired[str]
    stateOrRegion: NotRequired[str]

class JurisdictionTypeDef(TypedDict):
    countryCode: str
    stateOrRegion: NotRequired[str]

class CanadaAdditionalInfoTypeDef(TypedDict):
    canadaQuebecSalesTaxNumber: NotRequired[str]
    canadaRetailSalesTaxNumber: NotRequired[str]
    isResellerAccount: NotRequired[bool]
    provincialSalesTaxId: NotRequired[str]

class EstoniaAdditionalInfoTypeDef(TypedDict):
    registryCommercialCode: str

class GeorgiaAdditionalInfoTypeDef(TypedDict):
    personType: PersonTypeType

class IsraelAdditionalInfoTypeDef(TypedDict):
    customerType: IsraelCustomerTypeType
    dealerType: IsraelDealerTypeType

class ItalyAdditionalInfoTypeDef(TypedDict):
    cigNumber: NotRequired[str]
    cupNumber: NotRequired[str]
    sdiAccountId: NotRequired[str]
    taxCode: NotRequired[str]

class KenyaAdditionalInfoTypeDef(TypedDict):
    personType: PersonTypeType

class PolandAdditionalInfoTypeDef(TypedDict):
    individualRegistrationNumber: NotRequired[str]
    isGroupVatEnabled: NotRequired[bool]

class RomaniaAdditionalInfoTypeDef(TypedDict):
    taxRegistrationNumberType: TaxRegistrationNumberTypeType

class SaudiArabiaAdditionalInfoTypeDef(TypedDict):
    taxRegistrationNumberType: NotRequired[SaudiArabiaTaxRegistrationNumberTypeType]

class SouthKoreaAdditionalInfoTypeDef(TypedDict):
    businessRepresentativeName: str
    itemOfBusiness: str
    lineOfBusiness: str

class SpainAdditionalInfoTypeDef(TypedDict):
    registrationType: RegistrationTypeType

class TurkeyAdditionalInfoTypeDef(TypedDict):
    industries: NotRequired[IndustriesType]
    kepEmailId: NotRequired[str]
    secondaryTaxId: NotRequired[str]
    taxOffice: NotRequired[str]

class UkraineAdditionalInfoTypeDef(TypedDict):
    ukraineTrnType: UkraineTrnTypeType

class BrazilAdditionalInfoTypeDef(TypedDict):
    ccmCode: NotRequired[str]
    legalNatureCode: NotRequired[str]

class IndiaAdditionalInfoTypeDef(TypedDict):
    pan: NotRequired[str]

class MalaysiaAdditionalInfoOutputTypeDef(TypedDict):
    serviceTaxCodes: List[MalaysiaServiceTaxCodeType]

class BatchDeleteTaxRegistrationErrorTypeDef(TypedDict):
    accountId: str
    message: str
    code: NotRequired[str]

class BatchDeleteTaxRegistrationRequestRequestTypeDef(TypedDict):
    accountIds: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchPutTaxRegistrationErrorTypeDef(TypedDict):
    accountId: str
    message: str
    code: NotRequired[str]

class DeleteTaxRegistrationRequestRequestTypeDef(TypedDict):
    accountId: NotRequired[str]

class DestinationS3LocationTypeDef(TypedDict):
    bucket: str
    prefix: NotRequired[str]

class TaxDocumentMetadataTypeDef(TypedDict):
    taxDocumentAccessToken: str
    taxDocumentName: str

class GetTaxRegistrationRequestRequestTypeDef(TypedDict):
    accountId: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListTaxRegistrationsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class MalaysiaAdditionalInfoTypeDef(TypedDict):
    serviceTaxCodes: Sequence[MalaysiaServiceTaxCodeType]

class SourceS3LocationTypeDef(TypedDict):
    bucket: str
    key: str

class AccountMetaDataTypeDef(TypedDict):
    accountName: NotRequired[str]
    address: NotRequired[AddressTypeDef]
    addressRoleMap: NotRequired[Dict[AddressRoleTypeType, JurisdictionTypeDef]]
    addressType: NotRequired[AddressRoleTypeType]
    seller: NotRequired[str]

class AdditionalInfoResponseTypeDef(TypedDict):
    brazilAdditionalInfo: NotRequired[BrazilAdditionalInfoTypeDef]
    canadaAdditionalInfo: NotRequired[CanadaAdditionalInfoTypeDef]
    estoniaAdditionalInfo: NotRequired[EstoniaAdditionalInfoTypeDef]
    georgiaAdditionalInfo: NotRequired[GeorgiaAdditionalInfoTypeDef]
    indiaAdditionalInfo: NotRequired[IndiaAdditionalInfoTypeDef]
    israelAdditionalInfo: NotRequired[IsraelAdditionalInfoTypeDef]
    italyAdditionalInfo: NotRequired[ItalyAdditionalInfoTypeDef]
    kenyaAdditionalInfo: NotRequired[KenyaAdditionalInfoTypeDef]
    malaysiaAdditionalInfo: NotRequired[MalaysiaAdditionalInfoOutputTypeDef]
    polandAdditionalInfo: NotRequired[PolandAdditionalInfoTypeDef]
    romaniaAdditionalInfo: NotRequired[RomaniaAdditionalInfoTypeDef]
    saudiArabiaAdditionalInfo: NotRequired[SaudiArabiaAdditionalInfoTypeDef]
    southKoreaAdditionalInfo: NotRequired[SouthKoreaAdditionalInfoTypeDef]
    spainAdditionalInfo: NotRequired[SpainAdditionalInfoTypeDef]
    turkeyAdditionalInfo: NotRequired[TurkeyAdditionalInfoTypeDef]
    ukraineAdditionalInfo: NotRequired[UkraineAdditionalInfoTypeDef]

class BatchDeleteTaxRegistrationResponseTypeDef(TypedDict):
    errors: List[BatchDeleteTaxRegistrationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetTaxRegistrationDocumentResponseTypeDef(TypedDict):
    destinationFilePath: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutTaxRegistrationResponseTypeDef(TypedDict):
    status: TaxRegistrationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class BatchPutTaxRegistrationResponseTypeDef(TypedDict):
    errors: List[BatchPutTaxRegistrationErrorTypeDef]
    status: TaxRegistrationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class GetTaxRegistrationDocumentRequestRequestTypeDef(TypedDict):
    destinationS3Location: DestinationS3LocationTypeDef
    taxDocumentMetadata: TaxDocumentMetadataTypeDef

class ListTaxRegistrationsRequestListTaxRegistrationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

MalaysiaAdditionalInfoUnionTypeDef = Union[
    MalaysiaAdditionalInfoTypeDef, MalaysiaAdditionalInfoOutputTypeDef
]

class TaxRegistrationDocumentTypeDef(TypedDict):
    s3Location: SourceS3LocationTypeDef

class TaxRegistrationTypeDef(TypedDict):
    legalAddress: AddressTypeDef
    legalName: str
    registrationId: str
    registrationType: TaxRegistrationTypeType
    status: TaxRegistrationStatusType
    additionalTaxInformation: NotRequired[AdditionalInfoResponseTypeDef]
    certifiedEmailId: NotRequired[str]
    sector: NotRequired[SectorType]
    taxDocumentMetadatas: NotRequired[List[TaxDocumentMetadataTypeDef]]

class TaxRegistrationWithJurisdictionTypeDef(TypedDict):
    jurisdiction: JurisdictionTypeDef
    legalName: str
    registrationId: str
    registrationType: TaxRegistrationTypeType
    status: TaxRegistrationStatusType
    additionalTaxInformation: NotRequired[AdditionalInfoResponseTypeDef]
    certifiedEmailId: NotRequired[str]
    sector: NotRequired[SectorType]
    taxDocumentMetadatas: NotRequired[List[TaxDocumentMetadataTypeDef]]

class AdditionalInfoRequestTypeDef(TypedDict):
    canadaAdditionalInfo: NotRequired[CanadaAdditionalInfoTypeDef]
    estoniaAdditionalInfo: NotRequired[EstoniaAdditionalInfoTypeDef]
    georgiaAdditionalInfo: NotRequired[GeorgiaAdditionalInfoTypeDef]
    israelAdditionalInfo: NotRequired[IsraelAdditionalInfoTypeDef]
    italyAdditionalInfo: NotRequired[ItalyAdditionalInfoTypeDef]
    kenyaAdditionalInfo: NotRequired[KenyaAdditionalInfoTypeDef]
    malaysiaAdditionalInfo: NotRequired[MalaysiaAdditionalInfoUnionTypeDef]
    polandAdditionalInfo: NotRequired[PolandAdditionalInfoTypeDef]
    romaniaAdditionalInfo: NotRequired[RomaniaAdditionalInfoTypeDef]
    saudiArabiaAdditionalInfo: NotRequired[SaudiArabiaAdditionalInfoTypeDef]
    southKoreaAdditionalInfo: NotRequired[SouthKoreaAdditionalInfoTypeDef]
    spainAdditionalInfo: NotRequired[SpainAdditionalInfoTypeDef]
    turkeyAdditionalInfo: NotRequired[TurkeyAdditionalInfoTypeDef]
    ukraineAdditionalInfo: NotRequired[UkraineAdditionalInfoTypeDef]

class VerificationDetailsTypeDef(TypedDict):
    dateOfBirth: NotRequired[str]
    taxRegistrationDocuments: NotRequired[Sequence[TaxRegistrationDocumentTypeDef]]

class GetTaxRegistrationResponseTypeDef(TypedDict):
    taxRegistration: TaxRegistrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AccountDetailsTypeDef(TypedDict):
    accountId: NotRequired[str]
    accountMetaData: NotRequired[AccountMetaDataTypeDef]
    taxInheritanceDetails: NotRequired[TaxInheritanceDetailsTypeDef]
    taxRegistration: NotRequired[TaxRegistrationWithJurisdictionTypeDef]

class TaxRegistrationEntryTypeDef(TypedDict):
    registrationId: str
    registrationType: TaxRegistrationTypeType
    additionalTaxInformation: NotRequired[AdditionalInfoRequestTypeDef]
    certifiedEmailId: NotRequired[str]
    legalAddress: NotRequired[AddressTypeDef]
    legalName: NotRequired[str]
    sector: NotRequired[SectorType]
    verificationDetails: NotRequired[VerificationDetailsTypeDef]

class ListTaxRegistrationsResponseTypeDef(TypedDict):
    accountDetails: List[AccountDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchPutTaxRegistrationRequestRequestTypeDef(TypedDict):
    accountIds: Sequence[str]
    taxRegistrationEntry: TaxRegistrationEntryTypeDef

class PutTaxRegistrationRequestRequestTypeDef(TypedDict):
    taxRegistrationEntry: TaxRegistrationEntryTypeDef
    accountId: NotRequired[str]
