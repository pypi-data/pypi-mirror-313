from .preprod_tracing import record, connect


if __name__ == "__main__":
    connect()

__all__ = ['record', 'connect']