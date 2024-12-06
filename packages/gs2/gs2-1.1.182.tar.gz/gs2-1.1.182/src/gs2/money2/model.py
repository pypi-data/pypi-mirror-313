# Copyright 2016 Game Server Services, Inc. or its affiliates. All Rights
# Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from __future__ import annotations

import re
from typing import *
from gs2 import core


class UnusedBalance(core.Gs2Model):
    unused_balance_id: str = None
    currency: str = None
    balance: float = None
    updated_at: int = None
    revision: int = None

    def with_unused_balance_id(self, unused_balance_id: str) -> UnusedBalance:
        self.unused_balance_id = unused_balance_id
        return self

    def with_currency(self, currency: str) -> UnusedBalance:
        self.currency = currency
        return self

    def with_balance(self, balance: float) -> UnusedBalance:
        self.balance = balance
        return self

    def with_updated_at(self, updated_at: int) -> UnusedBalance:
        self.updated_at = updated_at
        return self

    def with_revision(self, revision: int) -> UnusedBalance:
        self.revision = revision
        return self

    @classmethod
    def create_grn(
        cls,
        region,
        owner_id,
        namespace_name,
        currency,
    ):
        return 'grn:gs2:{region}:{ownerId}:money2:{namespaceName}:unused:{currency}'.format(
            region=region,
            ownerId=owner_id,
            namespaceName=namespace_name,
            currency=currency,
        )

    @classmethod
    def get_region_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):unused:(?P<currency>.+)', grn)
        if match is None:
            return None
        return match.group('region')

    @classmethod
    def get_owner_id_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):unused:(?P<currency>.+)', grn)
        if match is None:
            return None
        return match.group('owner_id')

    @classmethod
    def get_namespace_name_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):unused:(?P<currency>.+)', grn)
        if match is None:
            return None
        return match.group('namespace_name')

    @classmethod
    def get_currency_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):unused:(?P<currency>.+)', grn)
        if match is None:
            return None
        return match.group('currency')

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[UnusedBalance]:
        if data is None:
            return None
        return UnusedBalance()\
            .with_unused_balance_id(data.get('unusedBalanceId'))\
            .with_currency(data.get('currency'))\
            .with_balance(data.get('balance'))\
            .with_updated_at(data.get('updatedAt'))\
            .with_revision(data.get('revision'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "unusedBalanceId": self.unused_balance_id,
            "currency": self.currency,
            "balance": self.balance,
            "updatedAt": self.updated_at,
            "revision": self.revision,
        }


class DailyTransactionHistory(core.Gs2Model):
    daily_transaction_history_id: str = None
    year: int = None
    month: int = None
    day: int = None
    currency: str = None
    deposit_amount: float = None
    withdraw_amount: float = None
    updated_at: int = None
    revision: int = None

    def with_daily_transaction_history_id(self, daily_transaction_history_id: str) -> DailyTransactionHistory:
        self.daily_transaction_history_id = daily_transaction_history_id
        return self

    def with_year(self, year: int) -> DailyTransactionHistory:
        self.year = year
        return self

    def with_month(self, month: int) -> DailyTransactionHistory:
        self.month = month
        return self

    def with_day(self, day: int) -> DailyTransactionHistory:
        self.day = day
        return self

    def with_currency(self, currency: str) -> DailyTransactionHistory:
        self.currency = currency
        return self

    def with_deposit_amount(self, deposit_amount: float) -> DailyTransactionHistory:
        self.deposit_amount = deposit_amount
        return self

    def with_withdraw_amount(self, withdraw_amount: float) -> DailyTransactionHistory:
        self.withdraw_amount = withdraw_amount
        return self

    def with_updated_at(self, updated_at: int) -> DailyTransactionHistory:
        self.updated_at = updated_at
        return self

    def with_revision(self, revision: int) -> DailyTransactionHistory:
        self.revision = revision
        return self

    @classmethod
    def create_grn(
        cls,
        region,
        owner_id,
        namespace_name,
        year,
        month,
        day,
        currency,
    ):
        return 'grn:gs2:{region}:{ownerId}:money2:{namespaceName}:transaction:history:daily:{year}:{month}:{day}:currency:{currency}'.format(
            region=region,
            ownerId=owner_id,
            namespaceName=namespace_name,
            year=year,
            month=month,
            day=day,
            currency=currency,
        )

    @classmethod
    def get_region_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):transaction:history:daily:(?P<year>.+):(?P<month>.+):(?P<day>.+):currency:(?P<currency>.+)', grn)
        if match is None:
            return None
        return match.group('region')

    @classmethod
    def get_owner_id_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):transaction:history:daily:(?P<year>.+):(?P<month>.+):(?P<day>.+):currency:(?P<currency>.+)', grn)
        if match is None:
            return None
        return match.group('owner_id')

    @classmethod
    def get_namespace_name_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):transaction:history:daily:(?P<year>.+):(?P<month>.+):(?P<day>.+):currency:(?P<currency>.+)', grn)
        if match is None:
            return None
        return match.group('namespace_name')

    @classmethod
    def get_year_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):transaction:history:daily:(?P<year>.+):(?P<month>.+):(?P<day>.+):currency:(?P<currency>.+)', grn)
        if match is None:
            return None
        return match.group('year')

    @classmethod
    def get_month_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):transaction:history:daily:(?P<year>.+):(?P<month>.+):(?P<day>.+):currency:(?P<currency>.+)', grn)
        if match is None:
            return None
        return match.group('month')

    @classmethod
    def get_day_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):transaction:history:daily:(?P<year>.+):(?P<month>.+):(?P<day>.+):currency:(?P<currency>.+)', grn)
        if match is None:
            return None
        return match.group('day')

    @classmethod
    def get_currency_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):transaction:history:daily:(?P<year>.+):(?P<month>.+):(?P<day>.+):currency:(?P<currency>.+)', grn)
        if match is None:
            return None
        return match.group('currency')

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[DailyTransactionHistory]:
        if data is None:
            return None
        return DailyTransactionHistory()\
            .with_daily_transaction_history_id(data.get('dailyTransactionHistoryId'))\
            .with_year(data.get('year'))\
            .with_month(data.get('month'))\
            .with_day(data.get('day'))\
            .with_currency(data.get('currency'))\
            .with_deposit_amount(data.get('depositAmount'))\
            .with_withdraw_amount(data.get('withdrawAmount'))\
            .with_updated_at(data.get('updatedAt'))\
            .with_revision(data.get('revision'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dailyTransactionHistoryId": self.daily_transaction_history_id,
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "currency": self.currency,
            "depositAmount": self.deposit_amount,
            "withdrawAmount": self.withdraw_amount,
            "updatedAt": self.updated_at,
            "revision": self.revision,
        }


class LogSetting(core.Gs2Model):
    logging_namespace_id: str = None

    def with_logging_namespace_id(self, logging_namespace_id: str) -> LogSetting:
        self.logging_namespace_id = logging_namespace_id
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[LogSetting]:
        if data is None:
            return None
        return LogSetting()\
            .with_logging_namespace_id(data.get('loggingNamespaceId'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "loggingNamespaceId": self.logging_namespace_id,
        }


class ScriptSetting(core.Gs2Model):
    trigger_script_id: str = None
    done_trigger_target_type: str = None
    done_trigger_script_id: str = None
    done_trigger_queue_namespace_id: str = None

    def with_trigger_script_id(self, trigger_script_id: str) -> ScriptSetting:
        self.trigger_script_id = trigger_script_id
        return self

    def with_done_trigger_target_type(self, done_trigger_target_type: str) -> ScriptSetting:
        self.done_trigger_target_type = done_trigger_target_type
        return self

    def with_done_trigger_script_id(self, done_trigger_script_id: str) -> ScriptSetting:
        self.done_trigger_script_id = done_trigger_script_id
        return self

    def with_done_trigger_queue_namespace_id(self, done_trigger_queue_namespace_id: str) -> ScriptSetting:
        self.done_trigger_queue_namespace_id = done_trigger_queue_namespace_id
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[ScriptSetting]:
        if data is None:
            return None
        return ScriptSetting()\
            .with_trigger_script_id(data.get('triggerScriptId'))\
            .with_done_trigger_target_type(data.get('doneTriggerTargetType'))\
            .with_done_trigger_script_id(data.get('doneTriggerScriptId'))\
            .with_done_trigger_queue_namespace_id(data.get('doneTriggerQueueNamespaceId'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "triggerScriptId": self.trigger_script_id,
            "doneTriggerTargetType": self.done_trigger_target_type,
            "doneTriggerScriptId": self.done_trigger_script_id,
            "doneTriggerQueueNamespaceId": self.done_trigger_queue_namespace_id,
        }


class GitHubCheckoutSetting(core.Gs2Model):
    api_key_id: str = None
    repository_name: str = None
    source_path: str = None
    reference_type: str = None
    commit_hash: str = None
    branch_name: str = None
    tag_name: str = None

    def with_api_key_id(self, api_key_id: str) -> GitHubCheckoutSetting:
        self.api_key_id = api_key_id
        return self

    def with_repository_name(self, repository_name: str) -> GitHubCheckoutSetting:
        self.repository_name = repository_name
        return self

    def with_source_path(self, source_path: str) -> GitHubCheckoutSetting:
        self.source_path = source_path
        return self

    def with_reference_type(self, reference_type: str) -> GitHubCheckoutSetting:
        self.reference_type = reference_type
        return self

    def with_commit_hash(self, commit_hash: str) -> GitHubCheckoutSetting:
        self.commit_hash = commit_hash
        return self

    def with_branch_name(self, branch_name: str) -> GitHubCheckoutSetting:
        self.branch_name = branch_name
        return self

    def with_tag_name(self, tag_name: str) -> GitHubCheckoutSetting:
        self.tag_name = tag_name
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[GitHubCheckoutSetting]:
        if data is None:
            return None
        return GitHubCheckoutSetting()\
            .with_api_key_id(data.get('apiKeyId'))\
            .with_repository_name(data.get('repositoryName'))\
            .with_source_path(data.get('sourcePath'))\
            .with_reference_type(data.get('referenceType'))\
            .with_commit_hash(data.get('commitHash'))\
            .with_branch_name(data.get('branchName'))\
            .with_tag_name(data.get('tagName'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "apiKeyId": self.api_key_id,
            "repositoryName": self.repository_name,
            "sourcePath": self.source_path,
            "referenceType": self.reference_type,
            "commitHash": self.commit_hash,
            "branchName": self.branch_name,
            "tagName": self.tag_name,
        }


class GooglePlayContent(core.Gs2Model):
    product_id: str = None

    def with_product_id(self, product_id: str) -> GooglePlayContent:
        self.product_id = product_id
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[GooglePlayContent]:
        if data is None:
            return None
        return GooglePlayContent()\
            .with_product_id(data.get('productId'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "productId": self.product_id,
        }


class AppleAppStoreContent(core.Gs2Model):
    product_id: str = None

    def with_product_id(self, product_id: str) -> AppleAppStoreContent:
        self.product_id = product_id
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[AppleAppStoreContent]:
        if data is None:
            return None
        return AppleAppStoreContent()\
            .with_product_id(data.get('productId'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "productId": self.product_id,
        }


class GooglePlayVerifyReceiptEvent(core.Gs2Model):
    purchase_token: str = None

    def with_purchase_token(self, purchase_token: str) -> GooglePlayVerifyReceiptEvent:
        self.purchase_token = purchase_token
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[GooglePlayVerifyReceiptEvent]:
        if data is None:
            return None
        return GooglePlayVerifyReceiptEvent()\
            .with_purchase_token(data.get('purchaseToken'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "purchaseToken": self.purchase_token,
        }


class AppleAppStoreVerifyReceiptEvent(core.Gs2Model):
    environment: str = None

    def with_environment(self, environment: str) -> AppleAppStoreVerifyReceiptEvent:
        self.environment = environment
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[AppleAppStoreVerifyReceiptEvent]:
        if data is None:
            return None
        return AppleAppStoreVerifyReceiptEvent()\
            .with_environment(data.get('environment'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "environment": self.environment,
        }


class WithdrawEvent(core.Gs2Model):
    slot: int = None
    withdraw_details: List[DepositTransaction] = None
    status: WalletSummary = None

    def with_slot(self, slot: int) -> WithdrawEvent:
        self.slot = slot
        return self

    def with_withdraw_details(self, withdraw_details: List[DepositTransaction]) -> WithdrawEvent:
        self.withdraw_details = withdraw_details
        return self

    def with_status(self, status: WalletSummary) -> WithdrawEvent:
        self.status = status
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[WithdrawEvent]:
        if data is None:
            return None
        return WithdrawEvent()\
            .with_slot(data.get('slot'))\
            .with_withdraw_details(None if data.get('withdrawDetails') is None else [
                DepositTransaction.from_dict(data.get('withdrawDetails')[i])
                for i in range(len(data.get('withdrawDetails')))
            ])\
            .with_status(WalletSummary.from_dict(data.get('status')))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "slot": self.slot,
            "withdrawDetails": None if self.withdraw_details is None else [
                self.withdraw_details[i].to_dict() if self.withdraw_details[i] else None
                for i in range(len(self.withdraw_details))
            ],
            "status": self.status.to_dict() if self.status else None,
        }


class DepositEvent(core.Gs2Model):
    slot: int = None
    deposit_transactions: List[DepositTransaction] = None
    status: WalletSummary = None

    def with_slot(self, slot: int) -> DepositEvent:
        self.slot = slot
        return self

    def with_deposit_transactions(self, deposit_transactions: List[DepositTransaction]) -> DepositEvent:
        self.deposit_transactions = deposit_transactions
        return self

    def with_status(self, status: WalletSummary) -> DepositEvent:
        self.status = status
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[DepositEvent]:
        if data is None:
            return None
        return DepositEvent()\
            .with_slot(data.get('slot'))\
            .with_deposit_transactions(None if data.get('depositTransactions') is None else [
                DepositTransaction.from_dict(data.get('depositTransactions')[i])
                for i in range(len(data.get('depositTransactions')))
            ])\
            .with_status(WalletSummary.from_dict(data.get('status')))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "slot": self.slot,
            "depositTransactions": None if self.deposit_transactions is None else [
                self.deposit_transactions[i].to_dict() if self.deposit_transactions[i] else None
                for i in range(len(self.deposit_transactions))
            ],
            "status": self.status.to_dict() if self.status else None,
        }


class VerifyReceiptEvent(core.Gs2Model):
    content_name: str = None
    platform: str = None
    apple_app_store_verify_receipt_event: AppleAppStoreVerifyReceiptEvent = None
    google_play_verify_receipt_event: GooglePlayVerifyReceiptEvent = None

    def with_content_name(self, content_name: str) -> VerifyReceiptEvent:
        self.content_name = content_name
        return self

    def with_platform(self, platform: str) -> VerifyReceiptEvent:
        self.platform = platform
        return self

    def with_apple_app_store_verify_receipt_event(self, apple_app_store_verify_receipt_event: AppleAppStoreVerifyReceiptEvent) -> VerifyReceiptEvent:
        self.apple_app_store_verify_receipt_event = apple_app_store_verify_receipt_event
        return self

    def with_google_play_verify_receipt_event(self, google_play_verify_receipt_event: GooglePlayVerifyReceiptEvent) -> VerifyReceiptEvent:
        self.google_play_verify_receipt_event = google_play_verify_receipt_event
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[VerifyReceiptEvent]:
        if data is None:
            return None
        return VerifyReceiptEvent()\
            .with_content_name(data.get('contentName'))\
            .with_platform(data.get('platform'))\
            .with_apple_app_store_verify_receipt_event(AppleAppStoreVerifyReceiptEvent.from_dict(data.get('appleAppStoreVerifyReceiptEvent')))\
            .with_google_play_verify_receipt_event(GooglePlayVerifyReceiptEvent.from_dict(data.get('googlePlayVerifyReceiptEvent')))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "contentName": self.content_name,
            "platform": self.platform,
            "appleAppStoreVerifyReceiptEvent": self.apple_app_store_verify_receipt_event.to_dict() if self.apple_app_store_verify_receipt_event else None,
            "googlePlayVerifyReceiptEvent": self.google_play_verify_receipt_event.to_dict() if self.google_play_verify_receipt_event else None,
        }


class DepositTransaction(core.Gs2Model):
    price: float = None
    currency: str = None
    count: int = None
    deposited_at: int = None

    def with_price(self, price: float) -> DepositTransaction:
        self.price = price
        return self

    def with_currency(self, currency: str) -> DepositTransaction:
        self.currency = currency
        return self

    def with_count(self, count: int) -> DepositTransaction:
        self.count = count
        return self

    def with_deposited_at(self, deposited_at: int) -> DepositTransaction:
        self.deposited_at = deposited_at
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[DepositTransaction]:
        if data is None:
            return None
        return DepositTransaction()\
            .with_price(data.get('price'))\
            .with_currency(data.get('currency'))\
            .with_count(data.get('count'))\
            .with_deposited_at(data.get('depositedAt'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "price": self.price,
            "currency": self.currency,
            "count": self.count,
            "depositedAt": self.deposited_at,
        }


class WalletSummary(core.Gs2Model):
    paid: int = None
    free: int = None
    total: int = None

    def with_paid(self, paid: int) -> WalletSummary:
        self.paid = paid
        return self

    def with_free(self, free: int) -> WalletSummary:
        self.free = free
        return self

    def with_total(self, total: int) -> WalletSummary:
        self.total = total
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[WalletSummary]:
        if data is None:
            return None
        return WalletSummary()\
            .with_paid(data.get('paid'))\
            .with_free(data.get('free'))\
            .with_total(data.get('total'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "paid": self.paid,
            "free": self.free,
            "total": self.total,
        }


class FakeSetting(core.Gs2Model):
    accept_fake_receipt: str = None

    def with_accept_fake_receipt(self, accept_fake_receipt: str) -> FakeSetting:
        self.accept_fake_receipt = accept_fake_receipt
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[FakeSetting]:
        if data is None:
            return None
        return FakeSetting()\
            .with_accept_fake_receipt(data.get('acceptFakeReceipt'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "acceptFakeReceipt": self.accept_fake_receipt,
        }


class GooglePlaySetting(core.Gs2Model):
    package_name: str = None
    public_key: str = None

    def with_package_name(self, package_name: str) -> GooglePlaySetting:
        self.package_name = package_name
        return self

    def with_public_key(self, public_key: str) -> GooglePlaySetting:
        self.public_key = public_key
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[GooglePlaySetting]:
        if data is None:
            return None
        return GooglePlaySetting()\
            .with_package_name(data.get('packageName'))\
            .with_public_key(data.get('publicKey'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "packageName": self.package_name,
            "publicKey": self.public_key,
        }


class AppleAppStoreSetting(core.Gs2Model):
    bundle_id: str = None

    def with_bundle_id(self, bundle_id: str) -> AppleAppStoreSetting:
        self.bundle_id = bundle_id
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[AppleAppStoreSetting]:
        if data is None:
            return None
        return AppleAppStoreSetting()\
            .with_bundle_id(data.get('bundleId'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bundleId": self.bundle_id,
        }


class PlatformSetting(core.Gs2Model):
    apple_app_store: AppleAppStoreSetting = None
    google_play: GooglePlaySetting = None
    fake: FakeSetting = None

    def with_apple_app_store(self, apple_app_store: AppleAppStoreSetting) -> PlatformSetting:
        self.apple_app_store = apple_app_store
        return self

    def with_google_play(self, google_play: GooglePlaySetting) -> PlatformSetting:
        self.google_play = google_play
        return self

    def with_fake(self, fake: FakeSetting) -> PlatformSetting:
        self.fake = fake
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[PlatformSetting]:
        if data is None:
            return None
        return PlatformSetting()\
            .with_apple_app_store(AppleAppStoreSetting.from_dict(data.get('appleAppStore')))\
            .with_google_play(GooglePlaySetting.from_dict(data.get('googlePlay')))\
            .with_fake(FakeSetting.from_dict(data.get('fake')))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "appleAppStore": self.apple_app_store.to_dict() if self.apple_app_store else None,
            "googlePlay": self.google_play.to_dict() if self.google_play else None,
            "fake": self.fake.to_dict() if self.fake else None,
        }


class Receipt(core.Gs2Model):
    store: str = None
    transaction_i_d: str = None
    payload: str = None

    def with_store(self, store: str) -> Receipt:
        self.store = store
        return self

    def with_transaction_i_d(self, transaction_i_d: str) -> Receipt:
        self.transaction_i_d = transaction_i_d
        return self

    def with_payload(self, payload: str) -> Receipt:
        self.payload = payload
        return self

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[Receipt]:
        if data is None:
            return None
        return Receipt()\
            .with_store(data.get('Store'))\
            .with_transaction_i_d(data.get('TransactionID'))\
            .with_payload(data.get('Payload'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Store": self.store,
            "TransactionID": self.transaction_i_d,
            "Payload": self.payload,
        }


class CurrentModelMaster(core.Gs2Model):
    namespace_id: str = None
    settings: str = None

    def with_namespace_id(self, namespace_id: str) -> CurrentModelMaster:
        self.namespace_id = namespace_id
        return self

    def with_settings(self, settings: str) -> CurrentModelMaster:
        self.settings = settings
        return self

    @classmethod
    def create_grn(
        cls,
        region,
        owner_id,
        namespace_name,
    ):
        return 'grn:gs2:{region}:{ownerId}:money2:{namespaceName}'.format(
            region=region,
            ownerId=owner_id,
            namespaceName=namespace_name,
        )

    @classmethod
    def get_region_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+)', grn)
        if match is None:
            return None
        return match.group('region')

    @classmethod
    def get_owner_id_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+)', grn)
        if match is None:
            return None
        return match.group('owner_id')

    @classmethod
    def get_namespace_name_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+)', grn)
        if match is None:
            return None
        return match.group('namespace_name')

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[CurrentModelMaster]:
        if data is None:
            return None
        return CurrentModelMaster()\
            .with_namespace_id(data.get('namespaceId'))\
            .with_settings(data.get('settings'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "namespaceId": self.namespace_id,
            "settings": self.settings,
        }


class StoreContentModelMaster(core.Gs2Model):
    store_content_model_id: str = None
    name: str = None
    description: str = None
    metadata: str = None
    apple_app_store: AppleAppStoreContent = None
    google_play: GooglePlayContent = None
    created_at: int = None
    updated_at: int = None
    revision: int = None

    def with_store_content_model_id(self, store_content_model_id: str) -> StoreContentModelMaster:
        self.store_content_model_id = store_content_model_id
        return self

    def with_name(self, name: str) -> StoreContentModelMaster:
        self.name = name
        return self

    def with_description(self, description: str) -> StoreContentModelMaster:
        self.description = description
        return self

    def with_metadata(self, metadata: str) -> StoreContentModelMaster:
        self.metadata = metadata
        return self

    def with_apple_app_store(self, apple_app_store: AppleAppStoreContent) -> StoreContentModelMaster:
        self.apple_app_store = apple_app_store
        return self

    def with_google_play(self, google_play: GooglePlayContent) -> StoreContentModelMaster:
        self.google_play = google_play
        return self

    def with_created_at(self, created_at: int) -> StoreContentModelMaster:
        self.created_at = created_at
        return self

    def with_updated_at(self, updated_at: int) -> StoreContentModelMaster:
        self.updated_at = updated_at
        return self

    def with_revision(self, revision: int) -> StoreContentModelMaster:
        self.revision = revision
        return self

    @classmethod
    def create_grn(
        cls,
        region,
        owner_id,
        namespace_name,
        content_name,
    ):
        return 'grn:gs2:{region}:{ownerId}:money2:{namespaceName}:master:content:{contentName}'.format(
            region=region,
            ownerId=owner_id,
            namespaceName=namespace_name,
            contentName=content_name,
        )

    @classmethod
    def get_region_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):master:content:(?P<contentName>.+)', grn)
        if match is None:
            return None
        return match.group('region')

    @classmethod
    def get_owner_id_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):master:content:(?P<contentName>.+)', grn)
        if match is None:
            return None
        return match.group('owner_id')

    @classmethod
    def get_namespace_name_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):master:content:(?P<contentName>.+)', grn)
        if match is None:
            return None
        return match.group('namespace_name')

    @classmethod
    def get_content_name_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):master:content:(?P<contentName>.+)', grn)
        if match is None:
            return None
        return match.group('content_name')

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[StoreContentModelMaster]:
        if data is None:
            return None
        return StoreContentModelMaster()\
            .with_store_content_model_id(data.get('storeContentModelId'))\
            .with_name(data.get('name'))\
            .with_description(data.get('description'))\
            .with_metadata(data.get('metadata'))\
            .with_apple_app_store(AppleAppStoreContent.from_dict(data.get('appleAppStore')))\
            .with_google_play(GooglePlayContent.from_dict(data.get('googlePlay')))\
            .with_created_at(data.get('createdAt'))\
            .with_updated_at(data.get('updatedAt'))\
            .with_revision(data.get('revision'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "storeContentModelId": self.store_content_model_id,
            "name": self.name,
            "description": self.description,
            "metadata": self.metadata,
            "appleAppStore": self.apple_app_store.to_dict() if self.apple_app_store else None,
            "googlePlay": self.google_play.to_dict() if self.google_play else None,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "revision": self.revision,
        }


class StoreContentModel(core.Gs2Model):
    store_content_model_id: str = None
    name: str = None
    metadata: str = None
    apple_app_store: AppleAppStoreContent = None
    google_play: GooglePlayContent = None

    def with_store_content_model_id(self, store_content_model_id: str) -> StoreContentModel:
        self.store_content_model_id = store_content_model_id
        return self

    def with_name(self, name: str) -> StoreContentModel:
        self.name = name
        return self

    def with_metadata(self, metadata: str) -> StoreContentModel:
        self.metadata = metadata
        return self

    def with_apple_app_store(self, apple_app_store: AppleAppStoreContent) -> StoreContentModel:
        self.apple_app_store = apple_app_store
        return self

    def with_google_play(self, google_play: GooglePlayContent) -> StoreContentModel:
        self.google_play = google_play
        return self

    @classmethod
    def create_grn(
        cls,
        region,
        owner_id,
        namespace_name,
        content_name,
    ):
        return 'grn:gs2:{region}:{ownerId}:money2:{namespaceName}:model:content:{contentName}'.format(
            region=region,
            ownerId=owner_id,
            namespaceName=namespace_name,
            contentName=content_name,
        )

    @classmethod
    def get_region_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):model:content:(?P<contentName>.+)', grn)
        if match is None:
            return None
        return match.group('region')

    @classmethod
    def get_owner_id_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):model:content:(?P<contentName>.+)', grn)
        if match is None:
            return None
        return match.group('owner_id')

    @classmethod
    def get_namespace_name_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):model:content:(?P<contentName>.+)', grn)
        if match is None:
            return None
        return match.group('namespace_name')

    @classmethod
    def get_content_name_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):model:content:(?P<contentName>.+)', grn)
        if match is None:
            return None
        return match.group('content_name')

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[StoreContentModel]:
        if data is None:
            return None
        return StoreContentModel()\
            .with_store_content_model_id(data.get('storeContentModelId'))\
            .with_name(data.get('name'))\
            .with_metadata(data.get('metadata'))\
            .with_apple_app_store(AppleAppStoreContent.from_dict(data.get('appleAppStore')))\
            .with_google_play(GooglePlayContent.from_dict(data.get('googlePlay')))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "storeContentModelId": self.store_content_model_id,
            "name": self.name,
            "metadata": self.metadata,
            "appleAppStore": self.apple_app_store.to_dict() if self.apple_app_store else None,
            "googlePlay": self.google_play.to_dict() if self.google_play else None,
        }


