from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    cv_id: Mapped[int] = mapped_column(
        ForeignKey("cvs.id", ondelete="CASCADE"),
        nullable=False,
    )

    github_profile_id: Mapped[int] = mapped_column(
        ForeignKey("github_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(Text, nullable=False)
    missing_skills: Mapped[str] = mapped_column(Text, nullable=False)
    internship_email: Mapped[str] = mapped_column(Text, nullable=False)
    linkedin_message: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    user = relationship("User")
    cv = relationship("CV")
    github_profile = relationship("GitHubProfile")