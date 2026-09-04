"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-09-04

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String, unique=True, index=True, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("vertical", sa.String, nullable=False),
        sa.Column("password_hash", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "characters",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("vertical", sa.String, index=True, nullable=False),
        sa.Column("system_prompt", sa.Text, nullable=False),
        sa.Column("voice_id", sa.String, nullable=False),
    )

    op.create_table(
        "sessions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("character_id", UUID(as_uuid=True), sa.ForeignKey("characters.id"), nullable=False),
        sa.Column("started_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "messages",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("session_id", UUID(as_uuid=True), sa.ForeignKey("sessions.id"), nullable=False),
        sa.Column("role", sa.String, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "memory_facts",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("character_id", UUID(as_uuid=True), sa.ForeignKey("characters.id"), nullable=False),
        sa.Column("fact_text", sa.Text, nullable=False),
        sa.Column("embedding", Vector(1536), nullable=False),
    )

    op.create_table(
        "progress",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("vertical", sa.String, nullable=False),
        sa.Column("metric_json", JSONB, server_default="{}"),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("progress")
    op.drop_table("memory_facts")
    op.drop_table("messages")
    op.drop_table("sessions")
    op.drop_table("characters")
    op.drop_table("users")
