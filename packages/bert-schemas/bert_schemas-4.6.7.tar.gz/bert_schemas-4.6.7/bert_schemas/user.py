# Copyright 2024 Infleqtion
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# type: ignore
from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    StringConstraints,
    field_serializer,
    model_serializer,
)

from .questionnaire import RegistrationQandA

external_user_id: type[str] = Annotated[
    str, StringConstraints(pattern=r"^auth0|[a-z0-9]{24}$")
]


class RoleName(str, Enum):
    superuser = "superuser"
    user = "user"
    offline = "offline"

    def __str__(self):
        return str(self.value)


class PurchaseEntity(str, Enum):
    USER = "USER"
    PAID = "PAID"
    ORG = "ORG"


class JobLimitType(str, Enum):
    JOB_RATE = "JOB_RATE"
    JOB_QUOTA = "JOB_QUOTA"


class ExternalUserId(BaseModel):
    external_user_id: external_user_id


class Role(BaseModel):
    role_name: str
    model_config = ConfigDict(from_attributes=True)


class OrganizationBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class Organization(OrganizationBase):
    id: int
    slug: str
    model_config = ConfigDict(from_attributes=True)


class OrgUser(BaseModel):
    user_id: int
    org_id: int
    slug: str


class UserBase(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    email: EmailStr
    affiliation: str | None = None

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class OrganizationUser(UserBase):
    external_user_id: external_user_id
    jobs_run_today: int


class EmailPreference(BaseModel):
    jobs: bool
    general: bool
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserBase):
    name: Annotated[str, StringConstraints(min_length=1, max_length=100)] | None = None
    email: EmailStr | None = None
    onboard_date: datetime | None = None
    email_preferences: EmailPreference | None = None


class UserResponse(UserBase):
    external_user_id: external_user_id
    signup_date: datetime
    onboard_date: datetime | None = None
    active: bool
    email_preferences: EmailPreference
    org_user: OrgUser | None = Field(serialization_alias="organization", default=None)
    roles: list[Role] | None = None

    @field_serializer("roles")
    def role_names(roles: list[Role] | None) -> list[str] | None:
        return [role.role_name for role in roles] if roles else None

    @field_serializer("org_user")
    def organization(org_user: OrgUser | None) -> str | None:
        return org_user.slug if org_user else None


class UserSearchResponse(UserResponse):
    external_user_id: str


class User(UserBase):
    id: int
    external_user_id: external_user_id
    signup_date: datetime


class UserCreate(UserBase):
    external_user_id: external_user_id


class UserSignUp(UserBase):
    questionnaire: RegistrationQandA
    country: str
    response: str | None = None
    model_config = ConfigDict(use_enum_values=True)


class JobLimit(BaseModel):
    daily_limit: int
    daily_remaining: int
    standard_credits: int | None = None
    priority_credits: int | None = None


class JobPurchase(BaseModel):
    purchase_date: datetime
    quantity: int
    model_config = ConfigDict(from_attributes=True)


class UserJobPurchase(JobPurchase):
    user_id: int | None = None


class OrgJobPurchase(JobPurchase):
    org_id: int | None = None


class PurchasePriceData(BaseModel):
    currency: str
    product_data: dict
    unit_amount: int


class PurchaseLineItemQuantity(BaseModel):
    enabled: bool
    minimum: int
    maximum: int


class PurchaseLineItem(BaseModel):
    amount: int | None = None
    currency: str | None = None
    description: str | None = None
    price: str
    quantity: int
    adjustable_quantity: PurchaseLineItemQuantity | None = None
    price_data: PurchasePriceData | None = None


class CheckoutSessionLineItem(BaseModel):
    quantity: int


class CheckoutSession(BaseModel):
    status: str
    created: datetime
    amount_total: int
    line_items: list[CheckoutSessionLineItem]


class PurchaseCharge(BaseModel):
    created: datetime
    amount_captured: int
    currency: str
    card_last4: int
    card_brand: str
    receipt_url: str
    quantity: int


class CheckoutSessionLineItem(BaseModel):
    quantity: int


class CheckoutSessionResponse(BaseModel):
    session_url: HttpUrl


class EmailBase(BaseModel):
    subject: str
    email: EmailStr
    content: Annotated[str, StringConstraints(min_length=1, max_length=500)]


class FeedbackEmail(EmailBase):
    follow_up_requested: bool


class PasswordReset(BaseModel):
    redirect_url: str


class SalesforceLead(BaseModel):
    first_name: Annotated[str, StringConstraints(min_length=1, max_length=40)]
    last_name: Annotated[str, StringConstraints(min_length=1, max_length=80)]
    email: EmailStr
    company: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    external_user_id: external_user_id
    registration_date: datetime
    country: str

    @model_serializer
    def model(self) -> dict:
        return {
            "FirstName": self.first_name,
            "LastName": self.last_name,
            "Email": self.email,
            "Company": self.company,
            "QMS_User_ID__c": self.external_user_id,
            "QMS_Registration_Date__c": self.registration_date.strftime("%Y-%m-%d"),
            "Country": self.country,
        }
