from database import Base, engine

# ⚠️ هشدار: این روش تمام جدول‌های موجود را حذف می‌کند!
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Database reset successfully!")
