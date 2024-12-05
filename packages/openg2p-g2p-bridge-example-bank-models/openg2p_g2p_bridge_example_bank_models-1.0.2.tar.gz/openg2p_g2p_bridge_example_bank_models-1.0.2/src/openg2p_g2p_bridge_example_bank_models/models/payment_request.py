from enum import Enum

from openg2p_fastapi_common.models import BaseORMModelWithTimes
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class FundBlock(BaseORMModelWithTimes):
    __tablename__ = "fund_blocks"
    block_reference_no: Mapped[str] = mapped_column(String, index=True, unique=True)
    account_number: Mapped[str] = mapped_column(String)
    currency: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    amount_released: Mapped[float] = mapped_column(Float, default=0)


class InitiatePaymentBatchRequest(BaseORMModelWithTimes):
    __tablename__ = "initiate_payment_batch_requests"
    batch_id: Mapped[str] = mapped_column(String, index=True, unique=True)
    payment_initiate_attempts: Mapped[int] = mapped_column(Integer, default=0)
    payment_status: Mapped[PaymentStatus] = mapped_column(
        SqlEnum(PaymentStatus), default=PaymentStatus.PENDING
    )


class InitiatePaymentRequest(BaseORMModelWithTimes):
    __tablename__ = "initiate_payment_requests"
    batch_id: Mapped[str] = mapped_column(String, index=True, unique=False)
    payment_reference_number = mapped_column(
        String, index=True, unique=True
    )  # disbursement id
    remitting_account: Mapped[str] = mapped_column(String, nullable=False)
    remitting_account_currency: Mapped[str] = mapped_column(String, nullable=False)
    payment_amount: Mapped[float] = mapped_column(Float, nullable=False)
    payment_date: Mapped[str] = mapped_column(String, nullable=False)
    funds_blocked_reference_number: Mapped[str] = mapped_column(String, nullable=False)

    beneficiary_name: Mapped[str] = mapped_column(String)
    beneficiary_account: Mapped[str] = mapped_column(String)
    beneficiary_account_currency: Mapped[str] = mapped_column(String)
    beneficiary_account_type: Mapped[str] = mapped_column(String)
    beneficiary_bank_code: Mapped[str] = mapped_column(String)
    beneficiary_branch_code: Mapped[str] = mapped_column(String)

    beneficiary_mobile_wallet_provider: Mapped[str] = mapped_column(
        String, nullable=True
    )
    beneficiary_phone_no: Mapped[str] = mapped_column(String, nullable=True)

    beneficiary_email: Mapped[str] = mapped_column(String, nullable=True)
    beneficiary_email_wallet_provider: Mapped[str] = mapped_column(
        String, nullable=True
    )

    narrative_1: Mapped[str] = mapped_column(
        String, nullable=True
    )  # disbursement narrative
    narrative_2: Mapped[str] = mapped_column(String, nullable=True)  # program pneumonic
    narrative_3: Mapped[str] = mapped_column(
        String, nullable=True
    )  # cycle code pneumonic
    narrative_4: Mapped[str] = mapped_column(String, nullable=True)  # beneficiary id
    narrative_5: Mapped[str] = mapped_column(String, nullable=True)
    narrative_6: Mapped[str] = mapped_column(String, nullable=True)