class Event(core.Gs2Model):
    event_id: str = None
    transaction_id: str = None
    user_id: str = None
    event_type: str = None
    verify_receipt_event: VerifyReceiptEvent = None
    deposit_event: DepositEvent = None
    withdraw_event: WithdrawEvent = None
    created_at: int = None
    revision: int = None

    def with_event_id(self, event_id: str) -> Event:
        self.event_id = event_id
        return self

    def with_transaction_id(self, transaction_id: str) -> Event:
        self.transaction_id = transaction_id
        return self

    def with_user_id(self, user_id: str) -> Event:
        self.user_id = user_id
        return self

    def with_event_type(self, event_type: str) -> Event:
        self.event_type = event_type
        return self

    def with_verify_receipt_event(self, verify_receipt_event: VerifyReceiptEvent) -> Event:
        self.verify_receipt_event = verify_receipt_event
        return self

    def with_deposit_event(self, deposit_event: DepositEvent) -> Event:
        self.deposit_event = deposit_event
        return self

    def with_withdraw_event(self, withdraw_event: WithdrawEvent) -> Event:
        self.withdraw_event = withdraw_event
        return self

    def with_created_at(self, created_at: int) -> Event:
        self.created_at = created_at
        return self

    def with_revision(self, revision: int) -> Event:
        self.revision = revision
        return self

    @classmethod
    def create_grn(
        cls,
        region,
        owner_id,
        namespace_name,
        transaction_id,
    ):
        return 'grn:gs2:{region}:{ownerId}:money2:{namespaceName}:event:{transactionId}'.format(
            region=region,
            ownerId=owner_id,
            namespaceName=namespace_name,
            transactionId=transaction_id,
        )

    @classmethod
    def get_region_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):event:(?P<transactionId>.+)', grn)
        if match is None:
            return None
        return match.group('region')

    @classmethod
    def get_owner_id_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):event:(?P<transactionId>.+)', grn)
        if match is None:
            return None
        return match.group('owner_id')

    @classmethod
    def get_namespace_name_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):event:(?P<transactionId>.+)', grn)
        if match is None:
            return None
        return match.group('namespace_name')

    @classmethod
    def get_transaction_id_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):event:(?P<transactionId>.+)', grn)
        if match is None:
            return None
        return match.group('transaction_id')

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[Event]:
        if data is None:
            return None
        return Event()\
            .with_event_id(data.get('eventId'))\
            .with_transaction_id(data.get('transactionId'))\
            .with_user_id(data.get('userId'))\
            .with_event_type(data.get('eventType'))\
            .with_verify_receipt_event(VerifyReceiptEvent.from_dict(data.get('verifyReceiptEvent')))\
            .with_deposit_event(DepositEvent.from_dict(data.get('depositEvent')))\
            .with_withdraw_event(WithdrawEvent.from_dict(data.get('withdrawEvent')))\
            .with_created_at(data.get('createdAt'))\
            .with_revision(data.get('revision'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "eventId": self.event_id,
            "transactionId": self.transaction_id,
            "userId": self.user_id,
            "eventType": self.event_type,
            "verifyReceiptEvent": self.verify_receipt_event.to_dict() if self.verify_receipt_event else None,
            "depositEvent": self.deposit_event.to_dict() if self.deposit_event else None,
            "withdrawEvent": self.withdraw_event.to_dict() if self.withdraw_event else None,
            "createdAt": self.created_at,
            "revision": self.revision,
        }


class Wallet(core.Gs2Model):
    wallet_id: str = None
    user_id: str = None
    slot: int = None
    summary: WalletSummary = None
    deposit_transactions: List[DepositTransaction] = None
    shared_free_currency: bool = None
    created_at: int = None
    updated_at: int = None
    revision: int = None

    def with_wallet_id(self, wallet_id: str) -> Wallet:
        self.wallet_id = wallet_id
        return self

    def with_user_id(self, user_id: str) -> Wallet:
        self.user_id = user_id
        return self

    def with_slot(self, slot: int) -> Wallet:
        self.slot = slot
        return self

    def with_summary(self, summary: WalletSummary) -> Wallet:
        self.summary = summary
        return self

    def with_deposit_transactions(self, deposit_transactions: List[DepositTransaction]) -> Wallet:
        self.deposit_transactions = deposit_transactions
        return self

    def with_shared_free_currency(self, shared_free_currency: bool) -> Wallet:
        self.shared_free_currency = shared_free_currency
        return self

    def with_created_at(self, created_at: int) -> Wallet:
        self.created_at = created_at
        return self

    def with_updated_at(self, updated_at: int) -> Wallet:
        self.updated_at = updated_at
        return self

    def with_revision(self, revision: int) -> Wallet:
        self.revision = revision
        return self

    @classmethod
    def create_grn(
        cls,
        region,
        owner_id,
        namespace_name,
        user_id,
        slot,
    ):
        return 'grn:gs2:{region}:{ownerId}:money2:{namespaceName}:user:{userId}:wallet:{slot}'.format(
            region=region,
            ownerId=owner_id,
            namespaceName=namespace_name,
            userId=user_id,
            slot=slot,
        )

    @classmethod
    def get_region_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):user:(?P<userId>.+):wallet:(?P<slot>.+)', grn)
        if match is None:
            return None
        return match.group('region')

    @classmethod
    def get_owner_id_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):user:(?P<userId>.+):wallet:(?P<slot>.+)', grn)
        if match is None:
            return None
        return match.group('owner_id')

    @classmethod
    def get_namespace_name_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):user:(?P<userId>.+):wallet:(?P<slot>.+)', grn)
        if match is None:
            return None
        return match.group('namespace_name')

    @classmethod
    def get_user_id_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):user:(?P<userId>.+):wallet:(?P<slot>.+)', grn)
        if match is None:
            return None
        return match.group('user_id')

    @classmethod
    def get_slot_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+):user:(?P<userId>.+):wallet:(?P<slot>.+)', grn)
        if match is None:
            return None
        return match.group('slot')

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[Wallet]:
        if data is None:
            return None
        return Wallet()\
            .with_wallet_id(data.get('walletId'))\
            .with_user_id(data.get('userId'))\
            .with_slot(data.get('slot'))\
            .with_summary(WalletSummary.from_dict(data.get('summary')))\
            .with_deposit_transactions(None if data.get('depositTransactions') is None else [
                DepositTransaction.from_dict(data.get('depositTransactions')[i])
                for i in range(len(data.get('depositTransactions')))
            ])\
            .with_shared_free_currency(data.get('sharedFreeCurrency'))\
            .with_created_at(data.get('createdAt'))\
            .with_updated_at(data.get('updatedAt'))\
            .with_revision(data.get('revision'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "walletId": self.wallet_id,
            "userId": self.user_id,
            "slot": self.slot,
            "summary": self.summary.to_dict() if self.summary else None,
            "depositTransactions": None if self.deposit_transactions is None else [
                self.deposit_transactions[i].to_dict() if self.deposit_transactions[i] else None
                for i in range(len(self.deposit_transactions))
            ],
            "sharedFreeCurrency": self.shared_free_currency,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "revision": self.revision,
        }


class Namespace(core.Gs2Model):
    namespace_id: str = None
    name: str = None
    description: str = None
    currency_usage_priority: str = None
    shared_free_currency: bool = None
    platform_setting: PlatformSetting = None
    deposit_balance_script: ScriptSetting = None
    withdraw_balance_script: ScriptSetting = None
    log_setting: LogSetting = None
    created_at: int = None
    updated_at: int = None
    revision: int = None

    def with_namespace_id(self, namespace_id: str) -> Namespace:
        self.namespace_id = namespace_id
        return self

    def with_name(self, name: str) -> Namespace:
        self.name = name
        return self

    def with_description(self, description: str) -> Namespace:
        self.description = description
        return self

    def with_currency_usage_priority(self, currency_usage_priority: str) -> Namespace:
        self.currency_usage_priority = currency_usage_priority
        return self

    def with_shared_free_currency(self, shared_free_currency: bool) -> Namespace:
        self.shared_free_currency = shared_free_currency
        return self

    def with_platform_setting(self, platform_setting: PlatformSetting) -> Namespace:
        self.platform_setting = platform_setting
        return self

    def with_deposit_balance_script(self, deposit_balance_script: ScriptSetting) -> Namespace:
        self.deposit_balance_script = deposit_balance_script
        return self

    def with_withdraw_balance_script(self, withdraw_balance_script: ScriptSetting) -> Namespace:
        self.withdraw_balance_script = withdraw_balance_script
        return self

    def with_log_setting(self, log_setting: LogSetting) -> Namespace:
        self.log_setting = log_setting
        return self

    def with_created_at(self, created_at: int) -> Namespace:
        self.created_at = created_at
        return self

    def with_updated_at(self, updated_at: int) -> Namespace:
        self.updated_at = updated_at
        return self

    def with_revision(self, revision: int) -> Namespace:
        self.revision = revision
        return self

    @classmethod
    def create_grn(
        cls,
        region,
        owner_id,
        namespace_name,
    ):
        return 'grn:gs2:{region}:{ownerId}:money2:{namespaceName}'.format(
            region=region,
            ownerId=owner_id,
            namespaceName=namespace_name,
        )

    @classmethod
    def get_region_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+)', grn)
        if match is None:
            return None
        return match.group('region')

    @classmethod
    def get_owner_id_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+)', grn)
        if match is None:
            return None
        return match.group('owner_id')

    @classmethod
    def get_namespace_name_from_grn(
        cls,
        grn: str,
    ) -> Optional[str]:
        match = re.search('grn:gs2:(?P<region>.+):(?P<ownerId>.+):money2:(?P<namespaceName>.+)', grn)
        if match is None:
            return None
        return match.group('namespace_name')

    def get(self, key, default=None):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return default

    def __getitem__(self, key):
        items = self.to_dict()
        if key in items.keys():
            return items[key]
        return None

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Optional[Namespace]:
        if data is None:
            return None
        return Namespace()\
            .with_namespace_id(data.get('namespaceId'))\
            .with_name(data.get('name'))\
            .with_description(data.get('description'))\
            .with_currency_usage_priority(data.get('currencyUsagePriority'))\
            .with_shared_free_currency(data.get('sharedFreeCurrency'))\
            .with_platform_setting(PlatformSetting.from_dict(data.get('platformSetting')))\
            .with_deposit_balance_script(ScriptSetting.from_dict(data.get('depositBalanceScript')))\
            .with_withdraw_balance_script(ScriptSetting.from_dict(data.get('withdrawBalanceScript')))\
            .with_log_setting(LogSetting.from_dict(data.get('logSetting')))\
            .with_created_at(data.get('createdAt'))\
            .with_updated_at(data.get('updatedAt'))\
            .with_revision(data.get('revision'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "namespaceId": self.namespace_id,
            "name": self.name,
            "description": self.description,
            "currencyUsagePriority": self.currency_usage_priority,
            "sharedFreeCurrency": self.shared_free_currency,
            "platformSetting": self.platform_setting.to_dict() if self.platform_setting else None,
            "depositBalanceScript": self.deposit_balance_script.to_dict() if self.deposit_balance_script else None,
            "withdrawBalanceScript": self.withdraw_balance_script.to_dict() if self.withdraw_balance_script else None,
            "logSetting": self.log_setting.to_dict() if self.log_setting else None,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "revision": self.revision,
        }