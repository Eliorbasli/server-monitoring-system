from sqlalchemy.orm import declarative_base

Base = declarative_base()

def init_models():
    # Delayed imports to avoid circular dependency
    import app.models.server
    import app.models.status
